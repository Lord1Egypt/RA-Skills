#!/usr/bin/env python3
"""
 risk_flagger.py

 功能：识别藏品的潜在风险点
"""

def flag_risks(description, category=None):
    """识别藏品的潜在风险点"""
    risks = []
    
    # 通用风险识别
    text = description.lower()
    
    # 来源风险
    if any(keyword in text for keyword in ['祖传', '老师说', '拍卖公司', '海外回流', '有证书']):
        risks.append('来源故事包装替代本体判断')
    
    # 修补风险
    if any(keyword in text for keyword in ['修复', '修补', '补过', '修过', '冲线']):
        risks.append('修补遮瑕')
    
    # 款识风险
    if any(keyword in text for keyword in ['款', '款识', '印章', '题跋']):
        risks.append('后添款识/印章')
    
    # 门类特定风险
    if category == '书画':
        risks.extend([
            '真画假款',
            '后添款',
            '伪印',
            '拼接改装',
            '旧裱新画'
        ])
    elif category == '瓷器':
        risks.extend([
            '后写款',
            '仿古做旧',
            '修补遮瑕',
            '老底新身或新底老身'
        ])
    elif category == '玉器':
        risks.extend([
            '新玉仿老工',
            '老料新工',
            '酸蚀做旧',
            '染色仿沁',
            '机械工冒充手工老工'
        ])
    elif category == '铜器与杂项':
        risks.extend([
            '新仿古器',
            '新老拼配',
            '后刻铭文',
            '假皮壳、假锈',
            '翻修冒充原状'
        ])
    
    # 价格风险
    if any(keyword in text for keyword in ['值多少钱', '价格', '估价', '值不值']):
        risks.append('价格预期过高')
    
    # 交易风险
    if any(keyword in text for keyword in ['买', '入手', '拍', '拍卖']):
        risks.append('交易风险')
    
    return list(set(risks))  # 去重

def generate_risk_prompt(risks):
    """生成风险提示"""
    if not risks:
        return "暂未识别到明显风险点，但仍建议保持谨慎。"
    
    prompt = "# 风险提示\n\n"
    prompt += "## 潜在风险点\n"
    for risk in risks:
        prompt += f"- {risk}\n"
    
    prompt += "\n## 建议\n"
    prompt += "- 重点检查上述风险点\n"
    prompt += "- 确保图片清晰、多角度\n"
    prompt += "- 涉及交易时，建议上手或线下复核\n"
    prompt += "- 来源信息只能作旁证，不能替代器物本体判断"
    
    return prompt

if __name__ == "__main__":
    # 示例用法
    description = "帮我看看这件祖传的瓷器，有冲线，老师说是清代的"
    risks = flag_risks(description, '瓷器')
    print(generate_risk_prompt(risks))