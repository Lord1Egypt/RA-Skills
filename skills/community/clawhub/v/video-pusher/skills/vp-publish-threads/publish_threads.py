# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "playwright>=1.40",
# ]
# ///
"""Threads 自动发布脚本"""
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
            subpath = g.get("platforms", {}).get("threads")
            if not subpath:
                raise ValueError(f"账号组「{group_name}」未登录 Threads")
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
            page.goto("https://www.threads.com/")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            if "login" in page.url or page.locator('input[name="username"]').count() > 0:
                print("⚠️  请在浏览器中完成 Threads 登录...")
                page.wait_for_url("https://www.threads.com/", timeout=120000)
                time.sleep(3)

            # 打开发帖弹窗：先尝试导航栏"创建"按钮，再试首页文本框
            compose_btn_sel = (
                '[aria-label="创建"], [aria-label="Create"], '
                '[aria-label="New thread"], [aria-label="发帖"], '
                'a[href="/new-post"]'
            )
            compose_input_sel = (
                '[aria-label="文本栏为空白。请输入内容，撰写新帖子。"], '
                '[aria-label="Empty text field. Type to compose a new post."]'
            )
            try:
                page.wait_for_selector(compose_btn_sel, timeout=10000)
                page.locator(compose_btn_sel).first.click()
                time.sleep(1)
            except Exception:
                try:
                    page.wait_for_selector(compose_input_sel, timeout=10000)
                    page.locator(compose_input_sel).first.click()
                    time.sleep(1)
                except Exception:
                    print("⚠️  请手动点击发帖输入框")

            # 填写文案（先填文字，与原版一致）
            try:
                text_sel = 'div[contenteditable="true"], textarea[placeholder]'
                page.wait_for_selector(text_sel, timeout=15000)
                text_area = page.locator(text_sel).first
                text_area.click()
                full_text = title
                if description:
                    full_text += "\n" + description
                tag_str = format_tags(tags)
                if tag_str:
                    full_text += "\n" + tag_str
                text_area.type(full_text, delay=30)
                print("✏️  文案已填写")
            except Exception:
                print("⚠️  文案请手动填写")

            # 上传媒体（可选）：先尝试点击媒体按钮触发 file input
            if file_path:
                try:
                    media_btn_sel = (
                        '[aria-label*="photo"], [aria-label*="图片"], '
                        '[aria-label*="video"], [aria-label*="视频"], '
                        '[aria-label*="media"], [aria-label*="媒体"], '
                        '[aria-label*="Add"], [aria-label*="添加"]'
                    )
                    try:
                        upload_btn = page.locator(media_btn_sel).first
                        if upload_btn.is_visible():
                            upload_btn.click()
                            time.sleep(1)
                    except Exception:
                        pass
                    page.wait_for_selector('input[type="file"]', timeout=10000, state="attached")
                    page.locator('input[type="file"]').first.set_input_files(file_path)
                    print(f"📤 文件已上传：{os.path.basename(file_path)}")
                    time.sleep(4)
                except Exception:
                    print("⚠️  请手动上传文件")

            print("\n✅ 内容填写完毕！请检查后点击【发帖】按钮")
            print("Close the browser window when done.")
            try:
                page.wait_for_event("close", timeout=0)
            except Exception:
                pass
        except Exception:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Threads auto-publish — supports text-only or media posts, user clicks post manually",
        epilog='Examples:\n  %(prog)s --title "Post text" --group "GroupA"\n  %(prog)s --file photo.jpg --title "Post text" --group "GroupA"',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file",        default="",    help="image or video file path, optional (omit for text-only post)")
    parser.add_argument("--title",       required=True, help="post text (used as opening line), required")
    parser.add_argument("--description", default="",    help="additional body text, optional")
    parser.add_argument("--tags",        default="",    help="hashtags, space-separated, # added automatically, optional")
    parser.add_argument("--group",       required=True, help="account group name (must be logged in via vp-accounts)")
    args = parser.parse_args()
    publish(args.file or None, args.title, args.description, args.tags, args.group)
