import sys
import os
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Configuration
SESSION_DIR = os.path.expanduser("~/.qwen_session/")
OUTPUT_FILE = "/home/derek/文档/Derek_Obsidian_DB/AI应用对接/Qwen模块/qwen_session_history.md"
TARGET_URL = "https://www.qianwen.com/"

# Selectors
INPUT_SELECTORS = [
    "textarea",
    "div[contenteditable='true']",
    ".chat-input",
    "[class*='input'] textarea",
    "[class*='chat'] textarea",
]

MESSAGE_SELECTORS = [
    "#qk-markdown-react",
    ".qk-markdown.qk-markdown-react",
    ".chat-answers-card-wrap",
    ".answer-common-card",
    ".markdown-pc-special-class",
]

async def get_all_responses(page):
    """Returns list of all response texts found on page."""
    results = []
    for sel in MESSAGE_SELECTORS:
        try:
            elements = await page.query_selector_all(sel)
            if elements:
                for el in reversed(elements):
                    text = (await el.inner_text()).strip()
                    if text and text not in results:
                        results.append(text)
        except Exception:
            continue
    return results

async def run_qwen_multi_turn(timeout_seconds=120):
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR, exist_ok=True)

    async with async_playwright() as p:
        print(f"[*] Starting Playwright with persistent context: {SESSION_DIR}")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            args=["--no-sandbox"]
        )

        page = await context.new_page()
        history = []

        try:
            print(f"[*] Navigating to Qwen: {TARGET_URL}")
            await page.goto(TARGET_URL, timeout=timeout_seconds * 1000)

            # --- Login/Interface Detection ---
            input_found = False
            input_selector = None
            
            print("[*] Waiting for chat interface to load...")
            for sel in INPUT_SELECTORS:
                try:
                    await page.wait_for_selector(sel, timeout=10000)
                    input_found = True
                    input_selector = sel
                    print(f"[+] Input box found with selector: {sel}")
                    break
                except Exception:
                    continue

            if not input_found:
                print("[!] Input box not found. You may be logged out. Please login in the browser.")
                # Wait for user to login manually
                for sel in INPUT_SELECTORS:
                    try:
                        await page.wait_for_selector(sel, timeout=300000) # 5 min wait for login
                        input_found = True
                        input_selector = sel
                        print(f"[+] Login detected. Input box found: {sel}")
                        break
                    except Exception:
                        continue
                
                if not input_found:
                    raise Exception("Could not find input box even after waiting for login.")

            input_field = page.locator(input_selector).first

            # --- Multi-turn Loop ---
            print("[*] Multi-turn mode active. Type your question and press Enter. Type 'exit' to quit.")
            
            while True:
                # Read input from stdin (supports both pipe and interactive)
                loop = asyncio.get_event_loop()
                line = await loop.run_in_executor(None, sys.stdin.readline)
                
                if not line:
                    print("[*] EOF, exiting.")
                    break
                
                query = line.strip()
                if not query:
                    continue
                
                if query.lower() in ["exit", "quit", "关闭"]:
                    print("[*] Exiting...")
                    break

                print(f"[*] Sending query: {query}")
                await input_field.fill(query)
                await page.keyboard.press("Enter")
                
                # --- Response Stability Detection ---
                print("[*] Waiting for response...")
                start_time = asyncio.get_event_loop().time()
                last_text = ""
                
# Count existing responses before sending
                prev_count = len(await get_all_responses(page))
                
                stabilized = False
                while asyncio.get_event_loop().time() - start_time < timeout_seconds:
                    await asyncio.sleep(2)
                    
                    all_texts = await get_all_responses(page)
                    current_count = len(all_texts)
                    
                    # New response appeared (count increased)
                    if current_count > prev_count:
                        current_text = all_texts[-1]
                        if current_text == last_text:
                            # Text has stopped changing
                            stabilized = True
                            break
                        last_text = current_text
                    # Same count but text might be streaming
                    elif current_count == prev_count and last_text:
                        current_text = all_texts[-1] if all_texts else ""
                        if current_text == last_text:
                            stabilized = True
                            break
                        if current_text:
                            last_text = current_text

                if not last_text:
                    print("[!] Failed to capture response.")
                    continue

                print(f"[A]: {last_text}")
                
                # Record to history
                timestamp = datetime.now().isoformat()
                history.append({
                    "query": query,
                    "answer": last_text,
                    "timestamp": timestamp
                })

                # Write to file (Append mode)
                os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    f.write(f"## Session Entry: {timestamp}\n\n")
                    f.write(f"**Q**: {query}\n\n")
                    f.write(f"**A**: {last_text}\n\n")
                    f.write("---\n\n")

            # --- Cleanup (as per single script) ---
            print("[*] Cleaning up conversation...")
            try:
                print("[*] Waiting for sidebar to update...")
                await asyncio.sleep(5)

                entry = None
                try:
                    entry = await page.wait_for_selector('[data-react-window-index="3"]', timeout=10000)
                except Exception:
                    pass

                if entry:
                    more_btn = await entry.query_selector('button[aria-haspopup="menu"]')
                    if more_btn:
                        print("[*] Found more button, clicking...")
                        await more_btn.scroll_into_view_if_needed()
                        await asyncio.sleep(0.5)
                        await more_btn.click()
                        more_clicked = 'clicked'
                    else:
                        more_clicked = 'no_btn'
                else:
                    more_clicked = 'no_entry'

                if more_clicked == 'clicked':
                    await asyncio.sleep(2)
                    try:
                        loc = page.locator('[role="menuitem"]').filter(has_text="删除此对话")
                        await loc.first.wait_for(state="visible", timeout=5000)
                        await loc.first.click()
                        await asyncio.sleep(3)
                        confirm_btn = page.locator('[role="dialog"] button:has-text("确定")')
                        await confirm_btn.first.wait_for(state="visible", timeout=10000)
                        await asyncio.sleep(1)
                        await confirm_btn.first.click()
                        print("[+] Conversation deleted.")
                    except Exception as e:
                        print(f"[!] Cleanup error: {e}")
            except Exception as e:
                print(f"[!] Cleanup warning: {e}")

        except Exception as e:
            print(f"[-] Error: {str(e)}")
        finally:
            await asyncio.sleep(3)
            await context.close()

if __name__ == "__main__":
    asyncio.run(run_qwen_multi_turn())
