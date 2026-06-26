"""
XHS Expert - __INITIAL_STATE__ 解析器
从页面HTML中提取__INITIAL_STATE__，解析笔记/用户/评论数据
"""

import json
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class NoteCard:
    """笔记卡片"""
    note_id: str
    title: str
    desc: str
    user_id: str
    user_nickname: str
    user_avatar: str
    like_count: int
    collect_count: int
    comment_count: int
    share_count: int
    cover_url: str
    image_list: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    time: str = ""
    location: str = ""

    @classmethod
    def from_search_item(cls, item: Dict) -> "NoteCard":
        note_card = item.get("note_card", {})
        interact = note_card.get("interact_info", {})

        def parse_int(val):
            if val is None:
                return 0
            if isinstance(val, int):
                return val
            val_str = str(val).strip()
            if not val_str:
                return 0
            # 处理 "1.2万" 格式
            if "万" in val_str:
                return int(float(val_str.replace("万", "")) * 10000)
            return int(val_str)

        return cls(
            note_id=note_card.get("note_id", ""),
            title=note_card.get("title", ""),
            desc=note_card.get("desc", ""),
            user_id=note_card.get("user", {}).get("user_id", ""),
            user_nickname=note_card.get("user", {}).get("nickname", ""),
            user_avatar=note_card.get("user", {}).get("avatar", ""),
            like_count=parse_int(interact.get("liked_count")),
            collect_count=parse_int(interact.get("collected_count")),
            comment_count=parse_int(interact.get("comment_count")),
            share_count=parse_int(interact.get("share_count")),
            cover_url=note_card.get("cover", {}).get("url_default", ""),
            image_list=[img.get("url_default", "") for img in note_card.get("image_list", [])],
            tags=[t.get("name", "") for t in note_card.get("tag_list", [])],
            time=note_card.get("time", ""),
            location=note_card.get("location", {}).get("name", "")
        )


@dataclass
class CommentItem:
    """评论"""
    comment_id: str
    content: str
    user_id: str
    user_nickname: str
    user_avatar: str
    like_count: int
    create_time: str
    sub_comment_count: int
    sub_comments: List["CommentItem"] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict) -> "CommentItem":
        def parse_time(ts):
            if not ts:
                return ""
            try:
                return datetime.fromtimestamp(ts).isoformat()
            except Exception:
                return ""

        return cls(
            comment_id=data.get("id", ""),
            content=data.get("content", ""),
            user_id=data.get("user_info", {}).get("user_id", ""),
            user_nickname=data.get("user_info", {}).get("nickname", ""),
            user_avatar=data.get("user_info", {}).get("avatar", ""),
            like_count=int(data.get("like_count", 0) or 0),
            create_time=parse_time(data.get("create_time")),
            sub_comment_count=int(data.get("sub_comment_count", 0) or 0),
            sub_comments=[
                cls.from_dict(sub) for sub in data.get("sub_comment_list", [])
            ]
        )


@dataclass
class UserProfile:
    """用户资料"""
    user_id: str
    nickname: str
    avatar: str
    gender: int  # 0=未知 1=男 2=女
    ip_location: str
    desc: str
    following_count: int
    follower_count: int
    like_count: int
    collect_count: int
    note_count: int

    @classmethod
    def from_dict(cls, data: Dict) -> "UserProfile":
        basic = data.get("basic_info", {})
        return cls(
            user_id=data.get("user_id", ""),
            nickname=basic.get("nickname", ""),
            avatar=basic.get("avatar", ""),
            gender=int(basic.get("gender", 0) or 0),
            ip_location=data.get("ip_location", ""),
            desc=data.get("desc", ""),
            following_count=int(data.get("following_count", 0) or 0),
            follower_count=int(data.get("follower_count", 0) or 0),
            like_count=int(data.get("like_count", 0) or 0),
            collect_count=int(data.get("collect_count", 0) or 0),
            note_count=int(data.get("note_count", 0) or 0)
        )


class StateParser:
    """
    __INITIAL_STATE__ 解析器

    小红书页面将数据内嵌在 window.__INITIAL_STATE__ 变量中，
    通过正则表达式提取并解析，比 DOM 提取更稳定。
    """

    INITIAL_STATE_PATTERN = re.compile(
        r'window\.__INITIAL_STATE__\s*=\s*({.*?})\s*(?:;|\n)',
        re.DOTALL
    )

    def __init__(self, html_content: str = ""):
        self.html_content = html_content
        self._state: Optional[Dict] = None

    def extract_from_html(self, html: str) -> Optional[Dict[str, Any]]:
        """从HTML中提取__INITIAL_STATE__"""
        self.html_content = html
        match = self.INITIAL_STATE_PATTERN.search(html)
        if not match:
            return None

        raw_json = match.group(1)
        fixed_json = self._fix_json(raw_json)

        try:
            self._state = json.loads(fixed_json)
            return self._state
        except json.JSONDecodeError:
            return self._try_parse_aggressive(raw_json)

    def _fix_json(self, json_str: str) -> str:
        """修复常见JSON格式问题"""
        # 移除尾随逗号
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        # 单引号转双引号（处理简单的单引号字符串）
        json_str = re.sub(r"'([^'\\]*(?:\\.[^'\\]*)*)'", r'"\1"', json_str)
        return json_str

    def _try_parse_aggressive(self, json_str: str) -> Optional[Dict]:
        """激进修复"""
        # 移除注释
        cleaned = re.sub(r'//.*?\n', '', json_str)
        cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
        # 移除尾随逗号
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)

        try:
            self._state = json.loads(cleaned)
            return self._state
        except json.JSONDecodeError:
            return None

    def get_state(self) -> Optional[Dict]:
        return self._state

    def extract_note_cards(self) -> List[NoteCard]:
        """提取笔记列表"""
        if not self._state:
            return []

        notes = []

        # 搜索结果格式
        search_notes = (
            self._state
            .get("search", {})
            .get("searchUI", {})
            .get("notes", [])
        )
        for item in search_notes:
            try:
                notes.append(NoteCard.from_search_item(item))
            except Exception:
                continue

        # Feed流格式
        if not notes:
            feeds_items = (
                self._state
                .get("feeds", {})
                .get("items", [])
            )
            for item in feeds_items:
                try:
                    notes.append(NoteCard.from_search_item(item))
                except Exception:
                    continue

        return notes

    def extract_note_detail(self) -> Optional[Dict[str, Any]]:
        """提取笔记详情"""
        if not self._state:
            return None

        note_map = self._state.get("note", {}).get("noteDetailMap", {})
        if not note_map:
            return None

        note_id = list(note_map.keys())[0]
        return note_map[note_id]

    def extract_comments(self) -> List[CommentItem]:
        """提取评论列表"""
        if not self._state:
            return []

        comments = []
        comment_map = self._state.get("comment", {}).get("comments", {})

        for note_id, note_comments in comment_map.items():
            for c in note_comments:
                try:
                    comments.append(CommentItem.from_dict(c))
                except Exception:
                    continue

        return comments

    def extract_user_profile(self) -> Optional[UserProfile]:
        """提取用户资料"""
        if not self._state:
            return None

        user_map = self._state.get("user", {}).get("userInfoMap", {})
        if not user_map:
            return None

        user_id = list(user_map.keys())[0]
        return UserProfile.from_dict(user_map[user_id])

    def extract_xsec_token(self) -> str:
        """提取xsec-token"""
        if not self._state:
            return ""
        return self._state.get("note", {}).get("xsec_token", "")
