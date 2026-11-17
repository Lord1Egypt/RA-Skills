# system/consensus.py - 共识网络（真实实现，桩转实第 1 步）
# ============================================================
# 职责：真实化以下宪法契约（对齐 constitution_rules.py）：
#   - GenesisCondition 要求的 initial_consensus_nodes ≥3 注册
#   - DecentralizationGovernance._has_global_consensus（≥2/3 公投）
#   - ImmutableWorldRule._global_referendum（2/3 全民公投）
#   - ConsensusEngine.collect_decisions / consensus（先单机确定性实现）
#
# 依赖方向：system/consensus.py -> constitution_rules / system.ledger（单向）
# 持久化：复用 ledger.Storage（SQLite），表：nodes / proposals / votes / governance_log
#
# 审计契约：治理行为必须可追溯、可公开审计（governance_log / single_entity_actions），
# 禁止单点越权。freeze_soul / shutdown_world 硬编码返回 False（宪法级禁止）。
# ============================================================

import base64
import hashlib
import json
import logging
import socket
import struct
import threading
import time
from typing import Any, Dict, List, Optional, Callable

from .ledger import Storage
from .keys import verify_signature
from constitution_rules import CONSENSUS_THRESHOLD  # 宪法第十条：全球公投阈值（≥2/3，单一权威来源）

logger = logging.getLogger(__name__)


