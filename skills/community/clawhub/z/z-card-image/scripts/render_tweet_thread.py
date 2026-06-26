#!/usr/bin/env python3
"""
兼容入口：tweet-thread 已升级为 x-like-posts。
请优先使用 render_x_like_posts.py。
"""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name("render_x_like_posts.py")), run_name="__main__")
