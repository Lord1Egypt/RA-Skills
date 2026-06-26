#!/usr/bin/env python3
"""根据工时 ID 查询蜀宁 OA 工时详情"""

import argparse
import json
import os
import sys

from runtime_bootstrap import ensure_runtime

ensure_runtime(["requests", "ddddocr", "PIL"])

from oa_utils import build_session, get_time_entry_details, load_credentials, login, resolve_base_url, state_to_text

DEFAULT_CREDS = os.path.expanduser("~/.openclaw/workspace/memory/sn-work-record-credentials.md")


def main():
    parser = argparse.ArgumentParser(description="根据工时 ID 查询蜀宁 OA 工时详情")
    parser.add_argument("entry_id", help="工时 ID")
    parser.add_argument("--credentials", default=DEFAULT_CREDS)
    parser.add_argument("--base-url", dest="base_url", default=None)
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    try:
        username, password, base_url = load_credentials(args.credentials)
        base_url = resolve_base_url(base_url, args.base_url)

        print("正在登录 OA 系统...", file=sys.stderr)
        token = login(username, password, base_url)

        print(f"正在获取工时详情 {args.entry_id} ...", file=sys.stderr)
        session = build_session(token)
        detail, result = get_time_entry_details(session, base_url, args.entry_id)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

        if not detail:
            print("未找到工时详情")
            return

        state = str(detail.get("state", ""))
        print(f"工时详情：{args.entry_id}\n")
        print(f"日期：{detail.get('fillDate', '')}")
        print(f"项目：{detail.get('projectName', '')}")
        print(f"项目ID：{detail.get('projectId', '')}")
        print(f"时长：{detail.get('manHour', '')}h")
        print(f"描述：{detail.get('jobDesc', '')}")
        print(f"状态：{state_to_text(state)} ({state})")
        print(f"填写人：{detail.get('fillUserName', '')}")
        print(f"填写时间：{detail.get('createdTime', '')}")
        print(f"更新时间：{detail.get('updatedTime', '')}")
        print(f"是否删除：{detail.get('isDeleted', '')}")

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
