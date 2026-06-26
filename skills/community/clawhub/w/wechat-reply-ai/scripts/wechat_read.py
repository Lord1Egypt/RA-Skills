import argparse
import subprocess
import sys
import time
import win32clipboard
import uiautomation as auto
from pywinauto import Desktop
from pywinauto.keyboard import send_keys
import os


def find_wechat_window(timeout: float = 8.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        for win in Desktop(backend="uia").windows():
            title = (win.window_text() or "").strip()
            if not title:
                continue
            if "微信" in title or "Weixin" in title:
                handle = win.handle
                window = auto.ControlFromHandle(handle)
                if window:
                    return window
        time.sleep(0.5)
    raise RuntimeError("未找到微信主窗口")


def open_chat(window, contact_name):
    try:
        search_box = window.EditControl(Name="搜索")
        if search_box.Exists(0, 0):
            search_box.Click(simulateMove=False)
            time.sleep(0.3)
            search_box.SendKeys("{Ctrl}a{Del}", waitTime=0.1)
            time.sleep(0.2)
            search_box.SendKeys(contact_name, interval=0.05, waitTime=0.1)
            time.sleep(1.0)
            send_keys("{ENTER}")
            time.sleep(1.5)
            return
    except:
        pass

    send_keys("^f")
    time.sleep(0.6)
    send_keys("^a")
    time.sleep(0.2)
    send_keys("{DEL}")
    win32clipboard.OpenClipboard()
    win32clipboard.SetClipboardText(contact_name)
    win32clipboard.CloseClipboard()
    time.sleep(0.1)
    send_keys("^v")
    time.sleep(1.0)
    send_keys("{ENTER}")
    time.sleep(1.5)


def capture_window_png():
    """使用 uiautomation 截图"""
    script = r'''
param([string]$outPath, [int]$x, [int]$y, [int]$w, [int]$h)

Add-Type -AssemblyName System.Drawing

$bitmap = New-Object System.Drawing.Bitmap($w, $h)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($x, $y, 0, 0, (New-Object System.Drawing.Size($w, $h)))
$bitmap.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
Write-Output "OK"
'''

    window = find_wechat_window()
    rect = window.BoundingRectangle
    x, y = rect.left, rect.top
    w, h = rect.right - rect.left, rect.bottom - rect.top

    out_path = r"D:\Backup\Documents\Playground\wechat_screen.png"

    result = subprocess.run([
        'powershell', '-command',
        f'{script} -outPath "{out_path}" -x {x} -y {y} -w {w} -h {h}'
    ], capture_output=True, text=True, timeout=15)

    if os.path.exists(out_path):
        return out_path
    return None


def get_messages_by_keys():
    """通过键盘快捷键获取消息"""
    # 按 Home 键到顶部
    send_keys("{HOME}")
    time.sleep(0.2)

    # 尝试多次向上滚动并全选
    for _ in range(3):
        send_keys("^a")
        time.sleep(0.3)
        send_keys("^c")
        time.sleep(0.5)

        win32clipboard.OpenClipboard()
        try:
            text = win32clipboard.GetClipboardText()
            if text and len(text.strip()) > 10:
                win32clipboard.CloseClipboard()
                return text
        except:
            pass
        finally:
            win32clipboard.CloseClipboard()

        send_keys("{PGUP}")
        time.sleep(0.2)

    return ""


def main():
    parser = argparse.ArgumentParser(description="读取微信聊天记录")
    parser.add_argument("--contact", default="mike--", help="联系人名称")
    parser.add_argument("--lines", type=int, default=10, help="读取最近N条")
    parser.add_argument("--screenshot", action="store_true", help="截图模式")
    args = parser.parse_args()

    auto.SetGlobalSearchTimeout(3)

    try:
        window = find_wechat_window()
        window.SetActive()
        time.sleep(0.5)

        print(f"打开与 {args.contact} 的聊天...")
        open_chat(window, args.contact)
        time.sleep(1)

        if args.screenshot:
            print("截图...")
            img_path = capture_window_png()
            if img_path:
                print(f"\n截图已保存: {img_path}")
                print("请查看截图告诉我 mike-- 回了什么")
            else:
                print("截图失败")
            return 0

        # 尝试读取消息
        print("尝试读取消息...")
        text = get_messages_by_keys()

        print(f"\n=== 与 {args.contact} 的消息 ===\n")
        if text and len(text.strip()) > 5:
            lines = text.strip().split('\n')
            clean = [l.strip() for l in lines if l.strip()]
            for i, line in enumerate(clean[-args.lines:], 1):
                print(f"{i}. {line}")
        else:
            print("无法读取")

            # 最后尝试截图
            print("\n尝试截图...")
            img_path = capture_window_png()
            if img_path:
                print(f"截图: {img_path}")

        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
