#!/usr/bin/env python3
"""
六爻八卦算命脚本
根据出生年月日计算命理
"""

# 八卦数据
BAGUA = {
    '乾': {'symbol': '☰', 'element': '金', 'direction': '西北', 'traits': '刚健、积极、果断'},
    '兑': {'symbol': '☱', 'element': '金', 'direction': '西', 'traits': '口才、愉悦、灵活'},
    '离': {'symbol': '☲', 'element': '火', 'direction': '南', 'traits': '热情、创意、显眼'},
    '震': {'symbol': '☳', 'element': '木', 'direction': '东', 'traits': '行动、活力、冲动'},
    '巽': {'symbol': '☴', 'element': '木', 'direction': '东南', 'traits': '柔顺、谦逊、灵活'},
    '坎': {'symbol': '☵', 'element': '水', 'direction': '北', 'traits': '智慧、深沉、阴柔'},
    '艮': {'symbol': '☶', 'element': '土', 'direction': '东北', 'traits': '稳定、保守、固执'},
    '坤': {'symbol': '☷', 'element': '土', 'direction': '西南', 'traits': '包容、厚德、柔顺'},
}

# 八卦顺序（先天八卦）
BAGUA_ORDER = ['乾', '兑', '离', '震', '巽', '坎', '艮', '坤']

# 时辰对应
SHICHEN = {
    '子时': 23, '丑时': 1, '寅时': 3, '卯时': 5,
    '辰时': 7, '巳时': 9, '午时': 11, '未时': 13,
    '申时': 15, '酉时': 17, '戌时': 19, '亥时': 21
}

def calculate_bagua(year: int, month: int, day: int, hour: int = None) -> dict:
    """计算八卦命理"""
    
    # 计算年干支（简化版）
    stem_index = (year - 4) % 10
    branch_index = (year - 4) % 12
    stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    gan = stems[stem_index]
    zhi = branches[branch_index]
    
    # 确定主卦（根据年份奇偶和数字和）
    year_parity = year % 2
    digit_sum = sum(int(d) for d in str(year)) + sum(int(d) for d in str(month)) + sum(int(d) for d in str(day))
    if hour:
        digit_sum += hour
    
    # 选卦逻辑
    if year_parity == 1:  # 奇数年
        idx = (digit_sum + month) % 8
    else:  # 偶数年
        idx = (digit_sum + day) % 8
    
    main_gua = BAGUA_ORDER[idx]
    gua_info = BAGUA[main_gua]
    
    # 副卦（根据时辰或随机）
    if hour:
        sub_idx = (hour + month) % 8
    else:
        sub_idx = (day + month) % 8
    sub_gua = BAGUA_ORDER[sub_idx]
    sub_info = BAGUA[sub_gua]
    
    return {
        'year': year,
        'month': month,
        'day': day,
        'hour': hour,
        'ganzhi': f"{gan}{zhi}",
        'main_gua': main_gua,
        'main_info': gua_info,
        'sub_gua': sub_gua,
        'sub_info': sub_info,
    }

def generate_analysis(data: dict) -> str:
    """生成命理分析"""
    gua = data['main_gua']
    info = data['main_info']
    
    # 五行生克分析
    element = info['element']
    direction = info['direction']
    traits = info['traits']
    
    # 性格分析
    personality = get_personality_analysis(element, traits)
    
    # 运势分析
    career = get_career_analysis(element)
    wealth = get_wealth_analysis(element)
    love = get_love_analysis(element)
    health = get_health_analysis(element)
    
    result = f"""🎯 六爻八卦命理分析

📅 生辰：{data['year']}年{data['month']}月{data['day']}日
🌟 年干支：{data['ganzhi']}
🌞 主卦：{gua}卦（{info['symbol']}）
   五行属{info['element']}，位于{info['direction']}

💫 命理解读：
{personality}

📊 运势预测：
🎯 事业：{career}
💰 财运：{wealth}
💕 感情：{love}
🏥 健康：{health}

⚠️ 温馨提示：本分析仅供娱乐参考，人生掌握在自己手中！"""
    
    return result

