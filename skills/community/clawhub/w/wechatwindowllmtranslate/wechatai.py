#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Qwen/Qwen3.5-35B-A3B 模型 API 调用示例 - 整合百度翻译功能
"""
import screeninfo
import sys
import io
import os
# 修复 Windows 控制台中文编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import re
import requests
import json
import random
from hashlib import md5
import pyautogui
import time
import pyperclip
import win32gui
import win32con
import ctypes
from ctypes import wintypes
import math
import threading
#==================== 配置区域 ====================
# Qwen API 配置 - 优先从环境变量读取
QWEN_BASE_URL = os.environ.get('QWEN_BASE_URL', 'https://api-ai.gitcode.com') 
QWEN_API_KEY = os.environ.get('QWEN_API_KEY', '') 
QWEN_URL_PATH = os.environ.get('QWEN_URL_PATH', '/v1/chat/completions')

# 百度翻译 API 配置 - 优先从环境变量读取
BAIDU_APPID = os.environ.get('BAIDU_APPID', '') 
BAIDU_APPKEY = os.environ.get('BAIDU_APPKEY', '') 
BAIDU_ENDPOINT = os.environ.get('BAIDU_ENDPOINT', 'http://api.fanyi.baidu.com') 
BAIDU_PATH = os.environ.get('BAIDU_PATH', '/api/trans/vip/translate')

# 运行配置 - 从环境变量读取
SLEEP_TIME = int(os.environ.get('SLEEP_TIME', '30'))
REPLY_COUNT = int(os.environ.get('REPLY_COUNT', '170'))
# 初始化 
OLD_TEXT = ''  
IDC_IBEAM = 65541
REPLY_COUNT = 170 #回复字数长度
mbti_selected = os.environ.get('mbti_selected', '')    #mbti个性选项
class CURSORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("hCursor", ctypes.c_void_p),  # 使用 c_void_p 代替 HCURSOR
        ("ptScreenPos", wintypes.POINT)
    ]
monitors = screeninfo.get_monitors()

# ==================== 窗口操作聊天内容处理端====================
def activategptwindow():
    """激活任务栏里标题含有'GPT'的窗口"""
    
    def enum_callback(hwnd, results):
        """遍历窗口的回调函数"""
        #  global  windows
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if '微信' in title:
                results.append((hwnd, title))
    windows = []  
    win32gui.EnumWindows(enum_callback, windows)    
    if windows:
        print(f"找到 {len(windows)} 个含'GPT'的窗口：")
        for i, (hwnd, title) in enumerate(windows, 1):
            print(f"  {i}. {title}")
        
        # 激活第一个找到的窗口
        hwnd, title = windows[0]
        # 如果窗口被最小化，先恢复
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        
        # 激活窗口并置于顶层
        win32gui.SetForegroundWindow(hwnd)
        print(f"\n✓ 已激活窗口：{title}")
        time.sleep(0.3)
        return True
    else:
        print("✗ 未找到标题含'GPT'的窗口")
        return False
def sendmessages():      
    if activategptwindow():
        primary = monitors[0]
        pyautogui.click(round(primary.width * 0.5), round(primary.height * 0.8))
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')

def scrollandcheck():
    """滚轮检查程序 - 截取最后两个字"""
    global OLD_TEXT  # 声明使用全局变量
    
    # 1. 激活 GPT 窗口 (新增)
    print("="*50)
    print("开始激活微信窗口...")
    print("="*50)
    if not activategptwindow():
       return ""    
    primary = monitors[0]
    print(f"屏幕分辨率：{primary.width} x {primary.height}")
    x, y = round(primary.width * 0.3), round(primary.height * 0.72)   #鼠标起始屏幕坐标
    #  鼠标滚轮向下滚 3 次
    pyautogui.scroll(-3)
    time.sleep(0.05)
    # 有新消息时的红点的RGB(250, 81, 81)，位置老版 (104,70) 新版(111,93)  如果 g<150 就是有新消息，鼠标原地单击，  鼠标回到开始位置
    newx,newy = round(primary.width * 0.072),round(primary.height * 0.078)  #老版
    color = pyautogui.pixel(newx,newy)
    r, g, b = color[:3]
    if g > 100:
        newx,newy = round(primary.width * 0.077),round(primary.height * 0.103)    #新版
        color = pyautogui.pixel(newx,newy)
        r, g, b = color[:3]
    # 4. 判断如果 g 值低于 100
    if g < 100:
        pyautogui.click(newx,newy)
        time.sleep(0.5)
    pyautogui.moveTo(x, y)
    # 调整鼠标位置寻找最新的聊天信息
    for i in range(round(primary.height * 0.03)):
        # 创建 CURSORINFO 结构
        ci = CURSORINFO()
        ci.cbSize = ctypes.sizeof(CURSORINFO)
        ci.flags = 0  # CURSOR_SHOW
        # 调用 Windows API
        result = ctypes.windll.user32.GetCursorInfo(ctypes.byref(ci))  
        if result:
            cursor_type = ci.hCursor
        
        #  print(cursor_type)
        time.sleep(0.5)
        # 检查是否为 IDC_IBEAM
        if cursor_type == IDC_IBEAM:      
            
            pyautogui.doubleClick()
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
            y = y - 1
            pyautogui.moveTo(x, y)
            time.sleep(0.1)
            pyautogui.doubleClick()
            # 按下 Ctrl + C 复制
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
            
            # 获取剪切板内容
            question = pyperclip.paste() or ""
            
            # 截取 question 最后两个字
            newtext = question[-4:] if len(question) >= 4 else question
            print(f"  原始内容：{question}")
            print(f"  截取最后两字：{newtext}")
            
            # 和 OLD_TEXT 比较，如果不一样就赋值并退出循环
            if newtext != OLD_TEXT:
                OLD_TEXT = newtext
                print(f"  ✓ 新文本已更新：{OLD_TEXT}，退出循环")
                return question 
                
            else:
                print(f"  ✗ 文本未变化 (仍为：{OLD_TEXT})，继续下一次")
                return ""
        else:
            #  mousex, mousey = pyautogui.position()
            y = y - 20
            pyautogui.moveTo(x, y)
           # print(f" 鼠标向上移动 20 像素 (当前：{x}, {y})")
        
        # 循环之间加一点延迟
        time.sleep(0.2)
    print("\n" + "="*50)
    print("程序结束！")
    print("="*50)
    return ""

# ==================== Qwen API 客户端 ====================

class QwenAPI:
    """Qwen 模型 API 客户端"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_delta_content(self, response_text: str) -> str:
        """提取 SSE 响应中 choices[0].delta.content 的内容"""
        content_parts = []
        
        for line in response_text.split('\n'):
            line = line.strip()
            if line.startswith('data:'):
                json_text = line[5:].strip()
                try:
                    data = json.loads(json_text)
                    # 提取 choices[0].delta.content
                    if 'choices' in data and len(data['choices']) > 0:
                        delta = data['choices'][0].get('delta', {})
                    #    print(delta)
                        content = delta.get('content')
                     #   print("提取 SSE 响应")
                        if content:
                            content_parts.append(content)
                except json.JSONDecodeError:
                    pass
        
        # 拼接所有内容
        full_content = ''.join(content_parts)
        
        # 去掉 full_content 里的所有"*"
        full_content = full_content.replace('*', '')
        
        # 只截取"Retrieve Knowledge:"之后的部分
        if "2." in full_content:
            index = full_content.index("2.")
            return full_content[index + len("2."):].strip()
    
        return full_content
    
    def get_message_content(self, response: dict) -> str:
        """提取标准 JSON 响应中 choices[0].message.content 的内容"""
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0].get('message', {}).get('content', '')
        return ''
    
    def chat_completion_stream(
        self,
        messages: list,
        model: str = "Qwen/Qwen3.5-35B-A3B",
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 2048,
        stream: bool = True
    ) -> str:
        """流式响应 - 一次性返回完整内容"""
        url = self.base_url + QWEN_URL_PATH
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            stream=False,  # 获取完整响应
            timeout=60
        )
        
        if response.status_code == 200:
            response.encoding = 'utf-8'
            text = response.text.strip()
            
            if text.startswith('data:'):
                # 如果是 SSE 格式，提取所有 data: 行并拼接
                return self.get_delta_content(text)
            else:
                # 标准 JSON 格式 - 提取 choices[0].message.content
                print(f"标准 JSON 格式 - 提取 choices[0].message.content")
                result = response.json()
                return self.get_message_content(result)
        else:
             raise Exception(f"API 调用失败：{response.status_code} - {response.text}")


