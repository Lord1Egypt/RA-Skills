"""
archiver.py - 智能归档触发器
基于主题跳转、用户结束信号、空闲超时的自动归档
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from .encoder import DimensionEncoder
from .store import MemoryStore
from .pipeline import IngestPipeline


# 用户结束信号关键词
END_SIGNALS = [
    "先这样", "先到这", "就到这", "就这样吧",
    "下次聊", "下次再说", "回头聊",
    "好的", "行", "OK", "ok", "收到",
    "没什么了", "没事了", "没有了",
    "先去忙", "去忙了", "先走了",
    "拜拜", "再见", "晚安",
]

# 结束信号必须出现在句尾或单独成句才触发
# 避免 "好的，那我们继续讨论 RAG" 这种误判


@dataclass
class SessionState:
    """单个会话的跟踪状态"""
    session_id: str
    person_id: str
    start_ts: float = 0.0
    last_ts: float = 0.0
    last_topic: str = ""
    message_count: int = 0
    memory_ids: list[str] = field(default_factory=list)
    is_active: bool = True


class Archiver:
    """智能归档触发器"""

    def __init__(
        self,
        pipeline: IngestPipeline,
        store: MemoryStore,
        encoder: DimensionEncoder,
        idle_timeout: int = 3600,   # 1小时无活动自动归档
    ):
        self.pipeline = pipeline
        self.store = store
        self.encoder = encoder
        self.idle_timeout = idle_timeout

        # 活跃会话追踪（按 person_id 分组）
        self._sessions: dict[str, SessionState] = {}

        # 归档历史
        self._archive_log: list[dict] = []

    def track(
        self,
        content: str,
        person_code: str = "main",
        ts: float = None,
        topics: list[str] = None,
        nature_code: str = None,
        tool_codes: list[str] = None,
        knowledge_codes: list[str] = None,
        importance: str = "medium",
    ) -> dict:
        """
        追踪一条消息，自动检测归档触发条件。
        如果触发归档，先归档旧会话，再写入新消息。

        返回：{
            "written": {...},       # 写入的 memory
            "archived": [...]       # 本次触发归档的会话列表（可能为空）
        }
        """
        ts = ts or time.time()
        person_id = self.encoder.get_person_by_code(person_code)

        # 获取或创建会话状态
        if person_id not in self._sessions:
            self._sessions[person_id] = SessionState(
                session_id=f"sess_{person_id}_{int(ts)}",
                person_id=person_id,
                start_ts=ts,
            )
        session = self._sessions[person_id]

        # ── 检测触发条件 ──
        archived = []

        # 条件1：主题跳转（顶层主题变了才算）
        if topics and session.last_topic and topics[0] != session.last_topic:
            # 取顶层主题比较，避免同父主题下的兄弟跳转误触发
            old_top = session.last_topic.split(".")[0]
            new_top = topics[0].split(".")[0]
            if old_top != new_top and session.message_count > 0:
                archived.append(self._do_archive(session, ts, reason="topic_jump"))

        # 条件2：用户结束信号
        if self._is_end_signal(content):
            if session.message_count > 0:
                archived.append(self._do_archive(session, ts, reason="end_signal"))

        # 条件3：空闲超时
        if session.last_ts > 0 and (ts - session.last_ts) > self.idle_timeout:
            if session.message_count > 0:
                archived.append(self._do_archive(session, ts, reason="idle_timeout"))

        # ── 写入当前消息 ──
        result = self.pipeline.ingest(
            content=content,
            person_code=person_code,
            ts=ts,
            topics=topics,
            nature_code=nature_code,
            tool_codes=tool_codes,
            knowledge_codes=knowledge_codes,
            importance=importance,
        )

        # 更新会话状态
        session.last_ts = ts
        session.message_count += 1
        session.memory_ids.append(result["memory_id"])
        if topics:
            session.last_topic = topics[0]

        return {
            "written": result,
            "archived": archived,
        }

    def _is_end_signal(self, content: str) -> bool:
        """检测用户结束信号"""
        text = content.strip()

        # 精确匹配：整句就是一个结束信号
        if text in END_SIGNALS:
            return True

        # 句尾匹配：以结束信号结尾，且长度较短（避免误判长句）
        if len(text) < 20:
            for sig in END_SIGNALS:
                if text.endswith(sig):
                    return True

        return False

    def _do_archive(self, session: SessionState, ts: float, reason: str) -> dict:
        """执行归档：打包会话状态，重置会话"""
        archive_record = {
            "session_id": session.session_id,
            "person_id": session.person_id,
            "start_ts": session.start_ts,
            "end_ts": ts,
            "duration_s": int(ts - session.start_ts),
            "message_count": session.message_count,
            "memory_ids": list(session.memory_ids),
            "last_topic": session.last_topic,
            "reason": reason,
        }

        self._archive_log.append(archive_record)

        # 重置会话
        session.session_id = f"sess_{session.person_id}_{int(ts)}"
        session.start_ts = ts
        session.last_ts = 0
        session.last_topic = ""
        session.message_count = 0
        session.memory_ids = []

        return archive_record

    def force_archive(self, person_code: str = "main", ts: float = None) -> dict | None:
        """手动强制归档某个端口的当前会话"""
        ts = ts or time.time()
        person_id = self.encoder.get_person_by_code(person_code)
        session = self._sessions.get(person_id)
        if session and session.message_count > 0:
            return self._do_archive(session, ts, reason="manual")
        return None

    def check_idle(self, ts: float = None) -> list[dict]:
        """检查所有会话的空闲状态，归档超时的"""
        ts = ts or time.time()
        archived = []
        for person_id, session in self._sessions.items():
            if session.message_count > 0 and session.last_ts > 0:
                if (ts - session.last_ts) > self.idle_timeout:
                    archived.append(self._do_archive(session, ts, reason="idle_timeout"))
        return archived

    def get_active_sessions(self) -> list[dict]:
        """获取所有活跃会话的状态"""
        result = []
        for person_id, session in self._sessions.items():
            if session.message_count > 0:
                result.append({
                    "session_id": session.session_id,
                    "person_id": person_id,
                    "message_count": session.message_count,
                    "last_topic": session.last_topic,
                    "last_ts": session.last_ts,
                    "duration_s": int(time.time() - session.start_ts) if session.start_ts else 0,
                })
        return result

    def get_archive_log(self) -> list[dict]:
        """获取归档历史"""
        return list(self._archive_log)
