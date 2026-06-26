import re
import time
import subprocess
import os
import argparse
import json
import logging

# Set up simple logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def run_cmd(cmd, timeout=120):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out after {timeout}s: {cmd}")
        # Return a dummy completed process to avoid crashing the caller
        class DummyProcess:
            stdout = ""
            stderr = "TimeoutExpired"
            returncode = 124
        return DummyProcess()

def check_focus():
    res = run_cmd("osascript -e 'tell application \"System Events\" to get name of first application process whose frontmost is true'")
    return res.stdout.strip() in ["WeChat", "微信"]

def safe_send_detached(target_title, text):
    logger.info(f"Attempting to focus detached window: {target_title}")
    
    # 1. Focus the exact window by Title
    focus_res = run_cmd(f"peekaboo window focus --app 微信 --window-title '{target_title}'")
    if "Error" in focus_res.stdout or "not found" in focus_res.stdout:
        logger.error(f"Target window '{target_title}' not found.")
        return False
        
    time.sleep(1.5) # 给 macOS 充足的窗口切换动画时间

    # 2. Check if WeChat is indeed in front
    frontmost_res = run_cmd("osascript -e 'tell application \"System Events\" to get name of first application process whose frontmost is true'")
    frontmost_app = frontmost_res.stdout.strip()
    if frontmost_app not in ["WeChat", "微信"]:
        logger.warning(f"Safety Abort: WeChat is not the frontmost app. Currently frontmost: {frontmost_app}")
        return False

    # 3. Paste the message securely using AppleScript clipboard injection (most robust)
    safe_text = text.replace('\\', '\\\\').replace('"', '\\"')
    run_cmd(f"osascript -e 'set the clipboard to \"{safe_text}\"'")
    time.sleep(0.2)
    run_cmd("osascript -e 'tell application \"System Events\" to keystroke \"v\" using command down'")
    time.sleep(0.5)
    
    # 4. Final check before sending (hitting return)
    if check_focus():
        run_cmd("osascript -e 'tell application \"System Events\" to key code 36'") # 36 is Return key
        return True
    else:
        logger.warning("Safety Abort: WeChat lost focus right before hitting return.")
        return False

def get_window_id(app_name, window_title):
    res = run_cmd(f"peekaboo window list --app '{app_name}' --json")
    try:
        # Extract json part if there are logs prepended
        output = res.stdout
        if "{" in output:
            output = output[output.find("{"):]
        data = json.loads(output)
        for w in data.get("data", {}).get("windows", []):
            if w.get("window_title") == window_title:
                return w.get("window_id")
    except Exception as e:
        logger.error(f"Failed to parse window list for ID: {e}")
    return None

