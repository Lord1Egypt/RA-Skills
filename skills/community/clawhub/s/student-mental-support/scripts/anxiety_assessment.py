#!/usr/bin/env python3
"""
焦虑评估问卷生成器
用于评估大学生就业焦虑程度
"""

def generate_assessment_questions(user_data=None):
    """
    生成个性化的焦虑评估问卷
    
    Parameters:
    user_data: dict, 用户基本信息（可选）
    """
    
    questions = []
    
    # 基本信息（如果提供）
    if user_data:
        print(f"个人信息：")
        print(f"  - 专业：{user_data.get('major', '未提供')}")
        print(f"  - 年级：{user_data.get('grade', '未提供')}")
        print(f"  - 求职状态：{user_data.get('job_search_status', '未提供')}")
        print()
    
    # 焦虑评估问卷
    print("请评估以下情况对你的影响程度（1-5分）：")
    print("1 = 几乎没有影响，2 = 有一点影响，3 = 中等影响，4 = 较大影响，5 = 严重影响")
    print()
    
    questions.append({
        "id": "q1",
        "question": "你最近对找不到工作的担心程度",
        "category": "就业焦虑",
        "explanation": "反映对未来就业前景的担忧程度"
    })
    
    questions.append({
        "id": "q2",
        "question": "面试或求职过程中的紧张程度",
        "category": "面试压力",
        "explanation": "反映求职过程中的人际互动压力"
    })
    
    questions.append({
        "id": "q3",
        "question": "家庭和社会期望对你造成的压力程度",
        "category": "社会压力",
        "explanation": "反映外部期望带来的压力"
    })
    
    questions.append({
        "id": "q4",
        "question": "自我要求和成就期望的压力程度",
        "category": "自我压力",
        "explanation": "反映自我内部标准带来的压力"
    })
    
    questions.append({
        "id": "q5",
        "question": "经济压力和生存担忧的程度",
        "category": "经济压力",
        "explanation": "反映经济方面的担忧"
    })
    
    questions.append({
        "id": "q6",
        "question": "睡眠质量受到影响的程度",
        "category": "生理症状",
        "explanation": "反映压力对生理健康的影响"
    })
    
    questions.append({
        "id": "q7",
        "question": "食欲受到影响的程度",
        "category": "生理症状",
        "explanation": "反映压力对饮食的影响"
    })
    
    questions.append({
        "id": "q8",
        "question": "日常生活和工作效率受影响程度",
        "category": "功能影响",
        "explanation": "反映压力对日常功能的影响"
    })
    
    # 打印问卷
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q['question']} ({q['category']})")
        print(f"   解释：{q['explanation']}")
        print()
    
    # 评估说明
    print("\n评估说明：")
    print("总分评估标准：")
    print("  - 8-20分：轻度焦虑，建议使用自助减压方法")
    print("  - 21-35分：中度焦虑，建议结合专业指导和自助")
    print("  - 36-40分：重度焦虑，建议寻求专业心理咨询")
    
    return questions

def calculate_score(answers):
    """
    计算问卷总分
    
    Parameters:
    answers: dict, 问题ID -> 得分 (1-5)
    """
    if not answers:
        return 0
    
    total_score = sum(answers.values())
    return total_score

def interpret_score(total_score):
    """
    解释总分并提供建议
    
    Parameters:
    total_score: int, 问卷总分
    """
    interpretation = {}
    
    if total_score <= 20:
        interpretation['level'] = "轻度焦虑"
        interpretation['description'] = "压力在正常范围内，可通过自助方法缓解"
        interpretation['recommendations'] = [
            "每天进行深呼吸练习",
            "保持规律的作息时间",
            "适当运动缓解压力",
            "寻求朋友和家人支持"
        ]
        
    elif total_score <= 35:
        interpretation['level'] = "中度焦虑"
        interpretation['description'] = "压力已经影响日常生活，需要系统减压方法"
        interpretation['recommendations'] = [
            "结合自助和专业指导",
            "制定减压计划和时间管理",
            "考虑心理咨询支持",
            "学习正念冥想技巧"
        ]
        
    else:
        interpretation['level'] = "重度焦虑"
        interpretation['description'] = "压力严重影响身心健康，需要专业干预"
        interpretation['recommendations'] = [
            "立即寻求专业心理咨询",
            "联系学校心理中心",
            "考虑心理热线支持",
            "必要时寻求医疗帮助"
        ]
    
    return interpretation

if __name__ == "__main__":
    # 示例用户数据
    user_data = {
        "major": "计算机科学",
        "grade": "四年级",
        "job_search_status": "正在投递简历"
    }
    
    # 生成问卷
    questions = generate_assessment_questions(user_data)
    
    # 示例答案
    answers = {
        "q1": 4,
        "q2": 5,
        "q3": 3,
        "q4": 4,
        "q5": 2,
        "q6": 3,
        "q7": 2,
        "q8": 3
    }
    
    # 计算分数
    score = calculate_score(answers)
    interpretation = interpret_score(score)
    
    print(f"\n问卷总分：{score}")
    print(f"焦虑等级：{interpretation['level']}")
    print(f"描述：{interpretation['description']}")
    print(f"建议：")
    for rec in interpretation['recommendations']:
        print(f"  - {rec}")