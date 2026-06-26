#!/usr/bin/env python3
"""
通知模块
支持飞书、钉钉、Telegram等多种通知渠道
"""

import requests
import json
from typing import Dict, Optional
from datetime import datetime


class Notifier:
    """通知器基类"""
    
    def send(self, message: str, **kwargs) -> bool:
        """发送通知，子类实现"""
        raise NotImplementedError


class FeishuNotifier(Notifier):
    """飞书通知器"""
    
    def __init__(self, webhook_url: str):
        """
        初始化飞书通知器
        
        Args:
            webhook_url: 飞书机器人Webhook地址
        """
        self.webhook_url = webhook_url
    
    def send(self, title: str, content: str, 
             status: str = 'info', **kwargs) -> bool:
        """
        发送飞书通知
        
        Args:
            title: 消息标题
            content: 消息内容
            status: 状态类型 (info/success/warning/error)
            
        Returns:
            是否发送成功
        """
        # 根据状态选择颜色
        colors = {
            'info': 'blue',
            'success': 'green',
            'warning': 'orange',
            'error': 'red'
        }
        
        # 构建卡片消息
        card = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"📝 {title}"
                    },
                    "template": colors.get(status, 'blue')
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": content
                        }
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {
                                "tag": "plain_text",
                                "content": f"发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            }
                        ]
                    }
                ]
            }
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=card,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('code') == 0
            return False
            
        except Exception as e:
            print(f"飞书通知发送失败: {e}")
            return False
    
    def send_publish_success(self, task_title: str, note_url: str, 
                           publish_time: datetime):
        """发送发布成功通知"""
        content = f"**标题:** {task_title}\n\n"
        content += f"**状态:** ✅ 发布成功\n\n"
        content += f"**发布时间:** {publish_time.strftime('%Y-%m-%d %H:%M')}\n\n"
        content += f"**笔记链接:** [点击查看]({note_url})"
        
        return self.send(
            title="小红书发布成功",
            content=content,
            status='success'
        )
    
    def send_publish_failure(self, task_title: str, error: str):
        """发送发布失败通知"""
        content = f"**标题:** {task_title}\n\n"
        content += f"**状态:** ❌ 发布失败\n\n"
        content += f"**错误信息:** {error}\n\n"
        content += "请检查账号状态或稍后重试"
        
        return self.send(
            title="小红书发布失败",
            content=content,
            status='error'
        )
    
    def send_daily_summary(self, stats: Dict):
        """发送每日发布统计"""
        content = "**今日发布统计**\n\n"
        content += f"✅ 成功: {stats.get('published', 0)} 篇\n"
        content += f"❌ 失败: {stats.get('failed', 0)} 篇\n"
        content += f"⏰ 待发布: {stats.get('scheduled', 0)} 篇\n\n"
        content += f"成功率: {stats.get('success_rate', 0)}%"
        
        return self.send(
            title="每日发布报告",
            content=content,
            status='info'
        )


