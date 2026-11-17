"""零稀泥模式 — 事件发布器 event_publisher.py

Usage:
    pub = EventPublisher(state_path="/path/to/state")
    pub.publish("fix_closure", "bug-001", data={...})
    pub.publish_learn(data, learn_callback=my_learn_fn)
"""

import json, os, logging
from typing import Optional, Callable

log = logging.getLogger("event_publisher")


class EventPublisher:
    """事件发布器 — events.ndjson + 可选 learn 回调"""

    def __init__(self, state_dir: str = ".", state_path: str = "",
                 learn_callback: Optional[Callable] = None):
        """初始化事件发布器

        Args:
            state_dir: state 文件所在目录（state_path 优先）
            state_path: state 文件完整路径
            learn_callback: 可选的外部 learn 回调，替代动态 import pipeline
        """
        if state_path:
            self.events_path = os.path.join(os.path.dirname(state_path), "events.ndjson")
        else:
            self.events_path = os.path.join(state_dir, "events.ndjson")
        self._learn_callback = learn_callback

    def publish(self, kind: str, bug_id: str, data: dict = None, timestamp: str = "") -> dict:
        """发布事件到 events.ndjson"""
        from datetime import datetime, timezone
        ev = {
            "kind": kind, "bug_id": bug_id,
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        if data:
            ev.update(data)
        from . import file_ops as _fo
        lk = _fo.acquire_file_lock(self.events_path)
        try:
            with open(self.events_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        except Exception as e:
            log.warning("event fail: %s", e)
        finally:
            if lk:
                _fo.release_file_lock(self.events_path)
        return ev

    def publish_learn(self, data: dict, learn_callback: Optional[Callable] = None) -> dict:
        """发布 learn 事件

        优先级:
        1. 参数 learn_callback（最高优先级）
        2. 实例级别 self._learn_callback
        3. 动态 import pipeline.learn（向后兼容）
        4. fallback 到 events.ndjson
        """
        cb = learn_callback or self._learn_callback
        if cb is not None:
            try:
                cb(data)
                return data
            except Exception as e:
                log.warning("learn callback 失败: %s", e)
                # callback 失败不 fallback 到 import pipeline——直接返回
                return data

        # 向后兼容: 动态 import pipeline（仅当无 callback 时才尝试）
        try:
            import pipeline as _p
            if hasattr(_p, "learn"):
                _p.learn(data=data)
                return data
            raise ImportError("pipeline.learn not found")
        except Exception as e:
            log.warning("learn fail (fallback to events): %s", e)
            return self.publish(
                kind=data.get("kind", "fix_closure"),
                bug_id=data.get("bug_id", "?"),
                data=data,
            )
