"""第 4 层：恢复层（Recovery Manager）。

社交恢复 + 时间锁。化解 non_revocable 与「丢钥匙=资产永久冻结」的矛盾：
灵魂不可撤销，但凭证可安全更换。

增强（阶段1）：
- 恢复发起时全设备警报：通知所有守护者 + 关联设备，时间锁内任何关联设备可撤销
- 可插拔通知回调：webhook / push / 邮件，由上层注入
"""

import base64
import logging
import time
import uuid
from typing import Callable, List, Optional

logger = logging.getLogger(__name__)

# 恢复警报回调签名：(request_id, soul_hash, guardian_souls, timelock_until) -> None
RecoveryAlertCallback = Callable[[str, str, List[str], float], None]


class RecoveryManager:
    """社交恢复：N 守护者 M 同意 + 时间锁（延迟期可取消）。

    增强：恢复发起时触发全设备警报回调；时间锁内任何已绑定凭证的设备可撤销。
    """

    def __init__(
        self,
        storage,
        credential_vault,
        guardian_threshold: int = 3,
        timelock_seconds: int = 7 * 24 * 3600,
    ):
        self._storage = storage
        self._credentials = credential_vault
        self.guardian_threshold = guardian_threshold
        self.timelock_seconds = timelock_seconds
        self._alert_callbacks: List[RecoveryAlertCallback] = []

    # ── 警报回调注册 ──────────────────────────────────────────
    def register_alert_callback(self, callback: RecoveryAlertCallback) -> None:
        """注册恢复警报回调（webhook/push/邮件等）。"""
        self._alert_callbacks.append(callback)

    def _fire_recovery_alert(self, request_id: str, soul_hash: str, timelock_until: float) -> None:
        """触发所有恢复警报回调。"""
        guardians = self.get_guardians(soul_hash)
        for cb in self._alert_callbacks:
            try:
                cb(request_id, soul_hash, guardians, timelock_until)
            except Exception as e:
                logger.warning("recovery alert callback failed: %s", e)
        logger.info(
            "recovery ALERT fired request_id=%s soul_hash=%s guardians=%d callbacks=%d",
            request_id, soul_hash, len(guardians), len(self._alert_callbacks),
        )

    # ── 守护者管理 ────────────────────────────────────────────
    def add_guardian(self, soul_hash: str, guardian_soul: str) -> bool:
        """添加守护者。"""
        self._storage.execute(
            "INSERT OR IGNORE INTO guardians (soul_hash, guardian_soul, created_at) "
            "VALUES (?, ?, ?)",
            (soul_hash, guardian_soul, time.time()),
        )
        return True

    def get_guardians(self, soul_hash: str):
        rows = self._storage.query(
            "SELECT guardian_soul FROM guardians WHERE soul_hash=?", (soul_hash,)
        )
        return [r[0] for r in rows]

    # ── 恢复流程 ──────────────────────────────────────────────
    def initiate_recovery(self, soul_hash: str, new_public_key_b64: str) -> str:
        """发起恢复：创建请求，进入时间锁，触发全设备警报。返回 request_id。"""
        request_id = uuid.uuid4().hex
        now = time.time()
        timelock_until = now + self.timelock_seconds
        self._storage.execute(
            "INSERT INTO recovery_requests "
            "(request_id, soul_hash, new_public_key, created_at, timelock_until, status) "
            "VALUES (?, ?, ?, ?, ?, 'pending')",
            (request_id, soul_hash, new_public_key_b64, now, timelock_until),
        )
        logger.info("recovery initiated request_id=%s soul_hash=%s timelock=%ds",
                     request_id, soul_hash, self.timelock_seconds)
        # 触发全设备警报（守护者 + 关联设备）
        self._fire_recovery_alert(request_id, soul_hash, timelock_until)
        return request_id

    def approve_recovery(self, request_id: str, guardian_soul: str) -> bool:
        """守护者投票。非守护者无权投票。"""
        rows = self._storage.query(
            "SELECT soul_hash, status FROM recovery_requests WHERE request_id=?",
            (request_id,),
        )
        if not rows or rows[0][1] != "pending":
            return False
        soul_hash = rows[0][0]
        if guardian_soul not in self.get_guardians(soul_hash):
            return False
        self._storage.execute(
            "INSERT OR IGNORE INTO recovery_votes (request_id, guardian_soul, ts) "
            "VALUES (?, ?, ?)",
            (request_id, guardian_soul, time.time()),
        )
        logger.info("recovery vote cast request_id=%s guardian_soul=%s votes=%d",
                    request_id, guardian_soul, self.vote_count(request_id))
        return True

    def vote_count(self, request_id: str) -> int:
        rows = self._storage.query(
            "SELECT COUNT(*) FROM recovery_votes WHERE request_id=?", (request_id,)
        )
        return rows[0][0] if rows else 0

    def cancel_recovery(self, request_id: str, soul_hash: Optional[str] = None) -> bool:
        """原设备在时间锁内取消。增强：任何已绑定该灵魂的设备均可撤销。

        如果传入 soul_hash，验证该灵魂确实有已绑定凭证（关联设备撤销）。
        """
        if soul_hash:
            # 验证该灵魂有已绑定凭证（即有关联设备）
            creds = self._credentials.get_credentials(soul_hash)
            if not creds:
                logger.warning("cancel_recovery rejected: soul_hash=%s has no bound credentials", soul_hash)
                return False
        self._storage.execute(
            "UPDATE recovery_requests SET status='cancelled' "
            "WHERE request_id=? AND status='pending'",
            (request_id,),
        )
        logger.info("recovery cancelled request_id=%s by soul_hash=%s", request_id, soul_hash or "unknown")
        return True

    def finalize_recovery(self, request_id: str):
        """时间锁到期 + 票数达标 → 换新凭证。返回新 credential_id 或 None。

        关键路径用 storage.transaction() 包为原子操作：vote_count + bind_credential
        + status update 全部成功才提交；任一失败整体回滚，杜绝"半完成恢复"状态。
        """
        rows = self._storage.query(
            "SELECT soul_hash, new_public_key, timelock_until, status "
            "FROM recovery_requests WHERE request_id=?",
            (request_id,),
        )
        if not rows:
            return None
        soul_hash, new_public_key_b64, timelock_until, status = rows[0]
        if status != "pending":
            return None
        if time.time() < timelock_until:
            return None  # 时间锁未到期
        if self.vote_count(request_id) < self.guardian_threshold:
            return None  # 票数不足
        try:
            with self._storage.transaction():
                pubkey = base64.b64decode(new_public_key_b64)
                # bind_credential 在事务内落库；回滚时新凭证不会被持久化
                credential_id = self._credentials.bind_credential(
                    soul_hash, pubkey, "recovered"
                )
                self._storage.execute(
                    "UPDATE recovery_requests SET status='finalized' WHERE request_id=?",
                    (request_id,),
                )
        except Exception:
            return None
        return credential_id
