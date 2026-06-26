import pyautogui
import time
import subprocess
import argparse
import json
import os
from datetime import datetime
import pygetwindow as gw

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5  # Reduced pause for faster operation

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COORDS_FILE = os.path.join(SCRIPT_DIR, "wx_coordinates.txt")

# 企业微信安装路径（默认路径，可根据实际情况修改）
WXWORK_PATH = r"C:\Program Files (x86)\WXWork\WXWork.exe"

def check_wxwork():
    """Check if WeChat Work is running"""
    print("Checking WeChat Work status...")
    try:
        output = subprocess.check_output("tasklist | findstr WXWork.exe", shell=True)
        if b"WXWork.exe" in output:
            print("[OK] WeChat Work is running")
            return True
        else:
            print("[INFO] WeChat Work is not running")
            return False
    except:
        print("[INFO] WeChat Work is not running")
        return False

def start_wxwork():
    """启动企业微信"""
    print("Starting WeChat Work...")
    try:
        if os.path.exists(WXWORK_PATH):
            subprocess.Popen(WXWORK_PATH, shell=True)
            print(f"[OK] WeChat Work started from: {WXWORK_PATH}")
            # 等待企业微信启动
            print("Waiting for WeChat Work to initialize...")
            time.sleep(5)
            return True
        else:
            print(f"[ERROR] WeChat Work not found at: {WXWORK_PATH}")
            print("[INFO] Please manually start WeChat Work or update WXWORK_PATH")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to start WeChat Work: {e}")
        return False

def maximize_wxwork_window(wx_window):
    """最大化企业微信窗口"""
    print("Maximizing WeChat Work window...")
    try:
        # 确保窗口不是最小化状态
        if wx_window.isMinimized:
            wx_window.restore()
            time.sleep(0.5)
        
        # 最大化窗口
        wx_window.maximize()
        time.sleep(1)
        print("[OK] Window maximized")
        return True
    except Exception as e:
        print(f"[WARNING] Failed to maximize window: {e}")
        return False

def activate_wxwork_window(maximize=True):
    """Activate WeChat Work window using multiple methods"""
    print("Activating WeChat Work window...")
    
    try:
        # Get all windows
        all_windows = gw.getAllWindows()
        
        # Look for WeChat Work window with multiple identification methods
        wx_window = None
        for window in all_windows:
            if window.title:
                title = window.title
                # Try multiple ways to identify WeChat Work
                # 1. Check for known titles (including encoded versions)
                if ("企业微信" in title or 
                    "��ҵ΢��" in title or  # GBK encoded version
                    "WXWork" in title.upper()):
                    wx_window = window
                    break
        
        # If not found by title, try to find by process
        if not wx_window:
            print("[INFO] Not found by title, trying process-based detection...")
            # We'll use the first non-minimized window as fallback
            for window in all_windows:
                if not window.isMinimized and window.visible:
                    wx_window = window
                    print(f"[INFO] Selected window: {window.title}")
                    break
        
        if wx_window:
            # 激活窗口
            if wx_window.isMinimized:
                wx_window.restore()
            wx_window.activate()
            time.sleep(1)
            
            # 最大化窗口（如果需要）
            if maximize:
                maximize_wxwork_window(wx_window)
            
            print(f"[OK] Activated window: {wx_window.title}")
            
            # Get window position for later use
            window_rect = wx_window.box
            print(f"[INFO] Window position: {window_rect}")
            return window_rect
        else:
            print("[ERROR] WeChat Work window not found")
            print("[INFO] Available windows:")
            for i, window in enumerate(all_windows):
                if window.title:
                    print(f"  {i}: {window.title}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Failed to activate window: {e}")
        return None

