import random
from sentence_transformers import SentenceTransformer, util
class NLPProcessor:
    def __init__(self):
        # 所有题目
        self.all_questions = [
            {
                "question": "以下哪种情况表明个人防护装备可能需要更换？",
                "type": "single_choice",
                "options": ["A. 安全帽出现裂痕", "B. 防滑靴鞋底磨损严重", "C. 耳罩无法有效隔绝噪音", "D. 以上都是"],
                "answer": "D",
                "explanation": "个人防护装备出现任何损坏都应及时更换，以确保安全。"
            },
            {
                "question": "工人需定期检查个人防护装备，发现损坏应______。",
                "type": "short_answer",
                "answer": "立即更换",
                "explanation": "发现损坏应立即更换，以避免安全隐患。"
            },
            {
                "question": "如果发现同事未佩戴安全帽，应该如何处理？",
                "type": "short_answer",
                "answer": "提醒对方佩戴，并向主管报告，确保安全规范得到执行。",
                "explanation": "及时提醒和报告是确保工地安全的重要措施。"
            },
            {
                "question": "未经许可操作设备的后果包括以下哪项？",
                "type": "single_choice",
                "options": ["A. 增加事故风险", "B. 违反安全规定", "C. 可能导致设备损坏", "D. 以上都是"],
                "answer": "D",
                "explanation": "未经许可操作设备会带来多种安全隐患。"
            },
            {
                "question": "工地上所有人员必须遵守______标志和指示牌。",
                "type": "short_answer",
                "answer": "警示",
                "explanation": "遵守警示标志是确保工地安全的基本要求。"
            },
            {
                "question": "列举两种常见的工地危险行为。",
                "type": "short_answer",
                "answer": "奔跑或追逐打闹、在未授权区域操作设备。",
                "explanation": "这些行为可能导致严重的安全事故。"
            },
            {
                "question": "以下哪项不是安全培训的内容？",
                "type": "single_choice",
                "options": ["A. 紧急逃生路线熟悉", "B. 工地设备操作指南", "C. 个人绩效评估", "D. 应急事故处理培训"],
                "answer": "C",
                "explanation": "个人绩效评估不属于安全培训的内容。"
            },
            {
                "question": "安全演习的目的是提高工人对______的应对能力。",
                "type": "short_answer",
                "answer": "突发事故",
                "explanation": "安全演习有助于提高工人的应急处理能力。"
            },
            {
                "question": "为什么安全培训是工地工作的必要环节？",
                "type": "short_answer",
                "answer": "确保工人了解基本安全知识，减少事故发生率，提高应急处理能力。",
                "explanation": "安全培训是保障工地安全的基础。"
            },
            {
                "question": "进行高空作业时，以下哪项行为是错误的？",
                "type": "single_choice",
                "options": ["A. 确认安全绳索稳固", "B. 单独作业", "C. 设置警戒线", "D. 作业前检查平台稳固性"],
                "answer": "B",
                "explanation": "高空作业时不应单独作业，以确保安全。"
            },
            {
                "question": "高空作业区域周围需设置______以防无关人员进入。",
                "type": "short_answer",
                "answer": "安全标志",
                "explanation": "设置安全标志是防止无关人员进入的重要措施。"
            },
            {
                "question": "高空作业中，风速超过6级时为什么必须停止作业？",
                "type": "short_answer",
                "answer": "风速过大会增加坠落风险，影响安全操作。",
                "explanation": "风速过大会对高空作业安全造成严重影响。"
            },
            {
                "question": "发现电缆破损时，应如何处理？",
                "type": "single_choice",
                "options": ["A. 立即停止使用并报告主管", "B. 用胶带临时缠绕后继续使用", "C. 无需处理，正常使用",
                            "D. 直接剪断电缆"],
                "answer": "A",
                "explanation": "电缆破损应立即停止使用并报告，以避免触电事故。"
            },
            {
                "question": "电动工具的______必须完好无损，并确保接地良好。",
                "type": "short_answer",
                "answer": "电源线",
                "explanation": "电源线完好无损是确保电动工具安全使用的前提。"
            },
            {
                "question": "列举两种工地常见的电气安全隐患及其后果。",
                "type": "short_answer",
                "answer": "电缆老化（可能导致触电），接地不良（可能引发电击事故）。",
                "explanation": "电气安全隐患可能导致严重的安全事故。"
            },
            {
                "question": "机械设备在操作前检查的重点包括：",
                "type": "single_choice",
                "options": ["A. 外观检查是否损坏", "B. 运行状态是否正常", "C. 紧固件是否松动", "D. 以上都是"],
                "answer": "D",
                "explanation": "操作前应全面检查机械设备，确保安全。"
            },
            {
                "question": "机械设备发生故障时，应立即______并报告专业人员。",
                "type": "short_answer",
                "answer": "停止使用",
                "explanation": "发生故障时应立即停止使用，以避免进一步损坏或事故。"
            },
            {
                "question": "非专业人员操作机械设备可能会导致哪些后果？",
                "type": "short_answer",
                "answer": "设备损坏、工人受伤、影响正常施工。",
                "explanation": "非专业人员操作设备会带来多种安全隐患。"
            },
            {
                "question": "以下哪项是发现安全隐患后的正确处理方式？",
                "type": "single_choice",
                "options": ["A. 立即整改并报告主管", "B. 无需整改，忽略即可", "C. 自行决定是否整改",
                            "D. 延迟到项目结束后处理"],
                "answer": "A",
                "explanation": "发现安全隐患后应立即整改并报告，以确保安全。"
            },
            {
                "question": "发现事故隐患后，应及时填写______以记录详情并追踪处理情况。",
                "type": "short_answer",
                "answer": "事故报告单",
                "explanation": "填写事故报告单是追踪和处理隐患的重要步骤。"
            },
            {
                "question": "为什么安全记录对工地管理至关重要？",
                "type": "short_answer",
                "answer": "安全记录有助于追踪安全隐患、优化管理流程、提升安全措施的有效性。",
                "explanation": "安全记录是工地管理的重要组成部分。"
            },
            {
                "question": "以下哪项是进入工地时必备的个人防护装备？",
                "type": "single_choice",
                "options": ["A. 安全帽", "B. 护目镜", "C. 防滑靴", "D. 以上都是"],
                "answer": "D",
                "explanation": "安全帽、护目镜和防滑靴都是进入工地时必备的个人防护装备。"
            },
            {
                "question": "高空作业时，必须佩戴______并确保其固定牢靠。",
                "type": "short_answer",
                "answer": "安全带",
                "explanation": "安全带是高空作业时必备的安全装备，确保工人不会坠落。"
            },
            {
                "question": "列举三种工作场景下可能需要佩戴的防护装备。",
                "type": "short_answer",
                "answer": "耳罩（高噪音）、呼吸面罩（粉尘或有毒环境）、防滑靴（湿滑地面）。",
                "explanation": "不同的工作场景需要佩戴不同的防护装备以确保安全。"
            },
            {
                "question": "以下哪种行为违反了工地安全规则？",
                "type": "single_choice",
                "options": ["A. 遵守警示标志", "B. 未经许可操作机械设备", "C. 佩戴安全帽", "D. 遵守指示牌"],
                "answer": "B",
                "explanation": "未经许可操作机械设备是违反工地安全规则的行为。"
            },
            {
                "question": "禁止饮酒或服用______后进入工地。",
                "type": "short_answer",
                "answer": "影响判断力的药物",
                "explanation": "饮酒或服用影响判断力的药物会降低工人的安全意识，增加事故风险。"
            },
            {
                "question": "为什么工地上禁止奔跑或追逐打闹？",
                "type": "short_answer",
                "answer": "避免因不注意安全导致意外事故或受伤。",
                "explanation": "奔跑或追逐打闹会增加工地上的安全风险。"
            },
            {
                "question": "新入职员工必须接受以下哪种培训？",
                "type": "single_choice",
                "options": ["A. 技能培训", "B. 安全培训", "C. 财务培训", "D. 行政培训"],
                "answer": "B",
                "explanation": "新入职员工必须接受安全培训，以确保他们了解工地的安全规范。"
            },
            {
                "question": "定期参与______演练可以提高应对突发事故的能力。",
                "type": "short_answer",
                "answer": "安全演习（火灾逃生演练等）",
                "explanation": "定期参与安全演习可以提高工人的应急处理能力。"
            },
            {
                "question": "列举两种常见的工地安全演习内容。",
                "type": "short_answer",
                "answer": "火灾逃生演练、急救培训。",
                "explanation": "火灾逃生演练和急救培训是常见的工地安全演习内容。"
            },
            {
                "question": "高空作业时，以下哪种行为是正确的？",
                "type": "single_choice",
                "options": ["A. 单独作业", "B. 不佩戴安全绳", "C. 检查平台稳固后作业", "D. 不设置安全标志"],
                "answer": "C",
                "explanation": "高空作业时应检查平台稳固性，确保安全。"
            },
            {
                "question": "风速超过______级时，禁止进行高空作业。",
                "type": "short_answer",
                "answer": "6",
                "explanation": "风速超过6级时，高空作业的风险大大增加，必须停止作业。"
            },
            {
                "question": "高空作业为什么禁止单独操作？",
                "type": "short_answer",
                "answer": "为了确保有人及时应对突发情况，避免意外伤害。",
                "explanation": "高空作业时禁止单独操作，以确保有他人协助应对突发情况。"
            },
            {
                "question": "使用电动工具时，必须确保以下哪项条件？",
                "type": "single_choice",
                "options": ["A. 电源线无破损", "B. 工具接地良好", "C. 工具在保修期内", "D. A 和 B"],
                "answer": "D",
                "explanation": "使用电动工具时必须确保电源线无破损且工具接地良好。"
            },
            {
                "question": "触电事故发生时，第一步是______。",
                "type": "short_answer",
                "answer": "立即断电",
                "explanation": "触电事故发生时，第一步是立即断电，以防止进一步伤害。"
            },
            {
                "question": "为什么非专业电工不得从事电力操作或维修工作？",
                "type": "short_answer",
                "answer": "电力操作具有高风险，非专业人员可能因不熟悉操作导致事故或触电。",
                "explanation": "电力操作需要专业知识，非专业人员操作可能导致严重事故。"
            },
            {
                "question": "以下哪项属于机械设备作业前的检查内容？",
                "type": "single_choice",
                "options": ["A. 设备是否正常运行", "B. 设备是否定期维护", "C. 紧固件是否松动", "D. 以上都是"],
                "answer": "D",
                "explanation": "机械设备作业前应检查设备是否正常运行、是否定期维护以及紧固件是否松动。"
            },
            {
                "question": "机械设备作业区域内，禁止______人员靠近。",
                "type": "short_answer",
                "answer": "闲杂",
                "explanation": "机械设备作业区域内禁止闲杂人员靠近，以确保安全。"
            },
            {
                "question": "发现机械设备故障时应该如何处理？",
                "type": "short_answer",
                "answer": "立即停机，保护现场，通知专业人员进行检查维修。",
                "explanation": "发现机械设备故障时应立即停机并通知专业人员处理。"
            },
            {
                "question": "以下哪项是工地消防的必备措施？",
                "type": "single_choice",
                "options": ["A. 配备足够数量的灭火器", "B. 工人必须会使用灭火器", "C. 熟悉工地逃生路线", "D. 以上都是"],
                "answer": "D",
                "explanation": "工地消防的必备措施包括配备灭火器、培训工人使用灭火器以及熟悉逃生路线。"
            },
            {
                "question": "焊接作业前，必须严格执行______措施。",
                "type": "short_answer",
                "answer": "防火",
                "explanation": "焊接作业前必须严格执行防火措施，以防止火灾发生。"
            },
            {
                "question": "列举两种常见的工地火灾隐患。",
                "type": "short_answer",
                "answer": "易燃物品存放不当，电缆线路老化或私拉乱接。",
                "explanation": "易燃物品存放不当和电缆线路老化是常见的工地火灾隐患。"
            },
            {
                "question": "处理化学品时，以下哪项是正确的？",
                "type": "single_choice",
                "options": ["A. 戴上防护手套", "B. 化学品容器保持密封", "C. 在通风良好的区域操作", "D. 以上都是"],
                "answer": "D",
                "explanation": "处理化学品时应戴上防护手套、保持容器密封并在通风良好的区域操作。"
            },
            {
                "question": "所有化学品必须存放在______位置。",
                "type": "short_answer",
                "answer": "指定",
                "explanation": "化学品必须存放在指定位置，以确保安全。"
            },
            {
                "question": "为什么化学品泄漏时必须按应急程序操作？",
                "type": "short_answer",
                "answer": "避免扩散和人员受害，快速控制事态并减少损失。",
                "explanation": "化学品泄漏时必须按应急程序操作，以防止事态扩大。"
            },
            {
                "question": "发生火灾时，以下哪项行为是错误的？",
                "type": "single_choice",
                "options": ["A. 使用灭火器扑灭初期火势", "B. 立即报警拨打119", "C. 留在火场抢救财物",
                            "D. 撤离火场到安全区域"],
                "answer": "C",
                "explanation": "发生火灾时不应留在火场抢救财物，应立即撤离到安全区域。"
            },
            {
                "question": "发生事故后，应立即报告______并启动应急程序。",
                "type": "short_answer",
                "answer": "主管",
                "explanation": "发生事故后应立即报告主管并启动应急程序。"
            },
            {
                "question": "列举三种工地常见的紧急情况。",
                "type": "short_answer",
                "answer": "火灾、机械故障、人员受伤。",
                "explanation": "火灾、机械故障和人员受伤是工地常见的紧急情况。"
            },
            {
                "question": "以下哪项行为符合工地卫生要求？",
                "type": "single_choice",
                "options": ["A. 在工地随地乱扔垃圾", "B. 保持个人清洁卫生", "C. 不遵守饮食卫生规定", "D. 上岗前未洗手"],
                "answer": "B",
                "explanation": "保持个人清洁卫生是符合工地卫生要求的行为。"
            },
            {
                "question": "高温作业时，注意______以防中暑。",
                "type": "short_answer",
                "answer": "饮水和休息",
                "explanation": "高温作业时应注意饮水和休息，以防止中暑。"
            },
            {
                "question": "感到身体不适时，工人应该如何处理？",
                "type": "short_answer",
                "answer": "及时就医并向管理层报告，以防进一步恶化或传染他人。",
                "explanation": "感到身体不适时应及时就医并报告管理层，以确保健康和安全。"
            }
        ]
        self.questions = []  # 存储当前用户的问题列表
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # 加载预训练的语义相似度模型

    def get_questions(self):
        self.questions = random.sample(self.all_questions, 10)
        return self.questions

    def evaluate_answers(self, answers):
        score = 0
        results = []
        for i, answer in enumerate(answers):
            question = self.questions[i]
            if question["type"] == "single_choice":
                user_answer = answer.strip().upper() if answer else ""
                correct_answer = question["answer"].strip().upper()
                is_correct = (user_answer == correct_answer)
            elif question["type"] == "short_answer":
                # 计算语义相似度
                user_answer_embedding = self.model.encode(answer.strip().lower())
                correct_answer_embedding = self.model.encode(question["answer"].strip().lower())
                similarity = util.cos_sim(user_answer_embedding, correct_answer_embedding).item()
                is_correct = (similarity > 0.8)  # 设置相似度阈值
            if is_correct:
                score += 1
            results.append({
                "question": question["question"],
                "user_answer": answer if answer else "未作答",
                "correct_answer": question["answer"],
                "explanation": question["explanation"],
                "is_correct": is_correct
            })
        return score, results