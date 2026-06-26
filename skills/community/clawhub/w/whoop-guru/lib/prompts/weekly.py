"""
周报 Prompt 模板
用于生成周期性训练报告
"""

TEMPLATE_WEEKLY_REVIEW = """
第{week_num}周训练总结：

**数据统计**
- 训练天数：{training_days}天
- 完成率：{completion_rate}%
- 平均恢复：{avg_recovery}%
- 平均strain：{avg_strain}
- 睡眠债务变化：{sleep_debt_change}

**进步指标**
{progress_indicators}

**问题分析**
{problem_analysis}

下周调整方案：
{next_week_adjustments}
"""

TEMPLATE_WEEKLY_PLAN = """
下周训练计划（第{week_num}周）：

**训练目标**
{training_goals}

**训练安排**
{training_schedule}

**恢复重点**
{recovery_focus}

**注意事项**
{cautions}
"""

TEMPLATE_MONTHLY_REVIEW = """
月度训练报告（第{month_num}月）：

**整体表现**
- 训练天数：{total_days}天
- 总训练量：{total_volume}
- 目标完成率：{goal_completion}%

**身体变化**
- 体重变化：{weight_change}kg
- 体脂变化：{bf_change}%
- 力量变化：{strength_change}

**恢复稳定性**
{recovery_stability}

**下月重点**
{next_month_focus}
"""


def get_weekly_prompt(prompt_type: str, data: dict) -> str:
    """
    获取周报Prompt模板
    
    Args:
        prompt_type: 模板类型 (review, plan, monthly)
        data: 用户数据
    
    Returns:
        填充好的Prompt
    """
    templates = {
        "review": TEMPLATE_WEEKLY_REVIEW,
        "plan": TEMPLATE_WEEKLY_PLAN,
        "monthly": TEMPLATE_MONTHLY_REVIEW,
    }
    
    template = templates.get(prompt_type, "")
    
    try:
        return template.format(**data)
    except KeyError as e:
        return f"模板填充错误：缺少字段 {e}"
