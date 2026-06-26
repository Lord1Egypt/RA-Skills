"""
models.py - 数据模型定义
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class WechatSession:
    """一个会话（群聊或私聊）"""
    username: str
    display_name: str
    is_group: bool
    last_time: int  # timestamp
    last_summary: str
    unread_count: int
    msg_count: int = 0
    tags: List[str] = field(default_factory=list)

@dataclass
class WechatContact:
    """联系人"""
    username: str
    nick_name: str
    remark: str
    alias: str = ""

@dataclass
class WechatMessage:
    """一条消息"""
    local_id: int
    sender_id: int
    create_time: int  # timestamp
    msg_type: int
    content: str
    sender_wxid: str = ""

@dataclass
class GroupProfile:
    """群组画像"""
    table_name: str
    display_name: str
    msg_count: int
    time_range: tuple  # (min_ts, max_ts)
    top_senders: List[tuple]  # [(sender_id, count), ...]
    tags: List[str] = field(default_factory=list)

@dataclass
class PersonProfile:
    """个人画像（综合分析结果）"""
    wxid: str
    nick_name: str = ""
    frequent_topics: List[str] = field(default_factory=list)
    social_patterns: Dict = field(default_factory=dict)
    investment_behavior: Dict = field(default_factory=dict)
    gaming_habits: List[str] = field(default_factory=list)
    study_patterns: Dict = field(default_factory=dict)
    consumption_habits: Dict = field(default_factory=dict)
    key_relationships: List[Dict] = field(default_factory=list)
    language_style: Dict = field(default_factory=dict)
