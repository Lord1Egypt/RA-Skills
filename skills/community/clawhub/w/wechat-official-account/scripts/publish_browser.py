#!/usr/bin/env python3
"""
Create WeChat Official Account (公众号) draft via browser automation.
适用于个人订阅号（无 API 权限）或需要浏览器发文的场景。

每次打开或跳转页面后：等待 → 获取页面代码 → 由模型分析当前状态及下一步操作。
无硬编码，模型根据页面内容动态决策。

Usage:
  pip install playwright openai && playwright install chromium
  export DASHSCOPE_API_KEY=...   # 百炼，与 OpenClaw 主模型一致
  python3 publish_browser.py --title "标题" --content "正文" --cover cover.jpg
"""
import argparse
import os
import re
import sys
from pathlib import Path
from typing import Callable, Optional

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
        "Error: playwright not installed. Run: pip install playwright && playwright install chromium",
        file=sys.stderr,
    )
    sys.exit(1)

from page_analyzer import analyze_page

MP_BASE = "https://mp.weixin.qq.com"
DRAFT_URL = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg?t=operate/appmsg&lang=zh_CN"
APPMSG_URL = "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&lang=zh_CN"

PAGE_WAIT_MS = 3000  # 每次打开/跳转后等待时间


def default_user_data_dir() -> Path:
    base = Path.home() / ".openclaw" / "wechat-mp-browser"
    base.mkdir(parents=True, exist_ok=True)
    return base


def step_screenshot_and_confirm(page, step_name: str, step_num: int, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"step-{step_num:02d}-{step_name}.png"
    try:
        page.screenshot(path=str(path))
        print(f"[步骤 {step_num}] 截图已保存: {path}", file=sys.stderr)
    except Exception as e:
        print(f"截图失败: {e}", file=sys.stderr)
    print("  → 2 秒后自动继续...", file=sys.stderr)
    page.wait_for_timeout(2000)


def md_to_html(text: str) -> str:
    html = text
    html = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html)
    html = re.sub(r"__(.+?)__", r"<b>\1</b>", html)
    html = re.sub(r"\*(.+?)\*", r"<i>\1</i>", html)
    html = re.sub(r"_(.+?)_", r"<i>\1</i>", html)
    html = html.replace("\n", "<br>")
    return html


def wait_for_login(page, timeout_ms: int = 120_000) -> bool:
    try:
        page.wait_for_url(
            lambda url: "mp.weixin.qq.com" in url and "login" not in url.lower(),
            timeout=timeout_ms,
        )
        page.wait_for_timeout(5000)
        for _ in range(6):
            if "login" in page.url.lower():
                page.wait_for_timeout(5000)
                continue
            if page.locator("text=扫码登录").count() > 0:
                page.wait_for_timeout(5000)
                continue
            break
        return "login" not in page.url.lower()
    except Exception:
        return False


