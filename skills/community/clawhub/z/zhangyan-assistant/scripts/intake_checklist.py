#!/usr/bin/env python3
"""
 intake_checklist.py

 功能：检查用户输入信息是否完整，生成补图建议
"""

def check_input_completeness(user_input):
    """检查用户输入的完整性"""
    checklist = {
        '整体图': False,
        '局部细节图': False,
        '底部/背面图': False,
        '款识/印章/铭文特写': False,
        '尺寸': False,
        '材质': False,
        '来源': False,
        '是否修复过': False
    }
    
    # 简单的关键词匹配，实际应用中可能需要更复杂的NLP处理
    text = user_input.lower()
    
    # 检查图片相关
    if any(keyword in text for keyword in ['图', '照片', '图片', '拍照']):
        # 这里应该结合实际的图片识别逻辑
        pass
    
    # 检查文字信息
    if any(keyword in text for keyword in ['尺寸', '大小', '厘米', '公分']):
        checklist['尺寸'] = True
    
    if any(keyword in text for keyword in ['材质', '材料', '质地']):
        checklist['材质'] = True
    
    if any(keyword in text for keyword in ['来源', '出处', '哪里来', '怎么来']):
        checklist['来源'] = True
    
    if any(keyword in text for keyword in ['修复', '修补', '补过', '修过']):
        checklist['是否修复过'] = True
    
    return checklist

def generate_missing_info_prompt(checklist):
    """根据检查结果生成补图建议"""
    missing_items = [item for item, present in checklist.items() if not present]
    
    if not missing_items:
        return "信息已基本完整，可以开始分析。"
    
    prompt = "为了更准确地分析，建议补充以下信息：\n"
    for item in missing_items:
        prompt += f"- {item}\n"
    
    prompt += "\n图不全时，结论只能非常保守。"
    return prompt

if __name__ == "__main__":
    # 示例用法
    user_input = "帮我看看这件瓷器，是我祖传的，有冲线"
    checklist = check_input_completeness(user_input)
    print(generate_missing_info_prompt(checklist))