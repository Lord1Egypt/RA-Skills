#!/usr/bin/env python3
# wb_mouse_checkin.py  ——  WorkBuddy「Buddy 加油站」每日签到（自动领积分）
# ============================================================================
# 这是一个可分享、零第三方依赖的纯 ctypes 实现（仅依赖 Windows 系统 API + 标准库）。
# 鼠标点击 / 窗口置前 / 窗口截图 全部用 ctypes 完成；
# 若本机恰好装了 desktop-control-win skill，截图会优先用它（更稳），否则回退 PrintWindow。
#
# 【分享版 · 隐私说明】
#   本脚本不含任何个人身份信息、绝对路径或推送目标。所有坐标都是"相对客户区左下角"
#   的通用设计，第一次用请按自己屏幕校准（见下方 CALIBRATION 常量 与 references/calibration.md）。
#
# 用法:
#   python wb_mouse_checkin.py            # 干跑: 打印窗口信息 + 计算好的点击坐标, 不点击
#   python wb_mouse_checkin.py -run       # 执行真实签到
#   python wb_mouse_checkin.py -calibrate # 交互式校准(终端文字): 把鼠标移到三个目标点各按一次回车
#   python wb_mouse_checkin.py -calibrate-gui # 弹窗校准(推荐通用): 悬浮窗倒计时自动采样鼠标, 三步写 calibrate.json
#
# 退出码: 0=成功/已处于[今日已领]   2=失败(未领取/面板异常)   3=未找到 WorkBuddy 窗口
# ============================================================================

import ctypes, sys, time, zlib, struct, subprocess, os, json

if sys.platform != "win32":
    print("ERROR: 本脚本仅支持 Windows (依赖 ctypes.windll / user32 / gdi32)。")
    sys.exit(3)

# ===================== DPI 感知 (2026-08-04 关键修复) =====================
# 根因: Python 进程默认 DPI-unaware, GetWindowRect/ClientToScreen 返回的是
# Windows DPI 虚拟化的【逻辑坐标】, 而 SetCursorPos/mouse_event 用的是【物理坐标】,
# 两者差 2~3 倍缩放(本机实测: 窗口逻辑(619,169) -> 物理(1238,338)/(1857,507)),
# 导致"打印坐标正确但点击全打在窗口外"。强制 Per-Monitor DPI Aware 后,
# GetWindowRect 返回物理坐标, 与 SetCursorPos 同一坐标系, 点击精确命中。
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)   # PROCESS_PER_MONITOR_DPI_AWARE
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()     # 旧系统回退
    except Exception:
        pass

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
gdi32 = ctypes.windll.gdi32

# ============================== 配置区（按自己屏幕校准） ==============================
# 目标窗口标题（WorkBuddy 桌面客户端固定叫这个；若你的版本不同改这里）。
TARGET_TITLE = "WorkBuddy"

# 三个点击点统一用「相对客户区左下角」表示:
#   x = 距客户区左边缘的像素 (逻辑像素, 自动乘 DPI 缩放)
#   y = 距客户区底边缘的像素
# 这样窗口任意缩放(高/宽变化)都能命中, 校准一次永久复用。
# 校准方法见 references/calibration.md（或先 -calibrate 截一张图用画图量）。
# —— 以下为作者 1080p/常见布局的示例值, 你大概率需要改 ——
AVATAR_LEFT   = 94    # 左下角头像(账户菜单): 距左
AVATAR_BOTTOM = 41    #                     距底
GAS_LEFT      = 140   # "Buddy 加油站"菜单项: 距左
GAS_BOTTOM    = 541   #                     距底
CLAIM_LEFT    = 89    # "立即领取"按钮:      距左
CLAIM_BOTTOM  = 113   #                     距底

# 结果截图保存路径（默认脚本同目录）。
RESULT_NAME = "checkin_result.png"
# =============================================================================================

# ===================== 更新续签 · Windows 计划任务（2026-08-17） =====================
# 关键背景(老板质疑): WorkBuddy 重启时, 定时任务会话(运行在 WorkBuddy 应用进程内)
# 会连同"等几分钟重跑"的逻辑一起被终止 —— 依赖会话续签不可靠!
# 可靠载体 = Windows 任务计划程序(schtasks): 独立于 WorkBuddy 进程,
# 脚本点[重启升级]前注册一个 RESUME_DELAY 秒后运行的 -resume 计划任务,
# WorkBuddy 重启不影响它; 到点独立 python 进程唤醒, 检查续签标记 -> 等窗口 -> 补签。
RESUME_TASK_NAME = "WB_Checkin_Resume"   # Windows 计划任务名
RESUME_DELAY_SEC = 480                   # 点更新后多久由计划任务接管续签(8 分钟, 覆盖下载+安装+重启)
RESUME_WAIT_WIN  = 600                   # -resume 等 WorkBuddy 窗口出现的上限(秒)


# ===================== 显式声明 Win32 调用签名（关键！） =====================
# HWND 是 64 位指针, 不声明 argtypes 会被 ctypes 默认按 32 位 c_int 截断,
# 导致 SetForegroundWindow 等静默失败(窗口置不了顶)。这是最容易踩的坑。
HWND  = ctypes.c_void_p
BOOL  = ctypes.c_bool
LONG  = ctypes.c_long
INT   = ctypes.c_int
UINT  = ctypes.c_uint
SHORT = ctypes.c_short

user32.EnumWindows.argtypes = [ctypes.WINFUNCTYPE(BOOL, HWND, ctypes.c_void_p), ctypes.c_void_p]
user32.EnumWindows.restype = BOOL
user32.GetWindowTextW.argtypes = [HWND, ctypes.c_wchar_p, INT]
user32.GetWindowTextW.restype = INT
user32.GetWindowTextLengthW.argtypes = [HWND]
user32.GetWindowTextLengthW.restype = INT
user32.IsWindowVisible.argtypes = [HWND]
user32.IsWindowVisible.restype = BOOL
user32.IsWindow.argtypes = [HWND]                # 2026-08-17: 检测旧窗口句柄是否失效(点更新后应用重启)
user32.IsWindow.restype = BOOL
user32.FindWindowW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
user32.FindWindowW.restype = HWND
user32.GetWindowRect.argtypes = [HWND, ctypes.c_void_p]
user32.GetWindowRect.restype = BOOL
user32.GetClientRect.argtypes = [HWND, ctypes.c_void_p]
user32.GetClientRect.restype = BOOL
user32.ClientToScreen.argtypes = [HWND, ctypes.c_void_p]
user32.ClientToScreen.restype = BOOL
user32.IsIconic.argtypes = [HWND]
user32.IsIconic.restype = BOOL
user32.ShowWindow.argtypes = [HWND, INT]
user32.ShowWindow.restype = BOOL
user32.GetForegroundWindow.argtypes = []
user32.GetForegroundWindow.restype = HWND
user32.SetForegroundWindow.argtypes = [HWND]
user32.SetForegroundWindow.restype = BOOL
user32.GetWindowThreadProcessId.argtypes = [HWND, ctypes.POINTER(UINT)]
user32.GetWindowThreadProcessId.restype = UINT
user32.AttachThreadInput.argtypes = [UINT, UINT, BOOL]
user32.AttachThreadInput.restype = BOOL
user32.SetWindowPos.argtypes = [HWND, HWND, INT, INT, INT, INT, UINT]
user32.SetWindowPos.restype = BOOL
user32.SetCursorPos.argtypes = [INT, INT]
user32.SetCursorPos.restype = BOOL
user32.mouse_event.argtypes = [UINT, UINT, UINT, UINT, UINT]
user32.mouse_event.restype = None
user32.GetWindowDC.argtypes = [HWND]
user32.GetWindowDC.restype = HWND
user32.ReleaseDC.argtypes = [HWND, HWND]
user32.ReleaseDC.restype = INT
user32.PrintWindow.argtypes = [HWND, HWND, UINT]
user32.PrintWindow.restype = BOOL

