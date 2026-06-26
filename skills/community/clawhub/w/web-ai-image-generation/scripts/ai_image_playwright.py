#!/usr/bin/env python3
"""Standalone Playwright automation for Gemini / ChatGPT image generation.

This script is intentionally self-contained and does not import application code.
It opens the web UI, submits a prompt, waits for generated images, and saves
results to a local output directory.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import glob
import logging
import os
from pathlib import Path
from typing import Iterable

from playwright.async_api import Page, async_playwright

logger = logging.getLogger("ai_image_playwright")

DEFAULT_CHROME_PATH = "/usr/bin/google-chrome"
SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PROFILE_DIR = SKILL_DIR / ".runtime" / "profile"
DEFAULT_OUTPUT_DIR = SKILL_DIR / ".runtime" / "output"


def build_prompt(title: str, description: str = "") -> str:
    """Build a vertical short-video cover prompt."""
    title = (title or "").strip()
    description = (description or "").strip()
    if not title:
        raise ValueError("title/prompt cannot be empty")

    if description:
        desc_part = description if "演示" in description else f"视频里演示了{description}。"
    else:
        desc_part = ""

    return (
        f"请为短视频生成一张竖屏封面图片（3:4比例），主题是：{title}。{desc_part}\n\n"
        f"要求：标题文字必须清晰醒目并包含：'{title}'；画面适合手机信息流；"
        f"构图自然、有设计感、高清高质量；不要包含 APP 界面、手机边框、点赞评论按钮、状态栏或导航栏。"
    )


def clean_profile_locks(profile_dir: Path) -> None:
    """Remove stale Chromium profile lock files."""
    for lock_file in glob.glob(str(profile_dir / "**" / "LOCK"), recursive=True):
        try:
            os.remove(lock_file)
        except OSError:
            pass
    for name in ["SingletonLock", "SingletonSocket", "SingletonCookie"]:
        try:
            os.remove(profile_dir / name)
        except OSError:
            pass


async def fill_first_available(page: Page, selectors: Iterable[str], text: str) -> bool:
    for selector in selectors:
        try:
            locator = page.locator(selector).first
            await locator.wait_for(state="visible", timeout=5000)
            await locator.click()
            await locator.fill(text)
            return True
        except Exception:
            continue
    return False


async def click_first_available(page: Page, selectors: Iterable[str]) -> bool:
    for selector in selectors:
        try:
            locator = page.locator(selector).first
            await locator.wait_for(state="visible", timeout=5000)
            await locator.click()
            return True
        except Exception:
            continue
    return False


async def click_text_fallback(page: Page, labels: Iterable[str]) -> bool:
    for label in labels:
        try:
            locator = page.get_by_text(label, exact=False).first
            await locator.wait_for(state="visible", timeout=5000)
            await locator.click()
            return True
        except Exception:
            continue
    return False


async def wait_for_large_images(page: Page, platform: str, timeout_seconds: int = 180) -> None:
    """Wait until generated large image candidates appear and become stable."""
    await page.wait_for_timeout(20_000)
    waited = 20
    last_count = 0
    stable_count = 0

    while waited < timeout_seconds:
        await page.wait_for_timeout(5_000)
        waited += 5
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1_000)

        count = await count_image_candidates(page, platform)
        logger.info("found %s image candidates after %ss", count, waited)
        if count > 0:
            if count == last_count:
                stable_count += 1
                if stable_count >= 3:
                    await page.wait_for_timeout(10_000)
                    return
            else:
                stable_count = 0
                last_count = count


async def count_image_candidates(page: Page, platform: str) -> int:
    images = await page.query_selector_all("img")
    count = 0
    for img in images:
        try:
            info = await img.evaluate(
                """el => {
                    const rect = el.getBoundingClientRect();
                    return {
                        width: rect.width || el.naturalWidth || el.width || 0,
                        height: rect.height || el.naturalHeight || el.height || 0,
                        src: el.src || '',
                        alt: el.alt || '',
                        className: el.className || ''
                    };
                }"""
            )
            if platform == "chatgpt":
                is_candidate = (
                    info["width"] >= 300
                    and info["height"] >= 300
                    and (
                        "chatgpt.com/backend-api/estuary/content" in info["src"]
                        or "已生成图片" in info["alt"]
                        or ("absolute" in info["className"] and "z-1" in info["className"])
                        or ("chatgpt.com" in info["src"] and info["width"] >= 500 and info["height"] >= 500)
                        or (info["src"].startswith("http") and info["width"] >= 500 and info["height"] >= 500)
                    )
                )
            else:
                is_candidate = info["width"] >= 300 and info["height"] >= 300
            if is_candidate:
                count += 1
        except Exception:
            continue
    return count


async def save_canvas_image(page: Page, img, dest_path: Path) -> bool:
    try:
        await img.scroll_into_view_if_needed()
        await page.wait_for_timeout(500)
        data_url = await img.evaluate(
            """el => {
                const canvas = document.createElement('canvas');
                canvas.width = el.naturalWidth || el.width || 1024;
                canvas.height = el.naturalHeight || el.height || 1024;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(el, 0, 0);
                return canvas.toDataURL('image/jpeg', 0.95);
            }"""
        )
        if data_url and data_url.startswith("data:image"):
            _, encoded = data_url.split(",", 1)
            dest_path.write_bytes(base64.b64decode(encoded))
            return dest_path.exists() and dest_path.stat().st_size > 10_000
    except Exception as exc:
        logger.debug("canvas extraction failed: %s", exc)
    return False


async def download_generated_images(page: Page, platform: str, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    images = await page.query_selector_all("img")
    candidates = []

    print(f"[download] Total images on page: {len(images)}")

    for img in images:
        try:
            info = await img.evaluate(
                """el => {
                    const rect = el.getBoundingClientRect();
                    return {
                        width: rect.width || el.naturalWidth || el.width || 0,
                        height: rect.height || el.naturalHeight || el.height || 0,
                        src: el.src || '',
                        alt: el.alt || '',
                        className: el.className || ''
                    };
                }"""
            )
            # 调试：打印所有大图片
            if info["width"] >= 200 and info["height"] >= 200:
                print(f"[download] Image found: {info['width']}x{info['height']}, src: {info['src'][:80]}..., alt: '{info['alt']}', class: '{info['className'][:50]}'")

            if platform == "chatgpt":
                is_candidate = (
                    info["width"] >= 300
                    and info["height"] >= 300
                    and (
                        "chatgpt.com/backend-api/estuary/content" in info["src"]
                        or "已生成图片" in info["alt"]
                        or ("absolute" in info["className"] and "z-1" in info["className"])
                        or ("chatgpt.com" in info["src"] and info["width"] >= 500 and info["height"] >= 500)
                        or (info["src"].startswith("http") and info["width"] >= 500 and info["height"] >= 500)
                    )
                )
            else:
                is_candidate = info["width"] >= 400 and info["height"] >= 400
            if is_candidate:
                print(f"[download] ✓ Candidate matched: {info['width']}x{info['height']}, src: {info['src'][:60]}...")
                candidates.append((img, info))
        except Exception:
            continue

    print(f"[download] Found {len(candidates)} candidate images")

    saved: list[Path] = []
    for index, (img, info) in enumerate(candidates[-4:], start=1):
        dest_path = output_dir / f"{platform}_image_{index}.jpg"
        src = info.get("src", "")
        print(f"[download] Processing image {index}: {src[:60]}...")

        if platform == "chatgpt" and src.startswith("http"):
            try:
                print(f"[download] Trying page.request.get()...")
                response = await page.request.get(src)
                if response.ok:
                    dest_path.write_bytes(await response.body())
                    print(f"[download] ✓ Downloaded via page.request")
            except Exception as exc:
                print(f"[download] page.request failed: {exc}")

        if (not dest_path.exists() or dest_path.stat().st_size <= 10_000) and src.startswith("http"):
            if platform == "gemini" and any(domain in src for domain in ["googleusercontent.com", "gstatic.com"]):
                try:
                    response = await page.request.get(src)
                    if response.ok:
                        dest_path.write_bytes(await response.body())
                except Exception as exc:
                    logger.debug("gemini http download failed: %s", exc)

        if not dest_path.exists() or dest_path.stat().st_size <= 10_000:
            print(f"[download] Trying Canvas extraction...")
            await save_canvas_image(page, img, dest_path)

        if dest_path.exists() and dest_path.stat().st_size > 10_000:
            print(f"[download] ✓ Saved: {dest_path} ({dest_path.stat().st_size} bytes)")
            saved.append(dest_path)
        else:
            print(f"[download] ✗ Failed to save image {index}")
            dest_path.unlink(missing_ok=True)

    return saved


async def run_generation(platform: str, prompt: str, output_dir: Path, profile_dir: Path, chrome_path: str | None) -> list[Path]:
    if platform not in {"gemini", "chatgpt"}:
        raise ValueError("platform must be 'gemini' or 'chatgpt'")

    clean_profile_locks(profile_dir)
    profile_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        executable_path = chrome_path if chrome_path and Path(chrome_path).exists() else None
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
            executable_path=executable_path,
            args=["--lang=zh-CN", "--disable-blink-features=AutomationControlled", "--no-sandbox"],
            viewport={"width": 1280, "height": 800},
        )
        page = context.pages[0] if context.pages else await context.new_page()
        url = "https://gemini.google.com/app" if platform == "gemini" else "https://chatgpt.com/"
        await page.goto(url, wait_until="domcontentloaded", timeout=60_000)
        await page.wait_for_timeout(5_000)

        if "accounts.google.com" in page.url or "signin" in page.url.lower() or "auth" in page.url.lower():
            print("请在打开的浏览器窗口中完成登录，程序会等待 120 秒。")
            await page.wait_for_timeout(120_000)
            # 登录后等待页面跳转到目标站点
            try:
                await page.wait_for_url(lambda url: "gemini.google.com" in url or "chatgpt.com" in url, timeout=30_000)
            except Exception:
                pass
            await page.wait_for_timeout(3_000)

        if platform == "gemini":
            await click_text_fallback(page, ["制作图片", "生成图片", "Create image", "Generate image"])
            await page.wait_for_timeout(2_000)
            filled = await fill_first_available(
                page,
                [
                    'rich-textarea [contenteditable="true"]',
                    '#prompt-textarea.ProseMirror[contenteditable="true"]',
                    '[aria-label*="Gemini"][contenteditable="true"]',
                    '[contenteditable="true"]',
                ],
                prompt,
            )
            if not filled:
                raise RuntimeError("cannot find Gemini prompt input")
            sent = await click_first_available(page, ['button[aria-label="发送消息"]', 'button[aria-label*="Send"]'])
        else:
            await click_text_fallback(page, ["生成图片", "Create image", "Generate image"])
            await page.wait_for_timeout(2_000)
            filled = await fill_first_available(
                page,
                [
                    '#prompt-textarea.ProseMirror[contenteditable="true"]',
                    '[aria-label*="ChatGPT"][contenteditable="true"]',
                    '[contenteditable="true"]',
                    'textarea#prompt-textarea',
                    'textarea',
                ],
                prompt,
            )
            if not filled:
                raise RuntimeError("cannot find ChatGPT prompt input")
            sent = await click_first_available(page, ["#composer-submit-button", 'button[aria-label="发送提示"]', 'button[aria-label*="Send"]'])

        if not sent:
            await page.keyboard.press("Enter")

        await wait_for_large_images(page, platform)
        saved = await download_generated_images(page, platform, output_dir)
        await context.close()
        return saved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate images with Gemini or ChatGPT web UI via Playwright.")
    parser.add_argument("--platform", choices=["gemini", "chatgpt"], required=True)
    parser.add_argument("--prompt", help="Prompt text. If omitted, --title is used to build a cover prompt.")
    parser.add_argument("--title", help="Video title used by the built-in cover prompt builder.")
    parser.add_argument("--description", default="", help="Optional video description used by the built-in cover prompt builder.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--profile-dir", type=Path, default=DEFAULT_PROFILE_DIR)
    parser.add_argument("--chrome-path", default=DEFAULT_CHROME_PATH)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s: %(message)s")
    prompt = args.prompt or build_prompt(args.title or "", args.description)
    saved = await run_generation(args.platform, prompt, args.output_dir, args.profile_dir, args.chrome_path)
    for path in saved:
        print(path)


if __name__ == "__main__":
    asyncio.run(main())