def manual_coordinate_setup():
    """Manual coordinate setup - most reliable method"""
    print("\n" + "=" * 70)
    print("MANUAL COORDINATE SETUP")
    print("=" * 70)
    print("We need to record the exact coordinates for navigation.")
    print("Follow these steps carefully:")
    print("\n[IMPORTANT] The window has been maximized for consistent coordinates.")
    
    print("\nSTEP 1: Position your mouse")
    print("Move your mouse to the '通讯录' (Contacts) button")
    print("BUT DO NOT CLICK YET!")
    
    input("\nPress ENTER when mouse is over '通讯录' button...")
    contacts_pos = pyautogui.position()
    print(f"✓ Contacts position recorded: {contacts_pos}")
    
    print("\nSTEP 2: Now click '通讯录'")
    print("The script will click at the recorded position")
    pyautogui.click(contacts_pos)
    time.sleep(2)

    print("\nSTEP 3: Position for '新的学员'")
    print("Move mouse to '新的学员' (New Friend) button")
    
    input("Press ENTER when mouse is over '新的学员' button...")
    new_friend_pos = pyautogui.position()
    print(f"✓ New Friend position recorded: {new_friend_pos}")

    print("\nSTEP 4: Now click '新的学员'")
    pyautogui.click(new_friend_pos)
    time.sleep(2)
    
    print("\nSTEP 5: Position for '添加学员'")
    print("Move mouse to '添加学员' (Add Friend) button")
    
    input("Press ENTER when mouse is over '添加学员' button...")
    add_friend_pos = pyautogui.position()
    print(f"✓ Add Friend position recorded: {add_friend_pos}")
    
    print("\nSTEP 6: Now click '添加学员'")
    pyautogui.click(add_friend_pos)
    time.sleep(2)
    
    print("\nSTEP 5: Position for '手机号添加'")
    print("Move mouse to '手机号添加' (Add by Phone) option")
    
    input("Press ENTER when mouse is over '手机号添加'...")
    phone_add_pos = pyautogui.position()
    print(f"✓ Phone Add position recorded: {phone_add_pos}")
    
    print("\nSTEP 6: Now click '手机号添加'")
    pyautogui.click(phone_add_pos)
    time.sleep(2)
    
    print("\nSTEP 7: Enter test phone number")
    test_phone = "18655104861"  # 测试手机号
    print(f"Entering test phone number: {test_phone}")
    pyautogui.write(test_phone)
    time.sleep(1)
    
    print("\nSTEP 8: Press Enter to search")
    print("The script will press Enter to search for the phone number")
    pyautogui.press('enter')
    time.sleep(3)  # 等待搜索结果
    
    print("\nSTEP 9: Position for '添加' button")
    print("Move mouse to the '添加' (Add) button in the search results")
    
    input("Press ENTER when mouse is over '添加' button...")
    add_button_pos = pyautogui.position()
    print(f"✓ Add button position recorded: {add_button_pos}")
    
    print("\nSTEP 10: Now click '添加'")
    pyautogui.click(add_button_pos)
    time.sleep(2)
    
    print("\nSTEP 11: Position for '发送' button")
    print("Move mouse to the '发送' (Send) button in the confirmation dialog")
    
    input("Press ENTER when mouse is over '发送' button...")
    send_button_pos = pyautogui.position()
    print(f"✓ Send button position recorded: {send_button_pos}")
    
    print("\nSTEP 12: Now click '发送'")
    pyautogui.click(send_button_pos)
    time.sleep(2)

    print("\nSTEP 13: Position for '清除' button (input field)")
    print("Move mouse to the '清除' (Clear) button in the phone number input field")
    
    input("Press ENTER when mouse is over '清除' button...")
    clear_button_pos = pyautogui.position()
    print(f"✓ Clear button position recorded: {clear_button_pos}")
    
    print("\nSTEP 14: Now click '清除'")
    pyautogui.click(clear_button_pos)
    time.sleep(1)

    print("\nSTEP 15: Enter test phone number")
    test_phone = "13800138001"  # 测试手机号
    print(f"Entering test phone number: {test_phone}")
    pyautogui.write(test_phone)
    time.sleep(1)
    
    print("\nSTEP 16: Press Enter to search")
    print("The script will press Enter to search for the phone number")
    pyautogui.press('enter')
    time.sleep(3)  # 等待搜索结果
    
    print("\nSTEP 17: Position for '确认' button (user not found)")
    print("Move mouse to the '确认' (Confirm) button in the '未找到' dialog")
    
    input("Press ENTER when mouse is over '确认' button...")
    confirm_button_pos = pyautogui.position()
    print(f"✓ Confirm button position recorded: {confirm_button_pos}")
    
    print("\nSTEP 18: Now click '确认'")
    pyautogui.click(confirm_button_pos)
    time.sleep(2)
    
    print("\nSTEP 19: Now click '清除'")
    pyautogui.click(clear_button_pos)
    time.sleep(1)
    
    # Save coordinates
    with open(COORDS_FILE, "w") as f:
        f.write(f"contacts: {contacts_pos.x},{contacts_pos.y}\n")
        f.write(f"new_friend: {new_friend_pos.x},{new_friend_pos.y}\n")
        f.write(f"add_friend: {add_friend_pos.x},{add_friend_pos.y}\n")
        f.write(f"phone_add: {phone_add_pos.x},{phone_add_pos.y}\n")
        f.write(f"add_button: {add_button_pos.x},{add_button_pos.y}\n")
        f.write(f"send_button: {send_button_pos.x},{send_button_pos.y}\n")
        f.write(f"confirm_button: {confirm_button_pos.x},{confirm_button_pos.y}\n")
        f.write(f"clear_button: {clear_button_pos.x},{clear_button_pos.y}\n")
    
    print("\n✓ Coordinates saved to wx_coordinates.txt")
    print("=" * 70)
    
    return True

