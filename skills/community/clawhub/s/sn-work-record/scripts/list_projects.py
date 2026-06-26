#!/usr/bin/env python3
"""获取蜀宁 OA 项目列表，供用户选择默认项目"""

import argparse
import os
import sys

from runtime_bootstrap import ensure_runtime

ensure_runtime(["requests", "ddddocr", "PIL"])

from oa_utils import REQ_TIMEOUT, build_session, load_credentials, login, resolve_base_url

DEFAULT_CREDS = os.path.expanduser("~/.openclaw/workspace/memory/sn-work-record-credentials.md")


def main():
    parser = argparse.ArgumentParser(description="获取蜀宁 OA 项目列表")
    parser.add_argument("--credentials", default=DEFAULT_CREDS)
    parser.add_argument("--base-url", dest="base_url", default=None)
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    try:
        username, password, base_url, current_project_id, current_project_name = load_credentials(
            args.credentials, require_project=True
        )
        base_url = resolve_base_url(base_url, args.base_url)

        print("正在登录 OA 系统...", file=sys.stderr)
        token = login(username, password, base_url)

        print("正在获取项目列表...", file=sys.stderr)
        session = build_session(token)
        r = session.post(
            f"{base_url}/sn/project/timeFeeDropDownPageList",
            json={"page": 1, "size": 8000},
            timeout=REQ_TIMEOUT,
        )
        r.raise_for_status()
        result = r.json()

        if str(result.get("code")) != "200":
            print(f"获取项目列表失败: {result}", file=sys.stderr)
            sys.exit(1)

        if args.json:
            import json

            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

        items = result.get("data", {}).get("content", result.get("data", {}).get("records", []))
        if not items:
            print("未找到任何项目", file=sys.stderr)
            sys.exit(1)

        print(f"\n共找到 {len(items)} 个项目：\n")
        for i, p in enumerate(items, 1):
            pid = p.get("id", "")
            pname = p.get("projectBoName", p.get("projectName", p.get("name", "")))
            is_current = " ← 当前默认" if pid == current_project_id else ""
            print(f"  {i}. [{pid}] {pname}{is_current}")

        print("\n如需设为默认项目，请告诉助手：")
        print("  默认项目ID：<id>，默认项目名称：<名称>")
        print(f"\n当前默认：{current_project_name or '未设置'} [{current_project_id or '无'}]")

    except FileNotFoundError as e:
        print(f"文件未找到: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"凭据错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知异常: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
