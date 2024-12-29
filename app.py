from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from database import init_db, create_admin, save_record, register_user, verify_user, save_results
from nlp_processor import NLPProcessor

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置会话密钥

nlp_processor = NLPProcessor()
init_db()
create_admin()  # 创建管理员用户

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session.get('role') == 'admin':
        return redirect(url_for('admin'))
    questions = nlp_processor.get_questions()
    session['questions'] = questions
    return render_template('index.html', questions=questions, username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = verify_user(username, password)
        if user:
            session['username'] = username
            session['role'] = user[3]
            if user[3] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            return "用户名或密码错误"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            return redirect(url_for('login'))
        else:
            return "用户名已存在"
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('login'))
    questions = session.get('questions', [])
    answers = []
    for i, question in enumerate(questions):
        if question["type"] == "multiple_choice":
            answers.append(request.form.getlist(f'answer_{i+1}', []))
        else:
            answers.append(request.form.get(f'answer_{i+1}', ''))
    score, results = nlp_processor.evaluate_answers(answers)
    save_record(session['username'], score)
    save_results(session['username'], results)
    return render_template('results.html', username=session['username'], score=score, total=len(questions), results=results)

@app.route('/admin')
def admin():
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = sqlite3.connect('safety_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM records")
    records = c.fetchall()

    # 获取题目正确率分析
    c.execute("""
        SELECT question, 
               SUM(is_correct) as correct_count, 
               COUNT(*) as total 
        FROM results 
        GROUP BY question
    """)
    accuracy = c.fetchall()

    # 获取每个题目的错误答案（仅针对简答题）
    c.execute("""
        SELECT question, user_answer 
        FROM results 
        WHERE is_correct = 0
    """)
    incorrect_answers = c.fetchall()
    conn.close()

    # 将错误答案按题目分组
    question_incorrect_answers = {}
    for item in incorrect_answers:
        question = item[0]
        user_answer = item[1]
        if question not in question_incorrect_answers:
            question_incorrect_answers[question] = []
        question_incorrect_answers[question].append(user_answer)

    # 获取每个题目的正确答案、选项和类型
    question_correct_answers = {}
    question_options = {}
    question_types = {}
    for question in nlp_processor.all_questions:
        question_correct_answers[question['question']] = question['answer']
        if 'options' in question:  # 如果是单选题，保存选项
            question_options[question['question']] = question['options']
        question_types[question['question']] = question['type']  # 保存题目类型

    # 计算正确率
    accuracy_with_answers = []
    for item in accuracy:
        question = item[0]
        correct_count = item[1]
        total = item[2]
        correct_rate = (correct_count / total) * 100 if total > 0 else 0
        correct_answer = question_correct_answers.get(question, 'N/A')
        incorrect_answers = question_incorrect_answers.get(question, ['无'])  # 如果没有错误答案，显示为“无”
        options = question_options.get(question, [])  # 获取单选题的选项
        question_type = question_types.get(question, 'N/A')  # 获取题目类型
        accuracy_with_answers.append({
            'question': question,
            'correct_answer': correct_answer,
            'incorrect_answers': incorrect_answers,  # 多个错误答案
            'correct_rate': correct_rate,
            'options': options,  # 添加选项字段
            'type': question_type  # 添加题目类型字段
        })

    return render_template('admin.html', records=records, accuracy=accuracy_with_answers, username=session['username'])
@app.route('/safety_manual')
def safety_manual():
    return render_template('safety_manual.html')
if __name__ == '__main__':
    app.run(debug=True)