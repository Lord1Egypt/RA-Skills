# system/api.py - 服务接口（真实实现，桩转实第 4 步）
# ============================================================
# 职责：暴露系统能力给外部（企业集成面）：
#   - 世界实例生命周期（创世 / tick / 快照）
#   - Agent 操作（spawn / 决策 / 记忆导出）
#   - 经济操作（PoR 查验 / 发行 / 赎回）
#   - 审计查询（25 项报告拉取）
#
# 实现：纯标准库 http.server（无第三方依赖，可横向扩展部署）。
#   鉴权：基于 soul_hash 的 Bearer Token 中间件（可插拔）。
#   前端技术选型：webview 部分可部署到边缘 CDN（React/TS）。
# ============================================================

import base64
import hashlib
import hmac
import json
import logging
import os
import secrets
import select
import socket
import struct
import threading
import time
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, Optional

from .runtime import World
from .keys import load_or_create_key, generate_key, verify_signature
from .ledger import is_hex64

logger = logging.getLogger(__name__)

# WebSocket 握手魔术串（RFC 6455）
_WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

# 无需鉴权的公开路由
# 注：spawn（创世注册）公开，因为它自带公钥签名证明——无效证明在
# runtime 层被拒；有效证明即自证所有权，匿名注册新灵魂无安全危害。
_PUBLIC_ROUTES = {
    ("GET", "/health"),
    ("POST", "/agent/spawn"),
    ("POST", "/auth/challenge"),
    ("POST", "/auth/issue"),
    ("GET", "/protocol/schemas"),
    ("POST", "/protocol/validate"),
    # 账户抽象：会话密钥自主鉴权（挑战-响应签名），无需主身份 token——
    # 主私钥不在线是账户抽象的设计前提。key_id 本身不泄密。
    ("POST", "/aa/challenge"),
    ("POST", "/aa/execute"),
}


