# -*- coding: utf-8 -*-
"""
飞书机器人
优先使用 OpenClaw 长连接，回退到 Webhook
"""

import json
import urllib.request
import urllib.error
from typing import Tuple


class FeishuBot:
    def __init__(self, default_target: str = "Liam"):
        self.default_target = default_target
        self._message_module = None
        self._check_message_module()
    
    def _check_message_module(self):
        try:
            from message import send
            self._message_module = send
        except ImportError:
            self._message_module = None
    
    def _send_via_openclaw(self, message: str, target: str = None) -> Tuple[bool, str]:
        if self._message_module is None:
            return False, "OpenClaw message 模块不可用"
        
        try:
            target = target or self.default_target
            self._message_module(message=message, channel="feishu", target=target)
            return True, "OpenClaw 长连接发送成功"
        except Exception as e:
            return False, f"OpenClaw 发送失败: {e}"
    
    def _send_via_webhook(self, webhook_url: str, message: str) -> Tuple[bool, str]:
        if not webhook_url:
            return False, "未配置飞书 Webhook"
        
        payload = {
            "msg_type": "interactive",
            "card": {
                "elements": [
                    {
                        "tag": "markdown",
                        "content": message
                    }
                ],
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "🚢 特价预警通知"
                    },
                    "template": "blue"
                }
            }
        }
        
        try:
            data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get('StatusCode') == 0:
                    return True, "Webhook 发送成功"
                else:
                    return False, f"Webhook 发送失败: {result.get('msg')}"
        except urllib.error.URLError as e:
            return False, f"网络错误: {e}"
        except Exception as e:
            return False, f"Webhook 发送异常: {e}"
    
    def send(self, webhook_url: str = None, message: str = "", target: str = None) -> Tuple[bool, str]:
        errors = []
        
        success, msg = self._send_via_openclaw(message, target)
        if success:
            return True, msg
        errors.append(f"长连接: {msg}")
        
        if webhook_url:
            success, msg = self._send_via_webhook(webhook_url, message)
            if success:
                return True, msg
            errors.append(f"Webhook: {msg}")
        
        error_summary = " | ".join(errors)
        return False, f"所有通知方式均失败 - {error_summary}"
    
    def send_text(self, webhook_url: str = None, text: str = "", target: str = None) -> Tuple[bool, str]:
        return self.send(webhook_url, text, target)
    
    def is_openclaw_available(self) -> bool:
        return self._message_module is not None
