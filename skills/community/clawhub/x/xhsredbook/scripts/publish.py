#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publish.py - Publish to Xiaohongshu creator center
Uses persistent browser context to maintain login state across sessions.
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

from config import get_subdir, resolve_profile_dir

# Screenshot directory
SCREENSHOT_DIR = get_subdir("screenshots")

# Default content
FALLBACK_TITLE = "分享一个好东西！"
CONTENT = "今天给大家分享一个超级实用的工具！\n\n#好物分享 #种草 #推荐"


def save_shot(page, name: str) -> str:
    """Save screenshot"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOT_DIR / f"{timestamp}_{name}.png"
    page.screenshot(path=str(path))
    print(f"[Screenshot] {path}")
    return str(path)


def publish(content: str, image_paths, title: str = FALLBACK_TITLE, profile_dir: str | None = None):
    """
    Publish to Xiaohongshu using browser context.

    Args:
        content: Post content text
        image_paths: Single path (str/Path) or list of paths
        title: Title (<20 chars)
        profile_dir: Optional browser profile directory. If omitted, a temporary
            directory is used and login state will not persist after the run.
    """
    # Normalize to list
    if isinstance(image_paths, (str, Path)):
        image_paths = [str(image_paths)]
    else:
        image_paths = [str(p) for p in image_paths]

    # Ensure title is within 20 chars
    if len(title) > 20:
        title = title[:20]
        print(f"[Warning] Title truncated to 20 chars: {title}")

    print(f"\nStarting publish to Xiaohongshu...")
    print(f"[Images] {len(image_paths)} files")
    for ip in image_paths:
        print(f"  - {ip}")
    print(f"[Title] {title}")
    print(f"[Content] {content[:50]}...")

    user_data_dir, persistent = resolve_profile_dir(profile_dir)
    if persistent:
        print(f"[Profile] Using persistent browser profile: {user_data_dir}")
    else:
        print(f"[Profile] Using temporary browser profile: {user_data_dir}")
        print("[Profile] Login/session data will not be kept after this run unless XHS_PROFILE_DIR is set.")

    with sync_playwright() as p:
        # Launch browser context. Persistence is opt-in via profile_dir / XHS_PROFILE_DIR.
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            viewport={"width": 1920, "height": 1080},
            args=["--start-maximized"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        )

        page = context.new_page()

        try:
            # Step 1: Open creator center
            print("\n[1/8] Opening creator center...")
            page.goto("https://creator.xiaohongshu.com/publish/publish", timeout=30000)
            page.wait_for_timeout(3000)
            save_shot(page, "01_landing")

            # Check if we need to login
            try:
                if "login" in page.url.lower() or page.locator('text=扫码登录').first.is_visible(timeout=3000):
                    print("\n[ERROR] Not logged in! Please run save_login.py first to login.")
                    save_shot(page, "01_need_login")
                    raise Exception("Not logged in. Run: python scripts/save_login.py")
            except Exception as e:
                if "Not logged in" in str(e):
                    raise
                # Timeout on checking login means we're probably logged in
                pass

            # Step 1.5: Switch to image/text tab (上传图文)
            # -------------------------------------------------------
            # 小红书创作者中心默认打开"上传视频"tab。
            # 页面上的 file input accept=".mp4,.mov,..." 是视频的。
            # 必须点击"发布笔记"下拉箭头 → "上传图文" 才能切换。
            # 切换后会出现接受图片格式的 file input。
            # 不能靠"点击上传"文字判断，因为视频tab也有这个文字。
            # -------------------------------------------------------
            print("[1.5/8] Switching to image/text upload tab...")
            page.wait_for_timeout(2000)

            # Check: is there already an image-accepting file input?
            has_image_input = False
            try:
                img_inputs = page.locator('input[type="file"]')
                for i in range(img_inputs.count()):
                    accept = img_inputs.nth(i).get_attribute("accept") or ""
                    if any(ext in accept.lower() for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", "image"]):
                        has_image_input = True
                        print("[OK] Already on image/text tab (image file input found)")
                        break
            except Exception:
                pass

            if not has_image_input:
                # Must switch to image/text tab
                # Step A: Click dropdown arrow
                try:
                    dropdown = page.locator('.dropdownBtn').first
                    if dropdown.is_visible(timeout=3000):
                        dropdown.click()
                        print("[OK] Clicked dropdown arrow")
                        page.wait_for_timeout(1500)
                except Exception:
                    try:
                        page.locator('span.btn-text:has-text("发布笔记")').first.click(timeout=3000)
                        print("[OK] Clicked '发布笔记' button")
                        page.wait_for_timeout(1500)
                    except Exception:
                        print("[Debug] Could not click publish menu trigger")

                # Step B: Click visible "上传图文"
                clicked = False
                try:
                    candidates = page.get_by_text("上传图文")
                    for i in range(candidates.count()):
                        el = candidates.nth(i)
                        box = el.bounding_box()
                        if box and box['x'] > 0 and box['y'] > 0:
                            el.click()
                            print(f"[OK] Clicked '上传图文' (element {i}, pos {box['x']:.0f},{box['y']:.0f})")
                            clicked = True
                            page.wait_for_timeout(3000)
                            break
                except Exception as e:
                    print(f"[Debug] get_by_text failed: {e}")

                if not clicked:
                    try:
                        tab = page.locator('.creator-tab:has-text("上传图文")').first
                        tab.click(force=True)
                        print("[OK] Force-clicked creator-tab '上传图文'")
                        page.wait_for_timeout(3000)
                    except Exception:
                        print("[WARNING] Could not click '上传图文' tab")

            # Verify we now have an image file input
            page.wait_for_timeout(2000)
            save_shot(page, "01c_after_tab_switch")

            # Step 2: Find the correct image file input
            print("[2/8] Looking for image upload input...")
            image_input = None
            try:
                all_inputs = page.locator('input[type="file"]')
                count = all_inputs.count()
                print(f"[Debug] Found {count} file inputs")
                for i in range(count):
                    inp = all_inputs.nth(i)
                    accept = inp.get_attribute("accept") or ""
                    print(f"[Debug] Input {i}: accept='{accept}'")
                    if any(ext in accept.lower() for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", "image"]):
                        image_input = inp
                        print(f"[OK] Found image file input (index {i})")
                        break
            except Exception as e:
                print(f"[Debug] File input search error: {e}")

            # If no image-specific input found, try .input-file elements
            if image_input is None:
                try:
                    hidden_inputs = page.locator('.input-file')
                    count = hidden_inputs.count()
                    print(f"[Debug] Found {count} .input-file elements")
                    for i in range(count):
                        inp = hidden_inputs.nth(i)
                        accept = inp.get_attribute("accept") or ""
                        if "mp4" not in accept.lower():
                            image_input = inp
                            print(f"[OK] Found .input-file (index {i}, accept='{accept}')")
                            break
                except Exception:
                    pass

            if image_input is None:
                # Last resort: use any file input that's NOT the video one
                try:
                    all_inputs = page.locator('input[type="file"]')
                    for i in range(all_inputs.count()):
                        accept = all_inputs.nth(i).get_attribute("accept") or ""
                        if "mp4" not in accept:
                            image_input = all_inputs.nth(i)
                            print(f"[OK] Using non-video file input (index {i})")
                            break
                except Exception:
                    pass

            # Step 3: Upload images one by one
            print(f"[3/8] Uploading {len(image_paths)} image(s)...")
            for img_idx, img_path in enumerate(image_paths):
                print(f"  Uploading image {img_idx+1}/{len(image_paths)}: {Path(img_path).name}")
                if image_input:
                    image_input.set_input_files(img_path)
                else:
                    page.locator('input[type="file"]').first.set_input_files(img_path)
                page.wait_for_timeout(3000)

                # After first upload, the file input may change; re-locate for subsequent uploads
                if img_idx < len(image_paths) - 1:
                    try:
                        # Look for the "add more" upload button that appears after first image
                        add_inputs = page.locator('input[type="file"]')
                        count = add_inputs.count()
                        for i in range(count):
                            accept = add_inputs.nth(i).get_attribute("accept") or ""
                            if any(ext in accept.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                                image_input = add_inputs.nth(i)
                                break
                    except Exception:
                        pass

            print(f"[OK] {len(image_paths)} image(s) upload attempted")

            # Wait for image processing and editor to appear
            print("[3.5/8] Waiting for image to process...")
            page.wait_for_timeout(5000)
            save_shot(page, "03_after_image_upload")

            # Try clicking any overlay/confirm/next buttons
            for btn_text in ["下一步", "完成", "确定", "继续"]:
                try:
                    next_btn = page.locator(f'button:has-text("{btn_text}")').first
                    if next_btn.is_visible(timeout=2000):
                        next_btn.click()
                        print(f"[OK] Clicked '{btn_text}' button")
                        page.wait_for_timeout(2000)
                        break
                except Exception:
                    continue

            save_shot(page, "03b_after_next_button")

            # Wait for editor to appear (poll up to 30 seconds)
            print("[3.6/8] Waiting for content editor to appear...")
            editor_selectors = [
                '#post-textarea',
                '.ql-editor',
                '[contenteditable="true"]',
                'div[data-placeholder]',
                'textarea[placeholder*="正文"]',
                'textarea[placeholder*="内容"]',
                'div[data-slate-editor="true"]',
                '.content-editor',
                'div[role="textbox"]',
                'p[data-placeholder]',
            ]

            editor_ready = False
            for wait_round in range(6):  # 6 rounds x 5 sec = 30 sec max
                for selector in editor_selectors:
                    try:
                        el = page.locator(selector).first
                        if el.is_visible(timeout=1000):
                            print(f"[OK] Editor found via {selector} (after {(wait_round+1)*5}s)")
                            editor_ready = True
                            break
                    except Exception:
                        continue
                if editor_ready:
                    break
                # Scroll down to reveal editor if hidden below fold
                page.mouse.wheel(0, 300)
                page.wait_for_timeout(4000)

            if not editor_ready:
                save_shot(page, "03c_editor_not_ready")
                # Dump HTML for debugging
                try:
                    html = page.content()
                    debug_path = SCREENSHOT_DIR / f"{time.strftime('%Y%m%d_%H%M%S')}_page_debug.html"
                    debug_path.write_text(html, encoding="utf-8")
                    print(f"[Debug] Page HTML saved to: {debug_path}")
                except Exception:
                    pass

            # Step 4: Fill content
            print("[4/8] Filling content...")
            save_shot(page, "04_before_content_fill")
            editor_found = False
            for selector in editor_selectors:
                try:
                    editor = page.locator(selector).first
                    if editor.is_visible(timeout=3000):
                        editor.click()
                        page.wait_for_timeout(500)
                        for char in content:
                            page.keyboard.type(char, delay=10)
                        print(f"[OK] Content filled via {selector}")
                        editor_found = True
                        break
                except Exception as e:
                    print(f"[Debug] Selector {selector} failed: {e}")
                    continue

            if not editor_found:
                print("[ERROR] Content editor not found!")
                save_shot(page, "04_editor_not_found")
                # Dump page HTML for debugging
                try:
                    html = page.content()
                    debug_path = SCREENSHOT_DIR / f"{time.strftime('%Y%m%d_%H%M%S')}_page_debug.html"
                    debug_path.write_text(html, encoding="utf-8")
                    print(f"[Debug] Page HTML saved to: {debug_path}")
                except Exception:
                    pass
                raise Exception("Content editor not found")

            page.wait_for_timeout(2000)
            save_shot(page, "04_after_content")

            # Step 5: Try smart title
            print("[5/8] Trying smart title...")
            try:
                smart_title_btn = page.locator('button:has-text("智能标题")').first
                smart_title_btn.click(timeout=3000)
                print("[OK] Smart title button clicked")
                page.wait_for_timeout(3000)
            except Exception as e:
                print(f"[Warning] Smart title button not found: {e}")

            # Step 6: Check title, fill manually if empty
            print("[6/8] Checking and filling title...")
            try:
                title_input = page.locator('input[placeholder*="标题"]').first
                current_title = title_input.input_value()
                if not current_title or len(current_title.strip()) == 0:
                    print("[Warning] Smart title not generated, filling manually")
                    title_input.fill(title)
                    print(f"[OK] Title filled: {title}")
                else:
                    print(f"[OK] Smart title generated: {current_title}")
            except Exception as e:
                print(f"[Warning] Title handling failed: {e}")

            page.wait_for_timeout(1000)
            save_shot(page, "05_before_publish")

            # Step 7: Click publish
            print("[7/8] Clicking publish...")
            publish_btn = page.locator('button:has-text("发布")').first
            publish_btn.click()

            # Step 8: Wait for completion
            print("[8/8] Waiting for completion...")
            page.wait_for_timeout(5000)
            save_shot(page, "06_after_publish")

            print("\n[OK] Publish completed!")

        except Exception as e:
            print(f"\n[ERROR] Publish failed: {e}")
            save_shot(page, "error")
            raise

        finally:
            print("\nBrowser will close in 5 seconds...")
            page.wait_for_timeout(5000)
            context.close()


# Legacy entry point
def publish_to_xiaohongshu(image_path: str, title: str, content: str, profile_dir: str | None = None):
    publish(content, [image_path], title, profile_dir=profile_dir)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Publish to Xiaohongshu")
    parser.add_argument("image_path", help="Image file path")
    parser.add_argument("title", help="Post title (<20 chars)")
    parser.add_argument("content", help="Post content")
    parser.add_argument("--profile-dir", default=None, help="Browser profile directory")
    args = parser.parse_args()

    if not Path(args.image_path).exists():
        print(f"[ERROR] Image not found: {args.image_path}")
        sys.exit(1)

    try:
        publish(args.content, args.image_path, args.title[:20], profile_dir=args.profile_dir)
    except Exception as e:
        print(f"\n[ERROR] Publish failed: {e}")
        sys.exit(1)