def _safe_float(value, default: float = 0.0) -> Optional[float]:
    """安全转 float，失败返回 None（供调用方区分 0 和非法值）。"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _ws_accept(key: str) -> str:
    """计算 Sec-WebSocket-Accept 响应值。"""
    return base64.b64encode(
        hashlib.sha1((key + _WS_GUID).encode("utf-8")).digest()
    ).decode("ascii")


def _ws_frame(text: str) -> bytes:
    """编码一条服务端 -> 客户端文本帧（FIN=1, opcode=0x1, 无掩码）。"""
    data = text.encode("utf-8")
    header = bytearray([0x81])  # FIN + text
    n = len(data)
    if n < 126:
        header.append(n)
    elif n < 65536:
        header.append(126)
        header += struct.pack(">H", n)
    else:
        header.append(127)
        header += struct.pack(">Q", n)
    return bytes(header) + data


def _ws_close_frame() -> bytes:
    """关闭帧（opcode=0x8）。"""
    return b"\x88\x00"


def _ws_read_frame(rfile) -> Optional[Dict]:
    """读取一条客户端 -> 服务端 WebSocket 帧（RFC 6455）。

    返回 {"type": "text"|"close"|"ping", "data": str} 或 None（连接关闭）。
    仅解析单帧，不支持分片续帧（虚拟世界推送场景客户端不发分片）。
    """
    try:
        header = rfile.read(2)
        if len(header) < 2:
            return None
        b0, b1 = header[0], header[1]
        opcode = b0 & 0x0F
        masked = bool(b1 & 0x80)
        length = b1 & 0x7F
        if length == 126:
            ext = rfile.read(2)
            length = struct.unpack(">H", ext)[0]
        elif length == 127:
            ext = rfile.read(8)
            length = struct.unpack(">Q", ext)[0]
        mask = rfile.read(4) if masked else b""
        payload = rfile.read(length) if length > 0 else b""
        if masked and payload:
            payload = bytes(payload[i] ^ mask[i % 4] for i in range(len(payload)))
        if opcode == 0x8:  # close
            return {"type": "close", "data": None}
        if opcode == 0x9:  # ping
            return {"type": "ping", "data": None}
        if opcode == 0x1:  # text
            return {"type": "text", "data": payload.decode("utf-8", errors="replace")}
        return {"type": "unknown", "data": None}
    except socket.timeout:
        raise  # 超时向上抛出，由调用方 except socket.timeout 处理（不视为断开）
    except OSError:
        return None


def _b64url(data: bytes) -> str:
    """URL 安全的 base64 编码（去 padding）。"""
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64url_decode(s: str) -> bytes:
    """URL 安全的 base64 解码（补齐 padding）。"""
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


class ChallengeManager:
    """挑战-响应登录管理器：一次性 nonce 签发 + 签名校验。

    负责登录阶段 nonce 的生命周期管理（签发/速率限制/用后即焚）。
    会话 token 由第 2 层 SessionManager 统一管理，此处不涉及。
    """

    def __init__(
        self,
        key: Optional[bytes] = None,
        key_path: Optional[str] = None,
    ):
        if key is None and key_path:
            key = load_or_create_key(key_path)
        if key is None:
            key = generate_key()
        self._key = key
        # 挑战-响应登录：一次性的 nonce（绑灵魂，防重放，5 分钟过期）
        self.challenges: Dict[str, Dict] = {}
        self.challenge_ttl = 300
        # 并发保护：ThreadingHTTPServer 多线程下 challenges 读写加锁
        self._lock = threading.Lock()
        # 速率限制：每 soul 60s 内最多 5 次登录尝试（防暴力破解）
        self._rate_limit: Dict[str, list] = defaultdict(list)
        self._rate_window = 60
        self._rate_max = 5
        # 全局 IP 速率限制：每 IP 60s 内最多 20 次挑战签发（防 per-soul 限流绕过）
        self._ip_rate: Dict[str, list] = defaultdict(list)
        self._ip_rate_window = 60
        self._ip_rate_max = 20
        # IP 注册（Soul 创世）速率：每 IP 24h 内最多 10 次，防 Sybil
        self._spawn_ip_rate: Dict[str, list] = defaultdict(list)
        self._spawn_window = 86400
        self._spawn_max = 10

    def _check_rate(self, soul_hash: str) -> bool:
        """检查速率限制。返回 True 表示允许，False 表示超限。"""
        now = time.time()
        attempts = self._rate_limit[soul_hash]
        # 清理过期记录
        self._rate_limit[soul_hash] = [t for t in attempts if now - t < self._rate_window]
        if len(self._rate_limit[soul_hash]) >= self._rate_max:
            return False
        self._rate_limit[soul_hash].append(now)
        return True

    def _check_ip_rate(self, ip: str) -> bool:
        """全局 IP 速率限制（防遍历 soul_hash 绕过 per-soul 限流）。

        每个 IP 60s 最多 20 次挑战签发——即使攻击者遍历 1M 随机 soul_hash，
        每个新 hash 仍受 IP 维度限制，攻击速率被钉死在 ~20/60s ≈ 0.33/s。
        """
        if not ip:
            return True  # IP 未知时容许（不阻断内部调用）
        now = time.time()
        window = self._ip_rate_window
        self._ip_rate[ip] = [t for t in self._ip_rate[ip] if now - t < window]
        if len(self._ip_rate[ip]) >= self._ip_rate_max:
            return False
        self._ip_rate[ip].append(now)
        return True

    def _check_spawn_ip_rate(self, ip: str) -> bool:
        """创世注册 IP 速率限制：每 IP 24h 最多 10 次新灵魂注册。

        防御 Sybil：单 IP 不能造 >10 个灵魂/天。需要 KYC 邀请或 PoW 进一步放行。
        """
        if not ip:
            return True
        now = time.time()
        window = self._spawn_window
        self._spawn_ip_rate[ip] = [t for t in self._spawn_ip_rate[ip] if now - t < window]
        if len(self._spawn_ip_rate[ip]) >= self._spawn_max:
            return False
        self._spawn_ip_rate[ip].append(now)
        return True

    def issue_challenge(self, soul_hash: str, ip: str = "") -> str:
        """下发一次性 nonce（未绑定的旧 nonce 被覆盖，天然失效）。"""
        if not self._check_rate(soul_hash):
            return None  # per-soul 速率超限
        if not self._check_ip_rate(ip):
            return None  # 全局 IP 速率超限
        nonce = secrets.token_hex(16)
        with self._lock:
            self.challenges[soul_hash] = {
                "nonce": nonce,
                "expires": int(time.time()) + self.challenge_ttl,
            }
        return nonce

    def verify_challenge(
        self, soul_hash: str, nonce: str, signature_b64: str, pubkey: bytes
    ) -> bool:
        """校验挑战-响应签名：一次性、未过期、验签通过，三者缺一即拒。"""
        with self._lock:
            entry = self.challenges.pop(soul_hash, None)  # 一次性：用后即焚
        if not entry or entry["nonce"] != nonce:
            return False
        if entry["expires"] < int(time.time()):
            return False
        try:
            signature = base64.b64decode(signature_b64)
        except Exception:
            return False
        return verify_signature(pubkey, nonce.encode("utf-8"), signature)


class WorldAPI:
    """协议接口：把 World 的能力暴露为 REST 路由。"""

    def __init__(self, world: World):
        self.world = world
        # 挑战-响应 nonce 签名密钥（防篡改）
        key_path = os.path.join(world.storage.data_dir, "challenge_key")
        self.auth = ChallengeManager(key_path=key_path)

    # ---- 路由分发 ----
    def dispatch(
        self, method: str, path: str, body: Dict, token: Optional[str],
        client_ip: str = "",
    ) -> tuple:
        """返回 (status, payload_dict)。"""
        # 有状态会话验证（可撤销）；灵魂未注册则 token 无效；凭证吊销即 token 失效
        soul = self.world.sessions.verify(
            token, credential_vault=self.world.credentials
        )
        if soul is not None and not self.world.soul_ledger.exists(soul):
            soul = None
        logger.info(
            "request method=%s path=%s client_ip=%s soul=%s",
            method,
            path,
            client_ip or "-",
            soul if soul is not None else "-",
        )

        # 无需鉴权：健康检查
        if path == "/health":
            return 200, {"status": "ok", "world_id": self.world.world_id}

        # ---- 鉴权门：非公开路由必须携带有效 token ----
        if (
            soul is None
            and (method, path) not in _PUBLIC_ROUTES
            and not path.startswith("/ws/")
        ):
            return 401, {"error": "authentication required"}

        # ---- 世界生命周期 ----
        if method == "GET" and path == "/world":
            return 200, self._world_state()
        if method == "POST" and path == "/world/tick":
            return 200, self.world.tick()
        if method == "POST" and path == "/world/snapshot":
            return 200, {"snapshot_id": self.world.snapshot()}

        # ---- 审计查询 ----
        if method == "GET" and path == "/audit":
            report = self.world.audit()
            return 200, {"summary": report.summary()}
        if method == "GET" and path == "/audit/full":
            report = self.world.audit()
            return 200, {attr: getattr(report, attr) for attr, _ in report.FIELDS}

        # ---- Agent 操作 ----
        if method == "POST" and path == "/agent/spawn":
            # Sybil 防御：单 IP 24h 内最多 10 次新灵魂注册
            if client_ip and not self.auth._check_spawn_ip_rate(client_ip):
                return 429, {
                    "error": "当前 IP 注册频次超限（24h 最多 10 个灵魂）；"
                             "如需企业级批量注册，请联系协议监护人申请邀请码"
                }
            genesis_proof = body.get("genesis_proof")
            agent = self.world.spawn_agent(
                soul_hash=body.get("soul_hash"),
                genesis_proof=genesis_proof,
                personality=body.get("personality"),
            )
            if agent is None:
                return 400, {
                    "error": "创世证明须含有效公钥签名，且 soul_hash 必须等于公钥指纹"
                }
            return 201, {"soul_hash": agent.soul_hash, "needs": agent.needs}

        if method == "GET" and path.startswith("/agent/"):
            soul_hash = path[len("/agent/") :]
            agent = self.world.npcs.get(soul_hash)
            if agent is None:
                return 404, {"error": "agent not found"}
            return 200, {
                "soul_hash": soul_hash,
                "needs": agent.needs,
                "actions": agent.action_history[-20:],
            }

        if method == "GET" and path.startswith("/memory/"):
            soul_hash = path[len("/memory/") :]
            if soul != soul_hash:
                return 403, {"error": "仅本人可导出自身记忆"}
            mem = self.world.memory_integrity.export_memory(soul_hash)
            return 200, mem

        # ---- 经济操作 ----
        if method == "GET" and path == "/economy/por":
            return 200, {"reserves": self.world.economy.proof_of_reserve_report()}
        if method == "POST" and path == "/economy/issue":
            amount = _safe_float(body.get("amount", 0))
            owner_soul = body.get("owner_soul", "")
            if owner_soul != soul:
                return 403, {"error": "仅可为自己发行锚定资产"}
            if amount is None:
                return 400, {"error": "amount must be a number"}
            # initial_reserve 可选：省略时先发行后补足（law §2.3），提供时 1:1 足额
            initial_reserve = body.get("initial_reserve")
            if initial_reserve is not None:
                initial_reserve = _safe_float(initial_reserve)
            ok = self.world.economy.issue_pegged(
                body.get("asset_id", ""),
                amount,
                owner_soul,
                initial_reserve=initial_reserve,
            )
            return (200 if ok else 400), {"issued": ok}
        if method == "POST" and path == "/economy/deposit":
            amount = _safe_float(body.get("amount", 0))
            asset_id = body.get("asset_id", "")
            if self.world.economy.owner_of(asset_id) != soul:
                return 403, {"error": "仅资产所有者可补足储备"}
            if amount is None:
                return 400, {"error": "amount must be a number"}
            ok = self.world.economy.deposit_reserve(asset_id, amount)
            return (200 if ok else 400), {"deposited": ok}
        if method == "POST" and path == "/economy/redeem":
            amount = _safe_float(body.get("amount", 0))
            soul_hash = body.get("soul_hash", "")
            if soul_hash != soul:
                return 403, {"error": "仅可赎回自己的资产"}
            if amount is None:
                return 400, {"error": "amount must be a number"}
            ok = self.world.economy.redeem(
                body.get("asset_id", ""),
                amount,
                soul,
            )
            if ok:
                return 200, {"redeemed": True}
            # 检查是否是授权延迟
            decision = getattr(self.world.economy, "_last_decision", None)
            if decision:
                return 202, {
                    "redeemed": False,
                    "delayed": True,
                    "op_id": decision["op_id"],
                    "tier": decision["tier"],
                    "execute_at": decision["execute_at"],
                    "required_approve": decision["required_approve"],
                    "message": decision["message"]
                }
            return 400, {"redeemed": False}

        # ---- 鉴权签发（挑战-响应，凭私钥签 nonce，服务端仅验签）----
        if method == "POST" and path == "/auth/challenge":
            soul_hash = body.get("soul_hash", "")
            if not is_hex64(soul_hash):
                return 400, {"error": "soul_hash 必须为 64 位十六进制"}
            if not self.world.soul_ledger.exists(soul_hash):
                return 403, {
                    "error": "soul_hash 未注册到灵魂账本，请先以创世证明创建智能体"
                }
            nonce = self.auth.issue_challenge(soul_hash, ip=client_ip)
            if nonce is None:
                return 429, {"error": "too many login attempts, please try again later"}
            return 200, {"soul_hash": soul_hash, "nonce": nonce, "ttl": 300}
        if method == "POST" and path == "/auth/issue":
            soul_hash = body.get("soul_hash", "")
            nonce = body.get("nonce", "")
            signature = body.get("signature", "")
            if not is_hex64(soul_hash) or not nonce or not signature:
                return 400, {"error": "soul_hash / nonce / signature 均必填"}
            pubkey = self.world.soul_ledger.get_pubkey(soul_hash)
            if pubkey is None:
                return 403, {"error": "灵魂无注册公钥（旧版身份），拒绝签发"}
            if not self.auth.verify_challenge(soul_hash, nonce, signature, pubkey):
                return 403, {"error": "挑战签名校验失败：私钥不匹配或 nonce 已失效"}
            # 设备绑定：access token 携带 pubkey 前 32hex 指纹；
            # 若此设备凭证被 /credentials/revoke，token 立即失效。
            # 自动把创世公钥绑为"primary"凭证（幂等：已存在则不重复创建）。
            import hashlib as _hl
            pubkey_fingerprint = _hl.sha256(pubkey).hexdigest()[:32]
            existing_creds = self.world.credentials.get_credentials(soul_hash)
            already_bound = any(
                _hl.sha256(c["public_key"]).hexdigest()[:32] == pubkey_fingerprint
                and not c["revoked"]
                for c in existing_creds
            )
            if not already_bound:
                self.world.credentials.bind_credential(
                    soul_hash, pubkey, "primary"
                )
            access_token, refresh_token = self.world.sessions.issue(
                soul_hash, pubkey_fingerprint=pubkey_fingerprint
            )
            return 200, {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        # ---- 会话刷新 / 吊销（第2层：有状态 session）----
        if method == "POST" and path == "/auth/refresh":
            refresh_token = body.get("refresh_token", "")
            # 设备指纹可从请求头 X-Device-Pubkey 传入（base64 编码）
            import hashlib as _hl
            import base64 as _b64
            device_pk_b64 = body.get("device_pubkey", "")
            pubkey_fingerprint = ""
            if device_pk_b64:
                try:
                    device_pk = _b64.b64decode(device_pk_b64)
                    pubkey_fingerprint = _hl.sha256(device_pk).hexdigest()[:32]
                except Exception:
                    pubkey_fingerprint = ""
            result = self.world.sessions.refresh(
                refresh_token, pubkey_fingerprint=pubkey_fingerprint
            )
            if result is None:
                return 403, {"error": "refresh token 无效或已过期"}
            access_token, new_refresh = result
            return 200, {"access_token": access_token, "refresh_token": new_refresh}
        if method == "POST" and path == "/auth/revoke":
            if soul is None:
                return 401, {"error": "authentication required"}
            self.world.sessions.revoke(soul)
            return 200, {"revoked": True}

        # ---- 凭证管理（第1层：多设备凭证）----
        if method == "POST" and path == "/credentials/bind":
            if soul is None:
                return 401, {"error": "authentication required"}
            pubkey_b64 = body.get("public_key", "")
            device_label = body.get("device_label", "")
            try:
                pubkey = base64.b64decode(pubkey_b64)
            except Exception:
                return 400, {"error": "public_key 必须为 base64 编码"}
            credential_id = self.world.credentials.bind_credential(
                soul, pubkey, device_label
            )
            return 201, {"credential_id": credential_id}
        if method == "POST" and path == "/credentials/revoke":
            if soul is None:
                return 401, {"error": "authentication required"}
            credential_id = body.get("credential_id", "")
            self.world.credentials.revoke_credential(soul, credential_id)
            return 200, {"revoked": True}
        if method == "GET" and path == "/credentials/list":
            if soul is None:
                return 401, {"error": "authentication required"}
            creds = self.world.credentials.get_credentials(soul)
            creds = [
                {
                    "credential_id": c["credential_id"],
                    "public_key": base64.b64encode(c["public_key"]).decode("ascii"),
                    "device_label": c["device_label"],
                    "revoked": c["revoked"],
                }
                for c in creds
            ]
            return 200, {"credentials": creds}

        # ---- 授权管理（第3层：分级授权）----
        if method == "GET" and path == "/auth/operations":
            if soul is None:
                return 401, {"error": "authentication required"}
            ops = self.world.authorization.get_pending_operations(soul_hash=soul)
            return 200, {"operations": ops}
        if method == "POST" and path == "/auth/operations/approve":
            if soul is None:
                return 401, {"error": "authentication required"}
            op_id = body.get("op_id", "")
            ok = self.world.authorization.approve_operation(op_id, soul)
            return (200 if ok else 400), {"approved": ok}
        if method == "POST" and path == "/auth/operations/cancel":
            if soul is None:
                return 401, {"error": "authentication required"}
            op_id = body.get("op_id", "")
            ok = self.world.authorization.cancel_operation(op_id, soul)
            return (200 if ok else 400), {"cancelled": ok}
        if method == "POST" and path == "/auth/operations/process":
            # 仅内部调用，处理到期操作
            ops = self.world.authorization.process_execution_queue()
            # 自动执行赎回操作
            for op in ops:
                if op["op_type"] == "redeem":
                    asset_id = op["payload"].get("asset_id")
                    amount = op["payload"].get("amount")
                    if asset_id and amount:
                        self.world.economy.redeem(asset_id, amount, op["soul_hash"])
            return 200, {"executed": len(ops)}

        # ---- 恢复（第4层：社交恢复 + 时间锁）----
        if method == "POST" and path == "/recovery/guardian/add":
            if soul is None:
                return 401, {"error": "authentication required"}
            guardian_soul = body.get("guardian_soul", "")
            self.world.recovery.add_guardian(soul, guardian_soul)
            return 200, {"added": True}
        if method == "POST" and path == "/recovery/initiate":
            if soul is None:
                return 401, {"error": "authentication required"}
            new_public_key = body.get("new_public_key", "")
            request_id = self.world.recovery.initiate_recovery(soul, new_public_key)
            return 201, {"request_id": request_id}
        if method == "POST" and path == "/recovery/approve":
            if soul is None:
                return 401, {"error": "authentication required"}
            request_id = body.get("request_id", "")
            ok = self.world.recovery.approve_recovery(request_id, soul)
            return (200 if ok else 403), {"approved": ok}
        if method == "POST" and path == "/recovery/cancel":
            if soul is None:
                return 401, {"error": "authentication required"}
            request_id = body.get("request_id", "")
            self.world.recovery.cancel_recovery(request_id)
            return 200, {"cancelled": True}
        if method == "POST" and path == "/recovery/finalize":
            if soul is None:
                return 401, {"error": "authentication required"}
            request_id = body.get("request_id", "")
            credential_id = self.world.recovery.finalize_recovery(request_id)
            if credential_id is None:
                return 403, {"error": "恢复未就绪：时间锁未到期或票数不足"}
            return 200, {"credential_id": credential_id}

        # 恢复警报（第4层增强：恢复发起时通知守护者+关联设备）
        if method == "GET" and path == "/recovery/alerts":
            if soul is None:
                return 401, {"error": "authentication required"}
            # 仅本人可查自己的恢复警报（防信息泄露）
            alerts = [
                a for a in self.world._recovery_alerts
                if a["soul_hash"] == soul
            ]
            return 200, {"alerts": alerts, "count": len(alerts)}
        if method == "DELETE" and path == "/recovery/alerts":
            if soul is None:
                return 401, {"error": "authentication required"}
            # 已读后清除本人的警报（按 request_id 精确清除）
            request_id = body.get("request_id", "")
            before = len(self.world._recovery_alerts)
            self.world._recovery_alerts = [
                a for a in self.world._recovery_alerts
                if not (a["soul_hash"] == soul and a["request_id"] == request_id)
            ]
            removed = before - len(self.world._recovery_alerts)
            return 200, {"removed": removed}

        # ---- 账户抽象（升级版账户层：会话密钥授权日常操作）----
        if method == "POST" and path == "/aa/keys/issue":
            if soul is None:
                return 401, {"error": "authentication required"}
            pubkey_b64 = body.get("public_key", "")
            try:
                base64.b64decode(pubkey_b64)
            except Exception:
                return 400, {"error": "public_key 必须为 base64 编码的会话密钥公钥"}
            actions = body.get("allowed_actions")
            if actions is not None and not isinstance(actions, list):
                return 400, {"error": "allowed_actions 必须为字符串数组"}
            sk = self.world.account_abstraction.issue_session_key(
                soul_hash=soul,
                public_key_b64=pubkey_b64,
                spend_limit=_safe_float(body.get("spend_limit")) or None,
                duration_seconds=body.get("duration_seconds"),
                allowed_actions=set(actions) if actions else None,
            )
            return 201, sk.to_dict()
        if method == "GET" and path == "/aa/keys":
            if soul is None:
                return 401, {"error": "authentication required"}
            keys = self.world.account_abstraction.list_session_keys(
                soul, include_inactive=True
            )
            return 200, {"session_keys": [k.to_dict() for k in keys]}
        if method == "POST" and path == "/aa/keys/revoke":
            if soul is None:
                return 401, {"error": "authentication required"}
            if body.get("all"):
                count = self.world.account_abstraction.revoke_all_session_keys(soul)
                return 200, {"revoked_all": True, "count": count}
            key_id = body.get("key_id", "")
            ok = self.world.account_abstraction.revoke_session_key(key_id, soul)
            return (200 if ok else 404), {"revoked": ok}
        if method == "POST" and path == "/aa/challenge":
            # 公开路由：会话密钥持有者凭私钥签 nonce 自证（主身份不在线）
            key_id = body.get("key_id", "")
            sk = self.world.account_abstraction.get_session_key(key_id)
            if sk is None:
                return 404, {"error": "session key not found"}
            nonce = self.auth.issue_challenge(key_id, ip=client_ip)
            if nonce is None:
                return 429, {"error": "too many attempts, please try again later"}
            return 200, {"key_id": key_id, "nonce": nonce, "ttl": 300}
        if method == "POST" and path == "/aa/execute":
            # 公开路由：nonce 挑战签名 + 三重约束（额度/时效/范围）校验
            key_id = body.get("key_id", "")
            sk = self.world.account_abstraction.get_session_key(key_id)
            if sk is None:
                return 404, {"error": "session key not found"}
            try:
                sk_pubkey = base64.b64decode(sk.public_key_b64)
            except Exception:
                return 500, {"error": "session key pubkey corrupt"}
            if not self.auth.verify_challenge(
                key_id, body.get("nonce", ""), body.get("signature", ""), sk_pubkey
            ):
                return 403, {"error": "会话密钥挑战校验失败：签名无效或 nonce 已用"}
            action = body.get("action", "")
            amount = _safe_float(body.get("amount", 0)) or 0.0
            valid, reason, _ = self.world.account_abstraction.validate_session_key(
                key_id, action, amount
            )
            if not valid:
                return 403, {"error": reason}
            self.world.account_abstraction.consume_session_key(key_id, amount)
            sk = self.world.account_abstraction.get_session_key(key_id)
            return 200, {
                "executed": True,
                "action": action,
                "amount": amount,
                "spent_amount": sk.spent_amount,
                "remaining_limit": max(0.0, sk.spend_limit - sk.spent_amount),
                "status": sk.status,
            }

        # ---- 服务端签名密钥轮换（key_rotation 管理）----
        # 注：当前无角色权限模型，任何登录灵魂可调用；生产部署应叠加
        # 管理员角色门禁（待 authorization 层扩展）。
        if method == "GET" and path == "/keys":
            if soul is None:
                return 401, {"error": "authentication required"}
            keys = self.world.key_rotation.list_keys(include_revoked=True)
            return 200, {"keys": [k.to_dict() for k in keys]}  # 不含密钥材料
        if method == "POST" and path == "/keys/rotate":
            if soul is None:
                return 401, {"error": "authentication required"}
            rk = self.world.key_rotation.rotate()
            return 200, {"rotated": rk.to_dict()}
        if method == "POST" and path == "/keys/revoke":
            if soul is None:
                return 401, {"error": "authentication required"}
            key_id = body.get("key_id", "")
            ok = self.world.key_rotation.revoke_key(key_id)
            if not ok:
                return 404, {"error": "key not found"}
            return 200, {
                "revoked": True,
                "note": "该密钥签发的全部 access token 即刻失效",
            }

        # ---- 身份根（第 0 层：主密钥 + Shamir 分片）----
        if method == "POST" and path == "/identity/root/generate":
            if soul is None:
                return 401, {"error": "authentication required"}
            try:
                result = self.world.create_identity_root(
                    threshold=int(body.get("threshold", 3)),
                    num_shares=int(body.get("num_shares", 5)),
                )
            except ValueError as e:
                return 400, {"error": str(e)}
            result["warning"] = (
                "分片经网络返回，仅适用于无安全区的薄客户端；"
                "有能力时应在本设备本地生成（identity_root.IdentityRoot）。"
                "请离线分开保存各分片。"
            )
            return 200, result

        # ---- 灵魂漫游（跨世界身份互认）----
        if method == "POST" and path == "/roaming/worlds/register":
            if soul is None:
                return 401, {"error": "authentication required"}
            world_id = body.get("world_id", "")
            pubkey_b64 = body.get("public_key", "")
            if not world_id:
                return 400, {"error": "world_id 必填"}
            try:
                pubkey = base64.b64decode(pubkey_b64)
            except Exception:
                return 400, {"error": "public_key 必须为 base64 编码"}
            self.world.roaming.register_world(world_id, pubkey)
            return 201, {"registered": world_id}
        if method == "POST" and path == "/roaming/certificates":
            if soul is None:
                return 401, {"error": "authentication required"}
            target_world_id = body.get("target_world_id", "")
            if not target_world_id:
                return 400, {"error": "target_world_id 必填"}
            pubkey = self.world.soul_ledger.get_pubkey(soul)
            if pubkey is None:
                return 403, {"error": "灵魂无注册公钥，无法签发漫游证书"}
            cert = self.world.roaming.issue_roaming_certificate(
                soul_hash=soul,
                target_world_id=target_world_id,
                identity_proof={
                    "pubkey_b64": base64.b64encode(pubkey).decode("ascii"),
                    "soul_hash_in_source": soul,
                },
                memory_manifest=body.get("memory_manifest"),
                ttl_seconds=body.get("ttl_seconds"),
            )
            return 201, {"certificate": cert.to_dict()}
        if method == "POST" and path == "/roaming/verify":
            if soul is None:
                return 401, {"error": "authentication required"}
            cert_dict = body.get("certificate")
            if not isinstance(cert_dict, dict):
                return 400, {"error": "certificate 必填（证书字典）"}
            try:
                from .soul_roaming import SoulRoamingCertificate

                cert = SoulRoamingCertificate.from_dict(cert_dict)
            except (KeyError, TypeError):
                return 400, {"error": "证书结构不完整"}
            sig_b64 = body.get("challenge_signature", "")
            nonce = body.get("challenge_nonce", "")
            valid, reason = self.world.roaming.verify_roaming_certificate(
                cert,
                user_challenge_signature=base64.b64decode(sig_b64) if sig_b64 else None,
                challenge_nonce=nonce.encode("utf-8") if nonce else None,
            )
            return 200, {"valid": valid, "reason": reason}
        if method == "POST" and path == "/roaming/map":
            if soul is None:
                return 401, {"error": "authentication required"}
            cert_dict = body.get("certificate")
            local_soul_hash = body.get("local_soul_hash", "")
            if not isinstance(cert_dict, dict) or not local_soul_hash:
                return 400, {"error": "certificate 与 local_soul_hash 必填"}
            if local_soul_hash != soul:
                return 403, {"error": "仅可映射到本人本地灵魂"}
            try:
                from .soul_roaming import SoulRoamingCertificate

                cert = SoulRoamingCertificate.from_dict(cert_dict)
            except (KeyError, TypeError):
                return 400, {"error": "证书结构不完整"}
            valid, reason = self.world.roaming.verify_roaming_certificate(cert)
            if not valid:
                return 403, {"error": f"证书验证失败：{reason}"}
            self.world.roaming.map_roaming_soul(cert, local_soul_hash)
            return 201, {"mapped": True}
        if method == "POST" and path == "/roaming/mapping/lookup":
            if soul is None:
                return 401, {"error": "authentication required"}
            local = self.world.roaming.get_local_soul_hash(
                body.get("source_world_id", ""), body.get("source_soul_hash", "")
            )
            if local is None:
                return 404, {"error": "no mapping found"}
            return 200, {"local_soul_hash": local}

        # ---- 互认协议 ----
        if method == "GET" and path == "/protocol/schemas":
            from .protocol import SCHEMAS

            return 200, SCHEMAS
        if method == "POST" and path == "/protocol/validate":
            from .protocol import ProtocolValidator

            ok, failures = ProtocolValidator().validate(body.get("world_config", {}))
            return (200 if ok else 422), {"passed": ok, "failures": failures}

        return 404, {"error": f"unknown route: {method} {path}"}

    def stream_snapshot(self) -> Dict:
        """WebSocket 实时流：每次推送的世界状态快照。"""
        return self._world_state()

    def _world_state(self) -> Dict:
        w = self.world
        return {
            "world_id": w.world_id,
            "genesis_completed": w.genesis_completed,
            "clock": w.temporal_substrate.global_clock,
            "souls": len(w.soul_ledger.souls),
            "agents": list(w.npcs.keys()),
            "consensus_nodes": list(w.consensus.nodes.keys()),
            "oracle_sources": w.economy.oracle_sources,
        }


class _Handler(BaseHTTPRequestHandler):
    api: WorldAPI = None  # 由 serve() 注入

    def _client_ip(self) -> str:
        """取客户端 IP（优先反向代理 X-Forwarded-For；否则直连地址）。"""
        fwd = self.headers.get("X-Forwarded-For", "")
        if fwd:
            return fwd.split(",")[0].strip()
        return self.client_address[0] if self.client_address else ""

    def _respond(self, status: int, payload: Dict) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _route(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
        except (json.JSONDecodeError, ValueError, TypeError):
            body = {}
        token = self.headers.get("Authorization")
        client_ip = self._client_ip()
        try:
            status, payload = self.api.dispatch(
                self.command, self.path, body, token, client_ip
            )
        except (ValueError, TypeError) as e:
            status, payload = 400, {"error": f"invalid input: {e}"}
        self._respond(status, payload)

    def do_GET(self):
        # WebSocket 升级：/ws/world 实时世界流
        if (
            self.path == "/ws/world"
            and self.headers.get("Upgrade", "").lower() == "websocket"
        ):
            self._ws_stream()
            return
        self._route()

    def do_POST(self):
        self._route()

    def _ws_stream(self) -> None:
        """WebSocket 握手 + 持久事件循环。

        客户端连接后持续推送世界状态快照（默认每 1s 一帧），
        直到客户端断开或发送 close 帧。
        客户端可发送 JSON 消息控制推送行为：
          {"action": "subscribe", "events": ["world_state", "audit"]}
          {"action": "unsubscribe", "events": ["audit"]}
          {"action": "ping"}
        """
        try:
            key = self.headers.get("Sec-WebSocket-Key", "")
            self.send_response(101, "Switching Protocols")
            self.send_header("Upgrade", "websocket")
            self.send_header("Connection", "Upgrade")
            self.send_header("Sec-WebSocket-Accept", _ws_accept(key))
            self.end_headers()

            subscribed_events = {"world_state"}  # 默认订阅世界状态
            push_interval = 1.0  # 推送间隔（秒）
            last_push = 0.0

            while True:
                # 非阻塞检查客户端是否有数据可读（select 超时 0.1s）
                # 用 select 而非 socket.settimeout，彻底区分"超时无数据"和"连接断开"
                try:
                    readable, _, _ = select.select([self.connection], [], [], 0.1)
                except (OSError, ValueError):
                    break  # socket 已关闭
                if readable:
                    try:
                        msg = _ws_read_frame(self.rfile)
                        if msg is None:
                            break  # 客户端关闭（read 返回空）
                        if msg.get("type") == "close":
                            break
                        payload = msg.get("data")
                        if payload:
                            try:
                                cmd = json.loads(payload)
                                action = cmd.get("action", "")
                                if action == "subscribe":
                                    events = cmd.get("events", [])
                                    subscribed_events.update(events)
                                elif action == "unsubscribe":
                                    events = cmd.get("events", [])
                                    subscribed_events -= set(events)
                                elif action == "ping":
                                    self.wfile.write(_ws_frame(json.dumps({"type": "pong"})))
                                    self.wfile.flush()
                                elif action == "set_interval":
                                    push_interval = max(0.1, min(60.0, cmd.get("interval", 1.0)))
                            except (json.JSONDecodeError, TypeError):
                                pass
                    except socket.timeout:
                        pass  # 无入站消息，继续推送
                    except (BrokenPipeError, ConnectionResetError, OSError):
                        break  # 客户端断开

                # 周期性推送
                now = time.time()
                if now - last_push >= push_interval:
                    snapshot = self.api.stream_snapshot()
                    snapshot["event"] = "world_state"
                    if "audit" in subscribed_events:
                        snapshot["audit"] = self.api.world.audit_summary()
                    self.wfile.write(_ws_frame(json.dumps(snapshot, ensure_ascii=False)))
                    self.wfile.flush()
                    last_push = now

            self.wfile.write(_ws_close_frame())
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass  # 客户端断开或握手失败，静默结束

    def log_message(self, *args):
        pass  # 静默访问日志（企业服务避免噪声）


def serve(
    world: World,
    host: str = "127.0.0.1",
    port: int = 8000,
    tls_certfile: Optional[str] = None,
    tls_keyfile: Optional[str] = None,
    require_tls: bool = False,
):
    """启动 REST 服务（阻塞）。每次调用创建独立 Handler 类，支持多世界并行。

    安全参数：
      tls_certfile / tls_keyfile  两者同时提供时启用 HTTPS（ssl.wrap_socket）
      require_tls                 True 时若未启用 TLS 直接拒绝启动
                                  （生产部署：保护 access token / 签名挑战
                                   不在明文 HTTP 上传输）

    警告：仅本机或受控内网（host=127.0.0.1）默认安全；对外暴露必须走反向
    代理（nginx/Caddy）终结 TLS，或在此函数提供 tls_certfile/tls_keyfile。
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    api = WorldAPI(world)

    class _WorldHandler(_Handler):
        pass

    _WorldHandler.api = api
    use_tls = bool(tls_certfile and tls_keyfile)
    if require_tls and not use_tls:
        raise RuntimeError(
            "require_tls=True 但未提供 tls_certfile/tls_keyfile；"
            "明文 HTTP 禁止用于生产部署（access token / 签名挑战将裸奔）"
        )
    server = ThreadingHTTPServer((host, port), _WorldHandler)
    if use_tls:
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=tls_certfile, keyfile=tls_keyfile)
        server.socket = context.wrap_socket(server.socket, server_side=True)
        scheme = "https"
    else:
        scheme = "http"
        if host not in ("127.0.0.1", "localhost", "::1"):
            print(
                f"[system/api] ⚠ 警告：监听 {host} 但未启用 TLS；"
                "access_token / 签名挑战将以明文传输，"
                "生产部署必须前置反向代理或提供 tls_certfile/tls_keyfile",
                flush=True,
            )
    print(f"[system/api] serving world '{world.world_id}' at {scheme}://{host}:{port}")
    logger.info("serve start world_id=%s scheme=%s host=%s port=%d", world.world_id, scheme, host, port)
    server.serve_forever()


__all__ = ["WorldAPI", "ChallengeManager", "serve"]
