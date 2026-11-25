#!/usr/bin/env python3
"""编导模式 · 启动会话：POST /api/director/v2/start（SSE）。

传入创意描述，后端 AI 驱动 Stage 1（剧本），返回 session_id 并落地到本地状态文件
（.voooai_director_session.json），供后续 director_chat/status/export 复用。

⚠️ 编导模式为多轮 LLM + 多次生成，积分消耗较高。默认 --no-auto-generate（不自动推进），
   由 Agent 逐阶段向用户确认后再用 director_chat/navigate 推进，符合「绝不代替用户耗积分」。
鉴权：Authorization: Bearer vooai_xxx（AccessKey，需付费会员）。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import (
    api_post_stream, json_output, error_exit, save_session_state,
    DEFAULT_SSE_MAX_TIMEOUT,
)
from _director import finalize_turn


def main():
    parser = argparse.ArgumentParser(
        description="启动 VoooAI 编导模式会话（剧本→角色→分镜→成片）",
        epilog="""
环境变量:
  VOOOAI_ACCESS_KEY  必填，Bearer 鉴权（需付费会员）
  VOOOAI_BASE_URL    可选，默认 https://voooai.com

示例:
  # 启动一个短剧会话（默认不自动推进，逐阶段确认）
  python3 director_start.py "一部关于侦探的短剧，黑色电影风格"

  # 指定语言与引擎
  python3 director_start.py "30秒咖啡广告" --locale zh --engine-type evolink_gemini_25_flash

  # 实时把 AI 回复 token 打到 stderr（观察进度）
  python3 director_start.py "武侠短片" --verbose

  # 无凭证演练
  python3 director_start.py "测试" --dry-run

启动后:
  session_id 存入 .voooai_director_session.json
  用 director_chat.py 继续对话推进；director_status.py 查看阶段产出
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("description", help="首条创意描述（会原样传递，请勿改写用户意图）")
    parser.add_argument("--engine-type", default="", help="LLM 引擎（可选，默认平台缺省）")
    parser.add_argument("--tab-id", default="", help="页签 ID（多会话隔离，可选）")
    parser.add_argument("--auto-generate", action="store_true",
                        help="允许 AI 自动推进生成（默认关闭，逐阶段确认更省积分）")
    parser.add_argument("--locale", default="", help="界面语种 zh/en/ja/ko/ar（可选）")
    parser.add_argument("--state-file", default="", help="会话状态文件路径（默认 .voooai_director_session.json）")
    parser.add_argument("--timeout", type=int, default=DEFAULT_SSE_MAX_TIMEOUT, help=f"SSE 整体超时秒数（默认 {DEFAULT_SSE_MAX_TIMEOUT}）")
    parser.add_argument("--verbose", action="store_true", help="实时打印 AI 回复 token 到 stderr")
    parser.add_argument("--dry-run", action="store_true", help="仅打印请求体，不实际调用（无凭证/CI）")
    args = parser.parse_args()

    description = (args.description or "").strip()
    if not description:
        error_exit("description 不能为空")

    body = {"description": description, "auto_generate": bool(args.auto_generate)}
    if args.engine_type:
        body["engine_type"] = args.engine_type
    if args.tab_id:
        body["tab_id"] = args.tab_id
    if args.locale:
        body["locale"] = args.locale

    if args.dry_run:
        json_output({"success": True, "dry_run": True,
                     "endpoint": "POST /api/director/v2/start (SSE)",
                     "request_body": body, "message": "dry-run：未实际启动会话"})
        return

    print("正在启动编导会话（SSE）...", file=sys.stderr)
    result = api_post_stream("/api/director/v2/start", body,
                             max_timeout=args.timeout, verbose=args.verbose)
    if args.verbose:
        print("", file=sys.stderr)

    session_id = result.get("session_id", "")
    tab_id = result.get("tab_id", "") or args.tab_id
    if session_id:
        path = save_session_state(session_id, tab_id, args.state_file or None)
        print(f"会话已保存: session_id={session_id} → {path}", file=sys.stderr)

    out = finalize_turn(result, session_id=session_id or None, tab_id=tab_id)
    json_output(out)
    if not out.get("success") and not session_id:
        sys.exit(1)


if __name__ == "__main__":
    main()