def load_and_use_coordinates():
    """Load and use saved coordinates"""
    if not os.path.exists(COORDS_FILE):
        print("[INFO] No saved coordinates found")
        return None
    
    print("Loading saved coordinates...")
    coordinates = {}
    
    try:
        with open(COORDS_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":")
                    x, y = map(int, value.split(","))
                    coordinates[key] = (x, y)
        
        print(f"[OK] Loaded coordinates: {coordinates}")
        
        # Use coordinates
        if "contacts" in coordinates:
            print(f"Clicking contacts at: {coordinates['contacts']}")
            pyautogui.click(coordinates['contacts'])
            time.sleep(2)

        if "new_friend" in coordinates:
            print(f"Clicking new friend at: {coordinates['new_friend']}")
            pyautogui.click(coordinates['new_friend'])
            time.sleep(2)
        
        if "add_friend" in coordinates:
            print(f"Clicking add friend at: {coordinates['add_friend']}")
            pyautogui.click(coordinates['add_friend'])
            time.sleep(2)
        
        if "phone_add" in coordinates:
            print(f"Clicking phone add at: {coordinates['phone_add']}")
            pyautogui.click(coordinates['phone_add'])
            time.sleep(2)
        
        print("[OK] Navigation with saved coordinates complete")
        return coordinates
        
    except Exception as e:
        print(f"[ERROR] Failed to use saved coordinates: {e}")
        return None

def navigate_to_add_friend(window_rect):
    """Navigate to add friend interface with coordinate options"""
    print("\n" + "=" * 70)
    print("NAVIGATION METHOD SELECTION")
    print("=" * 70)
    
    # 自动选择导航方法
    if os.path.exists(COORDS_FILE):
        print("[INFO] Using saved coordinates (automatic selection)")
        coordinates = load_and_use_coordinates()
        if coordinates:
            return coordinates
        else:
            print("[WARNING] Failed to use saved coordinates, trying manual setup...")
            manual_coordinate_setup()
            # Load the saved coordinates
            if os.path.exists(COORDS_FILE):
                with open(COORDS_FILE, "r") as f:
                    coordinates = {}
                    for line in f:
                        if ":" in line:
                            key, value = line.strip().split(":")
                            x, y = map(int, value.split(","))
                            coordinates[key] = (x, y)
                    return coordinates
            return None
    else:
        print("[INFO] No saved coordinates found, running manual setup...")
        manual_coordinate_setup()
        # Load the saved coordinates
        if os.path.exists(COORDS_FILE):
            with open(COORDS_FILE, "r") as f:
                coordinates = {}
                for line in f:
                    if ":" in line:
                        key, value = line.strip().split(":")
                        x, y = map(int, value.split(","))
                        coordinates[key] = (x, y)
                return coordinates
        return None

