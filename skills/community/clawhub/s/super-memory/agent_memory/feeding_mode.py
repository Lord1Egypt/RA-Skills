from __future__ import annotations
"""
feeding_mode.py - 投喂模式实现

支持用户导入各种资料，智能处理并整理
- 支持文本、文件、链接导入
- 智能检测投喂结束
- 自动整理核心内容
- 生成摘要并存储
"""

import time
import logging
import urllib.request
import re
from typing import List, Dict, Optional
from urllib.parse import urlparse
import ipaddress
import socket

from .utils import _validate_url

logger = logging.getLogger(__name__)


def _is_safe_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        hostname = parsed.hostname
        if not hostname:
            return False
        try:
            resolved = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
            for family, _, _, _, sockaddr in resolved:
                ip = ipaddress.ip_address(sockaddr[0])
                if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                    return False
        except (socket.gaierror, ValueError):
            return False
        return True
    except Exception:
        return False


class FeedingMode:
    """
    投喂模式
    
    支持用户导入各种资料，智能处理并整理
    """
    
    def __init__(self, memory_bridge):
        """
        初始化投喂模式
        
        Args:
            memory_bridge: 记忆系统桥接实例
        """
        self.memory_bridge = memory_bridge
        self.is_active = False
        self.feeding_start_time = None
        self.last_feed_time = None
        self.feed_items = []
        self.feed_type_stats = {}
        
        # 时间阈值（秒）
        self.INACTIVITY_THRESHOLD = 300  # 5分钟无活动
        self.MAX_FEED_DURATION = 3600  # 1小时最大投喂时间
    
    def start(self) -> Dict:
        """
        开始投喂模式
        
        Returns:
            dict: 开始结果
        """
        if self.is_active:
            return {"success": False, "message": "投喂模式已经开启"}
        
        self.is_active = True
        self.feeding_start_time = time.time()
        self.last_feed_time = time.time()
        self.feed_items = []
        self.feed_type_stats = {}
        
        logger.info("开启投喂模式")
        return {
            "success": True,
            "message": "投喂模式已开启！您可以开始输入资料、知识或素材。当您长时间没有输入时，我会询问是否结束投喂。",
            "tips": [
                "您可以输入文本内容",
                "您可以粘贴文件路径或URL",
                "您可以直接输入 '结束投喂' 来手动结束"
            ]
        }
    
    def feed(self, content: str, content_type: str = "text") -> Dict:
        """
        投喂内容
        
        Args:
            content: 投喂的内容
            content_type: 内容类型 (text, file, url)
        
        Returns:
            dict: 投喂结果
        """
        if not self.is_active:
            return {"success": False, "message": "投喂模式未开启"}
        
        current_time = time.time()
        self.last_feed_time = current_time
        
        # 处理不同类型的内容
        processed_content = self._process_content(content, content_type)
        
        # 记录投喂项
        feed_item = {
            "content": content,
            "processed_content": processed_content,
            "content_type": content_type,
            "timestamp": current_time,
            "status": "processed"
        }
        
        self.feed_items.append(feed_item)
        
        # 更新类型统计
        self.feed_type_stats[content_type] = self.feed_type_stats.get(content_type, 0) + 1
        
        logger.info(f"投喂内容: {content_type}, 长度: {len(content)}")
        
        return {
            "success": True,
            "message": f"已接收 {content_type} 类型的内容",
            "item_count": len(self.feed_items)
        }
    
    def check_inactivity(self) -> Optional[Dict]:
        """
        检查是否长时间无活动
        
        Returns:
            dict: 活动检查结果，None表示无需处理
        """
        if not self.is_active:
            return None
        
        current_time = time.time()
        time_since_last_feed = current_time - self.last_feed_time
        
        if time_since_last_feed > self.INACTIVITY_THRESHOLD:
            return {
                "type": "inactivity",
                "message": "您已经有一段时间没有投喂新内容了。您是否要结束本次投喂？",
                "options": [
                    {"text": "是的，结束投喂", "action": "end_feeding"},
                    {"text": "继续投喂", "action": "continue_feeding"}
                ]
            }
        
        # 检查是否超过最大投喂时间
        if current_time - self.feeding_start_time > self.MAX_FEED_DURATION:
            return {
                "type": "timeout",
                "message": "本次投喂时间已超过1小时。建议您结束本次投喂并整理已有的内容。",
                "options": [
                    {"text": "结束并整理", "action": "end_feeding"},
                    {"text": "继续投喂", "action": "continue_feeding"}
                ]
            }
        
        return None
    
    def end(self) -> Dict:
        """
        结束投喂模式
        
        Returns:
            dict: 结束结果
        """
        if not self.is_active:
            return {"success": False, "message": "投喂模式未开启"}
        
        try:
            # 生成投喂总结
            summary = self._generate_summary()
            
            # 保存到记忆
            save_result = self.memory_bridge.remember(
                content=summary,
                importance="high",
                topics=["feeding_mode", "summary"]
            )
            
            # 重置状态
            self.is_active = False
            feed_count = len(self.feed_items)
            self.feed_items = []
            
            logger.info(f"结束投喂模式，共处理 {feed_count} 项内容")
            
            if save_result.get("memory_result", {}).get("written", False):
                return {
                    "success": True,
                    "message": f"投喂模式已结束。共处理 {feed_count} 项内容，已生成摘要并保存到记忆中。",
                    "summary": summary
                }
            else:
                return {
                    "success": True,
                    "message": f"投喂模式已结束。共处理 {feed_count} 项内容，但保存失败：" + save_result.get("memory_result", {}).get("reason", "未知错误"),
                    "summary": summary
                }
                
        except Exception as e:
            logger.error(f"结束投喂失败: {e}")
            return {"success": False, "message": f"结束失败：{str(e)}"}
    
    def _process_content(self, content: str, content_type: str) -> str:
        """
        处理不同类型的内容

        Args:
            content: 原始内容
            content_type: 内容类型

        Returns:
            str: 处理后的内容
        """
        if content_type == "text":
            return content.strip()

        elif content_type == "url":
            try:
                if not _is_safe_url(content):
                    logger.warning(f"Blocked unsafe URL: {content}")
                    return f"[BLOCKED URL] {content}"
                _validate_url(content)
                response = urllib.request.urlopen(content, timeout=10)
                html = response.read().decode('utf-8', errors='ignore')
                # 提取文本内容
                text = re.sub(r'<[^>]+>', '', html)
                return text[:1000]  # 限制长度
            except Exception as e:
                logger.warning("feeding_mode: %s", e)
                return f"[URL] {content}"

        elif content_type == "file":
            try:
                # 检查文件扩展名
                ext = os.path.splitext(content)[1].lower()
                
                # 如果是支持的文档格式，使用MediaProcessor处理
                supported_docs = ['.pdf', '.docx', '.txt', '.md', '.rtf']
                if ext in supported_docs:
                    try:
                        from media_processor import MediaProcessor
                        processor = MediaProcessor.auto()
                        result = processor.process(content)
                        if result["success"]:
                            return result["description"][:2000]  # 限制长度
                    except Exception as e:
                        logger.warning("feeding_mode: %s", e)
                
                # 其他文件类型，尝试直接读取
                with open(content, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                return text[:1000]  # 限制长度
            except Exception as e:
                logger.warning("feeding_mode: %s", e)
                return f"[文件] {content}"

        return content
    
    def _generate_summary(self) -> str:
        """
        生成投喂内容的摘要
        
        Returns:
            str: 摘要内容
        """
        if not self.feed_items:
            return "投喂内容为空"
        
        # 统计信息
        total_items = len(self.feed_items)
        content_types = list(self.feed_type_stats.keys())
        
        summary = f"# 投喂模式摘要\n\n"
        summary += f"**投喂统计**\n"
        summary += f"- 总项数: {total_items}\n"
        summary += f"- 内容类型: {', '.join(content_types)}\n"
        for content_type, count in self.feed_type_stats.items():
            summary += f"  - {content_type}: {count}项\n"
        
        # 提取关键内容
        summary += "\n**关键内容**\n"
        for i, item in enumerate(self.feed_items[:5]):  # 取前5项
            content = item['processed_content'][:200]
            summary += f"{i+1}. {content}...\n"
        
        if total_items > 5:
            summary += f"... 还有 {total_items - 5} 项内容\n"
        
        return summary
    
    def get_status(self) -> Dict:
        """
        获取投喂模式状态
        
        Returns:
            dict: 状态信息
        """
        current_time = time.time()
        status = {
            "is_active": self.is_active,
            "feed_count": len(self.feed_items),
            "content_types": list(self.feed_type_stats.keys()),
            "type_stats": self.feed_type_stats
        }
        
        if self.is_active:
            status["feeding_duration"] = current_time - self.feeding_start_time
            status["time_since_last_feed"] = current_time - self.last_feed_time
        
        return status


def create_feeding_mode(memory_bridge):
    """
    创建投喂模式实例
    
    Args:
        memory_bridge: 记忆系统桥接实例
    
    Returns:
        FeedingMode: 投喂模式实例
    """
    return FeedingMode(memory_bridge)
