"""FrameState 抽取：世界 tick → 渲染器的唯一输入。

确定性锚点说明（重要）
--------------------
`world.state_root()` 的 Merkle 输入含 `hlc`，而 HLC 的 pt 取自墙钟
（`system/hlc.py` 的 `peek()` → `_now_ms()`）。因此 state_root **跨运行不可能
逐字节一致，不能作为复现锚点**。

本模块另算 `content_digest`：只覆盖确定性字段（world_id / genesis_seed / tick /
排序后的 soul 位置与 needs / 事件三元组），同状态必得同摘要 —— 供 RenderManifest
与第三方复验使用。`state_root` 保留作跨节点旁证。
"""

import hashlib
import json
from typing import Dict, List, Optional
from pathlib import Path

from system.aoi_sync import DeltaSync


def _round_pos(pos) -> List[float]:
    return [round(float(v), 6) for v in pos]


def souls_view(world) -> Dict[str, Dict]:
    """当前 tick 的语义视图：soul → {position, needs, relationships}。

    只读世界状态，不写入；键序固定为 soul_hash 字典序，消除 dict 遍历序影响。
    """
    view: Dict[str, Dict] = {}
    for soul in sorted(world.npcs):
        agent = world.npcs[soul]
        view[soul] = {
            "position": _round_pos(world.positions.get(soul, [0.0, 0.0, 0.0])),
            "needs": {k: round(float(v), 6)
                      for k, v in sorted(getattr(agent, "needs", {}).items())},
            "relationships": {k: round(float(v), 6)
                              for k, v in sorted(getattr(agent, "relationships", {}).items())},
        }
    return view


def content_digest(world_id: str, genesis_seed: int, tick: int,
                   souls: Dict[str, Dict], events: List[Dict]) -> str:
    """确定性内容摘要：不覆盖 HLC / 墙钟 / 内存地址 / 进程随机量。"""
    material = {
        "world_id": world_id,
        "genesis_seed": genesis_seed,
        "tick": tick,
        "souls": souls,
        "events": [
            {
                "order_seq": e.get("order_seq"),
                "soul": e.get("soul"),
                "action": e.get("action"),
                "pos": _round_pos(e.get("pos", [0.0, 0.0, 0.0])),
                # 社交交互是世界的**事实**，必须进内容摘要 ——
                # 否则两个只在社交关系上不同的世界会得到同一个 digest，
                # 复现锚就漏掉了一整类真实差异。
                "interact": {
                    "partner": (e.get("interact") or {}).get("partner"),
                    "strength": round(float((e.get("interact") or {}).get("strength") or 0.0), 6),
                    "closeness": round(float((e.get("interact") or {}).get("closeness") or 0.0), 6),
                },
            }
            for e in events
        ],
    }
    blob = json.dumps(material, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def extract_tick_state(world, tick_num: int, events=None,
                       prev_souls: Optional[Dict[str, Dict]] = None) -> Dict:
    """抽取单 tick 的 FrameState（渲染器的唯一输入）。

    Args:
        world: system.runtime.World 实例
        tick_num: tick 序号
        events: 本 tick 由 World.tick() 返回的事件列表
        prev_souls: 上一 tick 的 souls 视图，用于计算语义增量；
                    为 None 时按「全部新增」处理
    """
    souls = souls_view(world)
    events = list(events or [])

    if prev_souls is None:
        delta = {"added": sorted(souls), "removed": [], "changed": [],
                 "bits": len(souls)}
    else:
        delta = DeltaSync.diff(souls, prev_souls)

    hlc: Dict = {}
    try:
        hlc = world.hlc.peek().to_dict()
    except Exception:
        hlc = {}

    return {
        "world_id": world.world_id,
        "genesis_seed": world.genesis_seed,
        "tick": tick_num,
        "hlc": hlc,                          # 非确定性：仅作旁证，不参与复现
        "state_root": world.state_root(),    # 含 HLC：跨节点验用，非复现锚
        "content_digest": content_digest(
            world.world_id, world.genesis_seed, tick_num, souls, events
        ),
        "souls": souls,
        "events": events,
        "delta": delta,
    }


def deterministic_soul_secret(genesis_seed: int, index: int) -> bytes:
    """由 genesis_seed 与序号派生固定的 32B 私钥字节。

    替代 `generate_user_keypair()`（其 Ed25519 随机源不可种子化）——
    同 (genesis_seed, index) 必得同 soul_hash，渲染复现的前提。
    """
    material = f"{genesis_seed}|agent-{index}".encode("utf-8")
    return hashlib.sha256(material).digest()


def derive_states(world_id: str, genesis_seed: int, data_dir: str,
                  agent_count: int, tick_from: int, tick_to: int) -> List[Dict]:
    """从创世重建 FrameState 序列（第三方复验原语）。

    与 extract 用同一条确定性路径，因此复验方无需信任生产方的产物，
    只需知道 (world_id, genesis_seed, agent_count, tick 区间)。
    """
    from system.runtime import World
    from system.keys import build_genesis_proof
    from system.ledger import derive_soul_hash

    world = World(world_id=world_id, data_dir=data_dir, genesis_seed=genesis_seed)
    for i in range(agent_count):
        secret = deterministic_soul_secret(genesis_seed, i)
        proof = build_genesis_proof(secret, {"genesis_id": f"agent-{i}"})
        soul = derive_soul_hash(proof)
        world.spawn_agent(soul_hash=soul, genesis_proof=proof)

    states: List[Dict] = []
    prev = None
    for tick_num in range(tick_from, tick_to + 1):
        result = world.tick()
        state = extract_tick_state(world, tick_num,
                                   events=result.get("events"), prev_souls=prev)
        states.append(state)
        prev = state["souls"]
    return states


def save_states(states: List[Dict], output_path: str):
    """保存 FrameState 序列到 JSONL。"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for state in states:
            f.write(json.dumps(state, ensure_ascii=False, sort_keys=True) + '\n')
    print(f"Saved {len(states)} states to {output_path}")


def load_states(input_path: str) -> List[Dict]:
    """从 JSONL 载入 FrameState 序列。"""
    states = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                states.append(json.loads(line))
    return states
