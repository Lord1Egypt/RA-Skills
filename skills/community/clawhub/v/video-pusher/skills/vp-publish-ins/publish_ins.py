# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "playwright>=1.40",
# ]
# ///
"""Instagram 自动发布脚本"""
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
            subpath = g.get("platforms", {}).get("ins")
            if not subpath:
                raise ValueError(f"账号组「{group_name}」未登录 Instagram")
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
            page.goto("https://www.instagram.com/")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            if "accounts/login" in page.url or page.locator('input[name="username"]').count() > 0:
                print("⚠️  请在浏览器中完成 Instagram 登录...")
                page.wait_for_url("https://www.instagram.com/", timeout=120000)
                time.sleep(3)

            # 点击「创建」按钮
            try:
                create_sel = '[aria-label="新帖子"], [aria-label="New post"], [aria-label="创建"]'
                page.wait_for_selector(create_sel, timeout=15000)
                page.locator(create_sel).first.click()
                time.sleep(1)
            except Exception:
                print("⚠️  请手动点击「创建」(+) 按钮")

            # 上传文件（可选）
            if file_path:
                try:
                    page.wait_for_selector('input[type="file"]', timeout=15000, state="attached")
                    page.locator('input[type="file"]').first.set_input_files(file_path)
                    print(f"📤 文件已上传：{os.path.basename(file_path)}")
                    time.sleep(4)
                except Exception:
                    print("⚠️  请手动选择文件")

                # 多步骤：裁剪 → 滤镜 → Caption
                for step_label in ["Next", "下一步", "OK"]:
                    try:
                        btn = page.locator(
                            f'button:has-text("{step_label}"), [aria-label="{step_label}"]'
                        ).first
                        if btn.is_visible():
                            btn.click()
                            time.sleep(2)
                    except Exception:
                        pass

            # 填写 Caption（title 作开头）
            try:
                caption_sel = (
                    'textarea[aria-label*="caption"], textarea[placeholder*="caption"], '
                    'div[aria-label*="caption"], textarea[placeholder*="Write"]'
                )
                page.wait_for_selector(caption_sel, timeout=20000)
                caption_area = page.locator(caption_sel).first
                caption_area.click()
                time.sleep(0.5)
                full_text = title
                if description:
                    full_text += "\n" + description
                tag_str = format_tags(tags)
                if tag_str:
                    full_text += "\n" + tag_str
                caption_area.type(full_text, delay=30)
                print("✏️  Caption 已填写")
            except Exception:
                print("⚠️  Caption 请手动填写")

            print("\n✅ 内容填写完毕！请检查后点击【分享 / Share】按钮")
            print("Close the browser window when done.")
            try:
                page.wait_for_event("close", timeout=0)
            except Exception:
                pass
        except Exception:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Instagram auto-publish — multi-step flow (crop → filter → caption), user clicks Share manually",
        epilog='Examples:\n  %(prog)s --file photo.jpg --title "Caption text" --group "GroupA"',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file",        default="",    help="image or video file path, optional")
    parser.add_argument("--title",       required=True, help="caption opening text, required")
    parser.add_argument("--description", default="",    help="additional caption text, optional")
    parser.add_argument("--tags",        default="",    help="hashtags, space-separated, # added automatically, optional")
    parser.add_argument("--group",       required=True, help="account group name (must be logged in via vp-accounts)")
    args = parser.parse_args()
    publish(args.file or None, args.title, args.description, args.tags, args.group)