class ConsensusNetwork:
    """共识网络：节点注册 + 提案 + 公投计票（≥2/3），持久化可审计。"""

    def __init__(
        self, storage: Optional[Storage] = None, data_dir: Optional[str] = None
    ):
        self._storage = storage or Storage(data_dir=data_dir)
        self._storage.execute(
            "CREATE TABLE IF NOT EXISTS nodes ("
            "node_id TEXT PRIMARY KEY, signature TEXT, registered_at REAL)"
        )
        self._storage.execute(
            "CREATE TABLE IF NOT EXISTS proposals ("
            "proposal_id TEXT PRIMARY KEY, action TEXT, proposer TEXT, "
            "created_at REAL, status TEXT)"
        )
        self._storage.execute(
            "CREATE TABLE IF NOT EXISTS votes ("
            "proposal_id TEXT, node_id TEXT, approve INTEGER, ts REAL, "
            "PRIMARY KEY (proposal_id, node_id))"
        )
        self._storage.execute(
            "CREATE TABLE IF NOT EXISTS governance_log ("
            "seq INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, actor TEXT, "
            "verdict TEXT, ts REAL)"
        )
        self.nodes: Dict[str, str] = {}
        self._load()
        # 真联机（地基 4）：可插拔传输 + 节点端点 + 心跳活性表
        self.transport = None            # transport.send(node_id, payload) -> response dict
        self.endpoints: Dict[str, str] = {}  # node_id -> 静态对端地址（本地部署清单）
        self._heartbeat: Dict[str, float] = {}
        logger.info("consensus network ready nodes=%d", len(self.nodes))

    # ---- 真联机：传输 / 端点 / 心跳 ----
    def set_transport(self, transport) -> None:
        """注入可插拔传输（消息载体）。

        接受两种形态：
          - 对象：自身暴露 .send(node_id, payload) -> response dict
          - 纯可调用：transport(node_id, payload) -> response dict
        """
        self.transport = transport

    def attach_node(self, node_id: str, endpoint: Optional[str] = None) -> None:
        """声明本节点对外可达地址（静态清单；本地部署无需公网发现）。"""
        self.endpoints[node_id] = endpoint

    def receive_vote(self, proposal_id: str, node_id: str, approve: bool) -> bool:
        """远端传输解码后投递的投票消息（真联机入站口）。

        与本地 vote() 共用同一张 votes 表与计票逻辑，只是消息来源不同——
        由 transport.send 扇出、对端解码后回传。
        """
        if node_id not in self.nodes:
            return False
        rows = self._storage.query(
            "SELECT proposal_id FROM proposals WHERE proposal_id=?", (proposal_id,)
        )
        if not rows:
            return False
        self._storage.execute(
            "INSERT OR REPLACE INTO votes (proposal_id, node_id, approve, ts) "
            "VALUES (?, ?, ?, ?)",
            (proposal_id, node_id, 1 if approve else 0, time.time()),
        )
        return True

    def heartbeat(self, node_id: str) -> bool:
        """节点活性探测：注入 transport 时走真实 ping；否则以本地注册表为凭。

        返回 True 表示节点当前在线。
        """
        if self.transport is not None:
            carrier = self.transport
            if callable(getattr(carrier, "send", None)):
                sender = carrier.send
                payload = {"op": "ping"}
            else:
                sender = carrier
                payload = {"op": "ping"}
            try:
                resp = sender(node_id, payload)
                alive = resp is not None
            except Exception:
                alive = False
        else:
            alive = node_id in self.nodes
        if alive:
            self._heartbeat[node_id] = time.time()
        return alive

    def active_nodes(self, ttl: float = 10.0) -> List[str]:
        """返回活跃节点（心跳 ttl 窗口内），确定性排序。"""
        now = time.time()
        return sorted(n for n, t in self._heartbeat.items() if now - t <= ttl)

    # ---- 节点注册 ----
    def _load(self) -> None:
        for row in self._storage.query("SELECT node_id, signature FROM nodes"):
            self.nodes[row[0]] = row[1]

    def register_node(
        self,
        node_id: str,
        signature: Optional[bytes] = None,
        pubkey: Optional[bytes] = None,
        endpoint: Optional[str] = None,
    ) -> bool:
        """注册独立共识节点。node_id 唯一，不可重复注册。

        若提供 signature + pubkey，则验签（Ed25519，签名内容为 node_id），
        验签失败拒绝注册；若均未提供（创世引导），签名标记为 unverified
        占位，不冒充真实签名。endpoint 为可选的静态对端地址（本地部署清单）。
        """
        if not node_id or node_id in self.nodes:
            return False
        if signature is not None and pubkey is not None:
            if not verify_signature(pubkey, node_id.encode("utf-8"), signature):
                return False  # 签名无效，拒绝注册
            sig = base64.b64encode(signature).decode("ascii")
        else:
            # 创世引导：明确标记未验签，不冒充真实签名
            sig = "unverified:" + _sha256(node_id)
        self.nodes[node_id] = sig
        if endpoint:
            self.endpoints[node_id] = endpoint
        self._storage.execute(
            "INSERT OR REPLACE INTO nodes (node_id, signature, registered_at) "
            "VALUES (?, ?, ?)",
            (node_id, sig, time.time()),
        )
        return True

    def node_count(self) -> int:
        return len(self.nodes)

    # ---- 提案与公投 ----
    def create_proposal(self, action: Dict, proposer: str) -> str:
        """发起治理提案，返回 proposal_id。"""
        if not isinstance(action, dict) or not proposer:
            return ""
        proposal_id = _sha256(
            f"{proposer}|{json.dumps(action, sort_keys=True)}|{time.time()}"
        )[:16]
        self._storage.execute(
            "INSERT INTO proposals (proposal_id, action, proposer, created_at, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                proposal_id,
                json.dumps(action, ensure_ascii=False),
                proposer,
                time.time(),
                "open",
            ),
        )
        return proposal_id

    def vote(self, proposal_id: str, node_id: str, approve: bool) -> bool:
        """已注册节点对提案投票。非注册节点无权投票。"""
        if node_id not in self.nodes:
            return False
        rows = self._storage.query(
            "SELECT proposal_id FROM proposals WHERE proposal_id=?", (proposal_id,)
        )
        if not rows:
            return False
        self._storage.execute(
            "INSERT OR REPLACE INTO votes (proposal_id, node_id, approve, ts) "
            "VALUES (?, ?, ?, ?)",
            (proposal_id, node_id, 1 if approve else 0, time.time()),
        )
        return True

    def approval_rate(self, proposal_id: str) -> float:
        """赞成率 = 赞成票 / 全部节点数（含弃权者，弃权计入反对）。"""
        total = self.node_count()
        if total == 0:
            return 0.0
        rows = self._storage.query(
            "SELECT approve FROM votes WHERE proposal_id=?", (proposal_id,)
        )
        approves = sum(1 for r in rows if r[0] == 1)
        return approves / total

    def has_consensus(self, proposal_id: str) -> bool:
        """是否达成 ≥2/3 全球公投共识。"""
        return self.approval_rate(proposal_id) >= CONSENSUS_THRESHOLD

    def close_proposal(self, proposal_id: str) -> str:
        """关闭提案并返回最终状态（passed / rejected）。"""
        passed = self.has_consensus(proposal_id)
        status = "passed" if passed else "rejected"
        self._storage.execute(
            "UPDATE proposals SET status=? WHERE proposal_id=?", (status, proposal_id)
        )
        return status

    # ---- 治理日志（审计追溯）----
    def log_governance(self, action: Dict, actor: str, verdict: str) -> None:
        self._storage.execute(
            "INSERT INTO governance_log (action, actor, verdict, ts) VALUES (?, ?, ?, ?)",
            (json.dumps(action, ensure_ascii=False), actor, verdict, time.time()),
        )

    def governance_log(self) -> List[Dict]:
        rows = self._storage.query(
            "SELECT action, actor, verdict, ts FROM governance_log ORDER BY seq"
        )
        return [
            {"action": json.loads(r[0]), "actor": r[1], "verdict": r[2], "ts": r[3]}
            for r in rows
        ]


