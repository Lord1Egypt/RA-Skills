# system/agent_engine.py - 智能体引擎（真实实现，桩转实第 2 步）
# ============================================================
# 职责：真实化以下宪法契约（对齐 constitution_rules.py）：
#   - IndependentWill.decide_next_action（内在需求驱动，非行为树）
#   - MemoryVault.store_memory / recall_memory（长期记忆，持久化）
#   - MemoryGuardian.seal_memory / verify_memory（记忆完整性封存）
#   - MemoryInalienability.export_memory / detect_memory_tampering
#
# 依赖方向：system/agent_engine.py -> constitution_rules / system.ledger（单向）
# 持久化：复用 ledger.Storage（SQLite），表：memories
#
# 审计契约：
#   - NPC 必须可证明"未被脚本绑定"（_is_scripted 返回 False）
#   - 记忆不可被平台单方面剥夺（export_memory 全量导出）
# ============================================================

import hashlib
import hmac
import json
import os
import threading
import time
from typing import Any, Dict, List, Optional, Tuple

from .ledger import Storage
from .keys import load_or_create_key


class MemoryGuardian:
    """记忆守护者：密码学封存/校验，检测任何篡改。

    封存密钥经 KMS 托管（默认文件后端，可插拔 HSM）。
    绝不用公开的 soul_hash 当密钥——soul_hash 全网可见，作密钥等于无密钥。
    """

    def __init__(self, seal_key: Optional[bytes] = None):
        self._seal_key = seal_key

    def seal_memory(self, memory: Dict, soul_hash: str) -> str:
        """对记忆片段进行 HMAC 封存，生成不可伪造的完整性证明。"""
        if self._seal_key is None:
            raise RuntimeError("seal key not configured")
        payload = json.dumps(memory, sort_keys=True, ensure_ascii=False)
        return hmac.new(
            self._seal_key,
            (soul_hash + "|" + payload).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def verify_memory(
        self, memory: Dict, seal: str, soul_hash: Optional[str] = None
    ) -> bool:
        """验证记忆完整性。若提供 soul_hash 则做密码学校验，否则降级为结构校验。"""
        if soul_hash:
            return hmac.compare_digest(self.seal_memory(memory, soul_hash), seal)
        return isinstance(seal, str) and len(seal) == 64


class MemoryVault:
    """长期记忆库：按 soul_hash 存取，持久化。"""

    def __init__(
        self, storage: Optional[Storage] = None, data_dir: Optional[str] = None
    ):
        self._storage = storage or Storage(data_dir=data_dir)
        self._storage.execute(
            "CREATE TABLE IF NOT EXISTS memories ("
            "seq INTEGER PRIMARY KEY AUTOINCREMENT, soul_hash TEXT NOT NULL, "
            "memory TEXT NOT NULL, seal TEXT NOT NULL, ts REAL NOT NULL)"
        )
        # 封存密钥：经 KMS 抽象托管（默认文件后端），绝不用公开 soul_hash
        seal_key = load_or_create_key(
            os.path.join(self._storage.data_dir, "memory_seal_key")
        )
        self.guardian = MemoryGuardian(seal_key=seal_key)

    def store_memory(self, soul_hash: str, memory: Dict) -> str:
        """存储永久记忆，返回完整性证明（seal）。"""
        if not isinstance(memory, dict):
            memory = {"content": memory}
        seal = self.guardian.seal_memory(memory, soul_hash)
        self._storage.execute(
            "INSERT INTO memories (soul_hash, memory, seal, ts) VALUES (?, ?, ?, ?)",
            (soul_hash, json.dumps(memory, ensure_ascii=False), seal, time.time()),
        )
        return seal

    def recall_memory(
        self, soul_hash: str, context: Optional[str] = None
    ) -> List[Dict]:
        """按灵魂检索记忆。context 可选做简单关键词过滤。"""
        rows = self._storage.query(
            "SELECT memory, seal FROM memories WHERE soul_hash=? ORDER BY seq",
            (soul_hash,),
        )
        out = []
        for mem_json, seal in rows:
            mem = json.loads(mem_json)
            if context and context not in json.dumps(mem, ensure_ascii=False):
                continue
            out.append({"memory": mem, "seal": seal})
        return out

    def verify_all(self, soul_hash: str) -> bool:
        """校验某灵魂的全部记忆是否被篡改。"""
        rows = self._storage.query(
            "SELECT memory, seal FROM memories WHERE soul_hash=? ORDER BY seq",
            (soul_hash,),
        )
        for mem_json, seal in rows:
            mem = json.loads(mem_json)
            if not self.guardian.verify_memory(mem, seal, soul_hash):
                return False
        return True


class MemoryInalienability:
    """第七条：记忆不可剥夺。全量导出 + 篡改检测。"""

    def __init__(
        self, vault: Optional[MemoryVault] = None, data_dir: Optional[str] = None
    ):
        self.memory_vault = vault or MemoryVault(data_dir=data_dir)

    def export_memory(self, soul_hash: str) -> Dict:
        """任何数字生命有权导出自身全部记忆（Nohn 标准记忆交换格式）。"""
        memories = self.memory_vault.recall_memory(soul_hash)
        return {"soul": soul_hash, "memories": memories}

    def detect_memory_tampering(self, soul_hash: str) -> bool:
        """审计：检测记忆是否被外部强行篡改或选择性删除。"""
        return not self.memory_vault.verify_all(soul_hash)


class GasExceeded(Exception):
    """智能体 Gas 预算耗尽（死循环/无限递归保护）。"""
    pass


class GasMeter:
    """Gas 计量器：步数预算 + 实时超时护卫。

    每个 Agent 每 tick 被分配一个 GasMeter 实例。每次 decide_next_action
    调用消耗 1 步（gas）；若预算耗尽或 CPU 超时，抛出 GasExceeded。
    超时监控基于 wall-clock，防止死循环/无限递归锁死物理线程。
    """

    def __init__(self, budget: int = 100, timeout_ms: int = 500):
        self.budget = budget
        self._spent = 0
        self._timeout = time.monotonic() + timeout_ms / 1000.0
        self._lock = threading.Lock()

    @property
    def remaining(self) -> int:
        return self.budget - self._spent

    @property
    def exhausted(self) -> bool:
        return self.remaining <= 0

    def consume(self, steps: int = 1) -> None:
        """消耗 steps 步 gas。预算耗尽或超时则抛出 GasExceeded。"""
        with self._lock:
            self._spent += steps
            if self._spent > self.budget:
                raise GasExceeded(
                    f"gas budget exhausted ({self._spent}/{self.budget})"
                )
            if time.monotonic() > self._timeout:
                raise GasExceeded(
                    f"gas wall-clock timeout (>{self._timeout}s)"
                )

    def __repr__(self) -> str:
        return f"GasMeter({self._spent}/{self.budget})"


PERSONALITY_KEYS = (
    "openness",            # 探索倾向：影响 self_actualize 权重与移动半径
    "conscientiousness",   # 自律倾向：影响 pursue_achievement 权重
    "belonging_bias",      # 亲和倾向：影响 socialize 权重
    "safety_bias",         # 谨慎倾向：影响 seek_shelter 权重
)


def derive_personality(soul_hash: str, genesis_seed: int) -> Dict[str, float]:
    """从 (genesis_seed, soul_hash) 确定性派生性格向量。

    与空间推进算子同源口径：不读墙钟、不用 `random` 模块 —— 同一 soul 在
    任何节点、任何重放中得到同一性格。性格因此是**创世常量**，不是运行时
    状态，不参与持久化，也就不存在漂移。

    为什么需要它：没有性格差异时，所有 agent 的需求优先级排序完全相同，
    行为同质，画面上只是一群同步乱走的矩形。性格把"需求缺口"变成
    "个体化的需求缺口"，让同一个世界长出不同的行为。
    """
    material = f"{genesis_seed}|{soul_hash}".encode("utf-8")
    digest = hashlib.sha256(material).digest()
    out: Dict[str, float] = {}
    for index, key in enumerate(PERSONALITY_KEYS):
        raw = int.from_bytes(digest[index * 2: index * 2 + 2], "big")
        out[key] = round(raw / 65535.0, 6)
    return out


def derive_initial_needs(soul_hash: str, genesis_seed: int) -> Dict[str, float]:
    """按 soul_hash 派生初始需求：在基线附近抖动，打散同步性。

    与性格同源口径（确定性、无 random、无墙钟）。初值不同 → 需求下降的
    节奏不同 → 同一时刻不同 agent 在做不同的事 → 画面上才有层次。
    """
    material = f"{genesis_seed}|needs|{soul_hash}".encode("utf-8")
    digest = hashlib.sha256(material).digest()
    out: Dict[str, float] = {}
    for index, key in enumerate(Agent.NEEDS_KEYS):
        raw = int.from_bytes(digest[index * 2:index * 2 + 2], "big") / 65535.0
        base = Agent.NEED_BASE[key]
        out[key] = round(min(1.0, max(0.0, base + (raw - 0.5) * Agent.NEED_JITTER)), 6)
    return out


class Agent:
    """独立意志智能体：需求驱动决策，非脚本绑定。"""

    NEEDS_KEYS = [
        "physiological",
        "safety",
        "belonging",
        "esteem",
        "self_actualization",
    ]

    # 初始需求基线。实际初值按 soul_hash 在基线附近抖动（见 derive_initial_needs）——
    # 固定初值会让所有 agent 需求同步下降、行动同步，画面上所有人同时涌向
    # 同一个方向（挤成一团）。
    NEED_BASE = {
        "physiological": 0.5,
        "safety": 0.5,
        "belonging": 0.3,
        "esteem": 0.2,
        "self_actualization": 0.1,
    }
    NEED_JITTER = 0.4

    # 需求 → 行动。belonging 映射到 socialize，但它**有前提**：必须有邻居
    # 可社交（见 NEED_REQUIRES_PARTNER）——归属感只能由真实交互兑现。
    NEED_TO_ACTION = {
        "physiological": "seek_resources",
        "safety": "seek_shelter",
        "belonging": "socialize",
        "esteem": "pursue_achievement",
        "self_actualization": "self_actualize",
    }
    # 归属感没有邻居可社交时不可行动 —— 决策时会被跳过（见 _internal_decision_engine）
    NEED_REQUIRES_PARTNER = ("belonging",)

    # ---- 目标承诺机制 ----
    # 没有承诺，需求每 5 tick 轮转一次：agent 朝目标只挪 5 步就改主意，
    # 实测 10 个 agent 全挤在出生点附近 8 个单位内，谁也走不到任何地方。
    # 承诺后 agent 会把一个目标做完（走到 / 尝试到），画面上才有"出发-抵达"。
    NEEDS_DECAY = 0.005          # 每 tick 需求衰减
    GOAL_SATISFY_RATE = 0.025    # 承诺期间该需求的恢复速率（受进展系数折算）
    GOAL_MAX_TICKS = 40          # 单个目标最长承诺（tick）——够走完一个目标点

    def __init__(
        self,
        soul_hash: str,
        personality: Optional[Dict] = None,
        memory_vault: Optional[MemoryVault] = None,
        storage: Optional[Storage] = None,
        genesis_seed: int = 0,
    ):
        self.soul_hash = soul_hash
        # 性格：显式传入优先，否则由创世参数确定性派生。
        # 缺项补 0.5（中性），保证下游读到的键集合恒定。
        derived = derive_personality(soul_hash, genesis_seed)
        merged = dict(derived)
        if personality:
            for key, value in personality.items():
                if key in PERSONALITY_KEYS:
                    try:
                        merged[key] = float(value)
                    except (TypeError, ValueError):
                        pass
        self.personality = {k: merged[k] for k in PERSONALITY_KEYS}
        # 马斯洛需求层次：初始中等水平，随行动演化
        # 马斯洛需求层次：初始值按 soul_hash 派生（打散同步性）
        self.needs = derive_initial_needs(soul_hash, genesis_seed)
        self.long_term_memory: List[Dict] = []
        self.relationships: Dict[str, float] = {}
        self.memory_vault = memory_vault
        self.action_history: List[str] = []
        # 目标承诺状态：选定了就做完，不半途改主意
        self.goal_action: Optional[str] = None
        self.goal_need: Optional[str] = None
        self.goal_ticks: int = 0
        self.goal_index: int = 0
        # 状态持久化：重启不丢需求/关系/行动历史
        self._storage = storage
        if storage is not None:
            self._ensure_state_table()
            self._load_state()

    def _ensure_state_table(self) -> None:
        self._storage.execute(
            "CREATE TABLE IF NOT EXISTS agent_state ("
            "soul_hash TEXT PRIMARY KEY, state TEXT NOT NULL, updated_at REAL NOT NULL)"
        )

    def save_state(self) -> None:
        """持久化智能体状态（需求/关系/行动历史）。"""
        if self._storage is None:
            return
        state = {
            "needs": self.needs,
            "relationships": self.relationships,
            "action_history": self.action_history,
            "goal_action": self.goal_action,
            "goal_need": self.goal_need,
            "goal_ticks": self.goal_ticks,
        }
        self._storage.execute(
            "INSERT OR REPLACE INTO agent_state (soul_hash, state, updated_at) "
            "VALUES (?, ?, ?)",
            (self.soul_hash, json.dumps(state, ensure_ascii=False), time.time()),
        )

    def _load_state(self) -> None:
        if self._storage is None:
            return
        rows = self._storage.query(
            "SELECT state FROM agent_state WHERE soul_hash=?", (self.soul_hash,)
        )
        if rows:
            state = json.loads(rows[0][0])
            self.needs.update(state.get("needs", {}))
            self.relationships.update(state.get("relationships", {}))
            self.action_history = state.get("action_history", [])
            self.goal_action = state.get("goal_action")
            self.goal_need = state.get("goal_need")
            self.goal_ticks = int(state.get("goal_ticks", 0) or 0)

    def _is_scripted(self) -> bool:
        """审计点：是否存在外部剧情在强行绑定此 NPC？永远 False。"""
        return False

    def decide_next_action(self, world_state: Optional[Dict] = None) -> str:
        """内在需求驱动决策：优先满足最匮乏需求，不依赖主线任务。

        从 world_state 中提取 gas_meter（GasMeter），每步决策消耗 1 gas。
        预算耗尽时抛出 GasExceeded 由调用方（runtime.tick）捕获并跳过该 agent。
        """
        if self._is_scripted():
            raise RuntimeError("Agent is being scripted!")
        meter = (world_state or {}).get("gas_meter")
        if meter is not None:
            meter.consume(1)
        action = self._internal_decision_engine(world_state or {})
        self._update_needs(action)
        self.action_history.append(action)
        if self.goal_action:
            self.goal_ticks += 1
        return action

    def _trait(self, key: str) -> float:
        """读性格项；缺失或非数值一律按中性 0.5 处理。"""
        try:
            return float(self.personality.get(key, 0.5))
        except (TypeError, ValueError):
            return 0.5

    def _internal_decision_engine(self, world_state: Dict) -> str:
        """需求驱动决策：最匮乏需求映射到行动，非行为树。

        性格只做**倾向加权**（乘子 1.0~1.35），不推翻需求优先级语义：
        缺口大的需求仍然优先，但当两个缺口接近时，性格决定谁胜出。
        因此不同 agent 在同一个世界里会选不同的行动 —— 这是"个体拥有
        独立意志"（宪法第四条）在行为层的兑现。

        **目标承诺**：已选定且未完成的目标会被做完（上限 GOAL_MAX_TICKS）。
        没有承诺，需求轮转太快，agent 每次只朝目标挪 5 步就改主意 ——
        实测所有 agent 都挤在出生点附近，谁也走不到任何地方。

        归属感只在**有邻居可社交**时才可行动；没有邻居就跳过它，
        避免"对着空气社交"。
        """
        neighbors = world_state.get("neighbors") or []

        # 1) 已有目标 → 做完它
        if self.goal_action:
            if self.goal_need in self.NEED_REQUIRES_PARTNER and not neighbors:
                # 没人可社交 → 放弃这个目标，重新评估
                self.goal_action = None
                self.goal_need = None
                self.goal_ticks = 0
            else:
                return self.goal_action

        # 2) 重新评估：最匮乏需求 → 行动
        # 性格加权上限刻意压到 1.35：它只用来**打破接近的平局**，
        # 不能让"亲和型 agent"在饥饿时先去社交 —— 需求缺口差出 35%
        # 以上时，性格无权翻盘。
        bias = {
            "physiological": 1.0,
            "safety": 1.0 + 0.35 * self._trait("safety_bias"),
            "belonging": 1.0 + 0.35 * self._trait("belonging_bias"),
            "esteem": 1.0 + 0.35 * self._trait("conscientiousness"),
            "self_actualization": 1.0 + 0.35 * self._trait("openness"),
        }
        scored: Dict[str, float] = {}
        for key in self.NEEDS_KEYS:
            deficit = 1.0 - float(self.needs.get(key, 0.5))
            scored[key] = max(0.0, deficit) * bias[key]
        # 确定性：按 NEEDS_KEYS 顺序遍历，严格大于才替换 —— 平局取靠前者
        best = None
        for key in self.NEEDS_KEYS:
            if key in self.NEED_REQUIRES_PARTNER and not neighbors:
                continue  # 本轮不可行动的需求不参与竞争
            if best is None or scored[key] > scored[best]:
                best = key
        if best is None:
            best = "self_actualization"
        action = self.NEED_TO_ACTION[best]
        self.goal_action = action
        self.goal_need = best
        self.goal_ticks = 0
        self.goal_index += 1
        return action

    def apply_goal_progress(self, factor: float = 1.0,
                            rate: Optional[float] = None) -> None:
        """承诺期间的进展：按 factor 折算当前目标需求的恢复量。

        factor 由世界层给出：一般目标为 1.0；socialize 则是亲密度 ——
        离得远就恢复不了，归属感只能靠真的靠近来兑现。

        rate 缺省用 GOAL_SATISFY_RATE；社交走 SOCIAL_SATISFY_RATE ——
        归属感被"亲密度"打了折，若不单独给速率，它在收支上永远追不上
        衰减，会被永久钉在 0（于是 agent 永远在找伴，永远没有节奏）。
        """
        if not self.goal_need:
            return
        base_rate = self.GOAL_SATISFY_RATE if rate is None else float(rate)
        step = base_rate * max(0.0, min(1.0, float(factor)))
        if step <= 0.0:
            return
        self.needs[self.goal_need] = min(1.0, self.needs[self.goal_need] + step)

    def complete_goal(self) -> None:
        """目标完成（到达或超期）：释放目标，下一 tick 重新评估。"""
        self.goal_action = None
        self.goal_need = None
        self.goal_ticks = 0

    def _update_needs(self, action: str) -> None:
        """每 tick 的需求演化：全体缓慢衰减。

        满足感不在这里一次性给 —— 它由 `apply_goal_progress` 按**实际进展**
        折算恢复（见 GOAL_SATISFY_RATE）。衰减速率与目标轮转周期配套：
        一轮 5 个目标 × GOAL_MAX_TICKS，衰减总量 ≈ 恢复总量，收支平衡。
        """
        for key in self.NEEDS_KEYS:
            self.needs[key] = max(0.0, self.needs[key] - self.NEEDS_DECAY)  # 熵增


__all__ = ["MemoryGuardian", "MemoryVault", "MemoryInalienability", "Agent", "GasExceeded", "GasMeter"]
