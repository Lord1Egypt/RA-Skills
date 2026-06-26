import asyncio
import uuid
from typing import Dict, Optional

from core.worker.worker import Worker
from core.skills.skill_executor import SkillExecutor


class WorkerManager:
    """
    Manages a pool of workers: creation, heartbeat monitoring, and acquisition.
    """

    def __init__(self, worker_config: dict, bus, skill_registry=None):
        self.config = worker_config
        self.bus = bus
        self.skill_registry = skill_registry
        self.workers: Dict[str, Worker] = {}
        self.idle_workers: asyncio.Queue = asyncio.Queue()
        self._running = True
        self._worker_count = 0

    async def start(self):
        """Start initial worker pool."""
        initial = self.config.get("initial_size", 3)
        for _ in range(initial):
            await self._create_worker()
        asyncio.create_task(self._monitor())

    async def acquire_worker(self) -> Worker:
        """Get an idle worker. Block if none available."""
        return await self.idle_workers.get()

    async def release_worker(self, worker: Worker):
        """Return a worker to the idle pool."""
        await self.idle_workers.put(worker)

    async def _create_worker(self) -> Worker:
        """Create and start a new worker."""
        worker_id = f"worker-{uuid.uuid4().hex[:8]}"
        executor = SkillExecutor(self.skill_registry) if self.skill_registry else None
        worker = Worker(worker_id, self.bus, executor)
        self.workers[worker_id] = worker
        self._worker_count += 1
        await worker.start()
        await self.idle_workers.put(worker)
        return worker

    async def _monitor(self):
        """Monitor worker health and scale pool."""
        while self._running:
            await asyncio.sleep(10)
            # Clean up dead workers
            dead = [wid for wid, w in self.workers.items() if not w._running]
            for wid in dead:
                del self.workers[wid]

            # Auto-scale: maintain idle pool
            max_size = self.config.get("max_size", 20)
            idle_count = self.idle_workers.qsize()
            if idle_count < 2 and self._worker_count < max_size:
                await self._create_worker()

    async def stop(self):
        """Stop all workers."""
        self._running = False
        for worker in self.workers.values():
            await worker.stop()
        self.workers.clear()
