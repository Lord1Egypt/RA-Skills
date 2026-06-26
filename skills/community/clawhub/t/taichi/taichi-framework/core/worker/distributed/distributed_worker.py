import asyncio
import json
import logging
import time
from typing import List, Any

from core.skills.skill_executor import SkillExecutor
from .distributed_bus import DistributedBus

logger = logging.getLogger("taichi.distworker")


class DistributedWorker:
    """
    Peer worker in distributed mode.
    Workers communicate directly with each other via DistributedBus.
    No central dispatcher - they negotiate task distribution themselves.
    """

    def __init__(self, worker_id: str, redis_url: str, skill_registry, config: dict):
        self.worker_id = worker_id
        self.redis_url = redis_url
        self.skill_executor = SkillExecutor(skill_registry)
        self.config = config
        self.bus = DistributedBus(redis_url, worker_id)
        self.peers: List[str] = []
        self.assigned_shard: int = 0
        self.total_shards: int = 0
        self.partial_results: List[Any] = []
        self._running = True
        self._result_collector_task: asyncio.Task = None

    async def start(self):
        await self.bus.connect()
        # Register message handlers
        await self.bus.register_handler("task.broadcast", self._on_task_broadcast)
        await self.bus.register_handler("peer.discovered", self._on_peer_discovered)
        await self.bus.register_handler("result.partial", self._on_partial_result)
        await self.bus.register_handler("result.final", self._on_final_result)
        await self.bus.register_handler("shutdown", self._on_shutdown)

        # Register self in Redis worker set
        await self._register()

        # Start heartbeat
        asyncio.create_task(self._heartbeat())

        logger.info(f"[{self.worker_id}] Started")

    async def _register(self):
        """Register this worker in the shared worker set."""
        r = await self.bus.redis_client.__class__.from_url(self.redis_url, decode_responses=True)
        await r.sadd("taichi:workers", self.worker_id)
        # Fetch all workers
        peers = await r.smembers("taichi:workers")
        self.peers = [p for p in peers if p != self.worker_id]
        await r.aclose()
        logger.info(f"[{self.worker_id}] Registered, peers: {self.peers}")

    async def _heartbeat(self):
        """Send periodic heartbeat to shared hash."""
        while self._running:
            await asyncio.sleep(5)
            try:
                r = await self.bus.redis_client.__class__.from_url(self.redis_url, decode_responses=True)
                await r.hset(f"taichi:worker:{self.worker_id}", "heartbeat", time.time())
                await r.sadd("taichi:workers", self.worker_id)
                await r.aclose()
            except Exception as e:
                logger.error(f"[{self.worker_id}] Heartbeat error: {e}")

    async def _on_task_broadcast(self, message: dict):
        """Receive broadcast task, negotiate shard assignment, process."""
        logger.info(f"[{self.worker_id}] Received task broadcast")
        task_payload = message["payload"]
        correlation_id = message.get("correlation_id")
        total = len(self.peers) + 1  # include self

        # Consistent hash: sort workers, find my index
        all_workers = sorted(self.peers + [self.worker_id])
        my_index = all_workers.index(self.worker_id)

        shard_tasks = task_payload.get("tasks", [])
        # Distribute tasks round-robin by index
        my_tasks = [t for i, t in enumerate(shard_tasks) if i % total == my_index]

        logger.info(f"[{self.worker_id}] assigned {len(my_tasks)} tasks (shard {my_index}/{total})")

        # Execute assigned tasks
        results = []
        for task in my_tasks:
            result = await self._execute_task(task)
            results.append(result)

        # Send partial results to orchestrator (or first peer acting as collector)
        await self.bus.broadcast(
            "result.partial",
            {
                "from": self.worker_id,
                "shard_index": my_index,
                "results": results,
            },
            correlation_id=correlation_id,
        )
        logger.info(f"[{self.worker_id}] Sent {len(results)} partial results")

    async def _on_partial_result(self, message: dict):
        """Collect partial results from other workers."""
        self.partial_results.append(message["payload"])
        logger.info(f"[{self.worker_id}] Collected partial result from {message['payload'].get('from')}, "
                    f"total: {len(self.partial_results)}")

    async def _on_final_result(self, message: dict):
        """Final merged result received."""
        logger.info(f"[{self.worker_id}] Final result: {message['payload']}")

    async def _on_peer_discovered(self, message: dict):
        """New peer announced itself."""
        peer = message["from"]
        if peer not in self.peers:
            self.peers.append(peer)
            logger.info(f"[{self.worker_id}] New peer discovered: {peer}")

    async def _on_shutdown(self, message: dict):
        logger.info(f"[{self.worker_id}] Shutdown signal received")
        self._running = False

    async def _execute_task(self, task: dict) -> dict:
        """Execute a single task via SkillExecutor."""
        skill_name = task.get("skill", "bash_executor")
        params = task.get("params", {})
        return await self.skill_executor.execute(skill_name, params)

    async def stop(self):
        self._running = False
        await self.bus.close()
