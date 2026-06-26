"""
实时调用反馈上报器 v0.5.0 — 异步队列 + 批量上报
================================================
在 Skill 调用完成后，将运行指标实时上报到中心服务器。

特性:
  - 异步队列：不阻塞 Skill 执行
  - 批量上报：累积 N 条或 T 秒先到者触发
  - 容错：上报失败静默忽略，不影响用户体验
  - 自动脱敏：上报数据经过 sanitizer 处理
  - 优雅关闭：进程退出时刷新剩余队列

使用方式:
  from skills_monitor.core.realtime_reporter import RealtimeReporter
  rt = RealtimeReporter.get_instance()
  rt.enqueue({"skill_id": "...", "duration_ms": 120, ...})
"""

import atexit
import json
import logging
import queue
import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# 批量上报配置
DEFAULT_BATCH_SIZE = 10         # 累积 10 条触发上报
DEFAULT_FLUSH_INTERVAL = 60.0   # 或 60 秒触发上报
DEFAULT_MAX_QUEUE_SIZE = 500    # 队列上限（防止内存泄漏）
DEFAULT_MAX_RETRIES = 2         # 上报失败最多重试 2 次
DEFAULT_SERVER_URL = "http://localhost:5100"


class RealtimeReporter:
    """
    实时调用反馈上报器（单例模式）

    架构:
      enqueue() → [Queue] → [后台线程] → batch_upload() → 服务器

    后台线程策略:
      - 每 flush_interval 秒检查一次队列
      - 队列中累积 >= batch_size 条时立即上报
      - 进程退出时（atexit）刷新剩余数据
    """

    _instance: Optional["RealtimeReporter"] = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(
        cls,
        server_url: str = DEFAULT_SERVER_URL,
        batch_size: int = DEFAULT_BATCH_SIZE,
        flush_interval: float = DEFAULT_FLUSH_INTERVAL,
    ) -> "RealtimeReporter":
        """获取单例实例"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(server_url, batch_size, flush_interval)
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """重置单例（用于测试）"""
        with cls._lock:
            if cls._instance is not None:
                cls._instance.shutdown()
                cls._instance = None

    def __init__(
        self,
        server_url: str = DEFAULT_SERVER_URL,
        batch_size: int = DEFAULT_BATCH_SIZE,
        flush_interval: float = DEFAULT_FLUSH_INTERVAL,
        max_queue_size: int = DEFAULT_MAX_QUEUE_SIZE,
    ):
        self.server_url = server_url.rstrip("/")
        self.batch_size = batch_size
        self.flush_interval = flush_interval

        self._queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self._shutdown_event = threading.Event()
        self._stats = {
            "enqueued": 0,
            "uploaded": 0,
            "failed": 0,
            "dropped": 0,
            "batches_sent": 0,
        }

        # 身份信息（延迟加载）
        self._agent_id: Optional[str] = None
        self._token: Optional[str] = None

        # 启动后台线程
        self._thread = threading.Thread(
            target=self._worker,
            name="realtime-reporter",
            daemon=True,
        )
        self._thread.start()

        # 进程退出时刷新
        atexit.register(self.shutdown)

    # ──────── 入队 ────────

    def enqueue(self, event: Dict[str, Any]) -> bool:
        """
        将一个运行事件加入上报队列

        Args:
            event: 运行指标字典，至少包含：
                - skill_id: str
                - status: "success" | "error"
                - duration_ms: float
                - 可选: run_id, task_name, error_msg, ...

        Returns:
            True 成功入队, False 队列已满（被丢弃）
        """
        if self._shutdown_event.is_set():
            return False

        # 附加时间戳
        event.setdefault("reported_at", datetime.now().isoformat())

        try:
            self._queue.put_nowait(event)
            self._stats["enqueued"] += 1
            return True
        except queue.Full:
            self._stats["dropped"] += 1
            logger.warning("实时上报队列已满，丢弃事件")
            return False

    # ──────── 后台工作线程 ────────

    def _worker(self):
        """后台线程：定时检查队列并批量上报"""
        logger.debug("RealtimeReporter 后台线程已启动")

        while not self._shutdown_event.is_set():
            # 等待 flush_interval 或被 shutdown 唤醒
            self._shutdown_event.wait(timeout=self.flush_interval)

            # 收集队列中的事件
            batch = self._drain_queue(max_items=self.batch_size * 2)
            if batch:
                self._send_batch(batch)

        # shutdown 后最终刷新
        final_batch = self._drain_queue(max_items=self._queue.qsize() + 10)
        if final_batch:
            self._send_batch(final_batch)

        logger.debug("RealtimeReporter 后台线程已退出")

    def _drain_queue(self, max_items: int = 100) -> List[Dict[str, Any]]:
        """从队列中取出所有可用事件"""
        items = []
        while len(items) < max_items:
            try:
                item = self._queue.get_nowait()
                items.append(item)
            except queue.Empty:
                break
        return items

    # ──────── 批量上报 ────────

    def _send_batch(self, batch: List[Dict[str, Any]]):
        """将一批事件上报到中心服务器"""
        if not batch:
            return

        # 自动脱敏
        try:
            from skills_monitor.core.sanitizer import DataSanitizer
            sanitizer = DataSanitizer()
            batch = [sanitizer.sanitize(event) for event in batch]
        except ImportError:
            pass

        # 延迟加载身份
        self._ensure_identity()

        headers = {
            "X-Agent-ID": self._agent_id or "",
            "X-Agent-Token": self._token or "",
            "Content-Type": "application/json",
        }

        payload = {
            "data": {
                "events": batch,
                "batch_size": len(batch),
                "reported_at": datetime.now().isoformat(),
            },
            "report_type": "realtime_feedback",
        }

        for attempt in range(DEFAULT_MAX_RETRIES + 1):
            try:
                import requests
                resp = requests.post(
                    f"{self.server_url}/api/agent/report",
                    headers=headers,
                    json=payload,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self._stats["uploaded"] += len(batch)
                    self._stats["batches_sent"] += 1
                    logger.debug(f"实时上报成功: {len(batch)} 条事件")
                    return
                else:
                    logger.warning(f"实时上报响应异常: {resp.status_code}")
            except Exception as e:
                if attempt < DEFAULT_MAX_RETRIES:
                    time.sleep(1 * (attempt + 1))  # 指数退避
                else:
                    self._stats["failed"] += len(batch)
                    logger.warning(f"实时上报失败 (重试{attempt}次): {e}")

    def _ensure_identity(self):
        """延迟加载身份信息"""
        if self._agent_id:
            return

        try:
            from skills_monitor.core.identity import IdentityManager
            mgr = IdentityManager()
            self._agent_id = mgr.agent_id
            self._token = mgr.api_key
        except Exception as e:
            logger.warning(f"加载身份失败: {e}")

    # ──────── 生命周期管理 ────────

    def shutdown(self):
        """优雅关闭：刷新剩余队列"""
        if self._shutdown_event.is_set():
            return
        self._shutdown_event.set()

        # 等待后台线程结束（最多 5 秒）
        if self._thread.is_alive():
            self._thread.join(timeout=5)

    def flush(self):
        """手动触发刷新队列（不关闭线程）"""
        batch = self._drain_queue(max_items=self._queue.qsize() + 10)
        if batch:
            self._send_batch(batch)

    # ──────── 状态查询 ────────

    @property
    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self._stats,
            "queue_size": self._queue.qsize(),
            "is_running": not self._shutdown_event.is_set(),
            "thread_alive": self._thread.is_alive(),
        }

    @property
    def pending_count(self) -> int:
        """队列中待上报的事件数"""
        return self._queue.qsize()
