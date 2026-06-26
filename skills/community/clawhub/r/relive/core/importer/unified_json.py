import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

from core.importer.base import BaseImporter, UnifiedMessage


class UnifiedJsonImporter(BaseImporter):
    """
    统一的JSON导入器，支持自动检测多种聊天记录格式：
    - QQ 标准 JSON
    - WhatsApp JSON
    
    通过内容自动识别格式，无需手动指定文件类型。
    """
    
    FORMAT_QQ = "qq"
    FORMAT_WHATSAPP = "whatsapp"
    FORMAT_GENERIC = "generic"
    
    def __init__(self):
        self._format_detectors: List[Callable[[Dict], str]] = [
            self._detect_qq_format,
            self._detect_whatsapp_format,
        ]
        self._parsers: Dict[str, Callable[[Dict], List[UnifiedMessage]]] = {
            self.FORMAT_QQ: self._parse_qq_format,
            self.FORMAT_WHATSAPP: self._parse_whatsapp_format,
            self.FORMAT_GENERIC: self._parse_generic_format,
        }
    
    def _detect_format(self, data: Dict) -> str:
        """自动检测JSON格式"""
        for detector in self._format_detectors:
            fmt = detector(data)
            if fmt:
                return fmt
        return self.FORMAT_GENERIC
    
    def _detect_qq_format(self, data: Dict) -> Optional[str]:
        """检测QQ格式"""
        messages = data.get("messages") or []
        if not messages:
            return None
        
        first_msg = messages[0] if messages else {}
        
        has_sender = "sender" in first_msg
        has_sender_name = isinstance(first_msg.get("sender"), dict) and "name" in first_msg.get("sender", {})
        has_content_text = "content" in first_msg and isinstance(first_msg.get("content"), dict) and "text" in first_msg.get("content", {})
        has_time = "time" in first_msg or "timestamp" in first_msg
        
        if has_sender and has_content_text and has_time:
            return self.FORMAT_QQ
        return None
    
    def _detect_whatsapp_format(self, data: Dict) -> Optional[str]:
        """检测WhatsApp JSON格式"""
        if not data:
            return None
        
        first_value = next(iter(data.values()) if data else [])
        
        if isinstance(first_value, dict):
            if "messages" in first_value or "from_me" in first_value:
                return self.FORMAT_WHATSAPP
        
        return None
    
    def _parse_qq_format(self, data: Dict) -> List[UnifiedMessage]:
        """解析QQ格式"""
        messages: List[UnifiedMessage] = []
        raw_messages = data.get("messages") or []
        
        for msg in raw_messages:
            sender_info = msg.get("sender") or {}
            sender = (
                sender_info.get("name")
                or sender_info.get("uid")
                or sender_info.get("uin")
                or "unknown"
            )
            
            content_info = msg.get("content") or {}
            content_text = (content_info.get("text") or "").strip()
            
            timestamp = msg.get("time") or msg.get("timestamp")
            
            if not sender or not content_text:
                continue
            
            messages.append(UnifiedMessage(
                sender=sender,
                content=content_text,
                timestamp=str(timestamp) if timestamp is not None else None,
                metadata={
                    "platform": "qq",
                    "msg_id": msg.get("id"),
                    "msg_type": msg.get("type"),
                }
            ))
        
        return messages
    
    def _parse_whatsapp_format(self, data: Dict) -> List[UnifiedMessage]:
        """解析WhatsApp JSON格式"""
        messages: List[UnifiedMessage] = []
        
        for chat_id, chat_data in data.items():
            if not isinstance(chat_data, dict):
                continue
            
            chat_messages = chat_data.get("messages") or []
            chat_name = chat_data.get("name", "")
            
            for msg in chat_messages:
                is_from_me = msg.get("from_me", False)
                sender = msg.get("sender") if not is_from_me else "ME"
                
                if not sender and is_from_me:
                    sender = "ME"
                if not sender:
                    sender = chat_name or "unknown"
                
                content = msg.get("data") or msg.get("text") or ""
                
                timestamp = msg.get("timestamp")
                
                media_type = None
                if msg.get("media"):
                    media_type = msg.get("type")
                    if msg.get("caption"):
                        content = f"[{media_type}] {msg.get('caption')}"
                    else:
                        content = f"[{media_type}]"
                
                content_text = str(content).strip() if content else ""
                
                if not content_text:
                    continue
                
                messages.append(UnifiedMessage(
                    sender=str(sender),
                    content=content_text,
                    timestamp=str(timestamp) if timestamp is not None else None,
                    metadata={
                        "platform": "whatsapp",
                        "chat_id": chat_id,
                        "from_me": is_from_me,
                    }
                ))
        
        return messages
    
    def _parse_generic_format(self, data: Dict) -> List[UnifiedMessage]:
        """解析通用格式 - 支持最常见的JSON结构"""
        messages: List[UnifiedMessage] = []
        
        def extract_messages(obj: Any, path: str = "") -> List[Dict]:
            if isinstance(obj, list):
                result = []
                for item in obj:
                    if isinstance(item, dict):
                        if _has_message_fields(item):
                            result.append(item)
                        else:
                            result.extend(extract_messages(item, path))
                    elif isinstance(item, list):
                        result.extend(extract_messages(item, path))
                return result
            
            if isinstance(obj, dict):
                if _has_message_fields(obj):
                    return [obj]
                
                for key in ["messages", "msg_list", "chat", "chats", "data", "items", "records"]:
                    if key in obj:
                        return extract_messages(obj[key], f"{path}.{key}")
                
                for value in obj.values():
                    result = extract_messages(value, path)
                    if result:
                        return result
            
            return []
        
        def _has_message_fields(item: Dict) -> bool:
            has_content = any(k for k in item.keys() if "content" in k.lower() or "text" in k.lower() or "message" in k.lower())
            has_sender = any(k for k in item.keys() if "sender" in k.lower() or "from" in k.lower() or "user" in k.lower() or "name" in k.lower())
            has_time = any(k for k in item.keys() if "time" in k.lower() or "date" in k.lower())
            return has_content and (has_sender or has_time)
        
        raw_messages = extract_messages(data)
        
        for msg in raw_messages:
            content = _extract_field(msg, ["content", "text", "message", "msg", "data"])
            sender = _extract_field(msg, ["sender", "from", "user", "name", "username", "nickname"])
            timestamp = _extract_field(msg, ["timestamp", "time", "date", "datetime", "created_at"])
            
            if not sender or not content:
                continue
            
            messages.append(UnifiedMessage(
                sender=str(sender),
                content=str(content).strip(),
                timestamp=str(timestamp) if timestamp else None,
                metadata={"platform": "unknown"}
            ))
        
        return messages
    
    def parse(self, file_path: Path) -> List[UnifiedMessage]:
        """解析JSON文件，自动检测格式"""
        with open(file_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        if isinstance(data, list):
            data = {"messages": data}
        
        format_type = self._detect_format(data)
        
        parser = self._parsers.get(format_type, self._parse_generic_format)
        return parser(data)


def _extract_field(msg: Dict, candidates: List[str]) -> Optional[str]:
    """从消息中提取指定候选字段"""
    for key in candidates:
        for k, v in msg.items():
            if key.lower() in k.lower():
                if isinstance(v, (str, int, float)):
                    return str(v)
                elif isinstance(v, dict):
                    for subkey in ["text", "content", "value", "name"]:
                        if subkey in v:
                            return str(v[subkey])
    return None
