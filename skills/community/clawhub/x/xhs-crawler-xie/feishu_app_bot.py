#!/usr/bin/env python3
"""
飞书企业自建应用机器人
使用 App ID + App Secret 调用飞书 OpenAPI
支持自动刷新 access_token
"""

import time
import json
import logging
import requests
import base64
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime

from config import (
    FEISHU_APP_ID,
    FEISHU_APP_SECRET,
    LOG_FILE,
    LOG_LEVEL,
    LOG_FORMAT,
)

# 初始化日志
LOG_FILE.parent.mkdir(exist_ok=True)
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


class FeishuAppBot:
    """飞书企业自建应用机器人"""

    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        初始化飞书应用机器人
        
        Args:
            app_id: 飞书应用 App ID，默认从配置读取
            app_secret: 飞书应用 App Secret，默认从配置读取
        """
        self.app_id = app_id or FEISHU_APP_ID
        self.app_secret = app_secret or FEISHU_APP_SECRET
        self.access_token = None
        self.token_expire_time = 0

    def _get_tenant_access_token(self) -> str:
        """
        获取 tenant_access_token
        会自动处理过期刷新
        
        Returns:
            str: 有效的 access_token
        """
        # 检查当前 token 是否有效
        if self.access_token and time.time() < self.token_expire_time - 60:
            return self.access_token

        # 重新获取 token
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        
        try:
            response = requests.post(
                url,
                json={
                    "app_id": self.app_id,
                    "app_secret": self.app_secret
                },
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                self.access_token = result["tenant_access_token"]
                # token 有效期通常为 2 小时，这里设置 1.5 小时后刷新
                expire = result.get("expire", 7200)
                self.token_expire_time = time.time() + expire
                log.info("✅ 飞书 access_token 获取成功")
                return self.access_token
            else:
                log.error(f"获取 access_token 失败: {result}")
                raise Exception(f"获取 access_token 失败: {result.get('msg')}")

        except Exception as e:
            log.error(f"获取 access_token 异常: {e}")
            raise

    def send_text_to_chat(self, chat_id: str, text: str) -> bool:
        """
        发送文本消息到指定群聊
        
        Args:
            chat_id: 群聊 ID（以 'oc_' 开头）
            text: 消息内容
            
        Returns:
            bool: 发送是否成功
        """
        try:
            token = self._get_tenant_access_token()
            url = "https://open.feishu.cn/open-apis/im/v1/messages"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            params = {"receive_id_type": "chat_id"}
            
            payload = {
                "receive_id": chat_id,
                "msg_type": "text",
                "content": json.dumps({"text": text})
            }

            response = requests.post(
                url,
                headers=headers,
                params=params,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                log.info("✅ 飞书消息发送成功")
                return True
            else:
                log.error(f"飞书消息发送失败: {result}")
                return False

        except Exception as e:
            log.error(f"发送消息异常: {e}")
            return False

    def send_markdown_to_chat(self, chat_id: str, title: str, content: str) -> bool:
        """
        发送 Markdown 卡片消息到指定群聊
        
        Args:
            chat_id: 群聊 ID
            title: 卡片标题
            content: Markdown 内容
            
        Returns:
            bool: 发送是否成功
        """
        try:
            token = self._get_tenant_access_token()
            url = "https://open.feishu.cn/open-apis/im/v1/messages"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            params = {"receive_id_type": "chat_id"}
            
            # 构建卡片消息
            card_content = {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {"tag": "plain_text", "content": title},
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {"tag": "lark_md", "content": content}
                    }
                ]
            }
            
            payload = {
                "receive_id": chat_id,
                "msg_type": "interactive",
                "content": json.dumps(card_content)
            }

            response = requests.post(
                url,
                headers=headers,
                params=params,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                log.info("✅ 飞书卡片消息发送成功")
                return True
            else:
                log.error(f"飞书卡片消息发送失败: {result}")
                return False

        except Exception as e:
            log.error(f"发送卡片消息异常: {e}")
            return False

    def upload_image(self, image_path: Path) -> Optional[str]:
        """
        上传图片到飞书，获取 image_key
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            str: 图片的 image_key，失败返回 None
        """
        try:
            token = self._get_tenant_access_token()
            url = "https://open.feishu.cn/open-apis/im/v1/images"
            
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            # 读取图片文件
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # 构建 multipart 表单
            files = {
                "image": (image_path.name, image_data, "image/png")
            }
            data = {
                "image_type": "message"
            }
            
            response = requests.post(
                url,
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                image_key = result.get("data", {}).get("image_key")
                log.info(f"✅ 图片上传成功: {image_key}")
                return image_key
            else:
                log.error(f"图片上传失败: {result}")
                return None
                
        except Exception as e:
            log.error(f"上传图片异常: {e}")
            return False

    def send_image_to_chat(self, chat_id: str, image_path: Path) -> bool:
        """
        发送图片消息到指定群聊
        
        Args:
            chat_id: 群聊 ID
            image_path: 图片文件路径
            
        Returns:
            bool: 发送是否成功
        """
        # 先上传图片获取 image_key
        image_key = self.upload_image(image_path)
        if not image_key:
            return False
        
        try:
            token = self._get_tenant_access_token()
            url = "https://open.feishu.cn/open-apis/im/v1/messages"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            params = {"receive_id_type": "chat_id"}
            
            payload = {
                "receive_id": chat_id,
                "msg_type": "image",
                "content": json.dumps({"image_key": image_key})
            }
            
            response = requests.post(
                url,
                headers=headers,
                params=params,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                log.info("✅ 图片消息发送成功")
                return True
            else:
                log.error(f"图片消息发送失败: {result}")
                return False
                
        except Exception as e:
            log.error(f"发送图片消息异常: {e}")
            return False

    def send_notes_summary(self, chat_id: str, keyword: str, notes: List[Dict]) -> bool:
        """
        发送笔记汇总到飞书群
        
        Args:
            chat_id: 群聊 ID
            keyword: 搜索关键词
            notes: 笔记列表
            
        Returns:
            bool: 发送是否成功
        """
        if not notes:
            return self.send_text_to_chat(chat_id, f"❌ 未找到关键词「{keyword}」的相关笔记")

        time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 构建 Markdown 内容
        content_lines = [
            f"**📱 小红书搜索报告**",
            f"",
            f"🔍 关键词: {keyword}",
            f"📊 共找到: {len(notes)} 条笔记",
            f"⏰ 时间: {time_str}",
            f"",
            f"---",
            f"",
        ]

        for i, note in enumerate(notes, 1):
            title = note.get('标题', '无标题')[:40]
            author = note.get('作者昵称', '未知')
            likes = note.get('点赞数', 0)
            link = note.get('笔记链接', '')
            
            content_lines.append(f"**{i}. {title}**")
            content_lines.append(f"👤 {author} | 👍 {likes}")
            content_lines.append(f"🔗 [查看笔记]({link})")
            content_lines.append("")

        content = "\n".join(content_lines)
        return self.send_markdown_to_chat(chat_id, f"小红书搜索: {keyword}", content)

    def get_chat_list(self) -> List[Dict]:
        """
        获取机器人所在的群聊列表
        
        Returns:
            list: 群聊列表
        """
        try:
            token = self._get_tenant_access_token()
            url = "https://open.feishu.cn/open-apis/im/v1/chats"
            
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                items = result.get("data", {}).get("items", [])
                log.info(f"获取到 {len(items)} 个群聊")
                return items
            else:
                log.error(f"获取群聊列表失败: {result}")
                return []

        except Exception as e:
            log.error(f"获取群聊列表异常: {e}")
            return []


def send_notes_to_feishu(chat_id: str, keyword: str, notes: List[Dict]) -> bool:
    """
    便捷函数：发送笔记到飞书群
    
    Args:
        chat_id: 群聊 ID（以 'oc_' 开头）
        keyword: 搜索关键词
        notes: 笔记列表
        
    Returns:
        bool: 发送是否成功
    """
    bot = FeishuAppBot()
    return bot.send_notes_summary(chat_id, keyword, notes)


def send_image_to_feishu(chat_id: str, image_path: str) -> bool:
    """
    便捷函数：发送图片到飞书群
    
    Args:
        chat_id: 群聊 ID
        image_path: 图片文件路径
        
    Returns:
        bool: 发送是否成功
    """
    bot = FeishuAppBot()
    return bot.send_image_to_chat(chat_id, Path(image_path))


if __name__ == "__main__":
    # 测试
    print("🚀 测试飞书应用机器人")
    print()
    
    bot = FeishuAppBot()
    
    # 获取群聊列表
    print("📋 获取群聊列表...")
    chats = bot.get_chat_list()
    print(f"找到 {len(chats)} 个群聊:")
    for chat in chats:
        print(f"  - {chat.get('name')}: {chat.get('chat_id')}")
    print()
    
    # 测试发送消息
    test_chat_id = "oc_29fbba0871ab7371a4c1a1ebe0350dac"  # 你的测试群
    
    print(f"💬 发送测试消息到群: {test_chat_id}")
    success = bot.send_text_to_chat(test_chat_id, "🎉 飞书应用机器人连接成功！")
    
    if success:
        print("✅ 消息发送成功，请检查飞书群是否收到")
    else:
        print("❌ 消息发送失败")
