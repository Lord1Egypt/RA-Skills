#!/usr/bin/env python3

"""
poll_vcreative.py — 重启编辑类任务轮询

用法:
  python <SKILL_DIR>/scripts/poll_vcreative.py <task_id> [space_name]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_manage import ApiManage
from vod_common import get_space_name, out, bail

def main():
    if len(sys.argv) < 2:
        bail("用法: python <SKILL_DIR>/scripts/poll_vcreative.py <task_id> [space_name]")
    task_id = sys.argv[1]
    api = ApiManage()
    space_name = get_space_name(argv_pos=2)
    result = api.poll_vcreative(task_id, space_name)
    out(result)

if __name__ == "__main__":
    main()