def fill_article(
    page,
    *,
    title: str,
    content: str,
    author: str = "",
    cover_path: Optional[Path] = None,
    step_cb: Optional[Callable] = None,
) -> bool:
    page.wait_for_load_state("networkidle", timeout=20000)
    page.wait_for_timeout(3000)

    title_selectors = ["#title", "input[placeholder*='标题']", "[name='title']", "input.title"]
    for sel in title_selectors:
        try:
            inp = page.locator(sel).first
            if inp.count() > 0:
                inp.fill(title[:32], timeout=2000)
                print(f"标题已填入: {title[:32]}", file=sys.stderr)
                break
        except Exception:
            continue
    if step_cb:
        step_cb(page, "填入标题后")

    if author:
        author_selectors = ["#author", "input[placeholder*='作者']", "[name='author']"]
        for sel in author_selectors:
            try:
                inp = page.locator(sel).first
                if inp.count() > 0:
                    inp.fill(author[:16], timeout=2000)
                    break
            except Exception:
                continue

    raw = content[:19000]
    content_html = f"<div>{raw}</div>" if not raw.strip().startswith("<") else raw
    for attempt in range(5):
        try:
            ok = page.evaluate(
                """(html) => {
                return new Promise((resolve) => {
                    const api = window.__MP_Editor_JSAPI__;
                    if (!api) { resolve(false); return; }
                    api.invoke({
                        apiName: 'mp_editor_get_isready',
                        sucCb: (res) => {
                            if (!res || !res.isReady) { resolve(false); return; }
                            api.invoke({
                                apiName: 'mp_editor_set_content',
                                apiParam: { content: html },
                                sucCb: () => resolve(true),
                                errCb: () => resolve(false)
                            });
                        },
                        errCb: () => resolve(false)
                    });
                });
            }""",
                content_html,
            )
            if ok:
                print("正文已通过 mp_editor_set_content 写入", file=sys.stderr)
                break
        except Exception:
            pass
        page.wait_for_timeout(2000)
    else:
        try:
            ok = page.evaluate(
                """(html) => {
                const iframe = document.querySelector('iframe#ueditor_0, iframe[id*="ueditor"]') || document.querySelector('iframe');
                if (!iframe?.contentDocument?.body) return false;
                try {
                    iframe.contentDocument.body.innerHTML = html;
                    return true;
                } catch (e) { return false; }
            }""",
                content_html,
            )
            if ok:
                print("正文已通过 iframe 注入", file=sys.stderr)
        except Exception:
            try:
                editable = page.locator("[contenteditable='true']").first
                if editable.count() > 0:
                    editable.click()
                    editable.evaluate("(el, html) => { el.innerHTML = html; }", content_html)
                    print("正文已通过 contenteditable 注入", file=sys.stderr)
            except Exception as e:
                print(f"正文写入失败: {e}", file=sys.stderr)

    if cover_path and cover_path.exists():
        try:
            file_input = page.locator("input[type='file']").first
            if file_input.count() > 0:
                file_input.set_input_files(str(cover_path), timeout=5000)
            else:
                cover_area = page.locator("#js_cover_area, [class*='cover'], [class*='upload']").first
                if cover_area.count() > 0:
                    cover_area.click()
                    page.wait_for_timeout(500)
                    fi = page.locator("input[type='file']").first
                    if fi.count() > 0:
                        fi.set_input_files(str(cover_path), timeout=5000)
        except Exception as e:
            print(f"Warning: cover upload may have failed: {e}", file=sys.stderr)
    if step_cb:
        step_cb(page, "填入封面后")

    return True


