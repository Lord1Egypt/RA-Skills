#!/usr/bin/env python3
"""
消息处理器 - 处理 WhatsApp 消息，进行关键词正则匹配
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class MessageProcessor:
    """消息处理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        处理单个消息，检查是否匹配关键词
        返回处理后的消息（如果匹配），否则返回 None
        """
        try:
            content = message.get("content", "").strip()
            if not content:
                return None
            
            # 获取消息元数据
            processed_msg = self._extract_message_metadata(message)
            
            # 检查是否匹配关键词（支持正则表达式）
            matched_keywords = self._check_keywords_match(content, processed_msg.get("target_config", {}))
            
            if matched_keywords:
                # 找到匹配的关键词
                processed_msg["matched"] = True
                processed_msg["matched_keywords"] = matched_keywords
                processed_msg["match_count"] = len(matched_keywords)
                
                # 提取关键词上下文
                processed_msg["context"] = self._extract_keyword_context(content, matched_keywords)
                
                self.logger.debug(f"消息匹配到关键词: {matched_keywords}")
                return processed_msg
            else:
                # 没有匹配到关键词
                return None
                
        except Exception as e:
            self.logger.error(f"处理消息时出错: {str(e)}", exc_info=True)
            return None
    
    def _extract_message_metadata(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """提取消息元数据"""
        metadata = {
            "timestamp": message.get("timestamp", datetime.now().isoformat()),
            "sender": message.get("sender", ""),
            "source": message.get("source", ""),
            "content": message.get("content", ""),
            "type": message.get("type", "text"),
            "message_id": message.get("message_id", ""),
            "chat_id": message.get("chat_id", ""),
            "chat_name": message.get("chat_name", ""),
            "target_config": message.get("target_config", {}),
            "priority": message.get("priority", "medium"),
            "matched": False,
            "matched_keywords": [],
            "match_count": 0,
            "context": ""
        }
        
        # 添加附件信息（如果有）
        if "attachment" in message:
            metadata["attachment"] = message["attachment"]
            metadata["attachment_type"] = message.get("attachment_type", "")
        
        # 添加聊天链接（如果有）
        if metadata["chat_id"]:
            metadata["chat_link"] = f"whatsapp://chat?code={metadata['chat_id']}"
        
        return metadata
    
    def _check_keywords_match(self, content: str, target_config: Dict[str, Any]) -> List[str]:
        """检查消息内容是否匹配关键词（支持正则表达式）"""
        matched_keywords = []
        
        # 获取关键词列表
        keywords = target_config.get("keywords", [])
        keyword_patterns = target_config.get("keyword_patterns", [])
        
        # 检查简单关键词
        for keyword in keywords:
            if keyword and keyword.lower() in content.lower():
                matched_keywords.append(keyword)
        
        # 检查正则表达式模式
        for pattern in keyword_patterns:
            try:
                if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                    matched_keywords.append(f"正则: {pattern}")
            except re.error as e:
                self.logger.warning(f"正则表达式错误: {pattern} - {str(e)}")
        
        # 去重
        return list(set(matched_keywords))
    
    def _extract_keyword_context(self, content: str, keywords: List[str], 
                                context_chars: int = 50) -> str:
        """提取关键词上下文"""
        if not keywords:
            return ""
        
        # 找到所有关键词位置
        positions = []
        content_lower = content.lower()
        
        for keyword in keywords:
            # 清理正则标记
            clean_keyword = keyword.replace("正则: ", "")
            
            try:
                # 尝试作为正则匹配
                pattern = clean_keyword
                for match in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
                    positions.append((match.start(), match.end()))
            except re.error:
                # 如果正则失败，作为普通文本搜索
                start = 0
                while True:
                    idx = content_lower.find(clean_keyword.lower(), start)
                    if idx == -1:
                        break
                    positions.append((idx, idx + len(clean_keyword)))
                    start = idx + 1
        
        if not positions:
            return ""
        
        # 合并重叠或邻近的位置
        positions.sort()
        merged = []
        current_start, current_end = positions[0]
        
        for start, end in positions[1:]:
            if start <= current_end + context_chars:  # 邻近的位置合并
                current_end = max(current_end, end)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = start, end
        
        merged.append((current_start, current_end))
        
        # 提取上下文
        contexts = []
        for start, end in merged:
            context_start = max(0, start - context_chars)
            context_end = min(len(content), end + context_chars)
            
            # 提取上下文，确保不在单词中间截断
            if context_start > 0:
                # 向前找到空格或句首
                while context_start > 0 and content[context_start] not in (' ', '\n', '\t', '.', ',', '!', '?'):
                    context_start -= 1
            
            if context_end < len(content):
                # 向后找到空格或句尾
                while context_end < len(content) and content[context_end] not in (' ', '\n', '\t', '.', ',', '!', '?'):
                    context_end += 1
            
            context = content[context_start:context_end].strip()
            
            # 添加省略号
            if context_start > 0:
                context = "..." + context
            if context_end < len(content):
                context = context + "..."
            
            contexts.append(context)
        
        return " | ".join(contexts)
    
    def process_batch_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量处理消息"""
        matched_messages = []
        
        for msg in messages:
            processed = self.process_message(msg)
            if processed:
                matched_messages.append(processed)
        
        self.logger.info(f"批量处理完成: {len(messages)} 条消息，匹配 {len(matched_messages)} 条")
        return matched_messages
    
    def extract_keywords_from_config(self, targets_config: Dict[str, Any]) -> Dict[str, List[str]]:
        """从配置中提取所有关键词和模式"""
        keywords_by_target = {}
        
        if "targets" not in targets_config:
            return keywords_by_target
        
        for target in targets_config["targets"]:
            if not target.get("enabled", False):
                continue
            
            target_name = target.get("name", "unknown")
            keywords = target.get("keywords", [])
            patterns = target.get("keyword_patterns", [])
            
            all_patterns = keywords + patterns
            if all_patterns:
                keywords_by_target[target_name] = all_patterns
        
        return keywords_by_target
    
    def analyze_message_priority(self, message: Dict[str, Any], matched_keywords: List[str]) -> str:
        """分析消息优先级"""
        content = message.get("content", "").lower()
        target_priority = message.get("priority", "medium")
        
        # 高优先级关键词
        high_priority_keywords = ["urgent", "紧急", "critical", "重要", "asap", "立即", "马上", "立刻"]
        medium_priority_keywords = ["important", "重要", "需要注意", "提醒", "deadline", "截止"]
        
        # 检查消息中的优先级关键词
        for keyword in high_priority_keywords:
            if keyword in content:
                return "high"
        
        for keyword in medium_priority_keywords:
            if keyword in content:
                return "medium"
        
        # 返回目标配置的优先级
        return target_priority
    
    def filter_messages_by_time(self, messages: List[Dict[str, Any]], 
                               hours: int = 24) -> List[Dict[str, Any]]:
        """按时间过滤消息"""
        if not messages:
            return []
        
        filtered = []
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        for msg in messages:
            timestamp = msg.get("timestamp")
            if not timestamp:
                continue
            
            try:
                # 解析时间戳
                if isinstance(timestamp, (int, float)):
                    msg_time = timestamp
                else:
                    # 尝试解析 ISO 格式
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    msg_time = dt.timestamp()
                
                if msg_time >= cutoff_time:
                    filtered.append(msg)
            except Exception:
                # 如果时间解析失败，保留消息
                filtered.append(msg)
        
        return filtered
    
    def deduplicate_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去重消息（基于消息ID和内容）"""
        seen = set()
        deduplicated = []
        
        for msg in messages:
            # 创建唯一标识符
            msg_id = msg.get("message_id", "")
            content_hash = hash(msg.get("content", ""))
            identifier = f"{msg_id}_{content_hash}"
            
            if identifier not in seen:
                seen.add(identifier)
                deduplicated.append(msg)
        
        return deduplicated