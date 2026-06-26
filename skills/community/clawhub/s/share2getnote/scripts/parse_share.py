#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["playwright"]
# ///
"""Parse ChatGPT or Gemini shared conversation links and extract Q&A pairs.

Usage: uv run parse_share.py <url>

Output: JSON array to stdout
  [{"title": "question text", "content": "answer in markdown"}, ...]

Exit codes:
  0 - Success
  1 - Unsupported URL
  2 - Page load failed / timeout
  3 - No conversation data found
  4 - Playwright not installed / browser not installed
"""

import json
import re
import sys

# ── URL detection ──────────────────────────────────────────────────────────

CHATGPT_PATTERNS = [
    re.compile(r"https?://(chat\.openai\.com|chatgpt\.com)/share/"),
    re.compile(r"https?://chatgpt\.com/s/t_"),
]
GEMINI_PATTERNS = [
    re.compile(r"https?://gemini\.google\.com/share/"),
    re.compile(r"https?://g\.co/gemini/share/"),
]


def detect_platform(url: str) -> str:
    for pat in CHATGPT_PATTERNS:
        if pat.search(url):
            return "chatgpt"
    for pat in GEMINI_PATTERNS:
        if pat.search(url):
            return "gemini"
    return ""


# ── ChatGPT extraction JS ─────────────────────────────────────────────────

CHATGPT_EXTRACT_JS = """
() => {
    const messages = [];

    // Strategy 1: data-message-author-role attribute
    const roleEls = document.querySelectorAll('[data-message-author-role]');
    if (roleEls.length > 0) {
        roleEls.forEach(el => {
            const role = el.getAttribute('data-message-author-role');
            // Get the markdown/text content from the message container
            const contentEl = el.querySelector('.markdown, .whitespace-pre-wrap')
                              || el;
            messages.push({
                role: role,
                content: contentEl.innerText.trim()
            });
        });
        return messages;
    }

    // Strategy 2: article elements (newer layout)
    const articles = document.querySelectorAll('article');
    if (articles.length > 0) {
        articles.forEach((article, idx) => {
            // In share pages, articles alternate user/assistant
            // Check for heading or avatar indicators
            const heading = article.querySelector('h5, h6, [data-message-author-role]');
            let role = idx % 2 === 0 ? 'user' : 'assistant';
            if (heading) {
                const text = heading.innerText.toLowerCase();
                if (text.includes('you') || text.includes('user')) role = 'user';
                else role = 'assistant';
            }
            const contentEl = article.querySelector('.markdown, .whitespace-pre-wrap')
                              || article;
            messages.push({
                role: role,
                content: contentEl.innerText.trim()
            });
        });
        return messages;
    }

    // Strategy 3: role-based class patterns
    const allDivs = document.querySelectorAll('[class*="agent-turn"], [class*="user-turn"], [class*="human"], [class*="assistant"]');
    if (allDivs.length > 0) {
        allDivs.forEach(div => {
            const cls = div.className || '';
            let role = 'assistant';
            if (cls.includes('user') || cls.includes('human')) role = 'user';
            messages.push({
                role: role,
                content: div.innerText.trim()
            });
        });
        return messages;
    }

    // Strategy 4: Broad fallback - look for turn containers
    const turns = document.querySelectorAll('[data-testid*="conversation-turn"]');
    if (turns.length > 0) {
        turns.forEach((turn, idx) => {
            messages.push({
                role: idx % 2 === 0 ? 'user' : 'assistant',
                content: turn.innerText.trim()
            });
        });
        return messages;
    }

    return messages;
}
"""

# ── Gemini extraction JS ──────────────────────────────────────────────────

