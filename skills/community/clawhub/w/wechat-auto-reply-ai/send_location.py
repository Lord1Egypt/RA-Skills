#!/usr/bin/env python3
import sys
import argparse
import subprocess
import urllib.parse
import time

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return res
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}\nError: {e.stderr}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Send a location link via WeChat UI automation.")
    parser.add_argument("--target", required=True, help="Exact title of the WeChat detached window (e.g., '森哥')")
    parser.add_argument("--address", required=True, help="The location name or address to send (e.g., '朝阳大悦城')")
    args = parser.parse_args()

    encoded_address = urllib.parse.quote(args.address)
    # Using Tencent Map search link (optimal for WeChat)
    map_url = f"https://uri.amap.com/search?keyword={encoded_address}"
    
    message_text = f"📍 我在这里/去这里：{args.address}\n导航链接：{map_url}"
    
    print(f"🔍 Focusing WeChat window for '{args.target}'...")
    run_cmd(f"peekaboo window focus --app 微信 --window-title '{args.target}'")
    time.sleep(0.5)

    print("🛡️ Safety Lock Check...")
    check_focus_cmd = "osascript -e 'tell application \"System Events\" to get name of first application process whose frontmost is true'"
    res = subprocess.run(check_focus_cmd, shell=True, capture_output=True, text=True)
    if "微信" not in res.stdout and "WeChat" not in res.stdout:
        print("🚨 SAFETY ABORT: WeChat is not the active window!")
        sys.exit(1)

    print("📋 Copying location message to clipboard...")
    # Escape quotes for AppleScript
    safe_text = message_text.replace('"', '\\"')
    copy_cmd = f"osascript -e 'set the clipboard to \"{safe_text}\"'"
    run_cmd(copy_cmd)

    print("✉️ Pasting and sending...")
    run_cmd("osascript -e 'tell application \"System Events\" to keystroke \"v\" using command down'")
    time.sleep(0.5)
    run_cmd("osascript -e 'tell application \"System Events\" to key code 36'") # Return key

    print(f"✅ Location '{args.address}' successfully sent to {args.target}!")

if __name__ == "__main__":
    main()
