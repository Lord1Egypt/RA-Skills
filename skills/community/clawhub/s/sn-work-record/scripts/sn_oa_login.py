#!/usr/bin/env python3
"""蜀宁 OA 登录脚本（ddddocr 验证码 + 自动登录）

用法: python sn_oa_login.py [--credentials PATH] [--base-url URL]
退出码: 0=成功(token到stdout), 1=失败(错误到stderr)
"""

import argparse, os, sys

from runtime_bootstrap import ensure_runtime

ensure_runtime(["requests", "ddddocr", "PIL"])

DEFAULT_CREDS = os.path.expanduser("~/.openclaw/workspace/memory/sn-work-record-credentials.md")


def main():
    parser = argparse.ArgumentParser(description="蜀宁 OA 自动登录（ddddocr）")
    parser.add_argument("--credentials", default=DEFAULT_CREDS)
    parser.add_argument("--base-url", dest="base_url", default=None,
        help="OA 系统 base URL，不指定则从凭据文件读取")
    args = parser.parse_args()

    try:
        # 延迟导入，避免在 --help 时加载 ddddocr
        from oa_utils import load_credentials, login, resolve_base_url

        username, password, base_url = load_credentials(args.credentials)
        base_url = resolve_base_url(base_url, args.base_url)

        token = login(username, password, base_url)
        print(token, end="")  # 无换行，方便 capture
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}", file=sys.stderr); sys.exit(1)
    except ValueError as e:
        print(f"❌ 凭据错误: {e}", file=sys.stderr); sys.exit(1)
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr); sys.exit(1)
    except Exception as e:
        print(f"❌ 未知异常: {type(e).__name__}: {e}", file=sys.stderr); sys.exit(1)


if __name__ == "__main__":
    main()
