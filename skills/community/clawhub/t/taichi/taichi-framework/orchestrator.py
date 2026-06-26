#!/usr/bin/env python3
"""
Taichi Framework v2.1 - Orchestrator
Main entry point for the multi-agent framework.
Supports: centralized, distributed, hybrid modes.
"""
import asyncio
import json
import shutil
import sys
from pathlib import Path

import click
import yaml

sys.path.insert(0, str(Path(__file__).parent))

from core.utils.logger import setup_logger
from core.communication.centralized_bus import CentralizedBus
from core.agents.planner_agent import PlannerAgent
from core.agents.drafter_agent import DrafterAgent
from core.agents.validator_agent import ValidatorAgent
from core.agents.dispatcher_agent import DispatcherAgent
from core.skills.skill_registry import SkillRegistry
from core.worker.distributed.distributed_worker import DistributedWorker
from core.worker.group_coordinator import GroupCoordinator
from core.worker.hybrid_worker import HybridWorker


# ─────────────────────── centralized ───────────────────────

class Orchestrator:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = None
        self.bus = None
        self.skill_registry = None
        self.agents = {}
        self.logger = None

    async def initialize(self):
        with open(self.config_path) as f:
            self.config = yaml.safe_load(f)

        ws = Path(self.config["workspace"]["path"])
        ws.mkdir(parents=True, exist_ok=True)
        (ws / "logs").mkdir(exist_ok=True)
        (ws / "temp").mkdir(exist_ok=True)

        log_file = self.config["logging"].get("file")
        if log_file:
            log_file = str(ws / "logs" / "taichi.log")
        self.logger = setup_logger(
            name="taichi",
            level=self.config["logging"].get("level", "INFO"),
            log_file=log_file,
        )

        self.bus = CentralizedBus(
            redis_url=self.config["communication"]["redis_url"],
            permissions_config=self.config["communication"]["permissions_config"],
        )
        await self.bus.connect()
        await self.bus.subscribe("orchestrator", self._on_message)

        manifest = self.config["skills"]["manifest_path"]
        if not Path(manifest).is_absolute():
            manifest = str(Path(self.config_path).parent / manifest)
        self.skill_registry = SkillRegistry(manifest)

        cfg = self._load_mode("centralized")
        self.agents["planner"] = PlannerAgent("PlannerAgent", self.bus, cfg)
        self.agents["drafter"] = DrafterAgent("DrafterAgent", self.bus, cfg)
        self.agents["validator"] = ValidatorAgent("ValidatorAgent", self.bus, cfg)
        self.agents["dispatcher"] = DispatcherAgent(
            "DispatcherAgent", self.bus, cfg, self.skill_registry
        )

    def _load_mode(self, mode: str):
        p = Path(self.config_path).parent / "configs" / "modes" / f"{mode}.yaml"
        if p.exists():
            with open(p) as f:
                return yaml.safe_load(f)
        return {}

    async def _on_message(self, msg: dict):
        if msg.get("type") == "dispatch.completed":
            self.logger.info(f"Task completed: {msg.get('correlation_id')}")
            self.logger.info(f"Results: {msg['payload']}")

    async def start_agents(self):
        for a in self.agents.values():
            await a.start()

    async def submit(self, text: str):
        import uuid
        cid = uuid.uuid4().hex
        await self.bus.publish("PlannerAgent", {
            "type": "user.request",
            "from": "cli",
            "to": "PlannerAgent",
            "correlation_id": cid,
            "payload": {"text": text},
        })
        self.logger.info(f"Request submitted: {text}")
        return cid

    async def shutdown(self):
        if self.agents.get("dispatcher"):
            await self.agents["dispatcher"].stop()
        if self.bus:
            await self.bus.close()


# ─────────────────────── mode runners ───────────────────────

async def run_centralized(cfg_path: str, request: str, wait: int = 30):
    orch = Orchestrator(cfg_path)
    await orch.initialize()
    await orch.start_agents()
    await orch.submit(request)
    await asyncio.sleep(wait)
    await orch.shutdown()


async def run_distributed(cfg_path: str, num_workers: int, request: str, wait: int = 30):
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    logger = setup_logger(name="taichi", level=cfg["logging"].get("level", "INFO"))
    redis_url = cfg["communication"]["redis_url"]

    manifest = cfg["skills"]["manifest_path"]
    if not Path(manifest).is_absolute():
        manifest = str(Path(cfg_path).parent / manifest)
    skill_registry = SkillRegistry(manifest)

    import redis.asyncio as redis
    r = await redis.from_url(redis_url)
    await r.delete("taichi:workers")
    await r.aclose()

    workers = []
    for i in range(num_workers):
        wid = f"dist-worker-{i}"
        w = DistributedWorker(wid, redis_url, skill_registry, cfg)
        workers.append(w)
        await w.start()

    await asyncio.sleep(1)

    tasks = [
        {
            "task_id": f"dist-task-{i}",
            "skill": "bash_executor",
            "params": {"command": f"echo 'Distributed worker {i}: {request}'"},
            "timeout": 30,
        }
        for i in range(num_workers)
    ]

    corr_id = f"dist-{asyncio.get_event_loop().time():.0f}"
    await workers[0].bus.broadcast(
        "task.broadcast",
        {"tasks": tasks, "skill": "bash_executor"},
        correlation_id=corr_id,
    )
    logger.info(f"Distributed: broadcast {num_workers} tasks, corr_id={corr_id}")
    await asyncio.sleep(wait)
    for w in workers:
        await w.stop()
    logger.info("Distributed run complete")


