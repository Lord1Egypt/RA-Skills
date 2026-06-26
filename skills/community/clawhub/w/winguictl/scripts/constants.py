#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Win32 API constant definitions.

Contains virtual key code mappings, Win32 control type mappings, and other constants.
Input simulation and screenshot functionality has been migrated to use pywin32
(win32api/win32gui/win32con), making ctypes structures and low-level constants
no longer necessary.
"""

# ── Optional Dependency Detection ────────────────────────────────────
# Centralized detection for optional dependencies with helpful error messages

try:
    import cv2  # pylint: disable=unused-import
    import numpy as np  # pylint: disable=unused-import
    _OPENCV_AVAILABLE = True
except ImportError:
    _OPENCV_AVAILABLE = False
    cv2 = None  # type: ignore[misc,assignment]
    np = None  # type: ignore[misc,assignment]

try:
    import wx_ocr  # pylint: disable=unused-import
    _WX_OCR_AVAILABLE = True
except ImportError:
    _WX_OCR_AVAILABLE = False
    wx_ocr = None  # type: ignore[misc,assignment]


def check_opencv_available() -> None:
    """Raise RuntimeError if opencv-python is not installed."""
    if not _OPENCV_AVAILABLE:
        raise RuntimeError(
        "opencv-python is required for image matching. "
        "Install with: pip install opencv-python"
    )


def check_wx_ocr_available() -> None:
    """Raise RuntimeError if wx-ocr is not installed."""
    if not _WX_OCR_AVAILABLE:
        raise RuntimeError("wx-ocr is required for OCR. Install with: pip install wx-ocr")


# ── SendInput Constants ──────────────────────────────────────────────
# Absolute coordinate range for SendInput mouse operations (0-65535)
SENDINPUT_ABSOLUTE_MAX = 65535

# Default delays for input simulation (milliseconds)
DEFAULT_CLICK_DELAY_MS = 50
DEFAULT_KEY_DELAY_MS = 50
DEFAULT_DRAG_START_DELAY_MS = 50
DEFAULT_HOTKEY_DELAY_MS = 50

# Drag animation step interval (~60 FPS)
DEFAULT_DRAG_STEP_INTERVAL_MS = 16

# ── UIA Driver Timeouts ──────────────────────────────────────────────
DEFAULT_UIA_WAIT_TIMEOUT_SEC = 3
DEFAULT_COMBOBOX_DROPDOWN_TIMEOUT_MS = 500
DEFAULT_COMBOBOX_POLL_INTERVAL_MS = 50

# ── Error Codes ──────────────────────────────────────────────────────
class ErrorCode:
    """Standard error codes for action results."""

    OK = "OK"
    FAILED = "FAILED"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    TIMEOUT = "TIMEOUT"
    DRY_RUN = "DRY_RUN"
    ERROR = "ERROR"

# ── Virtual Key Code Mapping ─────────────────────────────────────────
# Key name (lowercase) → Win32 virtual key code, used for send_press_key / send_hotkey

VK_CODE_MAP = {
    "backspace": 0x08,
    "tab": 0x09,
    "enter": 0x0D,
    "return": 0x0D,
    "shift": 0x10,
    "ctrl": 0x11,
    "control": 0x11,
    "alt": 0x12,
    "pause": 0x13,
    "capslock": 0x14,
    "esc": 0x1B,
    "escape": 0x1B,
    "space": 0x20,
    "pageup": 0x21,
    "pagedown": 0x22,
    "end": 0x23,
    "home": 0x24,
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "insert": 0x2D,
    "delete": 0x2E,
    "del": 0x2E,
    "meta": 0x5B,
    "win": 0x5B,
    "cmd": 0x5B,
}

# F1-F12: VK_F1=0x70 (112) through VK_F12=0x7B (123)
# Formula: 0x6F + index gives 0x70 for F1, 0x7B for F12
for _index in range(1, 13):
    VK_CODE_MAP[f"f{_index}"] = 0x6F + _index
for _char in "abcdefghijklmnopqrstuvwxyz":
    VK_CODE_MAP[_char] = ord(_char.upper())
for _digit in "0123456789":
    VK_CODE_MAP[_digit] = ord(_digit)

# ── Win32 Control Class Name → Control Type Mapping ──────────────────
# Used in win32_driver.py to infer control type from window class name

WIN32_CONTROL_TYPE_MAP: dict[str, str] = {
    "Button": "Button",
    "Edit": "Edit",
    "ComboBox": "ComboBox",
    "ListBox": "ListBox",
    "Static": "Text",
    "ScrollBar": "ScrollBar",
    "ToolbarWindow32": "ToolBar",
    "ReBarWindow32": "ReBar",
    "msctls_statusbar32": "StatusBar",
    "msctls_progress32": "ProgressBar",
    "SysListView32": "ListView",
    "SysTreeView32": "TreeView",
    "SysTabControl32": "Tab",
    "SysHeader32": "Header",
    "SysLink": "Link",
    "RichEdit": "Edit",
    "RichEdit20A": "Edit",
    "RichEdit20W": "Edit",
    "TRichView": "Document",
    "TRichViewEdit": "Edit",
    "TComboBox": "ComboBox",
    "TListBox": "ListBox",
    "TButton": "Button",
    "TCheckBox": "CheckBox",
    "TRadioButton": "RadioButton",
    "TGroupBox": "GroupBox",
    "TEdit": "Edit",
    "TMemo": "Edit",
    "TPageControl": "Tab",
    "TTabSheet": "TabPage",
    "TToolBar": "ToolBar",
    "TStatusBar": "StatusBar",
    "TTreeView": "TreeView",
    "TListView": "ListView",
    "TProgressBar": "ProgressBar",
    "TTrackBar": "Slider",
    "TDateTimePicker": "DateTimePicker",
    "TMonthCalendar": "Calendar",
    "TUpDown": "Spinner",
    "THotKey": "HotKey",
    "TAnimate": "Animation",
    "THeaderControl": "Header",
    "TPageScroller": "PageScroller",
    "TControlBar": "ControlBar",
    "TCategoryPanelGroup": "CategoryPanel",
    "TFlowPanel": "Panel",
    "TGridPanel": "Grid",
    "TStackPanel": "Panel",
    "TPanel": "Panel",
    "TLabel": "Text",
    "TImage": "Image",
    "TShape": "Shape",
    "TBevel": "Bevel",
    "TPaintBox": "Canvas",
    "TChart": "Chart",
    "TDBGrid": "DataGrid",
    "TDBNavigator": "Navigator",
    "TDBLookupComboBox": "ComboBox",
    "TDBLookupListBox": "ListBox",
    "TDBRadioGroup": "RadioGroup",
    "TDBCheckBox": "CheckBox",
    "TDBEdit": "Edit",
    "TDBMemo": "Edit",
    "TDBText": "Text",
    "TDBRichEdit": "Edit",
    "TDBCtrlGrid": "Grid",
    "TDBChart": "Chart",
    "TDecisionGrid": "Grid",
    "TDecisionPivot": "Pivot",
    "TDecisionSource": "Source",
    "TDecisionQuery": "Query",
    "TDecisionCube": "Cube",
    "TCrossTabSource": "Source",
    "WindowsForms10.BUTTON": "Button",
    "WindowsForms10.EDIT": "Edit",
    "WindowsForms10.COMBOBOX": "ComboBox",
    "WindowsForms10.LISTBOX": "ListBox",
    "WindowsForms10.STATIC": "Text",
    "WindowsForms10.Window": "Window",
    "WindowsForms10.RichEdit": "Edit",
    "WindowsForms10.SysTreeView32": "TreeView",
    "WindowsForms10.SysListView32": "ListView",
    "WindowsForms10.SysTabControl32": "Tab",
    "WindowsForms10.msctls_statusbar32": "StatusBar",
    "WindowsForms10.msctls_progress32": "ProgressBar",
    "WindowsForms10.ToolbarWindow32": "ToolBar",
    "WindowsForms10.ReBarWindow32": "ReBar",
    "WindowsForms10.app": "Application",
    "WindowsForms10.MDICLIENT": "MDIClient",
    "WindowsForms10.SCROLLBAR": "ScrollBar",
    "ThunderRT6TextBox": "Edit",
    "ThunderRT6CheckBox": "CheckBox",
    "ThunderRT6OptionButton": "RadioButton",
    "ThunderRT6CommandButton": "Button",
    "ThunderRT6Frame": "GroupBox",
    "ThunderRT6ComboBox": "ComboBox",
    "ThunderRT6ListBox": "ListBox",
    "ThunderRT6DirListBox": "ListBox",
    "ThunderRT6FileListBox": "ListBox",
    "ThunderRT6DriveListBox": "ComboBox",
    "ThunderTextBox": "Edit",
    "ThunderCheckBox": "CheckBox",
    "ThunderOptionButton": "RadioButton",
    "ThunderCommandButton": "Button",
    "ThunderFrame": "GroupBox",
    "ThunderComboBox": "ComboBox",
    "ThunderListBox": "ListBox",
    "ThunderDirListBox": "ListBox",
    "ThunderFileListBox": "ListBox",
    "ThunderDriveListBox": "ComboBox",
    "#32770": "Dialog",
    "#32768": "Menu",
    "#32769": "Desktop",
    "#32771": "TaskSwitcher",
    "#32772": "TaskManager",
    "DUIViewWndClassName": "View",
    "DirectUIHWND": "UIView",
    "CtrlNotifySink": "Container",
    "FloatNotifySink": "Container",
    "NamespaceTreeControl": "TreeView",
    "SHELLDLL_DefView": "ShellView",
    "ExplorerBrowser": "Browser",
    "ComboBoxEx32": "ComboBox",
    "msctls_trackbar32": "Slider",
    "msctls_updown32": "Spinner",
    "msctls_hotkey32": "HotKey",
    "msctls_datetimepickertime": "DateTimePicker",
    "SysDateTimePick32": "DateTimePicker",
    "SysMonthCal32": "Calendar",
    "SysIPAddress32": "IPAddress",
    "SysPager": "Pager",
    "NativeHWNDHost": "Host",
    "tooltips_class32": "ToolTip",
    "tooltips_class": "ToolTip",
    "ComboLBox": "ListBox",
    "MDIClient": "MDIClient",
    "Toolbar": "ToolBar",
    "DDEMLAnsiClient": "DDEClient",
    "DDEMLAnsiServer": "DDEServer",
    "DDEMLUnicodeClient": "DDEClient",
    "DDEMLUnicodeServer": "DDEServer",
    "GDI+ Hook Window Class": "Hook",
    "Ghost": "Ghost",
    "IconOverlayClass": "Overlay",
    "MCIQTZ_WindowClass": "Media",
    "MediaPlayer": "Media",
    "OpenListView": "ListView",
    "PrintTray_Notify_WndClass": "Notify",
    "QPaste_CallbackWndClass": "Callback",
    "ReBarWindow": "ReBar",
    "SysAnimate32": "Animation",
    "SysCredential": "Credential",
    "SysMV_Windows10": "View",
    "SysPalette": "Palette",
    "SysRebar32": "ReBar",
    "SysTabControl": "Tab",
    "TaskManagerWindow": "TaskManager",
    "ToolbarWindow": "ToolBar",
    "TscShellContainerClass": "Shell",
    "UxTheme_Class": "Theme",
    "VBBubble": "Bubble",
    "VCFolder": "Folder",
    "VistaOpusWindow": "Window",
    "WMP Skin Container": "Container",
    "WMPAppFWContainer": "Container",
    "WMPAppHost": "Host",
    "WMPCoreWnd": "Core",
    "WMPGraphWnd": "Graph",
    "WMPLinkMsgWindow": "Message",
    "WMPNSInfo": "Info",
    "WMPPlayHost": "Host",
    "WMPSkinWnd": "Skin",
    "WMPSourceWnd": "Source",
    "WMPSwitchBarWnd": "Bar",
    "WMPVideoCtrlHost": "Host",
    "WMPVisualHost": "Host",
    "WMP_VideoAccelerator": "Accelerator",
    "WebViewHost": "WebView",
    "Internet Explorer_Server": "Browser",
    "Chrome_WidgetWin_0": "Browser",
    "Chrome_WidgetWin_1": "Browser",
    "MozillaWindowClass": "Browser",
    "MozillaDialogClass": "Dialog",
    "MozillaContentWindowClass": "Content",
    "MozillaDropShadowWindowClass": "Shadow",
    "MozillaTaskbarPreviewClass": "Preview",
    "MozillaTaskbarPreviewNumberClass": "Preview",
    "Afx:": "Window",
    "AfxWnd": "Window",
    "AfxControlBar": "ToolBar",
    "AfxMDIFrame": "MDIFrame",
    "AfxFrameOrView": "View",
    "TApplication": "Application",
    "TMainForm": "Window",
    "TForm": "Window",
    "TModalForm": "Dialog",
    "TDataModule": "DataModule",
    "TFrame": "Frame",
    "TActionMainMenuBar": "MenuBar",
    "TActionToolBar": "ToolBar",
    "TActionManager": "Manager",
    "TActionList": "List",
    "TAction": "Action",
    "TMenu": "Menu",
    "TPopupMenu": "PopupMenu",
    "TMainMenu": "MainMenu",
    "TMenuItem": "MenuItem",
    "TTimer": "Timer",
    "TOpenDialog": "FileDialog",
    "TSaveDialog": "FileDialog",
    "TOpenPictureDialog": "FileDialog",
    "TSavePictureDialog": "FileDialog",
    "TFontDialog": "Dialog",
    "TColorDialog": "Dialog",
    "TPrintDialog": "Dialog",
    "TPrinterSetupDialog": "Dialog",
    "TFindDialog": "Dialog",
    "TReplaceDialog": "Dialog",
    "TPageSetupDialog": "Dialog",
    "TCustomizeDlg": "Dialog",
    "TStandardColorMap": "ColorMap",
    "TTwain": "Twain",
    "TComPort": "Port",
    "TComComboBox": "ComboBox",
    "TComRadioGroup": "RadioGroup",
    "TComCheckBox": "CheckBox",
    "TComEdit": "Edit",
    "TComMemo": "Edit",
    "TComButton": "Button",
    "TComBitBtn": "Button",
    "TComSpeedButton": "Button",
    "TComSpinEdit": "Edit",
    "TComListBox": "ListBox",
    "TComCheckListBox": "ListBox",
    "TComTreeView": "TreeView",
    "TComListView": "ListView",
    "TComHeaderControl": "Header",
    "TComStatusBar": "StatusBar",
    "TComToolBar": "ToolBar",
    "TComCoolBar": "CoolBar",
    "TComPageControl": "Tab",
    "TComTabControl": "Tab",
    "TComScrollBox": "ScrollBox",
    "TComSplitter": "Splitter",
    "TComControlBar": "ControlBar",
    "TComPageScroller": "PageScroller",
    "TComCategoryPanelGroup": "CategoryPanel",
    "TComCategoryPanel": "Panel",
    "TComFlowPanel": "Panel",
    "TComGridPanel": "Grid",
    "TComStackPanel": "Panel",
    "TComPanel": "Panel",
    "TComLabel": "Text",
    "TComLinkLabel": "Link",
    "TComStaticText": "Text",
    "TComImage": "Image",
    "TComShape": "Shape",
    "TComBevel": "Bevel",
    "TComPaintBox": "Canvas",
    "TComChart": "Chart",
    "TComDBGrid": "DataGrid",
    "TComDBNavigator": "Navigator",
    "TComDBLookupComboBox": "ComboBox",
    "TComDBLookupListBox": "ListBox",
    "TComDBRadioGroup": "RadioGroup",
    "TComDBCheckBox": "CheckBox",
    "TComDBEdit": "Edit",
    "TComDBMemo": "Edit",
    "TComDBText": "Text",
    "TComDBRichEdit": "Edit",
    "TComDBCtrlGrid": "Grid",
    "TComDBChart": "Chart",
    "TComDecisionGrid": "Grid",
    "TComDecisionPivot": "Pivot",
    "TComDecisionSource": "Source",
    "TComDecisionQuery": "Query",
    "TComDecisionCube": "Cube",
    "TComCrossTabSource": "Source",
}
