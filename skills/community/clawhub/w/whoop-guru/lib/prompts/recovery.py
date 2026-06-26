"""
恢复优化 Prompt 模板
用于生成个性化恢复方案
"""

TEMPLATE_RECOVERY_SYSTEM = """
我每周训练{days_per_week}天，
感觉越来越累，恢复不够。

恢复数据显示：
- 平均恢复评分：{avg_recovery}%
- 平均HRV：{avg_hrv}ms
- 静息心率：{avg_rhr}bpm
- 睡眠债务：{sleep_debt}小时

给我一份恢复优化方案，包括：
1. 训练频率调整
2. 睡眠优化建议
3. 压力管理
4. 营养补充建议
5. 主动恢复动作
"""

TEMPLATE_RECOVERY_WEEKLY = """
本周恢复状态分析：

- 平均恢复：{avg_recovery}%
- 最佳恢复日：{best_day}
- 最差恢复日：{worst_day}
- HRV趋势：{hrv_trend}
- 睡眠质量：{sleep_quality}

下周恢复重点：
{next_week_focus}
"""

TEMPLATE_RECOVERY_SLEEP = """
最近睡眠问题：

- 平均睡眠时长：{avg_sleep_hours}小时
- 入睡时间：{sleep_onset}
- 中断次数：{disturbances}次
- 深睡比例：{deep_sleep_pct}%
- REM比例：{rem_sleep_pct}%

睡眠优化建议：
{recommendations}
"""


def get_recovery_prompt(prompt_type: str, data: dict) -> str:
    """
    获取恢复Prompt模板
    
    Args:
        prompt_type: 模板类型 (system, weekly, sleep)
        data: 用户数据
    
    Returns:
        填充好的Prompt
    """
    templates = {
        "system": TEMPLATE_RECOVERY_SYSTEM,
        "weekly": TEMPLATE_RECOVERY_WEEKLY,
        "sleep": TEMPLATE_RECOVERY_SLEEP,
    }
    
    template = templates.get(prompt_type, "")
    
    try:
        return template.format(**data)
    except KeyError as e:
        return f"模板填充错误：缺少字段 {e}"
