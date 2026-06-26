"""
pipeline.py - 写入管道
主题检测 → 编码 → 关联建立 → 写入存储

v5.2: 异步写入队列 — 高并发场景下不丢请求，后台批量持久化
v5.3: 写入队列 SQLite 持久化 — 进程崩溃不丢数据
"""

from __future__ import annotations

import time
import os
import json
import sqlite3
import threading
import queue
import logging
import hashlib
from datetime import datetime
from .encoder import DimensionEncoder
from .store import MemoryStore, _chunked_placeholders, SQLITE_MAX_VARIABLES
from .detector import TopicDetector, TopicSplitter
from .emotion import EmotionAnalyzer
from .temporal import TemporalReasoner
from .entity import EntityResolver

try:
    from .enterprise.compliance_guard import ComplianceGuard as _ComplianceGuard
    ComplianceGuard = _ComplianceGuard
except Exception:
    ComplianceGuard = None

logger = logging.getLogger(__name__)

# Fix (Bug 2): 线程锁，替代 fcntl 文件锁保护 JSON 索引文件并发写入
_index_write_lock = threading.Lock()


# 写入队列持久化 Schema
_WRITE_QUEUE_SCHEMA = """
CREATE TABLE IF NOT EXISTS _write_queue (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    item_hash   TEXT NOT NULL UNIQUE,         -- 防重复入队
    payload     TEXT NOT NULL,                 -- JSON 序列化的写入请求
    enqueued_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    status      TEXT DEFAULT 'pending'         -- pending / processing / done / failed
);
CREATE INDEX IF NOT EXISTS idx_wq_status ON _write_queue(status);
CREATE INDEX IF NOT EXISTS idx_wq_enqueued ON _write_queue(enqueued_at);
"""


