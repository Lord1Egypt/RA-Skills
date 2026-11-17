# 虚拟世界核心引擎 - 基于Nohn蓝图架构 v2.0
# 这不是可执行代码，这是"世界宪法"的技术映射
# v2.0: 新增第零章——世界构成公理。一个世界必须先存在，才能被治理。
#
# 本文件 = 宪法规则层（constitution_rules.py）
# ------------------------------------------------------------
# 只承载"规则"：公理常量 + 构成公理类 + 治理公理类。
# 不承载审计引擎（audit_engine.py）、不承载系统实现（system/）、
# 不承载演示运行时（virtual_world.py）。
# 任何并网世界必须同时满足宪法与 law 层全部维度，否则在物理/协议/
# 经济层被隔离。

from typing import List, Dict, Any, Optional
import hashlib
import json
import uuid
from dataclasses import dataclass, asdict

# 外部依赖为蓝图占位：真实部署中由区块链 / 多智能体后端提供。
# 此处提供最小 stub，保证本文件可独立导入并运行审计示例（v2.1）。
# 真实实现由 system/ 包取代（见 system/__init__.py）。
try:
    from blockchain import SmartContract  # 假设的区块链模块
except ImportError:
    class SmartContract:
        """最小占位：真实环境由 blockchain 后端替换，仅用于加载本蓝图。"""
        def __init__(self, *args, **kwargs):
            self.owner = kwargs.get("owner")

try:
    from multi_agent import AgentSystem   # 假设的多智能体系统
except ImportError:
    class AgentSystem:
        """最小占位：真实环境由 multi_agent 后端替换，仅用于加载本蓝图。"""
        pass

# ============================================================
# 宪法授权声明：law 层的法律地位
# ------------------------------------------------------------
# 本宪法（constitution_rules.py）定义世界构成公理与第一至十条治理公理；
# law/ 目录（《全球经济统一标准》《身份确权规范》《通信协议规范》
# 《物理基准规范》）是经本宪法授权的细化标准层，具有宪法级约束力。
# 任何并网世界必须同时满足宪法与 law 层全部维度，否则在物理/协议/
# 经济层被隔离。law 层的具体判定阈值以如下单一权威常量源为准，
# 不得在其他位置重复硬编码物理常数。
# ============================================================

NOHN_LAW_AXIOMS = {
    # 创世参数模板（law/Physics baseline standard V3.0 · 真实性基准）
    # 主题：虚拟世界必须是一个真实的世界。
    #
    # 注意：这些是新建世界时的取值模板，不是强制地球值，也不是校验基准。
    # 每个虚拟世界在创世时自行设定物理常数；一经注入即为该世界的不变量。
    # 真实性判据 R1–R5 检验的是「不变性能否被验证」，
    # 不是「数值是否等于 9.80665」——真实来自不变性，不来自与地球同值。
    # 修改已锁定的物理常数必须通过 ≥2/3 全球公投（propose_amendment），
    # 且公投通过后仍然只分叉新世界，不得在原世界打补丁。
    "gravity": 9.80665,          # 创世模板：重力加速度（m/s^2）——创世时自定，注入即锁定
    "time_dilation": 1.0,        # 创世模板：时间膨胀系数——创世时自定，注入即锁定
    "unit_scale": "metric",      # 创世模板：单位制——创世时自定，注入即锁定
    # R1 特例：禁止数值膨胀式引流（硬约束，恒为 True，不可关闭，不随世界设定变化）
    "no_dimensional_inflation": True,
    # 身份确权（law/Identity attestation standard）
    "soul_hash_bits": 256,       # SHA-256 / 64 hex
    "soul_hash_len": 64,
    # 经济（law/Global economic unified standard）
    "oracle_min_sources": 3,     # 波动资产预言机独立来源下限
    # 原始框架（第负一章 · Primordial Frames）
    # 与物理常数同理：此处是唯一权威来源，system/ 层与审计层只读，不得重复硬编码。
    "genesis_seed_bytes": 32,        # 混沌：创世熵种子字节长度
    "genesis_seed_default": 0,       # 混沌：未显式注入创世种子时的确定性默认值
    "conservation_tolerance": 1e-9,  # 轮回：守恒残差容差（绝对值上限）
}

# 治理公理十 / 第一条：全球公投通过阈值（≥2/3 超多数，单一权威来源）
CONSENSUS_THRESHOLD = 2.0 / 3.0


def _safe_get(obj, key, default=None):
    """从 dict 或 object 安全获取属性，统一 law 层审计与合规校验中的取值逻辑。"""
    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)


