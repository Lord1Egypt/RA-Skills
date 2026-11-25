#!/usr/bin/env python3
"""编导模式 · 确定性阶段推进：POST /api/director/v2/<session_id>/navigate。

纯后端状态迁移，**绕过 LLM、不消耗 LLM 积分**：确认某阶段完成并前进到下一阶段。
返回 next_action=auto_init 时，表示下一阶段内容仍需一次生成（可用 director_chat 触发，
该步会走 LLM 并可能耗积分——推进前应向用户确认）。

鉴权：Authorization: Bearer vooai_xxx（AccessKey，需付费会员）。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import json_output, error_exit, format_business_error
from _director import director_post, require_session


def main():
    parser = argparse.ArgumentParser(
        description="确认并推进编导阶段（确定性，不耗 LLM 积分）",
        epilog="""
示例:
  python3 director_navigate.py --stage 1     # 确认 Stage 1（剧本），进入 Stage 2
  python3 director_navigate.py --stage 2     # 确认 Stage 2（角色/元素），进入 Stage 3
  python3 director_navigate.py --stage 3     # 确认 Stage 3（分镜），进入 Stage 4

说明:
  - stage 取值 1-3（确认「已完成」的阶段号）
  - 返回 next_action=auto_init 时，下一阶段内容需再用 director_chat 触发生成
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--stage", type=int, required=True, help="要确认完成的阶段号（1-3）")
    parser.add_argument("--session-id", default="", help="会话 ID（缺省读状态文件）")
    parser.add_argument("--tab-id", default=None, help="页签 ID（缺省读状态文件）")
    parser.add_argument("--state-file", default="", help="会话状态文件路径")
    args = parser.parse_args()

    if args.stage < 1 or args.stage > 3:
        error_exit("stage 取值范围为 1-3")

    session_id, tab_id = require_session(args)
    body = {"action": "confirm", "stage": args.stage}
    if tab_id:
        body["tab_id"] = tab_id

    code, data = director_post(session_id, "navigate", body)
    if code != 200 or not (isinstance(data, dict) and data.get("success")):
        err = data if isinstance(data, dict) else {"message": str(data)}
        error_exit(format_business_error(code, {"error_code": err.get("error_code", ""),
                                                "message": err.get("error") or err.get("message", ""),
                                                "details": {}}))
    json_output({
        "success": True,
        "session_id": session_id,
        "confirmed_stage": data.get("confirmed_stage"),
        "next_stage": data.get("next_stage"),
        "next_action": data.get("next_action"),
        "hint": "若 next_action=auto_init，用 director_chat.py 触发下一阶段内容生成（可能耗积分）",
    })


if __name__ == "__main__":
    main()