gdi32.CreateCompatibleDC.argtypes = [HWND]
gdi32.CreateCompatibleDC.restype = HWND
gdi32.CreateCompatibleBitmap.argtypes = [HWND, INT, INT]
gdi32.CreateCompatibleBitmap.restype = HWND
gdi32.SelectObject.argtypes = [HWND, HWND]
gdi32.SelectObject.restype = HWND
gdi32.GetDIBits.argtypes = [HWND, HWND, UINT, UINT, ctypes.c_void_p, ctypes.c_void_p, UINT]
gdi32.GetDIBits.restype = INT
gdi32.DeleteObject.argtypes = [HWND]
gdi32.DeleteObject.restype = INT
gdi32.DeleteDC.argtypes = [HWND]
gdi32.DeleteDC.restype = INT

SW_RESTORE  = 9
HWND_TOP    = HWND(0)
SWP_NOMOVE  = 0x0002
SWP_NOSIZE  = 0x0001
PW_CLIENTONLY = 1  # PrintWindow 只画客户区

class RECT(ctypes.Structure):
    _fields_ = [("left", LONG), ("top", LONG), ("right", LONG), ("bottom", LONG)]
class POINT(ctypes.Structure):
    _fields_ = [("x", LONG), ("y", LONG)]

user32.GetCursorPos.argtypes = [ctypes.POINTER(POINT)]
user32.GetCursorPos.restype = BOOL
user32.GetSystemMetrics.argtypes = [INT]
user32.GetSystemMetrics.restype = INT
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", UINT), ("biWidth", INT), ("biHeight", INT),
                ("biPlanes", SHORT), ("biBitCount", SHORT), ("biCompression", UINT),
                ("biSizeImage", UINT), ("biXPelsPerMeter", INT), ("biYPelsPerMeter", INT),
                ("biClrUsed", UINT), ("biClrImportant", UINT)]

# ===================== 找 WorkBuddy 主窗口 =====================
# 坑: WorkBuddy 可能存在多个标题含 "WorkBuddy" 的窗口(如 "WorkBuddy - 个人中心 - 千问" 子窗口)。
# 子串匹配会命中 z 序最前的子窗口(可能是最小化/未显示的幽灵窗口), 导致所有点击打空。
# 修复: 精确匹配标题 == "WorkBuddy" 优先, 无精确匹配才回退子串。
_target = None
def _callback(hwnd, lparam):
    global _target
    if not user32.IsWindowVisible(hwnd):
        return True
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return True
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    title = buf.value.strip()
    if title == TARGET_TITLE:          # 精确匹配主窗口 -> 立即选中
        _target = hwnd
        return False
    if _target is None and TARGET_TITLE in title:   # 兜底: 记录第一个子串匹配
        _target = hwnd
    return True

EnumWindowsProc = ctypes.WINFUNCTYPE(BOOL, HWND, ctypes.c_void_p)
user32.EnumWindows(EnumWindowsProc(_callback), 0)
if not _target:
    _target = user32.FindWindowW(None, TARGET_TITLE)
if not _target:
    print(f"ERROR: 未找到标题含 '{TARGET_TITLE}' 的窗口 (请确认 WorkBuddy 正在运行)")
    sys.exit(3)

# 几何信息(窗口矩形/客户区/DPI/点击坐标)在下面 recompute_geometry() 中统一计算。
# 关键修复: 若脚本启动时窗口处于最小化(rect=-32000), 必须在 restore 之后**重新**算坐标,
# 否则头像/加油站/领取坐标会落在 -32000 幽灵位置, 点击全部打空。
wr = RECT(); cr = RECT(); o = POINT()
winW = cliW = winH = cliH = 0
scaleX = scaleY = 1.0

# ===================== 读取校准文件（若存在则覆盖默认坐标） =====================
# 移植给别人最易踩的坑: 直接 -run 会用下面这组【作者屏幕的示例默认坐标】,
# 头像在左下角位置稳还能蒙对, 但加油站/领取位置因布局不同而打空 -> 表现为"只点头像"。
# 解决办法: 先 -calibrate 交互记录, 存成本文件, 之后 -run 自动读取覆盖。
_calibrated = False
_CAL_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibrate.json")
if os.path.exists(_CAL_JSON):
    try:
        _d = json.load(open(_CAL_JSON, encoding="utf-8"))
        if isinstance(_d, dict):
            if "AVATAR" in _d:
                AVATAR_LEFT, AVATAR_BOTTOM = _d["AVATAR"]["left"], _d["AVATAR"]["bottom"]
            if "GAS" in _d:
                GAS_LEFT, GAS_BOTTOM = _d["GAS"]["left"], _d["GAS"]["bottom"]
            if "CLAIM" in _d:
                CLAIM_LEFT, CLAIM_BOTTOM = _d["CLAIM"]["left"], _d["CLAIM"]["bottom"]
            _calibrated = True
            print("[校准] 已读取 calibrate.json, 覆盖默认坐标")
    except Exception as e:
        print(f"[校准] 读取 calibrate.json 失败: {e} (使用默认示例坐标)")

def conv_bl(x_left, y_bottom):
    """相对客户区左下角 (x=距左, y=距底, 逻辑像素) -> 屏幕物理坐标。
       窗口任意缩放都命中: x 只跟左边缘有关, y 只跟底边缘有关。"""
    vx = x_left
    vy = cliH - y_bottom           # 距底 -> 距顶(客户区逻辑坐标)
    return int(o.x + vx * scaleX), int(o.y + vy * scaleY)

def recompute_geometry():
    """重新读取窗口几何并重算所有点击坐标。必须在窗口被 restore 之后调用,
       否则最小化状态下 rect=-32000 会让坐标算飞。

       2026-08-04 关键修复: 原点 o 不再用 ClientToScreen!
       实测: 点击头像弹出菜单后 ClientToScreen 返回 2x 错误值
       (wr=(619,169,1500x1000) 正常, 但 o=(1238,338)), 导致全部坐标翻倍打空。
       WorkBuddy 是无边框窗口(Chrome_WidgetWin_1), 客户区 = 整个窗口,
       客户区原点 = 窗口左上角 = GetWindowRect 的 left/top, 稳定可靠。
       窗口被移去哪坐标就跟随到哪, 天然免疫"窗口不在前台/被移动"。

       2026-08-06 防御: 幽灵矩形(-32000) = 窗口处于最小化/恢复动画中。
       实测: 点完 Buddy 加油站后窗口短暂进入最小化态, GetWindowRect 返回
       (-32000,-32000,160x28), 直接用它算坐标会把立即领取点打到屏幕外
       (-31911,-32084)。这里检测到幽灵矩形就自动恢复窗口并重读一次,
       仍异常则保留上次有效几何(不更新全局), 保证后续点击坐标不飞。"""
    global wr, cr, o, winW, winH, cliW, cliH, scaleX, scaleY, sa, sg, sc
    user32.GetWindowRect(_target, ctypes.byref(wr))
    if wr.left < -10000 or wr.right <= wr.left or wr.bottom <= wr.top:
        # 幽灵矩形: 尝试恢复窗口(最小化->正常), 再重读一次
        if user32.IsIconic(_target):
            user32.ShowWindow(_target, SW_RESTORE)
            time.sleep(0.4)
        user32.GetWindowRect(_target, ctypes.byref(wr))
        if wr.left < -10000 or wr.right <= wr.left or wr.bottom <= wr.top:
            # 窗口仍异常(可能是恢复动画中), 保留上次有效坐标, 本次不更新
            return
    user32.GetClientRect(_target, ctypes.byref(cr))
    o.x = wr.left
    o.y = wr.top
    winW = wr.right - wr.left; winH = wr.bottom - wr.top
    cliW = cr.right - cr.left; cliH = cr.bottom - cr.top
    scaleX = winW / cliW if cliW else 1.0
    scaleY = winH / cliH if cliH else 1.0
    sa = conv_bl(AVATAR_LEFT, AVATAR_BOTTOM)    # 头像/账户菜单
    sg = conv_bl(GAS_LEFT, GAS_BOTTOM)          # Buddy 加油站
    sc = conv_bl(CLAIM_LEFT, CLAIM_BOTTOM)      # 立即领取按钮
    if os.environ.get("WB_DEBUG"):
        print(f"[DBG-recompute] wr=({wr.left},{wr.top},{winW}x{winH}) o=({o.x},{o.y}) "
              f"sa={sa} sg={sg} sc={sc}", flush=True)

