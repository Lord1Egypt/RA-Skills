#!/usr/bin/env python3
"""
WX-OCR-Reply: OCR 截图识别微信聊天内容并自动回复
依赖: pyautogui, openai (用于生成回复)
"""

import subprocess
import time
import sys
import pyautogui
import os

def take_screenshot():
    """截图当前屏幕"""
    screenshot_path = "/tmp/wechat_screenshot.png"
    subprocess.run(["screencapture", "-x", screenshot_path])
    return screenshot_path

def ocr_screenshot(image_path):
    """使用 macOS Vision Framework OCR"""
    py_script = f'''
import Vision
import AppKit

image = AppKit.NSImage("{image_path}")
vn_image = Vision.VNImageRequestHandler(image, options={{}})
request = Vision.VNRecognizeTextRequest()
request.recognitionLevel = 0
vn_image.performRequests([request], error=None)

results = []
for observation in request.results:
    if observation.topCandidates(1):
        results.append(observation.topCandidates(1)[0].string)

print("\\\\n".join(results))
'''
    
    result = subprocess.run([sys.executable, "-c", py_script], capture_output=True, text=True)
    return result.stdout

def main():
    if len(sys.argv) < 2:
        print("用法: wx_ocr_reply.py <联系人名称>")
        sys.exit(1)
    
    contact_name = sys.argv[1]
    
    # 打开微信
    subprocess.run(['open', '-a', 'WeChat'])
    time.sleep(1)
    
    # 搜索联系人
    pyautogui.hotkey('command', 'f')
    time.sleep(0.5)
    pyautogui.write(contact_name)
    time.sleep(1)
    pyautogui.press('return')
    time.sleep(1)
    
    # 截图识别聊天内容
    print("截图识别聊天内容...")
    screenshot = take_screenshot()
    chat_content = ocr_screenshot(screenshot)
    print("识别到的内容:")
    print(chat_content)
    
    # TODO: 调用 LLM 生成回复
    # reply = generate_reply(chat_content)
    # pyautogui.write(reply)
    # pyautogui.press('return')

if __name__ == "__main__":
    main()