def capture_window(app_name, window_title, path):
    wid = get_window_id(app_name, window_title)
    if wid:
        # use native screencapture to bypass Swift UI deadlocks
        res = run_cmd(f"/usr/sbin/screencapture -l {wid} '{path}'")
        return os.path.exists(path)
    logger.error(f"Could not find window ID for {window_title}")
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
    parser = argparse.ArgumentParser(description="OpenClaw Generic WeChat Auto-Reply Monitor (UI-based)")
    parser.add_argument("--target", required=True, help="The exact title of the detached WeChat chat window.")
    parser.add_argument("--persona", required=True, help="The prompt guiding the LLM's reply style.")
    parser.add_argument("--interval", type=int, default=15, help="Polling interval in seconds (default: 15).")
    args = parser.parse_args()

    TARGET = args.target
    PERSONA = args.persona
    INTERVAL = args.interval
    
    # Workspace setup for state and images
    WORKSPACE = os.path.expanduser("~/.openclaw/workspace/memory/wechat_skill")
    os.makedirs(WORKSPACE, exist_ok=True)
    RAW_IMG = os.path.join(WORKSPACE, f"wechat_raw_{TARGET.replace(' ', '_')}.png")
    # New state file name to avoid conflicts with V2 logic
    STATE_FILE = os.path.join(WORKSPACE, f"last_seen_v3_{TARGET.replace(' ', '_')}.txt")
    JSON_FILE = os.path.join(WORKSPACE, f"last_parsed_{TARGET.replace(' ', '_')}.json")

    logger.info(f"Monitor V4.0 (Memory Bank) started for target: '{TARGET}' with interval {INTERVAL}s.")
    logger.info(f"Persona: {PERSONA}")

    # Remove old state
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

    # Monitor Loop
    while True:
        try:
            success = capture_window("微信", TARGET, RAW_IMG)
            if not success:
                logger.warning(f"Failed to capture window {TARGET}. Sleeping.")
                time.sleep(INTERVAL)
                continue
            
            analysis_prompt = """Analyze this WeChat chat screenshot.
1. Read the visible chat history from top to bottom.
2. Distinguish messages: GREEN bubbles are from "Self" (me), WHITE bubbles are from "Other".
3. If a bubble contains an image, sticker, or emoji, describe it briefly (e.g., [Image: cat sleeping]).
4. Extract the last few messages to establish context.
5. Identify the NEW messages from "Other" at the very bottom that haven't been replied to yet (messages from "Other" appearing AFTER the last "Self" message).
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
            
            # Add image compression to avoid large payload timeout
            COMPRESSED_IMG = os.path.join(WORKSPACE, f"wechat_mini_{TARGET.replace(' ', '_')}.png")
            run_cmd(f"sips -s format png -Z 1200 '{RAW_IMG}' --out '{COMPRESSED_IMG}'", timeout=10)
            
            # Use file redirection to completely avoid shell escaping issues!
            res = run_cmd(f"summarize \"{COMPRESSED_IMG}\" --prompt \"$(< {prompt_file})\" --plain --no-color --metrics off", timeout=180)
            raw_output = res.stdout.strip()
            logger.error(f"summarize code: {res.returncode}, stderr: {res.stderr}")

            # Robust JSON extraction
            json_str = ""
            match = re.search(r'(\{.*\})', raw_output, re.DOTALL)
            if match:
                json_str = match.group(1)
            else:
                json_str = raw_output # fallback

            try:
                chat_data = json.loads(json_str)
                
                # V4.0 Memory Bank Logic
                accumulated_history = load_accumulated_state(JSON_FILE)
                current_history = chat_data.get("context_history", [])
                new_history = merge_history(accumulated_history, current_history)
                chat_data["accumulated_history"] = new_history
                
                # Dump JSON to file for visibility
                with open(JSON_FILE, "w", encoding='utf-8') as jf:
                    json.dump(chat_data, jf, indent=2, ensure_ascii=False)
                    
            except json.JSONDecodeError:
                logger.debug(f"Failed to parse JSON. Raw output: {raw_output}")
                with open(JSON_FILE, "w", encoding='utf-8') as jf:
                    jf.write("{\"error\": \"JSON parsing failed\", \"raw\": " + json.dumps(raw_output, ensure_ascii=False) + "}")
                time.sleep(INTERVAL)
                continue

            if not chat_data.get("needs_reply") or not chat_data.get("new_messages_to_reply"):
                time.sleep(INTERVAL)
                continue

            new_msgs = chat_data.get("new_messages_to_reply", [])
            accumulated_context = chat_data.get("accumulated_history", [])
            
            # Use string representation of the new messages list as the state
            current_state_str = str(new_msgs)
            last_seen = ""
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r") as f:
                    last_seen = f.read().strip()
            
            if current_state_str == last_seen:
                time.sleep(INTERVAL)
                continue
                
            logger.info(f"New incoming messages detected: {new_msgs}")
            
            context_str = " | ".join(accumulated_context)
            msgs_str = " | ".join(new_msgs)
            
            # Generate reply via gemini CLI with FULL CONTEXT
            reply_prompt = (
                f"You are replying to a WeChat conversation.\n"
                f"Recent context (from memory bank): {context_str}\n"
                f"New messages to reply to: {msgs_str}\n"
                f"Persona/Style rules: {PERSONA}\n"
                f"Generate ONLY the exact text to send back. No quotes, no explanations.\n"
                f"CRITICAL RULE: If the user asks for a location, address, map, or navigation link (e.g. '去哪里', '发地图', '发定位'), "
                f"DO NOT reply with a URL. Instead, reply EXACTLY with this format: [ACTION:SEND_LOCATION|Address]. "
                f"For example, if the location is 三里屯, reply exactly: [ACTION:SEND_LOCATION|三里屯]"
            )
            prompt_file_reply = f"/tmp/wechat_reply_{TARGET.replace(' ', '_')}.txt"
            with open(prompt_file_reply, "w", encoding='utf-8') as pf:
                pf.write(reply_prompt)
            
            reply_res = run_cmd(f"gemini \"$(< {prompt_file_reply})\"")
            reply = clean_output(reply_res.stdout)
            
            if not reply or "cannot" in reply.lower():
                logger.warning("LLM failed to generate a reply, skipping.")
                time.sleep(INTERVAL)
                continue
                
            logger.info(f"Action: Replying '{reply}' to '{msgs_str}'")
            
            # Action Interceptor (V4.0)
            action_match = re.search(r'\[ACTION:SEND_LOCATION\|(.+?)\]', reply)
            send_success = False
            
            if action_match:
                address = action_match.group(1).strip()
                logger.info(f"⚡ Intercepted Location Request! Firing send_location.py for: {address}")
                script_path = os.path.expanduser("~/.openclaw/workspace/skills/wechat-auto-reply/send_location.py")
                # Call the external script
                loc_res = run_cmd(f"python3 \"{script_path}\" --target \"{TARGET}\" --address \"{address}\"")
                if "successfully sent" in loc_res.stdout:
                    send_success = True
                else:
                    logger.error(f"Failed to send location: {loc_res.stderr} | {loc_res.stdout}")
            else:
                # Safe Send via specific window title (normal text)
                send_success = safe_send_detached(TARGET, reply)
            
            if send_success:
                with open(STATE_FILE, "w") as f:
                    f.write(current_state_str)
                logger.info("Action: Reply sent and state updated.")
                
                # Update memory bank with the reply
                chat_data["accumulated_history"].append(f"Self: {reply}")
                with open(JSON_FILE, "w", encoding='utf-8') as jf:
                    json.dump(chat_data, jf, indent=2, ensure_ascii=False)
            else:
                logger.error("Action: Failed to safely send reply (Safety Abort triggered).")
                
        except Exception as e:
            logger.error(f"Error in Monitor Loop: {str(e)}")
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
