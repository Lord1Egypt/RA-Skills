#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
focusless.py —— Windows 下「拉起进程但不抢桌面焦点」的通用防护。

用途：给 autologin.py（QQ 浏览器 skill 原生点击自动登录）以及后续接入
主流程的「登录态自动恢复」步骤复用。自动化在用户桌面运行时，新拉起的
浏览器 / daemon 不应改变用户当前正在使用的窗口。

四层防御（缺一不可，任何单层都可能被 Chromium 忽略）：
  1. CreateProcess STARTUPINFO: STARTF_USESHOWWINDOW + SW_SHOWNOACTIVATE
     —— 窗口第一次显示时就不激活（部分程序遵守）。
  2. 启动参数层的配合（由调用方负责）：去掉 --start-maximized，
     改用固定窗口位置/尺寸 + 禁用后台节流，避免前台最大化与渲染节流。
  3. 窗口加固（本模块核心）：以「启动前后的可见顶层窗口句柄差集」精确
     识别新进程创建的窗口，只对这些新窗口追加 WS_EX_NOACTIVATE 扩展样式
     并压到 Z 序底部。绝不触碰用户已有的任何窗口。
  4. 兜底恢复：记录启动前的前台窗口，若焦点仍被改动，用
     AttachThreadInput + SetForegroundWindow 恢复用户原本的窗口。

用法：
    guard = FocusGuard("autologin")
    p = guard.launch([QB] + flags, stdout=qf, stderr=subprocess.STDOUT)
    ...
    guard.harden(timeout=10)      # 等新窗口出现并加固
    guard.report()                # 打印焦点对比，必要时恢复
