#!/usr/bin/env python3
"""编导模式 · 确认修改提案：POST /api/director/v2/<session_id>/modification/confirm。

当 AI 提出结构化修改提案（proposal）时，用本脚本确认执行。按提案 strategy：
  TEXT_REPLACE      在所有阶段数据中批量替换文本
  PARTIAL_INVALIDATE 更新当前阶段 + 标记下游 stale
  FULL_CASCADE       标记当前及下游全部 stale，触发重新生成

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
        description="确认并执行编导修改提案",
        epilog="""
示例:
  python3 director_confirm.py --proposal-id mp_a1b2c3d4
  python3 director_confirm.py --proposal-id mp_a1b2c3d4 --session-id dv2_xxxxxxxxxxxx

说明:
  proposal_id 来自 director_chat 回复中的修改提案（action/summary）
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--proposal-id", required=True, help="修改提案 ID（如 mp_a1b2c3d4）")
    parser.add_argument("--session-id", default="", help="会话 ID（缺省读状态文件）")
    parser.add_argument("--tab-id", default=None, help="页签 ID（缺省读状态文件）")
    parser.add_argument("--state-file", default="", help="会话状态文件路径")
    args = parser.parse_args()

    proposal_id = (args.proposal_id or "").strip()
    if not proposal_id:
        error_exit("proposal-id 不能为空")

    session_id, tab_id = require_session(args)
    body = {"proposal_id": proposal_id}
    if tab_id:
        body["tab_id"] = tab_id

    code, data = director_post(session_id, "modification/confirm", body)
    if code != 200 or not (isinstance(data, dict) and data.get("success")):
        err = data if isinstance(data, dict) else {"message": str(data)}
        error_exit(format_business_error(code, {"error_code": err.get("error_code", ""),
                                                "message": err.get("error") or err.get("message", ""),
                                                "details": {}}))
    json_output({
        "success": True,
        "session_id": session_id,
        "strategy": data.get("strategy"),
        "modified_stages": data.get("modified_stages", []),
        "summary": data.get("summary", ""),
    })


if __name__ == "__main__":
    main()
