"""
Prompts - 健身Prompt模板集合
包含7大核心模板：
1. 训练模板 (training.py)
2. 恢复模板 (recovery.py)
3. 伤病模板 (injury.py)
4. 周报模板 (weekly.py)
"""

from lib.prompts.training import (
    get_training_prompt,
    TEMPLATE_COMPLETE_PLAN,
    TEMPLATE_PLATEAU_BREAK,
    TEMPLATE_WEAKPOINT_DIAGNOSTIS,
    TEMPLATE_RECOVERY_SYSTEM,
    TEMPLATE_INJURY_PREVENTION,
    TEMPLATE_TRACKING_FRAMEWORK,
    TEMPLATE_16_WEEK_RERECOMPOSITION,
    TEMPLATE_DAILY_PLAN,
)

from lib.prompts.recovery import (
    get_recovery_prompt,
    TEMPLATE_RECOVERY_SYSTEM as RECOVERY_SYSTEM,
    TEMPLATE_RECOVERY_WEEKLY,
    TEMPLATE_RECOVERY_SLEEP,
)

from lib.prompts.injury import (
    get_injury_prompt,
    TEMPLATE_INJURY_PREVENTION as INJURY_PREVENTION,
    TEMPLATE_INJURY_RECOVERY,
    TEMPLATE_INJURY_SUBSTITUTE,
)

from lib.prompts.weekly import (
    get_weekly_prompt,
    TEMPLATE_WEEKLY_REVIEW,
    TEMPLATE_WEEKLY_PLAN,
    TEMPLATE_MONTHLY_REVIEW,
)

__all__ = [
    # Training
    'get_training_prompt',
    'TEMPLATE_COMPLETE_PLAN',
    'TEMPLATE_PLATEAU_BREAK',
    'TEMPLATE_WEAKPOINT_DIAGNOSTIS',
    'TEMPLATE_RECOVERY_SYSTEM',
    'TEMPLATE_INJURY_PREVENTION',
    'TEMPLATE_TRACKING_FRAMEWORK',
    'TEMPLATE_16_WEEK_RERECOMPOSITION',
    'TEMPLATE_DAILY_PLAN',
    # Recovery
    'get_recovery_prompt',
    'TEMPLATE_RECOVERY_WEEKLY',
    'TEMPLATE_RECOVERY_SLEEP',
    # Injury
    'get_injury_prompt',
    'TEMPLATE_INJURY_RECOVERY',
    'TEMPLATE_INJURY_SUBSTITUTE',
    # Weekly
    'get_weekly_prompt',
    'TEMPLATE_WEEKLY_REVIEW',
    'TEMPLATE_WEEKLY_PLAN',
    'TEMPLATE_MONTHLY_REVIEW',
]
