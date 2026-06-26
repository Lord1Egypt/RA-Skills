#!/usr/bin/env python3
"""CAN 接口初始化 — 转发到 can_init.sh（防御 agent 误用 python3 执行 .sh）"""
import subprocess, sys, os

script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "can_init.sh")
result = subprocess.run(["bash", script] + sys.argv[1:], stdout=sys.stdout, stderr=sys.stderr)
sys.exit(result.returncode)
