# skills/vp-publish-xhs/publish_xhs.py
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "playwright>=1.40",
# ]
# ///
"""小红书自动发布脚本"""
import argparse, time, os, json

PROFILE_BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "profile"
)
ACCOUNTS_FILE = os.path.join(PROFILE_BASE, "accounts.json")


def load_profile_dir(group_name):
    if not os.path.exists(ACCOUNTS_FILE):
        raise FileNotFoundError("accounts.json 不存在，请先创建账号组")
    with open(ACCOUNTS_FILE, encoding="utf-8") as f:
        accounts = json.load(f)
    for i, g in enumerate(accounts):
        if g["name"] == group_name:
            subpath = g.get("platforms", {}).get("xhs")
            if not subpath:
                raise ValueError(f"账号组「{group_name}」未登录小红书")
            return os.path.join(PROFILE_BASE, subpath)
    raise ValueError(f"账号组「{group_name}」不存在")


def clear_locks(profile_dir):
    for lock in ["SingletonLock", "SingletonCookie", "SingletonSocket"]:
        lp = os.path.join(profile_dir, lock)
        if os.path.exists(lp):
            os.remove(lp)


def format_tags(tags):
    if not tags:
        return ""
    return " ".join("#" + t.strip().lstrip("#") for t in tags.split() if t.strip())


def publish(file_path, title, description, tags, group):
    from playwright.sync_api import sync_playwright

    profile_dir = load_profile_dir(group)
    os.makedirs(profile_dir, exist_ok=True)
    clear_locks(profile_dir)

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
        page.goto("https://creator.xiaohongshu.com/publish/publish")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)

        if "login" in page.url or "sign" in page.url:
            print("⚠️  请在浏览器中扫码登录小红书...")
            page.wait_for_url("**/publish/**", timeout=120000)
            time.sleep(2)

        # 切换到视频上传模式
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".mp4", ".mov", ".avi", ".mkv", ".flv", ".m4v"]:
            try:
                btn = page.locator('text=上传视频').first
                if btn.is_visible():
                    btn.click()
                    time.sleep(1)
            except Exception:
                pass

        try:
            page.wait_for_selector('input[type="file"]', timeout=30000, state="attached")
        except Exception:
            input("Please complete login in the browser then press Enter...")

        print(f"📤 正在上传：{os.path.basename(file_path)}")
        page.locator('input[type="file"]').first.set_input_files(file_path)
        time.sleep(8)

        try:
            title_sel = 'input[placeholder*="标题"], input[placeholder*="填写标题"]'
            page.wait_for_selector(title_sel, timeout=60000)
            ti = page.locator(title_sel).first
            ti.click()
            ti.fill(title)
        except Exception:
            print("⚠️  标题请手动填写")

        try:
            desc_area = page.locator('div[contenteditable="true"]').first
            desc_area.click()
            time.sleep(0.5)
            body = description or ""
            if body:
                desc_area.type(body, delay=30)
            tag_str = format_tags(tags)
            if tag_str:
                desc_area.type("\n", delay=30)
                for tag in tag_str.split():
                    desc_area.type(tag, delay=30)
                    time.sleep(0.5)
                    page.keyboard.press("Escape")
                    time.sleep(0.3)
                    desc_area.type(" ", delay=30)
        except Exception:
            print("⚠️  正文请手动填写")

        print("\n✅ 内容填写完毕！请检查后点击【发布】按钮")
        print("Close the browser window when done.")
        try:
            page.wait_for_event("close", timeout=0)
        except Exception:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Xiaohongshu (XHS) auto-publish — opens browser, uploads video/image and fills in content, user clicks publish manually",
        epilog='Examples:\n  %(prog)s --file video.mp4 --title "My Title" --group "GroupA"',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file",        required=True,  help="video or image file path (mp4/mov/jpg/png), required")
    parser.add_argument("--title",       required=True,  help="post title, required")
    parser.add_argument("--description", default="",     help="post body text, optional")
    parser.add_argument("--tags",        default="",     help="hashtags, space-separated, # added automatically, optional")
    parser.add_argument("--group",       required=True,  help="account group name (must be logged in via vp-accounts)")
    args = parser.parse_args()
    publish(args.file, args.title, args.description, args.tags, args.group)
