#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""火山方舟密钥的读取点（整个 skill 只有这一个地方碰环境变量）

单独放一个文件，是为了让「密钥从哪来」这件事只有一处、好审计：
  - 只读进程环境变量 ARK_API_KEY
  - 不读任何配置文件，不读 $HOME 下的任何路径
  - 不打印、不落盘、不写日志
"""

import os

ENV_NAME = "ARK_API_KEY"


def get_key():
    """返回 ARK_API_KEY，没有就返回空字符串。"""
    return os.environ.get(ENV_NAME, "").strip()


def missing_key_hint():
    return f"缺 {ENV_NAME}（先 export {ENV_NAME}=... 再跑；键值只从环境变量读）"
