import asyncio
import json
import uuid
from typing import Optional

from core.skills.skill_executor import SkillExecutor


class Worker:
    """
    Lightweight worker that executes tasks assigned by DispatcherAgent.
    Workers listen on a shared Redis List channel and send results back via Redis List.
    """

    def __init__(self, worker_id: str, bus, skill_executor: SkillExecutor):
        self.worker_id = worker_id
        self.bus = bus
        self.skill_executor = skill_executor
        self._running = True
        self._task_queue_key = "taichi:tasks"

    async def start(self):
        """Listen for tasks on Redis List (BRPOP)."""
        asyncio.create_task(self._heartbeat())
        asyncio.create_task(self._listen_tasks())

    async def _listen_tasks(self):
        """Blocking pop from Redis list - one task at a time."""
        import logging
        logger = logging.getLogger(f"taichi.worker.{self.worker_id}")

        while self._running:
            try:
                # BRPOP: blocking pop from tail (FIFO queue)
                result = await self.bus.redis_client.blpop(self._task_queue_key, timeout=5)
                if result is None:
                    continue

                # result is (key, value)
                _, task_json = result
                task = json.loads(task_json)

                msg_type = task.get("type")
                if msg_type == "task.assign":
                    logger.info(f"Got task: {task.get('payload', {}).get('task_id')}")
                    task_result = await self._execute_task(task.get("payload", {}))
                    result_key = f"taichi:results:{task.get('correlation_id')}"
                    await self.bus.redis_client.rpush(
                        result_key,
                        json.dumps({"task_id": task.get("payload", {}).get("task_id"), **task_result})
                    )
                    logger.info(f"Task done: {task.get('payload', {}).get('task_id')}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker error: {e}")
                await asyncio.sleep(1)

    async def _execute_task(self, task: dict) -> dict:
        """Execute a single task via SkillExecutor."""
        skill_name = task.get("skill", "bash_executor")
        params = task.get("params", {})
        return await self.skill_executor.execute(skill_name, params)

    async def _heartbeat(self):
        """Send periodic heartbeat."""
        import logging
        import time
        logger = logging.getLogger(f"taichi.worker.{self.worker_id}")

        while self._running:
            await asyncio.sleep(10)
            try:
                await self.bus.redis_client.publish(
                    f"agent.WorkerManager",
                    json.dumps({
                        "type": "worker.heartbeat",
                        "from": self.worker_id,
                        "payload": {"timestamp": time.time()},
                    })
                )
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")

    async def stop(self):
        self._running = False
