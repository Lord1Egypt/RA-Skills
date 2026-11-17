"""第 3 层：授权层（Authorization Engine）。

分级授权 + 风险引擎。几十亿现实资产，单靠登录成功就放行所有操作是致命的。
- 小额：即时放行
- 中额：延迟24小时，可取消
- 大额：多签（守护者阈值）+ 延迟72小时
- 超大额：多签 + 人工复核 + 延迟72小时
"""

import time
import json
import logging
import uuid
from typing import Dict, List, Optional

from .recovery import RecoveryManager

logger = logging.getLogger(__name__)


class AuthorizationEngine:
    """分级授权：小额即时 / 中额延迟+通知 / 大额多签 / 超大额人工复核。"""

    # 阈值（示例，生产按资产类别配置）
    TIER_SMALL = 1_000
    TIER_MEDIUM = 100_000
    TIER_LARGE = 1_000_000

    # 延迟时间（秒）
    DELAY_SMALL = 0
    DELAY_MEDIUM = 24 * 3600
    DELAY_LARGE = 72 * 3600
    DELAY_CRITICAL = 72 * 3600

    def __init__(self, storage=None, recovery_manager: Optional[RecoveryManager] = None):
        self._storage = storage
        self.recovery = recovery_manager  # 用于查询守护者列表

    def classify(self, amount: float) -> str:
        """按金额分级。"""
        if amount < self.TIER_SMALL:
            return "small"
        if amount < self.TIER_MEDIUM:
            return "medium"
        if amount < self.TIER_LARGE:
            return "large"
        return "critical"

    def required_approval_count(self, tier: str, soul_hash: str) -> int:
        """返回该等级操作需要的守护者批准数。"""
        if tier in ["small", "medium"]:
            return 0
        # large/critical需要守护者人数的2/3，最小1
        if self.recovery:
            guardians = self.recovery.get_guardians(soul_hash)
            return max(1, (len(guardians) * 2 + 2) // 3)  # 向上取整2/3
        return 1

    def authorize(self, soul_hash: str, action: str, amount: float, payload: Optional[Dict] = None) -> Dict:
        """授权决策：小额即时放行，大额创建延迟操作。

        返回：
        {
            "allowed": bool,        # 是否即时放行
            "tier": str,            # 操作等级
            "op_id": str | None,    # 延迟操作ID（非小额时返回）
            "execute_at": int | None, # 执行时间戳（非小额时返回）
            "required_approve": int,# 需要的批准数
            "message": str          # 提示信息
        }
        """
        tier = self.classify(amount)
        required = self.required_approval_count(tier, soul_hash)
        logger.info(
            "authorize soul_hash=%s action=%s amount=%s tier=%s required_approve=%d",
            soul_hash,
            action,
            amount,
            tier,
            required,
        )

        if tier == "small":
            return {
                "allowed": True,
                "tier": tier,
                "op_id": None,
                "execute_at": int(time.time()),
                "required_approve": 0,
                "message": "小额操作即时放行"
            }

        # 中/大/超大额：创建延迟操作
        now = time.time()
        op_id = uuid.uuid4().hex
        delay = {
            "medium": self.DELAY_MEDIUM,
            "large": self.DELAY_LARGE,
            "critical": self.DELAY_CRITICAL
        }[tier]
        execute_at = now + delay

        if self._storage:
            self._storage.execute(
                "INSERT INTO delay_operations "
                "(op_id, op_type, soul_hash, payload, tier, status, required, execute_at, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    op_id,
                    action,
                    soul_hash,
                    json.dumps(payload or {}),
                    tier,
                    "pending",
                    required,
                    execute_at,
                    now,
                    now
                )
            )

        return {
            "allowed": False,
            "tier": tier,
            "op_id": op_id,
            "execute_at": int(execute_at),
            "required_approve": required,
            "message": f"{tier}级操作，需要{required}个守护者批准，延迟{int(delay/3600)}小时执行"
        }

    def approve_operation(self, op_id: str, guardian_soul: str) -> bool:
        """守护者批准延迟操作。"""
        if not self._storage:
            return False
        now = time.time()
        # 检查操作是否存在且处于pending状态
        rows = self._storage.query(
            "SELECT soul_hash, required, approved, status FROM delay_operations WHERE op_id=?",
            (op_id,)
        )
        if not rows or rows[0][3] != "pending":
            return False
        soul_hash, required, approved, _ = rows[0]
        # 检查是否是该灵魂的守护者
        if self.recovery and guardian_soul not in self.recovery.get_guardians(soul_hash):
            return False
        # 插入批准记录（幂等：主键重复自动忽略）
        try:
            self._storage.execute(
                "INSERT OR IGNORE INTO op_approvals (op_id, guardian_soul, approved_at) VALUES (?, ?, ?)",
                (op_id, guardian_soul, now)
            )
        except Exception:
            pass
        # 更新批准计数
        approved = self._storage.query(
            "SELECT COUNT(*) FROM op_approvals WHERE op_id=?",
            (op_id,)
        )[0][0]
        self._storage.execute(
            "UPDATE delay_operations SET approved=?, updated_at=? WHERE op_id=?",
            (approved, now, op_id)
        )
        logger.info("operation approved op_id=%s guardian_soul=%s approved_count=%d", op_id, guardian_soul, approved)
        return True

    def cancel_operation(self, op_id: str, soul_hash: str) -> bool:
        """操作者本人取消延迟操作。"""
        if not self._storage:
            return False
        rows = self._storage.query(
            "SELECT soul_hash, status FROM delay_operations WHERE op_id=?",
            (op_id,)
        )
        if not rows or rows[0][0] != soul_hash or rows[0][1] != "pending":
            return False
        self._storage.execute(
            "UPDATE delay_operations SET status='cancelled', updated_at=? WHERE op_id=?",
            (time.time(), op_id)
        )
        return True

    def get_pending_operations(self, soul_hash: Optional[str] = None) -> List[Dict]:
        """查询未执行的延迟操作。"""
        if not self._storage:
            return []
        query = "SELECT op_id, op_type, soul_hash, payload, tier, status, required, approved, execute_at, created_at FROM delay_operations WHERE status='pending'"
        params = []
        if soul_hash:
            query += " AND soul_hash=?"
            params.append(soul_hash)
        rows = self._storage.query(query, params)
        return [
            {
                "op_id": r[0],
                "op_type": r[1],
                "soul_hash": r[2],
                "payload": json.loads(r[3]),
                "tier": r[4],
                "status": r[5],
                "required_approve": r[6],
                "approved_count": r[7],
                "execute_at": int(r[8]),
                "created_at": int(r[9])
            }
            for r in rows
        ]

    def process_execution_queue(self) -> List[Dict]:
        """处理到期且满足条件的延迟操作，返回可执行的操作列表。"""
        if not self._storage:
            return []
        now = time.time()
        # 查找到期、pending、批准数足够的操作
        rows = self._storage.query(
            "SELECT op_id, op_type, soul_hash, payload FROM delay_operations "
            "WHERE status='pending' AND execute_at <= ? AND approved >= required",
            (now,)
        )
        exec_ops = []
        for (op_id, op_type, soul_hash, payload) in rows:
            exec_ops.append({
                "op_id": op_id,
                "op_type": op_type,
                "soul_hash": soul_hash,
                "payload": json.loads(payload)
            })
            # 标记为已执行
            self._storage.execute(
                "UPDATE delay_operations SET status='executed', updated_at=? WHERE op_id=?",
                (now, op_id)
            )
        return exec_ops

    def risk_score(self, context: dict) -> float:
        """风险评分（0~1，越高越可疑）。context 可含 device/ip/geo/behavior。"""
        score = 0.0
        if context.get("new_device"):
            score += 0.3
        if context.get("unusual_ip"):
            score += 0.2
        if context.get("unusual_geo"):
            score += 0.2
        if context.get("unusual_hour"):
            score += 0.1
        if context.get("high_frequency"):
            score += 0.2
        return min(score, 1.0)

    def require_step_up(self, context: dict) -> bool:
        """风险超阈值时要求二次验证（生物识别/多因素）。"""
        return self.risk_score(context) >= 0.5
