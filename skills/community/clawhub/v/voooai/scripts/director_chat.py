#!/usr/bin/env python3
"""编导模式 · 对话推进：POST /api/director/v2/<session_id>/chat（SSE）。

向进行中的编导会话发送用户消息，AI 据此产出/修改剧本、角色、分镜，并可自动推进阶段。
缺省从 .voooai_director_session.json 读取 session_id；多会话时用 --session-id 指定。

鉴权：Authorization: Bearer vooai_xxx（AccessKey，需付费会员）。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import api_post_stream, json_output, error_exit, DEFAULT_SSE_MAX_TIMEOUT
from _director import finalize_turn, require_session


def main():
    parser = argparse.ArgumentParser(
        description="向编导会话发送消息，推进创作（SSE）",
        epilog="""
环境变量:
  VOOOAI_ACCESS_KEY  必填，Bearer 鉴权（需付费会员）
  VOOOAI_BASE_URL    可选，默认 https://voooai.com

示例:
  # 继续当前会话（自动读状态文件里的 session_id）
  python3 director_chat.py "把主角设定为退休警探，增加一个反派"

  # 确认当前阶段并进入下一步
  python3 director_chat.py "剧本没问题，进入角色设计"

  # 局部重做
  python3 director_chat.py "重做第 3 个分镜，改成夜景"

  # 指定会话
  python3 director_chat.py "..." --session-id dv2_xxxxxxxxxxxx

  # 无凭证演练
  python3 director_chat.py "测试" --dry-run

提示:
  - 确定性阶段推进（不耗 LLM 积分）可用 director_navigate.py --stage N
  - 回复中的 actions[] 表示 AI 执行的结构化操作（加角色/加分镜等）
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("content", help="用户消息文本（会原样传递，请勿改写用户意图）")
    parser.add_argument("--session-id", default="", help="会话 ID（缺省读状态文件）")
    parser.add_argument("--tab-id", default=None, help="页签 ID（缺省读状态文件）")
    parser.add_argument("--state-file", default="", help="会话状态文件路径")
    parser.add_argument("--timeout", type=int, default=DEFAULT_SSE_MAX_TIMEOUT, help=f"SSE 整体超时秒数（默认 {DEFAULT_SSE_MAX_TIMEOUT}）")
    parser.add_argument("--verbose", action="store_true", help="实时打印 AI 回复 token 到 stderr")
    parser.add_argument("--dry-run", action="store_true", help="仅打印请求体，不实际调用（无凭证/CI）")
    args = parser.parse_args()

    content = (args.content or "").strip()
    if not content:
        error_exit("content 不能为空")

    session_id, tab_id = require_session(args)

    body = {"content": content}
    if tab_id:
        body["tab_id"] = tab_id

    if args.dry_run:
        json_output({"success": True, "dry_run": True,
                     "endpoint": f"POST /api/director/v2/{session_id}/chat (SSE)",
                     "request_body": body, "message": "dry-run：未实际发送"})
        return

    print("正在发送消息给编导 AI（SSE）...", file=sys.stderr)
    result = api_post_stream(f"/api/director/v2/{session_id}/chat", body,
                             max_timeout=args.timeout, verbose=args.verbose)
    if args.verbose:
        print("", file=sys.stderr)

    out = finalize_turn(result, session_id=session_id, tab_id=tab_id)
    json_output(out)
    if not out.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
