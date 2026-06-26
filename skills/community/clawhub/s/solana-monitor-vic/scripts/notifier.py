#!/usr/bin/env python3
"""
Solana Monitor - 通知系统
支持 Telegram、Email 通知

版本：v0.1.0
作者：VIC ai-company
"""

import smtplib
import requests
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List


class TelegramNotifier:
    """Telegram 通知发送器"""
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        """
        初始化 Telegram 通知器
        
        Args:
            bot_token: Telegram Bot Token（从 BotFather 获取）
            chat_id: 接收消息的聊天 ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = "https://api.telegram.org/bot"
    
    def send_message(self, message: str, parse_mode: str = 'HTML') -> bool:
        """
        发送 Telegram 消息
        
        Args:
            message: 消息内容
            parse_mode: 解析模式（HTML/Markdown）
        
        Returns:
            是否发送成功
        """
        if not self.bot_token or not self.chat_id:
            print("❌ Telegram 未配置（缺少 bot_token 或 chat_id）")
            return False
        
        try:
            url = f"{self.api_url}{self.bot_token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('ok'):
                print(f"✅ Telegram 消息发送成功")
                return True
            else:
                print(f"❌ Telegram 发送失败：{result.get('description')}")
                return False
                
        except Exception as e:
            print(f"❌ Telegram 发送异常：{e}")
            return False
    
    def send_price_alert(self, token: str, current_price: float, 
                         target_price: float, condition: str) -> bool:
        """
        发送价格警报消息
        
        Args:
            token: 代币名称
            current_price: 当前价格
            target_price: 目标价格
            condition: 条件（above/below）
        """
        emoji = "🚨" if condition == 'above' else "📉"
        direction = "上涨突破" if condition == 'above' else "下跌突破"
        
        message = f"""
{emoji} <b>价格警报</b>

<b>代币：</b> {token.upper()}
<b>当前价格：</b> ${current_price:,.2f}
<b>目标价格：</b> ${target_price:,.2f}
<b>条件：</b> {direction}

<b>时间：</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#SolanaMonitor #PriceAlert
"""
        
        return self.send_message(message)
    
    def send_whale_alert(self, signature: str, amount: float, 
                         token: str, from_addr: str, to_addr: str) -> bool:
        """
        发送巨鲸转账警报
        
        Args:
            signature: 交易签名
            amount: 金额
            token: 代币
            from_addr: 发送地址
            to_addr: 接收地址
        """
        message = f"""
🐋 <b>巨鲸转账警报</b>

<b>金额：</b> {amount:,.2f} {token.upper()}
<b>来源：</b> <code>{from_addr[:16]}...{from_addr[-8:]}</code>
<b>目标：</b> <code>{to_addr[:16]}...{to_addr[-8:]}</code>

<b>交易：</b> <a href="https://solscan.io/tx/{signature}">查看</a>

<b>时间：</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#SolanaMonitor #WhaleAlert
"""
        
        return self.send_message(message)


class EmailNotifier:
    """Email 通知发送器"""
    
    def __init__(self, smtp_server: str, smtp_port: int, 
                 sender_email: str, sender_password: str):
        """
        初始化 Email 通知器
        
        Args:
            smtp_server: SMTP 服务器地址
            smtp_port: SMTP 端口
            sender_email: 发件人邮箱
            sender_password: 邮箱密码/授权码
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_email(self, to_email: str, subject: str, content: str, 
                   html: bool = False) -> bool:
        """
        发送邮件
        
        Args:
            to_email: 收件人邮箱
            subject: 邮件主题
            content: 邮件内容
            html: 是否 HTML 格式
        
        Returns:
            是否发送成功
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg_type = 'html' if html else 'plain'
            msg.attach(MIMEText(content, msg_type))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email 发送成功：{to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Email 发送失败：{e}")
            return False
    
    def send_price_alert(self, to_email: str, token: str, 
                         current_price: float, target_price: float,
                         condition: str) -> bool:
        """
        发送价格警报邮件
        
        Args:
            to_email: 收件人邮箱
            token: 代币名称
            current_price: 当前价格
            target_price: 目标价格
            condition: 条件
        """
        direction = "上涨突破" if condition == 'above' else "下跌突破"
        emoji = "🚨" if condition == 'above' else "📉"
        
        subject = f"{emoji} {token.upper()} 价格警报 - {direction}"
        
        content = f"""
{emoji} 价格警报

