import sys
import os
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Configuration
SESSION_DIR = os.path.expanduser("~/.qwen_session/")
OUTPUT_FILE = "/home/derek/文档/Derek_Obsidian_DB/AI应用对接/Qwen模块/last_output.md"
TARGET_URL = "https://www.qianwen.com/"

async def run_qwen_automation(query, timeout_seconds=120):
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

    async with async_playwright() as p:
        print(f"[*] Starting Playwright with persistent context: {SESSION_DIR}")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            args=["--no-sandbox"]
        )

        page = await context.new_page()

        try:
            print(f"[*] Navigating to Qwen: {TARGET_URL}")
            await page.goto(TARGET_URL, timeout=timeout_seconds * 1000)

            # --- 登录检测 ---
            input_selectors = [
                "textarea",
                "div[contenteditable='true']",
                ".chat-input",
                "[class*='input'] textarea",
                "[class*='chat'] textarea",
            ]

            print("[*] Waiting for chat interface to load...")
            input_found = False
            for sel in input_selectors:
                try:
                    await page.wait_for_selector(sel, timeout=10000)
                    input_found = True
                    input_selector = sel
                    print(f"[+] Input box found with selector: {sel}")
                    break
                except Exception:
                    continue

            if not input_found:
                print("[!] Input box not found. You may need to log in first.")
                print("[!] Please complete the login in the browser window.")
                for sel in input_selectors:
                    try:
                        await page.wait_for_selector(sel, timeout=timeout_seconds * 1000)
                        input_selector = sel
                        input_found = True
                        print(f"[+] Login successful. Input box found with selector: {sel}")
                        break
                    except Exception:
                        continue

            if not input_found:
                raise Exception("Could not find input box on qianwen.com after login.")

            input_field = page.locator(input_selector).first

            # --- 发送问题 ---
            print(f"[*] Sending query: {query}")
            await input_field.fill(query)
            await page.keyboard.press("Enter")

            print(f"[*] Waiting for response (timeout: {timeout_seconds}s)...")

            # --- 抓取回复 ---
            start_time = asyncio.get_event_loop().time()
            last_text = ""

            message_selectors = [
                "#qk-markdown-react",
                ".qk-markdown.qk-markdown-react",
                ".chat-answers-card-wrap",
                ".answer-common-card",
                ".markdown-pc-special-class",
            ]

            while asyncio.get_event_loop().time() - start_time < timeout_seconds:
                await asyncio.sleep(2)

                current_text = ""
                for sel in message_selectors:
                    try:
                        elements = await page.query_selector_all(sel)
                        if elements:
                            for el in reversed(elements):
                                text = (await el.inner_text()).strip()
                                if len(text) > 0 and text != query:
                                    current_text = text
                                    break
                    except Exception:
                        continue
                    if current_text:
                        break

                if current_text == last_text and last_text != "":
                    break

                if current_text:
                    last_text = current_text

            if not last_text:
                raise Exception("Failed to capture any response from Qwen.")

            # --- 写入输出 ---
            timestamp = datetime.now().isoformat()
            output_content = f"""---
query: "{query}"
timestamp: "{timestamp}"
source: qianwen.com
---

# Qwen 回复

{last_text}
"""
            os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(output_content)

            print(f"\n[+] Success! Result written to {OUTPUT_FILE}")
            print("-" * 20)
            print(output_content)
            print("-" * 20)

            # --- 清理：删除当前对话 ---
            print("[*] Cleaning up: deleting current conversation...")
            try:
                # 等待侧边栏渲染
                print("[*] Waiting for sidebar to update...")
                await asyncio.sleep(5)

                # 找 data-react-window-index="3" 的条目（最新对话）
                entry = None
                try:
                    entry = await page.wait_for_selector('[data-react-window-index="3"]', timeout=10000)
                except Exception:
                    pass

                if entry:
                    # 在这个条目里找 "..." 按钮
                    more_btn = await entry.query_selector('button[aria-haspopup="menu"]')

                    if more_btn:
                        print("[*] Found more button, clicking...")
                        await more_btn.scroll_into_view_if_needed()
                        await asyncio.sleep(0.5)
                        await more_btn.click()
                        print("[*] More button clicked.")
                        more_clicked = 'clicked'
                    else:
                        print("[!] No more button found in entry.")
                        more_clicked = 'no_btn'
                else:
                    print("[!] No conversation entry found.")
                    more_clicked = 'no_entry'

                print(f"[*] More button: {more_clicked}")

                if more_clicked == 'clicked':
                    await asyncio.sleep(2)

                    # 在弹出的菜单中找到 "删除此对话" 并点击
                    print("[*] Looking for delete menu item...")

                    # 使用 Playwright 的 locator 直接点击
                    clicked = False
                    try:
                        loc = page.locator('[role="menuitem"]').filter(has_text="删除此对话")
                        await loc.first.wait_for(state="visible", timeout=5000)
                        await loc.first.click()
                        print("[*] Delete menu item clicked via locator.")
                        clicked = True
                    except Exception as e:
                        print(f"[!] Locator click failed: {e}")
                        try:
                            loc = page.locator("text=删除此对话")
                            await loc.first.wait_for(state="visible", timeout=3000)
                            await loc.first.click()
                            print("[*] Delete menu item clicked via text locator.")
                            clicked = True
                        except Exception as e2:
                            print(f"[!] Text locator also failed: {e2}")

                    if clicked:
                        print("[*] Delete menu item clicked.")
                        await asyncio.sleep(3)

                        # 确认对话框：找 "确定" 按钮
                        try:
                            confirm_btn = page.locator('[role="dialog"] button:has-text("确定")')
                            await confirm_btn.first.wait_for(state="visible", timeout=10000)
                            await asyncio.sleep(1)
                            await confirm_btn.first.click()
                            print("[*] Delete confirmed.")
                            await asyncio.sleep(5)
                        except Exception as e:
                            print(f"[!] Confirm button not found: {e}")
                            await asyncio.sleep(5)

                        print("[+] Conversation deleted.")
                    else:
                        print("[!] Could not find delete menu item.")
                else:
                    print(f"[!] Could not find more button: {more_clicked}")
            except Exception as e:
                print(f"[!] Cleanup warning: {e}")

        except Exception as e:
            print(f"[-] Error: {str(e)}")
            sys.exit(1)
        finally:
            await asyncio.sleep(3)
            await context.close()


if __name__ == "__main__":
    query_arg = None
    if len(sys.argv) > 1:
        query_arg = sys.argv[1]
    else:
        if not sys.stdin.isatty():
            query_arg = sys.stdin.read().strip()

    if not query_arg:
        print("Usage: python qwen_agent.py \"Your question\" or echo \"question\" | python qwen_agent.py")
        sys.exit(1)

    timeout = 120
    for i, arg in enumerate(sys.argv):
        if arg == "--timeout" and i + 1 < len(sys.argv):
            timeout = int(sys.argv[i+1])

    asyncio.run(run_qwen_automation(query_arg, timeout))
