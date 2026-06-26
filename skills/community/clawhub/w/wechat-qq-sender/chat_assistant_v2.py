#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信/QQ 智能回复助手（OCR 版）v2.0
支持微信和 QQ 的聊天截图识别与自动回复
"""

import pyautogui
import pygetwindow as gw
import time
import sys
import os
from PIL import ImageGrab, Image
import pyperclip
import cv2
import numpy as np
import warnings

# 设置 UTF-8 输出
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 初始化 EasyOCR（延迟加载）
_ocr_reader = None

def get_ocr_reader():
    """获取 OCR 读取器（单例）"""
    global _ocr_reader
    if _ocr_reader is None:
        print("🔄 加载 EasyOCR 模型...")
        import easyocr
        warnings.filterwarnings('ignore')
        _ocr_reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        print("✅ EasyOCR 模型加载完成")
    return _ocr_reader

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

class ChatAssistant:
    def __init__(self):
        self.platform = None  # 'wechat' 或 'qq'
        self.window = None
        
    def detect_platform(self):
        """检测当前窗口是微信还是 QQ"""
        print("检测聊天平台...")
        
        # 获取所有窗口
        all_windows = gw.getAllWindows()
        
        for window in all_windows:
            title = window.title.lower()
            
            # 检测微信
            if '微信' in window.title or 'wechat' in title:
                print(f"✅ 检测到微信窗口: {window.title}")
                self.platform = 'wechat'
                self.window = window
                return True
                
            # 检测 QQ
            elif 'qq' in title and 'qq' in title:
                print(f"✅ 检测到 QQ 窗口: {window.title}")
                self.platform = 'qq'
                self.window = window
                return True
        
        print("❌ 未找到微信或 QQ 窗口")
        return False
    
    def get_chat_area(self):
        """根据平台获取聊天区域坐标"""
        if not self.window:
            return None
        
        # 窗口基本信息
        left = self.window.left
        top = self.window.top
        width = self.window.width
        height = self.window.height
        
        if self.platform == 'wechat':
            # 微信聊天区域（右侧中间部分）
            # 左侧是联系人列表（约 280px），右侧是聊天内容
            chat_left = left + 280
            chat_top = top + 100
            chat_width = width - 280
            chat_height = height - 200
            
        elif self.platform == 'qq':
            # QQ 聊天区域（优化版：去掉左边头像列表和右边群成员列表）
            chat_left = left + int(width * 0.22)  # 22% 左边距
            chat_top = top + 120
            chat_right = right - int(width * 0.28)  # 28% 右边距（去掉群成员列表）
            chat_bottom = bottom - 180
            return (chat_left, chat_top, chat_right, chat_bottom)
            
        else:
            return None
        
        return (chat_left, chat_top, chat_left + chat_width, chat_top + chat_height)
    
    def capture_chat(self):
        """截图聊天区域"""
        chat_area = self.get_chat_area()
        if not chat_area:
            print("❌ 无法获取聊天区域")
            return None
        
        print(f"📸 截取聊天区域: {chat_area}")
        
        try:
            screenshot = ImageGrab.grab(bbox=chat_area)
            # 保存到专用目录（带清理功能）
            save_dir = os.path.expanduser("~/.openclaw/workspace/screenshots")
            os.makedirs(save_dir, exist_ok=True)
            
            # 清理旧截图（保留最近10张）
            screenshot_files = [f for f in os.listdir(save_dir) if f.endswith('.png')]
            screenshot_files.sort(key=lambda x: os.path.getmtime(os.path.join(save_dir, x)))
            if len(screenshot_files) > 10:
                old_files = screenshot_files[:-10]
                for old_file in old_files:
                    try:
                        os.remove(os.path.join(save_dir, old_file))
                    except:
                        pass
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_dir, f'chat_capture_{self.platform}_{timestamp}.png')
            screenshot.save(filename)
            print(f"✅ 截图保存: {filename}")
            return filename
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            return None
    
    def ocr_chat(self, image_path):
        """OCR 识别聊天内容 - 使用 EasyOCR"""
        print(f"🔍 识别 {self.platform} 聊天内容...")
        
        try:
            reader = get_ocr_reader()
            
            # 读取图片
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # 识别文字
            results = reader.readtext(img_array)
            
            # 过滤低置信度的结果
            texts = []
            for detection in results:
                text = detection[1]
                confidence = detection[2]
                if confidence > 0.4 and len(text) > 1:
                    texts.append(text)
            
            print(f"✅ 识别到 {len(texts)} 条文字")
            
            if texts:
                return "\n".join(texts)
            else:
                return "[未识别到文字]"
                
        except Exception as e:
            print(f"❌ OCR 失败: {e}")
            return "[OCR 失败]"
    
    def send_message(self, message):
        """发送消息"""
        if not self.window:
            print("❌ 窗口未找到")
            return False
        
        # 激活窗口
        try:
            self.window.activate()
        except:
            pyautogui.click(self.window.left + 100, self.window.top + 50)
        time.sleep(0.5)
        
        # 点击输入框（窗口底部中间）
        input_x = self.window.left + self.window.width // 2
        input_y = self.window.top + self.window.height - 100
        
        print(f"📝 点击输入框: ({input_x}, {input_y})")
        pyautogui.click(input_x, input_y)
        time.sleep(0.3)
        
        # 粘贴消息
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        
        # 发送
        pyautogui.press('enter')
        print("✅ 消息已发送")
        return True
    
    def process_chat(self, contact_name=None, auto_reply=False):
        """主流程：处理聊天"""
        print("=" * 60)
        print("微信/QQ 智能回复助手 v2.0")
        print("=" * 60)
        
        # 1. 检测平台
        if not self.detect_platform():
            return False
        
        # 2. 如果有指定联系人，先搜索
        if contact_name:
            print(f"🔍 搜索联系人: {contact_name}")
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            pyautogui.write(contact_name)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
        
        # 3. 截图聊天区域
        screenshot_path = self.capture_chat()
        if not screenshot_path:
            return False
        
        # 4. OCR 识别（返回截图路径）
        result = self.ocr_chat(screenshot_path)
        
        print("=" * 60)
        print(f"✅ 完成！截图已保存: {result}")
        print("💡 提示：将截图发送给 AI 助手分析聊天内容")
        print("=" * 60)
        
        return result

def main():
    """主函数"""
    import sys
    
    assistant = ChatAssistant()
    
    # 解析参数
    contact = sys.argv[1] if len(sys.argv) > 1 else None
    
    # 执行
    result = assistant.process_chat(contact)
    
    if result:
        print(f"\n截图文件: {result}")
        print("请将此截图发送给 AI 助手进行分析")
    else:
        print("\n❌ 处理失败")
        sys.exit(1)

if __name__ == '__main__':
    main()
