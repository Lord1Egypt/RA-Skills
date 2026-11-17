#!/usr/bin/env python3
"""蜀宁 OA 登录脚本（agent 多模态优先 + ddddocr 兜底）

三种用法：

1) 默认：ddddocr 闭环登录，token 输出到 stdout
   python sn_oa_login.py

2) 取图（把识别权交给 user 当前 agent 的多模态能力）：
   python sn_oa_login.py --fetch-only
   → stdout 输出 JSON：uuid / image_path / data_url，不登录

3) 提交（agent 识别出答案后）：
   python sn_oa_login.py --submit --uuid <uuid> --code <答案>
   → token 输出到 stdout；若验证码被拒，自动回退 ddddocr 重新取图登录

退出码: 0=成功, 1=失败
"""

import argparse
import json
import os
import sys

from runtime_bootstrap import ensure_runtime

ensure_runtime(["requests", "ddddocr", "PIL"])

DEFAULT_CREDS = os.path.expanduser("~/.openclaw/workspace/memory/sn-work-record-credentials.md")
CAPTCHA_DIR = os.path.expanduser("~/.cache/sn-oa")


def write_captcha(img_bytes, captcha_uuid):
    """落盘验证码，返回 (唯一路径, 固定最新路径)。

    服务端 data URL 前缀标 image/png，实际字节是 JPEG，故用 .jpg 扩展名。
    """
    os.makedirs(CAPTCHA_DIR, mode=0o700, exist_ok=True)
    unique_path = os.path.join(CAPTCHA_DIR, f"captcha_{captcha_uuid}.jpg")
    latest_path = os.path.join(CAPTCHA_DIR, "captcha_latest.jpg")
    for path in (unique_path, latest_path):
        fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "wb") as fh:
            fh.write(img_bytes)
    return unique_path, latest_path


def main():
    parser = argparse.ArgumentParser(description="蜀宁 OA 登录（agent 多模态优先 + ddddocr 兜底）")
    parser.add_argument("--credentials", default=DEFAULT_CREDS)
    parser.add_argument(
        "--base-url", dest="base_url", default=None, help="OA 系统 base URL，不指定则从凭据文件读取"
    )
    parser.add_argument("--fetch-only", action="store_true", help="只获取验证码并输出 JSON，不登录")
    parser.add_argument("--submit", action="store_true", help="用 --uuid/--code 提交登录")
    parser.add_argument("--uuid", dest="captcha_uuid", default=None, help="配合 --submit：--fetch-only 返回的 uuid")
    parser.add_argument("--code", dest="captcha_code", default=None, help="配合 --submit：识别出的验证码答案")
    parser.add_argument("--no-ddddocr-fallback", action="store_true", help="外部验证码被拒时不回退 ddddocr")
    args = parser.parse_args()

    if args.fetch_only and args.submit:
        parser.error("--fetch-only 与 --submit 不能同时使用")

    try:
        # 延迟导入，避免在 --help 时加载 ddddocr
        from oa_utils import (
            CaptchaRejectedError,
            fetch_captcha,
            load_credentials,
            login,
            login_with_code,
            resolve_base_url,
            save_cached_token,
        )

        username, password, base_url = load_credentials(args.credentials)
        base_url = resolve_base_url(base_url, args.base_url)

        if args.fetch_only:
            captcha_uuid, img_bytes, data_url = fetch_captcha(base_url)
            unique_path, latest_path = write_captcha(img_bytes, captcha_uuid)
            print(
                json.dumps(
                    {
                        "status": "captcha_required",
                        "uuid": captcha_uuid,
                        "image_path": latest_path,
                        "image_path_unique": unique_path,
                        "data_url": data_url,
                        "next": f"识别这张算术验证码后执行: --submit --uuid {captcha_uuid} --code <答案>",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return

        if args.submit:
            if not args.captcha_uuid or args.captcha_code is None:
                parser.error("--submit 需要同时提供 --uuid 和 --code")
            try:
                token, method = login_with_code(
                    username,
                    password,
                    base_url,
                    args.captcha_code,
                    args.captcha_uuid,
                    fallback_ddddocr=not args.no_ddddocr_fallback,
                )
            except CaptchaRejectedError as exc:
                print(f"❌ 验证码被拒绝（已禁用 ddddocr 回退）: {exc}", file=sys.stderr)
                sys.exit(1)
            print(f"[login] 验证码来源: {method}", file=sys.stderr)
            save_cached_token(token, base_url, username)
            print(token, end="")
            return

        token = login(username, password, base_url)
        save_cached_token(token, base_url, username)
        print(token, end="")  # 无换行，方便 capture
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"❌ 凭据错误: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知异常: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