recompute_geometry()   # 初始计算(若此刻窗口已最小化, do_checkin 的 focus() 会再算一次)

def _print_coords():
    print("== WorkBuddy 窗口信息 ==")
    print(f"  窗口矩形: L={wr.left} T={wr.top}  {winW}x{winH}")
    print(f"  客户区:   {cliW}x{cliH}  (逻辑像素)")
    print(f"  DPI缩放:  X={scaleX:.2f} Y={scaleY:.2f}")
    print(f"  客户区左上角屏幕坐标: ({o.x}, {o.y})")
    print("== 点击坐标 (相对客户区左下角: x=距左, y=距底; 窗口缩放自适应) ==")
    print(f"  头像(账户菜单): {sa}   [距左{AVATAR_LEFT}, 距底{AVATAR_BOTTOM}]")
    print(f"  Buddy加油站:    {sg}   [距左{GAS_LEFT}, 距底{GAS_BOTTOM}]")
    print(f"  立即领取按钮:   {sc}   [距左{CLAIM_LEFT}, 距底{CLAIM_BOTTOM}]")
    print()

# ===================== 鼠标点击（纯 ctypes，可靠） =====================
# 2026-08-12: 点击前 SetCursorPos 后停顿 0.12s -> 0.4s。
# 原因: 老板反馈"脚本控制鼠标时我正在用电脑, 移动不到正确位置"——
# 强制移动(SetCursorPos)本身没问题, 问题是与老板实时操作打架。
# 解决方案: ① do_checkin 开头 wait_mouse_idle() 等老板停手再接管(不抢);
#           ② SetCursorPos 的移动本身就是"小虾接管"的视觉预告, 多停 0.4s
#              给老板看到鼠标飞过去、松手确认。
def click_at(sx, sy, name):
    print(f">> 点击 {name} @ 屏幕 ({sx}, {sy})")
    user32.SetCursorPos(sx, sy)
    time.sleep(0.4)
    user32.mouse_event(0x0002, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
    time.sleep(0.05)
    user32.mouse_event(0x0004, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
    time.sleep(0.3)

# ===================== 鼠标空闲检测（2026-08-12 防"撞老板操作"） =====================
# 老板在用电脑(鼠标在动)时, 脚本安静等待, 绝不抢鼠标、不打断老板;
# 等鼠标连续静止 IDLE_SETTLE 秒才接管。老板不在电脑前时鼠标静止,
# 首次采样后约 IDLE_SETTLE 秒即通过, 与以前一样快。
# GetCursorPos 是纯读取, 不影响鼠标, 不打扰老板。
IDLE_SETTLE  = 2.0    # 鼠标连续静止多少秒才算"空闲"
IDLE_TIMEOUT = 60.0   # 最多等多久(秒); 超时继续执行, 不阻塞定时任务

def wait_mouse_idle():
    """等待鼠标空闲后返回。返回 True=检测到空闲; False=超时(仍继续执行)。"""
    p1 = POINT(); user32.GetCursorPos(ctypes.byref(p1))
    start = time.time(); idle_since = time.time()
    print(f"[接管] 等待鼠标空闲(连续静止{IDLE_SETTLE:.0f}s才接管, 最多等{IDLE_TIMEOUT:.0f}s)...")
    while time.time() - start < IDLE_TIMEOUT:
        time.sleep(0.3)
        p2 = POINT(); user32.GetCursorPos(ctypes.byref(p2))
        if p2.x == p1.x and p2.y == p1.y:
            if time.time() - idle_since >= IDLE_SETTLE:
                print(f"[接管] 鼠标已静止 {IDLE_SETTLE:.0f}s → 开始接管(鼠标将自动移动, 注意!)")
                return True
        else:
            idle_since = time.time()
        p1 = p2
    print(f"[接管] 等待超时({IDLE_TIMEOUT:.0f}s), 继续执行(不阻塞)")
    return False

# ===================== 接管预告（2026-08-12 老板建议） =====================
# 老板反馈: "在点头像之前多一段移动鼠标的冗余, 让我知道你在操作;
#            或者你可以先执行两次移动到头像位置"。
# 实现: announce_move() 在真正点击前把鼠标做两次可见的往返移动
#       (目标点 -> 屏幕右上角空白处 -> 目标点), 让老板看到鼠标"自己动",
#       明确知道小虾要接管了, 提前松手/移开视线, 避免与老板实时操作打架。
def announce_move(target, name):
    """接管预告: 鼠标先飞向 target, 再移开(屏幕右上角), 再飞回 target。
       形成两次明显的可见位移, 提示老板"小虾要开始操作了"。
       target: 屏幕坐标 (sx, sy)。移动过程中不点击, 纯预告。"""
    sw = user32.GetSystemMetrics(0)   # 屏幕宽
    sh = user32.GetSystemMetrics(1)   # 屏幕高
    corner = (sw - 40, 40)            # 屏幕右上角空白区(避开任务栏/开始菜单)
    print(f"[预告] 接管提示: 鼠标 {name}@({target[0]},{target[1]}) → 右上角{corner} → 回到{name}")
    user32.SetCursorPos(target[0], target[1]); time.sleep(0.5)
    user32.SetCursorPos(corner[0], corner[1]); time.sleep(0.5)
    user32.SetCursorPos(target[0], target[1]); time.sleep(0.5)

# ===================== PNG 解码（stdlib，用于校验，支持所有 filter） =====================
def load_png(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos = 8; w = h = color_type = 0; idat = b""
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos+4])[0]
        typ = data[pos+4:pos+8]
        chunk = data[pos+8:pos+8+ln]
        if typ == b"IHDR":
            w, h, _, color_type = struct.unpack(">IIBB", chunk[:10])
        elif typ == b"IDAT":
            idat += chunk
        elif typ == b"IEND":
            break
        pos += 12 + ln
    raw = zlib.decompress(idat)
    ch = 4 if color_type == 6 else 3
    stride = w * ch
    out = bytearray(w * h * ch)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p+stride]); p += stride
        if f == 1:
            for i in range(ch, stride):
                line[i] = (line[i] + line[i-ch]) & 0xff
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xff
        elif f == 3:
            for i in range(stride):
                a = line[i-ch] if i >= ch else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xff
        elif f == 4:
            for i in range(stride):
                a = line[i-ch] if i >= ch else 0
                b = prev[i]; c = prev[i-ch] if i >= ch else 0
                pp = a + b - c
                pa = abs(pp-a); pb = abs(pp-b); pc = abs(pp-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xff
        out[y*stride:(y+1)*stride] = line
        prev = line
    return w, h, ch, out

# ===================== PNG 编码（stdlib，用于 PrintWindow 回退截图） =====================
def save_png(path, w, h, rgba):
    """rgba: 长度 w*h*4 的 bytes, top-down RGBA。"""
    raw = bytearray()
    stride = w * 4
    for y in range(h):
        raw.append(0)  # filter type 0 (None)
        raw += rgba[y*stride:(y+1)*stride]
    comp = zlib.compress(bytes(raw), 9)
    def chunk(typ, cdata):
        c = typ + cdata
        return struct.pack(">I", len(cdata)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)  # 8-bit, color type 6 (RGBA)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", comp))
        f.write(chunk(b"IEND", b""))

# ===================== 截图：优先 desktop-control，回退 PrintWindow =====================
def _find_desktop_control_ps1():
    cand = os.path.join(os.path.expanduser("~"), ".workbuddy", "skills",
                        "desktop-control-win", "scripts", "screen-info.ps1")
    return cand if os.path.exists(cand) else None

def _screenshot_pw(hwnd, out_path):
    """PrintWindow 抓客户区 -> PNG。成功返回 True。"""
    rc = RECT(); user32.GetClientRect(hwnd, ctypes.byref(rc))
    w = rc.right - rc.left; h = rc.bottom - rc.top
    if w <= 0 or h <= 0:
        return False
    hwnd_dc = user32.GetWindowDC(hwnd)
    mem_dc = gdi32.CreateCompatibleDC(hwnd_dc)
    bmp = gdi32.CreateCompatibleBitmap(hwnd_dc, w, h)
    gdi32.SelectObject(mem_dc, bmp)
    ok = user32.PrintWindow(hwnd, mem_dc, PW_CLIENTONLY)
    if not ok:
        gdi32.DeleteObject(bmp); gdi32.DeleteDC(mem_dc); user32.ReleaseDC(hwnd, hwnd_dc)
        return False
    buf = ctypes.create_string_buffer(w * h * 4)
    bmi = BITMAPINFOHEADER()
    bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.biWidth = w
    bmi.biHeight = -h          # 负 = top-down 输出, 省去翻转
    bmi.biPlanes = 1
    bmi.biBitCount = 32
    bmi.biCompression = 0
    got = gdi32.GetDIBits(mem_dc, bmp, 0, h, ctypes.cast(buf, ctypes.c_void_p),
                          ctypes.byref(bmi), 0)
    gdi32.DeleteObject(bmp); gdi32.DeleteDC(mem_dc); user32.ReleaseDC(hwnd, hwnd_dc)
    if not got:
        return False
    # BGRA -> RGBA
    rgba = bytearray(w * h * 4)
    for i in range(w * h):
        b = buf[i*4]; g = buf[i*4+1]; r = buf[i*4+2]; a = buf[i*4+3]
        rgba[i*4] = r; rgba[i*4+1] = g; rgba[i*4+2] = b; rgba[i*4+3] = a
    save_png(out_path, w, h, bytes(rgba))
    return os.path.exists(out_path)

def take_screenshot(hwnd, out_path):
    """截图窗口客户区到 out_path。优先 desktop-control, 否则 PrintWindow。"""
    ps = _find_desktop_control_ps1()
    if ps:
        try:
            env = dict(os.environ)
            env.pop("ACC_PRODUCT_CONFIG_V3", None)  # 防超大环境块撑爆 PowerShell Add-Type
            r = subprocess.run(
                ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps,
                 "-Action", "screenshot", "-Target", TARGET_TITLE, "-OutputPath", out_path],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                env=env, timeout=60)
            if r.returncode == 0 and os.path.exists(out_path):
                return True
        except Exception:
            pass
    return _screenshot_pw(hwnd, out_path)

