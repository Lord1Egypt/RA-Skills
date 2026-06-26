# -*- coding: utf-8 -*-
"""
skill-evolve-pro · Phase 2
RolloutResult 数据类：单次任务执行的轨迹记录

基于 ReflACT 框架的标准化轨迹格式，兼容 SkillOpt types.RolloutResult
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional, List


@dataclass
class RolloutResult:
    """
    单次任务执行的轨迹记录。

    Attributes
    ----------
    id : str
        唯一标识，如 "rollout_20260603_001"
    skill_id : str
        所属技能ID
    task_type : str
        任务类型：search / tool_use / persona / decision / doc_generation 等
    task_description : str
        任务描述
    user_message : str
        用户原始消息
    predicted_answer : str
        AI 预测的回答
    reference_answer : Optional[str]
        参考答案（先生纠正时提供）
    hard : float
        硬指标：1.0=通过，0.0=失败
    soft : float
        软指标：置信度 0.0~1.0
    fail_reason : Optional[str]
        失败原因（hard=0时填写）
    feedback : Optional[str]
        先生反馈内容
    timestamp : str
        执行时间，ISO 格式
    metadata : dict
        其他元数据（如 token 消耗、工具调用记录等）
    """

    skill_id: str = ""
    task_type: str = "unknown"
    task_description: str = ""
    user_message: str = ""
    predicted_answer: str = ""
    reference_answer: Optional[str] = None
    hard: float = 0.0
    soft: float = 0.0
    fail_reason: Optional[str] = None
    feedback: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict = field(default_factory=dict)

    # 内部字段
    id: str = field(default="")

    def __post_init__(self):
        if not self.id:
            date_str = datetime.now().strftime("%Y%m%d")
            uid = uuid.uuid4().hex[:6]
            self.id = f"rollout_{date_str}_{uid}"

    def is_failure(self) -> bool:
        """硬指标未通过"""
        return self.hard < 1.0

    def is_soft_failure(self) -> bool:
        """软指标未通过（hard通过但 soft < 1.0）"""
        return self.hard >= 1.0 and self.soft < 1.0

    def is_hard_failure(self) -> bool:
        """硬指标失败"""
        return self.hard < 1.0

    def to_dict(self) -> dict:
        """序列化为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RolloutResult":
        """从字典反序列化"""
        # 过滤掉不在 dataclass 字段中的 key
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)

    def summary(self) -> str:
        """生成单行摘要（用于日志）"""
        status = "PASS" if self.hard >= 1.0 else "FAIL"
        reason = self.fail_reason or ""
        return (
            f"[{self.id}] {self.task_type}/{status} "
            f"(hard={self.hard:.1f}, soft={self.soft:.2f}) "
            f"{self.task_description[:40]} "
            f"reason={reason[:60]!r}"
        )


def make_rollout_result(
    skill_id: str,
    task_type: str,
    task_description: str,
    user_message: str,
    predicted_answer: str,
    reference_answer: Optional[str] = None,
    hard: float = 0.0,
    soft: float = 0.0,
    fail_reason: Optional[str] = None,
    feedback: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> RolloutResult:
    """
    便捷构造函数。

    Parameters
    ----------
    skill_id : str
        技能ID
    task_type : str
        任务类型
    task_description : str
        任务描述
    user_message : str
        用户原始消息
    predicted_answer : str
        AI 预测回答
    reference_answer : Optional[str]
        参考答案
    hard : float
        硬指标
    soft : float
        软指标
    fail_reason : Optional[str]
        失败原因
    feedback : Optional[str]
        先生反馈
    metadata : Optional[dict]
        其他元数据

    Returns
    -------
    RolloutResult
    """
    return RolloutResult(
        id=f"rollout_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}",
        skill_id=skill_id,
        task_type=task_type,
        task_description=task_description,
        user_message=user_message,
        predicted_answer=predicted_answer,
        reference_answer=reference_answer,
        hard=hard,
        soft=soft,
        fail_reason=fail_reason,
        feedback=feedback,
        timestamp=datetime.now().isoformat(),
        metadata=metadata or {},
    )


if __name__ == "__main__":
    # 快速测试
    r = make_rollout_result(
        skill_id="robot-evolve",
        task_type="tool_use",
        task_description="执行 cargo check 编译检查",
        user_message="帮我检查沧渊项目的 Rust 编译",
        predicted_answer="cargo check 执行成功",
        hard=0.0,
        soft=0.5,
        fail_reason="cargo check 报错：cannot find crate for 'tokio'",
        feedback="你漏了依赖声明",
    )
    print(r.summary())
    print(r.to_dict())
