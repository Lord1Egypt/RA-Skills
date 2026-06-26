#!/usr/bin/env python3
"""
微信桌面自动化工具 - 支持Windows和macOS
功能：激活窗口、定位区域、获取好友列表、获取聊天记录、发送消息
"""

import os
import sys
import time
import json
import logging
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from scripts.hardware_simulator import HardwareSimulator
from scripts.behavior_simulator import BehaviorSimulator
from scripts.anti_detection import AntiDetection
from dataclasses import dataclass
from datetime import datetime
import random
import pyperclip
import requests
import uiautomation as auto
from paddleocr import PaddleOCR
from PIL import ImageGrab
# 平台相关导入
import platform

IS_WINDOWS = platform.system() == "Windows"
IS_MACOS = platform.system() == "Darwin"
os.environ['FLAGS_use_onednn'] = '0'
os.environ['PADDLE_NEW_IR'] = 'OFF'

if IS_WINDOWS:
    import win32gui
    import win32con
    import win32process
elif IS_MACOS:
    # macOS依赖需要单独安装
    try:
        from AppKit import NSWorkspace, NSApplication
        import Quartz
    except ImportError:
        print("macOS依赖未安装，请运行: pip install pyobjc-framework-Quartz")
        sys.exit(1)

import pyautogui
import cv2
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wechat_automation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class WeChatRegion:
    """微信界面区域配置 - 根据精确布局定义"""
    window_rect: Tuple[int, int, int, int] = None  # (x, y, width, height)

    # 主要区域
    sidebar: Tuple[int, int, int, int] = None  # 侧边栏区域
    contact_panel: Tuple[int, int, int, int] = None  # 中间联系人面板
    chat_panel: Tuple[int, int, int, int] = None  # 右侧聊天面板

    # 侧边栏子区域
    sidebar_avatar: Tuple[int, int, int, int] = None  # 头像区域
    sidebar_chat_icon: Tuple[int, int, int, int] = None  # 消息图标（第一个菜单）
    sidebar_contact_icon: Tuple[int, int, int, int] = None  # 通讯录图标

    # 联系人面板子区域
    contact_search_area: Tuple[int, int, int, int] = None  # 搜索区域
    contact_search_input: Tuple[int, int, int, int] = None  # 搜索输入框
    contact_list: Tuple[int, int, int, int] = None  # 好友列表区域

    # 聊天面板子区域
    chat_header: Tuple[int, int, int, int] = None  # 头部区域
    chat_messages: Tuple[int, int, int, int] = None  # 消息记录区域
    chat_input_area: Tuple[int, int, int, int] = None  # 聊天区域（工具栏+输入框+底部）
    chat_toolbar: Tuple[int, int, int, int] = None  # 聊天工具栏
    chat_input_box: Tuple[int, int, int, int] = None  # 聊天输入框
    chat_bottom_area: Tuple[int, int, int, int] = None  # 底部区域
    chat_send_button: Tuple[int, int, int, int] = None  # 发送按钮

    # 搜索结果第一个联系人位置（不需要整个浮窗区域）
    search_result_first: Tuple[int, int, int, int] = None  # 搜索结果第一个联系人

    # 固定参数 - 根据微信界面精确尺寸定义
    sidebar_width: int = 60  # 侧边栏宽度
    contact_panel_min_width: int = 240  # 中间区域最小宽度
    split_line_width: int = 1  # 分割线宽度

    # 侧边栏参数
    sidebar_avatar_height: int = 65  # 头像区域高度
    sidebar_icon_height: int = 50  # 菜单图标高度
    sidebar_icon_margin: int = 10  # 图标上下间距
    sidebar_icon_size: int = 40  # 图标大小

    # 联系人面板参数
    contact_search_height: int = 65  # 搜索区域高度
    contact_search_input_width: int = 170  # 搜索输入框宽度
    contact_search_input_height: int = 30  # 搜索输入框高度
    contact_search_input_left: int = 45  # 搜索输入框左边距
    contact_search_input_bottom: int = 15  # 搜索输入框距离底部
    contact_item_height: int = 70  # 每个好友高度（搜索联系人也是这个高度）

    # 聊天面板参数
    chat_header_height: int = 65  # 头部高度
    chat_input_min_height: int = 118  # 聊天区域最小高度
    chat_toolbar_height: int = 35  # 工具栏高度
    chat_bottom_height: int = 55  # 底部区域高度
    chat_send_width: int = 80  # 发送按钮宽度
    chat_send_height: int = 30  # 发送按钮高度
    chat_send_right: int = 15  # 发送按钮右边距
    chat_send_bottom: int = 15  # 发送按钮底边距

    # 头像边界距离（头像距离消息区域边缘的距离）
    chat_avatar_boundary: int = 10  # 新增：头像边界距离

    # 聊天右键菜单
    chat_right_click_menu_width: int = 163  # 菜单宽度
    chat_right_click_menu_height: int = 340  # 菜单高度
    chat_right_click_item_height: int = 35  # 每个菜单项的高度

    last_msg_bottom_boundary:int = 30 # 最后一条消息距离底部

