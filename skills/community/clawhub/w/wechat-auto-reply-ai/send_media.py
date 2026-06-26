import time
import subprocess
import os
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def check_focus():
    res = run_cmd("osascript -e 'tell application \"System Events\" to get name of first application process whose frontmost is true'")
    return res.stdout.strip() in ["WeChat", "微信"]

def send_file_to_wechat(target_title, file_path):
    # 验证文件是否存在
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        logger.error(f"File not found: {abs_path}")
        return False
        
    logger.info(f"Targeting window '{target_title}' for file sending: {abs_path}")
    
    # 1. 强制激活目标独立小窗
    focus_res = run_cmd(f"peekaboo window focus --app 微信 --window-title '{target_title}'")
    if "Error" in focus_res.stdout or "not found" in focus_res.stdout:
        logger.error(f"Target window '{target_title}' not found.")
        return False
    time.sleep(0.5)
    
    # 2. 安全锁：确认焦点
    if not check_focus():
        logger.warning("Safety Abort: WeChat is not the frontmost app.")
        return False
        
    # 3. 使用 AppleScript 劫持系统剪贴板，将文件引用 (POSIX file) 塞入剪贴板
    logger.info("Injecting file reference into clipboard...")
    applescript_cmd = f"""osascript -e 'set the clipboard to POSIX file "{abs_path}"'"""
    run_cmd(applescript_cmd)
    time.sleep(0.5)
    
    # 4. 模拟 Cmd+V 粘贴文件
    logger.info("Pasting file into WeChat...")
    run_cmd("peekaboo hotkey 'cmd,v'")
    
    # 重要：微信解析图片或文件需要一点点时间，不能马上按回车
    time.sleep(1.0)
    
    # 5. 安全发送
    if check_focus():
        logger.info("Sending file...")
        run_cmd("peekaboo hotkey 'return'")
        return True
    else:
        logger.warning("Safety Abort: WeChat lost focus right before hitting return.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Send Image/File/GIF to a Detached WeChat Window")
    parser.add_argument("--target", required=True, help="The exact title of the detached WeChat chat window.")
    parser.add_argument("--file", required=True, help="The absolute or relative path to the file/image/GIF.")
    args = parser.parse_args()
    
    success = send_file_to_wechat(args.target, args.file)
    if success:
        logger.info("✅ File successfully sent.")
    else:
        logger.error("❌ Failed to send file.")

if __name__ == "__main__":
    main()