# ===================== 更新提示检测与处理（2026-08-17） =====================
# 老板反馈: "有时候签到不成功, WorkBuddy 有更新提示遮住了头像"。
# 实测横幅形态(见 checkin_after_ctrlw.png, 老板确认):
#   - 横跨客户区**底部**的白色条带(约 8% 客户区高度)
#   - 内容: 左侧升级图标 + 文案"新版本就绪"
#           + **绿色按钮「重启升级」** (teal 色, 实测 avgRGB=(95,208,169))
#           + 白色按钮「更新日志」(与白色横幅同色, 靠边框区分, 不点它)
#           + 右侧 × 关闭
#   - 头像在左下角被横幅遮住, 点头像无效 -> 签到失败
# 方案: 点头像之前先截图, 在客户区**底部 85%~100%** 区域扫描 teal 色像素
#       (G 分量显著高于 R, 整体中等亮度 = 品牌青绿按钮),
#       检测到即点击完成"点击更新(重启升级)", 然后等待横幅消失/应用重启。
# 颜色特征(teal): g >= 150, g - r >= 40, b >= 90, r <= 180。
#   实测 avgRGB=(95,208,169): g-r=113, 命中; 普通灰色 UI(g-r≈0) 天然不命中。
# 风险与缓解:
#   - 误判: 底部若有其它 teal 元素。缓解: g-r>=40 苛刻阈值 + 最大簇限制 +
#     簇尺寸阈值(>= 80 采样点, step=2)。
#   - 点「重启升级」后应用重启: 旧窗口句柄失效, 轮询等新窗口出现并重新绑定。
def detect_update_overlay(path):
    """检测 WorkBuddy 底部更新横幅, 返回「重启升级」绿色按钮屏幕坐标 (sx, sy, size) 或 None。
       横幅特征: 客户区底部 85%~100% 区域有 teal 色大按钮簇(品牌青绿)。"""
    try:
        w, h, ch, buf = load_png(path)
    except Exception:
        return None
    if w < 200 or h < 200:
        return None
    # 底部 85%~100% 区域 (横幅条带)
    y0 = int(h * 0.85)
    # 扫描 teal 色像素: G 高, R 低, B 中 (品牌青绿按钮)
    cands = []
    for y in range(y0, h, 2):
        for x in range(0, w, 2):
            i = (y * w + x) * ch
            r, g, b = buf[i], buf[i+1], buf[i+2]
            if g >= 150 and g - r >= 40 and b >= 90 and r <= 180:
                cands.append((x, y))
    if len(cands) < 100:
        return None
    # 60px 桶找最大簇
    bucket = {}
    for x, y in cands:
        key = (x // 60, y // 60)
        bucket.setdefault(key, []).append((x, y))
    best_key = max(bucket, key=lambda k: len(bucket[k]))
    pts = bucket[best_key]
    if len(pts) < 80:    # 太小视为误判
        return None
    ix = int(sum(p[0] for p in pts) / len(pts))
    iy = int(sum(p[1] for p in pts) / len(pts))
    sx, sy = img_to_screen(ix, iy, w, h)
    return (sx, sy, len(pts))

def _enum_workbuddy_hwnd():
    """重新枚举找 WorkBuddy 主窗口(精确匹配优先), 返回 hwnd 或 None。
       不修改全局 _target, 供 wait_for_new_window 等场景安全调用。"""
    found_exact = [None]
    found_substr = [None]
    def cb(hwnd, lp):
        if not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value.strip()
        if title == TARGET_TITLE:
            found_exact[0] = hwnd
            return False
        if TARGET_TITLE in title and found_substr[0] is None:
            found_substr[0] = hwnd
        return True
    EnumWindowsProc = ctypes.WINFUNCTYPE(BOOL, HWND, ctypes.c_void_p)
    user32.EnumWindows(EnumWindowsProc(cb), 0)
    return found_exact[0] or found_substr[0] or user32.FindWindowW(None, TARGET_TITLE)

def wait_for_new_window(old_hwnd, timeout=120):
    """轮询等待新的 WorkBuddy 窗口出现(应用重启后句柄变化), 返回新 hwnd 或 None。
       不会复用 old_hwnd; 只有新出现的 hwnd 才返回。"""
    start = time.time()
    while time.time() - start < timeout:
        nt = _enum_workbuddy_hwnd()
        if nt and nt != old_hwnd and user32.IsWindow(nt):
            return nt
        time.sleep(2)
    return None

def handle_update_overlay(pre_path, timeout=180):
    """检测并处理更新弹窗(完成"点击更新")。
       流程: 截图 -> detect_update_overlay -> 若有按钮, announce+click ->
             轮询: 窗口重启? 弹窗消失?  -> 返回结果。
       返回: 'done'(弹窗消失) | 'restarted'(应用重启完成, 新窗口已绑) | 
             'timeout'(超时) | 'not_found'(未检测到更新弹窗) | 'still'(点击后弹窗仍在, 但超时)"""
    btn = detect_update_overlay(pre_path)
    if not btn:
        return 'not_found'
    sx, sy, size = btn
    print(f"== 检测到可能的更新弹窗(中央彩色按钮 @{sx},{sy}, 簇大小 {size}), 点击[更新] ==")
    print("   (若实际不是更新弹窗而是主界面元素, 误点通常无害, 但会消耗一次) ")
    # 复用防撞约定: 预告 + 0.4s 停顿
    announce_move((sx, sy), "更新按钮")
    click_at(sx, sy, "更新按钮")
    # 轮询: 弹窗是否消失 或 窗口是否重启
    overlay_chk = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkin_overlay_chk.png")
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(3)
        # 检查旧窗口是否还在
        if not user32.IsWindow(_target):
            # 旧窗口销毁 -> 应用重启中, 等新窗口
            print("   (旧窗口句柄失效, 等待新窗口出现...)")
            new = wait_for_new_window(_target, timeout=60)
            if new:
                return 'restarted'   # 注意: _target 暂未更新, 由调用方在重启流程后统一 rebind
            continue
        # 旧窗口还在, 截图检查弹窗是否消失
        if take_screenshot(_target, overlay_chk):
            if not detect_update_overlay(overlay_chk):
                return 'done'
    return 'timeout'

# ===================== 领取结果验证（定点采样，主题无关） =====================
# 领取位置只有两种终态:
#   - 未领取: 仍是黑底白字[立即领取]按钮 -> 按钮内大量**近黑像素**(r,g,b<70)
#   - 已领取: 变成灰底[今日已领]按钮      -> 近黑像素≈0, 但灰填充像素多(95~220 的灰)
# 用"近黑像素数"区分(灰按钮也有白字, 不能用白字数判定)。
# 屏幕->图像坐标按客户区原点 o + 客户区尺寸 cliW/cliH 换算, 自适应 DPI。
def verify_claimed(path, sx, sy, radius=22):
    """返回 'claimed' | 'unclaimed' | 'unknown'"""
    w, h, ch, buf = load_png(path)
    cw = cliW if cliW else w
    chh = cliH if cliH else h
    ix = int((sx - o.x) * w / cw)
    iy = int((sy - o.y) * h / chh)
    dark = gray = 0
    for dy in range(-radius, radius + 1, 2):
        for dx in range(-radius, radius + 1, 2):
            x, y = ix + dx, iy + dy
            if 0 <= x < w and 0 <= y < h:
                i = (y * w + x) * ch
                r, g, b = buf[i], buf[i+1], buf[i+2]
                if r < 70 and g < 70 and b < 70:
                    dark += 1
                elif abs(r-g) < 28 and abs(g-b) < 28 and 95 <= r <= 220:
                    gray += 1
    if dark >= 30:
        return "unclaimed"   # 黑按钮还在 -> 没领上
    if gray >= 60:
        return "claimed"     # 灰按钮 -> 已领
    return "unknown"         # 既不是黑也不是灰 -> 面板可能没正常打开

def find_dark_button(path, step=4):
    """扫描整图, 动态定位黑底白字按钮(近黑像素最密集的簇中心)。
       返回图像坐标 (ix, iy) 或 None。用于不依赖 CLAIM 校准值、动态点[立即领取]。
       - 近黑判定: r,g,b < 70 (黑底按钮)
       - 网格聚类: 60px 桶找最密簇, 取簇内平均坐标
       - 过少黑像素(<40)视为没找到"""
    w, h, ch, buf = load_png(path)
    pts = []
    for y in range(0, h, step):
        for x in range(0, w, step):
            i = (y * w + x) * ch
            r, g, b = buf[i], buf[i+1], buf[i+2]
            if r < 70 and g < 70 and b < 70:
                pts.append((x, y))
    if len(pts) < 40:
        return None
    # 60px 网格分桶, 找黑像素最密集的桶
    bucket = {}
    for x, y in pts:
        key = (x // 60, y // 60)
        bucket.setdefault(key, []).append((x, y))
    best_key = max(bucket, key=lambda k: len(bucket[k]))
    bpts = bucket[best_key]
    return int(sum(p[0] for p in bpts) / len(bpts)), int(sum(p[1] for p in bpts) / len(bpts))

def img_to_screen(ix, iy, img_w, img_h):
    """图像坐标(客户区截图物理像素) -> 屏幕坐标。与 verify_claimed 的换算互逆:
       verify_claimed: ix = (sx - o.x) * w / cw  =>  sx = o.x + ix * cw / w"""
    cw = cliW if cliW else img_w
    chh = cliH if cliH else img_h
    return int(o.x + ix * cw / img_w), int(o.y + iy * chh / img_h)

# ===================== 窗口钉死（彻底消除"自动移位导致坐标漂移"） =====================
def _is_maximized(hwnd):
    """检查窗口是否处于最大化状态（IsIconic 只检测最小化，不检测最大化）。"""
    wp = ctypes.Structure
    class WINDOWPLACEMENT(ctypes.Structure):
        _fields_ = [("length", UINT), ("flags", UINT),
                    ("showCmd", UINT),
                    ("ptMinPosition", POINT), ("ptMaxPosition", POINT),
                    ("rcNormalPosition", RECT)]
    user32.GetWindowPlacement.argtypes = [HWND, ctypes.POINTER(WINDOWPLACEMENT)]
    user32.GetWindowPlacement.restype = BOOL
    pl = WINDOWPLACEMENT()
    pl.length = ctypes.sizeof(WINDOWPLACEMENT)
    if user32.GetWindowPlacement(hwnd, ctypes.byref(pl)):
        return pl.showCmd == 3  # SW_MAXIMIZE = 3
    return False

def force_pos(hwnd, x=200, y=150, w=1500, h=1000):
    """把目标窗口钉死到固定屏幕位置与尺寸, 使相对坐标完全确定、可复现。

    关键坑: WorkBuddy 在 SetForegroundWindow 时会自动挪动/改自己窗口,
    导致'打印坐标'与'实际点击坐标'漂移、点击打空(实测曾出现打印(690,1203)
    却点到(1254,1358))。把窗口钉到固定位置后, 所有相对坐标稳定映射, 不再漂移。
    校准值 AVATAR(38,30)/GAS(144,556)/CLAIM(89,112) 均在此布局下实测。

    重要: 若窗口处于最大化状态, 必须先 ShowWindow(SW_RESTORE) 恢复正常尺寸,
    否则 SetWindowPos 无法改变最大化窗口的位置和大小(会被系统拒绝)。"""
    if _is_maximized(hwnd):
        user32.ShowWindow(hwnd, SW_RESTORE)
        time.sleep(0.4)
    user32.SetWindowPos(hwnd, HWND_TOP, x, y, w, h, 0)
    time.sleep(0.4)

# ===================== 窗口置前（可靠三步） =====================
def focus():
    """可靠把目标窗口置前(最小化先恢复, 线程绑定绕过前台锁, z序置顶)。
       原实现漏了 argtypes 声明导致 HWND 截断、SetForegroundWindow 静默失败,
       是"窗口没在最上方"导致点击打空的真凶。"""
    hwnd = _target
    # 先确保窗口脱离最小化/幽灵状态(-32000 是 Windows 最小化窗口的哨兵坐标):
    # restore 后验证 GetWindowRect, 若仍幽灵则重试(最多3次), 防 WorkBuddy 恢复慢/失败。
    for _ in range(3):
        if user32.IsIconic(hwnd):
            user32.ShowWindow(hwnd, SW_RESTORE)
            time.sleep(0.3)
        rc = RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rc))
        if rc.left > -10000 and rc.right > rc.left and rc.bottom > rc.top:
            break
        user32.ShowWindow(hwnd, 5)   # SW_SHOW 兜底
        time.sleep(0.4)
    fg = user32.GetForegroundWindow()
    if fg and fg != hwnd:
        fg_tid = user32.GetWindowThreadProcessId(fg, None)
        my_tid = kernel32.GetCurrentThreadId()
        if fg_tid and fg_tid != my_tid:
            user32.AttachThreadInput(fg_tid, my_tid, True)
        user32.SetForegroundWindow(hwnd)
        if fg_tid and fg_tid != my_tid:
            user32.AttachThreadInput(fg_tid, my_tid, False)
    else:
        user32.SetForegroundWindow(hwnd)
    # 注意: 不再调用 force_pos。WorkBuddy 会主动把 SetWindowPos 设的 (200,150) 1500x1000
    # 改回原尺寸 1481x1005 并移到 (831,411) 之类——实测导致点击全部打空、面板根本没开、
    # verify_claimed 又在主界面灰背景上误判 claimed(假阳性)。改为让 WorkBuddy 自己
    # 把窗口恢复到自然位置(631,261)1481x1005, calibrate 相对坐标自适应不变。
    time.sleep(0.5)
    recompute_geometry()   # 关键: 窗口可能刚从最小化恢复, rect 已从 -32000 变正常, 重算坐标