class WriteQueue:
    """
    异步写入队列。

    生产者（API/CLI）将写入请求放入队列，
    后台消费者线程批量持久化到 SQLite。

    v5.3 修复: SQLite 持久化 — 进程崩溃后重启可恢复未处理的写入请求。

    设计：
    - 内部队列有容量上限（默认 1000），满时阻塞生产者
    - 每个入队请求同时写入 SQLite _write_queue 表（持久化）
    - 消费者按批次 flush（默认每 50 条或每 500ms）
    - flush 成功后从 SQLite 删除对应记录
    - 启动时自动恢复 SQLite 中 status=pending 的请求
    - 支持 graceful shutdown（drain 后关闭）
    - 线程安全，多生产者/单消费者
    """

    def __init__(
        self,
        pipeline: "IngestPipeline",
        max_queue_size: int = 1000,
        batch_size: int = 50,
        flush_interval_ms: int = 500,
    ):
        self._pipeline = pipeline
        self._queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self._batch_size = batch_size
        self._flush_interval = flush_interval_ms / 1000.0
        self._worker: threading.Thread | None = None
        self._running = False
        self._stats = {"enqueued": 0, "written": 0, "dropped": 0, "batches": 0, "recovered": 0}

        # SQLite 持久化
        self._db_path = pipeline.store.db_path
        self._ensure_queue_table()

    def _ensure_queue_table(self):
        """创建写入队列持久化表（复用 store 连接）"""
        conn = self._pipeline.store.conn
        conn.executescript(_WRITE_QUEUE_SCHEMA)
        conn.commit()

    def _get_conn(self):
        """获取数据库连接（复用 store 的线程安全连接）"""
        return self._pipeline.store.conn

    def start(self):
        """启动后台写入线程（含崩溃恢复）"""
        if self._running:
            return
        self._running = True

        # 恢复上次崩溃遗留的 pending 请求
        recovered = self._recover_pending()
        if recovered > 0:
            logger.info(f"WriteQueue: 从崩溃恢复 {recovered} 条待写入请求")
            self._stats["recovered"] = recovered

        self._worker = threading.Thread(target=self._consume_loop, daemon=True, name="WriteQueueWorker")
        self._worker.start()
        logger.info("WriteQueue: 后台写入线程已启动")

    def _recover_pending(self) -> int:
        """
        从 SQLite 恢复上次未处理的写入请求。

        进程崩溃后重启时调用，恢复 pending + stale processing 的记录。
        """
        try:
            conn = self._get_conn()

            # Fix #12: 重置 stale processing（上次崩溃残留）→ pending
            conn.execute(
                "UPDATE _write_queue SET status = 'pending' WHERE status = 'processing'"
            )
            conn.commit()

            rows = conn.execute(
                "SELECT id, payload FROM _write_queue WHERE status = 'pending' ORDER BY enqueued_at"
            ).fetchall()

            recovered = 0
            for row_id, payload_str in rows:
                try:
                    item = json.loads(payload_str)
                    # 标记为 processing，防止重复恢复
                    conn.execute(
                        "UPDATE _write_queue SET status = 'processing' WHERE id = ?", (row_id,)
                    )
                    conn.commit()

                    # 放入内存队列（保留 _queue_hash 用于 flush 时删除）
                    item["_queue_db_id"] = row_id
                    self._queue.put_nowait(item)
                    recovered += 1
                except queue.Full:
                    # 队列满了，剩余的保持 pending 状态
                    conn.execute(
                        "UPDATE _write_queue SET status = 'pending' WHERE id = ?", (row_id,)
                    )
                    conn.commit()
                    break
                except Exception as e:
                    logger.warning("pipeline: %s", e)

            return recovered
        except Exception as e:
            logger.warning("pipeline: %s", e)
            return 0

    def stop(self, drain: bool = True, timeout: float = 10.0):
        """
        停止后台线程。

        参数:
            drain: 是否先排空队列
            timeout: 排空超时
        """
        if not self._running:
            return
        self._running = False
        # 放入毒丸让 consumer 退出
        try:
            self._queue.put_nowait(None)
        except queue.Full:
            logger.debug("pipeline: write queue full, poison pill dropped")
        if self._worker:
            self._worker.join(timeout=timeout)
        logger.info(f"WriteQueue: 已停止, stats={self._stats}")

    def enqueue(
        self,
        content: str,
        person_code: str = "main",
        ts: float = None,
        topics: list[str] = None,
        nature_code: str = None,
        tool_codes: list[str] = None,
        knowledge_codes: list[str] = None,
        importance: str = "medium",
        owner_agent_id: str = "_system",
        visibility: str = "team",
        timeout: float = 5.0,
    ) -> dict:
        """
        将写入请求放入队列（持久化 + 内存队列）。

        返回: {"queued": True, "position": int} 或 {"queued": False, "reason": str}
        """
        item = {
            "content": content,
            "person_code": person_code,
            "ts": ts or time.time(),
            "topics": topics,
            "nature_code": nature_code,
            "tool_codes": tool_codes,
            "knowledge_codes": knowledge_codes,
            "importance": importance,
            "owner_agent_id": owner_agent_id,
            "visibility": visibility,
        }

        # 计算 hash 防重复入队
        item_hash = hashlib.sha256(
            json.dumps(item, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()[:16]
        item["_queue_hash"] = item_hash

        # 1. 先写 SQLite（持久化，崩溃不丢）
        try:
            conn = self._get_conn()
            conn.execute(
                "INSERT OR IGNORE INTO _write_queue (item_hash, payload, status) VALUES (?, ?, 'pending')",
                (item_hash, json.dumps(item, ensure_ascii=False)),
            )
            conn.commit()
        except Exception as e:
            logger.warning("pipeline: %s", e)

        # 2. 放入内存队列
        try:
            self._queue.put(item, timeout=timeout)
            self._stats["enqueued"] += 1
            return {"queued": True, "position": self._queue.qsize()}
        except queue.Full:
            self._stats["dropped"] += 1
            return {"queued": False, "reason": "队列已满，请稍后重试"}

    def _consume_loop(self):
        """消费者主循环"""
        batch = []
        last_flush = time.time()

        while self._running or not self._queue.empty():
            try:
                # 带超时的取，保证定期 flush
                item = self._queue.get(timeout=self._flush_interval)
                if item is None:  # 毒丸
                    break
                batch.append(item)

                # 批次满了或超时 → flush
                now = time.time()
                if len(batch) >= self._batch_size or (now - last_flush) >= self._flush_interval:
                    self._flush_batch(batch)
                    batch = []
                    last_flush = now

            except queue.Empty:
                # 超时，flush 现有批次
                if batch:
                    self._flush_batch(batch)
                    batch = []
                    last_flush = time.time()

        # 退出前 flush 剩余
        if batch:
            self._flush_batch(batch)

    def _flush_batch(self, batch: list[dict]):
        """批量持久化"""
        # NOTE: 串行执行ingest是因为内部有事务依赖，长期可考虑分离编码与存储阶段
        try:
            processed_hashes = []
            for item in batch:
                try:
                    self._pipeline.ingest(
                        content=item["content"],
                        person_code=item["person_code"],
                        ts=item.get("ts"),
                        topics=item.get("topics"),
                        nature_code=item.get("nature_code"),
                        tool_codes=item.get("tool_codes"),
                        knowledge_codes=item.get("knowledge_codes"),
                        importance=item.get("importance", "medium"),
                        skip_throttle=True,
                        owner_agent_id=item.get("owner_agent_id", "_system"),
                        visibility=item.get("visibility", "team"),
                    )
                    self._stats["written"] += 1
                    # 收集成功写入的 hash，用于清理 SQLite
                    h = item.get("_queue_hash")
                    if h:
                        processed_hashes.append(h)
                except Exception as e:
                    logger.error(f"WriteQueue: 单条写入失败: {e}")
                    self._stats["dropped"] += 1

            # 从 SQLite 删除已成功写入的记录
            if processed_hashes:
                try:
                    conn = self._get_conn()
                    for placeholders, chunk_ids in _chunked_placeholders(processed_hashes):
                        conn.execute(
                            f"DELETE FROM _write_queue WHERE item_hash IN ({placeholders})",
                            chunk_ids,
                        )
                    conn.commit()
                except Exception as e:
                    logger.warning("pipeline: %s", e)

            self._stats["batches"] += 1
            logger.debug(f"WriteQueue: flush {len(batch)} 条 (total_written={self._stats['written']})")
        except Exception as e:
            logger.error(f"WriteQueue: batch flush 失败: {e}")

    def get_stats(self) -> dict:
        return {
            **self._stats,
            "queue_size": self._queue.qsize(),
            "running": self._running,
        }


class IngestPipeline:
    """将原始对话消息写入记忆系统"""

    # 写入限流配置
    MAX_BATCH_SIZE = 50           # 单批最大写入条数
    WRITE_COOLDOWN_MS = 100       # 批间冷却时间（毫秒）
    MAX_CONTENT_LENGTH = 50_000   # 单条内容最大长度（字符），防止撑爆 SQLite

    # 合规扫描模式: "off" | "tag" | "reject"
    COMPLIANCE_MODE = os.environ.get("AGENT_MEMORY_COMPLIANCE_MODE", "tag")

    def __init__(self, store: MemoryStore, encoder: DimensionEncoder, index_dir: str = None, embedding_store=None, topic_registry=None, semantic_matcher=None, llm_fn=None):
        self.store = store
        self.encoder = encoder
        self.topic_registry = topic_registry
        self.semantic_matcher = semantic_matcher
        self.llm_fn = llm_fn
        self.detector = TopicDetector(encoder, topic_registry=topic_registry, semantic_matcher=semantic_matcher)
        self.splitter = TopicSplitter(encoder)  # 默认无 LLM，回退单片段
        self.emotion_analyzer = EmotionAnalyzer(llm_fn=llm_fn)  # Phase 1: 情感分析器（v7.1: 注入 llm_fn）
        self.temporal_reasoner = TemporalReasoner(llm_fn=llm_fn)  # Phase 2.1: 双时间线推理器
        self.entity_resolver = EntityResolver(store=store)  # Phase 2.2: 实体消解引擎
        self.embedding_store = embedding_store  # EmbeddingStore 实例，可选
        self._write_queue: WriteQueue | None = None  # 异步写入队列（可选）

        # S-10: 合规扫描器
        self._compliance_guard = None
        if ComplianceGuard is not None:
            try:
                self._compliance_guard = ComplianceGuard()
                logger.info("ComplianceGuard 已集成到写入管道 (mode=%s)", self.COMPLIANCE_MODE)
            except Exception as e:
                logger.warning("ComplianceGuard 初始化失败: %s", e)

        # 每日索引目录
        self._index_dir = index_dir or str(
            os.path.join(os.path.dirname(__file__), "daily_index")
        )

        # 窗口状态（受 _state_lock 保护）
        self._state_lock = threading.Lock()
        self._last_time_ts: int = 0
        self._last_person: str = ""
        self._last_memory_id: str = ""
        self._last_topic: str = ""
        self._window_buffer: list[str] = []
        self._window_size: int = 5  # 用户可配置

        # 写入节流状态
        self._write_timestamps: list[float] = []  # 最近写入时间戳
        self._throttle_window_sec = 1.0            # 节流窗口（秒）
        self._throttle_max_writes = 20             # 窗口内最大写入数

    def ingest(
        self,
        content: str,
        person_code: str = "main",
        ts: float = None,
        topics: list[str] = None,
        nature_code: str = None,
        tool_codes: list[str] = None,
        knowledge_codes: list[str] = None,
        importance: str = "medium",
        skip_throttle: bool = False,
        owner_agent_id: str = "_system",
        visibility: str = "team",
    ) -> dict:
        """
        写入一条消息

        参数：
            content: 对话内容
            person_code: 端口 code（main/mobile/web）
            ts: 时间戳，None 则取当前时间
            topics: 显式指定主题路径列表，None 则自动检测
            nature_code: 显式指定性质 code，None 则自动检测
            tool_codes: 显式指定工具 code 列表，None 则自动检测
            knowledge_codes: 显式指定知识类型 code 列表，None 则自动检测
            importance: 重要度 (high/medium/low)
            skip_throttle: 跳过限流检查（批量写入时使用）

        返回：写入的 memory 记录
        """
        # Fix (P1): 内容长度校验 — 防止 100MB 内容撑爆 SQLite WAL + FTS
        if len(content) > self.MAX_CONTENT_LENGTH:
            logger.warning(
                f"内容长度 {len(content)} 超过上限 {self.MAX_CONTENT_LENGTH}，已截断"
            )
            content = content[:self.MAX_CONTENT_LENGTH]

        if not content or not content.strip():
            return {"memory_id": None, "skipped": True, "reason": "empty_content"}

        # S-10: 合规扫描 — 写入前检测 PII/敏感信息
        compliance_result = None
        if self._compliance_guard is not None and self.COMPLIANCE_MODE != "off":
            try:
                compliance_result = self._compliance_guard.scan(content)
                if not compliance_result.is_compliant:
                    if self.COMPLIANCE_MODE == "reject":
                        logger.warning(
                            "合规扫描拒绝写入: risk=%s, types=%s",
                            compliance_result.risk_level,
                            compliance_result.detected_types,
                        )
                        return {
                            "memory_id": None,
                            "skipped": True,
                            "reason": "compliance_rejected",
                            "compliance": {
                                "risk_level": compliance_result.risk_level,
                                "detected_types": compliance_result.detected_types,
                                "details": compliance_result.details,
                            },
                        }
                    # tag 模式: 使用脱敏后的内容继续写入
                    if compliance_result.redacted_content:
                        content = compliance_result.redacted_content
                    logger.info(
                        "合规扫描标记: risk=%s, types=%s, 已脱敏",
                        compliance_result.risk_level,
                        compliance_result.detected_types,
                    )
            except Exception as e:
                logger.warning("合规扫描异常，跳过: %s", e)

        # 写入限流检查
        if not skip_throttle and self._is_throttled():
            import logging
            logging.getLogger(__name__).debug("写入限流触发，跳过低优先级写入")
            return {"memory_id": None, "throttled": True}

        ts = ts or time.time()
        person_id = self.encoder.get_person_by_code(person_code)
        content_hash = DimensionEncoder.content_hash(content)

        # 检测主题
        if topics is None:
            topics = self.detector.detect(content, auto_register=True)
        if not topics:
            topics = ["misc"]

        # 检测性质
        if nature_code is None:
            nature_code = self.detector.detect_nature(content)
        nature_id = self.encoder.encode_nature(nature_code)

        # 检测工具
        tool_ids = []
        if tool_codes:
            for code in tool_codes:
                tool_ids.append(self.encoder.get_tool_by_code(code))

        # 检测知识类型
        knowledge_ids = []
        if knowledge_codes:
            for code in knowledge_codes:
                knowledge_ids.append(self.encoder.encode_knowledge(code))
        else:
            for code in self.detector.detect_knowledge(content):
                knowledge_ids.append(self.encoder.encode_knowledge(code))

        # Phase 1: 情感分析
        emotion = self.emotion_analyzer.analyze(content, importance, nature_code)

        # Phase 2.1: 双时间线信号提取
        temporal_signals = self.temporal_reasoner.extract_temporal_signals(content)
        valid_from = temporal_signals.get("valid_from")
        valid_until = temporal_signals.get("valid_until")
        occurrence_time = temporal_signals.get("occurrence_time")
        mention_time = ts  # 首次提及时间 = 写入时间
        is_correction = temporal_signals.get("is_correction", False)

        # 编码
        time_id = self.encoder.encode_time(ts, precision="second")
        memory_id = self.encoder.generate_memory_id(
            time_id, person_id, topics, nature_id, tool_ids
        )

        # Fix (Issue 1): 用 store 的事务上下文统一管理结构化数据+向量的写入
        # 确保 pipeline.ingest() 内 store.insert_memory() 和 embedding_store.add()
        # 在同一个 SQLite 事务中完成
        try:
            with self.store.transaction() as txn_conn:
                # 写入结构化数据（传入事务连接）
                self.store.insert_memory_in_txn(
                    txn_conn=txn_conn,
                    memory_id=memory_id,
                    time_id=time_id,
                    time_ts=int(ts),
                    person_id=person_id,
                    nature_id=nature_id,
                    content=content,
                    content_hash=content_hash,
                    topics=topics,
                    tools=tool_ids,
                    knowledge_types=knowledge_ids,
                    importance=importance,
                    owner_agent_id=owner_agent_id,
                    visibility=visibility,
                    valence=emotion["valence"],
                    arousal=emotion["arousal"],
                    dominance=emotion.get("dominance", 0.5),
                    significance=emotion["significance"],
                    confidence=emotion["confidence"],
                    primary_emotions=json.dumps(emotion.get("primary_emotions", {}), ensure_ascii=False),
                    compound_emotions=json.dumps(emotion.get("compound_emotions", []), ensure_ascii=False),
                    # Phase 2.1: 双时间线字段
                    valid_from=valid_from,
                    valid_until=valid_until,
                    occurrence_time=occurrence_time,
                    mention_time=mention_time,
                )

                # 写入向量库（同一个事务连接）
                if self.embedding_store:
                    try:
                        self.embedding_store.add(
                            memory_id=memory_id,
                            content=content,
                            metadata={
                                "nature_id": nature_id,
                                "importance": importance,
                                "person_id": person_id,
                            },
                            conn=txn_conn,
                        )
                    except Exception as e:
                        # 向量写入失败 → 回滚整个事务（保证一致性）
                        raise RuntimeError(f"向量写入失败，事务回滚: {e}") from e

                # FTS 已在 insert_memory_in_txn 内同步
        except RuntimeError:
            # 向量写入失败导致的回滚，直接向上抛出
            raise
        except Exception as e:
            logger.error(f"写入事务失败: {e}")
            raise

        # 以下操作在事务外执行（有各自的事务管理）
        # Phase 2.1: 修正信号检测 — 如果检测到修正，查找相关旧记忆并标记失效
        invalidated_ids = []
        if is_correction:
            invalidated_ids = self._handle_temporal_correction(
                content=content,
                new_memory_id=memory_id,
                person_id=person_id,
                topics=topics,
            )

        # Phase 2.1+: LLM 驱动的事实失效检测 — 即使无明确修正信号词，也用 LLM 判断语义层面的失效
        llm_invalidated_ids = []
        if self.temporal_reasoner._llm_fn is not None:
            llm_invalidated_ids = self._handle_llm_invalidation(
                content=content,
                new_memory_id=memory_id,
                person_id=person_id,
                already_invalidated=invalidated_ids,
            )
            # 合并去重
            for mid in llm_invalidated_ids:
                if mid not in invalidated_ids:
                    invalidated_ids.append(mid)

        # Phase 2.2: 实体提取与关联
        entity_ids = []
        try:
            extracted = self.entity_resolver.extract_entities(content)
            if extracted:
                self.entity_resolver.link_memory_entities(memory_id, extracted)
                entity_ids = [
                    self.entity_resolver.resolve_entity(e["name"], e.get("type"))
                    for e in extracted
                    if self.entity_resolver.resolve_entity(e["name"], e.get("type"))
                ]
        except Exception as e:
            logger.warning("entity: extract/link failed: %s", e)

        # 自动提取待办任务（性质为 todo 时）
        task_id = None
        if nature_code == "todo":
            topic = topics[0] if topics else None
            task_id = self.store.add_task(
                memory_id=memory_id,
                title=content[:100],
                assignee="ai" if any(w in content for w in ["配置", "添加", "开发", "实现", "写"]) else "user",
                topic_code=topic,
            )

        # 更新每日索引
        self._update_daily_index(ts, memory_id, topics, nature_id, importance)

        # 建立关联 + 更新窗口状态（原子操作，防止并发交错）
        with self._state_lock:
            # 建立时间关联
            if self._last_memory_id and self._last_person == person_id:
                time_gap = int(ts) - self._last_time_ts
                if time_gap < 300:  # 5分钟内算连续对话
                    self.store.insert_link(
                        self._last_memory_id, memory_id,
                        link_type="temporal",
                        weight=max(0.1, 1.0 - time_gap / 300),
                        reason=f"时间间隔 {time_gap}s",
                    )

            # 建立主题关联
            if self._last_topic and topics and self._last_topic == topics[0]:
                self.store.insert_link(
                    self._last_memory_id, memory_id,
                    link_type="topic",
                    weight=0.8,
                    reason=f"同主题 {topics[0]}",
                )

            # ── Layer 1+2: 写入时因果检测 ──
            causal_hints = self.detector.detect_causal_signals(content)
            if causal_hints and self._last_memory_id and self._last_person == person_id:
                best = causal_hints[0]  # 置信度最高的
                # 只在时间窗口内（5min）且置信度足够时建 link
                time_gap = int(ts) - self._last_time_ts
                if time_gap < 300 and best.confidence >= 0.4:
                    link_weight = min(1.0, best.confidence * (1.0 - time_gap / 300))
                    # 确定因果方向：当前消息是"结果"，前一条是"原因"
                    if best.effect_text:
                        # 有明确结果 → 前因导致当前
                        self.store.insert_link(
                            self._last_memory_id, memory_id,
                            link_type="causal.led_to",
                            weight=link_weight,
                            reason=f"写入时因果 ({best.source}): {best.explanation}",
                        )
                    elif best.confidence >= 0.7:
                        # 高置信度但无明确切分 → 前因相关
                        self.store.insert_link(
                            self._last_memory_id, memory_id,
                            link_type="causal.timeline_before",
                            weight=link_weight * 0.8,
                            reason=f"写入时因果 ({best.source}): {best.explanation}",
                        )

            # 更新窗口状态
            self._last_time_ts = int(ts)
            self._last_person = person_id
            self._last_memory_id = memory_id
            self._last_topic = topics[0] if topics else ""
            self._window_buffer.append(memory_id)
            if len(self._window_buffer) > self._window_size:
                self._window_buffer.pop(0)

        result = {
            "memory_id": memory_id,
            "time_id": time_id,
            "person_id": person_id,
            "nature_id": nature_id,
            "topics": topics,
            "tools": tool_ids,
            "knowledge": knowledge_ids,
            "importance": importance,
            "task_id": task_id,
            "emotion": emotion,
            # Phase 2.1: 双时间线信息
            "temporal_signals": temporal_signals,
            "invalidated_ids": invalidated_ids,
            # Phase 2.2: 实体信息
            "entity_ids": entity_ids,
        }
        # S-10: 附带合规扫描结果
        if compliance_result is not None and not compliance_result.is_compliant:
            result["compliance"] = {
                "risk_level": compliance_result.risk_level,
                "detected_types": compliance_result.detected_types,
                "redacted": True,
            }
        return result

    def _update_daily_index(self, ts: float, memory_id: str, topics: list[str], nature_id: str, importance: str):
        """写入时自动生成/更新每日索引文件

        Fix (P0): 加线程锁 + 原子写入，防止多线程同时写同一 JSON 文件导致损坏。
        Fix (Bug 2): 移除 fcntl 文件锁，改用 threading.Lock 实现线程安全。
        """
        dt = datetime.fromtimestamp(ts)
        date_str = dt.strftime("%Y-%m-%d")
        hour_str = dt.strftime("%H:%M")

        os.makedirs(self._index_dir, exist_ok=True)
        index_path = os.path.join(self._index_dir, f"{date_str}.json")
        lock_path = index_path + ".lock"

        # Fix (Bug 2): 用线程锁替代 fcntl 文件锁，防止同进程内多线程并发写入
        with _index_write_lock:
            try:
                # 读取已有索引
                if os.path.exists(index_path):
                    try:
                        with open(index_path, "r", encoding="utf-8") as f:
                            index = json.load(f)
                    except (json.JSONDecodeError, IOError):
                        index = {
                            "date": date_str, "total": 0,
                            "topics_summary": {}, "entries": [],
                        }
                else:
                    index = {
                        "date": date_str, "total": 0,
                        "topics_summary": {}, "entries": [],
                    }

                # 追加条目
                entry = {
                    "time": hour_str,
                    "memory_id": memory_id,
                    "topics": topics,
                    "nature": nature_id,
                    "importance": importance,
                }
                index["entries"].append(entry)
                index["total"] = len(index["entries"])

                for topic in topics:
                    if topic not in index["topics_summary"]:
                        index["topics_summary"][topic] = 0
                    index["topics_summary"][topic] += 1

                # 原子写入：唯一 tmp → rename（防止多线程共用 .tmp 互相覆盖）
                import uuid as _uuid
                tmp_path = f"{index_path}.{os.getpid()}.{_uuid.uuid4().hex[:8]}.tmp"
                with open(tmp_path, "w", encoding="utf-8") as f:
                    json.dump(index, f, ensure_ascii=False, indent=2)
                os.replace(tmp_path, index_path)
            except Exception as e:
                logger.warning("pipeline: %s", e)

    def set_window_size(self, size: int):
        """设置连续对话窗口大小"""
        self._window_size = size

    def _handle_temporal_correction(
        self,
        content: str,
        new_memory_id: str,
        person_id: str,
        topics: list[str],
    ) -> list[str]:
        """
        Phase 2.1: 处理修正信号 — 查找相关旧记忆并标记失效。

        策略：
        1. 在同一人物、同主题的范围内查找旧记忆
        2. 对每条旧记忆检测是否被新内容修正
        3. 如果检测到修正，调用 TemporalReasoner.mark_invalid 标记失效

        返回: 被标记失效的记忆 ID 列表
        """
        invalidated = []
        try:
            # 查找同人物的近期记忆（最近 30 天）
            time_from = int(time.time()) - 86400 * 30
            candidates = self.store.query(
                time_from=time_from,
                person_id=person_id,
                limit=20,
            )

            for mem in candidates:
                mid = mem.get("memory_id", "")
                if mid == new_memory_id:
                    continue
                # 跳过已经失效的
                if not self.temporal_reasoner.is_fact_valid(mem):
                    continue
                # 检测是否被修正
                if self.temporal_reasoner.detect_invalidation(content, mem) and self.temporal_reasoner.mark_invalid(mid, new_memory_id, self.store):
                    invalidated.append(mid)

            if invalidated:
                logger.info(
                    "temporal: 修正信号检测到 %d 条旧记忆被标记失效",
                    len(invalidated),
                )
        except Exception as e:
            logger.warning("temporal: 修正处理异常: %s", e)

        return invalidated

    def _handle_llm_invalidation(
        self,
        content: str,
        new_memory_id: str,
        person_id: str,
        already_invalidated: list[str] | None = None,
    ) -> list[str]:
        """
        Phase 2.1+: LLM 驱动的事实失效检测。

        查找同人物的近期旧记忆，用 LLM 判断新内容是否使旧事实失效。
        LLM 调用失败时静默跳过。

        参数:
            content: 新写入的内容
            new_memory_id: 新记忆 ID
            person_id: 人物 ID
            already_invalidated: 已被规则引擎标记失效的记忆 ID 列表（排除用）

        返回: 被标记失效的记忆 ID 列表
        """
        invalidated = []
        already_invalidated = already_invalidated or []

        try:
            # 查找同人物的近期记忆（最近 30 天）
            time_from = int(time.time()) - 86400 * 30
            candidates = self.store.query(
                time_from=time_from,
                person_id=person_id,
                limit=20,
            )

            # 过滤掉自身和已失效的记忆
            old_facts = []
            for mem in candidates:
                mid = mem.get("memory_id", "")
                if mid == new_memory_id:
                    continue
                if mid in already_invalidated:
                    continue
                if not self.temporal_reasoner.is_fact_valid(mem):
                    continue
                old_facts.append(mem)

            if not old_facts:
                return []

            # 调用 LLM 检测失效
            invalidation_results = self.temporal_reasoner.detect_invalidation_llm(
                new_content=content,
                old_facts=old_facts,
            )

            # 根据检测结果标记失效
            for item in invalidation_results:
                old_id = item.get("old_fact_id", "")
                reason = item.get("reason", "")
                if not old_id:
                    continue
                # 匹配完整 memory_id（LLM 返回的可能是截断的 ID）
                matched_id = None
                for mem in old_facts:
                    if mem.get("memory_id", "").startswith(old_id) or old_id == mem.get("memory_id", ""):
                        matched_id = mem["memory_id"]
                        break
                if matched_id and self.temporal_reasoner.mark_invalid(matched_id, new_memory_id, self.store):
                    invalidated.append(matched_id)
                    logger.info(
                        "temporal: LLM 检测到记忆 %s 失效 (reason=%s)",
                        matched_id[:16], reason[:50],
                    )

            if invalidated:
                logger.info(
                    "temporal: LLM 事实失效检测标记 %d 条旧记忆失效",
                    len(invalidated),
                )
        except Exception as e:
            logger.warning("temporal: LLM 失效检测异常: %s", e)

        return invalidated

    def set_throttle(self, max_writes_per_sec: int = 20):
        """配置写入限流参数"""
        self._throttle_max_writes = max_writes_per_sec

    def _is_throttled(self) -> bool:
        """
        检查是否触发写入限流。

        策略：1 秒内最多允许 throttle_max_writes 次写入。
        high 重要度不受限（跳过检查由 skip_throttle 参数控制）。
        """
        now = time.time()
        with self._state_lock:
            # 清理过期的记录
            self._write_timestamps = [t for t in self._write_timestamps if now - t < self._throttle_window_sec]

            if len(self._write_timestamps) >= self._throttle_max_writes:
                return True

            self._write_timestamps.append(now)
            return False

    def set_llm(self, llm_fn):
        """设置 LLM 函数，启用多主题智能拆分 + 情感 LLM 精修 + LLM 事实失效检测
        llm_fn 签名: fn(prompt: str) -> str
        """
        self.llm_fn = llm_fn
        self.splitter = TopicSplitter(self.encoder, llm_fn=llm_fn)
        self.emotion_analyzer = EmotionAnalyzer(llm_fn=llm_fn)
        self.temporal_reasoner = TemporalReasoner(llm_fn=llm_fn)

    def batch_ingest(
        self,
        messages: list[dict],
        person_code: str = "main",
    ) -> list[dict]:
        """
        批量写入消息（跳过限流，每批最多 MAX_BATCH_SIZE 条）。

        messages: [{"content": str, "importance": str, ...}, ...]

        返回: 写入结果列表
        """
        results = []
        batch = messages[:self.MAX_BATCH_SIZE]

        for msg in batch:
            result = self.ingest(
                content=msg.get("content", ""),
                person_code=person_code,
                ts=msg.get("ts"),
                topics=msg.get("topics"),
                nature_code=msg.get("nature_code"),
                importance=msg.get("importance", "medium"),
                skip_throttle=True,
            )
            # Fix #2: 保留原始 content 供后续向量批量写入使用
            result["_content"] = msg.get("content", "")
            results.append(result)

        return results

    def split_and_ingest(
        self,
        content: str,
        person_code: str = "main",
        ts: float = None,
        importance: str = "medium",
    ) -> list[dict]:
        """
        先用 LLM 拆分多主题，再逐片段写入。
        返回所有写入的 memory 记录列表。
        """
        ts = ts or time.time()
        fragments = self.splitter.split(content)

        results = []
        for i, frag in enumerate(fragments):
            frag_ts = ts + i  # 同一秒内递增
            topics = [frag["topic"]] if frag.get("topic") else None
            nature = frag.get("nature") or None
            tools = frag.get("tools") or None
            knowledge = frag.get("knowledge") or None

            result = self.ingest(
                content=frag["content"],
                person_code=person_code,
                ts=frag_ts,
                topics=topics,
                nature_code=nature,
                tool_codes=tools,
                knowledge_codes=knowledge,
                importance=importance,
            )
            result["_split_fragment"] = i
            results.append(result)

        return results

    # ── 异步写入队列 ──────────────────────────────────

    def enable_async_queue(self, max_queue_size: int = 1000, batch_size: int = 50, flush_interval_ms: int = 500):
        """启用异步写入队列"""
        self._write_queue = WriteQueue(
            pipeline=self,
            max_queue_size=max_queue_size,
            batch_size=batch_size,
            flush_interval_ms=flush_interval_ms,
        )
        self._write_queue.start()
        logger.info("异步写入队列已启用")

    def async_ingest(self, **kwargs) -> dict:
        """
        异步写入：放入队列立即返回，后台持久化。
        参数同 ingest()。
        如果队列未启用，降级为同步写入。
        """
        if self._write_queue and self._write_queue._running:
            return self._write_queue.enqueue(**kwargs)
        # 降级：同步写入
        return self.ingest(**kwargs)

    def shutdown(self, drain: bool = True, timeout: float = 10.0):
        """关闭异步队列和后台线程"""
        if self._write_queue:
            self._write_queue.stop(drain=drain, timeout=timeout)
            self._write_queue = None

    def get_queue_stats(self) -> dict | None:
        """获取异步队列统计"""
        if self._write_queue:
            return self._write_queue.get_stats()
        return None