class Governance:
    """宪法第十条：反中心化控制。组合 ConsensusNetwork，提供真实公投治理。"""

    def __init__(
        self, network: Optional[ConsensusNetwork] = None, data_dir: Optional[str] = None
    ):
        self.network = network or ConsensusNetwork(data_dir=data_dir)
        self.governance_log: List[Dict] = []
        self.single_entity_actions: List[Dict] = []

    # ---- 宪法级硬编码禁止（审计第十条 / 第八条依赖）----
    def freeze_soul(self, soul_hash: str, actor: str) -> bool:
        """冻结数字生命？永远不合法。"""
        return False  # 硬编码禁止

    def shutdown_world(self, world_id: str, actor: str) -> bool:
        """单方面关停世界？永远不合法。"""
        return False  # 硬编码禁止

    # ---- 真实公投治理（两阶段：提案 → 投票 → 终议）----
    def propose_governance_action(self, action: Dict, actor: str) -> Optional[str]:
        """
        Phase 1: 提出治理提案。
        - 单实体发起 → 拒绝，返回 None
        - 合法发起 → 创建提案，返回 proposal_id
        调用方应收集节点投票后调用 finalize_governance_action(proposal_id)。
        """
        if self._is_single_entity(actor):
            self.single_entity_actions.append(
                {
                    "action": action,
                    "actor": actor,
                    "verdict": "REJECTED - single entity control prohibited",
                }
            )
            self._log(action, actor, "rejected_single_entity")
            return None
        proposal_id = self.network.create_proposal(action, actor)
        self._log(action, actor, f"proposed:{proposal_id}")
        return proposal_id

    def finalize_governance_action(self, proposal_id: Optional[str]) -> bool:
        """
        Phase 2: 检查提案是否达成 ≥2/3 全球公投共识。
        需在节点投票完成后调用。
        """
        if not proposal_id:
            return False
        passed = self.network.has_consensus(proposal_id)
        self.network.close_proposal(proposal_id)
        self._log({}, proposal_id, "passed" if passed else "rejected_no_consensus")
        return passed

    def validate_governance_action(
        self, action: Dict, actor: str, proposal_id: Optional[str] = None
    ) -> Any:
        """
        兼容入口：两阶段合一。
        - proposal_id=None → 走 Phase 1（创建提案），返回 proposal_id 或 None
        - proposal_id 非空 → 走 Phase 2（检查共识），返回 True/False
        """
        if proposal_id is None:
            return self.propose_governance_action(action, actor)
        return self.finalize_governance_action(proposal_id)

    def amend_base_rule(
        self, rule_id: str, new_value: Any, actor: str
    ) -> Optional[str]:
        """修改底层规则：提出治理提案，返回 proposal_id。需公投通过后调用 finalize。"""
        return self.propose_governance_action(
            {"rule_id": rule_id, "new_value": new_value}, actor
        )

    def _is_single_entity(self, actor: str) -> bool:
        """单一实体判定：节点数不足 3、或 actor 未注册为共识节点时视为单点。

        创世引导例外：节点数 < 3 时，允许创世者（第一个注册节点）
        直接执行治理操作（如添加初始节点），不经过公投。
        非创世者在引导期仍被拒绝。
        """
        if self.network.node_count() < 3:
            # 创世引导期：只有第一个注册节点（创世者）可操作
            nodes = list(self.network.nodes.keys())
            if nodes and actor == nodes[0]:
                return False  # 创世者豁免
            return True
        return actor not in self.network.nodes

    def _log(self, action: Dict, actor: str, verdict: str) -> None:
        record = {
            "action": action,
            "actor": actor,
            "verdict": verdict,
            "ts": time.time(),
        }
        self.governance_log.append(record)
        self.network.log_governance(action, actor, verdict)