# ===================== 运行前自检 =====================
def _preflight():
    """返回告警列表(空=无告警)。重点防止'用默认坐标直接跑'导致只点头像。"""
    warns = []
    if not _calibrated:
        warns.append("未检测到 calibrate.json, 当前用的是脚本内置【示例默认坐标】(作者屏幕校准值)。"
                     "若你的屏幕/布局不同, 点击基本会打空 —— 这正是最常见'只点头像'的原因!"
                     "请先运行 `python wb_mouse_checkin.py -calibrate` 交互校准一次。")
    for nm, (x, y) in [("头像", sa), ("加油站", sg), ("领取", sc)]:
        if not (o.x <= x <= o.x + winW and o.y <= y <= o.y + winH):
            warns.append(f"{nm} 计算坐标 ({x},{y}) 落在 WorkBuddy 窗口之外, 坐标严重偏移, 请重新校准。")
    return warns

# ===================== 主流程 =====================
# 2026-08-17 重构(老板需求): 签到失败 -> 检查是否有更新横幅 -> 有则点[重启升级] ->
#   应用重启后**继续执行签到**(最多 3 轮); 实在等不到重启则写续签标记 + 退出码 4,
#   由外部(定时任务会话)在更新完成后接管续签。
MAX_CHECKIN_ATTEMPTS = 3
STATE_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkin_state.json")