def click_save_draft(page) -> bool:
    """点击「保存为草稿」按钮。"""
    page.wait_for_timeout(1500)
    selectors = [
        "text=保存为草稿",
        "button:has-text('保存为草稿')",
        "a:has-text('保存为草稿')",
        "text=保存",
        "button:has-text('保存')",
        "[class*='save']:has-text('保存')",
    ]
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if el.count() > 0:
                el.click(timeout=3000)
                print("已点击「保存为草稿」", file=sys.stderr)
                page.wait_for_timeout(2000)
                return True
        except Exception:
            continue
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create WeChat Official Account draft via browser (model-driven)"
    )
    parser.add_argument("--title", help="Article title (≤32 chars)")
    parser.add_argument("--content", help="Article body (Markdown or HTML)")
    parser.add_argument("--content-file", help="Read content from file")
    parser.add_argument("--author", default="", help="Author name (≤16 chars)")
    parser.add_argument("--cover", help="Cover image path (jpg/png)")
    parser.add_argument("--headed", action="store_true", default=True)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--user-data-dir", help="Browser profile dir")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--step", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--model", help="LLM model (default: qwen3.5-plus, 百炼)")
    args = parser.parse_args()

    if args.model:
        os.environ["WECHAT_MP_ANALYZER_MODEL"] = args.model

    content = args.content
    if args.content_file:
        p = Path(args.content_file)
        if not p.exists():
            print(f"Error: file not found: {p}", file=sys.stderr)
            return 1
        content = p.read_text(encoding="utf-8")
    if not args.check_only:
        if not args.title:
            print("Error: --title required (unless --check-only)", file=sys.stderr)
            return 1
        if not content:
            print("Error: --content or --content-file required", file=sys.stderr)
            return 1

    if content and not content.strip().startswith("<"):
        content = md_to_html(content)

    cover_path = Path(args.cover) if args.cover else None
    if args.cover and not cover_path.exists():
        print(f"Error: cover not found: {cover_path}", file=sys.stderr)
        return 1

    user_data = Path(args.user_data_dir) if args.user_data_dir else default_user_data_dir()
    step_dir = Path.home() / ".openclaw" / "wechat-steps"
    step_num = [0]

    def step_cb(pg, name: str) -> None:
        if args.step:
            step_num[0] += 1
            step_screenshot_and_confirm(pg, name, step_num[0], step_dir)

    headless = args.headless and not args.headed
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data),
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"],
            permissions=["clipboard-read", "clipboard-write"],
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        # 首次打开首页
        page.goto(MP_BASE, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(PAGE_WAIT_MS)
        if args.step:
            step_num[0] += 1
            step_screenshot_and_confirm(page, "01-打开首页", step_num[0], step_dir)

        if args.check_only:
            result = analyze_page(page)
            print(
                f"state: {result['state']}\nnext_action: {result['next_action']}\nreason: {result['reason']}",
                file=sys.stderr,
            )
            if args.debug:
                (Path.home() / ".openclaw").mkdir(parents=True, exist_ok=True)
                (Path.home() / ".openclaw" / "wechat-page-check.html").write_text(
                    page.content(), encoding="utf-8"
                )
                print("页面 HTML 已保存到 ~/.openclaw/wechat-page-check.html", file=sys.stderr)
            browser.close()
            return 0 if result["state"] != "login_required" else 1

        # 模型驱动主循环
        max_rounds = 30
        for round_idx in range(max_rounds):
            result = analyze_page(page, context=f"目标：创建公众号文章，标题《{args.title}》")
            print(
                f"[分析] state={result['state']} next_action={result['next_action']} reason={result['reason']}",
                file=sys.stderr,
            )

            action = result["next_action"]

            if action == "wait_for_scan":
                print("\n" + "=" * 50, file=sys.stderr)
                print("请使用微信扫描屏幕上的二维码登录", file=sys.stderr)
                print("=" * 50 + "\n", file=sys.stderr)
                if not wait_for_login(page, timeout_ms=args.timeout * 1000):
                    print("登录超时", file=sys.stderr)
                    browser.close()
                    return 1
                page.wait_for_timeout(PAGE_WAIT_MS)
                continue

            if action == "goto_draft":
                url = result.get("url") or DRAFT_URL
                if url.startswith("/"):
                    url = f"https://mp.weixin.qq.com{url}"
                elif not url.startswith("http"):
                    url = DRAFT_URL
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                page.wait_for_load_state("networkidle", timeout=10000)
                page.wait_for_timeout(PAGE_WAIT_MS)
                if args.step:
                    step_num[0] += 1
                    step_screenshot_and_confirm(page, "跳转草稿页", step_num[0], step_dir)
                continue

            if action == "click_new_draft":
                selector = result.get("selector")
                clicked = False
                if selector:
                    try:
                        page.locator(selector).first.click(timeout=3000)
                        clicked = True
                    except Exception:
                        pass
                if not clicked:
                    for sel in ["text=新建图文", "text=新建图文消息", "text=新建", "a:has-text('新建')"]:
                        try:
                            if page.locator(sel).first.count() > 0:
                                page.locator(sel).first.click(timeout=3000)
                                clicked = True
                                break
                        except Exception:
                            continue
                page.wait_for_timeout(PAGE_WAIT_MS)
                if len(browser.pages) > 1:
                    page = browser.pages[-1]
                    page.bring_to_front()
                    page.wait_for_load_state("domcontentloaded", timeout=15000)
                    page.wait_for_timeout(PAGE_WAIT_MS)
                if args.step:
                    step_num[0] += 1
                    step_screenshot_and_confirm(page, "新建图文", step_num[0], step_dir)
                continue

            if action == "fill_article":
                if args.debug:
                    try:
                        page.screenshot(path=str(Path.home() / ".openclaw" / "wechat-debug.png"))
                        (Path.home() / ".openclaw").mkdir(parents=True, exist_ok=True)
                        (Path.home() / ".openclaw" / "wechat-debug.html").write_text(
                            page.content(), encoding="utf-8"
                        )
                    except Exception:
                        pass
                fill_article(
                    page,
                    title=args.title,
                    content=content,
                    author=args.author,
                    cover_path=cover_path,
                    step_cb=step_cb if args.step else None,
                )
                if click_save_draft(page):
                    print("已保存为草稿。")
                else:
                    print("请手动点击「保存为草稿」或「群发」。")
                break

            if action == "done":
                print("流程完成", file=sys.stderr)
                break

            if action == "user_action_required":
                print(f"需用户操作: {result['reason']}", file=sys.stderr)
                # 若在编辑页附近，尝试 fill_article
                if result["state"] == "draft_editor":
                    fill_article(
                        page,
                        title=args.title,
                        content=content,
                        author=args.author,
                        cover_path=cover_path,
                        step_cb=step_cb if args.step else None,
                    )
                    if click_save_draft(page):
                        print("已保存为草稿。")
                    else:
                        print("请手动点击「保存为草稿」或「群发」。")
                break

            # 未知 action，等待后重试
            page.wait_for_timeout(PAGE_WAIT_MS)
        else:
            print("达到最大轮次，未完成流程", file=sys.stderr)

        if args.headed:
            try:
                input("按 Enter 关闭浏览器...")
            except EOFError:
                page.wait_for_timeout(600_000)
        else:
            page.wait_for_timeout(5000)

        browser.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
