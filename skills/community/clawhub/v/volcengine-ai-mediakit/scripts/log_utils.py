#!/usr/bin/env python3
"""
log_utils.py — 零依赖的日志/错误工具函数。

从 vod_common.py 中提取，用于打破以下循环引用：
  api_manage -> vod_transport -> vod_common -> api_manage

本模块不 import 项目内其他模块，可被任意模块安全导入。
"""

import sys
import json
import time


def log(msg: str):
    """输出带时间戳的日志到 stderr。"""
    print(f"[info] {time.strftime('%Y-%m-%d %H:%M:%S')} {msg}", file=sys.stderr, flush=True)


def bail(msg: str):
    """输出 JSON 格式的错误信息到 stdout 并退出。"""
    print(json.dumps({"error": f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"}, ensure_ascii=False))
    sys.exit(1)


def out(data):
    """输出 JSON 或字符串到 stdout。"""
    print(json.dumps(data, ensure_ascii=False) if not isinstance(data, str) else data)
