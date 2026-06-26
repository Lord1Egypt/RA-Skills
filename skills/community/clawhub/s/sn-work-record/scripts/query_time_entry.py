#!/usr/bin/env python3
"""查询蜀宁 OA 某天工时列表"""

import argparse
import json
import os
import sys

from runtime_bootstrap import ensure_runtime

ensure_runtime(["requests", "ddddocr", "PIL"])

from oa_utils import build_session, load_credentials, login, query_time_entries, resolve_base_url, state_to_text

DEFAULT_CREDS = os.path.expanduser("~/.openclaw/workspace/memory/sn-work-record-credentials.md")


def main():
    parser = argparse.ArgumentParser(description="查询蜀宁 OA 某天工时列表")
    parser.add_argument("fill_date", nargs="?", help="查询日期，格式 YYYY-MM-DD")
    parser.add_argument("--fill-date", dest="fill_date_flag", help="查询日期，格式 YYYY-MM-DD")
    parser.add_argument("--credentials", default=DEFAULT_CREDS)
    parser.add_argument("--base-url", dest="base_url", default=None)
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    fill_date = args.fill_date_flag or args.fill_date
    if not fill_date:
        parser.error("请提供查询日期，例如：2026-04-10")

    try:
        username, password, base_url = load_credentials(args.credentials)
        base_url = resolve_base_url(base_url, args.base_url)

        print("正在登录 OA 系统...", file=sys.stderr)
        token = login(username, password, base_url)

        print(f"正在查询 {fill_date} 的工时...", file=sys.stderr)
        session = build_session(token)
        items, result = query_time_entries(session, base_url, fill_date)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

        if not items:
            print(f"{fill_date} 暂无工时记录")
            return

        print(f"{fill_date} 共 {len(items)} 条工时记录：\n")
        for i, item in enumerate(items, 1):
            state = str(item.get("state", ""))
            print(f"{i}. 项目：{item.get('projectName', '')}")
            print(f"   时长：{item.get('manHour', '')}h")
            print(f"   描述：{item.get('jobDesc', '')}")
            print(f"   状态：{state_to_text(state)} ({state})")
            print(f"   ID：{item.get('id', '')}")
            print(f"   填写时间：{item.get('createdTime', '')}")
            print(f"   更新时间：{item.get('updatedTime', '')}")
            if i != len(items):
                print()

    except FileNotFoundError as e:
        print(f"文件未找到: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"凭据错误: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知异常: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
