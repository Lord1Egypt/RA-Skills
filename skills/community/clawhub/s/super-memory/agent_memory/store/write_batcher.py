"""Write batcher for high-concurrency SQLite writes.

Batches individual write requests and commits them together,
reducing SQLite lock contention and improving throughput.
"""

import queue
import threading
import time
import logging
from typing import Any, Optional
from concurrent.futures import Future

logger = logging.getLogger(__name__)


class WriteBatcher:
    """Batch write operations to reduce SQLite lock contention.

    Instead of each write acquiring its own SQLite lock,
    writes are queued and committed in batches.

    Usage:
        batcher = WriteBatcher(store)
        future = batcher.submit("content", "mem_id")
        result = future.result(timeout=5)  # Wait for write to complete
    """

    def __init__(self, store, batch_size=50, flush_interval=0.1, max_queue=10000):
        self._store = store
        self._batch_size = batch_size
        self._flush_interval = flush_interval
        self._max_queue = max_queue
        self._queue = queue.Queue(maxsize=max_queue)
        self._stopped = threading.Event()
        self._writer_thread = threading.Thread(
            target=self._writer_loop,
            daemon=True,
            name="WriteBatcher",
        )
        self._writer_thread.start()
        self._stats = {
            "total_submitted": 0,
            "total_committed": 0,
            "total_errors": 0,
            "batch_count": 0,
        }
        self._stats_lock = threading.Lock()

    def submit(self, content: str, memory_id: str = None, **kwargs) -> Future:
        """Submit a write request. Returns a Future for the result."""
        if self._stopped.is_set():
            raise RuntimeError("WriteBatcher is stopped")

        future = Future()
        self._queue.put((content, memory_id, kwargs, future), timeout=30)

        with self._stats_lock:
            self._stats["total_submitted"] += 1

        return future

    def _writer_loop(self):
        """Background thread that batches and commits writes."""
        batch = []
        last_flush = time.time()

        while not self._stopped.is_set() or not self._queue.empty():
            try:
                # Try to get an item with timeout
                try:
                    item = self._queue.get(timeout=self._flush_interval)
                    batch.append(item)
                except queue.Empty:
                    pass

                # Flush if batch is full or interval elapsed
                now = time.time()
                should_flush = (
                    len(batch) >= self._batch_size or
                    (batch and now - last_flush >= self._flush_interval)
                )

                if should_flush and batch:
                    self._flush_batch(batch)
                    batch = []
                    last_flush = now

            except Exception as e:
                logger.error("WriteBatcher error: %s", e)
                # Fail all pending items in batch
                for content, memory_id, kwargs, future in batch:
                    if not future.done():
                        future.set_exception(e)
                batch = []
                with self._stats_lock:
                    self._stats["total_errors"] += 1

        # Flush remaining items on shutdown
        if batch:
            self._flush_batch(batch)

    def _flush_batch(self, batch):
        """Commit a batch of writes in a single transaction."""
        try:
            # Use store's transaction for atomic batch commit
            with self._store.transaction():
                for content, memory_id, kwargs, future in batch:
                    try:
                        result = self._store.insert_memory(content, memory_id, **kwargs)
                        future.set_result(result)
                        with self._stats_lock:
                            self._stats["total_committed"] += 1
                    except Exception as e:
                        future.set_exception(e)
                        with self._stats_lock:
                            self._stats["total_errors"] += 1

            with self._stats_lock:
                self._stats["batch_count"] += 1

        except Exception as e:
            # Transaction failed — fail all items
            logger.error("Batch commit failed: %s", e)
            for content, memory_id, kwargs, future in batch:
                if not future.done():
                    future.set_exception(e)
            with self._stats_lock:
                self._stats["total_errors"] += len(batch)

    def flush(self):
        """Wait for all queued writes to complete."""
        # Submit a sentinel and wait for it
        sentinel = Future()
        self._queue.put((None, None, {}, sentinel), timeout=30)
        try:
            sentinel.result(timeout=60)
        except Exception:
            pass  # Sentinel doesn't actually write

    def stop(self, timeout=10):
        """Stop the batcher and flush remaining writes."""
        self._stopped.set()
        self._writer_thread.join(timeout=timeout)

    def get_stats(self) -> dict:
        """Return batcher statistics."""
        with self._stats_lock:
            return dict(self._stats)
