# system/edge_sdk.py - AR 眼镜聚合端口（地平线三·接入层）
# ============================================================
# 职责：把全球分布式部署的世界，聚合成面向 AR 眼镜的单一轻量接入面。
#   定位是"被嵌入的白标 SDK"而非消费级入口：各家巨头/政府的世界 App
#   内嵌本 SDK，身份/资产/空间在底层互通——App 入口各家做，互通协议我们做。
#
# 眼镜是灵魂的"窗口"，不是灵魂本身：每副眼镜只是六层账户体系里的
# 一个设备凭证（Layer 1），绑定到 soul_hash。换眼镜 = 吊销旧设备 +
# 绑定新设备，灵魂/资产/记忆不变。服务端只存设备公钥，私钥永驻
# 眼镜安全区（内存态，不上传、不落盘）。
#
# 三个职责（全部复用既有组件，本模块只做编排，不发明新概念）：
#   1. 设备凭证登记  眼镜首启生成密钥对，公钥绑定灵魂
#                    → 复用 Layer 1 credentials.bind_credential
#   2. 就近接入      按终端地理坐标路由到最近 DC / Geo-Shard
#                    → 复用 spatial_sharding.ShardRouter.dc_of
#   3. 视口流        只推 AOI 关注域内增量，DC 间移动无缝切换
#                    → 复用 aoi_sync.DeltaSync + runtime.agents_near / move_agent
#
# 依赖方向：edge_sdk -> credentials / sessions / aoi_sync / keys（单向，
#   不反向 import runtime；World 由调用方注入）。
# ============================================================

import base64
import hashlib
import logging
import time
from typing import Dict, List, Optional

from . import keys
from .aoi_sync import DeltaSync

logger = logging.getLogger(__name__)


class EdgeDevice:
    """眼镜端设备身份（SDK 侧模型）。

    私钥仅驻留眼镜安全区（内存态），任何路径均不得落盘/上传；
    服务端只接触公钥与签名。
    """

    def __init__(self, label: str = "ar_glasses"):
        kp = keys.generate_user_keypair()
        self.secret = kp["secret"]
        self.pubkey = kp["pubkey"]
        self.label = label
        self.credential_id: Optional[str] = None

    def soul_hash(self) -> str:
        """本设备自身的 soul_hash（SHA-256(公钥)）。"""
        return keys.derive_soul_hash_from_pubkey(self.pubkey)

    def sign(self, message: bytes) -> bytes:
        """眼镜安全区签名（等价生物识别在场确认后触发）。"""
        return keys.sign_with_device(self.secret, message)

    def verify(self, message: bytes, signature: bytes) -> bool:
        return keys.verify_signature(self.pubkey, message, signature)

    def pubkey_b64(self) -> str:
        return base64.b64encode(self.pubkey).decode("ascii")

    def fingerprint(self) -> str:
        """公钥指纹（SHA-256 前 32 hex，绑定到 access token）。"""
        return hashlib.sha256(self.pubkey).hexdigest()[:32]


