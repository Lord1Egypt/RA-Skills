"""运行环境引导：补 ezdxf vendor 路径，必要时切到带 Pillow 的本地 Python。

顺序：
1. 找 ezdxf：SITE_LAYOUT_VENDOR -> CAD_FILE_READER_HOME/vendor -> ${CODEX_HOME:-$HOME/.codex}/skills/cad-file-reader/vendor；
2. 检查 Pillow；
3. 当前解释器缺 ezdxf/Pillow 时，若 Codex 本地 Python 3.12 存在，用 os.execv 原地切换；
4. 切换后重新执行本函数，确保 vendor 路径在新解释器里仍有效。

只用 stdlib，不读图纸、不联网。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List, Optional


def _vendor_candidates() -> List[Path]:
    candidates: List[Path] = []
    raw = os.environ.get("SITE_LAYOUT_VENDOR")
    if raw:
        candidates.append(Path(raw).expanduser())
    home = os.environ.get("CAD_FILE_READER_HOME")
    if home:
        candidates.append(Path(home).expanduser() / "vendor")
    candidates.append(Path.home() / ".codex" / "skills" / "cad-file-reader" / "vendor")
    return candidates


def _find_vendor() -> Optional[Path]:
    for candidate in _vendor_candidates():
        if (candidate / "ezdxf" / "__init__.py").is_file():
            return candidate
    return None


def _runtime_python() -> Optional[Path]:
    override = os.environ.get("SITE_LAYOUT_PYTHON")
    if override:
        candidate = Path(override).expanduser()
        return candidate if candidate.is_file() else None
    candidate = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
        / "python"
        / "bin"
        / "python3"
    )
    return candidate if candidate.is_file() else None


def _probe(module: str) -> bool:
    try:
        __import__(module)
    except Exception:
        return False
    return True


def ensure_runtime(entry_file: str) -> None:
    """确保 ezdxf 与 Pillow 可用；不满足时切解释器，仍不满足则抛 RuntimeError。"""
    vendor = _find_vendor()
    if vendor is not None and str(vendor) not in sys.path:
        sys.path.insert(0, str(vendor))

    missing = []
    if not _probe("ezdxf"):
        missing.append("ezdxf")
    if not _probe("PIL"):
        missing.append("Pillow")
    if missing:
        runtime = _runtime_python()
        if runtime is not None and Path(sys.executable).resolve() != runtime.resolve():
            argv = [str(runtime), str(Path(entry_file).resolve())] + sys.argv[1:]
            os.execv(str(runtime), argv)
        raise RuntimeError(
            "缺少依赖：{}。可设置 SITE_LAYOUT_VENDOR 指向含 ezdxf 的 vendor 目录，"
            "或安装 ezdxf>=1.4 与 Pillow>=10；本机可运行 "
            "~/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3".format(
                ", ".join(missing)
            )
        )
