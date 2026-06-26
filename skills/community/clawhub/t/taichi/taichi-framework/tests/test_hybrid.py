#!/usr/bin/env python3
"""
Hybrid mode integration test.
Run: python tests/test_hybrid.py
Requires Redis running.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.worker.hybrid_worker import HybridWorker
from core.worker.group_coordinator import GroupCoordinator
from core.skills.skill_registry import SkillRegistry


async def test_hybrid():
    print("[test] Starting hybrid mode test...")

    skill_reg = SkillRegistry("configs/skills/manifest.yaml")
    redis_url = "redis://localhost:6379"

    # Clean
    import redis.asyncio as redis
    r = await redis.from_url(redis_url)
    await r.delete("taichi:group:tasks")
    await r.aclose()

    # Start 3 planner workers
    worker_ids = []
    workers = []
    for i in range(3):
        wid = f"test-planner-{i}"
        w = HybridWorker(wid, redis_url, skill_reg, {})
        workers.append(w)
        worker_ids.append(wid)
        await w.start()
    print(f"[test] Started {len(workers)} workers")

    await asyncio.sleep(1)

    # Test coordinator
    coord = GroupCoordinator("test_group", "planner", worker_ids, redis_url, "voting_merge")
    await coord.connect()

    result = await coord.execute({"text": "test hybrid task"})
    print(f"[test] Coordinator result: {result}")

    # shutdown
    for w in workers:
        await w.stop()

    print("[test] PASSED")


if __name__ == "__main__":
    asyncio.run(test_hybrid())
