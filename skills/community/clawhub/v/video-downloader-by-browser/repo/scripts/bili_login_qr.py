#!/usr/bin/env python3
"""
B站扫码登录脚本（零凭据：本文件不含任何真实账号 / 手机号 / cookie 值）

用法:
  python bili_login_qr.py <工作目录> [超时秒, 默认 180]

行为:
  1. 无头启动本机 Chrome / Chromium（沙箱无显示器时走这条路）
  2. 打开 B站登录页，等待二维码
  3. 把二维码保存为 <工作目录>/bili_qrcode.png，并打印 READY_FOR_SCAN
  4. 轮询登录态；用户用「哔哩哔哩 App」扫码并在手机上点「确认登录」
  5. 检测到 SESSDATA 后，把 cookie 落盘为 <工作目录>/bilibili_cookies.txt (Netscape 格式)
  6. 打印 LOGIN_SUCCESS 并退出(0)；超时未登录退出(2)

注意:
  - 本脚本不含任何真实账号 / 手机号 / cookie 值；凭据只在运行时产生
  - cookie 只写到运行时工作目录，绝不回写进 skill、绝不随包分发
  - 沙箱无显示器时，靠「我出二维码 → 你扫 → 我捕获」完成登录
"""

import sys
import os
import time
import shutil

try:
    from playwright.sync_api import sync_playwright
except Exception as e:  # noqa
    print("ERR: playwright 不可用:", e, file=sys.stderr)
    sys.exit(3)

LOGIN_URL = "https://passport.bilibili.com/login"


def log(msg):
    print(msg, flush=True)


def save_cookies_netscape(ctx, path):
    cookies = ctx.cookies()
    with open(path, "w") as f:
        f.write("# Netscape HTTP Cookie File\n")
        for c in cookies:
            domain = c["domain"]
            flag = "TRUE" if domain.startswith(".") else "FALSE"
            path_ = c.get("path", "/")
            secure = "TRUE" if c.get("secure") else "FALSE"
            exp = c.get("expires", 0) or 0
            exp = int(exp) if exp else 0
            f.write(
                f"{domain}\t{flag}\t{path_}\t{secure}\t{exp}\t"
                f"{c['name']}\t{c['value']}\n"
            )


def capture_qr(page, qr_path):
    """截图二维码。B站登录页可见二维码容器是 `.login-scan__qrcode`（display:block），
    优先截它；其余 canvas（多为 display:none 干扰项）兜底。"""
    for sel in [".login-scan__qrcode", "img.qrcode", ".qrcode-box img", "#login-qrcode img"]:
        try:
            el = page.query_selector(sel)
            if el:
                el.screenshot(path=qr_path)
                return True
        except Exception:  # noqa
            continue
    # 兜底：截整页，用户仍能识别并扫码
    try:
        page.screenshot(path=qr_path)
        return True
    except Exception:  # noqa
        return False


def main():
    if len(sys.argv) < 2:
        log("用法: python bili_login_qr.py <工作目录> [超时秒]")
        sys.exit(1)

    workdir = sys.argv[1]
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 180
    os.makedirs(workdir, exist_ok=True)
    qr_path = os.path.join(workdir, "bili_qrcode.png")
    cookie_path = os.path.join(workdir, "bilibili_cookies.txt")

    with sync_playwright() as p:
        launch_args = dict(headless=True)
        chrome = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
        if chrome:
            launch_args["executable_path"] = chrome
        browser = p.chromium.launch(**launch_args)

        ctx = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            )
        )
        page = ctx.new_page()

        log("OPEN_LOGIN_PAGE")
        page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=30000)

        # 优先切到「扫码登录」tab（若默认不是）
        for label in ["扫码登录", "二维码登录"]:
            try:
                page.click(f"text={label}", timeout=4000)
                break
            except Exception:  # noqa
                continue

        try:
            # 可见二维码容器是 .login-scan__qrcode；canvas 多为 display:none 干扰项
            page.wait_for_selector(".login-scan__qrcode, canvas", state="attached", timeout=15000)
            page.wait_for_timeout(1500)  # 等二维码渲染
        except Exception as e:  # noqa
            log("ERR: 未找到二维码元素: " + str(e))
            browser.close()
            sys.exit(2)

        if capture_qr(page, qr_path):
            log(f"READY_FOR_SCAN {qr_path}")
            log("请用哔哩哔哩 App 扫码，并在手机上点「确认登录」")
        else:
            log("ERR: 二维码截图失败")
            browser.close()
            sys.exit(2)

        deadline = time.time() + timeout
        while time.time() < deadline:
            cookies = ctx.cookies()
            if any(c["name"] == "SESSDATA" for c in cookies):
                save_cookies_netscape(ctx, cookie_path)
                # 把 expires=-1 改为 0，避免 yt-dlp 跳过会话 cookie 导致仍 412
                try:
                    with open(cookie_path) as f:
                        data = f.read()
                    data = data.replace("\t-1\t", "\t0\t")
                    with open(cookie_path, "w") as f:
                        f.write(data)
                except Exception:  # noqa
                    pass
                log(f"LOGIN_SUCCESS {cookie_path}")
                browser.close()
                sys.exit(0)
            time.sleep(3)

        log("TIMEOUT_NO_LOGIN")
        browser.close()
        sys.exit(2)


if __name__ == "__main__":
    main()
