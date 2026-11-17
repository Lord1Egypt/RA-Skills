#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨平台双语文 JSON 自举冒烟（Windows cp1252 防线）。

供 CI 与本地 `PYTHONIOENCODING=ascii` 验证：确认 pyboot 把 stdout 切到 UTF-8
后，zh/en 两种 JSON 均能原样输出且可被 json.loads 解析。不改业务逻辑。
"""
try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass
import json
import platform
import sys

lang = "zh"
if "--lang" in sys.argv[1:]:
    i = sys.argv.index("--lang")
    if i + 1 < len(sys.argv) and sys.argv[i + 1] in ("zh", "en"):
        lang = sys.argv[i + 1]

version = _boot_pyboot.skill_version() if "_boot_pyboot" in globals() else "unknown"
msg = "English JSON output OK" if lang == "en" else "中文JSON输出OK"
print(json.dumps({
    "status": "ok",
    "skill_version": version,
    "message": msg,
    "os": platform.system(),
}, ensure_ascii=False))
