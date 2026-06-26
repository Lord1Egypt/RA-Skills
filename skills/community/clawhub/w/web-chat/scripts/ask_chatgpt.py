#!/usr/bin/env python3
"""
ask_chatgpt.py - Send a message to ChatGPT via browser automation and get the response.

Connects to an already-running Chrome instance via CDP (Chrome DevTools Protocol),
navigates to chatgpt.com, sends a user message, waits for the response,
and extracts both the reply text and any citation links.

Usage:
    python ask_chatgpt.py "Your question here"
    python ask_chatgpt.py --port 9222 "Your question here"
    python ask_chatgpt.py --timeout 180 "Your question here"
    python ask_chatgpt.py --new-chat "Your question here"   # Force a new chat session
"""

import argparse
import json
import sys
import time
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeout


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CHATGPT_URL = "https://chatgpt.com"
CHATGPT_CHAT_URL = "https://chatgpt.com/"

# Recognized hostnames for detecting a ChatGPT tab
CHATGPT_HOSTS = ("chatgpt.com", "chat.openai.com")

# Selectors – ChatGPT's UI may change; we try multiple fallbacks.
# The prompt textarea has historically been both <textarea> and <div contenteditable>.
INPUT_SELECTORS = [
    'div#prompt-textarea[contenteditable="true"]',
    "textarea#prompt-textarea",
    "#prompt-textarea",
    'div[contenteditable="true"][data-placeholder]',
    'div[role="textbox"]',
]

SEND_BUTTON_SELECTORS = [
    'button[data-testid="send-button"]',
    'button[aria-label="Send prompt"]',
    'button[aria-label*="Send"]',
    'button[aria-label="发送"]',
    'form button[data-testid="send-button"]',
]

# Selector for the "stop generating" / streaming-in-progress indicator
STOP_BUTTON_SELECTORS = [
    'button[data-testid="stop-button"]',
    'button[aria-label="Stop generating"]',
    'button[aria-label="Stop streaming"]',
    'button[aria-label*="Stop"]',
    'button[aria-label="停止生成"]',
]

