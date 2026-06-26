"""
Windows UTF-8 encoding fix — import 即自动生效。

在 Windows 上，PowerShell / cmd 默认使用 GBK (CP936) 编码。
当 Node.js 以 UTF-8 解码 Python 子进程的 stdout/stderr 时，
中文输出会变成乱码。此模块在 import 时自动将 stdout/stderr/stdin
reconfigure 为 UTF-8，确保与 OpenClaw Node.js 宿主通信正确。

macOS / Linux 不受影响——模块检测到非 Windows 平台后直接跳过。
"""

import sys as _sys
import os as _os

if _sys.platform == 'win32':
    # 1) 影响当前进程的 stdio
    for _stream_name in ('stdout', 'stderr', 'stdin'):
        _stream = getattr(_sys, _stream_name, None)
        if _stream is not None and hasattr(_stream, 'reconfigure'):
            try:
                _stream.reconfigure(encoding='utf-8', errors='replace')
            except Exception:
                pass

    # 2) 影响后续 spawn 的子进程
    _os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