GEMINI_EXTRACT_JS = """
() => {
    const messages = [];

    // Strategy 1: user-query and model-response containers
    const userQueries = document.querySelectorAll(
        'user-query, .user-query, [class*="query-text"], [class*="user-message"]'
    );
    const modelResponses = document.querySelectorAll(
        'model-response, .model-response, [class*="response-text"], [class*="model-message"]'
    );

    if (userQueries.length > 0 || modelResponses.length > 0) {
        // Interleave user queries and model responses
        const maxLen = Math.max(userQueries.length, modelResponses.length);
        for (let i = 0; i < maxLen; i++) {
            if (i < userQueries.length) {
                messages.push({
                    role: 'user',
                    content: userQueries[i].innerText.trim()
                });
            }
            if (i < modelResponses.length) {
                // Try to get just the text content, excluding UI buttons
                const contentEl = modelResponses[i].querySelector(
                    '.markdown, .response-content, .model-response-text'
                ) || modelResponses[i];
                messages.push({
                    role: 'assistant',
                    content: contentEl.innerText.trim()
                });
            }
        }
        return messages;
    }

    // Strategy 2: conversation-turn containers
    const turns = document.querySelectorAll(
        '[class*="conversation-turn"], [class*="turn-container"], .turn'
    );
    if (turns.length > 0) {
        turns.forEach((turn, idx) => {
            messages.push({
                role: idx % 2 === 0 ? 'user' : 'assistant',
                content: turn.innerText.trim()
            });
        });
        return messages;
    }

    // Strategy 3: Broad fallback - find alternating message blocks
    const msgBlocks = document.querySelectorAll(
        'message-content, [class*="message"], [role="presentation"]'
    );
    if (msgBlocks.length > 0) {
        msgBlocks.forEach((block, idx) => {
            const text = block.innerText.trim();
            if (text.length > 0) {
                messages.push({
                    role: idx % 2 === 0 ? 'user' : 'assistant',
                    content: text
                });
            }
        });
        return messages;
    }

    return messages;
}
"""


# ── Core logic ─────────────────────────────────────────────────────────────


def pair_messages(raw_messages: list) -> list[dict]:
    """Pair consecutive user/assistant messages into Q&A turns."""
    pairs = []
    i = 0
    while i < len(raw_messages):
        msg = raw_messages[i]
        if msg["role"] == "user":
            question = msg["content"]
            answer = ""
            # Collect all consecutive assistant messages as the answer
            j = i + 1
            while j < len(raw_messages) and raw_messages[j]["role"] == "assistant":
                if answer:
                    answer += "\n\n"
                answer += raw_messages[j]["content"]
                j += 1
            if answer:
                pairs.append({"question": question, "answer": answer})
            i = j
        else:
            # Skip orphan assistant messages
            i += 1
    return pairs


def format_title(question: str, index: int, total: int) -> str:
    """Format the note title from the user's question."""
    # Use first line only
    first_line = question.split("\n")[0].strip()
    # Truncate if too long
    if len(first_line) > 100:
        first_line = first_line[:97] + "..."
    # Add turn prefix for multi-turn conversations
    if total > 1:
        return f"[{index}/{total}] {first_line}"
    return first_line


def format_output(pairs: list[dict], url: str, platform: str) -> list[dict]:
    """Format Q&A pairs into the final output structure."""
    total = len(pairs)
    results = []
    platform_label = "ChatGPT" if platform == "chatgpt" else "Gemini"
    for i, pair in enumerate(pairs, 1):
        title = format_title(pair["question"], i, total)
        content = pair["answer"]
        # Append source info
        content += f"\n\n---\n*来源: [{platform_label} 分享]({url}) - 第 {i}/{total} 轮*"
        results.append({"title": title, "content": content})
    return results