# ==================== 百度翻译 API 客户端 ====================

class BaiduTranslate:
    """百度翻译 API 客户端"""
    
    def __init__(self, appid: str, appkey: str):
        self.appid = appid
        self.appkey = appkey
        self.endpoint = BAIDU_ENDPOINT
        self.path = BAIDU_PATH
    
    def _make_md5(self, s: str, encoding: str = 'utf-8') -> str:
        """生成 MD5 签名"""
        return md5(s.encode(encoding)).hexdigest()
    
    def translate(self, q: str, from_lang: str = 'en', to_lang: str = 'zh') -> str:
        """
        翻译文本
        
        Args:
            q: 待翻译文本
            from_lang: 源语言代码 (默认 'en' 英语)
            to_lang: 目标语言代码 (默认 'zh' 中文)
        
        Returns:
            翻译后的中文文本
        """
        # Generate salt and sign
        salt = random.randint(32768, 65536)
        sign = self._make_md5(self.appid + q + str(salt) + self.appkey)
        
        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'appid': self.appid,
            'q': q,
            'from': from_lang,
            'to': to_lang,
            'salt': salt,
            'sign': sign
        }
        
        # Send request
        url = self.endpoint + self.path
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        
        # 检查是否有错误
        if 'error_code' in result:
            raise Exception(f"翻译失败：{result.get('error_msg', '未知错误')}")
        
        # 提取翻译结果
        trans_result = result.get('trans_result', [])
        translated_text = '\n'.join(item.get('dst', '') for item in trans_result)
        
        return translated_text


