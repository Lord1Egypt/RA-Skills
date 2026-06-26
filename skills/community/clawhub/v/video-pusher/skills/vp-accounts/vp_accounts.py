# skills/vp-accounts/vp_accounts.py
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "playwright>=1.40",
# ]
# ///
import os, sys, json, argparse
from pathlib import Path

# ── 路径常量 ────────────────────────────────────────────────
# 脚本位于 skills/vp-accounts/vp_accounts.py
# 向上三级到达 video-pusher/
PROFILE_BASE = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    ),
    "profile"
)
ACCOUNTS_FILE = os.path.join(PROFILE_BASE, "accounts.json")

PLATFORM_URLS = {
    "douyin":    "https://creator.douyin.com/creator-micro/content/upload",
    "xhs":       "https://creator.xiaohongshu.com/publish/publish",
    "shipinhao": "https://channels.weixin.qq.com/platform/post/create",
    "threads":   "https://www.threads.net/",
    "ins":       "https://www.instagram.com/",
}
PLATFORMS = list(PLATFORM_URLS.keys())

# Quick DOM probe: selector visible within a few seconds = already logged in.
# These platforms are SPAs; the URL does NOT change when the login screen
# appears.  The file-input only renders once the upload UI is shown (logged in).
_ALREADY_LOGGED_IN_SELECTOR = {
    "douyin":    'input[type="file"]',
    "xhs":       'input[type="file"]',
    "shipinhao": 'input[type="file"]',
}

# URL pattern that the page navigates to *after* a successful login.
# Douyin: login success → redirects to /creator-micro/home
# XHS / Shipinhao: no confirmed redirect; fall back to DOM selector.
_POST_LOGIN_URL = {
    "douyin": "**/creator-micro/home**",
}
PLATFORM_NAMES = {
    "douyin": "Douyin", "xhs": "Xiaohongshu", "shipinhao": "WeChat Channels",
    "threads": "Threads", "ins": "Instagram",
}

# ── 纯逻辑函数 ──────────────────────────────────────────────

