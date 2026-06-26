import asyncio
import json
from typing import Dict, Optional, TYPE_CHECKING
from .base_agent import BaseAgent
from core.worker.worker_manager import WorkerManager

if TYPE_CHECKING:
    from core.communication.centralized_bus import CentralizedBus


class DispatcherAgent(BaseAgent):
    """
    Dispatcher Agent: dispatches validated tasks to workers via Redis List,
    collects results by polling Redis List keyed by correlation_id.
    Input:  validate.result (approved)
    Output: dispatch.completed -> orchestrator
    """

    def __init__(self, name: str, bus: 'CentralizedBus', config: dict, skill_registry=None):
        super().__init__(name, bus, config)
        self.worker_manager: Optional[WorkerManager] = None
        self.skill_registry = skill_registry
        self.pending_futures: Dict[str, asyncio.Future] = {}
        self._task_queue_key = "taichi:tasks"

    async def start(self):
        await super().start()
        self.worker_manager = WorkerManager(
            worker_config=self.config.get("worker_pool", {}),
            bus=self.bus,
            skill_registry=self.skill_registry,
        )
        await self.worker_manager.start()

    async def handle_message(self, message: dict):
        msg_type = message.get("type")
        if msg_type == "validate.result":
            payload = message["payload"]
            if payload.get("status") == "approved":
                await self._dispatch_tasks(payload.get("tasks", []), message["correlation_id"])

    async def _dispatch_tasks(self, tasks: list, correlation_id: str):
        if not tasks:
            await self.send(
                to="orchestrator",
                msg_type="dispatch.completed",
                payload={"results": []},
                correlation_id=correlation_id,
            )
            return

        # Push all tasks to Redis List
        for task in tasks:
            msg = {
                "type": "task.assign",
                "to_dispatcher": "DispatcherAgent",
                "payload": task,
                "correlation_id": correlation_id,
            }
            await self.bus.redis_client.rpush(self._task_queue_key, json.dumps(msg))

        # Collect results by polling Redis
        results = []
        result_key = f"taichi:results:{correlation_id}"
        timeout = 30
        start = asyncio.get_event_loop().time()

        while len(results) < len(tasks) and (asyncio.get_event_loop().time() - start) < timeout:
            result = await self.bus.redis_client.lpop(result_key)
            if result:
                results.append(json.loads(result))
            else:
                await asyncio.sleep(0.1)

        await self.bus.redis_client.delete(result_key)

        await self.send(
            to="orchestrator",
            msg_type="dispatch.completed",
            payload={"results": results},
            correlation_id=correlation_id,
        )

    async def stop(self):
        if self.worker_manager:
            await self.worker_manager.stop()
        await super().stop()