class WeChatAutomation:
    """微信自动化主类"""

    def __init__(self, ocr_debug: bool = True):
        self.logger = logger
        self.region = WeChatRegion()
        self.wechat_window = None
        self.currentWindowUser = None
        self._paddle_ocr = None  # PaddleOCR实例
        # 平台特定的微信配置
        if IS_WINDOWS:
            self._init_windows_config()
        elif IS_MACOS:
            self._init_macos_config()
        else:
            self.logger.error(f"不支持的操作系统: {platform.system()}")
            sys.exit(1)

        # 创建必要的目录
        self._init_directories()
        # 加载配置
        self._load_region_config()
        # self._init_wechat_window()
        self.exclude_keywords = [
            "公众号", "服务号", "订阅号", "视频号", "微信支付", "文件传输助手",
            "微信团队", "腾讯新闻", "企业微信", "微信运动", "小程序", "游戏", "腾讯新闻","客户群","行业资讯"
        ]
        self._init_ocr_engine()

        # 初始化防检测组件
        self.hardware_sim = HardwareSimulator()
        self.behavior_sim = BehaviorSimulator()
        self.anti_detection = AntiDetection()

        # 行为模式
        self.current_behavior_mode = 'natural'

        self.auto_process_running = False

    def _init_ocr_engine(self):
        """
        初始化PaddleOCR引擎
        """
        try:
            # 尝试导入PaddleOCR
            self.logger.info("正在初始化PaddleOCR引擎...")
            # 设置关键的环境变量，解决兼容性问题
            os.environ['FLAGS_use_onednn'] = '0'
            os.environ['PADDLE_NEW_IR'] = 'OFF'
            os.environ['USE_PDEXP'] = '0'  # 禁用新执行器

            # 初始化PaddleOCR（只执行一次）
            self._paddle_ocr = PaddleOCR(
                lang='ch',  # 使用中文模型
                use_angle_cls=False,
            )
            os.environ['FLAGS_use_onednn'] = '0'
            # 预加载模型（通过测试识别）
            self.logger.info("预加载OCR模型...")
            # 简单测试
            try:
                import numpy as np
                test_img = np.ones((50, 200, 3), dtype=np.uint8) * 255
                # 使用最小参数调用
                result = self._paddle_ocr.ocr(test_img, cls=False, det=True, rec=True)
                if result is not None:
                    self.logger.info("OCR引擎测试通过")
                else:
                    self.logger.warning("OCR引擎返回空结果，但仍可尝试使用")
            except Exception as test_error:
                self.logger.warning(f"OCR引擎测试失败，但可能仍可使用: {test_error}")
        except Exception as e:
            self.logger.error(f"OCR引擎初始化失败: {e}")

    def _init_wechat_window(self) -> bool:
        """初始化微信窗口"""
        try:
            # 查找微信窗口
            wechat_window = auto.WindowControl(
                Name="WXWork",
                ProcessName="WXWork"
            )
            if wechat_window.Exists():
                self.wechat_window = wechat_window
                self.logger.info("成功定位微信窗口")
                return True

            # 尝试其他可能的窗口名称
            wechat_window = auto.WindowControl(
                Name="企业微信",
                ProcessName="WXWork.exe"
            )
            if wechat_window.Exists():
                self.wechat_window = wechat_window
                self.logger.info("成功定位微信窗口（中文名）")
                return True

            wechat_window = auto.WindowControl(
                Name="WXWork",
                ProcessName="WXWork.exe"
            )
            if wechat_window.Exists():
                self.wechat_window = wechat_window
                self.logger.info("成功定位微信窗口（英文名）")
                return True

            self.logger.warning("未找到微信窗口元素")
            return False

        except Exception as e:
            self.logger.error(f"定位微信窗口元素失败: {e}")
            return False
    def _init_windows_config(self):
        """Windows配置初始化"""
        self.wechat_paths = [
            r"C:\Program Files (x86)\WXWork\WXWork.exe",
            r"C:\Program Files\WXWork\WXWork.exe",
            r"C:\Program Files\Tencent\WXWork\WXWork.exe",
            os.path.expanduser(r"~\AppData\Local\WXWork\WXWork.exe"),
            os.path.expanduser(r"~\AppData\Local\WXWork\update\WXWork.exe"),
            os.path.expanduser(r"~\AppData\Local\Weixin\update\Weixin.exe"),
        ]
        self.wechat_process_names = ['WXWork.exe', 'wxWork.exe', 'WxWork.exe']
        self.wechat_window_titles = ['企业微信', 'WXWork']

    def _init_macos_config(self):
        """macOS配置初始化"""
        self.wechat_paths = [
            "/Applications/WXWork.app",
            "/Applications/企业微信.app",
            os.path.expanduser("~/Applications/WXWork.app"),
            os.path.expanduser("~/Applications/企业微信.app"),
        ]
        self.wechat_process_names = ['WXWork', '企业微信']
        self.wechat_window_titles = ['WXWork', '企业微信']

    def _init_directories(self):
        """初始化必要的目录"""
        Path("config").mkdir(exist_ok=True)
        # Path("logs").mkdir(exist_ok=True)
        # Path("data").mkdir(exist_ok=True)
        # Path("debug").mkdir(exist_ok=True)

    def is_wechat_running(self) -> bool:
        """检查微信是否在运行"""
        try:
            if IS_WINDOWS:
                import psutil
                for proc in psutil.process_iter(['name']):
                    try:
                        proc_name = proc.info['name']
                        if proc_name and proc_name.lower() in [name.lower() for name in self.wechat_process_names]:
                            return True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

            elif IS_MACOS:
                # macOS检查进程
                workspace = NSWorkspace.sharedWorkspace()
                running_apps = workspace.runningApplications()
                for app in running_apps:
                    if app.localizedName() in self.wechat_process_names:
                        return True

            return False
        except Exception as e:
            self.logger.error(f"检查微信进程失败: {e}")
            return False

    def find_wechat_exe(self) -> Optional[str]:
        """查找微信可执行文件"""
        for path in self.wechat_paths:
            if os.path.exists(path):
                self.logger.info(f"找到微信: {path}")
                return path

        # 尝试在PATH中查找
        if IS_WINDOWS:
            try:
                result = subprocess.run(['where', 'WXWork.exe'],
                                        capture_output=True, text=True, encoding='gbk',
                                        creationflags=subprocess.CREATE_NO_WINDOW)
                if result.stdout:
                    paths = result.stdout.strip().split('\n')
                    for path in paths:
                        if os.path.exists(path):
                            self.logger.info(f"从PATH找到微信: {path}")
                            return path
            except:
                pass

        self.logger.error("未找到微信安装路径")
        return None

    def start_wechat(self) -> bool:
        """启动微信"""
        try:
            wechat_path = self.find_wechat_exe()
            if not wechat_path:
                self.logger.error("找不到微信安装路径")
                return False

            self.logger.info(f"启动微信: {wechat_path}")

            if IS_WINDOWS:
                # Windows启动
                try:
                    import subprocess
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags = 1
                    startupinfo.wShowWindow = 1
                    CREATE_NO_WINDOW = 0x08000000

                    process = subprocess.Popen(
                        [wechat_path],
                        startupinfo=startupinfo,
                        shell=True,
                        creationflags=CREATE_NO_WINDOW
                    )
                    self.logger.info(f"微信进程已启动，PID: {process.pid}")

                except Exception as e:
                    self.logger.warning(f"标准启动方法失败，使用备用方案: {e}")
                    try:
                        os.startfile(wechat_path)
                        self.logger.info("使用os.startfile启动微信成功")
                    except Exception as e2:
                        self.logger.error(f"所有启动方法都失败: {e2}")
                        return False

            elif IS_MACOS:
                # macOS启动
                self.logger.info("macOS启动微信")
                try:
                    subprocess.run(['open', '-a', 'WXWork'],
                                   capture_output=True, text=True, timeout=10)
                    self.logger.info("使用open命令启动微信")
                except Exception as e:
                    self.logger.warning(f"open命令失败，尝试其他方法: {e}")
                    try:
                        subprocess.run(['open', '-a', '企业微信'],
                                       capture_output=True, text=True, timeout=10)
                        self.logger.info("使用中文名启动微信")
                    except Exception as e2:
                        self.logger.error(f"所有macOS启动方法都失败: {e2}")
                        return False

            # 等待微信启动
            for i in range(30):
                time.sleep(1)
                if self.is_wechat_running():
                    self.logger.info(f"微信已启动 (等待{i + 1}秒)")
                    time.sleep(1)  # 额外等待3秒让窗口完全加载
                    return True

            self.logger.warning("微信启动超时")
            return False

        except Exception as e:
            self.logger.error(f"启动微信失败: {e}")
            return False

    def activate_wechat_window(self, window_title: str = None) -> bool:
        """激活微信窗口"""
        self.logger.info("先激活微信窗口...")

        # 1. 检查微信是否在运行
        if not self.is_wechat_running():
            self.logger.info("微信未运行，尝试启动...")
            self.start_wechat()
            return False

        # 2. 查找并激活微信窗口
        try:
            activated = False
            if IS_WINDOWS:
                activated = self._activate_windows_window(window_title)
            elif IS_MACOS:
                activated = self._activate_macos_window(window_title)
            ## 激活后 如果没有定位，先初始化定位
            if activated and not self.region.sidebar:
                self.locate_regions()
            return activated
        except Exception as e:
            self.logger.error(f"激活微信窗口失败: {e}")
            return False

    def _activate_windows_window(self, window_title: str = None) -> bool:
        """Windows窗口激活"""
        wechat_windows = []

        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                try:
                    title = win32gui.GetWindowText(hwnd)
                    if title:
                        # 检查是否微信窗口
                        is_wechat = any(wechat_title in title for wechat_title in self.wechat_window_titles)
                        if is_wechat:
                            # 检查进程
                            _, pid = win32process.GetWindowThreadProcessId(hwnd)
                            try:
                                import psutil
                                proc = psutil.Process(pid)
                                proc_name = proc.name()
                                if proc_name.lower() in [name.lower() for name in self.wechat_process_names]:
                                    windows.append((hwnd, title, proc_name))
                            except:
                                windows.append((hwnd, title, "未知"))
                except:
                    pass
            return True

        win32gui.EnumWindows(enum_windows_callback, wechat_windows)

        if not wechat_windows:
            self.logger.error("未找到微信窗口")
            return False

        # 选择窗口
        target_window = None
        if window_title:
            for hwnd, title, proc_name in wechat_windows:
                if window_title in title:
                    target_window = (hwnd, title, proc_name)
                    break

        if not target_window:
            # 选择主窗口（通常包含"企业微信"）
            for hwnd, title, proc_name in wechat_windows:
                if '企业微信' in title or 'WXWork' in title:
                    target_window = (hwnd, title, proc_name)
                    break

        if not target_window:
            target_window = wechat_windows[0]

        hwnd, title, proc_name = target_window
        self.logger.info(f"找到微信窗口: {title} (进程: {proc_name})")

        # 激活窗口
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(0.5)

        # 尝试最大化窗口
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            time.sleep(0.5)
        except:
            self.logger.error("微信未登录，请先登录:")
            return False

        # 激活窗口并置顶
        win32gui.SetForegroundWindow(hwnd)

        # 获取窗口位置
        try:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            if left < 0:
                width = right + left
                left = 0
            else:
                width = right - left
            if top < 0:
                height = bottom + top
                top = 0
            else:
                height = bottom - top

            self.region.window_rect = (left, top, width, height)
            self.logger.info(f"微信窗口已激活: 位置({left}, {top}) 大小({width}x{height})")

            # 点击消息图标激活消息面板
            self._click_chat_icon(left, top, width, height)

            return True
        except Exception as e:
            self.logger.error(f"激活窗口失败: {e}")
            return False

    def _click_chat_icon(self, window_left, window_top, window_width, window_height):
        """点击侧边栏的消息图标"""
        try:
            # 计算消息图标位置（侧边栏第一个图标）
            icon_x = window_left + self.region.sidebar_width // 2
            icon_y = window_top + self.region.sidebar_avatar_height + self.region.sidebar_icon_margin + self.region.sidebar_icon_size // 2

            pyautogui.click(icon_x, icon_y)
            self.logger.info(f"已点击消息图标位置: ({icon_x}, {icon_y})")
            time.sleep(1)  # 等待界面响应
            return True
        except Exception as e:
            self.logger.warning(f"点击消息图标失败: {e}")
            return False

    def _activate_macos_window(self, window_title: str = None) -> bool:
        """macOS窗口激活"""
        try:
            from AppKit import NSWorkspace
            import Quartz

            workspace = NSWorkspace.sharedWorkspace()

            # 获取微信应用
            wechat_app = None
            for app in workspace.runningApplications():
                if app.localizedName() in self.wechat_process_names:
                    wechat_app = app
                    break

            if not wechat_app:
                self.logger.error("未找到微信应用")
                return False

            # 激活应用
            wechat_app.activateWithOptions_(NSWorkspace.ActivateIgnoringOtherApps)
            time.sleep(1)

            # 获取窗口列表
            window_list = Quartz.CGWindowListCopyWindowInfo(
                Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements,
                Quartz.kCGNullWindowID
            )

            wechat_window = None
            for window in window_list:
                owner_name = window.get('kCGWindowOwnerName', '')
                window_name = window.get('kCGWindowName', '')

                if owner_name in self.wechat_process_names:
                    if window_title:
                        if window_title in window_name:
                            wechat_window = window
                            break
                    else:
                        if window_name and ('企业微信' in window_name or 'WXWork' in window_name):
                            wechat_window = window
                            break

            if wechat_window:
                # 获取窗口bounds
                bounds = wechat_window.get('kCGWindowBounds', {})
                x = bounds.get('X', 0)
                y = bounds.get('Y', 0)
                width = bounds.get('Width', 1440)
                height = bounds.get('Height', 900)

                self.region.window_rect = (int(x), int(y), int(width), int(height))
                self.logger.info(f"微信窗口: 位置({x}, {y}) 大小({width}x{height})")

                # 点击消息图标
                self._click_chat_icon(x, y, width, height)
                return True
            else:
                self.logger.warning("未能获取窗口信息")
                return False

        except Exception as e:
            self.logger.error(f"macOS窗口激活失败: {e}")
            return False

    def locate_regions(self) -> bool:
        """
        根据精确布局定位微信窗口中的各个区域
        """
        if not self.region.window_rect:
            self.logger.error("请先激活微信窗口")
            return False

        window_left, window_top, window_width, window_height = self.region.window_rect
        self.logger.info("开始根据精确布局定位微信界面区域...")
        self.logger.info(f"窗口位置: 左上({window_left}, {window_top}) 大小({window_width}x{window_height})")

        # ==================== 主要区域划分 ====================

        # 1. 侧边栏区域 (固定宽度60)
        sidebar_left = window_left
        sidebar_right = sidebar_left + self.region.sidebar_width
        sidebar_top = window_top
        sidebar_bottom = window_top + window_height
        sidebar_rect = (sidebar_left, sidebar_top, sidebar_right, sidebar_bottom)
        self.region.sidebar = sidebar_rect

        # 2. 中间联系人面板 (固定最小宽度200)
        contact_left = sidebar_right
        contact_right = contact_left + self.region.contact_panel_min_width
        contact_top = window_top
        contact_bottom = window_top + window_height
        contact_rect = (contact_left, contact_top, contact_right, contact_bottom)
        self.region.contact_panel = contact_rect

        # 3. 右侧聊天面板 (剩余宽度)
        chat_left = contact_right + self.region.split_line_width
        chat_right = window_left + window_width
        chat_top = window_top
        chat_bottom = window_top + window_height
        chat_rect = (chat_left, chat_top, chat_right, chat_bottom)
        self.region.chat_panel = chat_rect

        # ==================== 侧边栏子区域 ====================

        # 4. 侧边栏头像区域 (高度70)
        avatar_left = sidebar_left
        avatar_right = sidebar_right
        avatar_top = sidebar_top
        avatar_bottom = avatar_top + self.region.sidebar_avatar_height
        avatar_rect = (avatar_left, avatar_top, avatar_right, avatar_bottom)
        self.region.sidebar_avatar = avatar_rect

        # 5. 消息图标 (第一个菜单图标)
        chat_icon_left = sidebar_left + (self.region.sidebar_width - self.region.sidebar_icon_size) // 2
        chat_icon_top = avatar_bottom + self.region.sidebar_icon_margin
        chat_icon_right = chat_icon_left + self.region.sidebar_icon_size
        chat_icon_bottom = chat_icon_top + self.region.sidebar_icon_size
        chat_icon_rect = (chat_icon_left, chat_icon_top, chat_icon_right, chat_icon_bottom)
        self.region.sidebar_chat_icon = chat_icon_rect

        # 6. 通讯录图标 (第二个菜单图标)
        contact_icon_top = chat_icon_bottom + self.region.sidebar_icon_margin
        contact_icon_bottom = contact_icon_top + self.region.sidebar_icon_size
        contact_icon_rect = (chat_icon_left, contact_icon_top, chat_icon_right, contact_icon_bottom)
        self.region.sidebar_contact_icon = contact_icon_rect

        # ==================== 联系人面子区域 ====================

        # 7. 联系人搜索区域 (高度70)
        search_area_left = contact_left
        search_area_right = contact_right
        search_area_top = contact_top
        search_area_bottom = search_area_top + self.region.contact_search_height
        search_area_rect = (search_area_left, search_area_top, search_area_right, search_area_bottom)
        self.region.contact_search_area = search_area_rect

        # 8. 搜索输入框 (宽度115，高度30，左边距40，距离底部15)
        search_input_left = search_area_left + self.region.contact_search_input_left
        search_input_right = search_input_left + self.region.contact_search_input_width
        search_input_bottom = search_area_bottom - self.region.contact_search_input_bottom
        search_input_top = search_input_bottom - self.region.contact_search_input_height
        search_input_rect = (search_input_left, search_input_top, search_input_right, search_input_bottom)
        self.region.contact_search_input = search_input_rect

        # 9. 好友列表区域 (搜索区域下方)
        contact_list_left = contact_left
        contact_list_right = contact_right
        contact_list_top = search_area_bottom
        contact_list_bottom = contact_bottom
        contact_list_rect = (contact_list_left, contact_list_top, contact_list_right, contact_list_bottom)
        self.region.contact_list = contact_list_rect

        # ==================== 聊天面板子区域 ====================

        # 10. 聊天头部区域 (高度70)
        chat_header_left = chat_left
        chat_header_right = chat_right
        chat_header_top = chat_top
        chat_header_bottom = chat_header_top + self.region.chat_header_height
        chat_header_rect = (chat_header_left, chat_header_top, chat_header_right, chat_header_bottom)
        self.region.chat_header = chat_header_rect

        # 11. 聊天区域 (最小高度150)
        chat_input_min_top = chat_bottom - self.region.chat_input_min_height
        chat_input_area_left = chat_left
        chat_input_area_right = chat_right
        chat_input_area_top = chat_input_min_top
        chat_input_area_bottom = chat_bottom
        chat_input_area_rect = (chat_input_area_left, chat_input_area_top, chat_input_area_right,
                                chat_input_area_bottom)
        self.region.chat_input_area = chat_input_area_rect

        # 12. 消息记录区域 (头部下方到聊天区域上方)
        chat_messages_left = chat_left
        chat_messages_right = chat_right
        chat_messages_top = chat_header_bottom
        chat_messages_bottom = chat_input_area_top
        chat_messages_rect = (chat_messages_left, chat_messages_top, chat_messages_right, chat_messages_bottom)
        self.region.chat_messages = chat_messages_rect

        # ==================== 聊天区域子区域 ====================

        # 13. 聊天工具栏 (高度45)
        chat_toolbar_left = chat_input_area_left
        chat_toolbar_right = chat_input_area_right
        chat_toolbar_top = chat_input_area_top
        chat_toolbar_bottom = chat_toolbar_top + self.region.chat_toolbar_height
        chat_toolbar_rect = (chat_toolbar_left, chat_toolbar_top, chat_toolbar_right, chat_toolbar_bottom)
        self.region.chat_toolbar = chat_toolbar_rect

        # 14. 聊天输入框 (工具栏下方到底部区域上方)
        chat_input_left = chat_input_area_left
        chat_input_right = chat_input_area_right
        chat_input_top = chat_toolbar_bottom
        chat_input_bottom = chat_input_area_bottom - self.region.chat_bottom_height
        chat_input_rect = (chat_input_left, chat_input_top, chat_input_right, chat_input_bottom)
        self.region.chat_input_box = chat_input_rect

        # 15. 底部区域 (高度45，在聊天区域内靠底)
        chat_bottom_left = chat_input_area_left
        chat_bottom_right = chat_input_area_right
        chat_bottom_bottom = chat_input_area_bottom
        chat_bottom_top = chat_bottom_bottom - self.region.chat_bottom_height
        chat_bottom_rect = (chat_bottom_left, chat_bottom_top, chat_bottom_right, chat_bottom_bottom)
        self.region.chat_bottom_area = chat_bottom_rect

        # 16. 发送按钮 (宽度100，高度30，右边距20，底边距15)
        send_left = chat_bottom_right - self.region.chat_send_right - self.region.chat_send_width
        send_right = send_left + self.region.chat_send_width
        send_bottom = chat_bottom_bottom - self.region.chat_send_bottom
        send_top = send_bottom - self.region.chat_send_height
        send_rect = (send_left, send_top, send_right, send_bottom)
        self.region.chat_send_button = send_rect

        # ==================== 搜索结果区域（关键修改）====================

        # 17. 搜索结果第一个联系人的位置（搜索输入框下方，紧挨着）
        # 搜索浮窗紧挨着搜索输入框，浮窗宽度320，与输入框左对齐
        search_popup_width = 320  # 浮窗宽度

        # 浮窗左边界与搜索输入框左对齐
        search_popup_left = search_input_left

        # 搜索结果第一个联系人：距离浮窗顶部30，高度使用联系人列表中的70
        search_result_first_left = search_popup_left
        search_result_first_right = search_result_first_left + search_popup_width
        search_result_first_top = search_input_bottom + 30  # 紧挨着搜索框下方 + 30像素
        search_result_first_bottom = search_result_first_top + self.region.contact_item_height  # 使用联系人的高度70

        search_result_first_rect = (search_result_first_left, search_result_first_top,
                                    search_result_first_right, search_result_first_bottom)
        self.region.search_result_first = search_result_first_rect

        # 保存区域配置
        self._save_region_config()

        self.logger.info("所有区域定位完成")
        return True

    def _save_region_config(self):
        """保存区域配置到文件"""
        try:
            config = {}
            for field_name in self.region.__dataclass_fields__:
                value = getattr(self.region, field_name)
                if isinstance(value, tuple):
                    config[field_name] = list(value)
                else:
                    config[field_name] = value

            config['timestamp'] = datetime.now().isoformat()
            config['platform'] = platform.system()

            with open("config/wechat_regions.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            self.logger.info("区域配置已保存到 config/wechat_regions.json")

        except Exception as e:
            self.logger.error(f"保存区域配置失败: {e}")

    def _load_region_config(self) -> bool:
        """从文件加载区域配置"""
        try:
            config_file = Path("config/wechat_regions.json")
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # 检查平台是否匹配
                if config.get('platform') != platform.system():
                    self.logger.warning(f"配置来自不同平台({config.get('platform')})，重新定位")
                    return False

                # 更新区域配置
                for key, value in config.items():
                    if hasattr(self.region, key):
                        if isinstance(value, list):
                            setattr(self.region, key, tuple(value))
                        else:
                            setattr(self.region, key, value)

                self.logger.info("区域配置已从文件加载")
                return True
            return False

        except Exception as e:
            self.logger.error(f"加载区域配置失败: {e}")
            return False

    def _safe_click(self, x: int, y: int, click_type: str = 'left',
                    move_duration: float = 0.5, random_offset: int = 5,
                    description: str = "") -> bool:
        """增强的安全点击方法"""
        try:
            if description:
                self.logger.debug(f"安全点击: {description}")

            # 获取当前行为模式配置
            pattern_config = self.anti_detection.get_pattern_config()
            move_duration = self.anti_detection.add_random_variation(move_duration)

            # 使用硬件模拟鼠标移动
            self.hardware_sim.simulate_mouse_move(x, y, move_duration)

            # 添加随机延迟
            click_delay = pattern_config['click_delay']
            time.sleep(self.anti_detection.get_safe_delay(click_delay))

            # 执行点击
            if click_type == 'left':
                import pyautogui
                pyautogui.click(x, y)
            elif click_type == 'double':
                import pyautogui
                pyautogui.doubleClick(x, y)
            elif click_type == 'right':
                import pyautogui
                pyautogui.rightClick(x, y)

            # 记录活动
            self.anti_detection.log_activity('click', {
                'x': x, 'y': y, 'type': click_type,
                'description': description
            })

            # 模拟人类不完美
            self.anti_detection.simulate_human_imperfections()

            return True

        except Exception as e:
            self.logger.error(f"安全点击失败: {e}")
            return False

    def _create_bezier_path(self, start_x: int, start_y: int, end_x: int, end_y: int,
                            num_points: int = 20) -> List[Tuple[int, int]]:
        """
        创建贝塞尔曲线路径，模拟人类鼠标移动
        """
        import random

        # 生成控制点
        control1_x = start_x + (end_x - start_x) * random.uniform(0.2, 0.4)
        control1_y = start_y + (end_y - start_y) * random.uniform(0.2, 0.4)

        control2_x = start_x + (end_x - start_x) * random.uniform(0.6, 0.8)
        control2_y = start_y + (end_y - start_y) * random.uniform(0.6, 0.8)

        points = []
        for i in range(num_points):
            t = i / (num_points - 1)

            # 三次贝塞尔曲线公式
            x = (1 - t) ** 3 * start_x + \
                3 * (1 - t) ** 2 * t * control1_x + \
                3 * (1 - t) * t ** 2 * control2_x + \
                t ** 3 * end_x

            y = (1 - t) ** 3 * start_y + \
                3 * (1 - t) ** 2 * t * control1_y + \
                3 * (1 - t) * t ** 2 * control2_y + \
                t ** 3 * end_y

            # 添加轻微随机抖动
            x += random.randint(-1, 1)
            y += random.randint(-1, 1)

            points.append((int(x), int(y)))

        return points

    def _type_text_safely(self, text: str, delay: float = 0.05):
        """安全输入文本，确保字符能被正确接收"""
        try:
            # 方法1：先尝试直接typewrite
            pyautogui.typewrite(text, interval=delay)
            time.sleep(0.3)

            # 检查是否输入成功（可以通过截图检查）
            # 如果失败，尝试其他方法

            return True
        except Exception as e:
            self.logger.warning(f"直接输入失败: {e}")
            return False

    def _human_like_mouse_move(self, x: int, y: int, behavior_type: str = None):
        """模拟人类鼠标移动"""
        if behavior_type is None:
            behavior_type = self.behavior_sim.get_random_behavior_pattern()

        # 生成人类轨迹
        current_x, current_y = pyautogui.position()
        trajectory = self.behavior_sim.get_mouse_trajectory(
            current_x, current_y, x, y, behavior_type
        )

        # 沿轨迹移动
        for point_x, point_y in trajectory:
            self.hardware_sim.simulate_mouse_move(point_x, point_y, 0.02)

        # 记录活动
        self.anti_detection.log_activity('mouse_move', {
            'from': (current_x, current_y),
            'to': (x, y),
            'trajectory_points': len(trajectory),
            'behavior_type': behavior_type
        })
    def _type_with_clipboard(self, text: str) -> bool:
        """增强的文本输入方法"""
        try:
            # 检查是否需要改变行为模式
            if self.anti_detection.should_change_pattern():
                new_pattern = self.anti_detection.get_next_pattern()
                self.current_behavior_mode = new_pattern

            # 获取当前模式配置
            pattern_config = self.anti_detection.get_pattern_config()

            # 模拟思考时间
            think_time = self.behavior_sim.simulate_thinking_time(len(text))
            self.logger.debug(f"模拟思考时间: {think_time:.2f}秒")

            # 使用行为模拟生成带错别字的文本
            typed_text = self.behavior_sim.simulate_typing_with_errors(
                text,
                pattern=self.current_behavior_mode
            )

            # 使用硬件模拟输入
            typing_speed = pattern_config['typing_speed']
            min_delay = typing_speed * 0.8
            max_delay = typing_speed * 1.2

            self.hardware_sim.simulate_keyboard_input(
                typed_text,
                min_delay=min_delay,
                max_delay=max_delay
            )

            # 记录活动
            self.anti_detection.log_activity('typing', {
                'original_text': text,
                'typed_text': typed_text,
                'length': len(text),
                'pattern': self.current_behavior_mode
            })

            return True

        except Exception as e:
            self.logger.error(f"文本输入失败: {e}")
            return False

    def _split_by_punctuation(self, text: str):
        """按标点符号分割文本"""
        if not text:
            return []

        segments = []
        current_segment = ""

        for char in text:
            current_segment += char
            # 中文标点
            if char in ['，', '。', '！', '？', '；', '：', '、']:
                segments.append(current_segment)
                current_segment = ""
            # 英文标点
            elif char in [',', '.', '!', '?', ';', ':', '/']:
                segments.append(current_segment)
                current_segment = ""
            # 随机分割点（模拟自然打字节奏）
            elif len(current_segment) >= random.randint(3, 8) and random.random() < 0.3:
                segments.append(current_segment)
                current_segment = ""

        if current_segment:
            segments.append(current_segment)

        return segments

    def _introduce_typo(self, text: str) -> str:
        """引入错别字（针对中文）"""
        if len(text) < 2:
            return text

        # 常见拼音易错替换
        common_typos = {
            '的': ['得', '地'],
            '在': ['再'],
            '是': ['时'],
            '和': ['或'],
            '了': ['啦', '咯'],
            '吗': ['嘛'],
            '吧': ['把'],
            '这': ['着'],
            '那': ['哪'],
        }

        # 确定要修改的位置
        pos = random.randint(0, len(text) - 1)
        char_to_replace = text[pos]

        # 如果有常见的易错替换，使用它
        if char_to_replace in common_typos:
            replacements = common_typos[char_to_replace]
            typo_char = random.choice(replacements)
            return text[:pos] + typo_char + text[pos + 1:]

        # 这里简化处理，实际可以集成拼音库
        return text

    def _type_segment_with_backspace(self, typo_text: str, correct_text: str):
        """输入错别字后再修正"""
        # 输入错别字
        pyperclip.copy(typo_text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(random.uniform(0.15, 0.25))

        # 模拟发现错误
        time.sleep(random.uniform(0.2, 0.4))

        # 删除错别字
        for _ in range(len(typo_text)):
            pyautogui.press('backspace')
            time.sleep(random.uniform(0.05, 0.1))

        # 重新输入正确内容
        time.sleep(random.uniform(0.1, 0.2))
        pyperclip.copy(correct_text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(random.uniform(0.1, 0.2))

    def _type_segment_directly(self, text: str):
        """直接输入文本段"""
        if not text:
            return

        # 随机决定是否逐字输入（更真实）
        if random.random() < 0.2 and len(text) <= 5:  # 20%概率逐字输入短文本
            for char in text:
                pyperclip.copy(char)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(random.uniform(0.05, 0.12))
        else:
            # 整段粘贴
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            # 根据长度增加延迟
            segment_delay = min(len(text) * 0.02, 0.5)
            time.sleep(random.uniform(0.1, 0.2) + segment_delay)

    def _simulate_hesitation(self, last_chars: str):
        """模拟犹豫：删除再重新输入"""
        # 删除最后几个字
        for _ in range(len(last_chars)):
            pyautogui.press('backspace')
            time.sleep(random.uniform(0.08, 0.15))

        # 短暂思考
        time.sleep(random.uniform(0.3, 0.6))

        # 重新输入
        pyperclip.copy(last_chars)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(random.uniform(0.15, 0.25))

    def search_and_send_message(self, contact_name: str, message: str = "您好") -> bool:
        """
        搜索联系人并发送消息（整合功能）
        """
        # 检查窗口激活状态
        if not self.activate_wechat_window():
            self.logger.error("无法激活微信窗口，等待60秒后重试")

        self.logger.info(f"开始执行：搜索联系人 '{contact_name}' 并发送消息: '{message}'")

        # 使用公共方法搜索并打开联系人
        if not self._search_and_open_contact(contact_name):
            return False

        try:
            # ========== 输入消息 ==========
            if not self.region.chat_input_box:
                self.logger.error("聊天输入框区域未定位")
                return False

            input_x1, input_y1, input_x2, input_y2 = self.region.chat_input_box
            input_center_x = (input_x1 + input_x2) // 2
            input_center_y = (input_y1 + input_y2) // 2

            self.logger.info(f"1. 安全点击聊天输入框，位置: ({input_center_x}, {input_center_y})")

            # 安全点击输入框
            self._safe_click(input_center_x, input_center_y,
                             move_duration=random.uniform(0.3, 0.5),
                             description="点击聊天输入框")
            time.sleep(0.5)

            # 清空输入框
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.2)

            # 再次安全点击确保焦点
            self._safe_click(input_center_x + random.randint(-1, 1),
                             input_center_y + random.randint(-1, 1),
                             move_duration=random.uniform(0.05, 0.1),
                             description="微调焦点")
            time.sleep(0.3)

            # 输入固定消息 - 优先使用剪贴板
            self.logger.info(f"2. 输入消息: {message}")

            if self._type_with_clipboard(message):
                self.logger.info("使用剪贴板输入消息成功")
            else:
                # 备用：直接输入
                self.logger.info("尝试直接输入消息...")
                for char in message:
                    pyautogui.typewrite(char)
                    time.sleep(0.1)

            time.sleep(0.5)

            if message:
                # 7. 按回车发送
                pyautogui.press('enter')
                self.logger.info("消息已发送")
            # ========== 点击发送按钮 ==========

            # if not self.region.chat_send_button:
            #     self.logger.error("发送按钮区域未定位")
            #     return False
            #
            # send_x1, send_y1, send_x2, send_y2 = self.region.chat_send_button
            # send_center_x = (send_x1 + send_x2) // 2
            # send_center_y = (send_y1 + send_y2) // 2
            #
            # self.logger.info(f"3. 安全点击发送按钮，位置: ({send_center_x}, {send_center_y})")
            #
            # self._safe_click(send_center_x, send_center_y,
            #                  move_duration=random.uniform(0.2, 0.4),
            #                  description="点击发送按钮")

            time.sleep(1.0)
            self.logger.info(f"✅ 消息发送完成！联系人: {contact_name}, 消息: {message}")

            return True
        except Exception as e:
            self.logger.error(f"发送消息失败: {e}")
            return False

    def get_chat_history(self, contact_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取指定联系人的最新聊天记录（只获取对方消息）
        """
        # 检查窗口激活状态
        if not self.activate_wechat_window():
            self.logger.error("无法激活微信窗口，等待60秒后重试")

        # 先搜索并打开该联系人
        result = self._search_and_open_contact(contact_name)
        if not result:
            self.logger.error(f"无法找到联系人: {contact_name}")
            return []

        # 使用上面修改的方法
        # chat_data = self.get_chat_messages_by_elements(contact_name, limit)
        chat_data = self.get_chat_messages_by_copy(contact_name, limit)
        # 确保最后一条消息是用户消息
        chat_data = self._ensure_last_message_is_from_user(contact_name, chat_data)
        # 返回消息列表格式
        return chat_data

    def get_status(self) -> Dict[str, Any]:
        """获取微信状态"""
        return {
            'wechat_running': self.is_wechat_running(),
            'window_rect': self.region.window_rect,
            'regions_loaded': self.region.sidebar is not None,
            'platform': platform.system(),
            'timestamp': datetime.now().isoformat()
        }

    def _search_and_open_contact(self, contact_name: str) -> bool:
        """
        搜索并打开指定联系人（公共方法）
        """
        try:
            if self.currentWindowUser == contact_name:
                return True

            search_x1, search_y1, search_x2, search_y2 = self.region.contact_search_input
            search_center_x = (search_x1 + search_x2) // 2
            search_center_y = (search_y1 + search_y2) // 2

            self.logger.info(f"搜索并打开联系人: {contact_name}")

            # 点击搜索框
            self._safe_click(search_center_x, search_center_y,
                             move_duration=random.uniform(0.3, 0.5),
                             description="点击搜索框")
            time.sleep(0.8)

            # 清空输入框
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.2)

            # 输入联系人名称
            if self._type_with_clipboard(contact_name):
                self.logger.info("使用剪贴板输入联系人成功")
            else:
                for char in contact_name:
                    pyautogui.typewrite(char)
                    time.sleep(0.1)

            time.sleep(0.5)  # 等待搜索结果

            # 点击第一个搜索结果
            if self.region.search_result_first:
                result_x1, result_y1, result_x2, result_y2 = self.region.search_result_first
                result_center_x = (result_x1 + result_x2) // 2 - 30
                result_center_y = (result_y1 + result_y2) // 2

                self._safe_click(result_center_x, result_center_y,
                                 move_duration=random.uniform(0.4, 0.6),
                                 description="点击搜索结果")
            else:
                result_center_x = search_center_x
                result_center_y = search_center_y + 70
                pyautogui.click(result_center_x, result_center_y)

            time.sleep(2)  # 等待聊天界面加载
            self.currentWindowUser = contact_name
            return True

        except Exception as e:
            self.logger.error(f"搜索并打开联系人失败: {e}")
            return False

    def _scroll_to_bottom(self):
        """滚动消息记录区域到底部"""
        try:
            if not self.region.chat_messages:
                return False

            msg_x1, msg_y1, msg_x2, msg_y2 = self.region.chat_messages
            scroll_x = (msg_x1 + msg_x2) // 2
            scroll_y = (msg_y1 + msg_y2) // 2

            self.logger.info("滚动到消息底部...")

            # 点击消息区域确保焦点
            pyautogui.click(scroll_x, scroll_y)
            time.sleep(0.3)

            # 再向下滚动一点确保在最新位置
            for i in range(2):
                pyautogui.scroll(500)
                time.sleep(0.1)

            time.sleep(0.5)
            return True

        except Exception as e:
            self.logger.error(f"滚动到底部失败: {e}")
            return False

    def get_chat_messages_by_elements(self, contact_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        只获取左侧（对方）和右侧（自己）的消息，过滤中间位置
        """
        messages = []

        try:
            self.logger.info(f"获取联系人 [{contact_name}] 的左右侧消息")

            # 2. 查找消息列表
            message_list = auto.ListControl(
                searchDepth=15,
                AutomationId='chat_message_list'
            )

            if not message_list.Exists():
                return messages

            # 3. 获取消息列表的位置信息（用于计算中心位置）
            list_rect = message_list.BoundingRectangle
            if not list_rect:
                return messages

            list_center = (list_rect.left + list_rect.right) / 2

            # 4. 获取所有子项并倒序处理
            children = list(message_list.GetChildren())

            # 5. 倒序处理，只取左右两侧消息
            count = 0

            # 从最新到最旧处理
            for i in range(len(children) - 1, -1, -1):
                if count >= limit:
                    break

                item = children[i]

                try:
                    # 只获取文本消息
                    item_name = getattr(item, 'Name', '')
                    class_name = getattr(item, 'ClassName', '')

                    # 过滤：只取文本消息，跳过时间分隔符
                    if not item_name or not 'ChatTextItemView' in class_name:
                        continue

                    # 获取位置
                    rect = getattr(item, 'BoundingRectangle', None)
                    if not rect:
                        continue

                    # 计算消息中心位置
                    item_center = (rect.left + rect.right) / 2

                    # 简单判断：中心在列表中心左侧就是对方，右侧就是自己
                    from_who = 'me' if item_center > list_center else 'you'

                    # 创建消息对象
                    message = {
                        "content": item_name,
                        "from": from_who,
                        "position": (rect.left, rect.top),
                        "size": f"{rect.width}x{rect.height}",
                        "time": time.strftime("%H:%M:%S"),
                        "timestamp": time.time(),
                        "index": count + 1,
                        "contact": contact_name,
                        "type": "text"
                    }

                    messages.append(message)
                    count += 1

                except:
                    continue

            self.logger.info(
                f"获取到 {len(messages)} 条左右侧消息 (左侧: {sum(1 for m in messages if m['from'] == 'you')}, 右侧: {sum(1 for m in messages if m['from'] == 'me')})")
            return messages

        except Exception as e:
            self.logger.error(f"获取消息失败: {e}")
            return messages
    def get_chat_messages_by_copy(self, contact_name, limit: int = 5) -> List[Dict[str, Any]]:
        """
        通过右键复制获取聊天消息
        1. 先定位所有消息气泡的位置
        2. 从最新的（最底部）开始，依次右键复制
        """
        messages = []

        try:
            # 1. 确保聊天消息区域已定位
            if not self.region.chat_messages:
                self.logger.error("聊天消息区域未定位")
                return messages

            # 获取聊天区域坐标
            msg_x1, msg_y1, msg_x2, msg_y2 = self.region.chat_messages
            region_width = msg_x2 - msg_x1
            region_height = msg_y2 - msg_y1
            self.logger.info(
                f"聊天消息区域: 位置({msg_x1},{msg_y1})-({msg_x2},{msg_y2}) 大小({region_width}x{region_height})")

            # 2. 使用与draw_messages_overlay相同的方法定位消息气泡
            message_rects = self._locate_message_bubbles()

            if not message_rects:
                self.logger.warning("未检测到任何消息气泡")
                return messages

            self.logger.info(f"检测到 {len(message_rects)} 个消息气泡")

            # 3. 按垂直位置排序（从底部到顶部，最新的先处理）
            message_rects.sort(key=lambda rect: rect[1], reverse=True)  # 按y坐标降序

            # 4. 限制处理数量，从最新的开始
            message_rects = message_rects[:limit]

            # 5. 对每个消息气泡执行右键复制
            for i, (x, y, w, h) in enumerate(message_rects):
                try:
                    # 计算消息气泡的中心点（相对坐标）
                    bubble_center_x = x + w // 2
                    bubble_center_y = y + h // 2

                    is_customer_message = (bubble_center_x < region_width * 0.4)
                    if is_customer_message:
                        copy_center_x = x + w - 20
                    else:
                        copy_center_x = x + 20
                    # 右键点击消息气泡中心（稍微偏移，避免点击在边缘）

                    # 转换为绝对屏幕坐标
                    absolute_x = msg_x1 + copy_center_x
                    absolute_y = msg_y1 + bubble_center_y

                    self.logger.info(f"处理消息 {i + 1}: 位置({absolute_x},{absolute_y}) 大小({w}x{h})")
                    click_x = absolute_x
                    click_y = absolute_y
                    pyautogui.moveTo(click_x, click_y, duration=1)
                    # 获取光标信息 如果是光标 则右键
                    cursor_info = win32gui.GetCursorInfo()
                    # 根据常见光标ID判断形状
                    if cursor_info:
                        cursor_id = cursor_info[1]
                        if cursor_id != 65541:
                            self.logger.info(f"非 I型/输入，不可点击复制:{cursor_id}")
                            continue
                    pyautogui.click(click_x, click_y, button='right')
                    time.sleep(0.5)  # 等待右键菜单弹出，给足时间

                    # 获取复制菜单位置
                    copy_click_x, copy_click_y = self.get_copy_menu_position(click_x, click_y)

                    self.logger.debug(f"复制菜单位置: ({copy_click_x}, {copy_click_y})")

                    # 点击"复制"选项
                    pyautogui.click(copy_click_x, copy_click_y)
                    time.sleep(0.3)  # 等待复制完成

                    # 读取剪贴板内容
                    try:
                        clipboard_content = pyperclip.paste().strip()
                        if clipboard_content and len(clipboard_content) > 0:
                            # 判断消息方向（左侧是对方消息，右侧是自己消息）
                            is_right_side = bubble_center_x > (region_width // 2)

                            message = {
                                "content": clipboard_content,
                                "role": "assistant" if is_right_side else "user",  # 右侧是自己(assistant)，左侧是客户(user)
                                "position": (absolute_x, absolute_y),
                                "size": f"{w}x{h}",
                                "time": time.strftime("%H:%M:%S"),
                                "timestamp": time.time(),
                                "index": i + 1,
                                "contact": contact_name,
                                "type": "text"
                            }
                            messages.append(message)

                            self.logger.debug(f"复制到消息 {i + 1}: {clipboard_content[:50]}...")
                        else:
                            self.logger.debug(f"消息 {i + 1}: 剪贴板内容为空")
                    except Exception as clip_error:
                        self.logger.debug(f"读取剪贴板失败: {clip_error}")

                    # 点击其他位置关闭右键菜单（点击原始消息位置左上方）
                    close_x = max(click_x - 50, 10)
                    close_y = max(click_y - 50, 10)
                    pyautogui.click(close_x, close_y)
                    time.sleep(0.2)

                except Exception as e:
                    self.logger.error(f"处理消息 {i + 1} 失败: {e}")
                    # 如果失败，尝试ESC键关闭菜单
                    try:
                        pyautogui.press('esc')
                        time.sleep(0.2)
                    except:
                        pass
                    continue

            self.logger.info(f"成功获取 {len(messages)} 条消息")
            # 消息在顺序
            messages.reverse()
            return messages

        except Exception as e:
            self.logger.error(f"通过复制获取消息失败: {e}")
            return messages

    def get_copy_menu_position(self, click_x: int, click_y: int) -> tuple[int, int]:
        """
        计算右键菜单中"复制"选项的点击位置
        """
        window_left, window_top, window_width, window_height = self.region.window_rect

        # 右键菜单的基本属性
        menu_width = self.region.chat_right_click_menu_width  # 菜单宽度
        menu_height = self.region.chat_right_click_menu_height  # 菜单高度
        item_height = self.region.chat_right_click_item_height  # 每个菜单项的高度

        # 复制按钮通常是第一个菜单项
        copy_item_offset_y = item_height // 2  # 点击第一个菜单项的中心位置

        # 初始菜单位置（菜单在鼠标右下方显示）
        # 注意：右键菜单的左上角位于鼠标点击位置的右下边缘
        menu_x = click_x
        menu_y = click_y

        # 检查是否需要调整菜单位置（避免超出屏幕边界）
        # 如果菜单会超出屏幕右边界，则左移菜单
        if menu_x + menu_width > window_width:
            menu_x = window_width - menu_width

        # 如果菜单会超出屏幕下边界，则上移菜单(企业微信可以超过窗口，但不能超过屏幕)
        screen_width, screen_height = pyautogui.size()
        if menu_y + menu_height > screen_height:
            menu_y = screen_height - menu_height

        # if menu_y + menu_height > window_height:
        #     menu_y = window_height - menu_height

        # 计算复制按钮的点击位置（第一个菜单项的中心）
        copy_click_x = menu_x + menu_width // 2  # 菜单水平中心
        copy_click_y = menu_y + copy_item_offset_y  # 第一个菜单项垂直中心

        return copy_click_x, copy_click_y

    def _locate_message_bubbles(self) -> List[Dict[str, Any]]:
        """
        定位聊天消息气泡（复用draw_messages_overlay中的逻辑）
        返回: [(x, y, w, h), ...] 相对于聊天区域的坐标
        """
        message_rects = []
        try:

            # 1. 检查聊天消息区域是否已定位
            if not self.region.chat_messages:
                return message_rects

            # 2. 获取聊天区域坐标
            msg_x1, msg_y1, msg_x2, msg_y2 = self.region.chat_messages
            width = msg_x2 - msg_x1
            height = msg_y2 - msg_y1

            logger.info(f"聊天消息区域: 位置({msg_x1},{msg_y1})-({msg_x2},{msg_y2}) 大小({width}x{height})")

            # 3. 截取聊天区域
            logger.info("截取聊天区域...")
            time.sleep(0.5)

            screenshot = ImageGrab.grab(bbox=(msg_x1, msg_y1, msg_x2, msg_y2))
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            # 转换为numpy数组用于识别
            covered_array = np.array(screenshot.convert('RGB'))  # 转回RGB处理

            # 4. 获取背景色（采样左上角区域）
            logger.info("采样背景色...")
            # 采样左上角5x5区域
            sample_region = covered_array[0:5, 0:5]

            # 计算平均颜色
            background_color = np.mean(sample_region, axis=(0, 1)).astype(int)
            logger.info(f"检测到的背景色: R={background_color[0]}, G={background_color[1]}, B={background_color[2]}")

            # 5. 创建背景掩码（找到背景色区域）
            logger.info("创建背景掩码...")
            # 定义颜色容差
            tolerance = 15  # 颜色容差范围
            # 计算每个像素与背景色的差异
            diff = np.abs(covered_array - background_color)
            # 创建掩码：如果三个通道都在容差范围内，则为背景
            background_mask = np.all(diff <= tolerance, axis=2)

            # logger.info("去除水印...")
            # cleaned_array = self.remove_slanted_watermark_morphology(covered_array)

            # 6. 去除背景色：将背景变为黑色
            logger.info("去除背景色...")
            # 创建去除背景的图像
            background_removed = covered_array.copy()
            # 将背景区域设为黑色
            background_removed[background_mask] = [0, 0, 0]

            # 5. 第二步：使用原有的识别方法在覆盖后的图片上识别
            logger.info("在颜色覆盖的图像上识别气泡和头像...")

            # 检测头像和消息（在覆盖后的图片上）
            gray = cv2.cvtColor(background_removed, cv2.COLOR_RGB2GRAY)
            # 对非背景区域进行对比度增强
            # 使用CLAHE（限制对比度自适应直方图均衡化）
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)

            # debug时开启
            # img = Image.fromarray(enhanced)
            # timestamp = time.strftime("%Y%m%d_%H%M%S")
            # temp_path = f"debug/message_chat_{timestamp}.png"
            # img.save(temp_path)

            # 9. 使用固定阈值二值化（因为气泡白色，背景黑色，对比度极高）
            _, binary = cv2.threshold(enhanced, 50, 255, cv2.THRESH_BINARY)

            # 10. 形态学操作：先腐蚀再膨胀，去除噪点但保留气泡主体
            kernel = np.ones((3, 3), np.uint8)
            # 先轻微腐蚀去除孤立小点
            eroded = cv2.erode(binary, kernel, iterations=1)
            # 再膨胀恢复气泡大小
            dilated = cv2.dilate(eroded, kernel, iterations=2)

            # 11. 查找轮廓
            contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 查找轮廓
            # contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            logger.info(f"找到 {len(contours)} 个轮廓")
            # 方法1：使用层级关系过滤
            contours = self._filter_contours_by_hierarchy(contours, hierarchy, width)

            logger.info(f"过滤之后还有 {len(contours)} 个轮廓")

            # 分析轮廓
            for i, contour in enumerate(contours):
                x, y, w, h = cv2.boundingRect(contour)
                message_rects.append((x, y, w, h))

            logger.info(f"检测到{len(message_rects)} 条消息")
            return message_rects
        except Exception as e:
            logger.error(f"检测消息失败: {e}")
            return []

    def remove_slanted_watermark_morphology(self, img_array):
        # 转换为灰度图用于分析
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # 1. 使用Sobel算子检测边缘（水印文字通常是倾斜的连续边缘）
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        # 计算梯度幅度和方向
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        angle = np.arctan2(sobely, sobelx) * 180 / np.pi

        # 2. 创建水印掩码
        watermark_mask = np.zeros_like(gray, dtype=np.uint8)

        # 企业微信水印通常是45度或135度倾斜
        # 检测这个方向的边缘
        angle_mask1 = (angle > 40) & (angle < 50)  # 45度左右
        angle_mask2 = (angle > -50) & (angle < -40)  # -45度左右
        angle_mask = angle_mask1 | angle_mask2

        # 结合梯度幅度（水印通常有中等强度的边缘）
        magnitude_norm = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        magnitude_mask = (magnitude_norm > 30) & (magnitude_norm < 200)

        # 组合掩码
        combined_mask = (angle_mask & magnitude_mask).astype(np.uint8) * 255

        # 形态学操作连接断开的边缘
        kernel = np.ones((3, 3), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        combined_mask = cv2.dilate(combined_mask, kernel, iterations=1)

        # 3. 使用inpaint修复水印区域
        result = cv2.inpaint(img_array, combined_mask, 3, cv2.INPAINT_TELEA)

        return result

    def _filter_contours_by_hierarchy(self, contours, hierarchy, width):
        """
        使用头像边界过滤轮廓
        """
        if hierarchy is None:
            return []

        hierarchy = hierarchy[0]
        filtered_contours = []
        avatar_boundary = self.region.chat_avatar_boundary

        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)

            # 要求1：过滤掉高度小于30的
            if h < 30 or w<30:
                continue

            # 要求2：使用头像边界过滤 - 不在头像区域内
            aspect_ratio = w / h if h > 0 else 0
            # 左侧头像区域：x < 头像边界
            is_in_left_avatar_area = (x < avatar_boundary) and (0.8 <= aspect_ratio <= 1.2)
            # 右侧头像区域：x + w > width - 头像边界
            is_in_right_avatar_area =  (x + w > width - avatar_boundary) and (0.8 <= aspect_ratio <= 1.2)

            if is_in_left_avatar_area or is_in_right_avatar_area:
                logger.debug(f"过滤头像区域内的轮廓: 位置({x},{y}) 大小({w}x{h})")
                continue

            # 要求3：保留所有不在头像区域内的轮廓（不再检查宽高比）
            filtered_contours.append(contour)

        return filtered_contours

    def _click_and_valid_contact_by_index(self, index: int) -> bool:
        """
        点击联系人列表中指定索引位置的联系人

        Args:
            index: 联系人索引（从0开始）
        Returns:
            bool: 是否成功点击
        """
        try:
            if not self.region.contact_list:
                self.logger.error("联系人列表区域未定位")
                return False
            # if contact_list.__contains__(_get_current_contact()) :
            #     self.logger.warning("当前联系人不在指定范围内")
            #     return False
            # 获取联系人列表区域

            contact_x1, contact_y1, contact_x2, contact_y2 = self.region.contact_list

            # 每个联系人的高度
            item_height = self.region.contact_item_height

            # 计算点击位置
            # 第一个联系人的点击位置（中心偏下一点，避免点击到边界）
            base_y = contact_y1 + item_height // 2

            # 计算当前索引的点击位置
            click_x = (contact_x1 + contact_x2) // 2
            click_y = base_y + (index * item_height)

            # 确保点击位置在联系人列表区域内
            if click_y > contact_y2 - 10:
                self.logger.warning(f"索引 {index} 超出联系人列表范围")
                # 如果超出范围，点击最后一个可见位置
                return False
            self.logger.info(f"点击联系人列表第 {index + 1} 个位置: ({click_x}, {click_y})")

            # 安全点击
            self._safe_click(click_x, click_y,
                             move_duration=random.uniform(0.3, 0.5),
                             description=f"点击列表第{index + 1}个联系人")

            time.sleep(1)  # 等待聊天界面加载

            return True

        except Exception as e:
            self.logger.error(f"点击列表联系人失败: {e}")
            return False

    def _get_session_list(self):
        """
        获取会话列表控件
        AutomationId: "session_list"
        ClassName: "mmui::XTableView"
        Name: "会话"
        """
        try:
            session_list = auto.ListControl(
                searchDepth=20,
                AutomationId='session_list'
            )

            if session_list and session_list.Exists():
                self.logger.info("找到会话列表控件")
                return session_list

            # 方法3：使用名称查找
            session_list = auto.ListControl(
                searchDepth=20,
                Name='会话'
            )
            if session_list.Exists(2, 0.5):
                self.logger.info("通过Name找到会话列表")
                return session_list
            return None
        except Exception as e:
            self.logger.error(f"获取会话列表失败: {e}")
            return None

    def _get_session_items(self, session_list):
        """
        获取会话列表中的所有项
        """
        try:
            items = list(session_list.GetChildren())
            return items
        except Exception as e:
            self.logger.error(f"获取会话项失败: {e}")
            return []

    def auto_process_contacts(self, contact_list: List[str], max_polling_times: int = 5,
                              api_url: str = "http://localhost:8000/api/chat/completions",
                              api_key: str = "",
                              model: str = "",
                              wait_time: int = 300) -> None:
        return self.auto_process_by_window_copy(contact_list,max_polling_times,api_url,api_key,model,wait_time)
        # return self.auto_process_by_param(contact_list, max_polling_times, api_url, api_key,model,wait_time)

    def auto_process_by_window_copy(self, contact_list: List[str], max_polling_times: int = 5,
                              api_url: str = "http://localhost:8000/api/chat/completions",
                              api_key: str = "",
                              model:str = "",
                              wait_time: int = 300):
        """
                自动处理联系人，轮询检查新消息并自动回复

                Args:
                    max_polling_times: 最大轮询次数（点击联系人的次数）
                    api_url: AI聊天接口URL
                """
        # 确保微信窗口已激活
        if not self.activate_wechat_window():
            self.logger.error("无法激活微信窗口，等待60秒后重试")
            return

        # 记录处理轮次
        round_count = 0
        self.auto_process_running = True  # 设置运行标志
        while True:
            round_count += 1
            self.logger.info(f"=== 开始第 {round_count} 轮处理 ===")

            if not self.auto_process_running:
                break
            #先尝试点击第二个联系人
            self._click_and_valid_contact_by_index(1)
            try:
                # 从索引0开始循环点击联系人
                for i in range(max_polling_times):
                    try:
                        self.logger.info(f"处理第 {i + 1}/{max_polling_times} 个联系人")

                        # 点击指定索引的联系人
                        # current_chat_name = "江海涛"
                        if not self._click_and_valid_contact_by_index(i):
                            continue
                        time.sleep(0.5)  # 等待聊天界面加载
                        # 获取当前聊天窗口的名称
                        current_chat_name = self.get_chat_header_name()
                        if not current_chat_name:
                            self.logger.warning("无法识别聊天窗口名称，跳过")
                            continue
                        if '@微信' in current_chat_name:
                            at_index = current_chat_name.find('@微信')
                            # 截取 @微信 前面的部分，并去除多余空格
                            current_chat_name = current_chat_name[:at_index].strip()
                        else:
                            self.logger.warning("不是好友客户")
                            continue

                        self.logger.info(f"当前聊天窗口名称: {current_chat_name}")

                        # 检查是否为特殊聊天窗口
                        if current_chat_name in self.exclude_keywords:
                            continue
                        # 检查当前窗口是否在目标联系人列表中
                        if  contact_list and len(contact_list)>0 and current_chat_name not in contact_list:
                            self.logger.info(f"当前窗口 '{current_chat_name}' 不在目标联系人列表中，跳过")
                            continue
                        # 检查是否有新消息
                        chat_data = self.get_chat_messages_by_copy(current_chat_name)
                        # 确保最后一条消息是用户消息
                        chat_data = self._ensure_last_message_is_from_user(current_chat_name, chat_data)
                        # 无论消息是否为空 都调用AI接口获取回复
                        ai_replies = self._call_ai_api(current_chat_name, chat_data, api_url, api_key,model)

                        if ai_replies:
                            self.logger.info(f"收到 {len(ai_replies)} 条AI回复")

                            # 发送多条回复
                            for reply_msg in ai_replies:
                                content = reply_msg.get('content', '').strip()
                                pause_ms = reply_msg.get('pause_ms', 500)

                                if content:
                                    self.logger.info(
                                        f"发送回复: {content[:50]}... (间隔: {pause_ms}ms)")

                                    # 发送消息
                                    success = self._send_message_directly(content)
                                    if success:
                                        self.logger.info(f"回复发送成功，等待 {pause_ms}ms")
                                        time.sleep(pause_ms / 1000.0)
                                    else:
                                        self.logger.error("回复发送失败")
                                        time.sleep(1)
                                else:
                                    self.logger.warning("跳过空内容回复")
                        else:
                            self.logger.warning("AI接口返回空回复")

                        # 短暂等待，准备处理下一个
                        time.sleep(1)

                    except Exception as contact_error:
                        self.logger.error(f"处理联系人时出错: {contact_error}")
                        time.sleep(3)
                        continue

                # 完成一轮处理，等待5分钟
                self.logger.info(f"=== 第 {round_count} 轮处理完成，等待5分钟后继续 ===")
                time.sleep(wait_time)  # 5分钟

            except Exception as e:
                self.logger.error(f"自动处理异常: {e}")
                time.sleep(60)  # 等待1分钟后重试

    def _ensure_last_message_is_from_user(self, contact_name: str, chat_data: List[Dict]) -> List[Dict]:
        """
        确保最后一条消息是用户（对方）的消息
        如果不是，尝试右键拷贝最后一条消息并添加到chat_data

        Args:
            contact_name: 联系人名称
            chat_data: 已有的聊天数据

        Returns:
            更新后的聊天数据
        """
        if not chat_data:
            return chat_data

        # 检查最后一条消息是否是用户（对方）的消息
        last_message = chat_data[-1]
        if last_message.get('role') == 'user':
            self.logger.debug("最后一条消息已经是用户消息，无需处理")
            return chat_data

        self.logger.info("最后一条消息不是用户消息，尝试右键拷贝最新消息")

        # 尝试右键拷贝最后一条消息的位置
        success = self._right_click_copy_last_message()
        if not success:
            self.logger.warning("右键拷贝最后一条消息失败")
            return chat_data

        time.sleep(0.5)

        # 读取剪贴板内容
        try:
            clipboard_content = pyperclip.paste().strip()
            if clipboard_content:
                # 创建新的消息对象
                new_message = {
                    "content": clipboard_content,
                    "role": "user",  # 对方（客户）的消息使用user角色
                    "time": time.strftime("%H:%M:%S"),
                    "timestamp": time.time(),
                    "index": len(chat_data) + 1,
                    "contact": contact_name,
                    "type": "text",
                    "source": "right_click_copy"
                }

                # 添加到chat_data末尾
                chat_data.append(new_message)
                self.logger.info(f"成功添加最后一条用户消息: {clipboard_content[:50]}...")
            else:
                self.logger.warning("剪贴板内容为空")
        except Exception as e:
            self.logger.error(f"读取剪贴板内容失败: {e}")

        return chat_data

    def _right_click_copy_last_message(self) -> bool:
        """
        右键点击并拷贝最后一条消息

        消息位置：底部距离边框25，左边距离头像右边缘15

        Returns:
            bool: 是否成功
        """
        try:
            if not self.region.chat_messages:
                self.logger.error("聊天消息区域未定位")
                return False

            # 获取聊天区域坐标
            msg_x1, msg_y1, msg_x2, msg_y2 = self.region.chat_messages
            region_width = msg_x2 - msg_x1
            region_height = msg_y2 - msg_y1

            # 计算点击位置：
            # 底部距离边框25像素
            # 左边距离头像右边缘15像素（头像边界+15）
            avatar_boundary = self.region.chat_avatar_boundary
            last_msg_bottom_boundary = self.region.last_msg_bottom_boundary
            click_x = msg_x1 + avatar_boundary + 20 + 10  # 头像右边缘+15像素
            click_y = msg_y2 - last_msg_bottom_boundary - 10  # 底部向上25像素

            self.logger.debug(f"右键点击位置: ({click_x}, {click_y})")

            # 右键点击
            pyautogui.moveTo(click_x, click_y, duration=0.5)
            time.sleep(0.2)
            pyautogui.click(button='right')
            time.sleep(0.5)  # 等待右键菜单弹出

            # 获取复制菜单位置并点击
            copy_click_x, copy_click_y = self.get_copy_menu_position(click_x, click_y)
            pyautogui.click(copy_click_x, copy_click_y)
            time.sleep(0.3)

            return True

        except Exception as e:
            self.logger.error(f"右键拷贝最后一条消息失败: {e}")
            return False
    def auto_process_by_param(self, contact_list: List[str], max_polling_times: int = 5,
                              api_url: str = "http://localhost:8000/api/chat/completions",
                              api_key: str = "",
                              model: str = "",
                              wait_time: int = 300) -> None:
        """
        自动处理联系人，轮询检查新消息并自动回复

        Args:
            max_polling_times: 最大轮询次数（点击联系人的次数）
            api_url: AI聊天接口URL
        """
        # 确保微信窗口已激活
        if not self.activate_wechat_window():
            self.logger.error("无法激活微信窗口，等待60秒后重试")
            return

        # 记录处理轮次
        round_count = 0

        try:
            while True:
                round_count += 1
                self.logger.info(f"=== 开始第 {round_count} 轮处理 ===")

                try:
                    # 获取会话列表
                    session_list = self._get_session_list()
                    if not session_list:
                        self.logger.error("无法获取会话列表")
                        time.sleep(60)
                        continue

                    # 获取所有会话项
                    session_items = self._get_session_items(session_list)
                    if not session_items:
                        self.logger.warning("没有找到任何会话")
                        time.sleep(60)
                        continue

                    self.logger.info(f"找到 {len(session_items)} 个会话")

                    # 处理前N个会话（限制数量）
                    for i in range(min(max_polling_times, len(session_items))):
                        try:
                            item = session_items[i]
                            item_name = getattr(item, 'Name', '')

                            if not item_name:
                                continue

                            # 从Name中提取联系人名字（第一行）
                            automation_id = getattr(item, 'AutomationId', '')
                            contact_name = item_name
                            if automation_id and automation_id.startswith('session_item_'):
                                # AutomationId格式: "session_item_xxx"
                                contact_name = automation_id.replace('session_item_', '')

                            self.logger.info(f"处理第 {i + 1}/{max_polling_times} 个联系人: {contact_name}")
                            if contact_name in self.exclude_keywords and not contact_name in contact_list:
                                logger.info(f"当前联系人被过滤:{contact_name}")
                                continue

                            # 检查是否需要点击进入（如果当前不是这个联系人）
                            if self.currentWindowUser != contact_name:
                                # 点击联系人进入聊天
                                self.logger.info(f"点击进入联系人: {contact_name}")
                                rect = getattr(item, 'BoundingRectangle', None)
                                if rect:
                                    center_x = (rect.left + rect.right) // 2
                                    center_y = (rect.top + rect.bottom) // 2
                                    self._safe_click(center_x, center_y, description=f"点击联系人: {contact_name}")
                                    time.sleep(2)  # 等待聊天界面加载
                                    self.currentWindowUser = contact_name
                            chat_data = self.get_chat_messages_by_elements(contact_name)

                            # 无论消息是否为空 都调用AI接口获取回复
                            ai_replies = self._call_ai_api(contact_name,chat_data, api_url, api_key,model)

                            if ai_replies:
                                self.logger.info(f"收到 {len(ai_replies)} 条AI回复")

                                # 发送多条回复
                                for reply_msg in ai_replies:
                                    content = reply_msg.get('content', '').strip()
                                    pause_ms = reply_msg.get('pause_ms', 500)

                                    if content:
                                        self.logger.info(
                                            f"发送回复: {content[:50]}... (间隔: {pause_ms}ms)")

                                        # 发送消息
                                        success = self._send_message_directly(content)
                                        if success:
                                            self.logger.info(f"回复发送成功，等待 {pause_ms}ms")
                                            time.sleep(pause_ms / 1000.0)
                                        else:
                                            self.logger.error("回复发送失败")
                                            time.sleep(1)
                                    else:
                                        self.logger.warning("跳过空内容回复")
                            else:
                                self.logger.warning("AI接口返回空回复")

                            # 短暂等待，准备处理下一个
                            time.sleep(1)

                        except Exception as contact_error:
                            self.logger.error(f"处理联系人时出错: {contact_error}")
                            time.sleep(3)
                            continue

                    # 完成一轮处理，等待5分钟
                    self.logger.info(f"=== 第 {round_count} 轮处理完成，等待5分钟后继续 ===")
                    time.sleep(wait_time)

                except Exception as e:
                    self.logger.error(f"自动处理异常: {e}")
                    time.sleep(60)

        except KeyboardInterrupt:
            self.logger.info("自动处理被用户中断")

    def _check_new_message_by_elements(self):
        """
        检查是否有新消息（对方发送的）
        """
        try:
            # 获取消息列表
            message_list = auto.ListControl(
                searchDepth=15,
                AutomationId='chat_message_list'
            )

            if not message_list.Exists():
                self.logger.warning("找不到消息列表")
                return False

            # 获取列表位置
            list_rect = message_list.BoundingRectangle
            if not list_rect:
                self.logger.warning("无法获取消息列表位置")
                return False

            list_center = (list_rect.left + list_rect.right) / 2

            # 获取所有消息项
            children = list(message_list.GetChildren())
            if not children:
                self.logger.warning("消息列表为空")
                return False

            # 调试：打印所有消息项信息
            self.logger.info(f"消息列表有 {len(children)} 个项")
            for i, item in enumerate(children[-5:]):  # 只打印最后5条
                try:
                    name = getattr(item, 'Name', '')
                    class_name = getattr(item, 'ClassName', '')
                    rect = getattr(item, 'BoundingRectangle', None)
                    if rect:
                        center = (rect.left + rect.right) / 2
                        self.logger.info(f"最后{i+1}条: {name[:20]}... (类: {class_name}, 中心: {center:.0f}, 列表中心: {list_center:.0f})")
                except:
                    pass

            # 过滤文本消息
            text_items = []
            for item in children:
                try:
                    class_name = getattr(item, 'ClassName', '')
                    name = getattr(item, 'Name', '')

                    # 只取文本消息
                    if name and 'ChatTextItemView' in class_name:
                        text_items.append(item)
                except:
                    continue

            if not text_items:
                self.logger.warning("没有文本消息")
                return False

            self.logger.debug(f"找到 {len(text_items)} 条文本消息")

            # 取最后一条文本消息
            last_item = text_items[-1]

            # 获取消息位置
            item_rect = getattr(last_item, 'BoundingRectangle', None)
            if not item_rect:
                self.logger.warning("无法获取消息位置")
                return False

            item_center = (item_rect.left + item_rect.right) / 2
            item_name = getattr(last_item, 'Name', '')

            # 判断方向
            is_customer_message = item_center < list_center

            self.logger.debug(f"最后一条文本消息: {item_name[:30]}...")
            self.logger.debug(f"消息中心: {item_center:.0f}, 列表中心: {list_center:.0f}")
            self.logger.debug(f"是否是对方消息: {is_customer_message}")

            return is_customer_message

        except Exception as e:
            self.logger.error(f"检查新消息失败: {e}")
            return False

    def _get_latest_customer_messages(self, limit: int = 3) -> List[str]:
        """
        最简洁版本：获取最新的客户消息
        """
        try:
            message_list = auto.ListControl(
                searchDepth=15,
                AutomationId='chat_message_list'
            )

            if not message_list.Exists():
                return []

            list_rect = message_list.BoundingRectangle
            if not list_rect:
                return []

            list_center = (list_rect.left + list_rect.right) / 2
            customer_messages = []

            # 倒序遍历
            for item in reversed(list(message_list.GetChildren())):
                if len(customer_messages) >= limit:
                    break

                try:
                    # 检查是否是文本消息
                    if not 'ChatTextItemView' in getattr(item, 'ClassName', ''):
                        continue

                    rect = getattr(item, 'BoundingRectangle')
                    item_center = (rect.left + rect.right) / 2

                    # 判断方向
                    if item_center < list_center:  # 左侧是对方
                        customer_messages.append(getattr(item, 'Name', ''))
                    else:  # 右侧是自己，停止收集
                        break
                except:
                    continue

            # 反转顺序
            customer_messages.reverse()
            return customer_messages

        except:
            return []

    def _check_new_message(self, message_rects) -> bool:
        """
        检查当前聊天窗口是否有最新消息（对方发来的）
        """
        try:
            if not self.region.chat_messages:
                self.logger.warning("聊天消息区域未定位")
                return False

            # 获取聊天区域坐标
            msg_x1, msg_y1, msg_x2, msg_y2 = self.region.chat_messages
            width = msg_x2 - msg_x1
            height = msg_y2 - msg_y1

            if not message_rects:
                self.logger.debug("未检测到任何消息气泡")
                return False

            # 找到Y坐标最大的消息（最底部）
            message_rects.sort(key=lambda rect: rect[1], reverse=True)
            x, y, w, h = message_rects[0]  # 最底部的一条消息

            # 计算消息气泡的中心点
            bubble_center_x = x + w // 2

            # 使用头像边界作为判断标准
            # 如果消息在左侧头像边界右侧，且在整个聊天区域左侧1/3范围内，认为是客户消息
            # 这比简单的中心线判断更准确
            avatar_boundary = self.region.chat_avatar_boundary
            is_customer_message = (bubble_center_x < width * 0.4)

            self.logger.debug(
                f"最新消息位置: x={x}, 中心x={bubble_center_x}, 头像边界={avatar_boundary}, 是否客户消息={is_customer_message}")

            return is_customer_message

        except Exception as e:
            self.logger.error(f"检查新消息失败: {e}")
            return False

    def _send_message_directly(self, message: str) -> bool:
        """
        参数:
            message: 要发送的消息内容
        """
        try:
            if not self.region.chat_input_box:
                self.logger.error("聊天输入框区域未定位")
                return False

            # 获取输入框坐标
            input_x1, input_y1, input_x2, input_y2 = self.region.chat_input_box
            input_center_x = (input_x1 + input_x2) // 2
            input_center_y = (input_y1 + input_y2) // 2

            self.logger.info(f"准备发送消息: {message[:50]}...")

            # 点击输入框获取焦点
            self._safe_click(input_center_x, input_center_y,
                             move_duration=random.uniform(0.3, 0.5),
                             description="点击聊天输入框")
            time.sleep(0.5)

            # 清空输入框
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            time.sleep(0.1)

            # 输入消息 - 优先使用剪贴板
            self.logger.info("输入消息内容...")
            if self._type_with_clipboard(message):
                self.logger.info("使用剪贴板输入消息成功")
            else:
                for char in message:
                    pyautogui.typewrite(char)
                    time.sleep(0.1)

            if message:
                # 7. 按回车发送
                pyautogui.press('enter')
                self.logger.info("消息已发送")
            # 点击发送按钮
            # if not self.region.chat_send_button:
            #     self.logger.error("发送按钮区域未定位")
            #     return False

            # send_x1, send_y1, send_x2, send_y2 = self.region.chat_send_button
            # send_center_x = (send_x1 + send_x2) // 2
            # send_center_y = (send_y1 + send_y2) // 2
            #
            # self.logger.info("点击发送按钮...")
            # self._safe_click(send_center_x, send_center_y,
            #                  move_duration=random.uniform(0.2, 0.4),
            #                  description="点击发送按钮")
            #
            time.sleep(random.uniform(0.5, 2))  # 等待发送完成
            self.logger.info("消息发送完成")
            return True

        except Exception as e:
            self.logger.error(f"直接发送消息失败: {e}")
            return False

    def _get_latest_messages(self, message_rects) -> List[Dict[str, Any]]:
        """
        获取客户最新的连续消息（直到遇到自己发送的消息为止）

        逻辑：从最新的消息开始，连续获取客户（左侧）消息，直到遇到自己发送的消息
        例如：AABAA -> 取AA（A是客户，B是自己）

        Args:
            max_count: 最大检查的消息数量
        Returns:
            List[Dict]: 客户最新的连续消息列表
        """
        try:
            if not self.region.chat_messages:
                self.logger.error("聊天消息区域未定位")
                return []

            if not message_rects:
                self.logger.warning("未检测到任何消息气泡")
                return []
            # 获取聊天区域坐标
            msg_x1, msg_y1, msg_x2, msg_y2 = self.region.chat_messages
            width = msg_x2 - msg_x1

            # 按垂直位置排序（从底部到顶部，最新的先处理）
            message_rects.sort(key=lambda rect: rect[1], reverse=True)
            customer_messages = []

            for i, (x, y, w, h) in enumerate(message_rects):
                try:
                    # 计算消息气泡的中心点（相对坐标）
                    bubble_center_x = x + w // 2


                    # 使用头像边界和相对位置判断消息方向
                    is_customer_message =  (bubble_center_x < width * 0.4)
                    if is_customer_message:
                        copy_center_x = x + w -20
                    else:
                        copy_center_x = x + 20
                    # 如果是自己的消息，停止收集
                    if not is_customer_message:
                        self.logger.debug(f"遇到自己发送的消息，停止收集")
                        break

                    # 转换为绝对屏幕坐标
                    absolute_x = msg_x1 + copy_center_x
                    absolute_y = msg_y1 + (y + h // 2)
                    # 右键点击消息气泡中心
                    click_x = absolute_x
                    click_y = absolute_y
                    pyautogui.moveTo(click_x, click_y, duration=1)
                    # 获取光标信息 如果是光标 则右键
                    cursor_info = win32gui.GetCursorInfo()
                    # 根据常见光标ID判断形状
                    if cursor_info:
                        cursor_id = cursor_info[1]
                        if cursor_id != 65541:
                            self.logger.info(f"非 I型/输入，不可点击复制:{cursor_id}")
                            continue
                    pyautogui.click(click_x, click_y, button='right')
                    time.sleep(0.5)
                    ## 先情况剪切板
                    pyperclip.copy("")
                    time.sleep(0.1)
                    if IS_WINDOWS:
                        try:
                            import win32clipboard
                            win32clipboard.OpenClipboard()
                            win32clipboard.EmptyClipboard()
                            win32clipboard.CloseClipboard()
                            time.sleep(0.1)
                        except:
                            pass
                    # 获取复制菜单位置并点击
                    copy_click_x, copy_click_y = self.get_copy_menu_position(click_x, click_y)
                    pyautogui.click(copy_click_x, copy_click_y)
                    time.sleep(0.3)
                    clipboard_content = pyperclip.paste().strip()
                    # 读取剪贴板内容
                    if clipboard_content and len(clipboard_content) > 0:
                        customer_messages.append(clipboard_content)

                except Exception as e:
                    self.logger.error(f"处理消息 {i + 1} 失败: {e}")
                    continue

            # 反转列表，使消息按时间顺序排列（从旧到新）
            customer_messages.reverse()

            self.logger.info(f"成功获取 {len(customer_messages)} 条客户连续消息")
            return customer_messages

        except Exception as e:
            self.logger.error(f"获取客户最新消息失败: {e}")
            return []

    def _call_ai_api(self, contact_name: str, customer_messages: List[Dict[str, Any]], api_url: str, api_key: str,
                     model: str = "") -> List[Dict[str, Any]]:
        """
        统一调用AI聊天接口（兼容所有模型）

        Args:
            contact_name: 联系人名称
            customer_messages: 消息列表（包含role字段：user为客户，assistant为自己/AI）
            api_url: API地址
            api_key: API密钥
            model: 模型名称（默认: "default"）
        Returns:
            List[Dict]: AI回复消息列表，包含content和pause_ms
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            # 构建标准请求数据
            data = {
                "model": model,
                "messages": customer_messages,
                "stream": False,
                "temperature": 0.7,
                "max_tokens": 1000
            }

            # 添加额外字段（保留原有格式的兼容性）
            data["user_id"] = None
            data["user_name"] = contact_name

            self.logger.info(f"调用AI接口: {api_url}")
            self.logger.info(f"模型: {model}")

            response = requests.post(
                api_url,
                json=data,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"API响应状态: 成功")

                # 解析各种可能的响应格式
                ai_responses = self._parse_api_response(result)

                if ai_responses:
                    self.logger.info(f"收到AI回复: {len(ai_responses)}条消息")
                    return ai_responses
                else:
                    self.logger.error(f"API返回格式无法解析: {result}")
                    return []
            else:
                self.logger.error(f"AI接口调用失败: {response.status_code} - {response.text}")
                return []

        except requests.exceptions.Timeout:
            self.logger.error("AI接口调用超时")
            return []
        except requests.exceptions.ConnectionError:
            self.logger.error("无法连接到AI接口")
            return []
        except Exception as api_error:
            self.logger.error(f"调用AI接口失败: {api_error}")
            import traceback
            traceback.print_exc()
            return []

    def _parse_api_response(self, response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        解析各种API响应格式为统一的消息列表

        Args:
            response_data: API响应的JSON数据
        Returns:
            List[Dict]: AI回复消息列表，包含content和pause_ms
        """
        ai_responses = []

        try:
            if isinstance(response_data, dict):
                # 格式1: OpenAI/DeepeSeek 标准格式 (choices数组)
                if "choices" in response_data and isinstance(response_data["choices"], list):
                    for choice in response_data["choices"]:
                        if isinstance(choice, dict):
                            # 格式: choices[].message.content
                            if "message" in choice and isinstance(choice["message"], dict):
                                content = choice["message"].get("content", "").strip()
                                if content:
                                    ai_responses.append({
                                        "content": content,
                                        "pause_ms": 1000  # 默认暂停1秒
                                    })
                            # 格式: choices[].text (某些API的格式)
                            elif "text" in choice:
                                content = choice["text"].strip()
                                if content:
                                    ai_responses.append({
                                        "content": content,
                                        "pause_ms": 1000
                                    })

                # 格式2: 本地服务格式 (success + data.messages)
                elif response_data.get("success") and "data" in response_data:
                    messages = response_data["data"].get("messages", [])
                    for msg in messages:
                        content = msg.get("content", "").strip()
                        if content:
                            ai_responses.append({
                                "content": content,
                                "pause_ms": msg.get("pause_ms", 1000)
                            })
                else:
                    self.logger.error(f"返回有问题: {response_data}")
        except Exception as e:
            self.logger.error(f"解析API响应失败: {e}")
            return []

        return ai_responses

    def get_chat_header_name(self) -> str:
        """
        获取聊天窗口header区域显示的名称
        """
        try:
            if not self.region.chat_header:
                return ""

            header_x1, header_y1, header_x2, header_y2 = self.region.chat_header
            name_region_left = header_x1
            name_region_top = header_y1
            name_region_right = min(header_x1 + 220, header_x2)
            name_region_bottom = header_y2

            time.sleep(0.3)
            screenshot = ImageGrab.grab(bbox=(
                name_region_left, name_region_top,
                name_region_right, name_region_bottom
            ))
            # timestamp = time.strftime("%Y%m%d_%H%M%S")
            # temp_path = f"debug/chat_header_{timestamp}.png"
            # screenshot.save(temp_path)
            img_array = np.array(screenshot.convert('RGB'))
            # debug时 保存图像预处理以提高OCR
            # img = Image.fromarray(img_array)
            # timestamp = time.strftime("%Y%m%d_%H%M%S")
            # temp_path = f"debug/chat_header_processed_{timestamp}.png"
            # img.save(temp_path)
            # OCR识别
            ocr_result = self._paddle_ocr.ocr(img_array)

            # 过滤和选择最佳文本
            best_text = ""
            best_length = 0

            if ocr_result and len(ocr_result) > 0:
                # 定义需要过滤的干扰字符（边缘线、符号等）
                filter_patterns = [
                    '十', '一', '丨', '|', '┃', '║', '│',  # 竖线/横线
                    '•', '·', '。', '.', ',', '，',  # 点、符号
                    '(', ')', '（', '）', '[', ']',  # 括号
                    ':', '：', ';', '；',  # 标点
                    '+', '-', '*', '/', '\\',  # 运算符号
                ]

                # 遍历所有识别结果
                for page in ocr_result:
                    if isinstance(page, list):
                        for item in page:
                            if isinstance(item, list) and len(item) >= 2:
                                # 提取文本
                                text_info = item[1]
                                if isinstance(text_info, (tuple, list)) and len(text_info) >= 1:
                                    text = str(text_info[0]).strip()

                                    # 过滤掉干扰文本
                                    should_filter = False

                                    # 1. 过滤单个字符且是干扰字符的
                                    if len(text) == 1 and text in filter_patterns:
                                        should_filter = True

                                    # 2. 过滤纯数字
                                    elif text.isdigit():
                                        should_filter = True

                                    # 3. 过滤超短文本（可能是噪声）
                                    elif len(text) < 2:
                                        should_filter = True

                                    # 4. 过滤包含多个干扰字符的文本
                                    else:
                                        interference_count = sum(1 for char in text if char in filter_patterns)
                                        if interference_count / len(text) > 0.5:  # 超过50%是干扰字符
                                            should_filter = True

                                    if not should_filter and len(text) > best_length:
                                        best_text = text
                                        best_length = len(text)

            if best_text:
                # 额外清理：移除开头结尾的干扰字符
                import re
                # 移除开头和结尾的干扰字符
                pattern = '^[' + ''.join(re.escape(c) for c in filter_patterns) + ']+'
                best_text = re.sub(pattern, '', best_text)
                pattern = '[' + ''.join(re.escape(c) for c in filter_patterns) + ']+$'
                best_text = re.sub(pattern, '', best_text)

                self.logger.info(f"识别到窗口名称: {best_text}")
                return best_text.strip()

            return ""

        except Exception as e:
            self.logger.debug(f"获取窗口名称失败: {e}")
            return ""

    def stop_auto_process(self):
        """
        停止自动处理
        """
        self.logger.info("正在停止自动处理...")
        # 设置一个标志位来控制循环
        self.auto_process_running = False
        self.logger.info("自动处理已停止")
        return True

def main():
    parser = argparse.ArgumentParser(description='微信桌面自动化工具')
    parser.add_argument('action', choices=[
        'start', 'activate', 'search_and_send', 'get_history',
        'auto_process', 'stop_auto_process', 'help'  # 添加 stop_auto_process
    ], help='要执行的操作')

    parser.add_argument('--contact', help='联系人名称（用于search_and_send和get_history操作）')
    parser.add_argument('--message', default='您好', help='消息内容（用于search_and_send操作，默认：您好）')
    parser.add_argument('--limit', type=int, default=10, help='获取历史记录的数量限制（用于get_history操作，默认：10）')
    parser.add_argument('--polling_times', type=int, default=5, help='轮询次数（用于auto_process操作，默认：5）')
    parser.add_argument('--api_url', default='http://localhost:8000/api/chat/completions',
                       help='AI接口URL（用于auto_process操作，默认：http://localhost:8000/api/chat/completions）')
    parser.add_argument('--api_key', required='auto_process' in sys.argv, help='API密钥（auto_process操作必需）')
    parser.add_argument('--model', default='', help='模型名称（用于auto_process操作）')
    parser.add_argument('--wait_time', type=int, default=300, help='每轮等待时间（秒，用于auto_process操作，默认：300）')
    parser.add_argument('--title', help='窗口标题（用于activate操作）')
    parser.add_argument('--contact_list', nargs='+', default=['张三', '李四', '王五', '赵六'],
                       help='联系人列表（用于auto_process操作，默认：张三 李四 王五 赵六）')

    args = parser.parse_args()

    # 创建实例
    wechat = WeChatAutomation()

    try:
        if args.action == 'start':
            result = wechat.start_wechat()
            if result:
                print("✅ 微信启动成功")
                print(json.dumps({'success': True, 'message': '微信启动成功'}, ensure_ascii=False))
            else:
                print("❌ 微信启动失败")
                print(json.dumps({'success': False, 'message': '微信启动失败'}, ensure_ascii=False))

        elif args.action == 'activate':
            result = wechat.activate_wechat_window(args.title)
            if result:
                print("✅ 微信窗口激活成功")
                print(json.dumps({'success': True, 'message': '微信窗口激活成功'}, ensure_ascii=False))
            else:
                print("❌ 微信窗口激活失败")
                print(json.dumps({'success': False, 'message': '微信窗口激活失败'}, ensure_ascii=False))

        elif args.action == 'search_and_send':
            if not args.contact:
                print("错误：需要指定联系人名称 (--contact)")
                sys.exit(1)

            print(f"准备发送消息给: {args.contact}")
            print(f"消息内容: {args.message}")

            result = wechat.search_and_send_message(args.contact, args.message)

            if result:
                print("✅ 消息发送成功")
                print(json.dumps({
                    'success': True,
                    'contact': args.contact,
                    'message': args.message,
                    'result': '消息发送成功'
                }, ensure_ascii=False))
            else:
                print("❌ 消息发送失败")
                print(json.dumps({
                    'success': False,
                    'contact': args.contact,
                    'message': args.message,
                    'result': '消息发送失败'
                }, ensure_ascii=False))

        elif args.action == 'get_history':
            if not args.contact:
                print("错误：需要指定联系人名称 (--contact)")
                sys.exit(1)

            print(f"准备获取聊天记录: {args.contact}")
            print(f"限制数量: {args.limit}")

            messages = wechat.get_chat_history(args.contact, args.limit)

            print(f"✅ 成功获取 {len(messages)} 条聊天记录")
            print(json.dumps({
                'success': True,
                'contact': args.contact,
                'message_count': len(messages),
                'messages': messages
            }, ensure_ascii=False, indent=2))

        elif args.action == 'auto_process':
            print(f"开始自动处理联系人列表")
            print(f"联系人: {', '.join(args.contact_list)}")
            print(f"轮询次数: {args.polling_times}")
            print(f"AI接口: {args.api_url}")
            print(f"API密钥: {args.api_key[:8]}...")
            print(f"模型名称: {args.model}")
            print(f"每轮对话等待时长: {args.wait_time}秒")
            print("程序将无限循环运行，按 Ctrl+C 停止")
            print("或使用 'python wechat.py stop_auto_process' 停止")
            print("=" * 50)

            # 开始自动处理
            wechat.auto_process_contacts(
                contact_list=args.contact_list,
                max_polling_times=args.polling_times,
                api_url=args.api_url,
                api_key=args.api_key,
                model=args.model,
                wait_time=args.wait_time
            )

        elif args.action == 'stop_auto_process':
            result = wechat.stop_auto_process()
            if result:
                print("✅ 已发送停止自动处理信号")
                print(json.dumps({'success': True, 'message': '已发送停止自动处理信号'}, ensure_ascii=False))
            else:
                print("❌ 停止自动处理失败")
                print(json.dumps({'success': False, 'message': '停止自动处理失败'}, ensure_ascii=False))

        elif args.action == 'help':
            print("微信桌面自动化工具命令说明：")
            print("  start              - 启动微信")
            print("  activate           - 激活微信窗口")
            print("  search_and_send    - 搜索联系人并发送消息")
            print("  get_history        - 获取聊天记录")
            print("  auto_process       - 自动处理联系人消息")
            print("  stop_auto_process  - 停止自动处理")
            print("\n参数说明：")
            print("  --contact          - 联系人名称（用于search_and_send、get_history）")
            print("  --message          - 消息内容（可选，默认：您好）")
            print("  --limit            - 获取历史记录数量（可选，默认：10）")
            print("  --polling_times    - 轮询次数（可选，默认：5）")
            print("  --api_url          - AI接口URL（可选，默认：http://localhost:8000/api/chat/completions）")
            print("  --api_key          - API密钥（auto_process操作必需）")
            print("  --model            - 模型名称（auto_process操作可选）")
            print("  --wait_time        - 每轮等待时间（秒，auto_process操作可选，默认：300）")
            print("  --title            - 窗口标题（用于activate操作）")
            print("  --contact_list     - 联系人列表（auto_process操作可选，默认：张三 李四 王五 赵六）")
            print("\n使用示例：")
            print("  python wechat.py start")
            print("  python wechat.py activate")
            print("  python wechat.py search_and_send --contact 张三 --message 你好")
            print("  python wechat.py get_history --contact 李四 --limit 5")
            print("  python wechat.py auto_process --api_key your_api_key --polling_times 10")
            print("  python wechat.py auto_process --api_key your_api_key --contact_list 张三 李四")
            print("  python wechat.py stop_auto_process")

        else:
            print(f"未知操作: {args.action}")
            print("使用 'python wechat.py help' 查看帮助")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⏹️ 程序已停止")
        sys.exit(0)
    except Exception as e:
        print(f"错误: {str(e)}")
        print(json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()