def load_accounts(path=None):
    """读取 accounts.json，文件不存在时返回空列表"""
    p = Path(path or ACCOUNTS_FILE)
    if not p.exists():
        return []
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def save_accounts(path_or_list, data=None):
    """保存 accounts.json
    用法：save_accounts(accounts)  或  save_accounts(path, accounts)
    """
    if data is None:
        path, data = ACCOUNTS_FILE, path_or_list
    else:
        path = path_or_list
    os.makedirs(os.path.dirname(str(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_profile_subpath(accounts, group_name, platform):
    """返回 '{platform}/group_{index}'，账号组不存在时 raise ValueError"""
    for i, g in enumerate(accounts):
        if g["name"] == group_name:
            return f"{platform}/group_{i}"
    raise ValueError(f"账号组「{group_name}」不存在")

def format_tags(tags):
    """将空格分隔的标签规范化为 '#tag1 #tag2' 格式"""
    if not tags:
        return ""
    return " ".join("#" + t.strip().lstrip("#") for t in tags.split() if t.strip())

def clear_singleton_locks(profile_dir):
    """清理 Chromium 遗留的锁文件，防止 'profile already in use' 错误"""
    for lock in ["SingletonLock", "SingletonCookie", "SingletonSocket"]:
        lp = os.path.join(profile_dir, lock)
        if os.path.exists(lp):
            os.remove(lp)


# ── CLI 命令实现 ────────────────────────────────────────────

def cmd_list():
    accounts = load_accounts()
    output = []
    for g in accounts:
        platforms_status = {p: p in g.get("platforms", {}) for p in PLATFORMS}
        output.append({"name": g["name"], "platforms": platforms_status})
    print(json.dumps(output, ensure_ascii=False, indent=2))

def cmd_add(name):
    accounts = load_accounts()
    if any(g["name"] == name for g in accounts):
        print(f"Error: account group '{name}' already exists.", file=sys.stderr)
        sys.exit(1)
    accounts.append({"name": name, "platforms": {}})
    save_accounts(accounts)
    print(f"✅ Account group '{name}' created.")

def cmd_delete(name):
    accounts = load_accounts()
    new = [g for g in accounts if g["name"] != name]
    if len(new) == len(accounts):
        print(f"Error: account group '{name}' not found.", file=sys.stderr)
        sys.exit(1)
    save_accounts(new)
    print(f"✅ Account group '{name}' deleted.")

def cmd_login(group_name, platform):
    import time
    from playwright.sync_api import sync_playwright

    accounts = load_accounts()
    group = next((g for g in accounts if g["name"] == group_name), None)
    if group is None:
        print(f"Error: account group '{group_name}' not found. Create it first with 'add'.", file=sys.stderr)
        sys.exit(1)

    subpath = get_profile_subpath(accounts, group_name, platform)
    profile_dir = os.path.join(PROFILE_BASE, subpath)
    os.makedirs(profile_dir, exist_ok=True)
    clear_singleton_locks(profile_dir)

    url = PLATFORM_URLS[platform]
    name = PLATFORM_NAMES[platform]
    print(f"\nOpening {name} login page...")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
            ignore_default_args=["--enable-automation"],
            no_viewport=True,
        )
        page = context.new_page()
        page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        )
        try:
            page.goto(url)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            if platform in _ALREADY_LOGGED_IN_SELECTOR:
                selector = _ALREADY_LOGGED_IN_SELECTOR[platform]
                # Quick probe: upload UI visible within 3 s → already logged in
                try:
                    page.wait_for_selector(selector, timeout=3000)
                    print(f"✅ Already logged in to {name}. Close the browser to continue.")
                except Exception:
                    print(f"Log in to {name} in the browser.\n")
                    # Douyin: detect login via URL change; others: just wait for close
                    if platform in _POST_LOGIN_URL:
                        try:
                            page.wait_for_url(_POST_LOGIN_URL[platform], timeout=294_000)
                            print(f"✅ Login successful! Close the browser to save session.")
                        except Exception:
                            pass
                    else:
                        print("Close the browser window when done.")
            else:
                # Threads / Instagram: manual close
                print(f"Log in to {name} in the browser.\n")
                print("Close the browser window when done.")

            # All platforms: wait for user to close the window (macOS X button
            # closes the page, not the full context, so listen to page close)
            page.wait_for_event("close", timeout=0)
        except Exception:
            pass  # browser closed at any point — that's fine

    group.setdefault("platforms", {})[platform] = subpath
    save_accounts(accounts)
    print(f"✅ {name} session saved to {profile_dir}")


def cmd_remove_platform(group_name, platform):
    import shutil
    accounts = load_accounts()
    group = next((g for g in accounts if g["name"] == group_name), None)
    if group is None:
        print(f"Error: account group '{group_name}' not found.", file=sys.stderr)
        sys.exit(1)
    subpath = group.get("platforms", {}).pop(platform, None)
    if subpath is None:
        print(f"Error: '{platform}' is not logged in under group '{group_name}'.", file=sys.stderr)
        sys.exit(1)
    save_accounts(accounts)
    # Remove the profile directory for this platform
    profile_dir = os.path.join(PROFILE_BASE, subpath)
    if os.path.isdir(profile_dir):
        shutil.rmtree(profile_dir)
    print(f"✅ {PLATFORM_NAMES[platform]} removed from group '{group_name}'.")


def cmd_status(group_name, platform):
    if platform not in PLATFORMS:
        print(f"Error: unsupported platform '{platform}'. Choose from: {PLATFORMS}", file=sys.stderr)
        sys.exit(1)
    accounts = load_accounts()
    group = next((g for g in accounts if g["name"] == group_name), None)
    if group is None:
        print(f"Error: account group '{group_name}' not found.", file=sys.stderr)
        sys.exit(1)
    # 两步验证：1. accounts.json 中有此平台 key；2. profile 目录存在
    subpath = group.get("platforms", {}).get(platform)
    if not subpath:
        sys.exit(1)
    profile_dir = os.path.join(PROFILE_BASE, subpath)
    if not os.path.isdir(profile_dir):
        sys.exit(1)
    sys.exit(0)

# ── 入口 ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="vp_accounts",
        description="Account group manager for multi-platform publishing",
        epilog='Examples:\n  %(prog)s add "GroupA"\n  %(prog)s login "GroupA" douyin\n  %(prog)s remove "GroupA" douyin\n  %(prog)s list',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True, metavar="command")

    sub.add_parser("list", help="list all account groups and their login status")

    p_add = sub.add_parser("add", help="create a new account group")
    p_add.add_argument("name", metavar="group-name")

    p_del = sub.add_parser("delete", help="delete an account group")
    p_del.add_argument("name", metavar="group-name")

    p_login = sub.add_parser("login", help="open browser to log in; session saved automatically on close")
    p_login.add_argument("name", metavar="group-name")
    p_login.add_argument("platform", choices=PLATFORMS, metavar="platform", help=f"one of: {', '.join(PLATFORMS)}")

    p_status = sub.add_parser("status", help="check login status (exit 0=logged in, exit 1=not logged in)")
    p_status.add_argument("name", metavar="group-name")
    p_status.add_argument("platform", choices=PLATFORMS, metavar="platform", help=f"one of: {', '.join(PLATFORMS)}")

    p_remove = sub.add_parser("remove", help="remove a platform login from an account group")
    p_remove.add_argument("name", metavar="group-name")
    p_remove.add_argument("platform", choices=PLATFORMS, metavar="platform", help=f"one of: {', '.join(PLATFORMS)}")

    args = parser.parse_args()

    if args.cmd == "list":
        cmd_list()
    elif args.cmd == "add":
        cmd_add(args.name)
    elif args.cmd == "delete":
        cmd_delete(args.name)
    elif args.cmd == "login":
        cmd_login(args.name, args.platform)
    elif args.cmd == "status":
        cmd_status(args.name, args.platform)
    elif args.cmd == "remove":
        cmd_remove_platform(args.name, args.platform)

if __name__ == "__main__":
    main()
