#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""区域录制 GUI (Region Recorder) - pure ctypes / Win32, no third-party deps.

Flow:
  1. 框选区域  -> click, then drag with the left button to draw the region
  2. 确认选区  -> keep the rectangle (green frame shows what you picked)
  3. 开始录制  -> ffmpeg records exactly that rectangle; a red frame + status bar show up
  4. 结束录制  -> stop, the mp4 is finalized and the path is shown

Options:
  --out DIR    output folder (default: ~/Videos/Screen Recordings)
  --sec N      preset the time limit spin (0 = stop manually)
"""
import argparse
import ctypes
import ctypes.wintypes as wt
import datetime as dt
import pathlib
import subprocess
import sys

# ---------------------------------------------------------------- win32 glue
u32 = ctypes.WinDLL("user32", use_last_error=True)
g32 = ctypes.WinDLL("gdi32", use_last_error=True)
k32 = ctypes.WinDLL("kernel32", use_last_error=True)

_dpi_log = []
_u32i = ctypes.WinDLL("user32")
try:
    _u32i.SetProcessDpiAwarenessContext.argtypes = [ctypes.c_void_p]
    _r = _u32i.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))     # PER_MONITOR_AWARE_V2
    _dpi_log.append("ctx_v2=%s" % _r)
except Exception as _e:
    _r = 0
    _dpi_log.append("ctx_v2 EXC %r" % (_e,))
if not _r:
    try:
        _r = ctypes.WinDLL("shcore").SetProcessDpiAwareness(2)        # PER_MONITOR_DPI_AWARE
        _dpi_log.append("shcore=%s" % (_r & 0xFFFFFFFF))
    except Exception as _e:
        _dpi_log.append("shcore EXC %r" % (_e,))
if not _r:
    try:
        _dpi_log.append("SetProcessDPIAware=%s" % _u32i.SetProcessDPIAware())
    except Exception as _e:
        _dpi_log.append("SetProcessDPIAware EXC %r" % (_e,))

LRESULT = ctypes.c_ssize_t
WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wt.HWND, ctypes.c_uint, ctypes.c_size_t, ctypes.c_ssize_t)

WM_PAINT, WM_DESTROY, WM_CLOSE, WM_COMMAND, WM_TIMER = 0x000F, 0x0002, 0x0010, 0x0111, 0x0113
WM_LBUTTONDOWN, WM_LBUTTONUP, WM_MOUSEMOVE, WM_RBUTTONDOWN = 0x0201, 0x0202, 0x0200, 0x0204
WM_KEYDOWN, WM_ERASEBKGND = 0x0100, 0x0014
WM_SETFONT, WM_GETDLGCODE = 0x0030, 0x0087

WS_OVERLAPPED, WS_CAPTION, WS_SYSMENU, WS_MINIMIZEBOX = 0x00000000, 0x00C00000, 0x00080000, 0x00020000
WS_POPUP, WS_CHILD, WS_VISIBLE, WS_BORDER = 0x80000000, 0x40000000, 0x10000000, 0x00800000
WS_EX_TOPMOST, WS_EX_TOOLWINDOW, WS_EX_LAYERED = 0x00000008, 0x00000080, 0x00080000
BS_PUSHBUTTON, ES_AUTOHSCROLL = 0x00000000, 0x0080
SW_HIDE, SW_SHOW, SW_SHOWNA = 0, 5, 8
HWND_TOP, HWND_TOPMOST, HWND_NOTOPMOST = 0, -1, -2
SWP_NOSIZE, SWP_NOMOVE, SWP_NOACTIVATE, SWP_SHOWWINDOW = 0x0001, 0x0002, 0x0010, 0x0040
DT_LEFT, DT_CENTER, DT_SINGLELINE, DT_VCENTER, DT_NOPREFIX = 0x00000000, 0x00000001, 0x00000020, 0x00000004, 0x00000800
RGN_DIFF = 4
LWA_ALPHA = 0x2
SM_XVIRTUALSCREEN, SM_YVIRTUALSCREEN, SM_CXVIRTUALSCREEN, SM_CYVIRTUALSCREEN = 76, 77, 78, 79
CREATE_NO_WINDOW = 0x08000000
VK_ESCAPE = 0x1B

ID_PICK, ID_CONFIRM, ID_REDRAW, ID_START, ID_STOP = 101, 102, 103, 104, 105

u32.CreateWindowExW.restype = wt.HWND
u32.DefWindowProcW.restype = LRESULT
g32.CreateSolidBrush.restype = ctypes.c_void_p
g32.CreatePen.restype = ctypes.c_void_p
g32.CreateFontW.restype = ctypes.c_void_p
g32.SelectObject.restype = ctypes.c_void_p
k32.GetModuleHandleW.restype = wt.HMODULE
u32.BeginPaint.restype = wt.HDC
u32.SetCapture.restype = wt.HWND
u32.GetDC.restype = wt.HDC

COL_FRAME_READY = 0x0020C040   # BGR -> green
COL_FRAME_REC = 0x00211FEA     # BGR -> red
COL_DIM = 110


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                ("right", ctypes.c_long), ("bottom", ctypes.c_long)]


class PAINTSTRUCT(ctypes.Structure):
    _fields_ = [("hdc", wt.HDC), ("fErase", wt.BOOL), ("rcPaint", RECT),
                ("fRestore", wt.BOOL), ("fIncUpdate", wt.BOOL), ("rgbReserved", ctypes.c_byte * 32)]


class WNDCLASSEXW(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("style", ctypes.c_uint), ("lpfnWndProc", WNDPROC),
                ("cbClsExtra", ctypes.c_int), ("cbWndExtra", ctypes.c_int), ("hInstance", wt.HINSTANCE),
                ("hIcon", wt.HICON), ("hCursor", wt.HANDLE), ("hbrBackground", wt.HBRUSH),
                ("lpszMenuName", wt.LPCWSTR), ("lpszClassName", wt.LPCWSTR), ("hIconSm", wt.HICON)]


class DEVMODEW(ctypes.Structure):
    _fields_ = [("dmDeviceName", ctypes.c_wchar * 32), ("dmSpecVersion", ctypes.c_ushort),
                ("dmDriverVersion", ctypes.c_ushort), ("dmSize", ctypes.c_ushort),
                ("dmDriverExtra", ctypes.c_ushort), ("dmFields", wt.DWORD),
                ("dmOrientation", ctypes.c_short), ("dmPaperSize", ctypes.c_short),
                ("dmPaperLength", ctypes.c_short), ("dmPaperWidth", ctypes.c_short),
                ("dmScale", ctypes.c_short), ("dmCopies", ctypes.c_short),
                ("dmDefaultSource", ctypes.c_short), ("dmPrintQuality", ctypes.c_short),
                ("dmColor", ctypes.c_short), ("dmDuplex", ctypes.c_short),
                ("dmYResolution", ctypes.c_short), ("dmTTOption", ctypes.c_short),
                ("dmCollate", ctypes.c_short), ("dmFormName", ctypes.c_wchar * 32),
                ("dmLogPixels", ctypes.c_ushort), ("dmBitsPerPel", wt.DWORD),
                ("dmPelsWidth", wt.DWORD), ("dmPelsHeight", wt.DWORD),
                ("dmDisplayFlags", wt.DWORD), ("dmDisplayFrequency", wt.DWORD)]


# ---- 64-bit safe signatures (no argtypes => int args get truncated to c_int) ----
u32.CreateWindowExW.argtypes = [wt.DWORD, wt.LPCWSTR, wt.LPCWSTR, wt.DWORD,
                                ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                wt.HWND, wt.HMENU, wt.HINSTANCE, ctypes.c_void_p]
u32.DefWindowProcW.argtypes = [wt.HWND, ctypes.c_uint, ctypes.c_size_t, ctypes.c_ssize_t]
u32.SendMessageW.argtypes = [wt.HWND, ctypes.c_uint, ctypes.c_size_t, ctypes.c_ssize_t]
u32.SendMessageW.restype = LRESULT
u32.RegisterClassExW.argtypes = [ctypes.POINTER(WNDCLASSEXW)]
u32.AdjustWindowRect.argtypes = [ctypes.POINTER(RECT), wt.DWORD, wt.BOOL]
u32.SetWindowPos.argtypes = [wt.HWND, wt.HWND, ctypes.c_int, ctypes.c_int,
                             ctypes.c_int, ctypes.c_int, ctypes.c_uint]
u32.SetLayeredWindowAttributes.argtypes = [wt.HWND, wt.COLORREF, ctypes.c_ubyte, wt.DWORD]
u32.SetWindowRgn.argtypes = [wt.HWND, ctypes.c_void_p, wt.BOOL]
u32.SetWindowTextW.argtypes = [wt.HWND, wt.LPCWSTR]
u32.GetWindowTextW.argtypes = [wt.HWND, wt.LPWSTR, ctypes.c_int]
u32.GetWindowRect.argtypes = [wt.HWND, ctypes.POINTER(RECT)]
u32.EnableWindow.argtypes = [wt.HWND, wt.BOOL]
u32.ShowWindow.argtypes = [wt.HWND, ctypes.c_int]
u32.SetTimer.argtypes = [wt.HWND, ctypes.c_size_t, ctypes.c_uint, ctypes.c_void_p]
u32.KillTimer.argtypes = [wt.HWND, ctypes.c_size_t]
u32.InvalidateRect.argtypes = [wt.HWND, ctypes.c_void_p, wt.BOOL]
u32.BeginPaint.argtypes = [wt.HWND, ctypes.POINTER(PAINTSTRUCT)]
u32.EndPaint.argtypes = [wt.HWND, ctypes.POINTER(PAINTSTRUCT)]
u32.DrawTextW.argtypes = [wt.HDC, wt.LPCWSTR, ctypes.c_int, ctypes.POINTER(RECT), ctypes.c_uint]
u32.GetSystemMetrics.argtypes = [ctypes.c_int]
u32.IsWindowVisible.argtypes = [wt.HWND]
u32.PostQuitMessage.argtypes = [ctypes.c_int]
u32.EnumDisplaySettingsW.argtypes = [wt.LPCWSTR, wt.DWORD, ctypes.POINTER(DEVMODEW)]
u32.GetCursorPos.argtypes = [ctypes.POINTER(wt.POINT)]
u32.SetCapture.argtypes = [wt.HWND]
u32.SetFocus.argtypes = [wt.HWND]
u32.SetForegroundWindow.argtypes = [wt.HWND]
u32.DestroyWindow.argtypes = [wt.HWND]
u32.LoadCursorW.argtypes = [wt.HINSTANCE, wt.LPCWSTR]
u32.GetDC.argtypes = [wt.HWND]
u32.ReleaseDC.argtypes = [wt.HWND, wt.HDC]
u32.GetMessageW.argtypes = [ctypes.POINTER(wt.MSG), wt.HWND, ctypes.c_uint, ctypes.c_uint]
u32.DispatchMessageW.argtypes = [ctypes.POINTER(wt.MSG)]
u32.TranslateMessage.argtypes = [ctypes.POINTER(wt.MSG)]
k32.GetModuleHandleW.argtypes = [wt.LPCWSTR]
g32.CreateSolidBrush.argtypes = [wt.COLORREF]
g32.CreatePen.argtypes = [ctypes.c_int, ctypes.c_int, wt.COLORREF]
g32.CreateFontW.argtypes = ([ctypes.c_int] * 5) + ([wt.DWORD] * 8) + [wt.LPCWSTR]
g32.CreateRectRgn.argtypes = [ctypes.c_int] * 4
g32.CreateRectRgn.restype = ctypes.c_void_p
g32.CombineRgn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
g32.SelectObject.argtypes = [wt.HDC, ctypes.c_void_p]
g32.DeleteObject.argtypes = [ctypes.c_void_p]
u32.FillRect.argtypes = [wt.HDC, ctypes.POINTER(RECT), ctypes.c_void_p]
g32.SetBkMode.argtypes = [wt.HDC, ctypes.c_int]
g32.SetTextColor.argtypes = [wt.HDC, wt.COLORREF]
g32.MoveToEx.argtypes = [wt.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
g32.LineTo.argtypes = [wt.HDC, ctypes.c_int, ctypes.c_int]
g32.GetDeviceCaps.argtypes = [wt.HDC, ctypes.c_int]


class RegionRecorderGUI:
    def __init__(self, outdir, limit_preset, selftest=None, selftest_sec=4.0):
        self.hinst = k32.GetModuleHandleW(None)
        hdc = u32.GetDC(0)
        self.dpi = g32.GetDeviceCaps(hdc, 88) or 96
        u32.ReleaseDC(0, hdc)
        self.s = self.dpi / 96.0                 # UI scale
        # safety net: if the process somehow stayed DPI-unaware, window/cursor coords
        # are logical and must be scaled up before handing them to gdigrab.
        self.logical_w = u32.GetSystemMetrics(0) or 1
        dm = DEVMODEW()
        dm.dmSize = ctypes.sizeof(DEVMODEW)
        ok = u32.EnumDisplaySettingsW(None, -1, ctypes.byref(dm))
        self.phys_w = dm.dmPelsWidth if ok else self.logical_w
        self.phys_h = dm.dmPelsHeight if ok else 1
        self.k = (self.phys_w / float(self.logical_w)) if self.phys_w >= self.logical_w else 1.0
        self.outdir = pathlib.Path(outdir)
        self.outdir.mkdir(parents=True, exist_ok=True)

        self.handlers = {}
        self.ctrl = {}
        self.hwnd_panel = self.hwnd_dim = self.hwnd_frame = self.hwnd_bar = None
        self.region = None                       # (x, y, w, h) physical px
        self.drag_from = None
        self.dragging = False
        self.frozen_rect = None
        self.proc = None
        self.ffmpeg = find_ffmpeg()
        self.rec_start = 0.0
        self.limit = float(limit_preset or 0)
        self.last_file = None
        self.font = g32.CreateFontW(-int(15 * self.s), 0, 0, 0, 400, 0, 0, 0, 1, 0, 0, 0, 0, "Microsoft YaHei UI")
        self.font_title = g32.CreateFontW(-int(19 * self.s), 0, 0, 0, 500, 0, 0, 0, 1, 0, 0, 0, 0, "Microsoft YaHei UI")
        self.br_green = g32.CreateSolidBrush(COL_FRAME_READY)
        self.br_red = g32.CreateSolidBrush(COL_FRAME_REC)
        self.br_bar = g32.CreateSolidBrush(0x002B2B2B)
        self.pen_band = g32.CreatePen(0, max(2, int(2 * self.s)), 0x0000D7FF)
        self.pen_hint = g32.CreatePen(0, 1, 0x00FFFFFF)
        self.frame_brush = self.br_green

        self._register_classes()
        self._build_panel()
        self._build_bar()
        self._build_dim()
        u32.ShowWindow(self.hwnd_panel, SW_SHOW)
        u32.SetWindowPos(self.hwnd_panel, HWND_TOPMOST, 0, 0, 0, 0,
                         SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW)
        self._status("就绪 · 缩放 %d%% · 坐标=%s%s" % (
            int(round(self.s * 100)),
            "物理像素" if abs(self.k - 1.0) < 0.01 else "逻辑像素 ×%.1f" % self.k,
            "" if self.ffmpeg else "  ⚠ 未找到 ffmpeg, 请放到 ffmpeg\\bin\\ffmpeg.exe 或加入 PATH"))
        u32.SetTimer(self.hwnd_panel, 2, 700, None)     # keep us above other topmost apps
        self._write_facts()
        self.selftest = selftest
        self.selftest_sec = selftest_sec
        self.st_flags = set()
        if selftest:
            self.st_t0 = dt.datetime.now()
            u32.SetTimer(self.hwnd_panel, 3, 150, None)

    def _write_facts(self):
        try:
            (pathlib.Path(__file__).resolve().parent / "last_run.txt").write_text(
                "time      : %s\n" % dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                "dpi api   : %s\n" % "; ".join(_dpi_log) +
                "GetDeviceCaps(88) = %d   ui scale s = %.2f\n" % (self.dpi, self.s) +
                "logical screen    = %d x %d\n" % (self.logical_w, u32.GetSystemMetrics(1)) +
                "physical screen   = %d x %d\n" % (self.phys_w, self.phys_h) +
                "coord factor k    = %.2f  (%s)\n" % (
                    self.k, "物理像素 = 直接可用" if abs(self.k - 1.0) < 0.01
                    else "逻辑像素, 录屏时会放大 %.1f 倍" % self.k),
                encoding="utf-8")
        except Exception:
            pass

    # ------------------------------------------------------------ classes
    def _register_classes(self):
        self.wc = WNDCLASSEXW()
        self.wc.cbSize = ctypes.sizeof(WNDCLASSEXW)
        self.wc.lpfnWndProc = WNDPROC(self._wndproc)
        self.wc.hInstance = self.hinst
        self.wc.hCursor = u32.LoadCursorW(0, wt.LPCWSTR(32512))   # IDC_ARROW
        self.wc.lpszClassName = "RRGuiClass"
        self.wc.hbrBackground = g32.CreateSolidBrush(0x00F5F5F5)
        if not u32.RegisterClassExW(ctypes.byref(self.wc)):
            raise ctypes.WinError(ctypes.get_last_error())

    def _mk(self, cls, text, style, ex, x, y, w, h, parent=None, cid=0):
        hwnd = u32.CreateWindowExW(ex, cls, text, style, x, y, w, h, parent, cid, self.hinst, None)
        if not hwnd:
            raise ctypes.WinError(ctypes.get_last_error())
        self.handlers[hwnd] = self._wndproc
        return hwnd

    # ------------------------------------------------------------ panel
    def _build_panel(self):
        s = self.s
        CW, CH = int(430 * s), int(258 * s)          # client area
        style = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU
        r = RECT(0, 0, CW, CH)
        u32.AdjustWindowRect(ctypes.byref(r), style, False)
        W, H = r.right - r.left, r.bottom - r.top
        self.panel_size = (W, H)
        px = u32.GetSystemMetrics(0) - W - int(24 * s)      # default: top-right, out of the way
        py = int(24 * s)
        self.hwnd_panel = self._mk("RRGuiClass", "区域录制", style,
                                   WS_EX_TOPMOST, px, py, W, H)
        self.lbl_title = self._mk("Static", "区域录制", WS_CHILD | WS_VISIBLE,
                                  0, int(16 * s), int(12 * s), int(398 * s), int(28 * s), self.hwnd_panel)
        self.lbl_region = self._mk("Static", "区域: 未选择   请点「框选区域」后用左键拖拽", WS_CHILD | WS_VISIBLE,
                                   0, int(16 * s), int(46 * s), int(398 * s), int(24 * s), self.hwnd_panel)
        y = int(80 * s)
        bw, bh = int(130 * s), int(34 * s)
        self.btn_pick = self._mk("Button", "框选区域", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                                 0, int(16 * s), y, bw, bh, self.hwnd_panel, ID_PICK)
        self.btn_confirm = self._mk("Button", "确认选区", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                                    0, int(154 * s), y, bw, bh, self.hwnd_panel, ID_CONFIRM)
        self.btn_redraw = self._mk("Button", "重画", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                                   0, int(292 * s), y, int(122 * s), bh, self.hwnd_panel, ID_REDRAW)
        y2 = int(126 * s)
        self.btn_start = self._mk("Button", "开始录制", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                                  0, int(16 * s), y2, int(180 * s), int(40 * s), self.hwnd_panel, ID_START)
        self.btn_stop = self._mk("Button", "结束录制", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                                 0, int(204 * s), y2, int(210 * s), int(40 * s), self.hwnd_panel, ID_STOP)
        y3 = int(178 * s)
        self._mk("Static", "限时(秒), 0=手动结束", WS_CHILD | WS_VISIBLE,
                 0, int(16 * s), y3 + int(3 * s), int(178 * s), int(22 * s), self.hwnd_panel)
        self.ed_limit = self._mk("Edit", str(int(self.limit)), WS_CHILD | WS_VISIBLE | WS_BORDER | ES_AUTOHSCROLL,
                                 0, int(200 * s), y3, int(100 * s), int(26 * s), self.hwnd_panel)
        self.lbl_status = self._mk("Static", "就绪", WS_CHILD | WS_VISIBLE,
                                   0, int(16 * s), int(216 * s), int(398 * s), int(34 * s), self.hwnd_panel)

        for h in (self.lbl_title, self.lbl_region, self.btn_pick, self.btn_confirm, self.btn_redraw,
                  self.btn_start, self.btn_stop, self.ed_limit, self.lbl_status):
            u32.SendMessageW(h, WM_SETFONT, self.font, 1)
        u32.SendMessageW(self.lbl_title, WM_SETFONT, self.font_title, 1)
        for h in (self.btn_confirm, self.btn_redraw, self.btn_stop):
            u32.EnableWindow(h, False)

    def _build_bar(self):
        s = self.s
        W, H = int(330 * s), int(96 * s)
        self.hwnd_bar = self._mk("RRGuiClass", "REC", WS_POPUP, WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
                                 int(40 * s), int(40 * s), W, H)
        self.lbl_rec = self._mk("Static", "● REC 0:00.0", WS_CHILD | WS_VISIBLE,
                                0, int(12 * s), int(8 * s), int(306 * s), int(28 * s), self.hwnd_bar)
        self.btn_stopbar = self._mk("Button", "结束录制", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
                                    0, int(12 * s), int(44 * s), int(306 * s), int(38 * s), self.hwnd_bar, ID_STOP)
        u32.SendMessageW(self.lbl_rec, WM_SETFONT, self.font, 1)
        u32.SendMessageW(self.btn_stopbar, WM_SETFONT, self.font, 1)

    def _build_dim(self):
        vx = u32.GetSystemMetrics(SM_XVIRTUALSCREEN)
        vy = u32.GetSystemMetrics(SM_YVIRTUALSCREEN)
        vw = u32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
        vh = u32.GetSystemMetrics(SM_CYVIRTUALSCREEN)
        self.vscreen = (vx, vy, vw, vh)
        self.hwnd_dim = self._mk("RRGuiClass", "RRdim", WS_POPUP,
                                 WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_LAYERED,
                                 vx, vy, vw, vh)
        u32.SetLayeredWindowAttributes(self.hwnd_dim, 0, COL_DIM, LWA_ALPHA)

    def _build_frame(self):
        x, y, w, h = self.region
        pad = max(3, int(3 * self.s))
        self.hwnd_frame = self._mk("RRGuiClass", "RRframe", WS_POPUP,
                                   WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
                                   x - pad, y - pad, w + 2 * pad, h + 2 * pad)
        r_out = g32.CreateRectRgn(0, 0, w + 2 * pad, h + 2 * pad)
        r_in = g32.CreateRectRgn(pad, pad, pad + w, pad + h)
        g32.CombineRgn(r_out, r_out, r_in, RGN_DIFF)
        u32.SetWindowRgn(self.hwnd_frame, r_out, True)
        g32.DeleteObject(r_in)
        u32.SetWindowPos(self.hwnd_frame, HWND_TOPMOST, 0, 0, 0, 0,
                         SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW)

    # ------------------------------------------------------------ helpers
    def _status(self, text):
        u32.SetWindowTextW(self.lbl_status, text)

    def _set_region_label(self):
        if self.region:
            x, y, w, h = self.region
            u32.SetWindowTextW(self.lbl_region, "区域: %d × %d   (左上 %d, %d)" % (w, h, x, y))
        else:
            u32.SetWindowTextW(self.lbl_region, "区域: 未选择   请点「框选区域」后用左键拖拽")

    def _place_outside(self, w, h):
        """Pick a top-left for a w×h window that sits outside the region if possible."""
        vx, vy, vw, vh = self.vscreen
        x, y, rw, rh = self.region
        gap = int(10 * self.s)
        for cand in ((x, y + rh + gap), (x, y - h - gap), (x + rw + gap, y), (x - w - gap, y)):
            cx, cy = cand
            if cx >= vx and cy >= vy and cx + w <= vx + vw and cy + h <= vy + vh:
                return cx, cy
        # no clean spot: put it in the corner with the least overlap
        corners = [(vx + gap, vy + gap), (vx + vw - w - gap, vy + gap),
                   (vx + gap, vy + vh - h - gap), (vx + vw - w - gap, vy + vh - h - gap)]
        best, best_cost = corners[0], None
        for cx, cy in corners:
            ox = max(0, min(cx + w, x + rw) - max(cx, x))
            oy = max(0, min(cy + h, y + rh) - max(cy, y))
            cost = ox * oy
            if best_cost is None or cost < best_cost:
                best, best_cost = (cx, cy), cost
        return best

    def _move(self, hwnd, x, y, w=None, h=None):
        u32.SetWindowPos(hwnd, HWND_TOPMOST, int(x), int(y), int(w or 0), int(h or 0),
                         SWP_NOACTIVATE | (SWP_NOSIZE if w is None else 0))

    # ------------------------------------------------------------ actions
    def action_pick(self):
        self._stop_recording()   # safety
        self.frozen_rect = None
        self.drag_from = None
        u32.EnableWindow(self.btn_confirm, False)
        u32.EnableWindow(self.btn_redraw, False)
        self._status("拖拽选择区域 -- 左键按住拖出矩形, 松开; 右键或 ESC 取消")
        self._set_region_label()
        u32.SetWindowPos(self.hwnd_dim, self.hwnd_panel, 0, 0, 0, 0,
                         SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW)
        u32.SetForegroundWindow(self.hwnd_dim)
        u32.SetFocus(self.hwnd_dim)

    def action_confirm(self):
        if not self.frozen_rect:
            return
        x1, y1, x2, y2 = self.frozen_rect
        w = abs(x2 - x1) - abs(x2 - x1) % 2
        h = abs(y2 - y1) - abs(y2 - y1) % 2
        if w < 16 or h < 16:
            self._status("选区太小, 请重画")
            return
        self.region = (min(x1, x2), min(y1, y2), w, h)
        u32.ShowWindow(self.hwnd_dim, SW_HIDE)
        if self.hwnd_frame:
            u32.DestroyWindow(self.hwnd_frame)
            self.hwnd_frame = None
        self._build_frame()
        self.frame_brush = self.br_green
        u32.InvalidateRect(self.hwnd_frame, None, True)
        u32.EnableWindow(self.btn_confirm, False)
        u32.EnableWindow(self.btn_redraw, True)
        self._set_region_label()
        self._status("选区已确认, 绿框就是录制范围. 点「开始录制」")

    def action_redraw(self):
        if self.hwnd_frame:
            u32.DestroyWindow(self.hwnd_frame)
            self.hwnd_frame = None
        self.action_pick()

    def action_start(self):
        if self.proc:
            return
        if not self.region:
            self._status("还没有选区: 先点「框选区域」拖出矩形, 再点「确认选区」")
            return
        if not self.ffmpeg:
            self._status("未找到 ffmpeg。放到 ffmpeg\\bin\\ffmpeg.exe, 或在 PATH 上装 ffmpeg, 然后重启本程序")
            return
        try:
            self.limit = max(0.0, float(u32_get_text(self.ed_limit) or 0))
        except ValueError:
            self.limit = 0.0
        x, y, w, h = self.region
        if abs(self.k - 1.0) >= 0.01:            # logical -> physical for gdigrab
            x, y = int(round(x * self.k)), int(round(y * self.k))
            w, h = int(round(w * self.k)), int(round(h * self.k))
        w -= w % 2
        h -= h % 2
        ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        out = self.outdir / ("region_%s.mp4" % ts)
        cmd = [self.ffmpeg, "-hide_banner", "-loglevel", "error",
               "-f", "gdigrab", "-framerate", "30", "-draw_mouse", "1",
               "-offset_x", str(x), "-offset_y", str(y), "-video_size", "%dx%d" % (w, h),
               "-i", "desktop",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
               "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-y", str(out)]
        try:
            self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
        except OSError as e:
            self.proc = None
            self._status("启动 ffmpeg 失败: %s" % e)
            return
        self.rec_start = dt.datetime.now()
        self.last_file = out

        self.frame_brush = self.br_red
        if self.hwnd_frame:
            u32.InvalidateRect(self.hwnd_frame, None, True)

        u32.ShowWindow(self.hwnd_panel, SW_HIDE)
        u32.EnableWindow(self.btn_start, False)
        bx, by = self._place_outside(int(330 * self.s), int(96 * self.s))
        u32.SetWindowPos(self.hwnd_bar, HWND_TOPMOST, bx, by, 0, 0,
                         SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW)
        u32.SetWindowTextW(self.lbl_rec, "● REC  0:00.0")
        u32.EnableWindow(self.btn_stopbar, True)
        u32.SetTimer(self.hwnd_bar, 1, 200, None)

    def panel_pos(self):
        r = RECT()
        u32.GetWindowRect(self.hwnd_panel, ctypes.byref(r))
        return r.left, r.top

    def action_stop(self):
        self._stop_recording()

    def _stop_recording(self):
        if not self.proc:
            return
        u32.KillTimer(self.hwnd_bar, 1)
        p = self.proc
        self.proc = None
        try:
            if p.stdin:
                p.stdin.write(b"q")
                p.stdin.flush()
            p.wait(timeout=20)
        except Exception:
            try:
                p.terminate()
                p.wait(timeout=10)
            except Exception:
                pass
        u32.ShowWindow(self.hwnd_bar, SW_HIDE)
        u32.EnableWindow(self.btn_start, True)
        u32.ShowWindow(self.hwnd_panel, SW_SHOW)
        u32.SetWindowPos(self.hwnd_panel, HWND_TOPMOST, 0, 0, 0, 0,
                         SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW)
        self.frame_brush = self.br_green
        if self.hwnd_frame:
            u32.InvalidateRect(self.hwnd_frame, None, True)
        elapsed = (dt.datetime.now() - self.rec_start).total_seconds() if self.rec_start else 0
        if self.last_file and self.last_file.exists():
            mb = self.last_file.stat().st_size / 1048576
            self._status("已保存 %.1fs / %.2f MB  %s" % (elapsed, mb, self.last_file.name))
        else:
            self._status("录制结束, 但文件没生成, 检查 ffmpeg")

    # ------------------------------------------------------------ painting
    def paint_dim(self, hwnd):
        ps = PAINTSTRUCT()
        hdc = u32.BeginPaint(hwnd, ctypes.byref(ps))
        if self.frozen_rect:
            x1, y1, x2, y2 = self.frozen_rect
        elif self.dragging and self.drag_from:
            x1, y1 = self.drag_from
            pt = wt.POINT()
            u32.GetCursorPos(ctypes.byref(pt))
            x2, y2 = pt.x, pt.y
        else:
            x1 = y1 = x2 = y2 = None

        if x1 is not None:
            old = g32.SelectObject(hdc, self.pen_band)
            g32.MoveToEx(hdc, x1, y1, None)
            g32.LineTo(hdc, x2, y1)
            g32.LineTo(hdc, x2, y2)
            g32.LineTo(hdc, x1, y2)
            g32.LineTo(hdc, x1, y1)
            g32.SelectObject(hdc, old)
            txt = "%d × %d" % (abs(x2 - x1), abs(y2 - y1))
            tx = min(x1, x2) + int(8 * self.s)
            ty = max(min(y1, y2) - int(30 * self.s), 4)
            r = RECT(tx - int(6 * self.s), ty - 2, tx + int(150 * self.s), ty + int(26 * self.s))
            u32.FillRect(hdc, ctypes.byref(r), ctypes.c_void_p(self.br_bar))
            g32.SetBkMode(hdc, 1)
            g32.SetTextColor(hdc, 0x00FFFFFF)
            rr = RECT(tx, ty, tx + int(160 * self.s), ty + int(24 * self.s))
            u32.DrawTextW(hdc, txt, -1, ctypes.byref(rr), DT_LEFT | DT_SINGLELINE | DT_VCENTER)

        vx, vy, vw, vh = self.vscreen
        hint = "左键按住拖拽选择区域    松开后用「确认选区」    ESC / 右键取消"
        g32.SetBkMode(hdc, 1)
        g32.SetTextColor(hdc, 0x00FFFFFF)
        old = g32.SelectObject(hdc, self.font)
        hr = RECT(vx, vy + int(24 * self.s), vx + vw, vy + int(60 * self.s))
        u32.DrawTextW(hdc, hint, -1, ctypes.byref(hr), DT_CENTER | DT_SINGLELINE | DT_VCENTER)
        g32.SelectObject(hdc, old)
        u32.EndPaint(hwnd, ctypes.byref(ps))

    def paint_frame(self, hwnd):
        ps = PAINTSTRUCT()
        hdc = u32.BeginPaint(hwnd, ctypes.byref(ps))
        u32.FillRect(hdc, ctypes.byref(ps.rcPaint), ctypes.c_void_p(self.frame_brush))
        u32.EndPaint(hwnd, ctypes.byref(ps))

    # ------------------------------------------------------------ wndproc
    def _wndproc(self, hwnd, msg, wparam, lparam):
        try:
            if msg == WM_PAINT:
                if hwnd == self.hwnd_dim:
                    self.paint_dim(hwnd)
                    return 0
                if hwnd == self.hwnd_frame:
                    self.paint_frame(hwnd)
                    return 0
            elif msg == WM_ERASEBKGND:
                if hwnd in (self.hwnd_dim, self.hwnd_frame):
                    return 1
            elif msg == WM_LBUTTONDOWN and hwnd == self.hwnd_dim:
                x = ctypes.c_short(lparam & 0xFFFF).value + self.vscreen[0]
                y = ctypes.c_short((lparam >> 16) & 0xFFFF).value + self.vscreen[1]
                self.dragging = True
                self.frozen_rect = None
                self.drag_from = (x, y)
                u32.SetCapture(hwnd)
                u32.InvalidateRect(hwnd, None, True)
                return 0
            elif msg == WM_MOUSEMOVE and hwnd == self.hwnd_dim and self.dragging:
                u32.InvalidateRect(hwnd, None, True)
                return 0
            elif msg == WM_LBUTTONUP and hwnd == self.hwnd_dim and self.dragging:
                pt = wt.POINT()
                u32.GetCursorPos(ctypes.byref(pt))
                self.dragging = False
                u32.ReleaseCapture()
                x1, y1 = self.drag_from
                if abs(pt.x - x1) > 8 and abs(pt.y - y1) > 8:
                    self.frozen_rect = (x1, y1, pt.x, pt.y)
                    u32.EnableWindow(self.btn_confirm, True)
                    u32.EnableWindow(self.btn_redraw, True)
                    self._status("已框出 %d × %d -- 点「确认选区」, 或「重画」" %
                                 (abs(pt.x - x1), abs(pt.y - y1)))
                else:
                    self.frozen_rect = None
                    self._status("选区太小, 请重新拖拽")
                u32.InvalidateRect(hwnd, None, True)
                return 0
            elif msg == WM_RBUTTONDOWN and hwnd == self.hwnd_dim:
                self.dragging = False
                self.frozen_rect = None
                self.drag_from = None
                u32.ReleaseCapture()
                u32.ShowWindow(self.hwnd_dim, SW_HIDE)
                self._status("已取消框选")
                return 0
            elif msg == WM_KEYDOWN and wparam == VK_ESCAPE and hwnd == self.hwnd_dim:
                self.dragging = False
                self.frozen_rect = None
                self.drag_from = None
                u32.ReleaseCapture()
                u32.ShowWindow(self.hwnd_dim, SW_HIDE)
                self._status("已取消框选")
                return 0
            elif msg == WM_COMMAND:
                cid = wparam & 0xFFFF
                if cid == ID_PICK:
                    self.action_pick()
                elif cid == ID_CONFIRM:
                    self.action_confirm()
                elif cid == ID_REDRAW:
                    self.action_redraw()
                elif cid == ID_START:
                    self.action_start()
                elif cid == ID_STOP:
                    self.action_stop()
                return 0
            elif msg == WM_TIMER and hwnd == self.hwnd_panel and wparam == 3 and self.selftest:
                t = (dt.datetime.now() - self.st_t0).total_seconds()
                if t > 0.4 and "r" not in self.st_flags:
                    self.st_flags.add("r")
                    self.region = tuple(self.selftest)
                    self._build_frame()
                    u32.InvalidateRect(self.hwnd_frame, None, True)
                    self._set_region_label()
                    self._status("SELFTEST: 区域已设定, 1 秒后开始录制")
                elif t > 1.0 and "s" not in self.st_flags:
                    self.st_flags.add("s")
                    self.action_start()
                elif t > 1.0 + self.selftest_sec and "e" not in self.st_flags:
                    self.st_flags.add("e")
                    self.action_stop()
                    self._status("SELFTEST: 已结束 -> " + str(self.region))
                elif t > 2.2 + self.selftest_sec and "q" not in self.st_flags:
                    self.st_flags.add("q")
                    u32.DestroyWindow(self.hwnd_panel)
                return 0
            elif msg == WM_TIMER and hwnd == self.hwnd_panel:
                for h in (self.hwnd_frame, self.hwnd_bar, self.hwnd_dim, self.hwnd_panel):
                    if h and u32.IsWindowVisible(h):
                        u32.SetWindowPos(h, HWND_TOPMOST, 0, 0, 0, 0,
                                         SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)
                return 0
            elif msg == WM_TIMER and hwnd == self.hwnd_bar:
                el = (dt.datetime.now() - self.rec_start).total_seconds()
                if self.limit and el >= self.limit:
                    self._stop_recording()
                    return 0
                tail = "/ %gs" % int(self.limit) if self.limit else "(手动结束)"
                u32.SetWindowTextW(self.lbl_rec, "● REC  %d:%04.1f  %s" % (int(el // 60), el % 60, tail))
                return 0
            elif msg == WM_CLOSE:
                if hwnd == self.hwnd_panel:
                    u32.DestroyWindow(hwnd)
                else:
                    u32.ShowWindow(hwnd, SW_HIDE)
                return 0
            elif msg == WM_DESTROY:
                if hwnd == self.hwnd_panel:
                    self._stop_recording()
                    u32.PostQuitMessage(0)
                return 0
        except Exception as e:      # never let a python error kill the loop
            print("WNDPROC ERROR:", repr(e), file=sys.stderr)
        return u32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def run(self):
        msg = wt.MSG()
        while u32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            u32.TranslateMessage(ctypes.byref(msg))
            u32.DispatchMessageW(ctypes.byref(msg))
        return 0


def u32_get_text(hwnd):
    buf = ctypes.create_unicode_buffer(64)
    u32.GetWindowTextW(hwnd, buf, 64)
    return buf.value.strip()


def find_ffmpeg():
    import os
    env = os.environ.get("FFMPEG")
    if env and pathlib.Path(env).exists():
        return env
    local = pathlib.Path(__file__).resolve().parent / "ffmpeg" / "bin" / "ffmpeg.exe"
    if local.exists():
        return str(local)
    import shutil
    return shutil.which("ffmpeg")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(pathlib.Path.home() / "Videos" / "Screen Recordings"))
    ap.add_argument("--sec", type=float, default=0.0, help="preset time limit, 0 = manual stop")
    ap.add_argument("--selftest", help='QA mode: "X Y W H" region, record without user input, then quit')
    ap.add_argument("--selftest-sec", type=float, default=4.0)
    a = ap.parse_args()
    st = None
    if a.selftest:
        st = tuple(int(v) for v in a.selftest.replace(",", " ").split())
        if len(st) != 4:
            print("--selftest needs 4 numbers: X Y W H")
            return 2
    gui = RegionRecorderGUI(a.out, a.sec, st, a.selftest_sec)
    return gui.run()


if __name__ == "__main__":
    sys.exit(main())