class EdgeSdk:
    """AR 眼镜聚合端口（服务端接入层）。

    由 runtime.World 装配（world.edge），世界 App 通过本接口完成
    设备绑定 / 就近路由 / 视口订阅，无需理解跨 DC 内部细节。
    """

    def __init__(self, world):
        self.world = world
        # 设备登记表：credential_id -> 设备运行时状态（位置 / 就近 DC / 最近在线）
        self.devices: Dict[str, Dict] = {}
        # 视口增量基线：soul_hash -> 上次推送的全量视口（用于差分）
        self._viewport_cache: Dict[str, Dict] = {}

    # ----------------------------------------------------------
    # 职责 1：设备凭证登记（眼镜 = 灵魂的一个窗口）
    # ----------------------------------------------------------

    def register_device(
        self,
        soul_hash: str,
        device_pubkey: bytes,
        label: str = "ar_glasses",
        position: Optional[List[float]] = None,
    ) -> str:
        """把一副 AR 眼镜绑定到灵魂。

        复用 Layer 1 credentials：服务端只存公钥。返回 credential_id；
        换眼镜 = revoke_device(旧 id) + register_device(新公钥)，灵魂不变。
        """
        if len(device_pubkey) != 32:
            raise ValueError("device_pubkey 必须为 32 字节原始 Ed25519 公钥")
        credential_id = self.world.credentials.bind_credential(
            soul_hash, device_pubkey, label
        )
        self.devices[credential_id] = {
            "soul_hash": soul_hash,
            "label": label,
            "position": list(position) if position else None,
            "dc": self.nearest_dc(position) if position else self.world.local_dc,
            "last_seen": time.time(),
            "revoked": False,
        }
        logger.info(
            "edge device bound soul=%s label=%s dc=%s",
            soul_hash[:16], label,
            self.devices[credential_id]["dc"],
        )
        return credential_id

    def revoke_device(self, credential_id: str) -> bool:
        """吊销设备凭证（丢眼镜/被窃后一键踢下线，关联 token 立即失效）。"""
        ok = False
        for soul_hash in self._device_owner(credential_id):
            self.world.credentials.revoke_credential(soul_hash, credential_id)
            ok = True
        if credential_id in self.devices:
            self.devices[credential_id]["revoked"] = True
        logger.info("edge device revoked id=%s", credential_id[:8])
        return ok

    def _device_owner(self, credential_id: str) -> List[str]:
        """反查凭证属主（device 表优先，回落到 credentials 全量扫描）。"""
        if credential_id in self.devices:
            return [self.devices[credential_id]["soul_hash"]]
        owners = []
        for soul_hash in list(self.world.soul_ledger.souls.keys()):
            for c in self.world.credentials.get_credentials(soul_hash):
                if c["credential_id"] == credential_id:
                    owners.append(soul_hash)
        return owners

    def device_status(self, credential_id: str) -> Optional[Dict]:
        """查询设备运行时状态（位置 / 就近 DC / 在线时间）。"""
        info = self.devices.get(credential_id)
        if info is None:
            return None
        return {
            "credential_id": credential_id,
            "soul_hash": info["soul_hash"],
            "label": info["label"],
            "position": info["position"],
            "dc": info["dc"],
            "last_seen": info["last_seen"],
            "revoked": info["revoked"],
        }

    # ----------------------------------------------------------
    # 职责 2：就近接入（地理坐标 → 最近 DC）
    # ----------------------------------------------------------

    def nearest_dc(self, position: List[float]) -> str:
        """按终端地理坐标返回最近 DC（经 Geo-Shard 路由表）。

        position 为虚拟世界坐标；Geo-Shard 按包围盒归属 DC，
        无匹配时回落本节点 local_dc（单机形态恒为 dc_local）。
        """
        if position is None:
            return self.world.local_dc
        dc = self.world.shard_manager.router.dc_of(position)
        return dc or self.world.local_dc

    def shard_of(self, position: List[float]) -> Optional[str]:
        """返回坐标所在 Geo-Shard ID（供状态/日志展示）。"""
        return self.world.shard_manager.router.shard_of(position)

    # ----------------------------------------------------------
    # 职责 3：视口流（AOI 关注域内增量，不推全量世界）
    # ----------------------------------------------------------

    def viewport(self, soul_hash: str, origin: Optional[List[float]] = None,
                 radius: float = 100.0) -> Dict[str, Dict]:
        """当前 AOI 视口快照：origin 周围 radius 内全部实体位置。

        origin 缺省取该灵魂自身坐标（眼镜以本人为视口中心）。
        复用 runtime.agents_near 的空间网格索引，O(局部候选) 而非 O(N)。
        """
        if origin is None:
            origin = self.world.position_of(soul_hash)
        nearby = self.world.agents_near(origin, radius)
        return {
            s: {"position": self.world.position_of(s)}
            for s in nearby
        }

    def viewport_delta(self, soul_hash: str, origin: Optional[List[float]] = None,
                       radius: float = 100.0) -> Dict:
        """AOI 增量推送：相对上次快照只发 changed/added/removed。

        返回 {added, removed, changed, bits, data}；bits=0 表示无变化
        （眼镜端静默，不刷屏、不费电）。
        """
        current = self.viewport(soul_hash, origin, radius)
        last = self._viewport_cache.get(soul_hash, {})
        delta = DeltaSync.diff(current, last)
        if delta["bits"]:
            touched = delta["added"] + delta["changed"]
            delta["data"] = {s: current[s] for s in touched}
            self._viewport_cache[soul_hash] = current
        return delta

    def relocate(self, soul_hash: str, new_pos: List[float]) -> bool:
        """眼镜（灵魂）移动到新坐标：更新位置 + 就地 DC。

        跨 Geo-Shard 边界时复用 runtime.move_agent 的 Handover 握手
        完成状态锁转移，眼镜无感（无需重连）。
        """
        ok = self.world.move_agent(soul_hash, new_pos)
        if ok:
            self._viewport_cache.pop(soul_hash, None)  # 视口中心变了，基线作废
            for info in self.devices.values():
                if info["soul_hash"] == soul_hash:
                    info["position"] = list(new_pos)
                    info["dc"] = self.nearest_dc(new_pos)
                    info["last_seen"] = time.time()
        return ok

    # ----------------------------------------------------------
    # 设备会话（复用 Layer 2 sessions：挑战-响应，私钥不上传）
    # ----------------------------------------------------------

    def login(self, soul_hash: str, nonce: str, signature: bytes,
              device_pubkey: bytes) -> Optional[tuple]:
        """眼镜登录：服务端验签 nonce，签成后签发 access+refresh。

        返回 (access_token, refresh_token) 或 None。
        access token 绑定该设备公钥指纹——吊销设备后立即失效。
        """
        if not keys.verify_signature(device_pubkey, nonce.encode("utf-8"), signature):
            return None
        fingerprint = hashlib.sha256(device_pubkey).hexdigest()[:32]
        # 设备必须已登记为该灵魂的凭证（否则伪造公钥即可冒领会话）
        creds = self.world.credentials.get_credentials(soul_hash)
        if not any(
            hashlib.sha256(c["public_key"]).hexdigest()[:32] == fingerprint
            and not c["revoked"]
            for c in creds
        ):
            return None
        return self.world.sessions.issue(soul_hash, fingerprint)


__all__ = ["EdgeDevice", "EdgeSdk"]