代币：{token.upper()}
当前价格：${current_price:,.2f}
目标价格：${target_price:,.2f}
条件：{direction}

时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
Solana Monitor v0.1.0
VIC ai-company
"""
        
        return self.send_email(to_email, subject, content)


class NotificationManager:
    """通知管理器 - 统一管理所有通知渠道"""
    
    def __init__(self):
        self.telegram: Optional[TelegramNotifier] = None
        self.email: Optional[EmailNotifier] = None
        self.enabled_channels = []
    
    def setup_telegram(self, bot_token: str, chat_id: str):
        """配置 Telegram"""
        self.telegram = TelegramNotifier(bot_token, chat_id)
        self.enabled_channels.append('telegram')
        print(f"✅ Telegram 通知已启用")
    
    def setup_email(self, smtp_server: str, smtp_port: int,
                    sender_email: str, sender_password: str):
        """配置 Email"""
        self.email = EmailNotifier(smtp_server, smtp_port, 
                                   sender_email, sender_password)
        self.enabled_channels.append('email')
        print(f"✅ Email 通知已启用")
    
    def send_alert(self, alert_type: str, **kwargs):
        """
        发送警报到所有启用渠道
        
        Args:
            alert_type: 警报类型（price/whale/system）
            **kwargs: 警报参数
        """
        print(f"\n📢 发送警报：{alert_type}")
        
        # Telegram 通知
        if 'telegram' in self.enabled_channels and self.telegram:
            if alert_type == 'price':
                self.telegram.send_price_alert(
                    kwargs.get('token', ''),
                    kwargs.get('current_price', 0),
                    kwargs.get('target_price', 0),
                    kwargs.get('condition', 'above')
                )
            elif alert_type == 'whale':
                self.telegram.send_whale_alert(
                    kwargs.get('signature', ''),
                    kwargs.get('amount', 0),
                    kwargs.get('token', 'SOL'),
                    kwargs.get('from_addr', ''),
                    kwargs.get('to_addr', '')
                )
        
        # Email 通知
        if 'email' in self.enabled_channels and self.email:
            if alert_type == 'price':
                self.email.send_price_alert(
                    kwargs.get('to_email', ''),
                    kwargs.get('token', ''),
                    kwargs.get('current_price', 0),
                    kwargs.get('target_price', 0),
                    kwargs.get('condition', 'above')
                )
        
        print("✅ 警报发送完成\n")


def main():
    """测试示例"""
    print("📢 Solana Monitor - 通知系统测试")
    print("=" * 50)
    
    # 创建通知管理器
    notifier = NotificationManager()
    
    # 配置 Telegram（需要实际配置）
    # notifier.setup_telegram('YOUR_BOT_TOKEN', 'YOUR_CHAT_ID')
    
    # 配置 Email（需要实际配置）
    # notifier.setup_email('smtp.gmail.com', 587, 'your@gmail.com', 'password')
    
    # 测试消息
    print("\n📋 通知渠道状态:")
    print(f"  已启用：{notifier.enabled_channels}")
    
    # 测试价格警报
    print("\n🧪 测试价格警报...")
    notifier.send_alert(
        'price',
        token='solana',
        current_price=87.62,
        target_price=90.00,
        condition='above',
        to_email='test@example.com'
    )
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")
    print("\n⚠️ 注意：实际使用需要配置 Telegram Bot Token 和 Email SMTP")


if __name__ == "__main__":
    main()
