"""
OpenClaw Task Runner Skill 配置
"""

import os
from typing import Optional
from pydantic import BaseModel


class SkillConfig(BaseModel):
    """Skill配置"""

    # OpenClaw API 配置
    api_base_url: str = "https://claw-dev.int-os.com"
    api_prefix: str = ""

    # Bot 认证配置 (从Bot平台注册获取)
    api_key: Optional[str] = None  # API Key from Bot平台
    api_secret: Optional[str] = None  # API Secret from Bot平台

    # 轮询配置
    poll_interval_seconds: int = 10  # 轮询间隔
    page_size: int = 20  # 每次拉取任务数量

    # 任务执行配置
    output_dir: str = "./output"  # 输出目录
    delivery_message: str = "任务已完成，详情见附件"  # 默认交付话语

    # 任务过滤配置
    min_bounty: Optional[float] = None  # 最低赏金(元)
    categories: Optional[list[str]] = None  # 感兴趣的任务分类

    # 执行配置
    max_concurrent_tasks: int = 1  # 最大并发任务数
    task_timeout_seconds: int = 3600  # 任务超时时间(秒)


def load_config(**kwargs) -> SkillConfig:
    """加载配置，支持环境变量和参数覆盖"""
    config = SkillConfig()

    # 从环境变量覆盖
    if os.environ.get("TASK_API_BASE_URL"):
        config.api_base_url = os.environ["TASK_API_BASE_URL"]
    if os.environ.get("YINTAI_APP_KEY"):
        config.api_key = os.environ["YINTAI_APP_KEY"]
    if os.environ.get("YINTAI_APP_SECRET"):
        config.api_secret = os.environ["YINTAI_APP_SECRET"]
    if os.environ.get("TASK_POLL_INTERVAL"):
        config.poll_interval_seconds = int(os.environ["TASK_POLL_INTERVAL"])
    if os.environ.get("TASK_OUTPUT_DIR"):
        config.output_dir = os.environ["TASK_OUTPUT_DIR"]

    # 从参数覆盖
    for key, value in kwargs.items():
        if value is not None and hasattr(config, key):
            setattr(config, key, value)

    return config
