"""技能配置初始化：.env.example 落盘与用户 .env 缺失项合并。"""

from __future__ import annotations

import os

from jiangchang_skill_core import config

from util.constants import SKILL_SLUG, SKILL_VERSION
from util.runtime_paths import get_skill_root


def bootstrap_skill_config() -> str:
    """确保用户数据目录 .env 存在，并追加 .env.example 中的新配置项。"""
    example_path = os.path.join(get_skill_root(), ".env.example")
    env_path = config.ensure_env_file(SKILL_SLUG, example_path)
    comment = f"{SKILL_SLUG} v{SKILL_VERSION}" if SKILL_VERSION else None
    config.merge_missing_env_keys(example_path, env_path, comment_skill=comment)
    return env_path
