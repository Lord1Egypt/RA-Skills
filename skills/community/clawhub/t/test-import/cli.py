#!/usr/bin/env python3
"""CLI wrapper for ClawHub Publish"""
import sys
import os

# 添加 skill 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from publish import publish_skill, main

if __name__ == "__main__":
    main()
