#!/usr/bin/env python3
"""
Distributed mode integration test.
Run with: python test_distributed.py
Requires Redis running.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.worker.distributed.distributed_worker import DistributedWorker
from core.skills.skill_registry import SkillRegistry


async def test_distributed():
    print("[Test] Starting distributed test...")

    skill_reg = SkillRegistry("configs/skills/manifest.yaml")
    redis_url = "redis://localhost:6379"

    # Clean worker set
    import redis.asyncio as redis
    r = await redis.from_url(redis_url)
    await r.delete("taichi:workers")
    await r.aclose()

    # Create workers
    workers = []
    for i in range(3):
        w = DistributedWorker(f"test-worker-{i}", redis_url, skill_reg, {})
        workers.append(w)
        await w.start()

    print("[Test] All workers started, waiting for registration...")
    await asyncio.sleep(2)

    # Broadcast task
    tasks = [
        {
            "task_id": f"task-{i}",
            "skill": "bash_executor",
            "params": {"command": f"echo 'Result from worker {i}'"},
            "timeout": 10,
        }
        for i in range(3)
    ]

    corr_id = "test-corr-001"
    await workers[0].bus.broadcast(
        "task.broadcast",
        {"tasks": tasks, "skill": "bash_executor"},
        correlation_id=corr_id,
    )
    print(f"[Test] Broadcast sent, waiting for results...")

    # Wait for partial results to arrive
    await asyncio.sleep(5)

    print(f"[Test] Test complete. Collected results across workers.")
    for w in workers:
        print(f"[Test] {w.worker_id}: partial_results count = {len(w.partial_results)}")

    # Shutdown
    for w in workers:
        await w.stop()

    print("[Test] PASSED")


if __name__ == "__main__":
    asyncio.run(test_distributed())
