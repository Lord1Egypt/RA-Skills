"""
GroupCoordinator - 元混合模式的组协调器

负责：
1. 管理一组 Worker（通过 Redis List 分发任务）
2. 收集 Worker 执行结果
3. 按协议合并结果（voting_merge / shard_draft / cross_check / consistent_hash）
4. 返回合并后的输出到下一个 Group 或 Orchestrator
"""
import asyncio
import json
import uuid
import logging
from typing import Dict, Any, List, Optional

import redis.asyncio as redis

logger = logging.getLogger("taichi.coordinator")


class GroupCoordinator:
    def __init__(
        self,
        group_id: str,
        role: str,
        worker_ids: List[str],
        redis_url: str,
        protocol: str,
        timeout_sec: int = 30,
    ):
        self.group_id = group_id
        self.role = role
        self.worker_ids = worker_ids
        self.redis_url = redis_url
        self.protocol = protocol
        self.timeout_sec = timeout_sec
        self.redis: Optional[redis.Redis] = None
        self.task_queue = "taichi:group:tasks"
        self._running_workers = set()

    async def connect(self):
        self.redis = await redis.from_url(self.redis_url, decode_responses=True)

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行组任务：
        1. 生成 session_id
        2. 向每个 Worker 发送任务（通过 Redis List）
        3. 收集结果
        4. 按协议合并
        """
        session_id = f"{self.group_id}:{uuid.uuid4().hex[:8]}"
        result_key = f"taichi:results:{session_id}"

        # 向每个 Worker 发送任务（JSON 包含 session_id、role、protocol、input）
        task_msg = json.dumps({
            "session_id": session_id,
            "role": self.role,
            "protocol": self.protocol,
            "input": input_data,
            "result_key": result_key,
        })

        for wid in self.worker_ids:
            await self.redis.rpush(self.task_queue, task_msg)
            logger.info(f"[{self.group_id}] sent task to {wid}")

        # 等待 Worker 完成
        results = await self._collect_results(result_key, len(self.worker_ids))

        # 按协议合并结果
        merged = self._merge_results(results, input_data)
        return merged

    async def _collect_results(self, result_key: str, expected: int) -> List[Dict]:
        """从 Redis List 收集结果（阻塞轮询）"""
        start = asyncio.get_event_loop().time()
        results = []
        while len(results) < expected:
            elapsed = asyncio.get_event_loop().time() - start
            if elapsed >= self.timeout_sec:
                logger.warning(f"[{self.group_id}] timeout, got {len(results)}/{expected}")
                break
            res = await self.redis.lpop(result_key)
            if res:
                results.append(json.loads(res))
            else:
                await asyncio.sleep(0.1)
        # 清理
        await self.redis.delete(result_key)
        return results

    def _merge_results(self, results: List[Dict], original_input: Dict) -> Dict[str, Any]:
        """根据协议合并 Worker 结果"""
        if not results:
            return {"error": "No results from workers"}

        if self.protocol == "voting_merge":
            # 选节点最多的 DAG
            best = max(results, key=lambda r: len(r.get("nodes", [])))
            logger.info(f"[{self.group_id}] voting_merge selected DAG with {len(best.get('nodes', []))} nodes")
            return best

        elif self.protocol == "shard_draft":
            # 合并所有任务
            all_tasks = []
            for r in results:
                all_tasks.extend(r.get("tasks", []))
            logger.info(f"[{self.group_id}] shard_draft merged {len(all_tasks)} tasks")
            return {"tasks": all_tasks}

        elif self.protocol == "cross_check":
            # 任一拒绝则整体拒绝，合并修改建议
            status = "approved"
            modifications = []
            for r in results:
                if r.get("status") == "rejected":
                    status = "rejected"
                modifications.extend(r.get("modifications", []))
            logger.info(f"[{self.group_id}] cross_check: {status}")
            return {"status": status, "modifications": modifications}

        elif self.protocol == "consistent_hash":
            # 直接转发 Worker 的调度确认
            return {"status": "dispatched", "workers": len(results)}

        else:
            return {"results": results}
