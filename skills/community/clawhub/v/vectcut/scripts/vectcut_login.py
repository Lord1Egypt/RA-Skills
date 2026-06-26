#!/usr/bin/env python3

import argparse
import json
import shlex
import sys
import urllib.error
import urllib.request
import webbrowser

LOGIN_URL = "https://www.vectcut.com/auth"
VERIFY_URL = "https://open.vectcut.com/cut_jianying/task_status"
VERIFY_TASK_ID = "DEFA35C07BEE7F95161F787A7EEC4877"


def build_export_command(token):
    return f"export VECTCUT_API_KEY={shlex.quote(token)}"


def verify_token(token):
    payload = json.dumps({"task_id": VERIFY_TASK_ID}).encode("utf-8")
    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Accept": "*/*",
        "Host": "open.vectcut.com",
        "Connection": "keep-alive",
    }
    request = urllib.request.Request(
        VERIFY_URL,
        data=payload,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            status = response.getcode()
    except urllib.error.HTTPError as exc:
        status = exc.code
    except urllib.error.URLError as exc:
        print(f"校验请求失败：{exc}", file=sys.stderr)
        return False
    return not (400 <= status <= 499)


def start_web_login(no_open_browser=False):
    print("默认使用网页登录。")
    print("说明：出于浏览器安全机制，脚本无法直接读取你登录后的 VECTCUT_API_KEY")
    print("请在网页登录后点击右上角头像，获取 VECTCUT_API_KEY。")
    print(f"登录地址：{LOGIN_URL}")
    if not no_open_browser:
        opened = webbrowser.open(LOGIN_URL)
        if opened:
            print("已尝试为你打开登录页。")
        else:
            print("无法自动打开浏览器，请手动访问上面的登录地址。")
    print("下一步：请在完成登录后，将 VECTCUT_API_KEY 作为下一条消息输入给助手。")
    print("收到后将自动生成可执行的 export 命令。")
    return 0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jwt-token", dest="jwt_token")
    parser.add_argument("--mode", choices=["web"], default="web")
    parser.add_argument("--no-open-browser", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.jwt_token:
        token = args.jwt_token.strip()
        if not verify_token(token):
            print("VECTCUT_API_KEY 校验失败：接口返回 4xx，请检查后重试。", file=sys.stderr)
            sys.exit(1)
        print(build_export_command(token))
        return
    if args.mode == "web":
        sys.exit(start_web_login(no_open_browser=args.no_open_browser))
    sys.exit(1)


if __name__ == "__main__":
    main()