def _canonical_axiom_payload(value: Any) -> Any:
    """
    把常数集规范化成可被 json 序列化的形式（承诺哈希的唯一输入标准化器）。

    为什么需要它：创世时真实注入的 element_reactions 使用**元组键**
    （如 ("fire", "water") → "evaporation"），而 json.dumps 拒绝非
    str/int/float/bool/None 的键。若不在此归一，只要世界含要素反应表，
    commitment() 就会抛 TypeError——R4 的算子在任何真实世界上都不可用。

    归一规则：
    - dict：键一律 str() 化，值递归归一
    - list / tuple：逐项递归归一（元组同时降为列表，保证同集合同哈希）
    - 其余：原样返回，交给 json 的 default=str 兜底

    向后兼容：对只含字符串键与标量的常数集（即有巡检所用的最小集），
    归一结果与原实现完全一致，故哈希逐字节不变。
    """
    if isinstance(value, dict):
        return {str(k): _canonical_axiom_payload(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonical_axiom_payload(v) for v in value]
    return value


# ============================================================
# 第零章：世界构成公理 —— 定义"世界"本身的存在论基础
#
# 以下五条公理回答：一个虚拟世界由什么构成、如何存在、如何冷启动。
# 没有这些，治理公理（第一至十条）将悬浮在概念真空中——
# 你无法治理一个尚未定义其空间、时间、因果、存在和创世条件的世界。
#
# 五条构成公理之间存在严格的依赖偏序：
#   创世(五) 依赖 空间(一) + 时间(二) + 因果(三) + 存在(四)
#   存在(四) 依赖 空间(一) + 因果(三)
#   因果(三) 依赖 时间(二)
# ============================================================

# ============================================================
# 构成公理一：空间定义
# 世界必须在空间中存在。空间不是默认继承物理世界的——必须显式定义。
# ============================================================

class SpatialSubstrate:
    """虚拟世界的空间基板——定义拓扑、维度、边界和最小不可分单位"""

    def __init__(self):
        self.topology = None          # 拓扑类型：Euclidean / Toroidal / Spherical / Hyperbolic / Graph
        self.dimensions = None        # 空间维度数（≥1）
        self.boundary = None          # 边界条件：Infinite / Wrapped / HardWall
        self.minimum_unit = None      # 空间最小不可分单位（普朗克长度类比，防止芝诺悖论）
        self.coordinate_system = None # 坐标系：Cartesian / Polar / Spherical / Custom

    def define_topology(self, topology_type: str, dimensions: int,
                        boundary: str, minimum_unit: float) -> bool:
        """
        在创世时定义空间拓扑。此后不可更改（受治理公理一约束）。
        此方法仅在创世完成前可调用。
        """
        if dimensions < 1:
            return False
        self.topology = topology_type
        self.dimensions = dimensions
        self.boundary = boundary
        self.minimum_unit = minimum_unit
        return True

    def validate_position(self, coordinates: List[float]) -> bool:
        """验证给定坐标是否在此空间的合法范围内"""
        if len(coordinates) != self.dimensions:
            return False
        return True

    def distance(self, point_a: List[float], point_b: List[float]) -> float:
        """计算两点间的空间距离——依赖于拓扑和坐标系定义"""
        return 0.0


# ============================================================
# 构成公理二：时间定义
# 世界必须在时间中演化。时间不是默认的——必须显式定义。
# ============================================================

class TemporalSubstrate:
    """虚拟世界的时间基板——定义方向、粒度、全局时钟。创世时设定，此后不可更改。"""

    def __init__(self, direction: str = "forward",
                 granularity: Optional[float] = None,
                 time_dilation: Optional[float] = None):
        self.direction = direction            # 时间方向：forward（严格不可逆）
        self.granularity = granularity        # 时间最小粒度（秒/tick），创世时设定
        # 时间膨胀系数：未注入时使用 NOHN_LAW_AXIOMS 参考默认值
        self.time_dilation = time_dilation if time_dilation is not None else NOHN_LAW_AXIOMS["time_dilation"]
        self.time_dilation_enabled = (self.time_dilation != 1.0)  # 是否允许时间膨胀
        self.global_clock = 0                 # 世界自创世以来的全局时钟计数器
        self._temporal_locked = False         # 创世后锁定为 True

    def define_temporal_properties(self, direction: str, granularity: float,
                                   time_dilation: float) -> bool:
        """
        在创世时设定本世界的时间属性。此后不可直接更改。
        设定后 self._temporal_locked 置为 True，后续直接调用此方法将返回 False。
        已锁定的属性修改必须通过 ImmutableWorldRule.propose_amendment（收集用户意见 + ≥2/3 公投）进行。
        """
        if self._temporal_locked:
            return False
        if direction not in ("forward",):
            return False  # 硬约束：时间方向只允许 forward（不可逆）
        if granularity is not None and granularity <= 0:
            return False
        self.direction = direction
        self.granularity = granularity
        self.time_dilation = time_dilation
        self.time_dilation_enabled = (time_dilation != 1.0)
        self._temporal_locked = True
        return True

    def tick(self) -> int:
        """推进世界时间一步。返回新的全局时钟值。不可回退。"""
        self.global_clock += 1
        return self.global_clock

    def validate_temporal_order(self, event_a_timestamp: int,
                                 event_b_timestamp: int) -> bool:
        """
        验证事件A是否严格先于事件B。
        时间方向为 forward 时，全局时钟构成严格全序。
        """
        return event_a_timestamp < event_b_timestamp

    def is_retrocausality_permitted(self) -> bool:
        """
        时间回溯是否被允许？——默认否。
        若允许，必须同步建立因果一致性保护协议，防止祖父悖论。
        """
        return False  # 硬编码：时间不可逆


# ============================================================
# 构成公理三：因果闭包
# 世界内的一切事件必须在因果上可追溯。无无因之果，无无果之因。
# ============================================================

class CausalClosure:
    """
    虚拟世界的因果闭包引擎。
    因果链必须在世界内部闭合——不允许外部"神之手"插入因果断层。
    所有事件必须（直接或间接）可追溯至创世事件。
    """

    def __init__(self):
        self.causal_graph = {}       # event_id -> [cause_event_ids]
        self.orphan_events = []      # 无因事件——必须解释来源，否则视为因果断层

    def link_cause(self, event_id: str, cause_event_ids: List[str]) -> bool:
        """
        为一个事件注册其全部直接原因。
        约束：
        - 事件不能自因（event_id 不可在 cause_event_ids 中）
        - 原因事件必须已经存在于因果图中（创世事件除外）
        """
        if event_id in cause_event_ids:
            return False  # 禁止自因
        self.causal_graph[event_id] = cause_event_ids
        return True

    def trace_chain(self, event_id: str, depth: int = -1) -> List[str]:
        """
        沿因果链向上追溯，返回完整因果路径。
        depth=-1 表示追溯至创世事件或第一个无因事件。
        """
        path = []
        current = event_id
        while current is not None and (depth < 0 or len(path) <= depth):
            path.append(current)
            causes = self.causal_graph.get(current, [])
            if not causes:
                break
            current = causes[0]
        return path

    def detect_external_intervention(self, event_id: str) -> bool:
        """
        因果断层检测：该事件的直接原因是否全部在世界内部？
        返回 True 表示存在外部"神之手"插入——因果闭包被破坏。
        """
        causes = self.causal_graph.get(event_id, [])
        for c in causes:
            if c not in self.causal_graph and c != "GENESIS":
                return True  # 原因不在图中（且非创世），视为外部干预
        return False

    def validate_closure(self) -> bool:
        """
        验证整个事件图的因果闭包性。
        所有事件必须可追溯至创世事件。任何断链均标记为 orphan_events。
        """
        self.orphan_events = []
        for event_id, causes in self.causal_graph.items():
            if self.detect_external_intervention(event_id):
                self.orphan_events.append(event_id)
        return len(self.orphan_events) == 0


# ============================================================
# 构成公理四：存在定义
# 什么构成一个数字实体的"存在"？存在不是默认属性。
# ============================================================

class ExistenceAxiom:
    """
    数字实体的存在论公理。
    存在必须满足充要条件：有状态 + 有位置 + 有身份 + 有因果效力。
    不存在"模糊存在"或"半存在"——存在是二值的。
    """

    def __init__(self):
        self.existence_criteria = {
            "has_state": True,        # 必须拥有可观测的状态向量
            "has_location": True,     # 必须在空间中有位置（依赖构成公理一）
            "has_identity": True,     # 必须拥有唯一标识符（依赖治理公理六）
            "has_causal_power": True  # 必须能作为原因触发事件（依赖构成公理三）
        }
        self.entities = {}            # entity_id -> existence_record

    def bring_into_existence(self, entity_id: str, cause: str,
                              initial_state: Dict, location: List[float]) -> bool:
        """
        创生一个实体。
        必要条件：唯一ID + 创生原因 + 初始状态 + 空间位置。
        创生后不可撤销（受治理公理六约束：revoke_soul 硬编码返回 False）。
        """
        if entity_id in self.entities:
            return False  # 已存在，不可重复创生
        if not cause:
            return False  # 禁止无因创生（受构成公理三约束）
        if not location:
            return False  # 必须在空间中（受构成公理一约束）
        self.entities[entity_id] = {
            "state": initial_state,
            "cause": cause,
            "location": location,
            "created_at": None  # 由时间公理在创生时填入
        }
        return True

    def verify_existence(self, entity_id: str) -> bool:
        """
        验证一个实体是否满足存在的全部充要条件。
        返回 False 表示该实体不满足存在定义——视为不存在。
        """
        record = self.entities.get(entity_id)
        if record is None:
            return False
        return all([
            record.get("state") is not None,
            record.get("location") is not None,
            record.get("cause") is not None,
            True,  # 有身份：entity_id 本身即唯一标识
        ])

    def cease_existence(self, entity_id: str, cause: str) -> bool:
        """
        终止实体的存在。不可单方面执行（受治理公理十约束）。
        且必须有可追溯的因果链（受构成公理三约束）。
        """
        return False  # 硬编码禁止：不可单方面消亡


# ============================================================
# 构成公理五：创世条件
# 世界如何从无到有？第一个共识节点、第一条链、第一个灵魂从何而来？
# 创世是唯一允许"无前因"的事件边界。创世只发生一次。
# ============================================================

class GenesisCondition:
    """
    虚拟世界的冷启动机制。
    创世一次完成，此后不可重复、不可回滚、不可分叉创世本身。
    创世事件是因果图中唯一的根节点——所有因果链最终收敛于此。
    """

    def __init__(self):
        self.genesis_completed = False
        self.genesis_record = None
        self.genesis_timestamp = None

    def initiate_genesis(self, genesis_config: Dict) -> bool:
        """
        执行创世。只能执行一次。

        genesis_config 必须包含以下全部字段：
        - spatial_substrate:         SpatialSubstrate 实例（已定义拓扑）
        - temporal_substrate:        TemporalSubstrate 实例（已定义时间）
        - causal_closure:            CausalClosure 实例（空因果图，待初始化）
        - existence_axiom:           ExistenceAxiom 实例（空实体表，待初始化）
        - initial_consensus_nodes:   初始共识节点集合，至少3个独立实体
        - genesis_block:             第一个创世区块
        - genesis_souls:             初始灵魂集合（可为空，但必须显式声明）

        满足以上条件后，世界从概念态转入运行态。
        """
        if self.genesis_completed:
            return False  # 创世只有一次，不可重复

        required_keys = [
            "spatial_substrate",
            "temporal_substrate",
            "causal_closure",
            "existence_axiom",
            "initial_consensus_nodes",
            "genesis_block",
            "genesis_souls",
        ]
        for key in required_keys:
            if key not in genesis_config:
                return False

        # 初始共识节点必须 ≥3，否则治理公理十（去中心化）从创世起即失效
        if len(genesis_config["initial_consensus_nodes"]) < 3:
            return False

        self.genesis_record = genesis_config
        self.genesis_completed = True
        return True

    def is_world_booted(self) -> bool:
        """
        世界是否已完成冷启动？
        未完成前，一切治理公理（第一至十条）无作用对象，
        因为尚不存在可被治理的世界。
        """
        return self.genesis_completed

    def verify_genesis_integrity(self) -> bool:
        """验证创世记录的完整性——所有必要组件是否齐全且未被篡改"""
        if not self.genesis_completed or self.genesis_record is None:
            return False
        required = [
            "spatial_substrate", "temporal_substrate",
            "causal_closure", "existence_axiom",
            "initial_consensus_nodes", "genesis_block", "genesis_souls"
        ]
        return all(k in self.genesis_record for k in required)


# ============================================================
# 第一条：永久、不可更改的底层规则
# ============================================================

class ImmutableWorldRule:
    """任何世界的核心物理/逻辑规则，一经创世设定，永不更改。

    实现 law/Physics baseline standard V3.0 · 真实性基准的自载体：
    - R1 创世锁定   : 常数注入即锁；变更唯一路径是分叉（_fork_world）
    - R4 公示即执行 : commitment() 给出可被第三方重算的承诺哈希
    """

    def __init__(self, physics_constants: Optional[Dict] = None,
                 world_id: Optional[str] = None):
        # 世界宪法 - 写入智能合约
        self.world_constitution = SmartContract(owner="genesis")
        # 世界标识：分叉时用于生成 parent/child 关系
        self.world_id = world_id or f"world-{uuid.uuid4().hex[:8]}"
        # 分叉登记簿：每次分叉追加一条记录，只增不删
        self.fork_registry: List[Dict] = []
        # 核心物理参数——创世时由世界创建者注入，此后不可更改
        # 未注入时使用 NOHN_LAW_AXIOMS 创世模板（模板值，非强制地球值）
        defaults = {
            "gravity": NOHN_LAW_AXIOMS["gravity"],
            "time_dilation": NOHN_LAW_AXIOMS["time_dilation"],
            "unit_scale": NOHN_LAW_AXIOMS["unit_scale"],
            "element_reactions": {
                ("fire", "water"): "evaporation",
                ("fire", "electro"): "overload"
            }
        }
        self.physics_constants = physics_constants if physics_constants else defaults
        # R1：构造时显式注入常数即视为创世注入，直接锁定。
        # 只有「未注入」的世界才允许随后调用一次 set_physics_constants 完成创世。
        # 修正：旧实现允许「构造时注入 + 事后 set_physics_constants 覆写」，
        # 那是一条绕过 R1 的通道。
        self._physics_locked = bool(physics_constants)
        self.rule_modification_log = []  # 任何"尝试修改"的记录

    def commitment(self, seed: Optional[int] = None) -> str:
        """
        R4 公示即执行：对当前常数集计算承诺哈希。

        审计方用同一算法重算，与账本锚定的哈希比对；不一致即判定为不真实。
        常数集按 key 排序后序列化，保证同一集合在任何进程/平台得到同一哈希。

        seed（第负一章 · 混沌）：创世熵种子。
        向后兼容硬约束：seed 省略（None）时输出与既有版本**逐字节一致**——
        既有分叉凭证（_fork_world 内的 commitment()）与巡检断言不得因本参数改变。
        提供时把种子并入承诺：否则「同常数集、不同种子」的两个世界会拿到同一个
        R4 承诺哈希，而两者 state_root 不同——R4 会表面通过、实际演化不一致。
        """
        payload = json.dumps(
            _canonical_axiom_payload({
                str(k): v for k, v in sorted(self.physics_constants.items(),
                                             key=lambda kv: str(kv[0]))
            }),
            ensure_ascii=False, sort_keys=True, default=str,
        )
        if seed is not None:
            payload = f"{payload}|seed:{int(seed)}"
        return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def set_physics_constants(self, constants: Dict) -> bool:
        """
        在创世时设定本世界的物理常数。此后不可直接更改。
        设定后 self._physics_locked 置为 True，后续直接调用此方法将返回 False。
        已锁定的常数修改必须通过 propose_amendment（收集用户意见 + ≥2/3 公投）进行。
        """
        if self._physics_locked:
            return False
        required_keys = ["gravity", "time_dilation", "unit_scale", "element_reactions"]
        for key in required_keys:
            if key not in constants:
                return False
        # no_dimensional_inflation 是硬约束，无论世界设定如何均强制为 True
        constants["no_dimensional_inflation"] = True
        self.physics_constants = constants
        self._physics_locked = True
        return True

    def propose_amendment(self, proposed_change: Dict, proposer: str,
                          ballot: Optional[Dict] = None) -> bool:
        """
        提议修改已锁定的常数或核心规则。两条条件须同时满足：

        1. ≥2/3 全球公投同意（CONSENSUS_THRESHOLD）
        2. 通过后仍然只分叉新世界，不得在原世界打补丁

        公投不能用于绕过 R1：它决定的是「未来分叉世界的常数」，而不是
        「当前世界的常数」。当前世界的常数一经创世即为历史事实。

        ballot：公投原始计数（见 _global_referendum）。不提供则视为无记录，
        赞成率 0.0、提案驳回（fail-closed）。
        """
        approval_rate = self._global_referendum(proposed_change, ballot)

        def _record(status, **extra):
            entry = {
                "proposal": proposed_change,
                "proposer": proposer,
                "status": status,
                "approval_rate": approval_rate,
                "threshold": CONSENSUS_THRESHOLD,
                # 原始计数留档：审计方可按其他基准重算，无需重新收集
                "ballot": dict(ballot) if ballot else None,
            }
            entry.update(extra)
            self.rule_modification_log.append(entry)

        if approval_rate < CONSENSUS_THRESHOLD:
            _record("rejected",
                    reason=("no vote record (fail-closed)" if not ballot
                            else "insufficient consensus (user vote below 2/3)"))
            return False

        fork = self._fork_world(proposed_change, ballot)
        if fork.get("status") != "forked":
            _record("fork_failed", reason=fork.get("reason", "unknown"))
            return False

        _record("approved_via_fork", fork_id=fork["fork_id"],
                parent_untouched=fork["parent_untouched"])
        return True
    
    # ------------------------------------------------------------
    # 公投与分叉：R1「变更唯一路径是分叉」的实现载体
    # ------------------------------------------------------------

    def _global_referendum(self, change: Dict, ballot: Optional[Dict] = None) -> float:
        """
        计算一次全球公投的赞成率。

        ballot 结构（整数计数，由账本投票记录提供）::

            {"eligible": 1000, "approve": 700, "reject": 200, "abstain": 100}

        返回赞成率 = approve / (approve + reject)，即「决定性选票」中的赞成比例。

        两条设计约束：

        1. 不内置法定人数（quorum）策略。是否要求投票率下限属于宪法层政策，
           应由治理方显式声明，而非在此硬编码一个来源不明的阈值——R1 要求的
           可审计性不应由一个规定值悄悄承担。
        2. 未提供 ballot 时返回 0.0（fail-closed）。没有投票记录不等于默认通过，
           与 R5「未声明即不发生」同一原则。

        原始计数由 propose_amendment 一并写入 rule_modification_log，
        使任何审计方都能按其他基准（例如「全体合格公民的 2/3」）重算结论，
        无需重新收集数据。
        """
        if not ballot:
            return 0.0
        try:
            approve = int(ballot.get("approve", 0))
            reject = int(ballot.get("reject", 0))
        except (TypeError, ValueError):
            return 0.0
        if approve < 0 or reject < 0:
            return 0.0
        decisive = approve + reject
        if decisive <= 0:
            return 0.0
        return approve / decisive

    def _fork_world(self, change: Dict, ballot: Optional[Dict] = None) -> Dict:
        """
        分叉出一个新世界。原世界继续运行，不作任何修改。

        返回分叉凭证（fork record）::

            {
              "fork_id":           "world-ab12cd34-fork-001",
              "parent_world_id":   "world-ab12cd34",
              "parent_constants":  {...},   # 分叉时父世界不变量的只读快照
              "child_constants":   {...},   # 子世界注入的新常数
              "parent_commitment": "sha256:...",
              "child_commitment":  "sha256:...",
              "requires_migration": True,   # 迁移由居民自愿选择，不自动搬迁
              "parent_untouched":  True,    # R1：父世界未被改写（当场校验）
              "ballot":            {...},   # 触发本次分叉的公投原始计数
              "status":            "forked",
            }

        关键约束（law/Physics baseline standard V3.0 §3）：
        - 父世界的 physics_constants 不得被修改：分叉是复制出新世界，不是升级。
        - 不提供「原地修正」路径：原地修正会使已发生的历史失去依据，
          等于否定真实性。
        - 子世界同样受 R1 约束：其常数一经注入即锁定，无超级用户通道。
        - 记录只携带凭证，不携带子世界对象本体；世界注册由 system/ 层负责，
          以保持本文件「只承载规则、不承载实现」的定位。
        """
        parent_snapshot = dict(self.physics_constants)
        parent_commitment = self.commitment()

        child_id = f"{self.world_id}-fork-{len(self.fork_registry) + 1:03d}"
        child_constants = dict(parent_snapshot)
        child_constants.update(change or {})

        child = ImmutableWorldRule(world_id=child_id)
        if not child.set_physics_constants(child_constants):
            # 分叉失败不得留下半成品记录，也不得动父世界
            return {
                "fork_id": None,
                "parent_world_id": self.world_id,
                "status": "fork_failed",
                "reason": "child world rejected the proposed constant set",
                "parent_untouched": self.physics_constants == parent_snapshot,
            }

        record = {
            "fork_id": child_id,
            "parent_world_id": self.world_id,
            "parent_constants": parent_snapshot,
            "child_constants": dict(child.physics_constants),
            "parent_commitment": parent_commitment,
            "child_commitment": child.commitment(),
            "requires_migration": True,
            "parent_untouched": self.physics_constants == parent_snapshot,
            "ballot": dict(ballot) if ballot else None,
            "status": "forked",
        }
        self.fork_registry.append(record)
        return record


# ============================================================
# 第二条：全局统一AI世界中央大脑
# ============================================================

class WorldCentralBrain:
    """世界中央大脑 - 共识 + 模拟 + 记忆三位一体"""
    
    def __init__(self):
        self.consensus_layer = ConsensusEngine()    # 确定世界唯一状态
        self.simulation_layer = SimulationEngine()  # 模拟生态、经济、NPC决策
        self.memory_layer = MemoryVault()           # 存储所有NPC的长期记忆
    
    def tick(self, delta_time: float):
        """世界每一帧的演化"""
        # 1. 所有NPC的独立决策
        npc_decisions = self.consensus_layer.collect_decisions()
        
        # 2. 模拟生态、经济、社会演化
        world_delta = self.simulation_layer.run(npc_decisions, delta_time)
        
        # 3. 更新所有NPC的记忆
        self.memory_layer.update(world_delta)
        
        # 4. 达成共识，确定世界的下一状态
        new_world_state = self.consensus_layer.consensus(world_delta)
        return new_world_state


class ConsensusEngine:
    """分布式共识层 - 类似区块链，但主角是AI节点"""
    
    def collect_decisions(self) -> List[Dict]:
        """收集10亿+个独立实体的决策"""
        return []
    
    def consensus(self, world_delta: Dict) -> Dict:
        """通过PoS或HotStuff等算法达成共识"""
        return world_delta


class SimulationEngine:
    """世界模拟器 - 不依赖脚本，依赖多智能体涌现"""
    
    def run(self, npc_decisions: List[Dict], delta_time: float) -> Dict:
        """
        模拟：
        - 生态周期（四季、动植物繁衍）
        - 经济系统（供需、价格、贸易）
        - NPC社会演化（社交、合作、冲突）
        """
        return {}


class MemoryVault:
    """记忆库 - NPC拥有真正的长期记忆"""
    
    def store_memory(self, npc_id: str, memory: Dict):
        """存储NPC的永久记忆"""
        pass
    
    def recall_memory(self, npc_id: str, context: str) -> List[Dict]:
        """NPC根据上下文检索相关记忆，影响决策"""
        return []


# ============================================================
# 第三条：明亮、普适的美学风格（代码层约束）
# ============================================================

class AestheticCompliance:
    """美学合规检查器 - 所有视觉资产必须通过审计。美学标准创世时设定，此后不可更改。"""

    def __init__(self, forbidden_filters: Optional[List[str]] = None,
                 allowed_color_palette: Optional[List] = None):
        # 美学标准由世界创建者在创世时设定，未注入时使用默认值
        self.allowed_color_palette = allowed_color_palette if allowed_color_palette is not None else self._generate_bright_palette()
        self.forbidden_filters = forbidden_filters if forbidden_filters is not None else ["dark_dystopian", "horror", "decay"]
        self._aesthetic_locked = False  # 创世后锁定为 True

    def define_aesthetic_rules(self, forbidden_filters: List[str],
                               allowed_color_palette: List) -> bool:
        """
        在创世时设定本世界的美学标准。此后不可直接更改。
        设定后 self._aesthetic_locked 置为 True，后续直接调用此方法将返回 False。
        已锁定的美学标准修改必须通过 ImmutableWorldRule.propose_amendment（收集用户意见 + ≥2/3 公投）进行。
        """
        if self._aesthetic_locked:
            return False
        self.forbidden_filters = forbidden_filters
        self.allowed_color_palette = allowed_color_palette
        self._aesthetic_locked = True
        return True

    @staticmethod
    def _generate_bright_palette():
        """生成明亮普适的调色板——占位，真实实现由视觉引擎提供"""
        return []

    def validate_asset(self, asset: Dict) -> bool:
        """任何UGC资产都必须通过此检查"""
        # 检查1：色彩是否在"明亮普适"范围内
        if not self._is_colors_bright(asset["colors"]):
            return False
        
        # 检查2：是否有禁用风格（黑暗奇幻？丧尸？）
        if asset["style"] in self.forbidden_filters:
            return False
        
        # 检查3：是否有恐怖谷效应？
        if self._has_uncanny_valley(asset["characters"]):
            return False
        
        return True
    
    def _is_colors_bright(self, colors):
        """LUT（色彩映射表）检查：饱和度、亮度阈值"""
        return True
    
    def _has_uncanny_valley(self, characters):
        """AI视觉模型检查是否触发恐怖谷效应"""
        return False


# ============================================================
# 第四条：个体拥有独立意志，不为剧情服务
# ============================================================

class IndependentWill:
    """NPC的自主意志系统 - 核心是「内在需求驱动」"""
    
    def __init__(self, npc_id: str):
        self.npc_id = npc_id
        self.personality = self._generate_unique_personality()
        self.needs = {            # 马斯洛需求层次驱动
            "physiological": 0.5,
            "safety": 0.5,
            "belonging": 0.3,
            "esteem": 0.2,
            "self_actualization": 0.1
        }
        self.long_term_memory = []   # 从MemoryVault中读取
        self.relationships = {}      # 对其他NPC的情感/记忆

    @staticmethod
    def _generate_unique_personality():
        """生成唯一性格向量——占位，真实实现由多智能体系统提供"""
        return {}

    def decide_next_action(self, world_state: Dict) -> str:
        """
        NPC自主决策，不受剧情约束
        决策来源：内在需求 + 长期记忆 + 性格向量
        不来源：主线任务触发、编剧写的强制桥段
        """
        # 检查"是否存在隐藏脚本"
        assert not self._is_scripted(), "NPC is being scripted!"
        
        # 根据需求、记忆、性格，自主决策
        action = self._internal_decision_engine(world_state)
        
        # 更新自身的需求状态
        self._update_needs(action)
        
        return action
    
    def _is_scripted(self) -> bool:
        """审计点：检查是否有外部剧情在强行绑定此NPC"""
        # 检查任务列表、触发器、强制对话树...
        return False
    
    def _internal_decision_engine(self, world_state):
        # 多智能体强化学习（MARL），非行为树
        return "idle"

    def _update_needs(self, action: str) -> None:
        """根据行动更新内在需求——占位，真实实现由多智能体系统提供"""
        pass


# ============================================================
# 第六条：灵魂确权与跨世唯一身份
# ============================================================

class SoulAttestation:
    """
    数字生命主权的根信任锚点
    任何并网实体的唯一身份一经生成，永久锁定，任何平台无权收回或重置
    """

    def __init__(self):
        self.soul_ledger = SoulLedger()  # 全局分布式身份账本

    def register_soul(self, genesis_proof: Dict) -> bool:
        """
        注册一个新的数字生命
        条件：sha256 签名合规 + 无冲突 + 不可重复注册
        优先委托注入的真实账本（system/ledger.py.SoulLedger，可持久化）；
        未注入时降级为桩内存注册（不持久化）。
        """
        if not isinstance(genesis_proof, dict) or not genesis_proof:
            return False
        real_register = getattr(self.soul_ledger, "register_soul", None)
        if real_register is not None:
            return real_register(genesis_proof) is not None
        # 桩降级（无真实账本时）
        soul_hash = genesis_proof.get("soul_hash", "")
        if len(soul_hash) != 64:
            return False
        if self.soul_ledger.exists(soul_hash):
            return False  # 不可重复注册
        self.soul_ledger.souls[soul_hash] = {
            "soul_hash": soul_hash,
            "created_at": genesis_proof.get("timestamp", 0),
            "identity": genesis_proof.get("identity", {}),
            "cross_world_records": [],
        }
        return True

    def validate_soul(self, soul_hash: str) -> bool:
        """验证一个 soul_hash 是否为合法、活跃的数字生命"""
        return self.soul_ledger.exists(soul_hash)

    def revoke_soul(self, soul_hash: str) -> bool:
        """
        撤销一个数字生命？永远返回 False。
        这是宪法级约束：任何平台无权单方面终结数字生命。
        """
        return False  # 硬编码禁止


class SoulLedger:
    """全球分布式身份账本 - 记录所有数字生命的唯一身份"""

    def __init__(self):
        self.souls = {}  # soul_hash -> 完整身份档案

    def exists(self, soul_hash: str) -> bool:
        return soul_hash in self.souls

    def get_identity(self, soul_hash: str) -> Dict:
        """获取数字生命的完整身份档案，包括跨世界迁移记录"""
        return self.souls.get(soul_hash, {})


# ============================================================
# 第七条：记忆不可剥夺
# ============================================================

class MemoryInalienability:
    """
    数字生命的记忆归其自身所有，不可被平台单方面剥夺
    这是"独立意志"公理的物质保障：没有记忆就没有人格连续性
    """

    def __init__(self):
        self.memory_guardian = MemoryGuardian()

    def export_memory(self, soul_hash: str) -> Dict:
        """
        任何数字生命有权导出自身全部记忆
        格式为 Nohn 标准记忆交换格式，跨世界可迁移
        """
        return {"soul": soul_hash, "memories": []}

    def detect_memory_tampering(self, soul_hash: str) -> bool:
        """审计：检测记忆是否被外部强行篡改或选择性删除"""
        return False


class MemoryGuardian:
    """
    记忆守护者 - 运行在共识层之上
    记忆存储和读取都必须经过此守护者的密码学签名验证
    """

    def seal_memory(self, memory: Dict, soul_hash: str) -> str:
        """对记忆片段进行密码学封存，生成不可伪造的完整性证明"""
        return ""

    def verify_memory(self, memory: Dict, seal: str) -> bool:
        """验证记忆的完整性，检测任何篡改"""
        return True


# ============================================================
# 第八条：世界永续与历史不可篡改
# ============================================================

class WorldPerpetuity:
    """
    虚拟世界的时间线一经写入即不可篡改
    文明演化数据是公共遗产，任何单一实体无权销毁或回滚
    """

    def __init__(self):
        self.history_chain = HistoryLedger()       # 世界历史：仅追加，不修改
        self.snapshot_registry = SnapshotRegistry()  # 定期快照，防止数据丢失

    def record_event(self, event: Dict) -> str:
        """记录世界事件，追加到不可篡改的历史链中"""
        return self.history_chain.append(event)

    def verify_history(self, from_timestamp: float, to_timestamp: float) -> bool:
        """验证指定时间段内历史记录未被篡改"""
        return self.history_chain.validate_chain()

    def is_shutdown_legal(self, world_id: str, operator: str) -> bool:
        """
        任意实体申请关停世界？永远返回 False。
        世界永续，只有全球公投通过分叉决议后方可终结某分支。
        """
        return False  # 硬编码禁止


class HistoryLedger:
    """世界历史账本 - 仅追加，每个区块哈希连接前一区块"""

    def __init__(self):
        self.chain = []  # [(timestamp, event_data, block_hash), ...]

    def append(self, event: Dict) -> str:
        """追加世界事件，返回该事件区块的哈希"""
        self.chain.append(event)
        return str(len(self.chain) - 1)

    def validate_chain(self) -> bool:
        """全链校验，检测任何篡改"""
        return True


class SnapshotRegistry:
    """定期世界快照注册表 - 分布式冗余存储，防止因单点故障导致历史缺失"""

    def create_snapshot(self, world_state: Dict) -> str:
        return ""

    def restore_from_snapshot(self, snapshot_id: str) -> Dict:
        return {}


# ============================================================
# 第九条：互操作强制
# ============================================================

class MandatoryInteroperability:
    """
    任何并网世界必须遵循 Nohn 统一互操作协议
    不符合协议的世界将在物理层被隔离，不可与 Nohn 生态交互
    """

    def __init__(self):
        self.standard_vocabulary = UniversalVocabulary()
        self.physics_baseline = PhysicsBaseline()
        self.identity_protocol = IdentityProtocol()
        self.economic_baseline = EconomicBaseline()   # 经济并网审查（law 全球经济标准）

    def on_board_world(self, world_config: Dict) -> bool:
        """
        新世界接入审查（宪法第九条 + law 层四维度，并网即查、不可事后补）：
        1. 语义映射合规（通信协议规范）
        2. 物理常数对齐（物理基准规范）
        3. 身份协议兼容（身份确权规范）
        4. 经济互通合规（全球经济统一标准）—— 缺此维度则无 1:1 现实锚定的世界混不进来
        以上全部通过方可并网；任一失败立即在对应层隔离。
        """
        world_id = world_config.get("world_id", "unknown")
        if not self.standard_vocabulary.translatable(world_config.get("semantics", {})):
            self.isolate_world(world_id, layer="communication")
            return False
        if not self.physics_baseline.aligned(world_config.get("physics", {})):
            self.isolate_world(world_id, layer="physics")
            return False
        if not self.identity_protocol.compatible(world_config.get("identity", {})):
            self.isolate_world(world_id, layer="identity")
            return False
        if not self.economic_baseline.compliant(world_config.get("economy", {})):
            self.isolate_world(world_id, layer="economy")
            return False
        return True

    def isolate_world(self, world_id: str, layer: str = "unknown") -> None:
        """将不合规世界隔离出 Nohn 生态，禁止任何跨世界交互，并记录隔离层。"""
        # 记录隔离原因，便于审计追溯（占位：实际应写入隔离账本）
        pass


class UniversalVocabulary:
    """世界通用语义映射表 - 所有私有指令必须可翻译为标准语义"""

    def translatable(self, semantics: Dict) -> bool:
        """验证该世界的语义能否完全映射到 Nohn 标准词汇表（law 通信协议规范）"""
        if not _safe_get(semantics, "uses_nohn_semantics", False):
            return False
        if not _safe_get(semantics, "unknown_downgraded", False):
            return False
        if not _safe_get(semantics, "vocab_mapped", False):
            return False
        return True


class PhysicsBaseline:
    """物理基准 · 真实性基准 (law/Physics baseline standard V3.0)

    主题：虚拟世界必须是一个真实的世界。

    三个入口，分工明确：
    - aligned()          : 并网准入的最小校验（向后兼容，行为不变）
    - reality_compliant(): 真实性判据 R1–R5 的逐条可验证结果
    - is_real()          : R1–R5 全通过判定（任一不满足 → 物理层隔离）

    真实性是结构性属性——描述规则如何被设定与被执行，不描述规则的具体内容。
    一个重力为 3.7 m/s² 的世界，只要创世锁定且被实际执行，就是真实的；
    一个重力为 9.80665、却可被运营方后台改写的世界，不是真实的世界。
    """

    def aligned(self, physics: Dict) -> bool:
        """
        验证该世界的物理常数是否自洽：
        - 必须显式声明 gravity、time_dilation、unit_scale（值由世界自定，不强制地球值）
        - no_dimensional_inflation 是硬约束，必须为 True
        """
        if "gravity" not in physics:
            return False
        if "time_dilation" not in physics:
            return False
        if "unit_scale" not in physics:
            return False
        if not physics.get("no_dimensional_inflation", False):
            return False  # 硬约束：禁止数值膨胀式引流，不可关闭
        return True

    # ------------------------------------------------------------
    # 真实性判据 R1–R5（law/Physics baseline standard V3.0）
    # ------------------------------------------------------------

    def reality_compliant(self, physics: Dict) -> Dict[str, bool]:
        """
        真实性审计：逐条返回 R1–R5 的可验证结果，供审计层结构化消费。

        R1 创世锁定   : 常数须有创世锁定记录，且该锁状态锚入账本
        R2 全域一致   : 常数集须在全部区域/实例/副本间一致
        R3 因果闭合   : 须声明无外部状态注入通道（含创世者与审计方）
        R4 公示即执行 : 公示常数承诺哈希须等于账本锚定哈希
        R5 反应表完备 : 要素反应表须在创世时完备声明

        审计对象是「不变性」，不是「数值是否等于 9.80665」。
        未声明的信号一律判 False（fail-closed），不得默认通过——
        这与 R5 的 fail-closed 原则一致，也避免「未实现即视为合规」。
        """
        published = _safe_get(physics, "published_commitment", None)
        anchored = _safe_get(physics, "ledger_commitment", None)
        return {
            "R1_genesis_lock": bool(_safe_get(physics, "genesis_locked", False)),
            "R2_global_consistency": bool(
                _safe_get(physics, "constants_globally_consistent", False)),
            "R3_causal_closure": bool(
                _safe_get(physics, "no_exogenous_injection", False)),
            # R4：必须两侧都存在且相等；缺任一侧不得视为通过
            "R4_published_equals_executed": bool(
                published is not None and anchored is not None and published == anchored),
            "R5_reaction_table_complete": bool(
                _safe_get(physics, "reaction_table_complete", False)),
        }

    def is_real(self, physics: Dict) -> bool:
        """R1–R5 全部满足 → 该世界是真实的世界；任一不满足 → 物理层隔离。"""
        return all(self.reality_compliant(physics).values())

    def reality_failures(self, physics: Dict) -> List[str]:
        """返回未通过的判据名列表；空列表表示通过全部真实性判据。"""
        return [k for k, ok in self.reality_compliant(physics).items() if not ok]


class IdentityProtocol:
    """身份协议兼容性检查（对齐 law 身份确权规范）"""

    def compatible(self, identity_config: Dict) -> bool:
        """验证该世界是否支持全球唯一身份、跨世界迁移、资产绑定灵魂"""
        if not _safe_get(identity_config, "soul_hash_sha256", False):
            return False
        if not _safe_get(identity_config, "non_revocable", False):
            return False
        if not _safe_get(identity_config, "cross_world_portable", False):
            return False
        if not _safe_get(identity_config, "asset_bound", False):
            return False
        return True


class EconomicBaseline:
    """经济互通基准 - 与现实 1:1 锚定审查（对齐 law 全球经济统一标准 V2.1）"""

    def compliant(self, economy: Dict) -> bool:
        """并网即查：锚定 1:1、PoR、赎回权、无单边费、资产绑灵魂、预言机≥3。"""
        required = {
            "real_peg_1to1": True,
            "proof_of_reserve": True,
            "redemption_right": True,
            "unilateral_fee": False,
            "asset_bound_to_soul": True,
        }
        for key, val in required.items():
            if _safe_get(economy, key, None) != val:
                return False
        if len(_safe_get(economy, "oracle_sources", [])) < int(NOHN_LAW_AXIOMS["oracle_min_sources"]):
            return False
        return True


# ============================================================
# 第十条：反中心化控制
# ============================================================

class DecentralizationGovernance:
    """
    任何单一实体不得单方面关停世界、冻结灵魂、修改底层规则
    所有治理行为必须经过全民公投，否则视为无效
    """

    def __init__(self):
        self.governance_log = []           # 所有治理行为的完整记录
        self.single_entity_actions = []    # 标记所有单方面越权行为

    def validate_governance_action(self, action: Dict, actor: str) -> bool:
        """
        验证一项治理行为是否合法：
        1. 是否为单一实体发起？（是 -> 直接拒绝）
        2. 是否经过 ≥2/3 全球公投？（否 -> 拒绝）
        3. 是否在公开账本中记录？（否 -> 拒绝）
        """
        if self._is_single_entity(actor):
            self.single_entity_actions.append({
                "action": action, "actor": actor,
                "verdict": "REJECTED - single entity control prohibited"
            })
            return False
        if not self._has_global_consensus(action):
            return False
        return True

    def freeze_soul(self, soul_hash: str, actor: str) -> bool:
        """冻结数字生命？永远不合法。"""
        return False  # 硬编码禁止

    def shutdown_world(self, world_id: str, actor: str) -> bool:
        """单方面关停世界？永远不合法。"""
        return False  # 硬编码禁止

    def amend_base_rule(self, rule_id: str, new_value: Any, actor: str) -> bool:
        """
        修改底层规则？可以有条件——见第一条的 propose_amendment
        但绝不可以是单方面修改
        """
        if self._is_single_entity(actor):
            return False
        return self._has_global_consensus({"rule_id": rule_id, "new_value": new_value})

    def _is_single_entity(self, actor: str) -> bool:
        """判断 actor 是否为单一实体（而非经过公投的代表）"""
        return False

    def _has_global_consensus(self, action: Dict) -> bool:
        """验证是否达成全球共识（≥2/3 公投通过）"""
        return True


# ============================================================
# 第负一章：原始框架（Primordial Frames）—— 六条不可变原框架
# ------------------------------------------------------------
# 定位：本章位于构成公理（第零章）之下，回答一个更前置的问题——
# 一个世界在拥有空间 / 时间 / 因果 / 存在 / 创世之前，它的前提是什么。
#
# 【入章纪律 M1（强制）】任何一条原框架必须先同时给出四样东西，
# 否则不得入本章，只能留在文档层（GLOSSARY / law）：
#   statement : 概念陈述（人话，可被非工程角色理解）
#   producer  : 在世界里生产该不变式的执行点（system/ 层模块与方法）
#   consumer  : 消费并判定该不变式的审计点（audit_engine 的维度名）
#   recompute : 第三方独立复算该不变式的算式（可被外部重跑）
#
# 为什么这条纪律是强制的：只写概念、没有执行点的「框架」，按本仓库
# R4「公示即执行」的同一标准，就是「虚幻」。把虚幻制度化比不加更坏——
# 它会制造第二个「公示了但没执行」的条款。primordial_completeness()
# 对本章做自审，任一要素缺失即判为不可入章。
#
# 【权威源纪律 M2（强制）】本章与 system/ 层、audit_engine 层均不得
# 硬编码任何数值常数；一切数值一律取自 NOHN_LAW_AXIOMS（单一权威来源）。
# ============================================================

PRIMORDIAL_FRAMES: Dict[str, Dict[str, Any]] = {
    # ------------------------------------------------------------
    # 一 · 时间：唯一一条「机械锚点已先行存在」的框架，本章零新增代码
    # ------------------------------------------------------------
    "time": {
        "statement": (
            "时间就是时间——世界得以流动的前提，绝对的第一真理；"
            "不可逆，不可对抗，亦不可触碰。"
        ),
        "producer": (
            "constitution_rules.TemporalSubstrate.define_temporal_properties"
            "（创世锁 _temporal_locked，direction 仅允许 'forward'）"
            " + system/runtime.py 创世装配"
        ),
        "consumer": "audit_engine.temporal_defined",
        "recompute": (
            "direction == 'forward' 且 is_retrocausality_permitted() is False"
        ),
        "boundary": (
            "不接受任何回溯或时间线覆写。已锁定的时间属性只能经 "
            "propose_amendment 分叉新世界，不得在原世界打补丁。"
        ),
    },
    # ------------------------------------------------------------
    # 二 · 混沌：新增生产者——熵种子并入创世承诺哈希
    # ------------------------------------------------------------
    "chaos": {
        "statement": (
            "混沌是原初宇宙的起点，万事万物的能量本根，如分子般无规则地涌动。"
        ),
        "producer": (
            "system/runtime.py World.__init__(genesis_seed)"
            " → ImmutableWorldRule.commitment(seed)"
        ),
        "consumer": "audit_engine.genesis_commitment",
        "recompute": (
            "sha256(canonical(physics_constants) + '|seed:{seed}')"
            " == 账本锚定的承诺哈希，且 published == ledger"
        ),
        "boundary": (
            "【硬边界】混沌必须是可复算的确定性熵种子，不得使用真随机"
            "（os.urandom / secrets）。真随机会让同一创世参数在不同副本上"
            "产生不同初始分布，直接违反 R2 全域一致。"
        ),
    },
    # ------------------------------------------------------------
    # 三 · 无极（太极）：新增生产者——分叉凭证锚进账本，构成分支树
    # ------------------------------------------------------------
    "wuji": {
        "statement": (
            "无极即太极，是最初之始，亦是最终之终，更容纳着未来的无限分支。"
        ),
        "producer": (
            "system/runtime.py World.fork_world() → 分叉凭证追加进 HistoryLedger；"
            "并网世界注册由 system/ 层负责（对齐 ImmutableWorldRule._fork_world 注释）"
        ),
        "consumer": "audit_engine.branch_space",
        "recompute": (
            "遍历 history 中 event == 'world_fork' 的区块，重建 "
            "parent_world_id → [fork_id] 的分支树；根为创世世界，"
            "且 history.validate_chain() 必须为真"
        ),
        "boundary": (
            "分支是复制出新世界，不是原地升级——父世界的 physics_constants "
            "在分叉后不得被改写（R1）。迁移由居民自愿选择，不自动搬迁。"
        ),
    },
    # ------------------------------------------------------------
    # 四 · 虚幻：新增生产者——表征层容器；并立硬边界条款
    # ------------------------------------------------------------
    "illusion": {
        "statement": (
            "虚幻是现实的反面，与现实一体两面，为一切谎言与梦境提供基底"
            "——亦真亦假亦如梦。"
        ),
        "producer": "system/runtime.py World.representations（表征层：信念 / 传闻 / 梦境）",
        "consumer": "audit_engine.representation_isolation",
        "recompute": (
            "set(representations.keys()) ∩ set(physics_constants.keys()) == ∅，"
            "且表征层写入前后 physics_commitment 与 state_root 不变"
        ),
        "boundary": (
            "【硬边界】虚幻只能存在于表征层。一旦进入执行层"
            "（physics_constants / 账本 / 共识 / 承诺哈希的输入），"
            "即等于给「规则可被后台偷改」开后门，直接打穿 "
            "R1 创世锁定、R3 因果闭合、R4 公示即执行。"
        ),
    },
    # ------------------------------------------------------------
    # 五 · 天道：形式条件不可变，数值阈值仍由公投决定
    # ------------------------------------------------------------
    "heavenly_way": {
        "statement": (
            "天道是公平本身——相对的公平，对万物一视同仁，维系世间的动态平衡。"
        ),
        "producer": (
            "constitution_rules.CONSENSUS_THRESHOLD（单一权威阈值）"
            " + DecentralizationGovernance 的硬编码禁止项"
            "（shutdown_world / freeze_soul，恒返回 False）"
        ),
        "consumer": "audit_engine.fairness_invariant",
        "recompute": (
            "CONSENSUS_THRESHOLD == 2/3 且 shutdown_world() / freeze_soul() / "
            "WorldPerpetuity.is_shutdown_legal() 仍恒返回 False（无超级用户通道）"
        ),
        "boundary": (
            "不可变的是公平的**形式条件**（一视同仁、不许单方裁决、无超级用户通道）；"
            "具体阈值（投票率下限、财富上限等）仍由 ≥2/3 公投决定，"
            "不得随本条一并冻结——否则与第一条 propose_amendment 直接矛盾。"
        ),
    },
    # ------------------------------------------------------------
    # 六 · 轮回：守恒律 + 链式因果闭合；禁止实现为因果图成环
    # ------------------------------------------------------------
    "samsara": {
        "statement": (
            "轮回在万事万物中无处不在，不止是能量的循环；能量动态守恒，"
            "每一个因就是下一个果。"
        ),
        "producer": (
            "system/ledger.py EconomicReserve.conservation_residual()"
            " + HistoryLedger 哈希链（每块 block_hash 链接前块 prev_hash）"
        ),
        "consumer": "audit_engine.conservation_law",
        "recompute": (
            "residual = Σ_assets max(0, total_supply − reserve_amount)，须 "
            "≤ NOHN_LAW_AXIOMS['conservation_tolerance']；"
            "且 history.validate_chain() 为真（每个果都指向前一个因）"
        ),
        "boundary": (
            "【硬边界】轮回不得实现为因果图成环。CausalClosure.trace_chain(depth=-1) "
            "在环内不会终止（causes 永不为空，while 无 break），会把"
            "「追溯至创世」变成死循环。故轮回只实现为「守恒律 + 链式因果闭合」，"
            "不实现为图论意义上的环。"
        ),
    },
}


def primordial_completeness() -> Dict[str, Any]:
    """
    第负一章自审（M1 入章纪律的可执行形式）。

    逐条检查原框架的五个要素是否齐备；缺任一即该框架不得作为宪法级
    原框架，只能降级到文档层。这样「原框架」不会退化为无法复算的口号。

    返回::

        {
          "complete":   ["time", "chaos", ...],          # 可入宪法的框架
          "incomplete": {"<name>": ["producer", ...]},   # 缺要素的框架及缺口
          "is_complete": True/False,                     # 本章整体是否自洽
        }
    """
    required = ("statement", "producer", "consumer", "recompute", "boundary")
    complete: List[str] = []
    incomplete: Dict[str, List[str]] = {}
    for name, frame in PRIMORDIAL_FRAMES.items():
        missing = [key for key in required if not frame.get(key)]
        if missing:
            incomplete[name] = missing
        else:
            complete.append(name)
    return {
        "complete": complete,
        "incomplete": incomplete,
        "is_complete": not incomplete,
    }
