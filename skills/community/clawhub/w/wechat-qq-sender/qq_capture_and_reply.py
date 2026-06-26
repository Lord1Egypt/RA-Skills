#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ 截图 + OCR + 自动回复
集成本地 OCR (EasyOCR)，无需外部发送
"""

import pyautogui
import pygetwindow as gw
import time
import sys
import os
from PIL import ImageGrab, Image
import re
import warnings

# 设置 UTF-8 输出
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 初始化 EasyOCR（延迟加载，避免启动慢）
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

def find_qq_window():
    """查找 QQ 窗口"""
    print("🔍 查找 QQ 窗口...")
    qq_windows = [w for w in gw.getAllWindows() if 'QQ' in w.title or 'qq' in w.title.lower()]
    if not qq_windows:
        print("❌ 未找到 QQ")
        return None
    return qq_windows[0]

def activate_window(window):
    """激活窗口"""
    print(f"🪟 激活：{window.title}")
    try:
        window.activate()
    except:
        pyautogui.click(window.left + 10, window.top + 10)
    time.sleep(0.5)

def search_group(group_name):
    """搜索群聊"""
    print(f"🔍 搜索群：{group_name}")
    pyautogui.hotkey('ctrl', 'alt', 's')
    time.sleep(1.5)
    
    # 点击搜索框
    window = gw.getActiveWindow()
    if window:
        pyautogui.click(window.left + 150, window.top + 60)
        time.sleep(0.3)
    
    # 清空并输入
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    pyautogui.press('delete')
    time.sleep(0.3)
    
    # 使用剪贴板粘贴
    import pyperclip
    pyperclip.copy(group_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)
    
    # 点击第一个结果
    if window:
        pyautogui.click(window.left + 150, window.top + 180)
    time.sleep(2.5)

def capture_chat_area(window):
    """截取聊天区域（优化版：只截中间聊天内容，去掉左右边栏）"""
    print("📸 截取聊天区域...")
    
    # 计算窗口尺寸
    window_width = window.width
    window_height = window.height
    
    # 优化后的截图区域（只截中间聊天内容）
    # 左边距：去掉头像列表和边栏 (~280px)
    # 右边距：去掉群成员列表 (~220px)
    # 上边距：去掉标题栏和搜索栏 (~120px)
    # 下边距：去掉输入框 (~180px)
    chat_left = window.left + int(window_width * 0.22)  # 22% 左边距
    chat_top = window.top + 120
    chat_right = window.right - int(window_width * 0.28)  # 28% 右边距（去掉群成员列表）
    chat_bottom = window.bottom - 180
    
    # 确保区域有效
    if chat_right <= chat_left or chat_bottom <= chat_top:
        print("⚠️ 窗口太小，使用默认区域")
        chat_left = window.left + 280
        chat_right = window.right - 240
    
    screenshot = ImageGrab.grab(bbox=(chat_left, chat_top, chat_right, chat_bottom))
    
    print(f"📐 截图区域: ({chat_left}, {chat_top}, {chat_right}, {chat_bottom})")
    print(f"📏 截图尺寸: {chat_right - chat_left} x {chat_bottom - chat_top}")
    
    # 清理旧截图（保留最近10张）
    save_dir = os.path.expanduser("~/.openclaw/workspace/screenshots")
    os.makedirs(save_dir, exist_ok=True)
    
    # 获取所有截图文件并按时间排序
    screenshot_files = [f for f in os.listdir(save_dir) if f.endswith('.png')]
    screenshot_files.sort(key=lambda x: os.path.getmtime(os.path.join(save_dir, x)))
    
    # 删除旧的截图（只保留最近10张）
    if len(screenshot_files) > 10:
        old_files = screenshot_files[:-10]  # 保留最新的10张
        for old_file in old_files:
            old_path = os.path.join(save_dir, old_file)
            try:
                os.remove(old_path)
                print(f"🗑️ 清理旧截图：{old_file}")
            except Exception as e:
                print(f"⚠️ 无法删除 {old_file}: {e}")
        print(f"🧹 已清理 {len(old_files)} 张旧截图")
    
    # 保存新截图
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(save_dir, f"qq_chat_{timestamp}.png")
    screenshot.save(save_path)
    print(f"✅ 截图保存：{save_path}")
    
    return save_path, screenshot

def simple_ocr(image):
    """
    OCR 识别 - 使用 EasyOCR
    返回识别到的文字列表（带置信度过滤）
    """
    print("🔍 进行 OCR 识别...")
    
    try:
        reader = get_ocr_reader()
        
        # 转换为 numpy array
        import numpy as np
        img_array = np.array(image)
        
        # 识别文字
        results = reader.readtext(img_array)
        
        # 过滤低置信度的结果（>0.4）
        texts = []
        for detection in results:
            text = detection[1]
            confidence = detection[2]
            if confidence > 0.4 and len(text) > 1:  # 过滤单字符和置信度低的
                texts.append(text)
        
        print(f"✅ OCR 识别完成，识别到 {len(texts)} 条有效文字")
        
        if texts:
            return "\n".join(texts)
        else:
            return "[未识别到有效文字]"
            
    except Exception as e:
        print(f"❌ OCR 识别失败: {e}")
        return "[OCR 识别失败]"

def analyze_chat(ocr_text):
    """
    分析聊天内容，生成回复建议
    """
    print("🧠 分析聊天内容...")
    
    # 简单的关键词匹配
    keywords = {
        "在吗": "在的，什么事？",
        "你好": "你好呀~",
        "谢谢": "不客气~",
        "拜拜": "拜拜~",
        "晚安": "晚安，好梦~",
        "早上好": "早安！",
        "吃什么": "我也不知道吃什么 (´• ω •`)",
        "玩游戏": "好啊，玩什么？",
        "工作": "加油工作！",
        "累": "注意休息呀~",
    }
    
    # 查找匹配的关键词
    for keyword, reply in keywords.items():
        if keyword in ocr_text:
            print(f"💡 检测到关键词：{keyword}")
            return reply
    
    # 默认回复
    return "收到~ (๑•̀ㅂ•́)و✧"

def send_reply(reply_text):
    """发送回复"""
    print(f"💬 发送回复：{reply_text}")
    
    # 点击输入框
    window = gw.getActiveWindow()
    if window:
        input_x = window.left + window.width // 2
        input_y = window.top + window.height - 150
        pyautogui.click(input_x, input_y)
        time.sleep(0.3)
    
    # 粘贴回复
    import pyperclip
    pyperclip.copy(reply_text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    
    # 发送
    pyautogui.press('enter')
    time.sleep(0.5)
    
    print("✅ 回复已发送")

def main():
    if len(sys.argv) < 2:
        print("用法：python qq_capture_and_reply.py <群聊名称>")
        print("示例：python qq_capture_and_reply.py 工作群")
        sys.exit(1)
    
    group_name = sys.argv[1]
    
    print("="*60)
    print("🐧 QQ 截图 + OCR + 自动回复")
    print("="*60)
    
    # 1. 找到 QQ
    qq_window = find_qq_window()
    if not qq_window:
        sys.exit(1)
    
    # 2. 激活窗口
    activate_window(qq_window)
    
    # 3. 搜索群聊
    search_group(group_name)
    
    # 4. 截图聊天区域
    screenshot_path, screenshot = capture_chat_area(qq_window)
    
    # 5. OCR 识别
    ocr_text = simple_ocr(screenshot)
    print(f"\n📝 OCR 结果：\n{ocr_text}\n")
    
    # 6. 分析并生成回复
    reply = analyze_chat(ocr_text)
    print(f"💡 建议回复：{reply}")
    
    # 7. 用户确认
    print("\n" + "="*60)
    print("⚠️  即将发送以上回复到群聊")
    print("="*60)
    
    # 等待用户确认（输入 y 发送，n 取消）
    try:
        user_input = input("\n是否发送？输入 y 发送，n 取消，或输入自定义回复：")
        if user_input.lower() == 'n':
            print("❌ 已取消发送")
            return
        elif user_input.lower() == 'y' or user_input == '':
            # 使用生成的回复
            pass
        else:
            # 使用用户自定义回复
            reply = user_input
            print(f"💬 使用自定义回复：{reply}")
    except KeyboardInterrupt:
        print("\n❌ 已取消")
        return
    
    # 发送回复
    print("\n🚀 发送中...")
    send_reply(reply)
    
    print("="*60)
    print("✅ 完成！")
    print("="*60)

if __name__ == "__main__":
    main()
