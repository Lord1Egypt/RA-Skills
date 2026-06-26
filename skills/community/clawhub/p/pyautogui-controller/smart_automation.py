#!/usr/bin/env python3
"""
智能自动化 - 基于自然语言理解的自动化控制器
能够理解用户意图，自动识别页面元素并执行操作
"""

import pyautogui
import time
import re
from typing import Optional, Dict, List, Callable
from automation_core import AutomationCore
from vision_controller import VisionController

class SmartAutomation:
    """智能自动化控制器"""
    
    def __init__(self):
        self.core = AutomationCore()
        self.vision = VisionController()
        self.intent_parser = IntentParser()
        self.action_executor = ActionExecutor(self.core, self.vision)
    
    def execute(self, command: str) -> Dict:
        """
        执行自然语言命令
        
        Args:
            command: 自然语言命令，如"打开 Chrome 并访问 https://example.com"
        
        Returns:
            执行结果
        """
        print(f"🎯 解析命令: {command}")
        
        # 1. 解析意图
        intent = self.intent_parser.parse(command)
        print(f"📋 识别意图: {intent}")
        
        # 2. 执行动作
        result = self.action_executor.execute_intent(intent)
        
        return result


class IntentParser:
    """意图解析器 - 将自然语言转换为结构化意图"""
    
    def __init__(self):
        self.patterns = {
            "open_browser": [
                r"打开.*浏览器",
                r"打开.*chrome",
                r"启动.*浏览器",
                r"访问.*网站",
            ],
            "navigate": [
                r"进入.*(https?://\S+)",
                r"访问.*(https?://\S+)",
                r"打开.*(https?://\S+)",
                r"跳转到.*(https?://\S+)",
            ],
            "click_element": [
                r"点击.*(按钮|链接|元素)",
                r"按下.*(确认|确定|OK)",
                r"选择.*(复选框|选项)",
            ],
            "input_text": [
                r"输入.*内容",
                r"填写.*文本",
                r"发送.*消息",
            ],
            "handle_captcha": [
                r"处理.*验证码",
                r"验证.*人机",
                r"点击.*验证",
            ],
            "verify_human": [
                r"确认.*人机",
                r"点击.*确认",
                r"勾选.*我已知晓",
                r"同意.*条款",
            ],
        }
    
    def parse(self, command: str) -> Dict:
        """
        解析命令
        
        Returns:
            {
                "action": "动作类型",
                "params": {"参数名": "参数值"},
                "steps": ["步骤1", "步骤2", ...]
            }
        """
        intent = {
            "original": command,
            "action": None,
            "params": {},
            "steps": [],
        }
        
        # 检测打开浏览器
        if self._match_pattern(command, "open_browser"):
            intent["action"] = "open_browser"
            intent["steps"].append("activate_chrome")
        
        # 检测导航
        url_match = self._extract_url(command)
        if url_match:
            intent["action"] = "navigate"
            intent["params"]["url"] = url_match
            intent["steps"].append(f"navigate_to:{url_match}")
        
        # 检测人机验证
        if self._match_pattern(command, "verify_human") or self._match_pattern(command, "handle_captcha"):
            intent["steps"].append("handle_verification")
        
        # 检测输入
        if self._match_pattern(command, "input_text"):
            text = self._extract_text_to_input(command)
            if text:
                intent["params"]["input_text"] = text
                intent["steps"].append(f"input_text:{text}")
        
        # 如果没有识别到具体动作，设为通用执行
        if not intent["action"]:
            intent["action"] = "general"
        
        return intent
    
    def _match_pattern(self, text: str, pattern_key: str) -> bool:
        """匹配模式"""
        if pattern_key not in self.patterns:
            return False
        
        for pattern in self.patterns[pattern_key]:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _extract_url(self, text: str) -> Optional[str]:
        """提取 URL"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        match = re.search(url_pattern, text)
        return match.group(0) if match else None
    
    def _extract_text_to_input(self, text: str) -> Optional[str]:
        """提取要输入的文本"""
        # 简单实现：提取引号内的内容
        match = re.search(r'["\']([^"\']+)["\']', text)
        return match.group(1) if match else None


class ActionExecutor:
    """动作执行器"""
    
    def __init__(self, core: AutomationCore, vision: VisionController):
        self.core = core
        self.vision = vision
        self.handlers = {
            "activate_chrome": self._activate_chrome,
            "navigate_to": self._navigate_to,
            "handle_verification": self._handle_verification,
            "input_text": self._input_text,
        }
    
    def execute_intent(self, intent: Dict) -> Dict:
        """执行意图"""
        results = []
        
        for step in intent.get("steps", []):
            print(f"  ▶ 执行: {step}")
            
            # 解析步骤
            if ":" in step:
                action, param = step.split(":", 1)
            else:
                action = step
                param = None
            
            # 执行处理
            if action in self.handlers:
                try:
                    result = self.handlers[action](param)
                    results.append({"step": step, "result": result, "success": True})
                except Exception as e:
                    results.append({"step": step, "error": str(e), "success": False})
            else:
                results.append({"step": step, "error": "Unknown action", "success": False})
        
        return {
            "intent": intent,
            "results": results,
            "success": all(r.get("success", False) for r in results),
        }
    
    def _activate_chrome(self, param=None):
        """激活 Chrome 浏览器"""
        print("    激活 Chrome...")
        
        # 方法1: 点击任务栏图标
        pyautogui.click(400, 1050)
        time.sleep(1)
        
        # 方法2: 使用 Alt+Tab 切换
        pyautogui.keyDown('alt')
        pyautogui.keyDown('tab')
        pyautogui.keyUp('tab')
        pyautogui.keyUp('alt')
        time.sleep(0.5)
        
        return {"status": "activated"}
    
    def _navigate_to(self, url: str):
        """导航到指定 URL"""
        print(f"    导航到: {url}")
        
        # 点击地址栏
        pyautogui.click(500, 50)
        time.sleep(0.3)
        
        # 输入 URL
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write(url, interval=0.01)
        time.sleep(0.3)
        
        # 回车
        pyautogui.press('enter')
        time.sleep(3)  # 等待页面加载
        
        return {"status": "navigated", "url": url}
    
    def _handle_verification(self, param=None):
        """处理人机验证"""
        print("    检测人机验证...")
        
        # 分析页面状态
        state = self.vision.analyze_page_state()
        
        # 检测验证码
        if state.get("has_captcha"):
            print("    发现验证码，尝试处理...")
            # TODO: 验证码识别和点击
            # 临时方案：等待用户手动处理
            time.sleep(5)
        
        # 检测复选框
        if state.get("has_checkbox"):
            print("    发现复选框，点击确认...")
            checkbox_pos = self.vision.find_checkbox()
            if checkbox_pos:
                self.core.mouse.click(checkbox_pos[0], checkbox_pos[1])
                time.sleep(0.5)
        
        # 检测确认按钮
        button_pos = self.vision.find_button_by_text(["确认", "确定", "OK", "我已知晓", "同意"])
        if button_pos:
            print(f"    发现确认按钮，点击...")
            self.core.mouse