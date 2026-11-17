"""兄弟技能 CLI 调用工具。

通过子进程调用同级其他 skill 的 main.py，并解析 JSON 输出。
具体调用哪些兄弟技能，由复制后的业务 skill 在 service 层按需决定。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

from util.logging_config import subprocess_env_with_trace
from util.runtime_paths import get_skills_root


def call_sibling_json(skill_slug: str, args: List[str]) -> Optional[Dict[str, Any]]:
    """通用兄弟技能调用器。

    Args:
        skill_slug: 兄弟技能的 slug（即同级目录名）。
        args: 传给 main.py 的命令行参数列表。

    Returns:
        若兄弟技能输出可解析的 JSON 对象则返回 dict；否则返回 None。
    """
    script_path = os.path.join(get_skills_root(), skill_slug, "scripts", "main.py")
    if not os.path.isfile(script_path):
        return None
    proc = subprocess.run(
        [sys.executable, script_path, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=subprocess_env_with_trace(),
    )
    raw = (proc.stdout or "").strip()
    if not raw or raw.startswith("ERROR"):
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def get_sibling_main_path(skill_slug: str) -> str:
    """获取兄弟技能的 main.py 绝对路径。

    使用示例（在 task_service.py 中）：
        from service.sibling_bridge import get_sibling_main_path, call_sibling_json
        result = call_sibling_json("account-manager", ["list", "--limit", "10"])
    """
    return os.path.join(get_skills_root(), skill_slug, "scripts", "main.py")
