"""
7个健身Prompt模板
用于生成个性化训练计划
"""

# 模板1：完整训练计划
TEMPLATE_COMPLETE_PLAN = """
我训练{experience}年，
深蹲{max_squat}kg、卧推{max_bench}kg、硬拉{max_deadlift}kg，
每周能训练{days_per_week}天。

给我一份完整的{goal}计划，包括：
- 训练部位分配
- 动作选择
- 组数次数
- 和纯增肌/纯减脂计划的区别

额外信息：
- 可用时间：{available_time}分钟
- 可用设备：{equipment}
- 当前体重：{body_weight}kg
- WHOOP恢复数据：平均恢复{avg_recovery}%，近7天训练负荷{strain_level}
"""

# 模板2：平台期突破
TEMPLATE_PLATEAU_BREAK = """
我{event}卡在{max_weight}kg三个月了，
体重{body_weight}kg，目标{goal_weight}kg。

给我一份突破平台期的专项计划。

WHOOP数据显示：
- 当前恢复状态：{recovery}%
- 近7天训练频率：{training_frequency}天
- HRV趋势：{hrv_trend}
- 睡眠质量：{sleep_quality}
"""

# 模板3：弱项诊断
TEMPLATE_WEAKPOINT_DIAGNOSTIS = """
我的{weak_point}进步很慢，
但{strong_point}在涨。

WHOOP数据显示我的{related_metric}表现：
- 该动作后心率恢复时间：{hr_recovery_time}
- 训练后HRV变化：{hrv_change}
- 肌肉疲劳度：{fatigue_level}

分析我的问题，给我一个针对性计划。
"""

# 模板4：恢复系统
TEMPLATE_RECOVERY_SYSTEM = """
我每周训练{days_per_week}天，
感觉越来越累，恢复不够。

恢复数据显示：
- 平均恢复评分：{avg_recovery}%
- 平均HRV：{avg_hrv}ms
- 静息心率：{avg_rhr}bpm
- 睡眠债务：{sleep_debt}小时

给我一份恢复优化方案。
"""

# 模板5：伤病预防
TEMPLATE_INJURY_PREVENTION = """
我的{injury_area}在{injury_movement}时有不适，
但不想停止训练。

WHOOP数据显示：
- 该动作后心率恢复变慢：{hr_recovery_change}%
- 过去30天该部位相关训练：{related_training}次
- 恢复评分趋势：{recovery_trend}

给我一份保护{injury_area}的训练方案，不停止训练。
"""

# 模板6：追踪框架
TEMPLATE_TRACKING_FRAMEWORK = """
我想要一个追踪系统，
告诉我训练是否有效，
如何在体重不变时判断是否在进步。

当前数据：
- 体重：{body_weight}kg（不变）
- 深蹲：{squat}kg（2个月没变）
- 卧推：{bench}kg（涨了2.5kg）
- 训练频率：{frequency}天/周

给我一个多维度的进步追踪框架。
"""

# 模板7：16周重组策略
TEMPLATE_16_WEEK_RERECOMPOSITION = """
我训练{experience}年，
体型：{body_type}
目标：{goal}

WHOOP历史数据摘要：
- 过去90天平均恢复：{avg_recovery}%
- 训练依从性：{compliance}%
- 睡眠质量评分：{sleep_score}
- 最大训练strain：{max_strain}

给我一份16周重组计划：
- 现实期望
- 训练方案
- 营养策略
- 有氧策略
- 追踪协议
- 4/8/12周调整方案
- 常见错误
"""

# 每日训练计划模板
TEMPLATE_DAILY_PLAN = """
基于以下数据，生成今日训练计划：

恢复状态：{recovery}%
近期训练负荷：{recent_strain}天高强度
睡眠债务：{sleep_debt}小时
用户目标：{goal}
可用时间：{available_time}分钟
身体状态：{body_status}

今日推荐：
- 训练类型：{recommended_type}
- 训练强度：{intensity}
- 具体动作：{exercises}
- 组数次数：{sets_reps}
- 注意事项：{cautions}
"""


def get_training_prompt(prompt_type: str, data: dict) -> str:
    """
    获取训练Prompt模板
    
    Args:
        prompt_type: 模板类型 (complete, plateau, weakpoint, recovery, injury, tracking, 16week, daily)
        data: 用户数据
    
    Returns:
        填充好的Prompt
    """
    templates = {
        "complete": TEMPLATE_COMPLETE_PLAN,
        "plateau": TEMPLATE_PLATEAU_BREAK,
        "weakpoint": TEMPLATE_WEAKPOINT_DIAGNOSTIS,
        "recovery": TEMPLATE_RECOVERY_SYSTEM,
        "injury": TEMPLATE_INJURY_PREVENTION,
        "tracking": TEMPLATE_TRACKING_FRAMEWORK,
        "16week": TEMPLATE_16_WEEK_RERECOMPOSITION,
        "daily": TEMPLATE_DAILY_PLAN,
    }
    
    template = templates.get(prompt_type, "")
    
    try:
        return template.format(**data)
    except KeyError as e:
        return f"模板填充错误：缺少字段 {e}"
