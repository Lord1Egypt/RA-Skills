#!/usr/bin/env python3
"""
飞书机器人消息推送模块
用于发送爬虫结果到飞书群聊
"""

import json
import logging
import requests
from typing import Optional, List, Dict
from datetime import datetime

from config import LOG_FILE, LOG_LEVEL, LOG_FORMAT

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


class FeishuBot:
    """飞书机器人"""

    def __init__(self, webhook_url: str):
        """
        初始化飞书机器人
        
        Args:
            webhook_url: 飞书机器人 Webhook 地址
        """
        self.webhook_url = webhook_url

    def send_text(self, text: str) -> bool:
        """
        发送纯文本消息
        
        Args:
            text: 消息内容
            
        Returns:
            bool: 发送是否成功
        """
        payload = {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        return self._send(payload)

    def send_markdown(self, title: str, content: str) -> bool:
        """
        发送 Markdown 格式消息
        
        Args:
            title: 消息标题
            content: Markdown 内容
            
        Returns:
            bool: 发送是否成功
        """
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    },
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": content
                        }
                    }
                ]
            }
        }
        return self._send(payload)

    def send_note_card(self, note: Dict) -> bool:
        """
        发送单条笔记卡片
        
        Args:
            note: 笔记数据字典
            
        Returns:
            bool: 发送是否成功
        """
        title = note.get('标题', '无标题')[:50]  # 限制长度
        content = note.get('内容', '')[:100] + "..." if len(note.get('内容', '')) > 100 else note.get('内容', '')
        author = note.get('作者昵称', '未知')
        likes = note.get('点赞数', 0)
        link = note.get('笔记链接', '')

        markdown_content = f"""**{title}**

📝 {content}

👤 作者: {author}
👍 点赞: {likes}
🔗 [查看笔记]({link})
"""

        return self.send_markdown("小红书笔记", markdown_content)

    def send_notes_summary(self, keyword: str, notes: List[Dict]) -> bool:
        """
        发送多条笔记汇总消息
        
        Args:
            keyword: 搜索关键词
            notes: 笔记列表
            
        Returns:
            bool: 发送是否成功
        """
        if not notes:
            return self.send_text(f"未找到关键词「{keyword}」的相关笔记")

        time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 构建汇总内容
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
        return self.send_markdown(f"小红书搜索: {keyword}", content)

    def send_error(self, error_msg: str) -> bool:
        """
        发送错误通知
        
        Args:
            error_msg: 错误信息
            
        Returns:
            bool: 发送是否成功
        """
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "❌ 爬虫运行异常"
                    },
                    "template": "red"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": error_msg
                        }
                    }
                ]
            }
        }
        return self._send(payload)

    def _send(self, payload: dict) -> bool:
        """
        发送消息到飞书
        
        Args:
            payload: 消息体
            
        Returns:
            bool: 发送是否成功
        """
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                self.webhook_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                log.info("✅ 飞书消息发送成功")
                return True
            else:
                log.error(f"飞书消息发送失败: {result.get('msg')}")
                return False
                
        except requests.exceptions.Timeout:
            log.error("飞书消息发送超时")
            return False
        except Exception as e:
            log.error(f"飞书消息发送异常: {e}")
            return False


def create_bot_from_config() -> Optional[FeishuBot]:
    """
    从配置文件创建飞书机器人
    
    Returns:
        FeishuBot: 飞书机器人实例，未配置返回 None
    """
    # 从环境变量或配置文件读取 Webhook 地址
    import os
    
    webhook_url = os.getenv("FEISHU_WEBHOOK_URL")
    
    if not webhook_url:
        # 尝试从文件读取
        config_file = Path(__file__).parent / "feishu_config.txt"
        if config_file.exists():
            webhook_url = config_file.read_text(encoding="utf-8").strip()
    
    if webhook_url:
        return FeishuBot(webhook_url)
    else:
        log.warning("未配置飞书 Webhook 地址")
        return None


# 便捷函数
def send_notes_to_feishu(webhook_url: str, keyword: str, notes: List[Dict]) -> bool:
    """
    便捷函数：发送笔记到飞书
    
    Args:
        webhook_url: 飞书 Webhook 地址
        keyword: 搜索关键词
        notes: 笔记列表
        
    Returns:
        bool: 发送是否成功
    """
    bot = FeishuBot(webhook_url)
    return bot.send_notes_summary(keyword, notes)


if __name__ == "__main__":
    # 测试
    import os
    
    webhook = os.getenv("FEISHU_WEBHOOK_URL")
    if not webhook:
        print("请先设置环境变量 FEISHU_WEBHOOK_URL")
        print("或在当前目录创建 feishu_config.txt 文件，写入 Webhook 地址")
        exit(1)
    
    bot = FeishuBot(webhook)
    
    # 测试发送文本
    bot.send_text("🎉 飞书机器人连接成功！")
    
    # 测试发送 Markdown
    bot.send_markdown(
        "测试消息",
        "**粗体文字**\n\n普通文字\n\n[链接](https://www.xiaohongshu.com)"
    )
    
    # 测试发送笔记
    test_note = {
        "标题": "测试笔记标题",
        "内容": "这是笔记的内容预览...",
        "作者昵称": "测试作者",
        "点赞数": 100,
        "笔记链接": "https://www.xiaohongshu.com"
    }
    bot.send_note_card(test_note)