def mark_pending(reason):
    """写续签标记(应用更新重启中, 需在重启完成后继续签到)。"""
    try:
        with open(STATE_JSON, "w", encoding="utf-8") as f:
            json.dump({"pending": True, "reason": reason,
                       "ts": time.strftime("%Y-%m-%d %H:%M:%S")},
                      f, ensure_ascii=False, indent=2)
        print(f"== 已写续签标记: {STATE_JSON} (reason={reason})")
    except Exception as e:
        print(f"== 写续签标记失败: {e}")

def clear_pending_state():
    """签到成功后清除续签标记。"""
    try:
        if os.path.exists(STATE_JSON):
            os.remove(STATE_JSON)
            print("== 已清除续签标记(签到成功)")
    except Exception:
        pass

# ===================== 续签载体: Windows 计划任务（2026-08-17 关键修复） =====================
# WorkBuddy 重启会杀掉运行在它进程内的 agent 会话(包括"等几分钟重跑"的定时逻辑),
# 所以续签不能依赖会话, 必须用独立于 WorkBuddy 的 Windows 计划任务:
#   点[重启升级]前 schedule_resume_task() 注册 8 分钟后的 -resume 计划任务
#   -> WorkBuddy 重启不影响计划任务 -> 到点独立 python 进程唤醒
#   -> do_resume() 检查 checkin_state.json(pending?) -> 等 WorkBuddy 窗口出现
#   -> attempt_checkin() 补签 -> 成功: 清标记 + cancel_resume_task()
def schedule_resume_task():
    """注册 Windows 计划任务: RESUME_DELAY_SEC 秒后运行本脚本 -resume 模式。
       返回 True/False。计划任务独立于 WorkBuddy 进程, 是续签的可靠载体。"""
    try:
        py = sys.executable
        script = os.path.abspath(__file__)
        st = time.strftime("%H:%M", time.localtime(time.time() + RESUME_DELAY_SEC))
        r = subprocess.run(
            ["schtasks", "/create", "/tn", RESUME_TASK_NAME,
             "/tr", f'"{py}" "{script}" -resume',
             "/sc", "once", "/st", st, "/f"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        if r.returncode == 0:
            print(f"== 已注册续签计划任务 [{RESUME_TASK_NAME}] {st} 执行: -resume (独立于 WorkBuddy 进程)")
            return True
        print(f"== 注册续签计划任务失败: {r.stderr.strip() or r.stdout.strip()}")
        return False
    except Exception as e:
        print(f"== 注册续签计划任务异常: {e}")
        return False

def cancel_resume_task():
    """删除续签计划任务(续签完成/不需要时清理, 防止残留)。"""
    try:
        subprocess.run(["schtasks", "/delete", "/tn", RESUME_TASK_NAME, "/f"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        print(f"== 已删除续签计划任务 [{RESUME_TASK_NAME}]")
    except Exception:
        pass

def do_resume():
    """-resume 模式: 更新重启后的续签入口(由 Windows 计划任务独立唤醒)。
       流程: 读 checkin_state.json -> 非 pending 直接结束(无需续签) ->
             等 WorkBuddy 窗口出现(最长 RESUME_WAIT_WIN 秒) -> attempt_checkin 补签 ->
             成功: 清标记 + 删计划任务, 退出 0; 失败: 保留标记, 退出 2。"""
    global _target
    print("== [resume] 续签模式启动(Windows 计划任务独立唤醒) ==")
    # 1) 检查是否真的需要续签
    need = False
    try:
        if os.path.exists(STATE_JSON):
            with open(STATE_JSON, encoding="utf-8") as f:
                need = bool(json.load(f).get("pending"))
    except Exception:
        pass
    if not need:
        print("== [resume] 无续签标记(pending=false 或文件不存在), 无需补签, 结束 ==")
        cancel_resume_task()
        return 0
    print(f"== [resume] 检测到续签标记, 等待 WorkBuddy 窗口出现(最长 {RESUME_WAIT_WIN}s)... ==")
    # 2) 等 WorkBuddy 更新重启完成(窗口重新出现)
    deadline = time.time() + RESUME_WAIT_WIN
    while time.time() < deadline:
        hwnd = _enum_workbuddy_hwnd()
        if hwnd and user32.IsWindow(hwnd):
            _target = hwnd
            print(f"== [resume] WorkBuddy 窗口已出现 hwnd={hwnd}, 开始补签 ==")
            break
        time.sleep(3)
    else:
        print(f"== [resume] {RESUME_WAIT_WIN}s 内未等到 WorkBuddy 窗口, 补签失败(保留标记) ==")
        return 2
    # 3) 补签(单轮即可; 若又遇到更新横幅, attempt_checkin 内部会再点更新,
    #    此时不重复注册计划任务——由本进程继续等/续签, 避免任务堆积)
    st = attempt_checkin()
    if st == "success":
        clear_pending_state()
        cancel_resume_task()
        print("== [resume] 续签成功, 已清除标记并删除计划任务 ==")
        return 0
    print("== [resume] 续签失败(见上方日志), 保留续签标记 ==")
    return 2

def attempt_checkin():
    """单轮完整签到。返回 'success' | 'failed'。
       流程: wait_mouse_idle -> focus -> 前置横幅检测(有则处理) ->
       头像 -> Buddy加油站 -> 中段校验(面板打开?) -> 立即领取 -> 终态校验(灰底今日已领?)。"""
    global _target
    RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), RESULT_NAME)
    MID = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkin_mid.png")
    PRE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkin_pre.png")

    wait_mouse_idle()  # 2026-08-12: 老板在用电脑时安静等待, 不抢鼠标; 空闲后才接管
    focus()   # 解决"窗口不在前台": 最小化先恢复 + SetForegroundWindow 可靠置前
    time.sleep(0.3); recompute_geometry()

    # ===== 2026-08-17: 前置更新横幅检测与处理 =====
    # 更新横幅(底部白色条带 + 绿色[重启升级]按钮)会遮住左下角头像, 点头像点到横幅上。
    # 点头像前先截图, 检测到绿色按钮就点击完成更新, 等横幅消失/应用重启后再签到。
    if take_screenshot(_target, PRE):
        ovr = handle_update_overlay(PRE, timeout=120)
        if ovr == 'restarted':
            # 应用已重启, 新窗口出现, 重新绑定并重算坐标 (global 声明, 修复局部变量坑)
            new_hwnd = wait_for_new_window(_target, timeout=60) or _enum_workbuddy_hwnd()
            if new_hwnd and user32.IsWindow(new_hwnd):
                _target = new_hwnd
                print(f"== 已绑定新窗口(更新后重启) hwnd={new_hwnd} ==")
                focus(); time.sleep(0.5); recompute_geometry()
                if take_screenshot(_target, PRE) and detect_update_overlay(PRE):
                    print("== 重启后仍有更新横幅(可能要二次确认), 本轮失败 ==")
                    return "failed"
            else:
                print("== 应用重启后未找到新窗口, 本轮失败 ==")
                return "failed"
        elif ovr == 'done':
            time.sleep(0.5); focus(); time.sleep(0.5); recompute_geometry()
            if take_screenshot(_target, PRE) and detect_update_overlay(PRE):
                print("== 点击后仍检测到更新横幅(可能需更长时间), 本轮失败 ==")
                return "failed"
        elif ovr == 'timeout':
            print("== 前置更新处理超时(120s), 本轮失败 ==")
            return "failed"
        # 'not_found' 正常情况, 继续签到流程
    else:
        print("== 预截图失败, 跳过更新横幅检测, 直接进入签到流程 ==")

    announce_move(sa, "头像/账户菜单")  # 2026-08-12: 点击前两次可见位移, 提示老板"小虾要操作了"
    click_at(*sa, "头像/账户菜单"); time.sleep(0.8)
    recompute_geometry()   # 坐标跟随窗口实际位置(GetWindowRect 原点), 每次点击前刷新
    click_at(*sg, "Buddy 加油站"); time.sleep(1.6)

    # ===== 中段校验: 加油站面板是否真的打开了? =====
    if not take_screenshot(_target, MID):
        print("== 中段截图失败, 无法校验 ==")
        return "failed"
    mid_state = verify_claimed(MID, sc[0], sc[1])
    if mid_state != "unclaimed":
        print(f"== 中段校验: 加油站面板未打开 (verify_claimed={mid_state}, 按钮位置无黑像素) ==")
        print("   → 极可能是 Buddy 加油站菜单项没点中, 面板根本没弹出来。")
        print(f"     请重新校准 GAS_LEFT/GAS_BOTTOM (当前 {GAS_LEFT}/{GAS_BOTTOM}); 也可先 -calibrate 重新记录。")
        print(f"     参考坐标: 头像{sa}  加油站{sg}  领取{sc}")
        try:
            import shutil as _sh; _sh.copy(MID, RESULT)
        except Exception:
            pass
        return "failed"
    print("== 中段校验: 加油站面板已打开 (检测到黑底立即领取按钮), 继续点立即领取 ==")

    recompute_geometry()
    click_at(*sc, "立即领取"); time.sleep(2.0)
    if not take_screenshot(_target, RESULT):
        print("== 截图失败, 无法校验 ==")
        return "failed"
    state = verify_claimed(RESULT, sc[0], sc[1])
    if state == "claimed":
        print("== 校验通过: 领取位置已是灰底[今日已领], 领取成功 ==")
        return "success"
    if state == "unclaimed":
        print("== 校验失败: 领取位置仍是黑底[立即领取], 没点中 ==")
        print(f"   → 面板已打开但[立即领取]按钮没点中, 请重新校准 CLAIM_LEFT/CLAIM_BOTTOM (当前 {CLAIM_LEFT}/{CLAIM_BOTTOM})")
        return "failed"
    print("== 校验异常: 领取位置既无黑按钮也无灰按钮 ==")
    print("   → 多半是【Buddy 加油站】菜单项没点中, 面板根本没打开 (或打开了但不在预期位置)。")
    print(f"     请重点重新校准 GAS_LEFT/GAS_BOTTOM (当前 {GAS_LEFT}/{GAS_BOTTOM}); 也可先 -calibrate 重新记录。")
    print(f"     参考坐标: 头像{sa}  加油站{sg}  领取{sc}")
    return "failed"

def do_checkin():
    """执行签到(含失败兜底)。返回 (status, screenshot_path)
       status: 'success' | 'failed' | 'update_pending'
       - 每轮先签到; 失败则截图检测更新横幅:
         * 有横幅 -> 点[重启升级] -> 写续签标记 -> 等应用重启(最长 180s)
           -> 重启成功: 下一轮继续签到(最多 MAX_CHECKIN_ATTEMPTS 轮)
           -> 重启超时: 返回 'update_pending'(退出码 4), 由外部定时任务续签
         * 无横幅 -> 判定真实失败
       - 签到成功 -> 清除续签标记"""
    global _target
    RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), RESULT_NAME)
    PRE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkin_pre.png")

    for attempt in range(1, MAX_CHECKIN_ATTEMPTS + 1):
        print(f"\n===== 签到尝试 {attempt}/{MAX_CHECKIN_ATTEMPTS} =====")
        st = attempt_checkin()
        if st == "success":
            clear_pending_state()
            return "success", RESULT

        # ===== 失败兜底: 检查是否有更新横幅作祟 =====
        print(f"== 签到失败(第 {attempt} 轮), 检查是否有更新横幅... ==")
        time.sleep(0.6)
        if take_screenshot(_target, PRE):
            btn = detect_update_overlay(PRE)
            if btn:
                sx, sy, size = btn
                print(f"== 检测到更新横幅(绿色[重启升级]按钮 @{sx},{sy}, 簇 {size}), 点击完成更新 ==")
                announce_move((sx, sy), "重启升级")
                click_at(sx, sy, "重启升级")
                mark_pending("update_restart")
                # 2026-08-17 关键: WorkBuddy 重启会杀掉 agent 会话, 续签不能依赖会话。
                # 先注册独立于 WorkBuddy 的 Windows 计划任务(8 分钟后 -resume),
                # 即使本进程/会话随重启终止, 计划任务到点也会独立唤醒补签。
                schedule_resume_task()
                # 本进程若还活着, 顺便等应用重启(最长 180s)直接续签, 不等计划任务
                print("== 等待应用重启完成(最长 180s; 若本进程被杀, 计划任务会接管) ... ==")
                new = wait_for_new_window(_target, timeout=180)
                if new and user32.IsWindow(new):
                    _target = new
                    cancel_resume_task()   # 本进程已接管续签, 撤掉计划任务避免重复
                    print(f"== 应用重启完成, 已绑定新窗口 hwnd={new}, 下一轮继续签到 ==")
                    focus(); time.sleep(0.6); recompute_geometry()
                    continue   # 下一轮续签
                print("== 180s 内未等到新窗口(可能本进程即将被重启终止), 已注册计划任务兜底, 返回 update_pending ==")
                return "update_pending", RESULT
        print("== 无更新横幅, 判定为真实失败 ==")
        return "failed", RESULT

    print(f"== 已达最大尝试次数({MAX_CHECKIN_ATTEMPTS} 轮), 签到失败 ==")
    return "failed", RESULT

