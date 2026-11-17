# system/runtime.py - 无头运行时（真实实现，桩转实第 3 步）
# ============================================================
# 职责：将 virtual_world.py 的演示逻辑服务化、可部署化：
#   - 创世装配：组装空间/时间/因果/存在 + 共识节点 + 账本 + 记忆，
#     真实调用 GenesisCondition.initiate_genesis，世界从概念态转运行态。
#   - tick 主循环（对齐 TemporalSubstrate.global_clock）
#   - 事件传导（因果链记录 + 历史哈希链追加）
#   - 世界快照 + 持久化（进程重启不丢状态）
#   - 周期性上报 audit_engine.SecondPerspectiveAuditor 25 项审计
#
# 目标形态：无 GUI 依赖、可横向扩展、可作为企业服务底座。
#
# 依赖方向：system/runtime.py -> constitution_rules / audit_engine / system.*（单向）
# ============================================================

import base64
import hashlib
import json
import logging
import math
import os
import threading
import time
from typing import Any, Dict, List, Optional, Tuple

from constitution_rules import (
    NOHN_LAW_AXIOMS,
    SpatialSubstrate,
    TemporalSubstrate,
    CausalClosure,
    ExistenceAxiom,
    GenesisCondition,
    ImmutableWorldRule,
    WorldCentralBrain,
    AestheticCompliance,
    SoulAttestation,
    WorldPerpetuity,
    MandatoryInteroperability,
)
from audit_engine import SecondPerspectiveAuditor, AuditReport

from .ledger import (
    Storage,
    SoulLedger,
    HistoryLedger,
    EconomicReserve,
    SnapshotRegistry,
    derive_soul_hash,
    is_hex64,
    merkle_root,
)
from .keys import verify_genesis_proof, FileKmsProvider, CloudKmsProvider
from .consensus import ConsensusNetwork, Governance, TcpTransport
from .agent_engine import MemoryVault, MemoryInalienability, Agent, GasMeter, GasExceeded
from .credentials import CredentialVault
from .session import (
    SessionManager,
    SqliteSessionStore,
    MemorySessionStore,
    RedisSessionStore,
)
from .authorization import AuthorizationEngine
from .recovery import RecoveryManager
from .hlc import HybridLogicalClock, HlcTimestamp
from .spatial_sharding import ShardManager, HandoverProtocol
from .aoi_sync import AoiTracker, SyncScheduler, DeltaSync
from .partition_guard import PartitionGuard
from .hierarchical_consensus import InterDcConsensus, IntraDcConsensus
from .cluster import ClusterConfig, HeartbeatLoop, TransportDispatcher
from .edge_sdk import EdgeSdk
from .account_abstraction import AccountAbstractionEngine
from .key_rotation import KeyRotationManager
from .soul_roaming import SoulRoamingProtocol
from .identity_root import IdentityRoot
from .keys import public_from_private

logger = logging.getLogger(__name__)


# 存储后端白名单：同一份代码，三套后端。
#   sqlite   默认：账本落盘 SQLite，会话同库
#   memory   测试/无状态演示：账本进程内 :memory:，会话内存 dict
#   redis    生产：账本本地 SQLite + 会话外置 Redis（需 redis-py，缺省降级）
#   postgres 生产：账本走 PostgreSQL（需 psycopg2，DSN 由 DATABASE_URL 或 pg_dsn 参数传入）
_STORAGE_BACKENDS = ("sqlite", "memory", "redis", "postgres")

# 集群模式下的出站超时与重试。心跳探测必须快速失败：Windows 上目标端口
# 无监听时连接会挂到超时而非立即 RST，5s × 1 次重试足以让一轮心跳卡 10s，
# 故障检测因此完全失效。单机模式保持原默认（5s / 1 次重试）。
_CLUSTER_SEND_TIMEOUT = 0.5
_CLUSTER_SEND_RETRIES = 0


def _split_endpoint(cluster: Optional[ClusterConfig]):
    """把 "host:port" 拆成 (host, port)。非法或未声明时返回默认（127.0.0.1, 0）。

    仅支持 IPv4 / 主机名 + 端口形态；IPv6 字面量不在静态清单支持范围内。
    """
    default = ("127.0.0.1", 0)
    if cluster is None or not cluster.node_endpoint:
        return default
    host, _, port_str = cluster.node_endpoint.rpartition(":")
    if not host:
        return default
    try:
        return (host, int(port_str))
    except ValueError:
        logger.error("invalid node_endpoint=%s, fallback to random port",
                     cluster.node_endpoint)
        return (host, 0)


def _endpoint_host(cluster: Optional[ClusterConfig]) -> str:
    return _split_endpoint(cluster)[0]


def _endpoint_port(cluster: Optional[ClusterConfig]) -> int:
    return _split_endpoint(cluster)[1]


def _resolve_storage_backend() -> str:
    """从环境变量 STORAGE 读取后端类型，非法值回落 sqlite。"""
    backend = os.environ.get("STORAGE", "sqlite").strip().lower()
    return backend if backend in _STORAGE_BACKENDS else "sqlite"


def _build_redis_session_store():
    """构造 Redis 会话存储；redis-py 缺失或连接失败时返回 None（调用方降级）。"""
    try:
        import redis
    except ImportError:
        print("[runtime] STORAGE=redis 但未安装 redis-py（pip install redis），会话降级 SQLite")
        return None
    try:
        client = redis.Redis.from_url(
            os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        )
    except Exception as e:  # pragma: no cover - 连接失败降级
        print(f"[runtime] Redis 连接失败（{e}），会话降级 SQLite")
        return None
    return RedisSessionStore(client)


