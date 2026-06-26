#!/usr/bin/env python3
"""
 response_formatter.py

 功能：格式化回复内容，确保专业、克制的表达风格
"""

def format_response(analysis, category=None):
    """格式化回复内容"""
    # 提取分析结果
    boundary = analysis.get('boundary', '单看图片只能做初步分析，关键判断仍以上手为准。')
    info = analysis.get('info', {})
    analysis_points = analysis.get('analysis', [])
    conclusion = analysis.get('conclusion', '暂不能定')
    suggestions = analysis.get('suggestions', [])
    
    # 构建回复
    response = f"# 初步分析结果\n\n"
    
    # 1. 边界说明
    response += f"## 边界说明\n{boundary}\n\n"
    
    # 2. 信息提炼
    response += "## 信息提炼\n"
    if info:
        for key, value in info.items():
            response += f"- {key}：{value}\n"
    else:
        response += "- 信息不足，需要补充\n"
    response += "\n"
    
    # 3. 分点分析
    response += "## 分点分析\n"
    if analysis_points:
        for i, point in enumerate(analysis_points, 1):
            response += f"{i}. {point}\n"
    else:
        response += "- 分析依据不足\n"
    response += "\n"
    
    # 4. 分层结论
    response += f"## 分层结论\n{conclusion}\n\n"
    
    # 5. 下一步建议
    response += "## 下一步建议\n"
    if suggestions:
        for suggestion in suggestions:
            response += f"- {suggestion}\n"
    else:
        response += "- 建议补图或上手复核\n"
    
    # 添加通用提醒
    response += "\n## 温馨提醒\n"
    response += "- 图片鉴定只能初判，关键判断以上手为准\n"
    response += "- 不替代官方、司法或文博机构的正式鉴定\n"
    response += "- 来源、证书或故事不能替代器物本体判断\n"
    
    return response

def generate_conclusion(confidence, issues):
    """根据分析结果生成分层结论"""
    if confidence >= 0.8 and not issues:
        return "初步看整体问题不大，但仍需以上手为准。"
    elif confidence >= 0.6 and len(issues) < 2:
        return "有一定时代感，但关键依据不足。"
    elif confidence >= 0.4 and len(issues) < 3:
        return "目前看有几处疑点，不能轻易往好处下判断。"
    elif confidence >= 0.2:
        return "初步看疑点较多，建议谨慎处理。"
    else:
        return "现在信息不足，暂不能定。"

if __name__ == "__main__":
    # 示例用法
    analysis = {
        'boundary': '单看图片只能做初步分析，关键判断仍以上手为准。',
        'info': {
            '门类': '瓷器',
            '尺寸': '高15cm',
            '来源': '祖传'
        },
        'analysis': [
            '器形有参考清代风格的意思',
            '釉面光泽略显浮亮',
            '底足修胎痕迹不够自然'
        ],
        'conclusion': '有一定时代感，但关键依据不足。',
        'suggestions': [
            '补拍底足细图',
            '提供更多角度的釉面照片',
            '建议上手观察胎质'
        ]
    }
    print(format_response(analysis, '瓷器'))