def get_personality_analysis(element: str, traits: str) -> str:
    analyses = {
        '金': f"你命中属金，性格刚毅果断，具有领导气质。天生具有{traits}的特点，善于把握时机，思维敏捷。但需注意过于刚硬易折，建议学会变通。",
        '木': f"你命中属木，生机勃勃，积极向上。天生具有{traits}的特点，为人正直仁慈，有较强的成长潜力。但需注意情绪波动，学会稳重。",
        '水': f"你命中属水，智慧深沉，性情柔和。天生具有{traits}的特点，擅长思考洞察力强。但需避免过于敏感内耗，保持积极心态。",
        '火': f"你命中属火，热情洋溢，活力四射。天生具有{traits}的特点，执行力强敢于表现。但需注意控制脾气，避免冲动。",
        '土': f"你命中属土，稳重厚道，为人踏实。天生具有{traits}的特点，值得信赖有耐心。但需注意过于保守，要敢于尝试新事物。"
    }
    return analyses.get(element, traits)

def get_career_analysis(element: str) -> str:
    analyses = {
        '金': "适合从事金融、法律、管理等需要决断力的行业。有领导才能，适合创业或担任管理岗位。",
        '木': "适合教育、文化、艺术、设计等需要创造力的行业。适合发展自己的兴趣特长。",
        '水': "适合咨询、研究、技术、策划等需要思考的行业。适合幕后工作或专业技术岗位。",
        '火': "适合销售、演艺、媒体、餐饮等需要表现力的行业。适合抛头露面的工作。",
        '土': "适合建筑、农业、房产、服务等需要稳定性的行业。适合长期发展的事业。"
    }
    return analyses.get(element, "有广阔的发展空间")

def get_wealth_analysis(element: str) -> str:
    analyses = {
        '金': "财运较好，有较强的理财观念。但切忌贪心，注意守财。适合稳健投资。",
        '木': "财运平稳，需通过努力积累财富。建议培养理财习惯，中长期投资更有利。",
        '水': "财运有一定波动，但智慧生财。适合知识付费或技术服务类收入。",
        '火': "财运来去较快，需注意理财规划。建议储存备用金，避免冲动消费。",
        '土': "财运稳定，但上升需要时间。适合不动产投资或长期储蓄。"
    }
    return analyses.get(element, "财运平稳")

def get_love_analysis(element: str) -> str:
    analyses = {
        '金': "对待感情认真负责，但有时过于理性。遇到对的人要主动把握。",
        '木': "在感情中真诚主动，但需注意控制情绪。适合日久生情的模式。",
        '水': "追求精神层面的契合，对感情较为挑剔。遇到缘分要勇敢表达。",
        '火': "热情主动，但有时冲动。在感情中要学会倾听和理解。",
        '土': "对待感情专一长情，但表达较为含蓄。需要主动制造浪漫惊喜。"
    }
    return analyses.get(element, "真诚对待即可收获好姻缘")

def get_health_analysis(element: str) -> str:
    analyses = {
        '金': "注意肺部及呼吸系统健康。少抽烟，多做有氧运动。",
        '木': "注意肝胆健康，保持规律作息。不要熬夜伤肝。",
        '水': "注意肾脏及泌尿系统健康。多喝水，注意保暖。",
        '火': "注意心脏及血液循环。保持平和心态，避免过度激动。",
        '土': "注意脾胃健康。规律饮食，适量运动助消化。"
    }
    return analyses.get(element, "保持良好生活习惯即可")

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 4:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
        hour = int(sys.argv[4]) if len(sys.argv) > 4 else None
        
        data = calculate_bagua(year, month, day, hour)
        print(generate_analysis(data))
    else:
        print("用法: python liuyao.py 年 月 日 [时辰]")
