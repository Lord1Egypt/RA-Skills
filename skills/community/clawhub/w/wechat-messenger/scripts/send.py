# -*- coding: utf-8 -*-
"""
WeChat Fast Messenger v2.0
Single-script, zero-screenshot, target < 5s.
Usage: python send.py "contact" "message"
"""
import sys, time, ctypes
from ctypes import wintypes
import win32gui, win32con, pyperclip

INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
VK_V, VK_A, VK_RETURN = 0x56, 0x41, 0x0D
VK_CONTROL = 0x11

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk",wintypes.WORD),("wScan",wintypes.WORD),
                ("dwFlags",wintypes.DWORD),("time",wintypes.DWORD),
                ("dwExtraInfo",ctypes.POINTER(ctypes.c_ulong))]
class INPUT(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [("ki",KEYBDINPUT),("mi",ctypes.c_char*32)]
    _anonymous_=("_u",)
    _fields_ = [("type",wintypes.DWORD),("_u",_U)]

u32 = ctypes.windll.user32

def _key(vk, up=False):
    i = INPUT()
    i.type = INPUT_KEYBOARD
    i.ki.wVk = vk
    i.ki.dwFlags = KEYEVENTF_KEYUP if up else 0
    u32.SendInput(1, ctypes.byref(i), ctypes.sizeof(i))

def press(vk, d=0.04):
    _key(vk,False); time.sleep(d); _key(vk,True)

def combo(*keys, d=0.05):
    for k in keys: _key(k,False)
    time.sleep(d)
    for k in reversed(keys): _key(k,True)

def paste(t):
    pyperclip.copy(t); time.sleep(0.03)
    combo(VK_CONTROL, VK_V, d=0.03)

def click(x,y):
    u32.SetCursorPos(x,y)
    u32.mouse_event(0x0002|0x0004,0,0,0,0)

def find_wechat():
    found = None
    def cb(h,_):
        nonlocal found
        if win32gui.IsWindowVisible(h) and "微信" in win32gui.GetWindowText(h):
            found=h; return False
        return True
    win32gui.EnumWindows(cb,None)
    if not found: found=win32gui.FindWindow("WeChatMainWndForPC",None)
    if not found: print("[ERROR] WeChat not found"); return None
    if win32gui.IsIconic(found): win32gui.ShowWindow(found,win32con.SW_RESTORE)
    u32.SetForegroundWindow(found)
    time.sleep(0.12)
    return found

def send(contact, message):
    t0 = time.time()
    hwnd = find_wechat()
    if not hwnd: return False
    r = win32gui.GetWindowRect(hwnd)
    x0,y0,w,h = r[0],r[1],r[2]-r[0],r[3]-r[1]
    # search box
    click(x0+130, y0+50); time.sleep(0.08)
    combo(VK_CONTROL, VK_A, d=0.03); time.sleep(0.02)
    paste(contact); time.sleep(0.25)
    press(VK_RETURN, d=0.06)
    # wait chat
    time.sleep(0.8)
    # input box
    click(x0+w//2, y0+h-60); time.sleep(0.06)
    paste(message); time.sleep(0.03)
    press(VK_RETURN, d=0.06)
    print(f"[OK] '{message}' -> {contact} ({time.time()-t0:.1f}s)")
    return True

if __name__=="__main__":
    if len(sys.argv)<3: print("Usage: python send.py <contact> <message>"); sys.exit(1)
    sys.exit(0 if send(sys.argv[1],sys.argv[2]) else 1)
