#!/usr/bin/env python3
"""编导模式 · 查询会话状态：GET /api/director/v2/<session_id>/status（或 /full_state）。

输出当前阶段、各阶段状态与产出（剧本/角色/分镜）。缺省从状态文件读 session_id。
鉴权：Authorization: Bearer vooai_xxx（AccessKey，需付费会员）。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import json_output, error_exit, format_business_error
from _director import director_get_status, require_session


def main():
    parser = argparse.ArgumentParser(
        description="查询编导会话的阶段状态与产出",
        epilog="""
示例:
  python3 director_status.py                 # 当前阶段 + 各阶段状态摘要
  python3 director_status.py --full          # 完整阶段数据（剧本/角色/分镜全量）
  python3 director_status.py --session-id dv2_xxxxxxxxxxxx

阶段模型:
  Stage 1 剧本 → Stage 2 角色与元素 → Stage 3 分镜 → Stage 4 工作流/成片
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--session-id", default="", help="会话 ID（缺省读状态文件）")
    parser.add_argument("--tab-id", default=None, help="页签 ID（缺省读状态文件）")
    parser.add_argument("--full", action="store_true", help="返回完整状态（full_state）")
    parser.add_argument("--state-file", default="", help="会话状态文件路径")
    args = parser.parse_args()

    session_id, tab_id = require_session(args)
    code, data = director_get_status(session_id, tab_id, full=args.full)

    if code != 200 or not (isinstance(data, dict) and data.get("success")):
        err = data if isinstance(data, dict) else {"message": str(data)}
        error_exit(format_business_error(code, {"error_code": err.get("error_code", ""),
                                                "message": err.get("error") or err.get("message", ""),
                                                "details": {}}))

    if args.full:
        # full_state 结构较丰富，直接透传
        json_output(data)
        return

    out = {
        "success": True,
        "session_id": session_id,
        "tab_id": tab_id,
        "status": data.get("status"),
        "current_stage": data.get("current_stage"),
        "auto_generate": data.get("auto_generate"),
        "stage_statuses": data.get("stage_statuses", {}),
        "source": data.get("source"),
    }
    # 各阶段产出的轻量摘要（键存在才带）
    stage_data = data.get("stage_data", {}) or {}
    brief = {}
    for sn, sd in stage_data.items():
        if isinstance(sd, dict):
            brief[str(sn)] = sorted(sd.keys())
    if brief:
        out["stage_data_keys"] = brief
    if data.get("note"):
        out["note"] = data["note"]
    json_output(out)


if __name__ == "__main__":
    main()
