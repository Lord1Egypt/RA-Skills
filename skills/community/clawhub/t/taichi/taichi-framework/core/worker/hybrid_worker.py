"""
HybridWorker - 元混合模式的 Worker

从共享 Redis List 接收 GroupCoordinator 的任务，
根据 role/protocol 执行对应逻辑，完成后结果写入 result_key。
"""
import asyncio
import json
import logging
from typing import Optional

import redis.asyncio as redis
from core.skills.skill_executor import SkillExecutor

logger = logging.getLogger("taichi.hybridworker")


class HybridWorker:
    def __init__(self, worker_id: str, redis_url: str, skill_registry, config: dict):
        self.worker_id = worker_id
        self.redis_url = redis_url
        self.skill_executor = SkillExecutor(skill_registry)
        self.config = config
        self.redis: Optional[redis.Redis] = None
        self._running = True
        self._task_queue = "taichi:group:tasks"

    async def start(self):
        """启动 Worker：连接到 Redis，开始监听任务队列"""
        self.redis = await redis.from_url(self.redis_url, decode_responses=True)
        asyncio.create_task(self._heartbeat())
        asyncio.create_task(self._listen_tasks())
        logger.info(f"[{self.worker_id}] HybridWorker started")

    async def _listen_tasks(self):
        """从共享队列阻塞接收任务（BLPOP）"""
        while self._running:
            try:
                result = await self.redis.blpop(self._task_queue, timeout=5)
                if result is None:
                    continue
                _, task_json = result
                task = json.loads(task_json)
                await self._handle_task(task)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[{self.worker_id}] error: {e}")
                await asyncio.sleep(1)

    async def _handle_task(self, task: dict):
        """根据 role 和 protocol 执行任务"""
        role = task.get("role")
        protocol = task.get("protocol")
        input_data = task.get("input", {})
        result_key = task.get("result_key")
        session_id = task.get("session_id")

        logger.info(f"[{self.worker_id}] handling {role}/{protocol} for {session_id}")

        if role == "planner":
            result = await self._role_planner(input_data)
        elif role == "drafter":
            result = await self._role_drafter(input_data)
        elif role == "validator":
            result = await self._role_validator(input_data)
        elif role == "dispatcher":
            result = await self._role_dispatcher(input_data)
        else:
            result = {"error": f"Unknown role: {role}"}

        # 写回结果
        await self.redis.lpush(result_key, json.dumps(result))
        logger.info(f"[{self.worker_id}] completed {role}/{protocol}")

    async def _role_planner(self, input_data: dict) -> dict:
        """Planner：生成 DAG"""
        text = input_data.get("text", "")
        return {
            "nodes": [
                {
                    "id": f"node-{i}",
                    "description": f"处理: {text} (step {i})",
                    "depends_on": [] if i == 0 else [f"node-{i-1}"],
                    "complexity": 1,
                }
                for i in range(min(3, max(1, len(text) // 5)))
            ],
            "entry_points": ["node-0"],
            "exit_points": ["node-0"],
        }

    async def _role_drafter(self, input_data: dict) -> dict:
        """Drafter：为 DAG 节点生成任务方案"""
        dag = input_data.get("dag", {})
        nodes = dag.get("nodes", [])
        tasks = []
        for node in nodes:
            tasks.append({
                "task_id": node["id"],
                "skill": "bash_executor",
                "params": {"command": f"echo 'Draft: {node['description']}'"},
                "timeout": 30,
            })
        return {"tasks": tasks}

    async def _role_validator(self, input_data: dict) -> dict:
        """Validator：校验方案"""
        draft = input_data.get("draft", {})
        tasks = draft.get("tasks", [])
        if not tasks:
            return {"status": "rejected", "reasons": ["No tasks"], "modifications": []}
        return {"status": "approved", "modifications": []}

    async def _role_dispatcher(self, input_data: dict) -> dict:
        """Dispatcher：确认任务已接收"""
        return {"status": "dispatched", "tasks": input_data.get("tasks", [])}

    async def _heartbeat(self):
        while self._running:
            await asyncio.sleep(5)
            try:
                r = await redis.from_url(self.redis_url, decode_responses=True)
                await r.lpush("taichi:workers:hybrid", json.dumps({
                    "id": self.worker_id,
                    "ts": asyncio.get_event_loop().time(),
                }))
                await r.aclose()
            except Exception as e:
                logger.error(f"[{self.worker_id}] heartbeat error: {e}")

    async def stop(self):
        self._running = False
        if self.redis:
            await self.redis.aclose()