async def run_hybrid(cfg_path: str, worker_counts: dict, request: str, wait: int = 30):
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    logger = setup_logger(name="taichi", level=cfg["logging"].get("level", "INFO"))
    redis_url = cfg["communication"]["redis_url"]

    manifest = cfg["skills"]["manifest_path"]
    if not Path(manifest).is_absolute():
        manifest = str(Path(cfg_path).parent / manifest)
    skill_registry = SkillRegistry(manifest)

    import redis.asyncio as redis
    r = await redis.from_url(redis_url)
    await r.delete("taichi:workers")
    await r.aclose()

    # 启动所有组的 HybridWorker
    all_workers = {}
    for role, count in worker_counts.items():
        ids = []
        for i in range(count):
            wid = f"hybrid-{role}-{i}"
            w = HybridWorker(wid, redis_url, skill_registry, cfg)
            await w.start()
            ids.append(wid)
            all_workers[role] = ids
        logger.info(f"Hybrid: started {count} workers for role={role}")

    await asyncio.sleep(1)

    # 1. Planner Group
    planner_coord = GroupCoordinator(
        "planner_group", "planner", all_workers["planner"],
        redis_url, "voting_merge"
    )
    await planner_coord.connect()
    dag = await planner_coord.execute({"text": request})
    logger.info(f"Hybrid: Planner output: {len(dag.get('nodes', []))} nodes")

    # 2. Drafter Group
    drafter_coord = GroupCoordinator(
        "drafter_group", "drafter", all_workers["drafter"],
        redis_url, "shard_draft"
    )
    await drafter_coord.connect()
    draft = await drafter_coord.execute({"dag": dag})
    logger.info(f"Hybrid: Drafter output: {len(draft.get('tasks', []))} tasks")

    # 3. Validator Group
    validator_coord = GroupCoordinator(
        "validator_group", "validator", all_workers["validator"],
        redis_url, "cross_check"
    )
    await validator_coord.connect()
    validation = await validator_coord.execute({"draft": draft})
    logger.info(f"Hybrid: Validator output: {validation}")

    if validation.get("status") != "approved":
        logger.warning(f"Hybrid: validation failed: {validation}")
        return {"status": "validation_failed", "details": validation}

    # 4. Dispatcher Group
    dispatcher_coord = GroupCoordinator(
        "dispatcher_group", "dispatcher", all_workers["dispatcher"],
        redis_url, "consistent_hash"
    )
    await dispatcher_coord.connect()
    dispatch = await dispatcher_coord.execute({"tasks": draft.get("tasks", [])})
    logger.info(f"Hybrid: Dispatcher output: {dispatch}")

    # shutdown workers
    for role_ids in all_workers.values():
        for wid in role_ids:
            # workers aren't exposed directly; they run async
            pass

    return {
        "status": "completed",
        "dag": dag,
        "draft": draft,
        "validation": validation,
        "dispatch": dispatch,
    }


# ─────────────────────── CLI ───────────────────────

@click.command()
@click.option("--config", default="config.yaml", help="Config file path")
@click.option("--mode", default="centralized", help="centralized|distributed|hybrid")
@click.option("--workers", default="3", help="Worker count (or comma-separated for hybrid: p,d,v,dp)")
@click.option("--request", "-r", default=None, help="User request text")
def main(config, mode, workers, request):
    default_cfg = Path("configs/default.config.yaml")
    user_cfg = Path(config)
    if not user_cfg.exists() and default_cfg.exists():
        shutil.copy(default_cfg, user_cfg)

    if mode == "distributed":
        n = int(workers)
        asyncio.run(run_distributed(config, n, request or "distributed task"))
    elif mode == "hybrid":
        counts = [int(x.strip()) for x in workers.split(",")]
        wc = {
            "planner": counts[0],
            "drafter": counts[1] if len(counts) > 1 else 3,
            "validator": counts[2] if len(counts) > 2 else 3,
            "dispatcher": counts[3] if len(counts) > 3 else 2,
        }
        asyncio.run(run_hybrid(config, wc, request or "hybrid task"))
    else:
        asyncio.run(run_centralized(config, request or "test request"))


if __name__ == "__main__":
    main()