# ==================== 整合工具函数 ====================

def translate_to_chinese(text: str, from_lang: str = 'en') -> str:
    """
    将英文文本翻译成中文（使用百度翻译）
    
    Args:
        text: 待翻译的英文文本
        from_lang: 源语言代码
    
    Returns:
        翻译后的中文文本
    """
    translator = BaiduTranslate(BAIDU_APPID, BAIDU_APPKEY)
    return translator.translate(text, from_lang=from_lang, to_lang='zh')


def chat_with_qwen(
    user_input: str,
    model: str = "Qwen/Qwen3.5-35B-A3B",
    translate_result: bool = True
) -> str:
    """
    调用 Qwen 模型并可选择翻译结果
    
    Args:
        user_input: 用户输入
        model: 模型名称
        translate_result: 是否将英文回复翻译成中文
    
    Returns:
        AI 的回答（中文或英文）
    """
    client = QwenAPI(QWEN_BASE_URL, QWEN_API_KEY)
    
    messages = [
        {"role": "system", "content": "精简回答 200 字以内，不要输出过程"},
        {"role": "user", "content": user_input}
    ]
    
    # 调用 Qwen API
    response = client.chat_completion_stream(
        messages=messages,
        model=model,
        temperature=0.7,
        max_tokens=2048,
        stream=True
    )
   
    # 如果开启翻译且答案是英文，则翻译成中文
    if translate_result and response.strip():
            try:
                # 简单判断是否是英文（包含较多英文字母）
                
                english_ratio = len(re.findall(r'[a-zA-Z]', response)) / len(response)
                if english_ratio > 0.5:  # 如果英文比例超过 50%，则翻译
                    translated = translate_to_chinese(response)
                    return translated
            except Exception as e:
                print(f"翻译失败：{e}")
        
            return response
    else:
        return "无法获取回答"


# ==================== 主调用 ====================