async def fetch_and_extract(url: str, platform: str, timeout: int = 60) -> tuple[list[dict], str]:
    """Use Playwright to fetch page and extract conversation data.

    Returns (raw_messages, page_title).
    """
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
        )
        page = await context.new_page()

        try:
            # Use domcontentloaded instead of networkidle - SPA pages may never
            # reach networkidle due to persistent WebSocket/SSE connections
            await page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
        except Exception as e:
            await browser.close()
            print(f"页面加载失败: {e}", file=sys.stderr)
            sys.exit(2)

        # Detect expired/invalid share links by checking for redirects
        current_url = page.url
        if "share_not_found" in current_url or "not_found" in current_url:
            await browser.close()
            print("分享链接已过期或不存在。", file=sys.stderr)
            sys.exit(2)
        if platform == "chatgpt" and "/share/" not in current_url and "/s/t_" not in current_url:
            await browser.close()
            print(
                f"页面被重定向到 {current_url}，分享链接可能已过期或需要登录。",
                file=sys.stderr,
            )
            sys.exit(2)

        # Platform-specific: wait for content selectors to appear in the rendered DOM
        content_found = False
        if platform == "chatgpt":
            selectors = [
                "[data-message-author-role]",
                "article",
                "[data-testid*='conversation-turn']",
            ]
            for sel in selectors:
                try:
                    await page.wait_for_selector(sel, timeout=30000)
                    content_found = True
                    break
                except Exception:
                    continue
        else:
            selectors = [
                "user-query, .user-query",
                "model-response, .model-response",
                "[class*='conversation-turn']",
                "message-content",
            ]
            for sel in selectors:
                try:
                    await page.wait_for_selector(sel, timeout=30000)
                    content_found = True
                    break
                except Exception:
                    continue

        if not content_found:
            # Last resort: wait a fixed time for JS to render
            await page.wait_for_timeout(8000)

        # Small extra wait to ensure all dynamic content has finished rendering
        await page.wait_for_timeout(2000)

        # Extract messages
        if platform == "chatgpt":
            raw = await page.evaluate(CHATGPT_EXTRACT_JS)
        else:
            raw = await page.evaluate(GEMINI_EXTRACT_JS)

        # Extract page title for fallback when no user messages exist
        page_title = await page.title()

        await browser.close()
        return raw, page_title


def main():
    if len(sys.argv) < 2:
        print("用法: python parse_share.py <url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1].strip()
    platform = detect_platform(url)
    if not platform:
        print(
            f"不支持的 URL: {url}\n"
            "支持的格式:\n"
            "  - https://chatgpt.com/share/...\n"
            "  - https://chatgpt.com/s/t_...\n"
            "  - https://chat.openai.com/share/...\n"
            "  - https://gemini.google.com/share/...\n"
            "  - https://g.co/gemini/share/...",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check Playwright is installed (when run via uv, it's auto-installed)
    try:
        import playwright  # noqa: F401
    except ImportError:
        print(
            "Playwright 未安装。请使用 uv 运行此脚本:\n"
            "  uv run SKILL_DIR/scripts/parse_share.py <url>\n"
            "或手动安装:\n"
            "  pip install playwright && python -m playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(4)

    # Ensure Chromium browser is installed
    import subprocess
    import shutil
    from pathlib import Path

    # Check if chromium binary already exists in Playwright's cache
    pw_browsers = Path.home() / "Library" / "Caches" / "ms-playwright"
    chromium_exists = any(pw_browsers.glob("chromium-*")) if pw_browsers.exists() else False

    if not chromium_exists:
        print("正在安装 Chromium 浏览器（首次运行需要下载）...", file=sys.stderr)
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minutes for large download
        )
        if result.returncode != 0:
            print(
                f"Chromium 浏览器安装失败:\n{result.stderr}",
                file=sys.stderr,
            )
            sys.exit(4)

    import asyncio

    raw_messages, page_title = asyncio.run(fetch_and_extract(url, platform))

    if not raw_messages:
        print(
            "未找到对话数据。可能原因:\n"
            "  - 分享链接已过期或已删除\n"
            "  - 页面结构已变更\n"
            "  - 链接需要登录才能访问",
            file=sys.stderr,
        )
        sys.exit(3)

    pairs = pair_messages(raw_messages)

    # Fallback: if no user messages exist (e.g. /s/t_ temporary share links),
    # use the page title as the question and combine all assistant messages.
    if not pairs:
        has_user = any(m["role"] == "user" for m in raw_messages)
        if not has_user:
            # Strip common prefixes like "ChatGPT - " from the page title
            title = page_title
            for prefix in ["ChatGPT - ", "ChatGPT — "]:
                if title.startswith(prefix):
                    title = title[len(prefix):]
                    break
            all_content = "\n\n".join(
                m["content"] for m in raw_messages if m["content"].strip()
            )
            if all_content:
                pairs = [{"question": title or "Untitled", "answer": all_content}]

    if not pairs:
        print("未能从页面中提取到有效的问答对。", file=sys.stderr)
        sys.exit(3)

    results = format_output(pairs, url, platform)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
