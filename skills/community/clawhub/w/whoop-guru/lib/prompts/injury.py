"""
伤病预防 Prompt 模板
用于生成保护性训练方案
"""

TEMPLATE_INJURY_PREVENTION = """
我的{injury_area}在{injury_movement}时有不适，
但不想停止训练。

WHOOP数据显示：
- 该动作后心率恢复变慢：{hr_recovery_change}%
- 过去30天该部位相关训练：{related_training}次
- 恢复评分趋势：{recovery_trend}

给我一份保护{injury_area}的训练方案，包括：
1. 替代动作推荐
2. 热身重点
3. 训练后拉伸
4. 辅助强化动作
5. 恢复注意事项
"""

TEMPLATE_INJURY_RECOVERY = """
{injury_area}恢复计划：

当前状态：{current_status}
疼痛程度：{pain_level}/10
已持续时间：{duration}

给我一份分阶段恢复计划：
1. 第一周（急性期）
2. 第二周（修复期）
3. 第三周（强化期）
4. 第四周（回归正常训练）
"""

TEMPLATE_INJURY_SUBSTITUTE = """
需要替换的训练动作：{original_movement}

原因：{reason}
可用设备：{equipment}

给我一份替代动作方案：
1. 替代动作列表
2. 每组次数范围
3. 注意事项
"""


def get_injury_prompt(prompt_type: str, data: dict) -> str:
    """
    获取伤病Prompt模板
    
    Args:
        prompt_type: 模板类型 (prevention, recovery, substitute)
        data: 用户数据
    
    Returns:
        填充好的Prompt
    """
    templates = {
        "prevention": TEMPLATE_INJURY_PREVENTION,
        "recovery": TEMPLATE_INJURY_RECOVERY,
        "substitute": TEMPLATE_INJURY_SUBSTITUTE,
    }
    
    template = templates.get(prompt_type, "")
    
    try:
        return template.format(**data)
    except KeyError as e:
        return f"模板填充错误：缺少字段 {e}"