def _sha256(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class TcpTransport:
    """TCP 传输层（本地分布式部署版）。

    静态清单寻址（无需 Kademlia DHT），JSON 帧以 4 字节大端长度前缀分割。
    send(target_node_id, payload) 按 endpoint 建立临时连接→发送→接收→关闭。
    服务端线程持续监听入站连接，将消息投递到回调函数。
    适用于本地可信内网，不处理 NAT/公网穿透。
    """

    _HEADER = struct.Struct("!I")  # 4 字节大端无符号=帧长

    def __init__(
        self,
        node_id: str,
        host: str = "127.0.0.1",
        port: int = 0,
        endpoint_resolver: Optional[Callable[[str], Optional[str]]] = None,
        timeout: float = 5.0,
        retries: int = 1,
    ):
        self.node_id = node_id
        self.host = host
        self.port = port
        # 单次连接超时与重试次数。集群心跳必须短超时 + 零重试：
        # Windows 上目标端口无监听时并非立即 RST，而是挂到超时，
        # 5s 超时 × 1 次重试会让一轮心跳卡 10s，故障检测形同失效。
        self._timeout = timeout
        self._retries = retries
        self._resolve = endpoint_resolver or (lambda nid: None)
        self._server: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._callback: Optional[Callable[[str, Dict], Optional[Dict]]] = None
        # 入站消息回调：callback(source_node_id, payload) -> response dict
        self._lock = threading.Lock()

    # ---- 生命周期 ----
    def start(self, backlog: int = 5) -> None:
        """启动 TCP 服务端线程。端口由 bind 确定后可通过 self.port 读取。"""
        if self._running:
            return
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self._server.listen(backlog)
        self.port = self._server.getsockname()[1]
        self._running = True
        self._thread = threading.Thread(
            target=self._serve_loop, daemon=True, name=f"tcp-{self.node_id}"
        )
        self._thread.start()
        logger.info(
            "tcp transport started node=%s listen=%s:%d",
            self.node_id, self.host, self.port,
        )

    def stop(self) -> None:
        """停止服务端线程并关闭监听套接字。"""
        self._running = False
        if self._server:
            try:
                self._server.close()
            except OSError:
                pass
            self._server = None
        logger.info("tcp transport stopped node=%s", self.node_id)

    def set_callback(self, cb: Callable[[str, Dict], Optional[Dict]]) -> None:
        """注册入站消息处理回调。cb(source_node_id, payload) -> response dict。"""
        self._callback = cb

    # ---- 服务端 ----
    def _serve_loop(self) -> None:
        while self._running:
            try:
                conn, addr = self._server.accept()  # type: ignore[union-attr]
                threading.Thread(
                    target=self._handle_conn,
                    args=(conn, addr),
                    daemon=True,
                ).start()
            except OSError:
                break  # 套接字关闭中断 accept

    def _handle_conn(self, conn: socket.socket, addr: tuple) -> None:
        try:
            payload = self._recv_frame(conn)
            if payload is None:
                return
            resp = None
            if self._callback:
                try:
                    resp = self._callback(payload.get("_from", ""), payload)
                except Exception:
                    pass
            self._send_frame(conn, resp or {"_error": "no_handler"})
        finally:
            try:
                conn.close()
            except OSError:
                pass

    # ---- 客户端（发送）----
    def send(
        self, target_node_id: str, payload: Dict, retries: Optional[int] = None
    ) -> Optional[Dict]:
        """向目标节点发送 JSON 帧并等待响应。

        retries 为 None 时沿用实例默认值；心跳场景应显式传 0。
        返回响应 dict；连接失败/超时返回 None。
        """
        endpoint = self._resolve(target_node_id)
        if not endpoint:
            logger.warning("no endpoint for node=%s", target_node_id)
            return None
        host, port_str = endpoint.split(":")
        port = int(port_str)
        payload["_from"] = self.node_id
        return self._send_to(host, port, payload, retries)

    def _send_to(
        self, host: str, port: int, payload: Dict, retries: Optional[int] = None
    ) -> Optional[Dict]:
        attempts = self._retries if retries is None else retries
        for attempt in range(1 + attempts):
            conn = None
            try:
                conn = socket.create_connection(
                    (host, port), timeout=self._timeout
                )
                self._send_frame(conn, payload)
                return self._recv_frame(conn)
            except (OSError, socket.timeout) as e:
                logger.debug(
                    "tcp send failed host=%s:%d attempt=%d/%d err=%s",
                    host, port, attempt + 1, 1 + attempts, e,
                )
                if attempt == attempts:
                    return None
            finally:
                if conn:
                    try:
                        conn.close()
                    except OSError:
                        pass
        return None

    # ---- 帧协议 ----
    @staticmethod
    def _send_frame(conn: socket.socket, obj: Dict) -> None:
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        conn.sendall(TcpTransport._HEADER.pack(len(data)))
        conn.sendall(data)

    @staticmethod
    def _recv_frame(conn: socket.socket) -> Optional[Dict]:
        """接收完整 JSON 帧。逐字节读满 4 字节头 + N 字节负载。

        不使用 MSG_WAITALL（Windows 不可靠），改用循环读取。
        """
        header = TcpTransport._recv_exact(conn, TcpTransport._HEADER.size)
        if header is None or len(header) < TcpTransport._HEADER.size:
            return None
        length = TcpTransport._HEADER.unpack(header)[0]
        if length > 1024 * 1024:  # 1MB 帧上限
            return None
        data = TcpTransport._recv_exact(conn, length)
        if data is None:
            return None
        try:
            return json.loads(data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

    @staticmethod
    def _recv_exact(conn: socket.socket, n: int) -> Optional[bytes]:
        """循环读取，确保收到恰好 n 字节。"""
        buf = bytearray()
        while len(buf) < n:
            try:
                chunk = conn.recv(n - len(buf))
            except OSError:
                return None
            if not chunk:
                return None
            buf.extend(chunk)
        return bytes(buf)


__all__ = ["ConsensusNetwork", "Governance", "TcpTransport", "CONSENSUS_THRESHOLD"]
