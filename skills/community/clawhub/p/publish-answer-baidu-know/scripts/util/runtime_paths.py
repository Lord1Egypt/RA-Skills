"""数据根、技能目录、兄弟技能根路径。"""

from __future__ import annotations

import os

from jiangchang_skill_core.runtime_env import get_data_root, get_sibling_skills_root, get_user_id

from util.constants import SKILL_SLUG

_SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_skill_root() -> str:
    return os.path.dirname(_SCRIPTS_DIR)


def get_openclaw_root() -> str:
    return get_sibling_skills_root(_SCRIPTS_DIR)


def get_skills_root() -> str:
    return get_sibling_skills_root(_SCRIPTS_DIR)


def get_skill_data_dir() -> str:
    path = os.path.join(get_data_root(), get_user_id(), SKILL_SLUG)
    os.makedirs(path, exist_ok=True)
    return path


def get_db_path(filename: str | None = None) -> str:
    name = filename or f"{SKILL_SLUG}.db"
    return os.path.join(get_skill_data_dir(), name)