"""
import ctypes
import os
import subprocess
import time

IS_WIN = (os.name == "nt")

SW_SHOWNOACTIVATE = 4
SW_RESTORE = 9
GWL_EXSTYLE = -20
WS_EX_NOACTIVATE = 0x08000000
HWND_BOTTOM = 1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOACTIVATE = 0x0010
SWP_NOSENDCHANGING = 0x0400
CREATE_NO_WINDOW = 0x08000000

if IS_WIN:
    from ctypes import wintypes

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    user32.GetForegroundWindow.restype = wintypes.HWND
    user32.GetForegroundWindow.argtypes = []
    user32.IsWindow.argtypes = [wintypes.HWND]
    user32.IsWindow.restype = wintypes.BOOL
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.IsWindowVisible.restype = wintypes.BOOL
    user32.IsIconic.argtypes = [wintypes.HWND]
    user32.IsIconic.restype = wintypes.BOOL
    user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.GetWindowTextW.restype = ctypes.c_int
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    user32.GetWindowThreadProcessId.restype = wintypes.DWORD
    user32.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.GetWindowLongW.restype = wintypes.LONG
    user32.SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.LONG]
    user32.SetWindowLongW.restype = wintypes.LONG
    user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND,
                                    ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                    ctypes.c_int, wintypes.UINT]
    user32.SetWindowPos.restype = wintypes.BOOL
    user32.EnumWindows.argtypes = [WNDENUMPROC, wintypes.LPARAM]
    user32.EnumWindows.restype = wintypes.BOOL
    user32.BringWindowToTop.argtypes = [wintypes.HWND]
    user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.SetForegroundWindow.argtypes = [wintypes.HWND]
    user32.SetForegroundWindow.restype = wintypes.BOOL
    user32.AttachThreadInput.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.BOOL]
    user32.AttachThreadInput.restype = wintypes.BOOL
    kernel32.GetCurrentThreadId.restype = wintypes.DWORD
    kernel32.GetCurrentThreadId.argtypes = []


def startupinfo_no_focus():
    """CreateProcess 层：窗口首次 ShowWindow 用 SW_SHOWNOACTIVATE。"""
    if not IS_WIN:
        return None
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = SW_SHOWNOACTIVATE
    return si


def creationflags_no_window():
    """控制台进程不弹黑窗口（对 GUI 程序无副作用，输出仍可 PIPE 捕获）。"""
    return CREATE_NO_WINDOW if IS_WIN else 0


def foreground():
    """返回 (hwnd, 标题)；非 Windows 返回 (0, '')。"""
    if not IS_WIN:
        return (0, "")
    h = int(user32.GetForegroundWindow())
    return (h, window_title(h))


def window_title(hwnd):
    if not IS_WIN or not hwnd:
        return ""
    buf = ctypes.create_unicode_buffer(512)
    user32.GetWindowTextW(hwnd, buf, 512)
    return buf.value


def visible_windows():
    """当前所有可见顶层窗口句柄集合。"""
    if not IS_WIN:
        return set()
    found = set()

    def cb(hwnd, _lparam):
        if user32.IsWindowVisible(hwnd):
            found.add(int(hwnd))
        return True

    user32.EnumWindows(WNDENUMPROC(cb), 0)
    return found


def harden(hwnd):
    """给窗口追加 WS_EX_NOACTIVATE 并压到 Z 序底部（不改用户已有窗口）。"""
    if not IS_WIN or not hwnd:
        return False
    try:
        style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_NOACTIVATE)
        user32.SetWindowPos(hwnd, HWND_BOTTOM, 0, 0, 0, 0,
                            SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE | SWP_NOSENDCHANGING)
        return True
    except Exception:
        return False


def restore_foreground(hwnd):
    """焦点被抢后恢复到原前台窗口（AttachThreadInput 绕开前台锁定）。"""
    if not IS_WIN or not hwnd or not user32.IsWindow(hwnd):
        return False
    fg = int(user32.GetForegroundWindow())
    if fg == hwnd:
        return True
    cur_tid = int(kernel32.GetCurrentThreadId())
    fg_tid = int(user32.GetWindowThreadProcessId(fg, None))
    attached = False
    try:
        if fg_tid and fg_tid != cur_tid:
            attached = bool(user32.AttachThreadInput(cur_tid, fg_tid, True))
        # ⚠️ 绝不对正常显示的窗口调 SW_RESTORE：全屏游戏/最大化窗口会被
        # 还原成普通窗口，反而破坏用户桌面。仅在确实最小化时才还原。
        if user32.IsIconic(hwnd):
            user32.ShowWindow(hwnd, SW_RESTORE)
        user32.BringWindowToTop(hwnd)
        user32.SetForegroundWindow(hwnd)
    finally:
        if attached:
            user32.AttachThreadInput(cur_tid, fg_tid, False)
    return int(user32.GetForegroundWindow()) == hwnd


class FocusGuard:
    """包住一段「会拉起进程」的代码，保证桌面焦点不被改变。"""

    def __init__(self, label="auto-login"):
        self.label = label
        self.origin_hwnd, self.origin_title = foreground()
        self.before_windows = visible_windows()
        self.hardened = set()
        self.reports = []

    def launch(self, argv, no_window=True, **kwargs):
        """替代 subprocess.Popen，注入无焦点启动参数。

        no_window=False 用于 CLI/daemon：只给 STARTUPINFO，避免 CREATE_NO_WINDOW
        影响它自己 lazy-start 子进程的控制台继承。
        """
        kwargs.setdefault("startupinfo", startupinfo_no_focus())
        if IS_WIN and no_window:
            kwargs["creationflags"] = kwargs.get("creationflags", 0) | CREATE_NO_WINDOW
        return subprocess.Popen(argv, **kwargs)

    def harden_new_windows(self, timeout=12, poll=0.5):
        """轮询识别新出现的窗口并加固；等窗口数稳定后才返回。

        Chromium 的窗口是渐进创建的（先隐藏壳窗口，再主窗口），
        找到第一批就返回会漏掉后面真正会抢焦点的主窗口。
        """
        if not IS_WIN:
            return 0
        deadline = time.time() + timeout
        stable = 0
        while time.time() < deadline:
            new = visible_windows() - self.before_windows - self.hardened
            for hwnd in new:
                if harden(hwnd):
                    self.hardened.add(hwnd)
            stable = 0 if new else stable + 1
            if self.hardened and stable >= 4:   # 连续 2s 无新窗口
                break
            time.sleep(poll)
        return len(self.hardened)

    def report(self, stage="after-launch"):
        """对比焦点；若被改动则恢复。返回 (是否保持原焦点, 描述)。"""
        hwnd, title = foreground()
        kept = (hwnd == self.origin_hwnd)
        desc = "焦点保持不变" if kept else "焦点被改动，已尝试恢复"
        if not kept and IS_WIN:
            restore_foreground(self.origin_hwnd)
            hwnd2, title2 = foreground()
            desc += ("，恢复成功" if hwnd2 == self.origin_hwnd
                     else "，恢复失败（当前：%s）" % (title2 or "无标题"))
        line = ("[FocusGuard/%s] %s | 原前台=%s | 现前台=%s | 新窗口加固=%d | %s"
                % (self.label, stage, self.origin_title or "<无标题>",
                   title or "<无标题>", len(self.hardened), desc))
        self.reports.append(line)
        print(line)
        return (kept, desc)
