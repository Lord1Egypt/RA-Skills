#!/usr/bin/env python3
"""
ask_gemini.py - Send a message to Gemini via browser automation and get the response.

Connects to an already-running Chrome instance via CDP (Chrome DevTools Protocol),
navigates to gemini.google.com, sends a user message, waits for the response,
and extracts both the reply text and any citation links.

Usage:
    python ask_gemini.py "Your question here"
    python ask_gemini.py --port 9222 "Your question here"
    python ask_gemini.py --timeout 180 "Your question here"
    python ask_gemini.py --new-chat "Your question here"   # Force a new chat session
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
GEMINI_URL = "https://gemini.google.com"
GEMINI_APP_URL = "https://gemini.google.com/app"

# Selectors – Gemini's UI may change; we try multiple fallbacks.
INPUT_SELECTORS = [
    'div.ql-editor[contenteditable="true"]',
    'rich-textarea div[contenteditable="true"]',
    'div[role="textbox"]',
    '.input-area-container div[contenteditable="true"]',
    'p[data-placeholder="Ask Gemini"]',
]

SEND_BUTTON_SELECTORS = [
    "button.send-button",
    'button[aria-label="Send message"]',
    'button[aria-label*="Send"]',
    'button[data-tooltip="Send"]',
    ".send-button-container button",
    "button.send",
]

# Selector for the "stop generating" / streaming-in-progress indicator
STOP_BUTTON_SELECTORS = [
    'button[aria-label="Stop response"]',
    'button[aria-label*="Stop"]',
    'mat-icon[data-mat-icon-name="stop_circle"]',
]

# Response container selectors (ordered by specificity – prefer div.markdown
# which contains the actual rendered response without UI chrome like "显示思路")
RESPONSE_SELECTORS = [
    "div.markdown.markdown-main-panel",
    "div.markdown",
    ".model-response-text",
    "message-content.model-response-text",
    "model-response message-content",
    ".response-container-content",
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
    page: Page, existing_count: int = 0, timeout_seconds: int = 120
) -> bool:
    """
    Wait until Gemini finishes generating its response.

    Strategy:
    1. Wait for a NEW response element to appear (count > existing_count).
    2. Then poll until the content stabilises (no changes for 3 seconds)
       AND no "stop generating" button is visible.
    """
    deadline = time.time() + timeout_seconds
    print("[*] Waiting for Gemini to start responding...", file=sys.stderr)

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
    """Get all response message elements on the page.

    Tries selectors in order.  Skips a selector if it matches elements but
    none of them contain visible text (handles Web-Component / shadow-DOM
    edge cases where the element exists but inner_text is empty).
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
    """Extract text from the last (most recent) response on the page."""
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
    Extract citation links from the last Gemini response.

    Gemini embeds citations as <a> tags within the response.  We also look
    for a dedicated citation / sources section.
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
            # Skip gemini.google.com internal links
            if parsed.hostname and "gemini.google.com" in parsed.hostname:
                continue

            # Skip Google internal service links (accounts, support, etc.)
            if parsed.hostname and parsed.hostname in (
                "accounts.google.com",
                "support.google.com",
                "policies.google.com",
            ):
                continue

            if href not in seen_urls:
                seen_urls.add(href)
                links.append({"url": href, "text": text or href})
    except Exception as e:
        print(f"[!] Error extracting citations: {e}", file=sys.stderr)

    # Also try to find a dedicated citation/sources section
    try:
        # Gemini sometimes renders citations in a separate panel
        citation_selectors = [
            "citation-chip a[href]",
            ".citation a[href]",
            "a.citation-link[href]",
            ".source-link a[href]",
            "fact-check-source a[href]",
            "search-result-group a[href]",
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


def send_message(page: Page, message: str, timeout_seconds: int = 120) -> dict:
    """
    Send a message to Gemini and wait for the response.

    Returns a dict with keys: response_text, citations, success, error
    """
    result = {
        "response_text": "",
        "citations": [],
        "success": False,
        "error": None,
    }

    # Count existing responses before sending (so we know when a new one appears)
    existing_responses = len(get_all_response_elements(page))

    # Find the input element
    input_el = find_element(page, INPUT_SELECTORS, timeout=10000)
    if not input_el:
        result["error"] = (
            "Could not find Gemini input field. The page may not have loaded correctly."
        )
        return result

    print(f"[*] Typing message ({len(message)} chars)...", file=sys.stderr)

    # Click to focus
    try:
        input_el.click()
        time.sleep(0.3)
    except Exception:
        pass

    # Type the message
    try:
        input_el.fill(message)
    except Exception:
        # fill() may not work on contenteditable; fallback to type()
        try:
            input_el.type(message, delay=10)
        except Exception:
            # Last resort: use keyboard
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
        description="Ask Gemini a question via browser automation"
    )
    parser.add_argument("message", help="The message/question to send to Gemini")
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

        # Find or create a Gemini tab
        page = None
        for p in context.pages:
            if "gemini.google.com" in p.url:
                page = p
                print(f"[*] Found existing Gemini tab: {p.url}", file=sys.stderr)
                break

        if page is None:
            page = context.new_page()
            print("[*] Opening new Gemini tab...", file=sys.stderr)

        # Navigate to Gemini
        target_url = GEMINI_APP_URL if args.new_chat else GEMINI_URL
        if args.new_chat or "gemini.google.com" not in page.url:
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
            print(f"[*] Navigated to {target_url}", file=sys.stderr)
            # Wait for page to be interactive
            time.sleep(3)

        # Check if we're on a login page
        current_url = page.url
        if "accounts.google.com" in current_url:
            print(
                "ERROR: You are not logged in to Google.\n"
                "Please log in to your Google account in the Chrome window first.",
                file=sys.stderr,
            )
            sys.exit(1)

        # If --new-chat requested and we're already on Gemini, click "New chat"
        if args.new_chat and "gemini.google.com" in page.url:
            try:
                new_chat_btn = page.query_selector(
                    'a[href="/app"], button[aria-label*="New chat"], '
                    'button[aria-label*="new chat"]'
                )
                if new_chat_btn:
                    new_chat_btn.click()
                    time.sleep(2)
                    print("[*] Started new chat session.", file=sys.stderr)
            except Exception:
                # If we can't find the button, just navigate to /app
                page.goto(GEMINI_APP_URL, wait_until="domcontentloaded", timeout=30000)
                time.sleep(3)

        # Send message and get response
        result = send_message(page, args.message, args.timeout)

        # Output
        if args.json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if result["success"]:
                print("=" * 60)
                print("  GEMINI RESPONSE")
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
                            f" - {link['text']}" if link["text"] != link["url"] else ""
                        )
                        print(f"  {i}. {link['url']}{text_part}")
                    print()
                else:
                    print("(No citation links found in the response)")
                    print()
            else:
                print(f"ERROR: {result.get('error', 'Unknown error')}", file=sys.stderr)
                if result["response_text"]:
                    print("\nPartial response:", file=sys.stderr)
                    print(result["response_text"], file=sys.stderr)
                sys.exit(1)

        # Note: we do NOT close the browser – it's the user's Chrome instance


if __name__ == "__main__":
    main()