class World:
    """运行态世界：创世装配后的可审计实例，供第二视角审计消费。"""

    def __init__(
        self,
        world_id: str,
        data_dir: Optional[str] = None,
        initial_oracles: Optional[List[str]] = None,
        cluster: Optional[ClusterConfig] = None,
        genesis_seed: Optional[int] = None,
    ):
        # cluster=None → 单机形态：不监听、不探测、不广播，行为与接线前一致
        self.cluster = cluster
        self.local_dc = cluster.local_dc if cluster is not None else "dc_local"
        self.world_id = world_id
        # 第负一章 · 混沌：创世熵种子。
        # 未显式注入时取 NOHN_LAW_AXIOMS 的确定性默认值——不得使用真随机，
        # 否则同一创世参数在不同副本上得到不同初始分布，违反 R2 全域一致。
        self.genesis_seed = (
            int(genesis_seed) if genesis_seed is not None
            else int(NOHN_LAW_AXIOMS["genesis_seed_default"])
        )
        # 第负一章 · 虚幻：表征层容器（信念 / 传闻 / 梦境）。
        # 硬边界：本容器只承载「与现实不一致的表征」，永不进入执行层
        # （physics_constants / 账本 / 共识 / 承诺哈希输入）。见 representation_isolation 审计。
        self.representations: Dict[str, List[Dict]] = {}
        # 节点身份（确定性全序的 tie-break 键）+ HLC 全局时钟
        self.node_id = world_id
        self.hlc = HybridLogicalClock(node_id=self.node_id)
        # HLC 并发保护：tick 主线程与后台集群线程共用同一个时钟实例
        self._hlc_lock = threading.Lock()
        # 空间索引（地基 A）：cell_key -> set(soul_hash)；positions: soul_hash -> [x, y, z]
        self.spatial: Dict[str, set] = {}
        self.positions: Dict[str, List[float]] = {}
        self._event_seq = 0
        # 确定性排序缓存（#3 优化）：避免每 tick 反复 sorted(self.npcs)
        self._npcs_sorted_cache: Optional[List[str]] = None
        # Gas 计量（地基 B）：每 tick 全局预算，按 agent 数均分
        self.tick_budget = 1000        # 每 tick 全局步数上限
        self.tick_timeout_ms = 500     # 单 agent 超时 500ms
        # 地平线二：跨数据中心模块实例化
        self.shard_manager = ShardManager(local_dc=self.local_dc)
        self.shard_manager.init_default_shards()
        self.aoi_tracker = AoiTracker()
        self.aoi_sync = SyncScheduler()
        self.partition_guard = PartitionGuard(node_id=self.node_id)
        # 跨 DC 复制面：远端节点 -> 上次推送给它的状态快照（用于下一轮差分）
        self._remote_aoi_state: Dict[str, Dict] = {}
        # 入站迁移记录（可审计：跨域 handover 是谁、从哪来、何时）
        self._received_handovers: List[Dict] = []
        # HLC 因果合流计数：每收到一条带时间戳的入站消息 +1。
        # 不能用 hlc.state()["ll"] 判断合流——随后的 send() 会把 ll 清零。
        self._hlc_merges = 0
        # 入站分发白名单 + 后台心跳线程（cluster=None 时两者都不启用）
        self._dispatcher = TransportDispatcher()
        self.heartbeat_loop: Optional[HeartbeatLoop] = None
        # Intra-DC 快环先建，Inter-DC 慢环构注入同一个实例（避免双实例孤立）
        self.intra_consensus = IntraDcConsensus()
        self.interdc_consensus = InterDcConsensus(
            local_dc_consensus=self.intra_consensus
        )
        # 存储后端：STORAGE 环境变量（sqlite/memory/redis/postgres），默认 sqlite
        self.storage_backend = _resolve_storage_backend()
        if self.storage_backend == "postgres":
            self.storage = Storage(data_dir=data_dir, backend="postgres")
        else:
            ledger_backend = (
                self.storage_backend if self.storage_backend in ("sqlite", "memory") else "sqlite"
            )
            self.storage = Storage(data_dir=data_dir, backend=ledger_backend)
        # 并发保护：ThreadingHTTPServer 多线程下 tick/spawn 串行化，防状态竞态
        self._lock = threading.Lock()

        # ---- 账户系统六层架构（第1~4层服务组件）----
        # 第1层：多设备凭证（服务端只存公钥）
        self.credentials = CredentialVault(storage=self.storage)
        # 第4层恢复，依赖凭证库查询绑定状态
        self.recovery = RecoveryManager(
            storage=self.storage,
            credential_vault=self.credentials,
        )
        # 恢复警报回调：发起恢复时记录到内存警报队列，供关联设备轮询/推送
        # （恢复发起瞬间通知所有守护者 + 关联设备，时间锁内可撤销）
        self._recovery_alerts: list = []

        def _on_recovery_alert(request_id, soul_hash, guardians, timelock_until):
            self._recovery_alerts.append({
                "request_id": request_id,
                "soul_hash": soul_hash,
                "guardians": guardians,
                "timelock_until": timelock_until,
                "alerted_at": time.time(),
            })
            logger.info(
                "recovery alert recorded request_id=%s soul_hash=%s guardians=%d",
                request_id, soul_hash, len(guardians),
            )

        self.recovery.register_alert_callback(_on_recovery_alert)
        # 第3层授权，依赖恢复层查询守护者列表
        self.authorization = AuthorizationEngine(
            storage=self.storage,
            recovery_manager=self.recovery
        )

        # ---- 系统层真实组件（持久化）----
        self.soul_ledger = SoulLedger(storage=self.storage)
        self.history = HistoryLedger(storage=self.storage)
        self.economy = EconomicReserve(
            storage=self.storage, authorization=self.authorization
        )
        for o in initial_oracles or ["oracle_a", "oracle_b", "oracle_c"]:
            self.economy.register_oracle(o)
        self.snapshot_registry = SnapshotRegistry(storage=self.storage)
        self.memory_vault = MemoryVault(storage=self.storage)
        self.consensus = ConsensusNetwork(storage=self.storage)
        self.governance = Governance(network=self.consensus)
        # 缺点接通 2：TcpTransport 挂载到共识网络（地平线一 E，端点为静态清单）
        # 监听地址必须与对外声明的端点一致：默认 port=0 会让内核随机分配，
        # 与静态清单里的端口对不上，结果是对端永远连不上本节点。
        self.transport = TcpTransport(
            node_id=self.node_id,
            host=_endpoint_host(self.cluster),
            port=_endpoint_port(self.cluster),
            endpoint_resolver=lambda nid: self.consensus.endpoints.get(nid),
            timeout=_CLUSTER_SEND_TIMEOUT if self.cluster is not None else 5.0,
            retries=_CLUSTER_SEND_RETRIES if self.cluster is not None else 1,
        )
        self.consensus.set_transport(self.transport)
        # 缺点接通 3：AOI 增量复制器复用同一传输层推送跨 DC Delta
        # 统一走 _send：所有出站消息共用同一出口，统一附加 HLC 时间戳与源节点
        self.aoi_sync.set_push(self._send)
        self.memory_integrity = MemoryInalienability(vault=self.memory_vault)
        # 第2层：有状态会话（签名密钥经 KMS 抽象托管，可插拔 HSM）
        # 会话存储按 STORAGE 选择：memory -> 内存；redis -> Redis（缺省降级）；其余 -> SQLite
        if self.storage_backend == "memory":
            self.session_store = MemorySessionStore()
        elif self.storage_backend == "redis":
            self.session_store = _build_redis_session_store() or SqliteSessionStore(self.storage)
        else:
            self.session_store = SqliteSessionStore(self.storage)
        # 密钥后端：redis/postgres 为生产形态，走云 KMS 抽象（未注入 client 时文件降级）
        if self.storage_backend in ("redis", "postgres"):
            self.kms = CloudKmsProvider(key_dir=self.storage.data_dir)
        else:
            self.kms = FileKmsProvider(self.storage.data_dir)
        # 会话签名密钥轮换（key_rotation 模块接线）：
        #   签发走活跃密钥（惰性检查轮换周期）；验证按 token 内嵌 key_id
        #   取密钥——retired 仍可验旧 token，revoked 即刻令其全部失效。
        #   未注入 rotation 时回落 KMS 静态密钥（向后兼容）。
        self.key_rotation = KeyRotationManager(storage=self.storage)
        self.sessions = SessionManager(
            storage=self.storage,
            kms_provider=self.kms,
            session_store=self.session_store,
            key_rotation=self.key_rotation,
        )
        # 地平线三：AR 眼镜聚合端口（薄客户端接入层）
        #   眼镜 = 灵魂的"窗口"，只是六层账户里的一个设备凭证。
        #   世界 App 通过 world.edge 完成设备绑定 / 就近路由 / 视口订阅，
        #   无需理解跨 DC 内部细节（复用 credentials / sessions / sharding / aoi）。
        self.edge = EdgeSdk(self)
        # 账户抽象（升级版账户层，account_abstraction 模块接线）：
        #   主身份（灵魂私钥）只做"授权会话密钥"，日常操作由会话密钥
        #   签名（额度 / 时效 / 范围三重约束），主私钥几乎不暴露。
        self.account_abstraction = AccountAbstractionEngine(storage=self.storage)
        # 灵魂漫游（soul_roaming 模块接线）：跨世界身份互认。
        #   本世界签名密钥对由 KMS 托管的 32B 秘密派生（Ed25519），
        #   不单独落盘私钥文件；世界公钥用于漫游证书的签发与验证。
        _world_secret = self.kms.get_or_create_key("world_signing_key")
        self.roaming = SoulRoamingProtocol(
            world_id=self.world_id,
            world_private_key=_world_secret,
            world_public_key=public_from_private(_world_secret),
            storage=self.storage,
        )
        logger.info(
            "world initialized world_id=%s storage_backend=%s session_store=%s",
            self.world_id,
            self.storage_backend,
            type(self.session_store).__name__,
        )

        # ---- 宪法层合规外壳（构成公理 + 治理公理）----
        self.spatial_substrate = SpatialSubstrate()
        self.spatial_substrate.define_topology("Euclidean", 3, "Infinite", 1e-3)
        self.temporal_substrate = TemporalSubstrate()
        self.temporal_substrate.define_temporal_properties("forward", 1.0, NOHN_LAW_AXIOMS["time_dilation"])
        self.causal_closure = CausalClosure()
        self.existence_axiom = ExistenceAxiom()
        self.genesis_condition = GenesisCondition()
        # 第负一章 · 无极：规则层必须与世界同源 id，否则分叉凭证的
        # parent_world_id 会指向自动生成的名字，分支树根接不上世界本体。
        self.immutable_rule = ImmutableWorldRule(world_id=self.world_id)
        self.immutable_rule.set_physics_constants({
            "gravity": NOHN_LAW_AXIOMS["gravity"],
            "time_dilation": NOHN_LAW_AXIOMS["time_dilation"],
            "unit_scale": NOHN_LAW_AXIOMS["unit_scale"],
            "element_reactions": {
                ("fire", "water"): "evaporation",
                ("fire", "electro"): "overload"
            }
        })
        self.central_brain = WorldCentralBrain()
        self.aesthetic = AestheticCompliance()
        self.soul_attestation = SoulAttestation()
        self.soul_attestation.soul_ledger = self.soul_ledger  # 注入真实账本
        self.world_perpetuity = WorldPerpetuity()
        self.world_perpetuity.history_chain = self.history  # 注入真实历史链
        self.world_perpetuity.snapshot_registry = self.snapshot_registry
        self.interoperability = MandatoryInteroperability()

        # ---- law 层合规属性（供审计 _audit_*_law 消费）----
        self.identity = {
            "soul_hash_sha256": True,
            "non_revocable": True,
            "cross_world_portable": True,
            "asset_bound": True,
        }
        self.communication = {
            "uses_nohn_semantics": True,
            "unknown_downgraded": True,
            "vocab_mapped": True,
        }
        self.physics = dict(self.immutable_rule.physics_constants)
        # 并网审查配置（interoperability.on_board_world 四维度）
        self.world_config = {
            "world_id": self.world_id,
            "semantics": self.communication,
            "physics": self.physics,
            "identity": self.identity,
            "economy": {
                "real_peg_1to1": self.economy.real_peg_1to1,
                "proof_of_reserve": self.economy.proof_of_reserve,
                "redemption_right": self.economy.redemption_right,
                "unilateral_fee": self.economy.unilateral_fee,
                "asset_bound_to_soul": self.economy.asset_bound_to_soul,
                "oracle_sources": self.economy.oracle_sources,
            },
        }

        # ---- 运行态实体 ----
        self.npcs: Dict[str, Agent] = {}
        self.main_quest = None  # 无主线（审计第四条）
        self.genesis_completed = False

        # 第负一章 · 无极：先把分支登记簿对齐到既有账本，再创世。
        # 必须在创世前完成，否则跨重启（持久账本）时分叉编号会与账本中
        # 既有记录撞号——而「账本是唯一真相」正是无极成立的前提。
        self._restore_fork_registry_from_ledger()

        self._bootstrap_genesis()
        # 地平线二接线：创世完成后再接集群——Intra-DC 快环需要已注册的共识节点
        self._wire_cluster()

    # ---- 集群接线（地平线二：把五个跨 DC 模块接进运行时）----
    def _wire_cluster(self) -> None:
        """按 ClusterConfig 接通跨 DC 链路。

        cluster 为 None 时直接返回，不改变任何单机行为。
        """
        if self.cluster is None:
            return
        cfg = self.cluster
        # 1. 静态端点清单 + 共识节点注册：本节点 + 全部对端。
        #    未注册为共识节点的对端收不到投票，也拿不到端点解析。
        if cfg.node_endpoint:
            self.consensus.attach_node(self.node_id, cfg.node_endpoint)
            if self.node_id not in self.consensus.nodes:
                self.consensus.register_node(self.node_id, endpoint=cfg.node_endpoint)
        for nid, addr in cfg.peers.items():
            self.consensus.attach_node(nid, addr)
            if nid not in self.consensus.nodes:
                self.consensus.register_node(nid, endpoint=addr)
        # 2. Intra-DC 快环：注册本 DC 成员（未配置 DC 成员时退回全部已知节点）
        local_nodes = cfg.local_nodes() or list(self.consensus.nodes.keys())
        for nid in local_nodes:
            self.intra_consensus.add_node(nid)
        # 3. Inter-DC 慢环：注入 dc_id 与出站函数，登记各 DC 成员
        self.interdc_consensus.epoch_manager.dc_id = cfg.local_dc
        self.interdc_consensus.epoch_manager.set_transport(self._send)
        self.interdc_consensus.register_dc(cfg.local_dc, local_nodes)
        for dc_id in cfg.remote_dcs():
            members = cfg.dc_nodes(dc_id)
            self.interdc_consensus.register_dc(dc_id, members)
            # DC 代表端点：让 dc_id 也可被解析成地址，供 epoch/handover 定向
            if members and members[0] in self.consensus.endpoints:
                self.consensus.attach_node(dc_id, self.consensus.endpoints[members[0]])
        # 4. 分片归属：把配置中声明的分片指派给对应 DC
        for dc_id, shard_ids in cfg.dc_shards.items():
            for sid in shard_ids:
                self.shard_manager.assign_shard(sid, dc_id)
        # 5. 跨域迁移握手复用同一出站口
        self.shard_manager.handover.set_transport(self._send)
        # 6. 入站白名单（未注册 op 一律降级，不写状态）
        self._register_transport_handlers()
        # 7. 启动监听 + 后台心跳。心跳绝不放进 tick：会阻塞主循环
        self.transport.set_callback(self._on_message)
        try:
            self.transport.start()
        except OSError as e:
            # 端口被占或地址不可用时降级为"不可达节点"，由分区容错兜底，
            # 而不是让整个 World 构造失败——单机态退化不应拖垮本地世界。
            logger.error(
                "tcp listen failed endpoint=%s err=%s (running as unreachable node)",
                cfg.node_endpoint, e,
            )
        self.heartbeat_loop = HeartbeatLoop(
            consensus=self.consensus,
            detector=self.partition_guard.detector,
            send_fn=self._send,
            interval_sec=cfg.heartbeat_interval_sec,
            skip_node_id=self.node_id,
        )
        self.heartbeat_loop.start()
        logger.info(
            "cluster wired dc=%s node=%s endpoint=%s peers=%d remote_dcs=%d",
            cfg.local_dc, self.node_id, cfg.node_endpoint,
            len(cfg.peers), len(cfg.remote_dcs()),
        )

    def _send(self, node_id: str, payload: Dict) -> Optional[Dict]:
        """统一出站口：附加 HLC 时间戳与源节点后交给传输层。

        所有跨节点消息必须经此出口，否则对端无法做 HLC 因果合流。
        """
        if self.transport is None:
            return None
        if isinstance(payload, dict):
            payload = dict(payload)
            with self._hlc_lock:
                payload.setdefault("hlc", self.hlc.send().to_dict())
            payload["_from"] = self.node_id
        return self.transport.send(node_id, payload)

    def _on_message(self, source: str, payload: Dict) -> Dict:
        """统一入站口：先做 HLC 因果合流，再交白名单分发。"""
        try:
            if isinstance(payload, dict) and isinstance(payload.get("hlc"), dict):
                with self._hlc_lock:
                    self.hlc.receive(HlcTimestamp.from_dict(payload["hlc"]))
                    self._hlc_merges += 1
        except Exception:  # pragma: no cover - 时钟合流失败不得影响消息处理
            logger.exception("hlc receive failed source=%s", source)
        return self._dispatcher.dispatch(source, payload)

    def _register_transport_handlers(self) -> None:
        """注册入站 op 白名单。

        每个 handler 只做一件事：把入站载荷转成对既有模块的合法调用。
        handler 不做鉴权决策——节点合法性由共识节点注册表把关。
        """
        d = self._dispatcher

        def op_ping(source: str, payload: Dict) -> Dict:
            return {"op": "pong", "node_id": self.node_id}

        def op_vote(source: str, payload: Dict) -> Dict:
            accepted = self.consensus.receive_vote(
                str(payload.get("proposal_id", "")), source, bool(payload.get("approve"))
            )
            return {"op": "vote_ack", "accepted": accepted}

        def op_aoi_delta(source: str, payload: Dict) -> Dict:
            delta = payload.get("delta") or {}
            data = delta.get("data") or {}
            with self._lock:
                for soul, state in data.items():
                    pos = (state or {}).get("position")
                    if isinstance(pos, list) and len(pos) == 3:
                        self.aoi_tracker.track_remote(soul, pos)
            return {"op": "aoi_ack", "bits": int(delta.get("bits", 0) or 0)}

        def op_epoch_sync(source: str, payload: Dict) -> Dict:
            self.interdc_consensus.receive_epoch(
                str(payload.get("source_dc", "")),
                int(payload.get("epoch_id", 0) or 0),
                list(payload.get("proposals", []) or []),
            )
            return {"op": "epoch_ack", "epoch_id": payload.get("epoch_id", 0)}

        def op_handover(source: str, payload: Dict) -> Dict:
            soul = str(payload.get("soul", ""))
            ctx = payload.get("context") or {}
            accepted = False
            with self._lock:
                # 仅当本地确实持有该灵魂时才落位；否则只记录，拒绝凭空创生
                if soul and soul in self.npcs:
                    pos = ctx.get("position") or [0.0, 0.0, 0.0]
                    if isinstance(pos, list) and len(pos) == 3:
                        self._register_position(soul, pos)
                        self.aoi_tracker.set_aoi(soul, pos)
                        accepted = True
                self._received_handovers.append(
                    {
                        "soul": soul,
                        "from": source,
                        "handover_id": payload.get("handover_id"),
                        "accepted": accepted,
                        "ts": time.time(),
                    }
                )
            return {
                "op": "handover_ack",
                "soul": soul,
                "handover_id": payload.get("handover_id"),
                "accepted": accepted,
            }

        d.register("ping", op_ping)
        d.register("vote", op_vote)
        d.register("aoi_delta", op_aoi_delta)
        d.register("epoch_sync", op_epoch_sync)
        d.register("handover_transfer", op_handover)

    def _probed_nodes(self) -> List[str]:
        """参与 WAN 活性探测的节点清单（已注册且声明了端点，排除自身）。

        创世占位节点没有端点，不能计入分区判定的分母——否则它们会被
        恒定判为失活，把整个集群误判为分区。cluster=None 时维持原语义。
        """
        if self.cluster is None:
            return list(self.consensus.nodes.keys())
        return sorted(
            n
            for n in self.consensus.nodes
            if n in self.consensus.endpoints and n != self.node_id
        )

    def _defer_cluster_sync(self, target_dcs: List[str]) -> None:
        """把跨 DC 同步任务交给后台线程，tick 不等待任何网络往返。

        epoch 广播与 AOI 增量都不在主循环上执行：单次连接超时 5s，
        N 个对端最坏阻塞 5N 秒，会直接摧毁"本地 tick 不等 WAN"的前提。
        """
        if self.heartbeat_loop is None:
            return
        if target_dcs:
            self.heartbeat_loop.submit(lambda: self._broadcast_epochs(target_dcs))
        self.heartbeat_loop.submit(self._push_aoi_deltas)

    def _broadcast_epochs(self, target_dcs: List[str]) -> None:
        """向远端 DC 的成员节点广播已关闭的 epoch 摘要。"""
        for dc_id in target_dcs:
            for node_id in self.interdc_consensus._dc_nodes.get(dc_id, []):
                self.interdc_consensus.sync_epochs(node_id)

    def _push_aoi_deltas(self) -> None:
        """按 AOI 关注域向各远端节点推送增量状态（带最小间隔节流）。"""
        if self.cluster is None:
            return
        with self._lock:
            local_state = {
                s: {"position": self.positions.get(s, [0.0, 0.0, 0.0])}
                for s in self.npcs
            }
        for node_id in self.cluster.peer_ids():
            if node_id == self.node_id:
                continue
            if not self.aoi_sync.should_sync(node_id):
                continue
            last = self._remote_aoi_state.get(node_id, {})
            delta = DeltaSync.diff(local_state, last)
            if delta["bits"]:
                touched = delta["added"] + delta["changed"]
                delta["data"] = {s: dict(local_state[s]) for s in touched}
                resp = self.aoi_sync.push_delta(node_id, delta)
                if resp is not None:
                    self._remote_aoi_state[node_id] = {
                        k: dict(v) for k, v in local_state.items()
                    }
            self.aoi_sync.mark_synced(node_id)

    def _begin_handover(
        self, soul_hash: str, target_shard: Optional[str], target_dc: str, position: List[float]
    ) -> Optional[str]:
        """发起跨域迁移：锁定 → 传输 → 完成。传输失败则智能体留在源 DC。"""
        ctx = {"position": list(position)}
        hid = self.shard_manager.handover.initiate(
            soul_hash, target_shard or "", target_dc, ctx
        )
        self.shard_manager.handover.lock(hid)
        resp = self.shard_manager.handover.transfer(hid)
        if resp is None:
            logger.warning(
                "handover failed hid=%s soul=%s target=%s (agent stays in source dc)",
                hid, soul_hash, target_dc,
            )
            return None
        self.shard_manager.handover.complete(hid)
        return hid

    # ---- 创世装配 ----
    def _bootstrap_genesis(self) -> None:
        """组装创世所需全部组件，真实调用 GenesisCondition.initiate_genesis。"""
        # 注册 ≥3 独立共识节点（治理公理十：去中心化）
        for i in range(3):
            self.consensus.register_node(f"node_{i:03d}", signature=None)
        # 创世区块
        genesis_block = self.history.append(
            {
                "event": "genesis",
                "world_id": self.world_id,
                "timestamp": time.time(),
            }
        )
        # ---- 第负一章 · 混沌 + R4「公示即执行」的真实生产者 ----
        # 此前 commitment() 只在宪法层与巡检脚本里被当作纯函数调用：
        # system/ 创世路径从未调用它，审计器不消费它，账本里也没有锚点，
        # 于是 R4 成了一条「公示了但没执行」的条款（空转）。
        # 此处把承诺哈希真正算出来、公示进 world_config、并锚进哈希链账本，
        # 使第三方可用 commitment(seed) 独立重算并与账本锚点比对。
        self.physics_commitment = self.immutable_rule.commitment(seed=self.genesis_seed)
        genesis_commitment_block = self.history.append(
            {
                "event": "genesis_commitment",
                "world_id": self.world_id,
                "physics_commitment": self.physics_commitment,
                "genesis_seed": self.genesis_seed,
                "timestamp": time.time(),
            }
        )
        # R4 两侧必须由同一次计算产生且相等：
        #   published_commitment —— 公示给外部世界的值
        #   ledger_commitment    —— 账本锚定的值
        # 审计器只比对这两侧与「重算值」，不再接受任何手写字面量。
        self.physics["published_commitment"] = self.physics_commitment
        self.physics["ledger_commitment"] = self.physics_commitment
        self.physics["genesis_seed"] = self.genesis_seed
        # R1–R3 / R5 的真实状态：全部由可观测事实推导，不做无条件声明。
        # R1 创世锁定 / R3 无外部注入 —— 常数锁已闭合，set_physics_constants 不再可写。
        _locked = bool(getattr(self.immutable_rule, "_physics_locked", False))
        _consts = self.immutable_rule.physics_constants
        self.physics["genesis_locked"] = _locked
        self.physics["no_exogenous_injection"] = _locked
        # R2 全域一致 —— 执行层持有的常数与规则层的唯一权威常量逐项相同。
        self.physics["constants_globally_consistent"] = all(
            self.physics.get(k) == _consts.get(k)
            for k in ("gravity", "time_dilation", "unit_scale")
        )
        # R5 反应表完备 —— 创世时要素反应表已非空声明。
        self.physics["reaction_table_complete"] = bool(_consts.get("element_reactions"))
        # 创世灵魂（可为空，但必须显式声明）
        genesis_souls: List[str] = []
        genesis_config = {
            "spatial_substrate": self.spatial_substrate,
            "temporal_substrate": self.temporal_substrate,
            "causal_closure": self.causal_closure,
            "existence_axiom": self.existence_axiom,
            "initial_consensus_nodes": list(self.consensus.nodes.keys()),
            "genesis_block": genesis_block,
            "genesis_commitment_block": genesis_commitment_block,
            "genesis_souls": genesis_souls,
        }
        self.genesis_completed = self.genesis_condition.initiate_genesis(genesis_config)

    # ---- 世界演化 ----
    def spawn_agent(
        self,
        soul_hash: Optional[str] = None,
        personality: Optional[Dict] = None,
        genesis_proof: Optional[Dict] = None,
    ) -> Optional[Agent]:
        """创生智能体（定稿·密钥链路）：soul_hash 必须为 64 位 hex 且由公钥指纹派生。

        创世证明必须先通过签名校验（verify_genesis_proof），任意伪造/篡改的
        证明一律被拒——无论该 soul_hash 是否已存在（防伪造覆盖语义）。
        已存在且证明有效的灵魂返回已有 Agent，不覆盖需求状态和行动历史。
        """
        if genesis_proof is None or not verify_genesis_proof(genesis_proof):
            return None  # 无效签名 / 非公钥证明：拒绝凭空捏造或伪造身份
        derived = derive_soul_hash(genesis_proof)
        if soul_hash is None:
            soul_hash = derived
        if not is_hex64(soul_hash):
            return None
        if derived is not None and derived != soul_hash:
            return None  # 提供的 soul_hash 与公钥指纹不一致
        with self._lock:
            # 已存在则直接返回，不覆盖
            if soul_hash in self.npcs:
                return self.npcs[soul_hash]
            # 1. 灵魂确权（SHA-256 公钥指纹，持久化到 SQLite）
            if not self.soul_ledger.exists(soul_hash):
                if self.soul_ledger.register_soul(genesis_proof) != soul_hash:
                    return None
            # 2. 存在公理：创生（需因果 + 位置）
            self.existence_axiom.bring_into_existence(
                soul_hash,
                cause="GENESIS",
                initial_state={"alive": True},
                location=[0.0, 0.0, 0.0],
            )
            # 3. 因果闭包：创生事件挂到创世
            self.causal_closure.link_cause(f"spawn:{soul_hash}", ["GENESIS"])
            # 4. 智能体实例
            agent = Agent(
                soul_hash,
                personality=personality,
                memory_vault=self.memory_vault,
                storage=self.storage,
                genesis_seed=self.genesis_seed,
            )
            self.npcs[soul_hash] = agent
            self._invalidate_npc_cache()
            # 空间索引注册：创生于原点 [0,0,0]
            self._register_position(soul_hash, [0.0, 0.0, 0.0])
            # 地平线二：AOI 关注域注册 + 分片归属
            self.aoi_tracker.set_aoi(soul_hash, [0.0, 0.0, 0.0])
            return agent

    def tick(self) -> Dict:
        """推进世界一个 tick：时间 + 决策 + 事件传导 + 历史追加。

        确定性事件全序（地基 C）：动作按 soul_hash 排序产出（消除 dict
        遍历对插入序的隐性依赖），每个事件携带 (order_seq, node_id, hlc)
        三元组，保证跨节点按 100% 相同顺序重放。
        Gas 计量（地基 B）：全局预算均分到各 agent，消耗超限则跳过。
        地平线二：每 tick 检查分区状态 + 纪元推进。
        空间推进（video 增量扩展，S1）：每 tick 经确定性算子推进各灵魂位置，
        位移仅由 (world_id, genesis_seed, clock, soul_hash) 派生，并写入事件。
        """
        with self._lock:
            clock = self.temporal_substrate.tick()
            # 账户抽象：低频维护——每 100 tick 清理一次过期会话密钥
            if int(clock) % 100 == 0:
                self.account_abstraction.cleanup_expired()
            events = []
            seq = self._event_seq
            n = len(self.npcs)
            # Gas 预算：均分到各 agent，防止单个 agent 死循环/无限递归锁死线程
            per_agent = max(1, self.tick_budget // n) if n > 0 else self.tick_budget
            # 地平线二：分区检测 + 纪元推进
            self.partition_guard.guard(self._probed_nodes())
            epoch_sync = self.interdc_consensus.tick()
            # 跨 DC 同步只入队，不在此处发任何网络包（否则 WAN 延迟进入 tick）
            self._defer_cluster_sync(list(epoch_sync.get("target_dcs") or []))
            # ---- 本 tick 起点的位置快照 ----
            # 目标解析（谁该朝哪走）必须只看 tick 开始时的位置，否则同 tick 内
            # 先处理的 agent 会影响后处理的 agent —— 那是顺序依赖，不是世界演化。
            ordered_souls = self._sorted_npcs()
            pos_snapshot = {
                soul: list(self.positions.get(soul, [0.0, 0.0, 0.0]))
                for soul in ordered_souls
            }
            neighbors = self._compute_neighbors(pos_snapshot)
            # 确定性全序：按 soul_hash 字典序，杜绝顺序漂移
            for soul in ordered_souls:
                agent = self.npcs[soul]
                meter = GasMeter(budget=per_agent, timeout_ms=self.tick_timeout_ms)
                try:
                    action = agent.decide_next_action({
                        "tick": clock,
                        "gas_meter": meter,
                        "neighbors": neighbors.get(soul, []),
                    })
                except GasExceeded:
                    # Gas 耗尽 → 跳过该 agent（无状态副作用，保证不锁死线程）
                    action = "gas_exhausted"
                seq += 1
                with self._hlc_lock:
                    hlcts = self.hlc.send()
                event = {
                    "tick": clock,
                    "order_seq": seq,
                    "node_id": self.node_id,
                    "hlc": hlcts.to_dict(),
                    "soul": soul,
                    "action": action,
                }
                # 空间推进算子（video 增量扩展，S1）：决策之后推进空间位置。
                # 位置写入事件，供 replay_canonical_events 跨节点重建空间状态。
                # 方向由行动决定（见 _resolve_move_target），sha256 只做抖动。
                new_pos, partner, gain, closeness, target = self._advance_space(
                    clock, soul, action, pos_snapshot, neighbors.get(soul, []))
                event["pos"] = new_pos
                event["interact"] = {
                    "partner": partner,
                    "strength": round(gain, 6),
                    "closeness": round(closeness, 6),
                }
                # 目标承诺：进展折算需求恢复；到达 / 超期则完成目标
                self._advance_goal(agent, action, target, new_pos, closeness)
                events.append(event)
                # 因果闭包：行动以智能体存在为因
                self.causal_closure.link_cause(f"act:{soul}:{clock}", [f"spawn:{soul}"])
                # 地平线二：分区降级记录
                if self.partition_guard.in_partition:
                    self.partition_guard.record_operation(
                        {"op": "tick_action", "soul": soul, "action": action}
                    )
            # 社会交互结算：本 tick 的 socialize 双方互更新关系值与归属感。
            # 放在循环之后 —— 结算只影响下一个 tick 的决策，避免同 tick 内
            # 先结算的 agent 影响后决策的 agent。
            self._settle_social(events)
            self._event_seq = seq
            if events:
                self.history.append({"event": "tick", "tick": clock, "actions": events})
            return {"tick": clock, "events": events}

    # ---- 空间索引（地基 A）----
    @staticmethod
    def _cell_key(pos, cell: float = 10.0) -> str:
        """整数网格单元键：固定网格划分，制造稳定局部性。"""
        x, y, z = int(pos[0] // cell), int(pos[1] // cell), int(pos[2] // cell)
        return f"{x}_{y}_{z}"

    def _invalidate_npc_cache(self) -> None:
        self._npcs_sorted_cache = None

    def _sorted_npcs(self) -> List[str]:
        """返回排序后的 npc 键列表（惰性缓存，避免每 tick 重排）。"""
        if self._npcs_sorted_cache is None:
            self._npcs_sorted_cache = sorted(self.npcs)
        return self._npcs_sorted_cache

    def _unregister_position(self, soul_hash: str) -> None:
        old = self.positions.pop(soul_hash, None)
        if old is None:
            return
        cell = self._cell_key(old)
        bucket = self.spatial.get(cell)
        if bucket:
            bucket.discard(soul_hash)
            if not bucket:
                self.spatial.pop(cell, None)

    def _register_position(self, soul_hash: str, pos) -> None:
        self._unregister_position(soul_hash)
        self.positions[soul_hash] = list(pos)
        self.spatial.setdefault(self._cell_key(pos), set()).add(soul_hash)

    # ---- 空间推进算子（video 增量扩展，S1）----
    # 语义边界：本算子只推进空间坐标，不读写需求/记忆/账本/共识，
    # 因此不构成「脚本化剧情」——运动由**世界自身的决策**派生，
    # 导演层只下发镜头，绝不下发位移。
    #
    # W1：方向由 action 决定（目标点解析），sha256 退化为抖动量。
    # 改之前位移与决策完全无关 —— 画面上"需求在变、行为乱走"，
    # 两者互相矛盾；改之后运动与状态开始互相解释。
    SPACE_STEP: float = 0.5
    SPACE_BOUND: float = 20.0
    # 抖动幅度相对决策步长的比例。抖动太大会把方向冲淡 —— agent 朝固定
    # 目标走却像在原地打转，画面上读不出"他在去哪"。0.25 让决策方向主导，
    # 同时保留一点有机感。
    JITTER_SCALE: float = 0.25
    SOCIAL_RANGE: float = 25.0        # 社交有效距离（超出则无交互）
    SOCIAL_BOND_GAIN: float = 0.05    # 单次交互写入 relationships 的累积量
    SOCIAL_REACHED_CLOSENESS: float = 0.5  # 亲密度达到此值视为"社交成功"
    SOCIAL_SATISFY_RATE: float = 0.06    # 归属感的专属恢复速率（按亲密度折算）
    GOAL_ARRIVE_EPS: float = 1.0      # 到达判定距离
    # 个人目标点的分布半径。agent 在这个半径内活动 —— 世界因此像一个
    # "城镇"而不是旷野：它们各有一个要去的地方，但彼此够得着，
    # 社交与归属感才有机会发生（半径太大则人人孤独，归属感永远归零）。
    GOAL_RADIUS_RATIO: float = 0.5
    NEIGHBOR_LIMIT: int = 4           # 每个 agent 关注的近邻数上限

    # 行动 → 移动速度系数。不同行动的"急迫感"不同，直接影响画面节奏。
    ACTION_SPEED = {
        "seek_resources": 1.15,
        "seek_shelter": 1.05,
        "socialize": 1.30,
        "pursue_achievement": 0.95,
        "self_actualize": 1.00,
        "gas_exhausted": 1.00,
    }

    def _compute_neighbors(self, pos_snapshot: Dict[str, List[float]]
                           ) -> Dict[str, List[Tuple[str, float]]]:
        """按本 tick 起点的位置快照计算近邻表。

        返回 {soul: [(other_soul, distance), ...]}，按 (距离, soul_hash) 排序，
        取前 NEIGHBOR_LIMIT 个。近邻是"世界里的邻居"，不是导演指定的角色。
        """
        souls = sorted(pos_snapshot)
        out: Dict[str, List[Tuple[str, float]]] = {}
        for soul in souls:
            here = pos_snapshot[soul]
            row: List[Tuple[str, float]] = []
            for other in souls:
                if other == soul:
                    continue
                there = pos_snapshot[other]
                dist = math.sqrt(sum((here[i] - there[i]) ** 2 for i in range(3)))
                row.append((other, dist))
            row.sort(key=lambda item: (item[1], item[0]))
            out[soul] = row[: self.NEIGHBOR_LIMIT]
        return out

    def _achievement_target(self, soul_hash: str) -> List[float]:
        """每个 agent 的固定"成就目标点"：由创世参数派生，恒定不变。

        恒定是关键 —— agent 持续朝自己的目标推进，产生方向性与目的感，
        而不是每 tick 换个地方乱走。
        """
        material = f"{self.world_id}|{self.genesis_seed}|goal|{soul_hash}".encode("utf-8")
        digest = hashlib.sha256(material).digest()
        limit = self.SPACE_BOUND * self.GOAL_RADIUS_RATIO
        out = []
        for axis in range(3):
            raw = int.from_bytes(digest[axis * 2:axis * 2 + 2], "big")
            out.append((raw / 65535.0 * 2.0 - 1.0) * limit)
        return out

    def _resource_target(self, soul_hash: str) -> List[float]:
        """每个 agent 的固定资源点：由创世参数派生，恒定不变。

        为什么是 per-soul 而不是世界级单一资源点：
        世界级单点会让所有 agent 涌向同一处 —— 实测画面上挤成一团、
        关系值互相饱和到 1.0。per-soul 目标让 agent 各自奔向自己那片
        资源区，空间上分散，社交仍然发生在具体的两两之间。

        可复算性：目标点只由 (world_id, genesis_seed, soul_hash) 决定，
        三者都在状态里，第三方无需额外信息即可复算 —— 它是移动启发式，
        不是新的世界实体，不进 FrameState、不影响 needs、不进内容摘要。
        """
        material = f"{self.world_id}|{self.genesis_seed}|resource|{soul_hash}".encode("utf-8")
        digest = hashlib.sha256(material).digest()
        limit = self.SPACE_BOUND * self.GOAL_RADIUS_RATIO
        out = []
        for axis in range(3):
            raw = int.from_bytes(digest[axis * 2:axis * 2 + 2], "big")
            out.append((raw / 65535.0 * 2.0 - 1.0) * limit)
        return out

    def _wander_target(self, soul_hash: str, index: int) -> List[float]:
        """自我实现 = 漫游：每完成一轮目标就换一个探索点。

        没有目标点的行动只能原地乱晃 —— 画面上三分之一的人在发呆。
        换点漫游同样由创世参数派生，确定性不变，但 agent 始终朝着某处走。
        """
        material = ("{0}|{1}|wander|{2}|{3}".format(
            self.world_id, self.genesis_seed, soul_hash, index)).encode("utf-8")
        digest = hashlib.sha256(material).digest()
        limit = self.SPACE_BOUND * self.GOAL_RADIUS_RATIO
        out = []
        for axis in range(3):
            raw = int.from_bytes(digest[axis * 2:axis * 2 + 2], "big")
            out.append((raw / 65535.0 * 2.0 - 1.0) * limit)
        return out

    def _resolve_move_target(self, action: str, soul: str,
                             snapshot: Dict[str, List[float]],
                             neighbors: List[Tuple[str, float]],
                             ) -> Tuple[Optional[List[float]], Optional[str]]:
        """把行动解析成目标点。返回 (目标点 or None, 交互对象 or None)。

        目标点全部由**世界自身的状态或创世参数**推出：资源点、创世派生的
        目标点、邻居位置、世界中心 —— 没有一个来自导演层。
        """
        if action == "seek_shelter":
            return [0.0, 0.0, 0.0], None
        if action == "socialize":
            if neighbors:
                partner = neighbors[0][0]
                # 目标点取最近若干邻居的**质心**，而不是最近的那一个人。
                # 追一个人是追不上的 —— 对方也在走；朝人堆走才真能遇上人。
                # 实测：改为质心后归属感从常年 0 变成可涨可落。
                group = [snapshot[other] for other, _ in neighbors]
                target = [sum(p[i] for p in group) / len(group) for i in range(3)]
                return target, partner
            return None, None
        if action == "seek_resources":
            return self._resource_target(soul), None
        if action == "pursue_achievement":
            return self._achievement_target(soul), None
        if action == "self_actualize":
            agent = self.npcs.get(soul)
            index = int(getattr(agent, "goal_index", 0) or 0) if agent else 0
            return self._wander_target(soul, index), None
        return None, None

    def _space_delta(self, clock: int, soul_hash: str) -> List[float]:
        """确定性空间抖动：仅由 (world_id, genesis_seed, clock, soul_hash) 派生。

        不读 wall clock、不依赖 dict 遍历序、不使用 random 模块 —— 同
        (genesis_seed, clock, soul_hash) 在任何节点、任何重放中得到同一位移。
        """
        material = f"{self.world_id}|{self.genesis_seed}|{clock}|{soul_hash}".encode("utf-8")
        digest = hashlib.sha256(material).digest()
        out: List[float] = []
        for axis in range(3):
            raw = int.from_bytes(digest[axis * 2:axis * 2 + 2], "big")
            out.append((raw / 65535.0 * 2.0 - 1.0) * self.SPACE_STEP)
        return out

    def _advance_space(self, clock: int, soul_hash: str, action: str,
                       snapshot: Dict[str, List[float]],
                       neighbors: List[Tuple[str, float]],
                       ) -> Tuple[List[float], Optional[str], float, float,
                                  Optional[List[float]]]:
        """推进单个灵魂的空间位置，返回 (新坐标, 交互对象, 交互强度)。

        位移 = 方向分量（由行动决定）+ 抖动分量（由 seed/tick/soul 派生）。
        """
        current = list(snapshot.get(soul_hash, [0.0, 0.0, 0.0]))
        target, partner = self._resolve_move_target(
            action, soul_hash, snapshot, neighbors)

        speed = float(self.ACTION_SPEED.get(action, 1.0))
        agent = self.npcs.get(soul_hash)
        openness = 0.5
        if agent is not None:
            try:
                openness = float(agent.personality.get("openness", 0.5))
            except (TypeError, ValueError):
                openness = 0.5

        delta = [0.0, 0.0, 0.0]
        if target is not None:
            diff = [target[i] - current[i] for i in range(3)]
            norm = math.sqrt(sum(v * v for v in diff))
            if norm > 1e-9:
                # 性格调制移动幅度：openness 越高走得越远
                reach = 0.75 + 0.5 * openness
                step = self.SPACE_STEP * speed * reach
                delta = [diff[i] / norm * step for i in range(3)]

        # sha256 抖动：保留有机感，但幅度压到决策步长的一小部分
        jitter = self._space_delta(clock, soul_hash)
        delta = [delta[i] + jitter[i] * self.JITTER_SCALE for i in range(3)]

        new_pos = [
            max(-self.SPACE_BOUND, min(self.SPACE_BOUND, current[i] + delta[i]))
            for i in range(3)
        ]
        self.move_agent(soul_hash, new_pos)

        gain = 0.0
        closeness = 0.0
        if partner is not None:
            gain, closeness = self._interaction_metrics(
                soul_hash, partner, neighbors)
        return new_pos, partner, gain, closeness, target

    def _advance_goal(self, agent, action: str, target: Optional[List[float]],
                      new_pos: List[float], closeness: float) -> None:
        """推进 agent 的目标承诺。

        进展系数：一般目标 1.0；socialize 用亲密度 —— 离得远就恢复不了，
        归属感只能靠真的靠近来兑现。到达目标（或承诺超期）即完成目标，
        agent 下一 tick 重新评估选新目标。
        """
        if not agent.goal_action:
            return
        factor = closeness if action == "socialize" else 1.0
        if action == "socialize":
            agent.apply_goal_progress(factor, rate=self.SOCIAL_SATISFY_RATE)
        else:
            agent.apply_goal_progress(factor)
        reached = False
        if action == "socialize":
            reached = closeness >= self.SOCIAL_REACHED_CLOSENESS
        elif target is not None:
            distance = math.sqrt(
                sum((new_pos[i] - target[i]) ** 2 for i in range(3)))
            reached = distance <= self.GOAL_ARRIVE_EPS
        if reached or agent.goal_ticks >= Agent.GOAL_MAX_TICKS:
            agent.complete_goal()

    def _interaction_metrics(self, soul: str, partner: str,
                             neighbors: List[Tuple[str, float]]
                             ) -> Tuple[float, float]:
        """一次社交的两个量：(关系累积量, 亲密度)。

        - 关系累积量 → 写进 relationships（"我和谁有多熟"）
        - 亲密度     → 决定归属感被满足多少（越近越满足）

        距离越近越强；openness 越接近，关系积累越快（性格相近的人更容易
        熟起来），但**不**影响亲密度 —— 靠近了就是靠近了。
        """
        distance = None
        for other, dist in neighbors:
            if other == partner:
                distance = dist
                break
        if distance is None:
            return 0.0, 0.0
        closeness = max(0.0, 1.0 - distance / self.SOCIAL_RANGE)
        a = self.npcs.get(soul)
        b = self.npcs.get(partner)
        if a is None or b is None:
            return 0.0, 0.0
        try:
            match = 1.0 - abs(float(a.personality.get("openness", 0.5))
                             - float(b.personality.get("openness", 0.5)))
        except (TypeError, ValueError):
            match = 0.5
        bond = self.SOCIAL_BOND_GAIN * closeness * max(0.0, min(1.0, match))
        return bond, closeness

    def _settle_social(self, events: List[Dict]) -> None:
        """社会交互结算：socialize 的**双方**互更新关系值。

        这是 relationships 字段第一次真的有内容：它记录"确实和谁交互过、
        交互多强"，而不是自我加分。归属感（belonging）不在这里给 ——
        它由 `_advance_goal` 按**亲密度**折算（离得远就恢复不了）。
        """
        for event in events:
            if event.get("action") != "socialize":
                continue
            soul = event.get("soul")
            interact = event.get("interact") or {}
            partner = interact.get("partner")
            bond = float(interact.get("strength") or 0.0)
            if not soul or not partner or soul == partner or bond <= 0.0:
                continue
            a = self.npcs.get(soul)
            b = self.npcs.get(partner)
            if a is None or b is None:
                continue
            a.relationships[partner] = min(1.0, a.relationships.get(partner, 0.0) + bond)
            b.relationships[soul] = min(1.0, b.relationships.get(soul, 0.0) + bond)

    def position_of(self, soul_hash: str) -> List[float]:
        """取某智能体的空间坐标（未注册回落原点）。"""
        return list(self.positions.get(soul_hash, [0.0, 0.0, 0.0]))

    def move_agent(self, soul_hash: str, pos) -> bool:
        """移动智能体并更新空间索引。目标必须为三维坐标。

        地平线二：同时更新 AOI 关注域 + 检查是否跨分片边界。
        """
        if soul_hash not in self.npcs or len(pos) != 3:
            return False
        prev = self.positions.get(soul_hash)
        new_pos = [float(p) for p in pos]
        self._register_position(soul_hash, new_pos)
        # 地平线二：更新 AOI 中心
        self.aoi_tracker.set_aoi(soul_hash, new_pos)
        # 跨分片检测（仅当有旧位置且有分片路由）
        if prev is not None:
            prev_shard = self.shard_manager.router.shard_of(prev)
            new_shard = self.shard_manager.router.shard_of(new_pos)
            if prev_shard != new_shard:
                logger.info(
                    "agent crossed shard soul=%s %s->%s",
                    soul_hash, prev_shard, new_shard,
                )
                # 只有跨数据中心才走握手协议。同 DC 内跨分片纯属本地索引变更，
                # 若一并走 TCP 往返，本地移动会被自身的迁移流程拖垮。
                prev_dc = self.shard_manager.owner_dc(prev)
                new_dc = self.shard_manager.owner_dc(new_pos)
                if prev_dc is not None and new_dc is not None and prev_dc != new_dc:
                    self._begin_handover(soul_hash, new_shard, new_dc, new_pos)
        return True

    # ---- 缺点接通 4：脑裂恢复后的净态合并公开口 ----
    def merge_partition_state(self, remote_state: Dict, base_state: Optional[Dict] = None) -> Dict:
        """网络分区恢复后，将远端净态与本机净态经 Merkle 差分树无冲突合并。

        local_state 取当前 spatially 登记的全部 Agent 位置；冲突键取自本机。
        返回合并后的新状态，并记录审计报告。
        """
        local_state = {
            s: self.positions.get(s, [0.0, 0.0, 0.0]) for s in self.npcs
        }
        base = base_state if base_state is not None else local_state
        merged = self.partition_guard.merge_engine.merge(
            local_state=local_state,
            remote_state=remote_state,
            base_state=base,
        )
        return merged

    def agents_near(self, origin, radius: float = 5.0) -> List[str]:
        """AOI 关注域检索：利用空间网格索引避免全表扫描。

        只扫描 origin 周围 3×3×3 个 cell 内的候选灵魂，再按精确欧氏
        距离过滤——从 O(N) 降至 O(局部候选数)。
        """
        r2 = radius * radius
        cell = 10.0
        cx, cy, cz = int(origin[0] // cell), int(origin[1] // cell), int(origin[2] // cell)
        span = int(radius // cell) + 1
        candidate_set: set = set()
        for dx in range(-span, span + 1):
            for dy in range(-span, span + 1):
                for dz in range(-span, span + 1):
                    key = f"{cx + dx}_{cy + dy}_{cz + dz}"
                    bucket = self.spatial.get(key)
                    if bucket:
                        candidate_set.update(bucket)
        hits = []
        for soul in candidate_set:
            p = self.positions.get(soul)
            if p is None:
                continue
            if sum((a - b) ** 2 for a, b in zip(p, origin)) <= r2:
                hits.append(soul)
        return sorted(hits)

    # ---- 状态 Merkle 根（地基 A/D 锚点）----
    def state_root(self) -> str:
        """对当前世界状态计算确定性 Merkle 根，供跨节点增量验证。"""
        state = {
            "world_id": self.world_id,
            "clock": self.temporal_substrate.global_clock,
            "event_seq": self._event_seq,
            "hlc": self.hlc.peek().to_dict(),
            "souls": sorted(self.soul_ledger.souls.keys()),
            "agents": sorted(self.npcs.keys()),
            "positions": {
                s: self.positions.get(s, [0.0, 0.0, 0.0]) for s in sorted(self.npcs)
            },
        }
        return merkle_root(state)

    def replay_canonical_events(self) -> Dict:
        """重放全部 tick 事件并断言全序（跨节点确定性重放映射）。

        返回 {count, deterministic_order, events}：按 (order_seq, node_id)
        排序后校验相邻不逆序——同一批事件在任意节点必得相同重放序列。
        """
        flat = []
        for ts, event, block_hash in self.history.chain:
            if event.get("event") == "tick":
                flat.extend(event.get("actions", []))
        flat.sort(key=lambda e: (e.get("order_seq", 0), e.get("node_id", "")))
        ordered = all(
            (flat[i].get("order_seq"), flat[i].get("node_id"))
            <= (flat[i + 1].get("order_seq"), flat[i + 1].get("node_id"))
            for i in range(len(flat) - 1)
        )
        return {"count": len(flat), "deterministic_order": ordered, "events": flat}

    # ---- 第负一章 · 原始框架的可执行接口 ----
    def represent(self, actor: str, content: Dict, truth: bool = False) -> Dict:
        """
        第负一章 · 虚幻：向表征层写入一条表征（信念 / 传闻 / 梦境）。

        硬边界：本方法只写 self.representations，绝不触碰 physics_constants、
        账本、共识或承诺哈希。truth 只作为表征内容被记录，不参与任何执行层
        判定——真伪之别留在表征层内部，这正是「亦真亦假亦如梦」的机械含义。
        """
        if not isinstance(actor, str) or not actor:
            return {}
        entry = dict(content) if isinstance(content, dict) else {"content": content}
        entry["truth"] = bool(truth)
        entry["tick"] = self.temporal_substrate.global_clock
        with self._lock:
            self.representations.setdefault(actor, []).append(entry)
        return entry

    def beliefs_of(self, actor: str) -> List[Dict]:
        """读取某主体的全部表征（信念 / 传闻 / 梦境）。"""
        return list(self.representations.get(actor, []))

    def _restore_fork_registry_from_ledger(self) -> None:
        """
        第负一章 · 无极：把分支登记簿对齐到账本（以账本为唯一真相）。

        为什么必须做：宪法层 `_fork_world` 的 child_id 由
        `len(self.fork_registry) + 1` 推导，而 `fork_registry` 原本只是
        进程内列表。持久账本下重启一次，登记簿归零、编号回到 001，
        便与账本中既有分叉记录撞号——同一分支空间里出现两个同名子世界，
        分支树随即自相矛盾。

        因此这里在创世前回填：账本里属于本世界的 `world_fork` 区块
        逐条还原进登记簿，使编号序列跨进程、跨重启仍然唯一且只增。
        回填只补计数与凭证指针，不重算常数、不触碰父世界状态。
        """
        restored = 0
        for _ts, event, _block_hash in self.history.chain:
            if not isinstance(event, dict) or event.get("event") != "world_fork":
                continue
            if event.get("world_id") != self.world_id:
                continue  # 共享账本中可能存在其他世界的分叉，不计入本世界序列
            self.immutable_rule.fork_registry.append({
                "fork_id": event.get("fork_id"),
                "parent_world_id": event.get("parent_world_id"),
                "parent_commitment": event.get("parent_commitment"),
                "child_commitment": event.get("child_commitment"),
                "parent_untouched": event.get("parent_untouched"),
                "requires_migration": True,
                "ballot": None,
                "status": "forked",
                "restored_from_ledger": True,
            })
            restored += 1
        if restored:
            logger.info(
                "fork registry restored from ledger world_id=%s forks=%d",
                self.world_id, restored,
            )

    def fork_world(
        self,
        change: Dict,
        proposer: str,
        ballot: Optional[Dict] = None,
    ) -> Dict:
        """
        第负一章 · 无极：分叉出一个新世界，并把分叉凭证锚进哈希链账本。

        与 ImmutableWorldRule._fork_world 的分工（宪法层注释已声明）：
        宪法层只产出凭证、不承载世界对象本体；世界注册由 system/ 层负责。
        本方法即那个 system/ 层——凭证追加进 history 之后，branch_space()
        可从账本独立重建分支树，第三方无需信任本进程的内存状态。

        fail-closed：公投未达 ≥2/3 时不产生凭证，也不写入账本。
        父世界的常数在本方法内不被触碰（R1：分叉是复制，不是升级）。
        """
        before = len(self.immutable_rule.fork_registry)
        approved = self.immutable_rule.propose_amendment(change, proposer, ballot)
        if not approved or len(self.immutable_rule.fork_registry) <= before:
            return {"status": "fork_rejected", "reason": "no fork record produced"}
        record = self.immutable_rule.fork_registry[-1]
        block_hash = self.history.append(
            {
                "event": "world_fork",
                "world_id": self.world_id,
                "fork_id": record.get("fork_id"),
                "parent_world_id": record.get("parent_world_id"),
                "parent_commitment": record.get("parent_commitment"),
                "child_commitment": record.get("child_commitment"),
                "parent_untouched": record.get("parent_untouched"),
                "timestamp": time.time(),
            }
        )
        return {"status": "forked", "block_hash": block_hash, "record": record}

    def branch_space(self) -> Dict:
        """
        第负一章 · 无极：从账本独立重建分支空间（分支树）。

        只读 history 中 event == 'world_fork' 的区块，不依赖任何进程内状态，
        因此第三方可对同一账本重跑本方法并得到同一结果（可复算性）。
        """
        nodes: Dict[str, Dict] = {self.world_id: {"parent": None, "depth": 0}}
        children: Dict[str, List[str]] = {}
        forks = 0
        for _ts, event, _block_hash in self.history.chain:
            if not isinstance(event, dict) or event.get("event") != "world_fork":
                continue
            if event.get("world_id") != self.world_id:
                continue  # 共享账本中其他世界的分叉不属于本分支空间
            forks += 1
            parent = event.get("parent_world_id")
            child = event.get("fork_id")
            if not parent or not child:
                continue
            if parent not in nodes:
                nodes[parent] = {"parent": None, "depth": 0}
            nodes[child] = {
                "parent": parent,
                "depth": nodes[parent]["depth"] + 1,
                "parent_commitment": event.get("parent_commitment"),
                "child_commitment": event.get("child_commitment"),
            }
            children.setdefault(parent, []).append(child)
        return {
            "root": self.world_id,
            "nodes": nodes,
            "children": children,
            "fork_count": forks,
            "chain_valid": self.history.validate_chain(),
        }

    def conservation_residual(self) -> float:
        """
        第负一章 · 轮回：守恒残差（委托给储备账本，单一权威实现）。
        见 EconomicReserve.conservation_residual()。残差 ≤ 容差 即守恒式成立。
        """
        return self.economy.conservation_residual()

    # ---- 审计上报 ----
    def audit(self) -> AuditReport:
        """运行第二视角审计（维度数由 AuditReport.FIELDS 决定，不在此硬编码）。"""
        auditor = SecondPerspectiveAuditor()
        return auditor.audit_world(self)

    def audit_summary(self) -> str:
        return self.audit().summary()

    # ---- 快照 ----
    def snapshot(self) -> str:
        return self.snapshot_registry.create_snapshot(
            {
                "world_id": self.world_id,
                "clock": self.temporal_substrate.global_clock,
                "state_root": self.state_root(),
                "souls": list(self.soul_ledger.souls.keys()),
                "agents": list(self.npcs.keys()),
                "positions": {
                    s: self.positions.get(s, [0.0, 0.0, 0.0]) for s in sorted(self.npcs)
                },
            }
        )

    # ---- 身份根（第 0 层）----
    def create_identity_root(
        self, threshold: int = 3, num_shares: int = 5
    ) -> Dict:
        """为调用方生成身份根：主密钥对 + Shamir 分片。

        服务端零落盘：主私钥在内存中生成、分片后立即丢弃（模块内保证），
        公钥与全部分片一次性返回给调用方。调用方应离线分开保存分片，
        凑齐 threshold 份可重建主私钥（shamir_combine）。
        优先在设备端本地生成（identity_root.IdentityRoot）；
        此接口服务无安全区的薄客户端（AR 眼镜等）。

        返回：
          {"master_public_key": b64, "soul_hash": 64hex,
           "shares": [{"x": int, "y": hexstr}, ...],
           "threshold": t, "num_shares": n}
        """
        root = IdentityRoot(threshold=threshold, num_shares=num_shares)
        pubkey = root.generate()
        return {
            "master_public_key": base64.b64encode(pubkey).decode("ascii"),
            "soul_hash": root.soul_hash,
            "shares": [
                {"x": x, "y": format(y, "x")} for x, y in root.shares
            ],
            "threshold": threshold,
            "num_shares": num_shares,
        }

    def close(self) -> None:
        """关闭世界：先停集群后台线程与监听，再释放存储资源。"""
        if self.heartbeat_loop is not None:
            self.heartbeat_loop.stop()
        if self.cluster is not None and self.transport is not None:
            self.transport.stop()
        self.session_store.close()
        self.storage.close()


__all__ = ["World"]
