#!/usr/bin/env python3
"""修改蜀宁 OA 工时记录，支持按 ID 更新描述或逻辑删除"""

import argparse
import json
import os
import sys

from runtime_bootstrap import ensure_runtime

ensure_runtime(["requests", "ddddocr", "PIL"])

from oa_utils import build_session, get_time_entry_details, load_credentials, login, resolve_base_url, state_to_text, update_time_entry

DEFAULT_CREDS = os.path.expanduser("~/.openclaw/workspace/memory/sn-work-record-credentials.md")


def main():
    parser = argparse.ArgumentParser(description="修改蜀宁 OA 工时记录")
    parser.add_argument("entry_id", help="工时 ID")
    parser.add_argument("--job-desc", help="新的工时描述")
    parser.add_argument("--delete", action="store_true", help="逻辑删除工时（isDeleted=1）")
    parser.add_argument("--credentials", default=DEFAULT_CREDS)
    parser.add_argument("--base-url", dest="base_url", default=None)
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    if args.job_desc is None and not args.delete:
        parser.error("请至少提供 --job-desc 或 --delete 之一")

    try:
        username, password, base_url = load_credentials(args.credentials)
        base_url = resolve_base_url(base_url, args.base_url)

        print("正在登录 OA 系统...", file=sys.stderr)
        token = login(username, password, base_url)
        session = build_session(token)

        print(f"正在修改工时 {args.entry_id} ...", file=sys.stderr)
        result = update_time_entry(
            session,
            base_url,
            args.entry_id,
            job_desc=args.job_desc,
            is_deleted=1 if args.delete else None,
        )
        detail, _ = get_time_entry_details(session, base_url, args.entry_id)

        if args.json:
            print(json.dumps({"update": result, "detail": detail}, ensure_ascii=False, indent=2))
            return

        state = str(detail.get("state", ""))
        print(f"工时修改成功：{args.entry_id}\n")
        print(f"日期：{detail.get('fillDate', '')}")
        print(f"项目：{detail.get('projectName', '')}")
        print(f"时长：{detail.get('manHour', '')}h")
        print(f"描述：{detail.get('jobDesc', '')}")
        print(f"状态：{state_to_text(state)} ({state})")
        print(f"是否删除：{detail.get('isDeleted', '')}")
        print(f"更新时间：{detail.get('updatedTime', '')}")

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