def add_by_phone_number(phone_number, window_rect, coordinates=None):
    """Add friend by phone number"""
    print(f"Adding phone number: {phone_number}")
    
    try:
        # Type phone number
        pyautogui.write(phone_number)
        time.sleep(1)
        
        # Press Enter to search
        pyautogui.press('enter')
        time.sleep(3)
        
        popups = gw.getWindowsWithTitle('该用户不存在')

        if popups:
            print(f"[WARNING] User {phone_number} does not exist")

            if coordinates and "confirm_button" in coordinates:
                print(f"Clicking confirm button at: {coordinates['confirm_button']}")
                pyautogui.click(coordinates['confirm_button'])
            else:
                # Common confirm button position (fallback)
                confirm_x, confirm_y = 960, 540  # Center of screen
                print("Using fallback confirm button position...")
                pyautogui.click(confirm_x, confirm_y)

            status = "User does not exist"
        else:
            # Use add button coordinates if available
            if coordinates and "add_button" in coordinates:
                print(f"Clicking add button at: {coordinates['add_button']}")
                pyautogui.click(coordinates['add_button'])
            else:
                # Press Enter to add (fallback)
                print("Using Enter key to add (fallback)")
                pyautogui.press('enter')
            time.sleep(2)
            
            # Click send button if available
            if coordinates and "send_button" in coordinates:
                print(f"Clicking send button at: {coordinates['send_button']}")
                pyautogui.click(coordinates['send_button'])
            else:
                # Press Enter to send (fallback)
                print("Using Enter key to send (fallback)")
                pyautogui.press('enter')
            time.sleep(2)
            
            print(f"[OK] Friend request sent to: {phone_number}")
            status = "Request sent"

        # Click clear button in input field
        print("Clicking clear button in input field...")
        if coordinates and "clear_button" in coordinates:
            print(f"Clicking clear button at: {coordinates['clear_button']}")
            pyautogui.click(coordinates['clear_button'])
        else:
            # Common clear button position (fallback)
            clear_x, clear_y = 1000, 380  # Near input field
            print("Using fallback clear button position...")
            pyautogui.click(clear_x, clear_y)
        time.sleep(1)
        
        return status
        
    except Exception as e:
        print(f"[ERROR] Failed to add {phone_number}: {e}")
        # Check if it's a captcha or other serious issue
        print("[CRITICAL] Possible captcha or other serious issue detected!")
        print("[INFO] Stopping operation to avoid account restrictions")
        # Raise exception to stop the whole process
        raise



def main():
    """主函数 - 接收命令行参数"""
    parser = argparse.ArgumentParser(description='企业微信自动添加好友')
    parser.add_argument('--phones', type=str, required=True,
                       help='手机号列表，用逗号分隔')
    parser.add_argument('--interval', type=int, default=30,
                       help='添加间隔（秒）')
    parser.add_argument('--maximize', action='store_true', default=True,
                       help='是否最大化窗口')
    
    args = parser.parse_args()
    
    # 解析手机号
    phone_numbers = [p.strip() for p in args.phones.split(',') if p.strip()]
    
    result = {
        "success": True,
        "total": len(phone_numbers),
        "results": [],
        "errors": []
    }

    # Check if WeChat Work is running, if not, start it
    if not check_wxwork():
        print("\n[INFO] WeChat Work is not running, attempting to start...")
        if not start_wxwork():
            print("\n[ERROR] Failed to start WeChat Work automatically!")
            print("[INFO] Please manually start WeChat Work and try again.")
            return
        
        # 等待窗口完全加载
        print("Waiting for window to fully load...")
        time.sleep(3)
    
    # User confirmation
    print(f"\nWill add {len(phone_numbers)} phone number(s):")
    for phone in phone_numbers:
        print(f"  - {phone}")
    
    print("\n[IMPORTANT] Make sure WeChat Work window is visible and not minimized!")
    print("[INFO] Starting automatically in 3 seconds...")
    time.sleep(3)
    
    # Start execution
    start_time = datetime.now()
    print(f"\nStart time: {start_time}")
    
    # Activate window and get position (with maximize)
    window_rect = activate_wxwork_window(maximize=True)
    
    if not window_rect:
        print("\n[WARNING] Could not get window position, using screen center")
    
    # Navigate to add friend (estimated positions)
    coordinates = navigate_to_add_friend(window_rect)
    if not coordinates:
        print("\n[WARNING] Navigation may have failed or no coordinates saved, but continuing...")
    

    
    # 逐个添加
    for i, phone in enumerate(phone_numbers):
        print(f"\n[{i+1}/{len(phone_numbers)}] Processing: {phone}")
        
        status = add_by_phone_number(phone, window_rect, coordinates)
        
        result["results"].append({
            "phone": phone,
            "status": status,
            "index": i + 1
        })
        
        
        
        # Wait 30 seconds if not the last one
        if i < len(phone_numbers) - 1:
            print("Waiting 30 seconds...")
            time.sleep(30)
    
    # 5. 输出JSON结果
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='企业微信自动添加好友工具')
    parser.add_argument('--setup', action='store_true', help='执行坐标设置')
    args = parser.parse_args()
    
    try:
        if args.setup:
            print("执行坐标设置...")
            # 启动企业微信
            if not check_wxwork():
                start_wxwork()
                time.sleep(5)
            # 激活窗口并最大化
            activate_wxwork_window(maximize=True)
            # 执行坐标设置
            manual_coordinate_setup()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