def do_sample():
    """即时采样: 把 WorkBuddy 置前, 读取当前鼠标屏幕坐标, 反算成[相对客户区左下角]
       的 left/bottom 并打印 JSON。不交互, 供外部(如微信分步引导)分步调用。"""
    focus()
    p = POINT(); user32.GetCursorPos(ctypes.byref(p))
    if cliW and cliH:
        rel_left = (p.x - o.x) / scaleX
        rel_topc = (p.y - o.y) / scaleY
        rel_bottom = cliH - rel_topc
        print(json.dumps({"screen": [p.x, p.y],
                          "left": round(rel_left, 1), "bottom": round(rel_bottom, 1)},
                         ensure_ascii=False))
        return 0
    print("ERROR: 窗口尺寸为0, 无法换算")
    return 2

def do_calibrate_gui():
    """弹窗校准(通用 GUI, 零依赖): tkinter 悬浮窗显示步骤 + 实时鼠标坐标 + 倒计时,
       每步自动采样鼠标位置, 三步写 calibrate.json。无需终端 / 微信 / 外部通道, 跨用户通用。
       无 GUI 环境(tkinter 缺失)时提示改用 -calibrate 终端文字版。"""
    try:
        import tkinter as tk
    except Exception:
        print("ERROR: 当前 Python 未安装 tkinter (GUI 库), 无法弹窗校准。")
        print("       请改用终端文字校准: python wb_mouse_checkin.py -calibrate")
        return 2
    OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibrate.json")
    steps = [
        ("第 1 步 / 共 3 步", "把鼠标移到左下角【头像】(账户菜单)\n移到后保持不动，倒计时结束自动记录", "AVATAR"),
        ("第 2 步 / 共 3 步", "点击头像展开菜单，把鼠标移到菜单里的【Buddy 加油站】\n移到后保持不动，倒计时结束自动记录", "GAS"),
        ("第 3 步 / 共 3 步", "点击加油站打开积分面板，把鼠标移到【立即领取】按钮\n移到后保持不动，倒计时结束自动记录", "CLAIM"),
    ]
    pts = {}
    focus()  # 先把 WorkBuddy 置前, 方便用户把鼠标移到目标
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.92)
    sw = root.winfo_screenwidth(); sh = root.winfo_screenheight()
    w, h = 384, 172
    root.geometry(f"{w}x{h}+{sw - w - 24}+{24}")   # 右上角, 不挡左下/中部的目标
    bg = "#1f4e79"
    title = tk.Label(root, text="", font=("Microsoft YaHei", 13, "bold"), fg="white", bg=bg)
    title.pack(fill="x", pady=(8, 2))
    hint = tk.Label(root, text="", font=("Microsoft YaHei", 11), fg="#e8eef5", bg=bg,
                    wraplength=344, justify="left")
    hint.pack(fill="x", padx=14, pady=(2, 6))
    cd = tk.Label(root, text="", font=("Microsoft YaHei", 30, "bold"), fg="#ffd966", bg=bg)
    cd.pack(pady=(0, 2))
    coord = tk.Label(root, text="", font=("Consolas", 10), fg="#a9c7e8", bg=bg)
    coord.pack(pady=(0, 8))

    def refresh_coord():
        p = POINT(); user32.GetCursorPos(ctypes.byref(p))
        coord.config(text=f"当前鼠标: ({p.x}, {p.y})")
        root.after(100, refresh_coord)

    def start_step(i):
        if i >= len(steps):
            finish()
            return
        nm, htext, key = steps[i]
        title.config(text=nm)
        hint.config(text=htext)
        cd.config(text="6")
        cnt = {"v": 6}
        def countdown():
            cd.config(text=str(cnt["v"]))
            if cnt["v"] <= 0:
                p = POINT(); user32.GetCursorPos(ctypes.byref(p))
                if cliW and cliH:
                    left = (p.x - o.x) / scaleX
                    bottom = cliH - (p.y - o.y) / scaleY
                    pts[key] = {"left": round(left, 1), "bottom": round(bottom, 1)}
                    print(f"[GUI校准] 记录 {key}: 距左 {pts[key]['left']}, 距底 {pts[key]['bottom']} (屏幕 {p.x},{p.y})")
                root.after(350, lambda: start_step(i + 1))
                return
            cnt["v"] -= 1
            root.after(1000, countdown)
        countdown()

    def finish():
        if pts:
            with open(OUT, "w", encoding="utf-8") as f:
                json.dump(pts, f, ensure_ascii=False, indent=2)
            title.config(text="✅ 校准完成")
            hint.config(text=f"已保存: {os.path.basename(OUT)}\n下次直接 -run 即可")
            cd.config(text="")
            coord.config(text=json.dumps(pts, ensure_ascii=False))
            root.after(2800, root.destroy)
        else:
            root.destroy()

    root.after(300, lambda: start_step(0))
    refresh_coord()
    root.mainloop()
    return 0

