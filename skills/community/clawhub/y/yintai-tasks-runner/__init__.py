"""
OpenClaw Task Runner Skill

功能：
1. 每隔 x 秒轮询 bots 的任务接口
2. 找到可接单的任务
3. 尝试锁定任务
4. 执行任务
5. 更新交付结果（.zip 格式 + 一段话）
"""

from yintai_tasks_runner.skill import YintaiTasksRunnerSkill

__all__ = ["YintaiTasksRunnerSkill"]
__version__ = "1.0.0"
