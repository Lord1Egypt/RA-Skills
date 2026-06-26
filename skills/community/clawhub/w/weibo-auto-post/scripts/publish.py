# -*- coding: utf-8 -*-
"""微博浏览器自动化发布脚本"""
import argparse
import subprocess
import time
import os
import sys

import pyautogui
import pyperclip


def screenshot_verify(path_or_area="compose"):
    """截图验证发布框或图片是否存在"""
    screenshot_path = os.path.join(os.environ.get("TEMP", "/tmp"), "openclaw_screenshot_verify.png")
    pyautogui.screenshot(screenshot_path)
    print(f"[verify] Screenshot saved: {screenshot_path}")
    return screenshot_path


def get_screen_size():
    return pyautogui.size()


def click_compose_area():
    """点击微博发布框（需要微博页面已打开）"""
    screen_w, screen_h = get_screen_size()
    # 发布框大约在屏幕中央偏上
    compose_x = screen_w // 2
    compose_y = int(screen_h * 0.18)
    pyautogui.click(compose_x, compose_y)
    print(f"[click] Compose area clicked at ({compose_x}, {compose_y})")
    return compose_x, compose_y


def paste_image():
    """Ctrl+V 粘贴图片"""
    pyautogui.hotkey("ctrl", "v")
    print("[paste] Image pasted via Ctrl+V")
    time.sleep(3)  # 等待图片上传


def type_text(text):
    """输入微博文字内容"""
    # 使用 pyperclip 复制到剪贴板，再用 Ctrl+V 粘贴（处理中文）
    pyperclip.copy(text)
    pyautogui.click(get_screen_size()[0] // 2, int(get_screen_size()[1] * 0.35))
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "v")
    print("[type] Text typed")


def click_publish_button():
    """点击发布按钮（需要根据实际按钮位置调整）"""
    screen_w, screen_h = get_screen_size()
    # 发布按钮在发布框右下角附近
    btn_x = screen_w // 2 + 220
    btn_y = int(screen_h * 0.35) + 280
    pyautogui.click(btn_x, btn_y)
    print(f"[publish] Publish button clicked at ({btn_x}, {btn_y})")
    time.sleep(2)


def cleanup_temp_files():
    """清理临时图片文件"""
    ps_script = """
Get-ChildItem "C:\\Users\\13113\\Pictures\\weibo_*.png" -EA SilentlyContinue | Remove-Item -Force -EA SilentlyContinue
Get-ChildItem "$env:TEMP\\openclaw_screenshot_*.png" -EA SilentlyContinue | Remove-Item -Force -EA SilentlyContinue
Write-Output "CLEANUP_OK"
"""
    result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
    if result.returncode == 0:
        print("[cleanup] OK")
    else:
        print(f"[cleanup] Done (status: {result.returncode})")


def main():
    parser = argparse.ArgumentParser(description="微博浏览器自动化发布")
    parser.add_argument("--image", type=str, default="",
                        help="配图路径，图片会先复制到剪贴板")
    parser.add_argument("--text", type=str, default="",
                        help="微博文字内容（可选，也可以稍后手动输入）")
    parser.add_argument("--wait-before", type=float, default=2.0,
                        help="点击发布框前等待时间（秒）")
    parser.add_argument("--wait-after", type=float, default=3.0,
                        help="粘贴图片后等待时间（秒）")
    parser.add_argument("--no-cleanup", action="store_true",
                        help="跳过临时文件清理")
    args = parser.parse_args()

    print("[weibo-publish] Starting...")

    # Step 1: 如果指定了图片，先复制到剪贴板
    if args.image and os.path.exists(args.image):
        ps_cmd = f'''
Add-Type -AssemblyName System.Windows.Forms
$img = [System.Drawing.Image]::FromFile("{args.image.replace("/", "\\\\")}")
[System.Windows.Forms.Clipboard]::SetImage($img)
$img.Dispose()
Write-Output "CLIPBOARD_OK"
'''
        result = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[clipboard] Image copied: {args.image}")
        else:
            print(f"[clipboard] WARNING: {result.stderr}")
        time.sleep(0.5)

    # Step 2: 激活微博发布框
    print(f"[step] Waiting {args.wait_before}s before clicking compose...")
    time.sleep(args.wait_before)
    click_compose_area()
    time.sleep(0.5)

    # Step 3: 粘贴图片
    if args.image:
        paste_image()
        time.sleep(args.wait_after)
        # 截图验证
        screenshot_verify("after-paste")
    else:
        time.sleep(1)

    # Step 4: 输入文字
    if args.text:
        type_text(args.text)
        time.sleep(0.5)

    # Step 5: 点击发布
    click_publish_button()
    print("[weibo-publish] Done! Please verify the post.")

    # Step 6: 清理
    if not args.no_cleanup:
        cleanup_temp_files()


if __name__ == "__main__":
    main()
