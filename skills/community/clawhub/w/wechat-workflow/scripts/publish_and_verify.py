#!/usr/bin/env python3
"""
wechat-manager: 发布文章到微信公众号草稿箱，并验证搜索可检索性
Usage: python publish_and_verify.py <markdown-file> [theme] [highlight]
"""

import os, re, shutil, subprocess, sys, time, urllib.request, urllib.parse, json, platform

# ANSI 颜色
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"

DEFAULT_THEME = "lapis"
DEFAULT_HIGHLIGHT = "solarized-light"
TOOLS_MD = os.path.expanduser("~/.openclaw/workspace/TOOLS.md")
PUBLISH_MAX_ATTEMPTS = 4
PUBLISH_RETRY_DELAY_SEC = 5


def check_wenyan() -> bool:
    if shutil.which("wenyan") is None:
        print(f"{RED}wenyan-cli 未安装，正在安装...{NC}")
        try:
            subprocess.run(["npm", "install", "-g", "@wenyan-md/cli"], check=True, capture_output=False)
            print(f"{GREEN}wenyan-cli 安装成功！{NC}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{RED}安装失败！请手动运行: npm install -g @wenyan-md/cli{NC}")
            return False
    return True


def load_credentials() -> tuple[str, str]:
    """优先从 secrets.json 读取凭证，fallback 到 TOOLS.md"""
    app_id, app_secret = "", ""
    secrets_file = os.path.expanduser("~/.openclaw/workspace/secrets.json")

    # 优先从 secrets.json 读取
    if os.path.isfile(secrets_file):
        with open(secrets_file, encoding="utf-8") as f:
            secrets = json.load(f)
        if "wechat" in secrets:
            app_id = secrets["wechat"].get("appid", "")
            app_secret = secrets["wechat"].get("appsecret", "")
            if app_id and app_secret:
                print(f"{YELLOW}从 secrets.json 读取微信公众号凭证{NC}")
                return app_id, app_secret

    # Fallback 到 TOOLS.md
    if os.path.isfile(TOOLS_MD):
        print(f"{YELLOW}从 TOOLS.md 读取凭证...{NC}")
        with open(TOOLS_MD, encoding="utf-8") as f:
            content = f.read()

        def _extract(key: str) -> str:
            m = re.search(rf"export\s+{key}=([^\s#]+)", content)
            return m.group(1).strip("'\"") if m else ""

        app_id = _extract("WECHAT_APP_ID")
        app_secret = _extract("WECHAT_APP_SECRET")

    return app_id or "", app_secret or ""


def check_env() -> bool:
    app_id, app_secret = load_credentials()
    if not app_id or not app_secret:
        print(f"{RED}凭证未配置！{NC}")
        print(f"{YELLOW}请在 TOOLS.md 中添加 WECHAT_APP_ID 和 WECHAT_APP_SECRET{NC}")
        return False
    os.environ["WECHAT_APP_ID"] = app_id
    os.environ["WECHAT_APP_SECRET"] = app_secret
    return True


def check_file(filepath: str) -> bool:
    if not os.path.isfile(filepath):
        print(f"{RED}文件不存在: {filepath}{NC}")
        return False
    return True


def publish(filepath: str, theme: str, highlight: str) -> bool:
    """执行 wenyan 发布"""
    print(f"{GREEN}准备发布文章...{NC}")
    print(f"  文件: {filepath}")
    print(f"  主题: {theme}")
    print(f"  代码高亮: {highlight}")
    print("")

    app_id, app_secret = load_credentials()
    env = os.environ.copy()
    if app_id:
        env["WECHAT_APP_ID"] = app_id
    if app_secret:
        env["WECHAT_APP_SECRET"] = app_secret

    cmd_parts = ["wenyan", "publish", "-f", filepath, "-t", theme, "-h", highlight]
    if platform.system() == "Windows":
        # On Windows, use shell=True with a properly escaped command string
        # Escape special cmd.exe characters in paths
        def cmd_escape(s):
            return str(s).replace("^", "^^").replace("&", "^&").replace("%", "^%").replace("<", "^<").replace(">", "^>").replace("|", "^|").replace('"', '""')
        cmd_str = " ".join(f'"{cmd_escape(p)}"' for p in cmd_parts)
        result = subprocess.run(cmd_str, check=False, env=env, shell=True)
    else:
        # Unix: use list form without shell
        result = subprocess.run(cmd_parts, check=False, env=env)

    if result.returncode == 0:
        print(f"{GREEN}发布成功！{NC}")
        return True

    print(f"{RED}发布失败（exit={result.returncode}）{NC}")
    return False


def search_article_sogou(title: str) -> bool:
    """用搜狗微信搜索验证文章是否可被检索"""
    print(f"\n{YELLOW}用搜狗微信搜索验证文章...{NC}")

    try:
        query = urllib.parse.quote(title)
        url = f"https://weixin.sogou.com/weixin?type=2&query={query}&ie=utf8"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # 检查是否找到相关结果
        if title[:10] in html or query[:10] in html:
            print(f"{GREEN}搜狗验证通过：文章已被检索到！{NC}")
            return True
        else:
            print(f"{YELLOW}搜狗验证：未找到明确匹配结果（可能需等待搜索引擎收录）{NC}")
            return False

    except Exception as e:
        print(f"{YELLOW}搜狗搜索请求失败（不影响发布）: {e}{NC}")
        return False


def show_help():
    print("Usage: publish_and_verify.py <markdown-file> [theme] [highlight]")
    print("Example: publish_and_verify.py article.md lapis solarized-light")


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

    # 发布 + 重试
    for attempt in range(1, PUBLISH_MAX_ATTEMPTS + 1):
        if attempt > 1:
            print(f"{YELLOW}第 {attempt} 次尝试...{NC}")
            time.sleep(PUBLISH_RETRY_DELAY_SEC)

        if publish(filepath, theme, highlight):
            # 发布成功后，提取标题做搜狗验证
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
            title_match = re.search(r"title:\s*([^\n]+)", content)
            if title_match:
                search_article_sogou(title_match.group(1).strip())

            print(f"\n{GREEN}请前往微信公众号后台审核并发布：https://mp.weixin.qq.com/{NC}")
            return 0

        if attempt < PUBLISH_MAX_ATTEMPTS:
            print(f"{YELLOW}{PUBLISH_RETRY_DELAY_SEC} 秒后重试...{NC}")

    print(f"\n{RED}发布失败，已达最大重试次数{NC}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
