"""_root.py — Wiki 根目录自动探测（脚本间共享）

导入约定：各脚本目录与本文件同目录，运行 `python scripts/<x>.py` 时
Python 自动把脚本所在目录加入 sys.path，故可直接 `from _root import detect_wiki_root`。

探测规则：
1. 编程助手环境（Trae/VS Code/Cursor 等"有当前项目"概念）：
   从 cwd 向上查找项目标记，命中则用 <project-root>/.wiki-creator/，与项目绑定。
2. 办公智能体环境（无项目概念）：用 ~/.wiki-creator/（全局共享，不绑定特定产品名）。
3. 任何场景都可用 `--root <path>` 显式覆盖。
"""
from __future__ import annotations

import re
from pathlib import Path

# 项目标记：出现任一即视为项目根
PROJECT_MARKERS = {
    ".git",
    ".vscode",
    ".trae",
    ".idea",
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "settings.gradle",
    "composer.json",
}


def normalize_path(p: "str | Path") -> Path:
    """规范化路径，处理 Git Bash 风格的路径（如 /c/Users/... → C:/Users/...）。

    Git Bash 中 /c/ 对应 Windows C:\\，/d/ 对应 D:\\，以此类推。
    若不转换，Path() 在 Windows 上会创建 \\c\\Users\\... 路径，
    导致 find/ls 等工具无法发现文件。
    """
    s = str(p)
    # 匹配 /c/、/d/ 等 Git Bash 风格路径（仅 Windows 上有意义）
    m = re.match(r"^/([a-zA-Z])/(.*)", s)
    if m:
        drive = m.group(1).upper()
        rest = m.group(2)
        s = f"{drive}:/{rest}"
    return Path(s)


def detect_wiki_root() -> Path:
    """返回探测到的 Wiki 根目录（Path 对象）。

    - cwd 位于项目内 → <project-root>/.wiki-creator/
    - 否则 → ~/.wiki-creator/（全局共享，不绑定特定产品名）
    """
    cwd = Path.cwd()
    for d in [cwd, *cwd.parents]:
        if any((d / m).exists() for m in PROJECT_MARKERS):
            return d / ".wiki-creator"
    return Path.home() / ".wiki-creator"
