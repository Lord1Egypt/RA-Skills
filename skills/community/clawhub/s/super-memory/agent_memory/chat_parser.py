from __future__ import annotations

import re
import csv
import json
import sqlite3
import logging
import hashlib
import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

import re as _re
_SAFE_TABLE_RE = _re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

logger = logging.getLogger(__name__)


class ChatSourceType(Enum):
    WECHAT_DB = "wechat_db"
    WECHAT_TXT = "wechat_txt"
    WECHAT_CSV = "wechat_csv"
    SOCIAL_MEDIA = "social_media"
    INTERVIEW = "interview"
    GENERIC = "generic"


@dataclass
class ChatMessage:
    msg_id: str = ""
    sender_id: str = ""
    sender_name: str = ""
    content: str = ""
    timestamp: int = 0
    msg_type: str = "text"
    is_self: bool = False
    reply_to: str = ""
    chat_id: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class ChatSession:
    chat_id: str = ""
    chat_name: str = ""
    chat_type: str = "private"
    participants: List[str] = field(default_factory=list)
    messages: List[ChatMessage] = field(default_factory=list)
    start_time: int = 0
    end_time: int = 0
    message_count: int = 0
    source_type: str = ""


@dataclass
class ParseResult:
    sessions: List[ChatSession]
    total_messages: int = 0
    total_sessions: int = 0
    source_type: str = ""
    parse_errors: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class ChatParser:

    _WECHAT_MSG_TYPE_MAP = {
        1: "text",
        3: "image",
        34: "voice",
        43: "video",
        47: "sticker",
        10000: "system",
        10002: "system",
        49: "text",
    }

    _MSG_TABLE_NAMES = ["MSG", "msg", "message", "messages", "ChatMsg", "chat_msg"]

    _XML_TAG_RE = re.compile(r'<[^>]+>')
    _SYSTEM_MSG_RE = re.compile(r'^[\-\—\~]+.*[\-\—\~]+$|^[【\[]?系统消息[】\]]?')

    _NEWLINE_FORMAT_RE = re.compile(
        r'^(.+?)\s+(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s*$',
        re.MULTILINE
    )
    _BRACKET_FORMAT_RE = re.compile(
        r'^\[(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.+?)[:：]\s*(.+)$',
        re.MULTILINE
    )
    _PAREN_FORMAT_RE = re.compile(
        r'^(.+?)[\(（](\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)[\)）][:：]\s*(.+)$',
        re.MULTILINE
    )
    _ISO_FORMAT_RE = re.compile(
        r'^(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s+(.+?)$',
        re.MULTILINE
    )

    _TIMESTAMP_FORMATS = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
    ]

    _SOCIAL_MEDIA_SPLIT_RE = re.compile(
        r'\n(?=---+\n|\d{4}[-/]\d{1,2}[-/]\d{1,2}|@[\w]+|#[\w]+)'
    )
    _SOCIAL_MEDIA_META_RE = re.compile(
        r'^(?:@([\w]+)|#([\w]+)|(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?))',
        re.MULTILINE
    )

    _INTERVIEW_Q_RE = re.compile(
        r'^(?:[QＱ\d]+[.、:：）)\s]+|问[:：]\s*|访谈者[:：]\s*)(.+)$',
        re.MULTILINE
    )
    _INTERVIEW_A_RE = re.compile(
        r'^(?:[AＡ\d]+[.、:：）)\s]+|答[:：]\s*|受访者[:：]\s*)(.+)$',
        re.MULTILINE
    )

    def parse(self, source, source_type: str = None, **kwargs) -> ParseResult:
        self_name = kwargs.get("self_name", "")
        chat_name = kwargs.get("chat_name", "")
        encoding = kwargs.get("encoding", "utf-8")

        if source_type is None:
            source_type = self._detect_source_type(source)

        st = ChatSourceType.GENERIC
        try:
            st = ChatSourceType(source_type)
        except ValueError:
            logger.warning("Unknown source_type '%s', falling back to generic", source_type)

        if st == ChatSourceType.WECHAT_DB:
            return self.parse_wechat_db(source, self_name=self_name)
        elif st == ChatSourceType.WECHAT_TXT:
            text = self._read_source(source, encoding)
            return self.parse_wechat_txt(text, self_name=self_name, chat_name=chat_name)
        elif st == ChatSourceType.WECHAT_CSV:
            return self.parse_wechat_csv(source, self_name=self_name, encoding=encoding)
        elif st == ChatSourceType.SOCIAL_MEDIA:
            text = self._read_source(source, encoding)
            return self.parse_social_media(text)
        elif st == ChatSourceType.INTERVIEW:
            text = self._read_source(source, encoding)
            return self.parse_interview(text, interviewer_name=self_name or "访谈者")
        else:
            text = self._read_source(source, encoding)
            return self.parse_wechat_txt(text, self_name=self_name, chat_name=chat_name)

    def parse_wechat_db(self, db_path: str, self_name: str = "",
                         chat_filter: str = None) -> ParseResult:
        errors: List[str] = []
        messages: List[ChatMessage] = []

        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
        except Exception as e:
            logger.error("Failed to connect to database %s: %s", db_path, e)
            errors.append(f"Database connection failed: {e}")
            return ParseResult(
                sessions=[],
                source_type=ChatSourceType.WECHAT_DB.value,
                parse_errors=errors,
            )

        try:
            table_name = self._find_msg_table(conn)
            if not table_name:
                errors.append("No message table found in database")
                return ParseResult(
                    sessions=[],
                    source_type=ChatSourceType.WECHAT_DB.value,
                    parse_errors=errors,
                )

            if not _SAFE_TABLE_RE.match(table_name):
                errors.append(f"Invalid table name detected: {table_name}")
                return ParseResult(
                    sessions=[],
                    source_type=ChatSourceType.WECHAT_DB.value,
                    parse_errors=errors,
                )

            query = f"SELECT * FROM [{table_name}]"
            params: list = []
            if chat_filter:
                query += " WHERE talker = ?"
                params.append(chat_filter)
            query += " ORDER BY createTime ASC"

            try:
                cursor = conn.execute(query, params)
            except sqlite3.OperationalError:
                query = f"SELECT * FROM [{table_name}] ORDER BY createTime ASC"
                cursor = conn.execute(query)

            rows = cursor.fetchall()

            for row in rows:
                try:
                    msg = self._row_to_message(dict(row), self_name)
                    if msg:
                        messages.append(msg)
                except Exception as e:
                    errors.append(f"Failed to parse row: {e}")
                    continue
        except Exception as e:
            logger.error("Failed to query database: %s", e)
            errors.append(f"Database query failed: {e}")
        finally:
            conn.close()

        messages = self._identify_speakers(messages, self_name)
        sessions = self._group_into_sessions(messages)

        total_msgs = sum(s.message_count for s in sessions)
        return ParseResult(
            sessions=sessions,
            total_messages=total_msgs,
            total_sessions=len(sessions),
            source_type=ChatSourceType.WECHAT_DB.value,
            parse_errors=errors,
        )

    def parse_wechat_txt(self, text: str, self_name: str = "",
                          chat_name: str = "") -> ParseResult:
        if not text or not text.strip():
            return ParseResult(
                sessions=[],
                source_type=ChatSourceType.WECHAT_TXT.value,
            )

        fmt = self._detect_txt_format(text)

        if fmt == "newline_name_time":
            messages = self._parse_messages_newline_format(text, self_name)
        elif fmt == "bracket_time_name":
            messages = self._parse_messages_bracket_format(text, self_name)
        elif fmt == "name_paren_time":
            messages = self._parse_messages_paren_format(text, self_name)
        elif fmt == "iso_time_name":
            messages = self._parse_messages_iso_format(text, self_name)
        else:
            messages = self._parse_messages_bracket_format(text, self_name)

        messages = self._identify_speakers(messages, self_name)
        sessions = self._group_into_sessions(messages)

        if chat_name and sessions:
            for s in sessions:
                if not s.chat_name:
                    s.chat_name = chat_name

        total_msgs = sum(s.message_count for s in sessions)
        return ParseResult(
            sessions=sessions,
            total_messages=total_msgs,
            total_sessions=len(sessions),
            source_type=ChatSourceType.WECHAT_TXT.value,
        )

    def parse_wechat_csv(self, file_path: str, self_name: str = "",
                          encoding: str = "utf-8") -> ParseResult:
        errors: List[str] = []
        messages: List[ChatMessage] = []

        try:
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames or []

                col_map = self._map_csv_columns(fieldnames)

                for row_num, row in enumerate(reader, 2):
                    try:
                        msg = self._csv_row_to_message(row, col_map, self_name)
                        if msg:
                            messages.append(msg)
                    except Exception as e:
                        errors.append(f"Row {row_num}: {e}")
                        continue
        except Exception as e:
            logger.error("Failed to read CSV file %s: %s", file_path, e)
            errors.append(f"CSV read failed: {e}")
            return ParseResult(
                sessions=[],
                source_type=ChatSourceType.WECHAT_CSV.value,
                parse_errors=errors,
            )

        messages = self._identify_speakers(messages, self_name)
        sessions = self._group_into_sessions(messages)

        total_msgs = sum(s.message_count for s in sessions)
        return ParseResult(
            sessions=sessions,
            total_messages=total_msgs,
            total_sessions=len(sessions),
            source_type=ChatSourceType.WECHAT_CSV.value,
            parse_errors=errors,
        )

    def parse_social_media(self, text: str, platform: str = "generic") -> ParseResult:
        if not text or not text.strip():
            return ParseResult(
                sessions=[],
                source_type=ChatSourceType.SOCIAL_MEDIA.value,
            )

        messages: List[ChatMessage] = []
        chunks = self._SOCIAL_MEDIA_SPLIT_RE.split(text)

        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue

            author = ""
            ts = 0
            content_lines: List[str] = []

            for line in chunk.split('\n'):
                line = line.strip()
                if not line:
                    continue

                meta_match = self._SOCIAL_MEDIA_META_RE.match(line)
                if meta_match:
                    if meta_match.group(1):
                        author = meta_match.group(1)
                    elif meta_match.group(2):
                        author = meta_match.group(2)
                    elif meta_match.group(3):
                        ts = self._parse_timestamp(meta_match.group(3))
                else:
                    content_lines.append(line)

            content = '\n'.join(content_lines).strip()
            if not content:
                continue

            msg = ChatMessage(
                msg_id=self._generate_msg_id(author or "unknown", ts, content),
                sender_name=author,
                content=self._clean_content(content),
                timestamp=ts or int(time.time()),
                msg_type="text",
                chat_id=f"social_{platform}",
            )
            messages.append(msg)

        sessions = self._group_into_sessions(messages, gap_seconds=86400)
        for s in sessions:
            s.chat_type = "group"
            s.source_type = ChatSourceType.SOCIAL_MEDIA.value

        total_msgs = sum(s.message_count for s in sessions)
        return ParseResult(
            sessions=sessions,
            total_messages=total_msgs,
            total_sessions=len(sessions),
            source_type=ChatSourceType.SOCIAL_MEDIA.value,
        )

    def parse_interview(self, text: str, interviewer_name: str = "访谈者") -> ParseResult:
        if not text or not text.strip():
            return ParseResult(
                sessions=[],
                source_type=ChatSourceType.INTERVIEW.value,
            )

        messages: List[ChatMessage] = []
        lines = text.split('\n')
        current_role = ""
        current_content_lines: List[str] = []
        ts = int(time.time())

        def flush():
            nonlocal current_role, current_content_lines
            if current_role and current_content_lines:
                content = '\n'.join(current_content_lines).strip()
                if content:
                    is_self = current_role == "interviewer"
                    sender = interviewer_name if is_self else "受访者"
                    messages.append(ChatMessage(
                        msg_id=self._generate_msg_id(sender, ts, content),
                        sender_name=sender,
                        content=self._clean_content(content),
                        timestamp=ts,
                        msg_type="text",
                        is_self=is_self,
                        chat_id="interview",
                    ))
                    ts += 1
            current_role = ""
            current_content_lines = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            q_match = self._INTERVIEW_Q_RE.match(stripped)
            a_match = self._INTERVIEW_A_RE.match(stripped)

            if q_match:
                flush()
                current_role = "interviewer"
                remaining = q_match.group(1).strip()
                if remaining:
                    current_content_lines.append(remaining)
            elif a_match:
                flush()
                current_role = "interviewee"
                remaining = a_match.group(1).strip()
                if remaining:
                    current_content_lines.append(remaining)
            else:
                current_content_lines.append(stripped)

        flush()

        participants = list(set(m.sender_name for m in messages))
        session = ChatSession(
            chat_id="interview",
            chat_name="访谈记录",
            chat_type="private",
            participants=participants,
            messages=messages,
            start_time=messages[0].timestamp if messages else 0,
            end_time=messages[-1].timestamp if messages else 0,
            message_count=len(messages),
            source_type=ChatSourceType.INTERVIEW.value,
        )

        return ParseResult(
            sessions=[session],
            total_messages=len(messages),
            total_sessions=1,
            source_type=ChatSourceType.INTERVIEW.value,
        )

    def _detect_txt_format(self, text: str) -> str:
        scores = {
            "newline_name_time": len(self._NEWLINE_FORMAT_RE.findall(text)),
            "bracket_time_name": len(self._BRACKET_FORMAT_RE.findall(text)),
            "name_paren_time": len(self._PAREN_FORMAT_RE.findall(text)),
            "iso_time_name": len(self._ISO_FORMAT_RE.findall(text)),
        }

        best = max(scores, key=scores.get)
        if scores[best] == 0:
            return "bracket_time_name"

        return best

    def _parse_messages_newline_format(self, text: str, self_name: str = "") -> List[ChatMessage]:
        messages: List[ChatMessage] = []
        lines = text.split('\n')

        current_sender = ""
        current_ts = 0
        content_lines: List[str] = []

        for line in lines:
            m = self._NEWLINE_FORMAT_RE.match(line.strip())
            if m:
                if current_sender and content_lines:
                    content = '\n'.join(content_lines).strip()
                    if content:
                        messages.append(ChatMessage(
                            msg_id=self._generate_msg_id(current_sender, current_ts, content),
                            sender_name=current_sender,
                            content=self._clean_content(content),
                            timestamp=current_ts,
                            msg_type=self._classify_msg_type(content),
                            chat_id="txt_chat",
                        ))

                current_sender = m.group(1).strip()
                current_ts = self._parse_timestamp(m.group(2))
                content_lines = []
            else:
                stripped = line.strip()
                if stripped:
                    content_lines.append(stripped)

        if current_sender and content_lines:
            content = '\n'.join(content_lines).strip()
            if content:
                messages.append(ChatMessage(
                    msg_id=self._generate_msg_id(current_sender, current_ts, content),
                    sender_name=current_sender,
                    content=self._clean_content(content),
                    timestamp=current_ts,
                    msg_type=self._classify_msg_type(content),
                    chat_id="txt_chat",
                ))

        return messages

    def _parse_messages_bracket_format(self, text: str, self_name: str = "") -> List[ChatMessage]:
        messages: List[ChatMessage] = []

        for m in self._BRACKET_FORMAT_RE.finditer(text):
            ts_str = m.group(1)
            sender = m.group(2).strip()
            content = m.group(3).strip()

            ts = self._parse_timestamp(ts_str)
            messages.append(ChatMessage(
                msg_id=self._generate_msg_id(sender, ts, content),
                sender_name=sender,
                content=self._clean_content(content),
                timestamp=ts,
                msg_type=self._classify_msg_type(content),
                chat_id="txt_chat",
            ))

        if not messages:
            messages = self._parse_messages_fallback(text)

        return messages

    def _parse_messages_paren_format(self, text: str, self_name: str = "") -> List[ChatMessage]:
        messages: List[ChatMessage] = []

        for m in self._PAREN_FORMAT_RE.finditer(text):
            sender = m.group(1).strip()
            ts_str = m.group(2)
            content = m.group(3).strip()

            ts = self._parse_timestamp(ts_str)
            messages.append(ChatMessage(
                msg_id=self._generate_msg_id(sender, ts, content),
                sender_name=sender,
                content=self._clean_content(content),
                timestamp=ts,
                msg_type=self._classify_msg_type(content),
                chat_id="txt_chat",
            ))

        if not messages:
            messages = self._parse_messages_fallback(text)

        return messages

    def _parse_messages_iso_format(self, text: str, self_name: str = "") -> List[ChatMessage]:
        messages: List[ChatMessage] = []
        lines = text.split('\n')

        current_sender = ""
        current_ts = 0
        content_lines: List[str] = []

        for line in lines:
            m = self._ISO_FORMAT_RE.match(line.strip())
            if m:
                if current_sender and content_lines:
                    content = '\n'.join(content_lines).strip()
                    if content:
                        messages.append(ChatMessage(
                            msg_id=self._generate_msg_id(current_sender, current_ts, content),
                            sender_name=current_sender,
                            content=self._clean_content(content),
                            timestamp=current_ts,
                            msg_type=self._classify_msg_type(content),
                            chat_id="txt_chat",
                        ))

                current_ts = self._parse_timestamp(m.group(1))
                current_sender = m.group(2).strip()
                content_lines = []
            else:
                stripped = line.strip()
                if stripped:
                    content_lines.append(stripped)

        if current_sender and content_lines:
            content = '\n'.join(content_lines).strip()
            if content:
                messages.append(ChatMessage(
                    msg_id=self._generate_msg_id(current_sender, current_ts, content),
                    sender_name=current_sender,
                    content=self._clean_content(content),
                    timestamp=current_ts,
                    msg_type=self._classify_msg_type(content),
                    chat_id="txt_chat",
                ))

        return messages

    def _parse_messages_fallback(self, text: str) -> List[ChatMessage]:
        messages: List[ChatMessage] = []
        lines = text.split('\n')
        ts = int(time.time())

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            sender = ""
            content = stripped

            colon_match = re.match(r'^(.+?)[:：]\s*(.+)$', stripped)
            if colon_match:
                sender = colon_match.group(1).strip()
                content = colon_match.group(2).strip()

            if content:
                messages.append(ChatMessage(
                    msg_id=self._generate_msg_id(sender or "unknown", ts, content),
                    sender_name=sender,
                    content=self._clean_content(content),
                    timestamp=ts,
                    msg_type=self._classify_msg_type(content),
                    chat_id="txt_chat",
                ))
                ts += 1

        return messages

    def _identify_speakers(self, messages: List[ChatMessage], self_name: str = "") -> List[ChatMessage]:
        if not messages:
            return messages

        if self_name:
            for msg in messages:
                msg.is_self = (msg.sender_name == self_name or msg.sender_id == self_name)
            return messages

        sender_counts: Dict[str, int] = {}
        for msg in messages:
            name = msg.sender_name or msg.sender_id
            if name:
                sender_counts[name] = sender_counts.get(name, 0) + 1

        if sender_counts:
            most_frequent = max(sender_counts, key=sender_counts.get)
            for msg in messages:
                name = msg.sender_name or msg.sender_id
                msg.is_self = (name == most_frequent)

        return messages

    def _group_into_sessions(self, messages: List[ChatMessage],
                              gap_seconds: int = 3600) -> List[ChatSession]:
        if not messages:
            return []

        sorted_msgs = sorted(messages, key=lambda m: m.timestamp)
        sessions: List[ChatSession] = []

        current_msgs: List[ChatMessage] = [sorted_msgs[0]]

        for i in range(1, len(sorted_msgs)):
            gap = sorted_msgs[i].timestamp - sorted_msgs[i - 1].timestamp
            if gap > gap_seconds:
                session = self._build_session(current_msgs)
                sessions.append(session)
                current_msgs = [sorted_msgs[i]]
            else:
                current_msgs.append(sorted_msgs[i])

        if current_msgs:
            session = self._build_session(current_msgs)
            sessions.append(session)

        return sessions

    @staticmethod
    def _parse_timestamp(ts_str: str) -> int:
        if not ts_str:
            return 0

        ts_str = ts_str.strip()

        try:
            val = int(ts_str)
            if val > 1e9:
                return val
            elif val > 1e6:
                return val
        except ValueError:
            pass

        for fmt in ChatParser._TIMESTAMP_FORMATS:
            try:
                dt = datetime.strptime(ts_str, fmt)
                return int(dt.timestamp())
            except ValueError:
                continue

        logger.warning("Failed to parse timestamp: '%s'", ts_str)
        return 0

    @staticmethod
    def _classify_msg_type(content: str, raw_type: int = 0) -> str:
        if raw_type:
            type_map = {
                1: "text",
                3: "image",
                34: "voice",
                43: "video",
                47: "sticker",
                10000: "system",
                10002: "system",
                49: "text",
            }
            return type_map.get(raw_type, "text")

        if not content:
            return "text"

        if content.startswith('<msg>') or content.startswith('<?xml'):
            if 'img' in content.lower():
                return "image"
            elif 'voice' in content.lower() or 'voicemsg' in content.lower():
                return "voice"
            elif 'video' in content.lower():
                return "video"
            elif 'emoji' in content.lower() or 'emoticon' in content.lower():
                return "sticker"
            return "text"

        if re.match(r'^\[.+\]$', content):
            inner = content[1:-1]
            if any(kw in inner for kw in ['图片', 'Image', 'photo']):
                return "image"
            elif any(kw in inner for kw in ['语音', 'Voice', 'audio']):
                return "voice"
            elif any(kw in inner for kw in ['视频', 'Video']):
                return "video"
            elif any(kw in inner for kw in ['表情', 'Sticker', 'emoji']):
                return "sticker"

        return "text"

    @staticmethod
    def _generate_msg_id(sender: str, timestamp: int, content: str) -> str:
        raw = f"{sender}_{timestamp}_{content[:50]}"
        return hashlib.sha256(raw.encode()).hexdigest()[:12]

    @staticmethod
    def _clean_content(content: str) -> str:
        if not content:
            return content

        if content.startswith('<?xml') or content.startswith('<msg>'):
            text_match = re.search(r'<content>(.*?)</content>', content, re.DOTALL)
            if text_match:
                content = text_match.group(1)
            else:
                content = re.sub(r'<[^>]+>', '', content)

        content = re.sub(r'<[^>]+>', '', content)

        content = re.sub(r'^[\-\—\~]{3,}$', '', content, flags=re.MULTILINE)

        content = re.sub(r'\n{3,}', '\n\n', content)

        return content.strip()

    def _detect_source_type(self, source) -> str:
        if isinstance(source, str):
            lower = source.lower()
            if lower.endswith('.db') or lower.endswith('.sqlite') or lower.endswith('.sqlite3'):
                return ChatSourceType.WECHAT_DB.value
            elif lower.endswith('.csv'):
                return ChatSourceType.WECHAT_CSV.value
            elif lower.endswith('.txt') or lower.endswith('.log'):
                return ChatSourceType.WECHAT_TXT.value
            elif '\n' in source:
                return ChatSourceType.WECHAT_TXT.value
        return ChatSourceType.GENERIC.value

    def _read_source(self, source, encoding: str = "utf-8") -> str:
        if isinstance(source, str):
            try:
                with open(source, 'r', encoding=encoding, errors='ignore') as f:
                    return f.read()
            except (FileNotFoundError, OSError):
                return source
        return str(source)

    def _find_msg_table(self, conn: sqlite3.Connection) -> str:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row[0] for row in cursor.fetchall()]

        for candidate in self._MSG_TABLE_NAMES:
            if candidate in tables:
                if _SAFE_TABLE_RE.match(candidate):
                    return candidate

        for t in tables:
            if not _SAFE_TABLE_RE.match(t):
                continue
            lower = t.lower()
            if 'msg' in lower or 'chat' in lower:
                try:
                    conn.execute(f"SELECT COUNT(*) FROM [{t}] LIMIT 1")
                    return t
                except sqlite3.OperationalError:
                    continue

        return ""

    def _row_to_message(self, row: dict, self_name: str = "") -> Optional[ChatMessage]:
        msg_id = str(row.get("msgSvrId", row.get("msgsvrid", row.get("id", ""))))
        content = str(row.get("strContent", row.get("content", row.get("StrContent", ""))))
        create_time = row.get("createTime", row.get("createtime", row.get("timestamp", 0)))

        try:
            ts = int(create_time) if create_time else 0
        except (ValueError, TypeError):
            ts = 0

        raw_type = row.get("type", row.get("Type", 0))
        try:
            raw_type = int(raw_type)
        except (ValueError, TypeError):
            raw_type = 0

        talker = str(row.get("talker", row.get("Talker", row.get("chat_id", ""))))
        is_send = row.get("isSend", row.get("issend", row.get("is_send", 0)))
        try:
            is_self = int(is_send) == 1
        except (ValueError, TypeError):
            is_self = False

        sender = str(row.get("sender", row.get("Sender", row.get("sender_id", ""))))

        msg_type = self._classify_msg_type(content, raw_type)
        cleaned = self._clean_content(content)

        if not cleaned and msg_type == "text":
            return None

        return ChatMessage(
            msg_id=msg_id or self._generate_msg_id(sender or talker, ts, cleaned),
            sender_id=sender,
            sender_name=sender,
            content=cleaned,
            timestamp=ts,
            msg_type=msg_type,
            is_self=is_self,
            chat_id=talker,
        )

    @staticmethod
    def _map_csv_columns(fieldnames: list) -> dict:
        col_map = {
            "timestamp": None,
            "sender": None,
            "content": None,
            "type": None,
            "chat_id": None,
        }

        timestamp_names = {"时间", "timestamp", "time", "date", "datetime", "创建时间", "发送时间"}
        sender_names = {"发送者", "sender", "name", "昵称", "用户名", "from", "说话人"}
        content_names = {"内容", "content", "text", "message", "消息", "正文", "msg"}
        type_names = {"类型", "type", "msg_type", "消息类型"}
        chat_id_names = {"会话id", "chat_id", "talker", "会话", "群名"}

        for name in fieldnames:
            lower = name.strip().lower()
            if lower in timestamp_names and col_map["timestamp"] is None:
                col_map["timestamp"] = name
            elif lower in sender_names and col_map["sender"] is None:
                col_map["sender"] = name
            elif lower in content_names and col_map["content"] is None:
                col_map["content"] = name
            elif lower in type_names and col_map["type"] is None:
                col_map["type"] = name
            elif lower in chat_id_names and col_map["chat_id"] is None:
                col_map["chat_id"] = name

        return col_map

    def _csv_row_to_message(self, row: dict, col_map: dict,
                             self_name: str = "") -> Optional[ChatMessage]:
        ts_str = row.get(col_map["timestamp"], "") if col_map["timestamp"] else ""
        sender = row.get(col_map["sender"], "") if col_map["sender"] else ""
        content = row.get(col_map["content"], "") if col_map["content"] else ""
        type_str = row.get(col_map["type"], "") if col_map["type"] else ""
        chat_id = row.get(col_map["chat_id"], "") if col_map["chat_id"] else ""

        ts = self._parse_timestamp(str(ts_str)) if ts_str else 0
        content = str(content).strip()
        if not content:
            return None

        raw_type = 0
        try:
            raw_type = int(type_str)
        except (ValueError, TypeError):
            pass

        msg_type = self._classify_msg_type(content, raw_type)
        cleaned = self._clean_content(content)

        return ChatMessage(
            msg_id=self._generate_msg_id(sender or "unknown", ts, cleaned),
            sender_name=str(sender),
            content=cleaned,
            timestamp=ts or int(time.time()),
            msg_type=msg_type,
            chat_id=str(chat_id) if chat_id else "csv_chat",
        )

    def _build_session(self, messages: List[ChatMessage]) -> ChatSession:
        if not messages:
            return ChatSession()

        chat_id = messages[0].chat_id or "unknown"
        participants = list(set(
            m.sender_name or m.sender_id for m in messages if (m.sender_name or m.sender_id)
        ))
        chat_type = "group" if len(participants) > 2 else "private"

        return ChatSession(
            chat_id=chat_id,
            chat_name=chat_id,
            chat_type=chat_type,
            participants=participants,
            messages=messages,
            start_time=messages[0].timestamp,
            end_time=messages[-1].timestamp,
            message_count=len(messages),
        )
