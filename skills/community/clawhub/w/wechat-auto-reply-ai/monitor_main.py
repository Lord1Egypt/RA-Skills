import re
import time
import subprocess
import os
import argparse
import json
import logging
import datetime
from threading import Lock

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


status_lock = Lock()
DASHBOARD_FILE = os.path.expanduser("~/.openclaw/workspace/memory/wechat_skill/dashboard_status.json")

def update_dashboard(target, update_data, log_msg=None, level="INFO"):
    global status_lock
    if log_msg:
        logger_func = getattr(logger, level.lower())
        logger_func(log_msg)
        
    with status_lock:
        data = {"targets": {}, "global_logs": []}
        if os.path.exists(DASHBOARD_FILE):
            try:
                with open(DASHBOARD_FILE, 'r') as f:
                    data = json.load(f)
            except:
                pass
                
        if target not in data["targets"]:
            data["targets"][target] = {}
            
        data["targets"][target].update(update_data)
        data["targets"][target]["last_check_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if log_msg:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            data["global_logs"].append(f"[{timestamp}] [{level}] {log_msg}")
            # Keep last 100 logs
            data["global_logs"] = data["global_logs"][-100:]
            
        with open(DASHBOARD_FILE, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def run_cmd(cmd, timeout=120):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out after {timeout}s: {cmd}")
        class DummyProcess:
            stdout = ""
            stderr = "TimeoutExpired"
            returncode = 124
        return DummyProcess()

def check_focus():
    res = run_cmd("osascript -e 'tell application \"System Events\" to get name of first application process whose frontmost is true'")
    return res.stdout.strip() in ["WeChat", "微信"]

def safe_paste_and_enter(text, wait_before_enter=0.5):
    safe_text = text.replace('\\', '\\\\').replace('"', '\\"')
    run_cmd(f"osascript -e 'set the clipboard to \"{safe_text}\"'")
    time.sleep(0.2)
    run_cmd("osascript -e 'tell application \"System Events\" to keystroke \"v\" using command down'")
    time.sleep(wait_before_enter)
    run_cmd("osascript -e 'tell application \"System Events\" to key code 36'") # Return
    time.sleep(0.5)

def search_and_focus_target(target_name):
    update_dashboard(target_name, {"status": "checking"}, f"🔍 Searching for target: {target_name}", "INFO")
    logger.info(f"🔍 Searching for target: {target_name}")
    # Focus WeChat
    run_cmd("peekaboo window focus --app 微信")
    time.sleep(1.0)
    
    if not check_focus():
        logger.warning("WeChat is not focused, aborting search.")
        return False
        
    # Cmd + F
    run_cmd("osascript -e 'tell application \"System Events\" to keystroke \"f\" using command down'")
    time.sleep(0.5)
    
    # Paste target name and hit enter (wait longer for search results to load)
    safe_paste_and_enter(target_name, wait_before_enter=1.5)
    time.sleep(1.5) # wait for chat to load
    return True

def get_main_window_id(exclude_titles=None):
    res = run_cmd("peekaboo window list --app 微信 --json")
    try:
        output = res.stdout
        if "{" in output:
            output = output[output.find("{"):]
        data = json.loads(output)
        
        main_window_candidates = []
        for w in data.get("data", {}).get("windows", []):
            title = w.get("window_title", "")
            # The main window usually has title "微信" or "WeChat" and is large
            if title in ["微信", "WeChat"]:
                # Exclude active detached chat windows from being considered the 'main' window
                if exclude_titles and any(excluded in title for excluded in exclude_titles):
                    continue
                bounds = w.get("bounds", {})
                area = bounds.get("width", 0) * bounds.get("height", 0)
                if area > 100000: # Filter out small windows like popups
                    main_window_candidates.append((area, w.get("window_id")))
        
        if main_window_candidates:
            # Return the ID of the largest window
            main_window_candidates.sort(key=lambda x: x[0], reverse=True)
            return main_window_candidates[0][1]

    except Exception as e:
        logger.error(f"Failed to parse window list: {e}")
    return None

def capture_main_window(path, exclude_titles=None):
    wid = get_main_window_id(exclude_titles=exclude_titles)
    if wid:
        res = run_cmd(f"/usr/sbin/screencapture -l {wid} '{path}'")
        return os.path.exists(path)
    logger.error("Could not find Main WeChat window ID.")
    return False

def clean_output(output):
    lines = output.split('\n')
    fail_markers = ["cannot", "unable", "don't have", "can't see", "Hook registry", "via model", "I am an AI"]
    filtered = [l for l in lines if not any(m in l for m in fail_markers) and l.strip() and not l.startswith('#')]
    return "\n".join(filtered).strip()

def merge_history(old_history, new_history):
    if not old_history: return new_history
    merged = list(old_history)
    for item in new_history:
        if item not in merged[-10:]:
            merged.append(item)
    return merged[-50:]

def load_accumulated_state(json_file):
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "accumulated_history" in data:
                    return data["accumulated_history"]
        except Exception:
            pass
    return []

def main():
    parser = argparse.ArgumentParser(description="OpenClaw WeChat Auto-Reply (Main Window Polling)")
    parser.add_argument("--targets", required=True, help="Comma separated list of target names (e.g., '冰冰,森哥')")
    parser.add_argument("--persona", required=True, help="The prompt guiding the LLM's reply style.")
    parser.add_argument("--interval", type=int, default=60, help="Polling interval in seconds (default: 60).")
    args = parser.parse_args()

    TARGETS = [t.strip() for t in args.targets.split(",") if t.strip()]
    PERSONA = args.persona
    INTERVAL = args.interval
    
    WORKSPACE = os.path.expanduser("~/.openclaw/workspace/memory/wechat_skill")
    os.makedirs(WORKSPACE, exist_ok=True)

    update_dashboard("System", {"status": "online"}, f"Monitor V5.0 started for targets: {TARGETS} with interval {INTERVAL}s", "INFO")

    while True:
        for TARGET in TARGETS:
            try:
                if not search_and_focus_target(TARGET):
                    continue
                    
                RAW_IMG = os.path.join(WORKSPACE, f"wechat_raw_main_{TARGET.replace(' ', '_')}.png")
                STATE_FILE = os.path.join(WORKSPACE, f"last_seen_v5_{TARGET.replace(' ', '_')}.txt")
                JSON_FILE = os.path.join(WORKSPACE, f"last_parsed_{TARGET.replace(' ', '_')}.json")
                
                success = capture_main_window(RAW_IMG)
                if not success:
                    update_dashboard(TARGET, {"status": "error", "last_error": "Failed to capture window"}, f"Failed to capture window for {TARGET}", "WARNING")
                    continue
                
                analysis_prompt = """Analyze this WeChat chat screenshot.
1. Read the visible chat history from top to bottom.
2. Distinguish messages: GREEN bubbles are from "Self" (me), WHITE bubbles are from "Other".
3. If a bubble contains an image, sticker, or emoji, describe it briefly (e.g., [Image: cat sleeping]).
4. Extract the last few messages to establish context.
5. Identify the NEW messages from "Other" at the very bottom that haven't been replied to yet.
Output STRICTLY in JSON format:
{
  "context_history": ["Self: hello", "Other: hi there", "Other: [Image: funny dog]"],
  "new_messages_to_reply": ["Other: what are you up to?"],
  "needs_reply": true
}
If the very last message is from "Self", set needs_reply to false. Do not output markdown blocks, just the raw JSON."""
                prompt_file = f"/tmp/wechat_prompt_{TARGET.replace(' ', '_')}.txt"
                with open(prompt_file, "w", encoding='utf-8') as pf:
                    pf.write(analysis_prompt)
                
                COMPRESSED_IMG = os.path.join(WORKSPACE, f"wechat_mini_main_{TARGET.replace(' ', '_')}.png")
                run_cmd(f"sips -s format png -Z 1200 '{RAW_IMG}' --out '{COMPRESSED_IMG}'", timeout=10)
                
                res = run_cmd(f"summarize \"{COMPRESSED_IMG}\" --prompt \"$(< {prompt_file})\" --plain --no-color --metrics off", timeout=180)
                raw_output = res.stdout.strip()
                
                json_str = ""
                match = re.search(r'(\{.*\})', raw_output, re.DOTALL)
                if match:
                    json_str = match.group(1)
                else:
                    json_str = raw_output

                try:
                    chat_data = json.loads(json_str)
                    accumulated_history = load_accumulated_state(JSON_FILE)
                    current_history = chat_data.get("context_history", [])
                    chat_data["accumulated_history"] = merge_history(accumulated_history, current_history)
                    
                    with open(JSON_FILE, "w", encoding='utf-8') as jf:
                        json.dump(chat_data, jf, indent=2, ensure_ascii=False)
                except json.JSONDecodeError:
                    update_dashboard(TARGET, {"status": "error", "last_error": "JSON Decode Error"}, f"JSON parsing failed for {TARGET}. Raw: {raw_output}", "ERROR")
                    time.sleep(2)
                    continue

                if not chat_data.get("needs_reply") or not chat_data.get("new_messages_to_reply"):
                    continue

                new_msgs = chat_data.get("new_messages_to_reply", [])
                current_state_str = str(new_msgs)
                last_seen = ""
                if os.path.exists(STATE_FILE):
                    with open(STATE_FILE, "r") as f:
                        last_seen = f.read().strip()
                
                if current_state_str == last_seen:
                    continue
                    
                update_dashboard(TARGET, {"status": "online", "last_messages": new_msgs, "last_reply": "", "image_path": f"wechat_mini_main_{TARGET.replace(' ', '_')}.png"}, f"[{TARGET}] New incoming messages: {new_msgs}", "INFO")
                
                context_str = " | ".join(chat_data.get("accumulated_history", []))
                msgs_str = " | ".join(new_msgs)
                
                reply_prompt = (
                    f"You are replying to a WeChat conversation.\\n"
                    f"Recent context (from memory bank): {context_str}\\n"
                    f"New messages to reply to: {msgs_str}\\n"
                    f"Persona/Style rules: {PERSONA}\\n"
                    f"Generate ONLY the exact text to send back. No quotes, no explanations.\\n"
                    f"CRITICAL RULE: If the user asks for a location, address, map, or navigation link, "
                    f"DO NOT reply with a URL. Instead, reply EXACTLY with this format: [ACTION:SEND_LOCATION|Address]. "
                )
                prompt_file_reply = f"/tmp/wechat_reply_{TARGET.replace(' ', '_')}.txt"
                with open(prompt_file_reply, "w", encoding='utf-8') as pf:
                    pf.write(reply_prompt)
                
                reply_res = run_cmd(f"gemini -p \"$(< {prompt_file_reply})\"")
                reply = clean_output(reply_res.stdout)
                
                if not reply or "cannot" in reply.lower():
                    continue
                    
                update_dashboard(TARGET, {"status": "online", "last_reply": reply, "last_error": ""}, f"[{TARGET}] Action: Replying '{reply}'", "INFO")
                
                action_match = re.search(r'\[ACTION:SEND_LOCATION\|(.+?)\]', reply)
                send_success = False
                
                if action_match:
                    address = action_match.group(1).strip()
                    logger.info(f"⚡ [{TARGET}] Intercepted Location Request! Address: {address}")
                    script_path = os.path.expanduser("~/.openclaw/workspace/skills/wechat-auto-reply/send_location.py")
                    # Since we are already in the main window and focused on the target, send_location might try to focus a detached window.
                    # But send_location.py hardcodes `peekaboo window focus --app 微信 --window-title '{args.target}'`.
                    # For V5 main window, we should just paste and enter directly since we are already focused!
                    # So we bypass send_location.py and just craft the message here.
                    import urllib.parse
                    encoded_address = urllib.parse.quote(address)
                    map_url = f"https://uri.amap.com/search?keyword={encoded_address}"
                    message_text = f"📍 我在这里/去这里：{address}\n导航链接：{map_url}"
                    if check_focus():
                        safe_paste_and_enter(message_text)
                        send_success = True
                else:
                    if check_focus():
                        safe_paste_and_enter(reply)
                        send_success = True
                
                if send_success:
                    with open(STATE_FILE, "w") as f:
                        f.write(current_state_str)
                    chat_data["accumulated_history"].append(f"Self: {reply}")
                    with open(JSON_FILE, "w", encoding='utf-8') as jf:
                        json.dump(chat_data, jf, indent=2, ensure_ascii=False)
                        
            except Exception as e:
                update_dashboard(TARGET, {"status": "error", "last_error": str(e)}, f"Error processing {TARGET}: {str(e)}", "ERROR")
                
        logger.info(f"Finished polling cycle. Sleeping for {INTERVAL} seconds...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