# Response container selectors (ordered by specificity)
RESPONSE_SELECTORS = [
    'div[data-message-author-role="assistant"] div.markdown',
    'div[data-message-author-role="assistant"] .markdown',
    'div[data-message-author-role="assistant"]',
    'div[class*="agent-turn"] div.markdown',
    'div[class*="agent-turn"]',
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def find_element(page: Page, selectors: list[str], timeout: int = 5000):
    """Try multiple selectors and return the first match."""
    for sel in selectors:
        try:
            el = page.wait_for_selector(sel, timeout=timeout, state="attached")
            if el:
                return el
        except PlaywrightTimeout:
            continue
    return None


def wait_for_response_complete(
    page: Page, existing_count: int, timeout_seconds: int = 120
) -> bool:
    """
    Wait until ChatGPT finishes generating its response.

    Strategy:
    1. Wait for a NEW response element to appear (count > existing_count).
    2. Then poll until the content stabilises (no changes for 3 seconds)
       AND no "stop generating" button is visible.
    """
    deadline = time.time() + timeout_seconds
    print("[*] Waiting for ChatGPT to start responding...", file=sys.stderr)

    # Phase 1: wait for a new response block to appear
    response_appeared = False
    while time.time() < deadline:
        elements = get_all_response_elements(page)
        if len(elements) > existing_count:
            # Verify the new element has text
            last = elements[-1]
            try:
                if last.inner_text().strip():
                    response_appeared = True
                    break
            except Exception:
                pass
        time.sleep(0.5)

    if not response_appeared:
        print("[!] No new response element detected within timeout.", file=sys.stderr)
        return False

    print("[*] Response started, waiting for completion...", file=sys.stderr)

    # Phase 2: wait for content to stabilise
    last_text = ""
    stable_count = 0
    required_stable = 6  # 6 * 0.5s = 3 seconds of stable content

    while time.time() < deadline:
        # Check if "stop" button is still visible (streaming in progress)
        stop_visible = False
        for sel in STOP_BUTTON_SELECTORS:
            try:
                btn = page.query_selector(sel)
                if btn and btn.is_visible():
                    stop_visible = True
                    break
            except Exception:
                continue

        # Get current response text
        current_text = get_last_response_text(page)

        if current_text == last_text and not stop_visible:
            stable_count += 1
        else:
            stable_count = 0
            last_text = current_text

        if stable_count >= required_stable:
            print("[*] Response complete.", file=sys.stderr)
            return True

        time.sleep(0.5)

    print(
        "[!] Timeout waiting for response to complete. Using partial content.",
        file=sys.stderr,
    )
    return True  # still return True so we can extract what we have


def get_all_response_elements(page: Page):
    """Get all assistant response message elements on the page.

    Tries selectors in order.  Skips a selector if it matches elements but
    none of them contain visible text (handles edge cases where the element
    exists but inner_text is empty).
    """
    for sel in RESPONSE_SELECTORS:
        elements = page.query_selector_all(sel)
        if elements:
            # Verify at least one element has text
            for el in elements:
                try:
                    if el.inner_text().strip():
                        return elements
                except Exception:
                    continue
    return []


def get_last_response_text(page: Page) -> str:
    """Extract text from the last (most recent) assistant response on the page."""
    elements = get_all_response_elements(page)
    if not elements:
        return ""
    last = elements[-1]
    try:
        return last.inner_text().strip()
    except Exception:
        return ""


def get_last_response_html(page: Page) -> str:
    """Extract inner HTML from the last response element."""
    elements = get_all_response_elements(page)
    if not elements:
        return ""
    last = elements[-1]
    try:
        return last.inner_html()
    except Exception:
        return ""


def extract_citation_links(page: Page) -> list[dict]:
    """
    Extract citation links from the last ChatGPT response.

    ChatGPT embeds citations as <a> tags within the response markdown.
    """
    elements = get_all_response_elements(page)
    if not elements:
        return []

    last_el = elements[-1]
    links: list[dict] = []
    seen_urls: set[str] = set()

    try:
        anchors = last_el.query_selector_all("a[href]")
        for a in anchors:
            href = a.get_attribute("href") or ""
            text = a.inner_text().strip()

            # Skip empty, internal, and javascript links
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue

            parsed = urlparse(href)

            # Skip ChatGPT / OpenAI internal links
            if parsed.hostname and any(
                h in parsed.hostname
                for h in (
                    "chatgpt.com",
                    "chat.openai.com",
                    "openai.com",
                    "auth.openai.com",
                )
            ):
                continue

            if href not in seen_urls:
                seen_urls.add(href)
                links.append({"url": href, "text": text or href})
    except Exception as e:
        print(f"[!] Error extracting citations: {e}", file=sys.stderr)

    # Also look for ChatGPT's dedicated citation/source chips
    try:
        citation_selectors = [
            'a[class*="citation"]',
            'a[data-citation]',
            'span[class*="citation"] a[href]',
        ]
        for sel in citation_selectors:
            citation_anchors = page.query_selector_all(sel)
            for a in citation_anchors:
                href = a.get_attribute("href") or ""
                text = a.inner_text().strip()
                if href and href not in seen_urls:
                    parsed = urlparse(href)
                    if parsed.scheme in ("http", "https"):
                        seen_urls.add(href)
                        links.append({"url": href, "text": text or href})
    except Exception:
        pass

    return links


def send_message(
    page: Page, message: str, timeout_seconds: int = 120
) -> dict:
    """
    Send a message to ChatGPT and wait for the response.

    Returns a dict with keys: response_text, citations, success, error
    """
    result = {
        "response_text": "",
        "citations": [],
        "success": False,
        "error": None,
    }

    # Count existing responses so we can detect when a new one appears
    existing_responses = len(get_all_response_elements(page))

    # Find the input element
    input_el = find_element(page, INPUT_SELECTORS, timeout=10000)
    if not input_el:
        result["error"] = (
            "Could not find ChatGPT input field. "
            "The page may not have loaded correctly."
        )
        return result

    print(f"[*] Typing message ({len(message)} chars)...", file=sys.stderr)

    # Click to focus
    try:
        input_el.click()
        time.sleep(0.3)
    except Exception:
        pass

    # Type the message.
    # ChatGPT's #prompt-textarea can be either <textarea> or <div contenteditable>.
    # fill() works on textarea; for contenteditable we may need type().
    tag = input_el.evaluate("el => el.tagName.toLowerCase()")
    is_contenteditable = input_el.evaluate(
        'el => el.getAttribute("contenteditable") === "true"'
    )

    if tag == "textarea":
        try:
            input_el.fill(message)
        except Exception:
            input_el.type(message, delay=10)
    elif is_contenteditable:
        # For contenteditable divs, type() is more reliable than fill()
        try:
            input_el.type(message, delay=10)
        except Exception:
            try:
                input_el.fill(message)
            except Exception:
                page.keyboard.type(message, delay=10)
    else:
        # Unknown element type — try both
        try:
            input_el.fill(message)
        except Exception:
            try:
                input_el.type(message, delay=10)
            except Exception:
                page.keyboard.type(message, delay=10)

    time.sleep(0.5)

    # Send: try clicking the send button first, then fall back to Enter key
    sent = False
    send_btn = find_element(page, SEND_BUTTON_SELECTORS, timeout=3000)
    if send_btn:
        try:
            send_btn.click()
            sent = True
            print("[*] Clicked send button.", file=sys.stderr)
        except Exception:
            pass

    if not sent:
        page.keyboard.press("Enter")
        print("[*] Pressed Enter to send.", file=sys.stderr)

    time.sleep(1)

    # Wait for response (pass existing count so we detect NEW responses)
    ok = wait_for_response_complete(page, existing_responses, timeout_seconds)
    if not ok:
        result["error"] = "Timeout or no response detected."

    # Give a little extra time for citations to render
    time.sleep(2)

    # Extract response
    result["response_text"] = get_last_response_text(page)
    result["citations"] = extract_citation_links(page)
    result["success"] = bool(result["response_text"])

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Ask ChatGPT a question via browser automation"
    )
    parser.add_argument("message", help="The message/question to send to ChatGPT")
    parser.add_argument(
        "--port",
        type=int,
        default=9222,
        help="Chrome remote debugging port (default: 9222)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Max seconds to wait for response (default: 120)",
    )
    parser.add_argument(
        "--new-chat",
        action="store_true",
        help="Force start a new chat session",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output result as JSON",
    )
    args = parser.parse_args()

    cdp_url = f"http://localhost:{args.port}"

    with sync_playwright() as pw:
        # Connect to existing Chrome via CDP
        print(f"[*] Connecting to Chrome at {cdp_url}...", file=sys.stderr)
        try:
            browser = pw.chromium.connect_over_cdp(cdp_url)
        except Exception as e:
            print(
                f"ERROR: Cannot connect to Chrome on port {args.port}.\n"
                f"Make sure Chrome is running with --remote-debugging-port={args.port}\n"
                f"Run: start_chrome.sh {args.port}\n"
                f"Detail: {e}",
                file=sys.stderr,
            )
            sys.exit(1)

        print(f"[*] Connected. Contexts: {len(browser.contexts)}", file=sys.stderr)

        # Use existing context (preserves login state)
        if browser.contexts:
            context = browser.contexts[0]
        else:
            context = browser.new_context()

        # Find or create a ChatGPT tab
        page = None
        for p in context.pages:
            try:
                parsed = urlparse(p.url)
                if parsed.hostname and any(
                    h in parsed.hostname for h in CHATGPT_HOSTS
                ):
                    page = p
                    print(
                        f"[*] Found existing ChatGPT tab: {p.url}", file=sys.stderr
                    )
                    break
            except Exception:
                continue

        if page is None:
            page = context.new_page()
            print("[*] Opening new ChatGPT tab...", file=sys.stderr)

        # Navigate to ChatGPT
        needs_navigation = True
        try:
            parsed = urlparse(page.url)
            if parsed.hostname and any(
                h in parsed.hostname for h in CHATGPT_HOSTS
            ):
                if not args.new_chat:
                    needs_navigation = False
        except Exception:
            pass

        if needs_navigation:
            target_url = CHATGPT_CHAT_URL
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
            print(f"[*] Navigated to {target_url}", file=sys.stderr)
            # Wait for page to be interactive
            time.sleep(3)

        # Check if we're on a login page
        current_url = page.url
        if "auth.openai.com" in current_url or "/auth/login" in current_url:
            print(
                "ERROR: You are not logged in to ChatGPT.\n"
                "Please log in to your OpenAI/ChatGPT account in the Chrome window first.",
                file=sys.stderr,
            )
            sys.exit(1)

        # If --new-chat requested and we're already on ChatGPT, navigate to root
        if args.new_chat:
            try:
                page.goto(
                    CHATGPT_CHAT_URL, wait_until="domcontentloaded", timeout=30000
                )
                time.sleep(3)
                print("[*] Started new chat session.", file=sys.stderr)
            except Exception:
                pass

        # Send message and get response
        result = send_message(page, args.message, args.timeout)

        # Output
        if args.json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if result["success"]:
                print("=" * 60)
                print("  CHATGPT RESPONSE")
                print("=" * 60)
                print()
                print(result["response_text"])
                print()

                if result["citations"]:
                    print("=" * 60)
                    print("  CITATION LINKS")
                    print("=" * 60)
                    print()
                    for i, link in enumerate(result["citations"], 1):
                        text_part = (
                            f" - {link['text']}"
                            if link["text"] != link["url"]
                            else ""
                        )
                        print(f"  {i}. {link['url']}{text_part}")
                    print()
                else:
                    print("(No citation links found in the response)")
                    print()
            else:
                print(
                    f"ERROR: {result.get('error', 'Unknown error')}", file=sys.stderr
                )
                if result["response_text"]:
                    print("\nPartial response:", file=sys.stderr)
                    print(result["response_text"], file=sys.stderr)
                sys.exit(1)

        # Note: we do NOT close the browser – it's the user's Chrome instance


if __name__ == "__main__":
    main()