def do_calibrate():
    """交互式校准: 引导用户把鼠标移到三个目标点, 按回车记录真实屏幕坐标,
       自动换算成[相对客户区左下角]并保存到 calibrate.json (下次 -run 自动读取)。
       彻底免去'用画图量像素'的误差, 是移植后最稳的校准方式。"""
    OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibrate.json")
    steps = [
        ("AVATAR", "【步骤1】请让 WorkBuddy 在前台、账户菜单处于收起状态。\n         把鼠标移到左下角的【头像】上, 然后切到本终端按回车记录。"),
        ("GAS",    "【步骤2】点击头像展开账户菜单。把鼠标移到菜单里的【Buddy 加油站】项上,\n         切到本终端按回车记录。"),
        ("CLAIM",  "【步骤3】点击【Buddy 加油站】打开积分面板。把鼠标移到面板里的【立即领取】按钮上,\n         切到本终端按回车记录。"),
    ]
    pts = {}
    for key, prompt in steps:
        focus()
        print("\n" + prompt)
        input("         （移动鼠标到目标后，回车记录；Ctrl+C 取消）")
        p = POINT(); user32.GetCursorPos(ctypes.byref(p))
        if cliW and cliH:
            rel_left = (p.x - o.x) / scaleX
            rel_topc = (p.y - o.y) / scaleY
            rel_bottom = cliH - rel_topc
            pts[key] = {"left": round(rel_left, 1), "bottom": round(rel_bottom, 1)}
            print(f"         ✅ 记录 {key}: 距左 {pts[key]['left']}, 距底 {pts[key]['bottom']}  (屏幕 {p.x},{p.y})")
        else:
            print("         ❌ 窗口尺寸为0, 无法换算, 跳过")
    if pts:
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(pts, f, ensure_ascii=False, indent=2)
        print(f"\n== 已保存校准到 {OUT} ==")
        print("   下次直接 `python wb_mouse_checkin.py -run` 即可, 脚本自动读取此文件覆盖默认坐标。")
        try:
            take_screenshot(_target, os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibrate_ref.png"))
            print("   参考截图已存 calibrate_ref.png")
        except Exception:
            pass
        return 0
    print("== 未记录到任何点 ==")
    return 2

# ===================== 入口 =====================
if __name__ == "__main__":
    if "-sample" in sys.argv:
        _print_coords()
        sys.exit(do_sample())

    if "-calibrate-gui" in sys.argv:
        _print_coords()
        sys.exit(do_calibrate_gui())

    if "-calibrate" in sys.argv:
        _print_coords()
        sys.exit(do_calibrate())

    if "-resume" in sys.argv:
        # 2026-08-17: 更新重启后的续签入口, 由 Windows 计划任务独立唤醒
        # (独立 python 进程, 不依赖 WorkBuddy / agent 会话存活)
        code = do_resume()
        sys.exit(code)

    if "-run" not in sys.argv:
        _print_coords()
        for w in _preflight():
            print("⚠️ " + w)
        print("[DryRun] 仅打印坐标, 未点击。加 -run 执行真实签到, -calibrate 交互校准。")
        sys.exit(0)

    _print_coords()
    for w in _preflight():
        print("⚠️ " + w)
    status, shot = do_checkin()
    print(f"\n== 结论: {status.upper()} | 截图: {shot} ==")
    # 退出码: 0=成功  2=失败(无更新横幅/更新后仍失败)  4=更新重启中(待续签, 需外部定时任务接管)
    code = {"success": 0, "failed": 2, "update_pending": 4}.get(status, 2)
    sys.exit(code)
