#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""项目路径解析：把作者本机绝对路径换成分级可移植解析。

本技能包里有两类"包外依赖"，都不该写死作者机器的路径：

1. **外部项目根**（可选，例如作者本机的 `资治通鉴蒸馏/` 工作区，里面有
   `书籍蒸馏/`、`学习记录/`、`PIPELINE_STATE.md`）。三级解析：
     ① 环境变量 `SIMAGUANG_PROJECT_DIR`（显式指定，最高优先）
     ② 相对探测：从当前工作目录、脚本目录、包根逐级向上找标志目录
     ③ 都没有 → `find_project_dir()` 返回 None，由调用方打印友好指引
        （`project_dir_help()`），或退化到包内默认输出位置。

2. **可执行工具 pdftotext**（PDF 抽取用）。三级解析：
     ① 环境变量 `SIMAGUANG_PDFTOTEXT`
     ② PATH 里 `shutil.which("pdftotext")`
     ③ Codex runtime 内置 poppler（`~/.cache/codex-runtimes/*/...`）
     ④ 都没有 → 返回 None，由调用方打印 `pdftotext_help()` 的安装指引

这样换一台没有该项目、没装 poppler 的机器，技能依旧可独立使用：
只做包内协议问答不需要项目目录；只处理 txt/docx/epub 不需要 pdftotext。
"""

from __future__ import annotations

import os
import shutil

try:  # 与其它入口一致：先自举 UTF-8，避免 ascii locale 下打印中文指引就崩
    import sys as _boot_sys

    _boot_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pyboot as _boot_pyboot

    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

from pathlib import Path

ENV_PROJECT = "SIMAGUANG_PROJECT_DIR"
ENV_PDFTOTEXT = "SIMAGUANG_PDFTOTEXT"

# 外部项目根的标志：看到这些之一就认为"找到了项目"
PROJECT_MARKERS = ("书籍蒸馏", "PIPELINE_STATE.md")

_MAX_UP = 6


def _upward_bases() -> list[Path]:
    """可能藏着外部项目根的起点：工作目录、脚本目录、包根。"""
    here = Path(__file__).resolve().parent
    bases = [Path.cwd(), here, here.parent]
    uniq: list[Path] = []
    for base in bases:
        try:
            resolved = base.resolve()
        except OSError:
            continue
        if resolved not in uniq:
            uniq.append(resolved)
    return uniq


def _has_marker(path: Path) -> bool:
    return any((path / marker).exists() for marker in PROJECT_MARKERS)


def find_project_dir() -> Path | None:
    """返回外部项目根；解析不到返回 None（不抛异常，调用方决定怎么降级）。

    环境变量指向不存在的目录时也返回 None —— 由 `env_problem()` 说明原因，
    避免静默用错目录。
    """
    env = os.environ.get(ENV_PROJECT, "").strip()
    if env:
        candidate = Path(env).expanduser()
        return candidate.resolve() if candidate.is_dir() else None

    for base in _upward_bases():
        current = base
        for _ in range(_MAX_UP + 1):
            if _has_marker(current):
                return current
            if current.parent == current:  # 已到根，防死循环
                break
            current = current.parent
    return None


def env_problem() -> str:
    """环境变量设了但目录不存在时返回一句人话，否则空串。"""
    env = os.environ.get(ENV_PROJECT, "").strip()
    if not env:
        return ""
    candidate = Path(env).expanduser()
    if candidate.is_dir():
        return ""
    return f"{ENV_PROJECT}={env} 指向的目录不存在。"


def project_dir_help() -> str:
    """解析失败时的友好指引（中文，可直接打印给用户）。"""
    problem = env_problem()
    lines = []
    if problem:
        lines.append(problem)
    lines += [
        "未找到外部项目根（标志：" + " / ".join(PROJECT_MARKERS) + "）。",
        "这类目录属于作者本地扩展，技能包本身不包含它；不影响协议问答与模板渲染。",
        "",
        "需要用到它时，显式指定路径后重试：",
        f'  macOS/Linux:  export {ENV_PROJECT}="/path/to/项目根"',
        f'  Windows CMD:  setx {ENV_PROJECT} "D:\\path\\to\\项目根"',
        f"  一次性:       {ENV_PROJECT}=/path/to/项目根 python3 scripts/<脚本>.py ...",
        "",
        "或改用脚本自带的 --out 参数，把输出写到你自己指定的位置。",
    ]
    return "\n".join(lines)


def _runtime_pdftotext() -> str | None:
    """Codex runtime 内置 poppler：存在就复用，不存在就算了。"""
    cache = Path(os.environ.get("XDG_CACHE_HOME") or (Path.home() / ".cache"))
    roots = [
        cache / "codex-runtimes",
        Path.home() / ".codex" / "runtimes",
    ]
    for root in roots:
        if not root.is_dir():
            continue
        for pattern in ("*/dependencies/native/poppler/**/pdftotext",
                        "*/native/poppler/**/pdftotext"):
            for hit in sorted(root.glob(pattern)):
                if hit.is_file() and os.access(hit, os.X_OK):
                    return str(hit)
    return None


def find_pdftotext() -> tuple[str | None, str]:
    """返回 (可执行文件路径 | None, 来源标记 env/path/runtime/missing)。"""
    env = os.environ.get(ENV_PDFTOTEXT, "").strip()
    if env:
        candidate = Path(env).expanduser()
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate), "env"
        return None, "missing"

    hit = shutil.which("pdftotext")
    if hit:
        return hit, "path"

    hit = _runtime_pdftotext()
    if hit:
        return hit, "runtime"

    return None, "missing"


def pdftotext_help() -> str:
    """缺 pdftotext 时的安装指引。"""
    return "\n".join([
        "未找到 pdftotext，PDF 抽取不可用（其它格式 txt/md/docx/epub/mobi 不受影响）。",
        "任选一种方式装上：",
        "  macOS:   brew install poppler",
        "  Debian/Ubuntu: sudo apt-get install poppler-utils",
        "  Windows: choco install poppler   （或 scoop install poppler，把 bin 加进 PATH）",
        f"  已有自定义路径: export {ENV_PDFTOTEXT}=\"/path/to/pdftotext\"",
    ])


if __name__ == "__main__":  # 手动排查用：python3 scripts/project_paths.py
    root = find_project_dir()
    print(f"{ENV_PROJECT} = {os.environ.get(ENV_PROJECT, '') or '(未设置)'}")
    print(f"项目根       = {root if root else '(未找到)'}")
    if not root:
        print(project_dir_help())
    exe, source = find_pdftotext()
    print(f"pdftotext    = {exe or '(未找到)'}  来源={source}")
    if not exe:
        print(pdftotext_help())