class DingTalkNotifier(Notifier):
    """钉钉通知器"""
    
    def __init__(self, webhook_url: str, secret: str = None):
        """
        初始化钉钉通知器
        
        Args:
            webhook_url: 钉钉机器人Webhook地址
            secret: 加签密钥（可选）
        """
        self.webhook_url = webhook_url
        self.secret = secret
    
    def _sign(self, timestamp: str) -> str:
        """生成签名（加签模式下需要）"""
        import hmac
        import hashlib
        import base64
        
        if not self.secret:
            return ''
        
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            self.secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        
        return base64.b64encode(hmac_code).decode('utf-8')
    
    def send(self, title: str, content: str, 
             status: str = 'info', **kwargs) -> bool:
        """发送钉钉通知"""
        import time
        
        timestamp = str(round(time.time() * 1000))
        sign = self._sign(timestamp)
        
        # 根据状态选择颜色
        colors = {
            'info': '#1890ff',
            'success': '#52c41a',
            'warning': '#faad14',
            'error': '#f5222d'
        }
        
        # 构建markdown消息
        message = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"### 📝 {title}\n\n"
                       f"{content}\n\n"
                       f"---\n"
                       f"发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            }
        }
        
        try:
            url = self.webhook_url
            if self.secret:
                url = f"{self.webhook_url}&timestamp={timestamp}&sign={sign}"
            
            response = requests.post(
                url,
                json=message,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('errcode') == 0
            return False
            
        except Exception as e:
            print(f"钉钉通知发送失败: {e}")
            return False
    
    def send_publish_success(self, task_title: str, note_url: str,
                           publish_time: datetime):
        """发送发布成功通知"""
        content = f"**标题:** {task_title}\n\n"
        content += f"**状态:** ✅ 发布成功\n\n"
        content += f"**发布时间:** {publish_time.strftime('%Y-%m-%d %H:%M')}\n\n"
        content += f"**笔记链接:** [{note_url}]({note_url})"
        
        return self.send(
            title="小红书发布成功",
            content=content,
            status='success'
        )
    
    def send_publish_failure(self, task_title: str, error: str):
        """发送发布失败通知"""
        content = f"**标题:** {task_title}\n\n"
        content += f"**状态:** ❌ 发布失败\n\n"
        content += f"**错误信息:** {error}\n\n"
        content += "请检查账号状态或稍后重试"
        
        return self.send(
            title="小红书发布失败",
            content=content,
            status='error'
        )


class TelegramNotifier(Notifier):
    """Telegram通知器"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        初始化Telegram通知器
        
        Args:
            bot_token: Bot Token
            chat_id: 聊天ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send(self, title: str, content: str, **kwargs) -> bool:
        """发送Telegram通知"""
        message = f"<b>{title}</b>\n\n{content}\n\n"
        message += f"<i>发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
        
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('ok', False)
            return False
            
        except Exception as e:
            print(f"Telegram通知发送失败: {e}")
            return False


class NotificationManager:
    """通知管理器"""
    
    def __init__(self, config: Dict):
        """
        初始化通知管理器
        
        Args:
            config: 配置字典
                {
                    'feishu_webhook': 'xxx',
                    'dingtalk_webhook': 'xxx',
                    'dingtalk_secret': 'xxx',
                    'telegram_bot_token': 'xxx',
                    'telegram_chat_id': 'xxx'
                }
        """
        self.notifiers = []
        
        # 初始化飞书
        if config.get('feishu_webhook'):
            self.notifiers.append(FeishuNotifier(config['feishu_webhook']))
        
        # 初始化钉钉
        if config.get('dingtalk_webhook'):
            self.notifiers.append(DingTalkNotifier(
                config['dingtalk_webhook'],
                config.get('dingtalk_secret')
            ))
        
        # 初始化Telegram
        if config.get('telegram_bot_token') and config.get('telegram_chat_id'):
            self.notifiers.append(TelegramNotifier(
                config['telegram_bot_token'],
                config['telegram_chat_id']
            ))
    
    def notify_all(self, title: str, content: str, status: str = 'info'):
        """向所有渠道发送通知"""
        results = []
        for notifier in self.notifiers:
            result = notifier.send(title, content, status)
            results.append({
                'type': type(notifier).__name__,
                'success': result
            })
        return results
    
    def notify_publish_success(self, task_title: str, note_url: str,
                              publish_time: datetime):
        """发送发布成功通知"""
        for notifier in self.notifiers:
            if hasattr(notifier, 'send_publish_success'):
                notifier.send_publish_success(task_title, note_url, publish_time)
    
    def notify_publish_failure(self, task_title: str, error: str):
        """发送发布失败通知"""
        for notifier in self.notifiers:
            if hasattr(notifier, 'send_publish_failure'):
                notifier.send_publish_failure(task_title, error)


# CLI接口
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='通知测试工具')
    parser.add_argument('--channel', choices=['feishu', 'dingtalk', 'telegram'],
                       required=True, help='通知渠道')
    parser.add_argument('--webhook', help='Webhook地址')
    parser.add_argument('--secret', help='加签密钥（钉钉）')
    parser.add_argument('--bot-token', help='Bot Token（Telegram）')
    parser.add_argument('--chat-id', help='Chat ID（Telegram）')
    parser.add_argument('--title', default='测试通知', help='消息标题')
    parser.add_argument('--content', default='这是一条测试消息', help='消息内容')
    
    args = parser.parse_args()
    
    if args.channel == 'feishu':
        if not args.webhook:
            print("错误: 飞书通知需要提供 --webhook")
            exit(1)
        notifier = FeishuNotifier(args.webhook)
    
    elif args.channel == 'dingtalk':
        if not args.webhook:
            print("错误: 钉钉通知需要提供 --webhook")
            exit(1)
        notifier = DingTalkNotifier(args.webhook, args.secret)
    
    elif args.channel == 'telegram':
        if not args.bot_token or not args.chat_id:
            print("错误: Telegram通知需要提供 --bot-token 和 --chat-id")
            exit(1)
        notifier = TelegramNotifier(args.bot_token, args.chat_id)
    
    # 发送测试通知
    result = notifier.send(args.title, args.content)
    print(f"通知发送{'成功' if result else '失败'}")
