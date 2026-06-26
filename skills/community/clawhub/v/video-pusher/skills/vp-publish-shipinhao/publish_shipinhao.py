# skills/vp-publish-shipinhao/publish_shipinhao.py
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "playwright>=1.40",
# ]
# ///
"""视频号自动发布脚本"""
import argparse, time, os, json

PROFILE_BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "profile"
)
ACCOUNTS_FILE = os.path.join(PROFILE_BASE, "accounts.json")


def load_profile_dir(group_name):
    if not os.path.exists(ACCOUNTS_FILE):
        raise FileNotFoundError("accounts.json 不存在")
    with open(ACCOUNTS_FILE, encoding="utf-8") as f:
        accounts = json.load(f)
    for i, g in enumerate(accounts):
        if g["name"] == group_name:
            subpath = g.get("platforms", {}).get("shipinhao")
            if not subpath:
                raise ValueError(f"账号组「{group_name}」未登录视频号")
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
        try:
            page = context.new_page()
            page.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
            )
            page.goto("https://channels.weixin.qq.com/platform/post/create")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            if "login" in page.url or page.locator('canvas').count() > 0:
                print("⚠️  请用微信扫描浏览器中的二维码登录...")
                page.wait_for_url("**/platform/**", timeout=120000)
                time.sleep(2)

            try:
                page.wait_for_selector('input[type="file"]', timeout=30000, state="attached")
                print(f"📤 正在上传：{os.path.basename(file_path)}")
                page.locator('input[type="file"]').first.set_input_files(file_path)
            except Exception:
                print("⚠️  请手动点击上传按钮选择文件")

            # 等待短标题字段出现（视频处理需要一定时间）
            title_sel = 'input[placeholder*="概括视频主要内容"]'
            try:
                page.wait_for_selector(title_sel, timeout=60000)
            except Exception:
                pass

            # 填写短标题
            try:
                ti = page.locator(title_sel).first
                ti.click()
                ti.fill(title)
                print("✏️  短标题已填写")
            except Exception:
                print("⚠️  短标题请手动填写")

            # 填写视频描述
            try:
                desc_sel = 'div[contenteditable], [role="textbox"], textarea:visible'
                page.wait_for_selector(desc_sel, timeout=10000)
                desc_area = page.locator(desc_sel).first
                desc_area.click()
                time.sleep(0.5)
                body = description or ""
                tag_str = format_tags(tags)
                full_text = body
                if tag_str:
                    full_text += ("\n" if full_text else "") + tag_str
                if full_text:
                    desc_area.fill("")
                    desc_area.type(full_text, delay=30)
                    print("✏️  描述已填写")
            except Exception:
                print("⚠️  描述请手动填写")

            print("\n✅ 内容填写完毕！请检查后点击【发表】按钮")
            print("Close the browser window when done.")
            try:
                page.wait_for_event("close", timeout=0)
            except Exception:
                pass
        except Exception:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="WeChat Channels (Shipinhao) auto-publish — title prepended to body (no separate title field), login via WeChat QR scan, user clicks publish manually",
        epilog='Examples:\n  %(prog)s --file video.mp4 --title "My Title" --group "GroupA"',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file",        required=True,  help="video file path, required")
    parser.add_argument("--title",       required=True,  help="title (prepended to body text — no separate title field in Channels), required")
    parser.add_argument("--description", default="",     help="body text, optional")
    parser.add_argument("--tags",        default="",     help="hashtags, space-separated, # added automatically, optional")
    parser.add_argument("--group",       required=True,  help="account group name (must be logged in via vp-accounts)")
    args = parser.parse_args()
    publish(args.file, args.title, args.description, args.tags, args.group)