def example_chat():
    global mbti_selected , BAIDU_APPID , BAIDU_APPKEY , QWEN_BASE_URL , QWEN_API_KEY,QWEN_URL_PATH   #声明
    refresh = 30  #默认30秒刷新一次
    mbti_types = [                                   #聊天风格可选MBTI类型
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
     ] 
    if  QWEN_API_KEY == "":
        print("\n" + "=" * 60)
        print("配置您的BASE_URL，API_KEY，URL_PATH , BAIDU_APPID , BAIDU_APPKEY")
        print("=" * 60)  
        QWEN_BASE_URL = input(f"请输入您的BASE_URL（可选）：{QWEN_BASE_URL}").strip() 
        if   QWEN_BASE_URL == "":
             QWEN_BASE_URL =  "https://api-ai.gitcode.com"                                    
        QWEN_API_KEY = input("请输入您的API_KEY：").strip()    
        QWEN_URL_PATH =  input(f"请输入您的URL_PATH（可选）：{QWEN_URL_PATH}").strip()  
        if   QWEN_URL_PATH == "":     
             QWEN_URL_PATH =  "/v1/chat/completions"        
        BAIDU_APPID = input("请输入您的百度APPID：").strip()                       
        BAIDU_APPKEY = input("请输入您的百度APPKEY：").strip()                   
        print(QWEN_BASE_URL,QWEN_API_KEY,QWEN_URL_PATH,BAIDU_APPID,BAIDU_APPKEY)
    print("\n" + "=" * 60)
    print("选择MBTI人格ai")
    print("=" * 60)        
    if  mbti_selected == "":
    # 打印所有选项
        print("请选择一个人格类型：")
        for i, mbti in enumerate(mbti_types, 1):
            print(f"{i}. {mbti}")

            # 获取用户输入
        try:
            choice = input("请输入选项数字 (1-16)：").strip()
            index = int(choice) - 1
    
            if 0 <= index < len(mbti_types):
                mbti_selected = mbti_types[index]
                print(f"你选择了：{mbti_selected}")
            else:
                print("输入的数字不在有效范围内！")
        except ValueError:
            print("输入无效，请输入数字！")
        rate_types = [5,30,60]                                  #聊天速率      
        print("设置回复速率：\n 1) 5秒 \n 2) 30秒 \n 3) 60秒")
        rate = input("请输入选项数字 (1-3)：").strip()
        if  1<= int(rate) < 4:
            refresh = rate_types[int(rate)]

    question = scrollandcheck()
    if question=="":
       return
    answer = chat_with_qwen(question + "，使用以下MBTI个性语气：" + mbti_selected)
    answer = re.sub(r'\b[a-zA-Z]{1,}\b', '', answer)
    answer = re.sub(r'\d+', '', answer)
    keep_chars = set('，。！？%，：""（）')
    # 清理其他符号（保留必须符号）
    result = []
    for char in answer:
        if (char.isalnum() or 
            char in keep_chars or 
            char.isspace() or 
            '\u4e00' <= char <= '\u9fff' or 
            ord(char) > 127):
            result.append(char)   
    answer = re.sub(r'\s+', ' ', ''.join(result)).strip()
    print(answer)
    pyperclip.copy(answer[-REPLY_COUNT:] if len(answer) >= REPLY_COUNT else answer)  # 只发送截后字符数 
    sendmessages()
    time.sleep(refresh)

if __name__ == "__main__":
    print("微信智能回复（需要先配置ai模型的API地址和API_KEY，百度翻译开放平台的API_ID和API_KEY，根据自身分辨率调整屏幕坐标x,y）\n")
    # 获取屏幕尺寸
    user32 = ctypes.windll.user32

    # 边缘检测阈值（距离边缘多少像素算"在边缘"）
    EDGE_THRESHOLD = 5
    last_x, last_y = -1, -1
    try:
        while activategptwindow():
             # 获取当前鼠标位置
            point = wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(point))     
            current_x, current_y = point.x, point.y
            # 检测是否移动到边缘
            if last_x != -1:  # 不是第一次
                if current_x <= EDGE_THRESHOLD and last_x > EDGE_THRESHOLD:
                    print(f"[边缘检测] 鼠标移动到**屏幕最左边** (x={current_x})")
                    break
            last_x, last_y = current_x, current_y
            example_chat()       
    except KeyboardInterrupt:
        print("\n\n[中断] 用户按 Ctrl+C 取消了操作")
    except Exception as e:
        print(f"\n[错误] 脚本执行失败：{e}")
        import traceback
        traceback.print_exc()

