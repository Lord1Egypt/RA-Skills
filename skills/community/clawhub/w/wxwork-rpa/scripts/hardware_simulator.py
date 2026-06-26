#!/usr/bin/env python3
"""
硬件层模拟 - 使用HID设备直接模拟输入
支持Windows和macOS
"""

import time
import random
import threading
from typing import List, Tuple, Optional
import logging
import pyautogui
logger = logging.getLogger(__name__)


class HardwareSimulator:
    """硬件层模拟器"""

    def __init__(self):
        self.is_windows = False
        self.is_macos = False

        try:
            import platform
            system = platform.system()
            self.is_windows = system == "Windows"
            self.is_macos = system == "Darwin"

            # 根据平台初始化相应的硬件模拟
            if self.is_windows:
                self._init_windows_hid()
            elif self.is_macos:
                self._init_macos_hid()
            else:
                logger.warning(f"不支持的操作系统: {system}")

        except Exception as e:
            logger.error(f"硬件模拟初始化失败: {e}")

    def _init_windows_hid(self):
        """Windows HID模拟"""
        try:
            # 使用pywinusb或hidapi
            import hid
            self.hid_device = None

            # 尝试查找虚拟HID设备
            devices = hid.enumerate()
            for device in devices:
                # 寻找可用的HID设备
                if device['vendor_id'] == 0x1A2C or device['product_id'] == 0x6004:
                    self.hid_device = hid.device()
                    self.hid_device.open(device['vendor_id'], device['product_id'])
                    logger.info("找到HID设备")
                    break

            if not self.hid_device:
                logger.warning("未找到合适的HID设备，将使用软件模拟")

        except ImportError:
            logger.warning("未安装hid库，使用备用方案")

    def _init_macos_hid(self):
        """macOS HID模拟"""
        try:
            # macOS可以使用IOKit或pyobjc
            from Quartz import CGEventCreateKeyboardEvent, CGEventPost, kCGHIDEventTap
            from AppKit import NSEvent
            self.macos_available = True
            logger.info("macOS HID模拟可用")
        except ImportError:
            logger.warning("macOS HID模拟不可用，使用备用方案")
            self.macos_available = False

    def simulate_mouse_move(self, x: int, y: int, duration: float = 0.5):
        """
        硬件级鼠标移动模拟
        Args:
            x, y: 目标坐标
            duration: 移动持续时间
        """
        try:
            if self.is_windows and hasattr(self, 'hid_device') and self.hid_device:
                self._windows_hid_mouse_move(x, y, duration)
            elif self.is_macos and hasattr(self, 'macos_available') and self.macos_available:
                self._macos_hid_mouse_move(x, y, duration)
            else:
                self._software_mouse_move(x, y, duration)

        except Exception as e:
            logger.error(f"硬件鼠标移动失败: {e}")
            self._software_mouse_move(x, y, duration)

    def _windows_hid_mouse_move(self, x: int, y: int, duration: float):
        """Windows HID鼠标移动"""
        import win32api
        import win32con

        # 获取当前鼠标位置
        current_x, current_y = win32api.GetCursorPos()

        # 生成贝塞尔曲线路径
        points = self._generate_bezier_path(current_x, current_y, x, y, 50)

        # 计算每个点的间隔时间
        interval = duration / len(points)

        for point_x, point_y in points:
            # 使用绝对坐标移动
            win32api.mouse_event(
                win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,
                int(point_x * 65535 / 1920),  # 假设屏幕宽度1920
                int(point_y * 65535 / 1080),  # 假设屏幕高度1080
                0, 0
            )
            time.sleep(interval)

    def _macos_hid_mouse_move(self, x: int, y: int, duration: float):
        """macOS HID鼠标移动"""
        try:
            from Quartz import (
                CGEventCreateMouseEvent, CGEventPost, kCGHIDEventTap,
                kCGEventMouseMoved, kCGMouseButtonLeft
            )

            # 创建鼠标移动事件
            event = CGEventCreateMouseEvent(
                None,
                kCGEventMouseMoved,
                (x, y),
                kCGMouseButtonLeft
            )

            # 分步移动，模拟人类行为
            steps = 20
            for i in range(steps):
                progress = (i + 1) / steps
                current_x = x * progress
                current_y = y * progress

                # 更新事件位置
                event = CGEventCreateMouseEvent(
                    None,
                    kCGEventMouseMoved,
                    (current_x, current_y),
                    kCGMouseButtonLeft
                )
                CGEventPost(kCGHIDEventTap, event)
                time.sleep(duration / steps)

        except Exception as e:
            logger.error(f"macOS HID鼠标移动失败: {e}")
            raise

    def _software_mouse_move(self, x: int, y: int, duration: float):
        """软件模拟鼠标移动（备用方案）"""
        import pyautogui

        # 使用带人类行为的移动
        pyautogui.moveTo(x, y, duration=duration,
                         tween=pyautogui.easeInOutQuad)

    def simulate_keyboard_input(self, text: str, min_delay: float = 0.05, max_delay: float = 0.15):
        """
        硬件级键盘输入模拟
        Args:
            text: 要输入的文本
            min_delay, max_delay: 按键延迟范围
        """
        try:
            if self.is_windows and hasattr(self, 'hid_device') and self.hid_device:
                self._windows_hid_keyboard_input(text, min_delay, max_delay)
            elif self.is_macos and hasattr(self, 'macos_available') and self.macos_available:
                self._macos_hid_keyboard_input(text, min_delay, max_delay)
            else:
                self._software_keyboard_input(text, min_delay, max_delay)

        except Exception as e:
            logger.error(f"硬件键盘输入失败: {e}")
            self._software_keyboard_input(text, min_delay, max_delay)

    def _software_keyboard_input(self, text: str, min_delay: float = 0.05, max_delay: float = 0.15):
        """
        软件模拟键盘输入（备用方案）- 修改为复制粘贴方式
        """
        logger.info("使用软件模拟键盘输入")

        # 分段输入，模拟人类打字
        segments = self._split_text_by_punctuation(text)

        for segment in segments:
            # 模拟思考时间
            think_time = random.uniform(0.1, 0.3)
            time.sleep(think_time)

            # 使用复制粘贴方式输入每个片段
            try:
                # 复制当前片段到剪贴板
                import pyperclip
                pyperclip.copy(segment)
                time.sleep(0.1)  # 确保复制完成

                # 发送粘贴快捷键
                import pyautogui
                if self.is_windows:
                    pyautogui.hotkey('ctrl', 'v')
                elif self.is_macos:
                    pyautogui.hotkey('command', 'v')
                else:
                    pyautogui.hotkey('ctrl', 'v')  # 默认用Ctrl

                # 随机延迟，模拟人类打字速度
                delay = random.uniform(min_delay, max_delay)
                time.sleep(delay)

                # 偶尔添加额外延迟（模拟犹豫）
                if random.random() < 0.05:
                    time.sleep(random.uniform(0.1, 0.2))

            except Exception as e:
                logger.warning(f"复制粘贴输入失败: {e}, 尝试逐字输入")
                # 如果复制粘贴失败，尝试原始的逐字输入（作为最后的手段）
                try:
                    for char in segment:
                        delay = random.uniform(min_delay, max_delay)
                        pyautogui.typewrite(char, interval=delay)
                        if random.random() < 0.05:
                            time.sleep(random.uniform(0.1, 0.2))
                except Exception as e2:
                    logger.error(f"逐字输入也失败: {e2}")

    def _windows_hid_keyboard_input(self, text: str, min_delay: float, max_delay: float):
        """Windows HID键盘输入 - 支持中文"""
        import pyperclip
        import pyautogui
        import win32api
        import win32con

        # 检查文本是否包含中文
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)

        if has_chinese or len(text) > 20:
            # 对于中文或长文本，使用复制粘贴方式
            logger.info("检测到中文或长文本，使用复制粘贴方式")

            # 分段处理
            segments = self._split_text_by_punctuation(text)

            for segment in segments:
                if not segment.strip():
                    continue

                # 模拟思考时间
                think_time = random.uniform(0.1, 0.3)
                time.sleep(think_time)

                # 复制到剪贴板
                pyperclip.copy(segment)
                time.sleep(0.1)

                # 发送Ctrl+V粘贴
                win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                time.sleep(0.01)
                win32api.keybd_event(ord('V'), 0, 0, 0)
                time.sleep(0.01)
                win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

                # 随机延迟
                delay = random.uniform(min_delay, max_delay)
                time.sleep(delay)
        else:
            # 对于英文短文本，可以使用直接按键
            logger.info("英文短文本，使用直接按键方式")
            for char in text:
                delay = random.uniform(min_delay, max_delay)
                time.sleep(delay)

                if char.isupper():
                    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
                    time.sleep(0.01)

                vk_code = self._char_to_vk(char)
                if vk_code:
                    win32api.keybd_event(vk_code, 0, 0, 0)
                    time.sleep(0.01)
                    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)

                if char.isupper():
                    win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
                    time.sleep(0.01)

    def _char_to_vk(self, char: str) -> Optional[int]:
        """字符转虚拟键码 - 支持更多字符"""
        import win32con

        if not char:
            return None

        char_lower = char.lower()

        # 字母
        if 'a' <= char_lower <= 'z':
            return ord(char_lower.upper())

        # 数字
        elif '0' <= char_lower <= '9':
            return ord(char_lower)

        # 特殊字符映射
        special_chars = {
            ' ': win32con.VK_SPACE,
            '\n': win32con.VK_RETURN,
            '\t': win32con.VK_TAB,
            '.': win32con.VK_OEM_PERIOD,
            ',': win32con.VK_OEM_COMMA,
            ';': win32con.VK_OEM_1,
            '/': win32con.VK_OEM_2,
            '`': win32con.VK_OEM_3,
            '[': win32con.VK_OEM_4,
            '\\': win32con.VK_OEM_5,
            ']': win32con.VK_OEM_6,
            "'": win32con.VK_OEM_7,
            '-': win32con.VK_OEM_MINUS,
            '=': win32con.VK_OEM_PLUS,
        }

        if char in special_chars:
            return special_chars[char]

        # 中文或其他Unicode字符返回None，使用复制粘贴方式
        return None

    def _generate_bezier_path(self, start_x: int, start_y: int,
                              end_x: int, end_y: int,
                              num_points: int = 20) -> List[Tuple[int, int]]:
        """
        生成贝塞尔曲线路径
        返回一系列坐标点
        """
        import numpy as np

        # 生成控制点
        control1_x = start_x + (end_x - start_x) * random.uniform(0.2, 0.4)
        control1_y = start_y + (end_y - start_y) * random.uniform(0.2, 0.4)

        control2_x = start_x + (end_x - start_x) * random.uniform(0.6, 0.8)
        control2_y = start_y + (end_y - start_y) * random.uniform(0.6, 0.8)

        points = []
        for i in range(num_points):
            t = i / (num_points - 1)

            # 三次贝塞尔曲线
            x = (1 - t) ** 3 * start_x + \
                3 * (1 - t) ** 2 * t * control1_x + \
                3 * (1 - t) * t ** 2 * control2_x + \
                t ** 3 * end_x

            y = (1 - t) ** 3 * start_y + \
                3 * (1 - t) ** 2 * t * control1_y + \
                3 * (1 - t) * t ** 2 * control2_y + \
                t ** 3 * end_y

            # 添加随机抖动
            x += random.randint(-1, 1)
            y += random.randint(-1, 1)

            points.append((int(x), int(y)))

        return points

    def simulate_human_behavior(self, behavior_type: str, **kwargs):
        """
        模拟人类行为模式
        Args:
            behavior_type: 行为类型（'typing', 'scrolling', 'clicking'）
        """
        if behavior_type == 'typing':
            self._simulate_human_typing(**kwargs)
        elif behavior_type == 'scrolling':
            self._simulate_human_scrolling(**kwargs)
        elif behavior_type == 'clicking':
            self._simulate_human_clicking(**kwargs)

    def _simulate_human_typing(self, text: str):
        """模拟人类打字行为"""
        # 分段输入
        segments = self._split_text_by_punctuation(text)

        for segment in segments:
            # 模拟思考时间
            think_time = random.uniform(0.1, 0.5)
            time.sleep(think_time)

            # 输入片段
            for char in segment:
                # 随机按键速度
                key_delay = random.uniform(0.05, 0.15)

                # 模拟按键
                self.simulate_keyboard_input(char, key_delay, key_delay)

                # 偶尔停顿（模拟犹豫）
                if random.random() < 0.05:
                    time.sleep(random.uniform(0.1, 0.3))

            # 片段后的停顿
            if segment and segment[-1] in '，。！？；：':
                time.sleep(random.uniform(0.2, 0.4))

    def _split_text_by_punctuation(self, text: str) -> List[str]:
        """按标点符号和随机逻辑分割文本 - 更慢更真实"""
        if not text:
            return []

        segments = []
        current_segment = ""

        for i, char in enumerate(text):
            current_segment += char

            # 中文标点后强制分段（较长停顿）
            if char in '，。！？；：':
                segments.append(current_segment)
                current_segment = ""
                continue

            # 英文标点后强制分段（中等停顿）
            elif char in ',.!?;:':
                segments.append(current_segment)
                current_segment = ""
                continue

            # 空格后有一定概率分段（模拟换行思考）
            elif char == ' ' and random.random() < 0.3:
                segments.append(current_segment)
                current_segment = ""
                continue

            # 随机分段逻辑 - 让打字速度变化更大
            segment_length = len(current_segment)

            # 短句子：3-8个字符，有30%概率分段
            if 3 <= segment_length <= 8 and random.random() < 0.3:
                segments.append(current_segment)
                current_segment = ""
                continue

            # 中等句子：9-15个字符，有50%概率分段
            elif 9 <= segment_length <= 15 and random.random() < 0.5:
                segments.append(current_segment)
                current_segment = ""
                continue

            # 长句子：超过15个字符，强制分段（避免太长）
            elif segment_length > 15:
                # 寻找最近的标点或空格分段
                last_break_pos = -1
                for j in range(len(current_segment) - 1, -1, -1):
                    if current_segment[j] in '，。！？；：,.!?;: ':
                        last_break_pos = j
                        break

                if last_break_pos > 0:
                    segments.append(current_segment[:last_break_pos + 1])
                    current_segment = current_segment[last_break_pos + 1:]
                else:
                    segments.append(current_segment)
                    current_segment = ""
                continue

        if current_segment:
            segments.append(current_segment)

        # 记录分段统计
        if segments:
            avg_len = sum(len(s) for s in segments) / len(segments)
            logger.debug(f"文本分段: 总字符={len(text)}, 段数={len(segments)}, 平均段长={avg_len:.1f}")

        return segments