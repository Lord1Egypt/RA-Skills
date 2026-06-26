#!/usr/bin/env python3
"""
wechat-publisher: 发布 Markdown 到微信公众号草稿箱
Usage: python publish.py <markdown-file> [theme] [highlight]
"""

import os
import re
import shutil
import subprocess
import sys
import time

# ANSI 颜色
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"

DEFAULT_THEME = "lapis"
DEFAULT_HIGHLIGHT = "solarized-light"
TOOLS_MD = os.path.expanduser("~/.openclaw/workspace/TOOLS.md")
PUBLISH_MAX_ATTEMPTS = 4  # 首次 + 重试 3 次
PUBLISH_RETRY_DELAY_SEC = 5


def check_wenyan() -> bool:
    """检查 wenyan-cli 是否安装，未安装则自动安装"""
    if shutil.which("wenyan") is None:
        print(f"{RED}wenyan-cli 未安装！{NC}")
        print(f"{YELLOW}正在安装 wenyan-cli...{NC}")
        try:
            subprocess.run(
                ["npm", "install", "-g", "@wenyan-md/cli"],
                check=True,
                capture_output=False,
            )
            print(f"{GREEN}wenyan-cli 安装成功！{NC}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{RED}安装失败！请手动运行: npm install -g @wenyan-md/cli{NC}")
            return False
    return True


def load_credentials() -> tuple[str, str]:
    app_id = os.environ.get("WECHAT_APP_ID")
    app_secret = os.environ.get("WECHAT_APP_SECRET")

    if app_id and app_secret:
        return app_id, app_secret

    if os.path.isfile(TOOLS_MD):
        print(f"{YELLOW}从 TOOLS.md 读取凭证...{NC}")
        with open(TOOLS_MD, encoding="utf-8") as f:
            content = f.read()

        def _extract(key: str) -> str:
            m = re.search(rf"export\s+{key}=([^\s#]+)", content)
            return m.group(1).strip("'\"") if m else ""

        app_id = _extract("WECHAT_APP_ID") or app_id or ""
        app_secret = _extract("WECHAT_APP_SECRET") or app_secret or ""

    return app_id or "", app_secret or ""


def check_env() -> bool:
    """检查环境变量，未设置则提示并退出"""
    app_id, app_secret = load_credentials()

    if not app_id or not app_secret:
        print(f"{RED}环境变量未设置！{NC}")
        print(f"{YELLOW}请在 TOOLS.md 中添加微信公众号凭证：{NC}")
        print("")
        print("  ## WeChat Official Account (微信公众号)")
        print("  ")
        print("  export WECHAT_APP_ID=your_app_id")
        print("  export WECHAT_APP_SECRET=your_app_secret")
        print("")
        print(f"{YELLOW}或者手动设置环境变量：{NC}")
        print("  export WECHAT_APP_ID=your_app_id")
        print("  export WECHAT_APP_SECRET=your_app_secret")
        print("")
        return False

    os.environ["WECHAT_APP_ID"] = app_id
    os.environ["WECHAT_APP_SECRET"] = app_secret
    return True


def check_file(filepath: str) -> bool:
    """检查文件是否存在"""
    if not os.path.isfile(filepath):
        print(f"{RED}文件不存在: {filepath}{NC}")
        return False
    return True


def publish(filepath: str, theme: str, highlight: str) -> bool:
    """执行发布"""
    print(f"{GREEN}准备发布文章...{NC}")
    print(f"  文件: {filepath}")
    print(f"  主题: {theme}")
    print(f"  代码高亮: {highlight}")
    print("")

    try:
        result = subprocess.run(
            ["wenyan", "publish", "-f", filepath, "-t", theme, "-h", highlight],
            check=False,
        )
        if result.returncode == 0:
            print("")
            print(f"{GREEN}发布成功！{NC}")
            print(f"{YELLOW}请前往微信公众号后台草稿箱查看：{NC}")
            print("  https://mp.weixin.qq.com/")
            return True
    except FileNotFoundError:
        pass

    print("")
    print(f"{RED}发布失败！{NC}")
    print(f"{YELLOW}常见问题：{NC}")
    print("  1. IP 未在白名单 → 添加到公众号后台")
    print("  2. Frontmatter 缺失 → 文件顶部添加 title + cover")
    print("  3. API 凭证错误 → 检查 TOOLS.md 中的凭证")
    return False


def show_help() -> None:
    """显示帮助"""
    prog = "publish.py" if "publish.py" in sys.argv[0] else "publish.sh"
    print(f"Usage: {prog} <markdown-file> [theme] [highlight]")
    print("")
    print("Examples:")
    print(f"  {prog} article.md")
    print(f"  {prog} article.md lapis")
    print(f"  {prog} article.md lapis solarized-light")
    print("")
    print("Available themes:")
    print("  default, lapis, phycat, ...")
    print("  Run 'wenyan theme -l' to see all themes")
    print("")
    print("Available highlights:")
    print("  atom-one-dark, atom-one-light, dracula, github-dark, github,")
    print("  monokai, solarized-dark, solarized-light, xcode")


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        show_help()
        return 0

    filepath = sys.argv[1]
    theme = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_THEME
    highlight = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_HIGHLIGHT

    if not check_wenyan():
        return 1
    if not check_env():
        return 1
    if not check_file(filepath):
        return 1

    for attempt in range(1, PUBLISH_MAX_ATTEMPTS + 1):
        if attempt > 1:
            print(f"{YELLOW}第 {attempt} 次发布尝试...{NC}")
        if publish(filepath, theme, highlight):
            return 0
        if attempt < PUBLISH_MAX_ATTEMPTS:
            print(f"{YELLOW}{PUBLISH_RETRY_DELAY_SEC} 秒后重试（剩余 {PUBLISH_MAX_ATTEMPTS - attempt} 次）...{NC}")
            time.sleep(PUBLISH_RETRY_DELAY_SEC)

    return 1


if __name__ == "__main__":
    sys.exit(main())
