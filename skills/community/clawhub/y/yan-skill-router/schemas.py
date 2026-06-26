#!/usr/bin/env python3
"""SkillRouter v2 — 数据模型定义"""
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum
import json
import time


class SelectionResult(Enum):
    CORRECT = "correct"
    WRONG = "wrong"
    AMBIGUOUS = "ambiguous"


@dataclass
class SkillProfile:
    """一个 skill 的完整画像"""
    name: str
    description: str
    dir: str
    path: str
    capabilities: list[str] = field(default_factory=list)
    brief_guide: str = ""
    body_start: str = ""
    relevance: float = 0.0  # embedding 得分

    def to_prompt_block(self, index: int) -> str:
        """格式化为给 LLM 看的文本块"""
        lines = [
            f"{index}. {self.name} (relevance: {self.relevance:.2f})",
            f"   描述: {self.description}",
        ]
        if self.capabilities:
            lines.append(f"   能力: {', '.join(self.capabilities)}")
        if self.brief_guide:
            lines.append(f"   指导: {self.brief_guide}")
        if self.body_start:
            lines.append(f"   详情: {self.body_start}")
        lines.append(f"   路径: {self.path}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SelectionRecord:
    """一次 skill 选择的完整记录"""
    timestamp: float
    query: str
    top5: list[dict]  # [{name, relevance}, ...]
    llm_chosen: Optional[str]  # None = LLM 拒选
    llm_reasoning: str = ""
    executed_ok: bool = False
    correctness: str = "unknown"  # correct / wrong / ambiguous / unknown
    user_correction: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "query": self.query,
            "top5": self.top5,
            "llm_chosen": self.llm_chosen,
            "llm_reasoning": self.llm_reasoning,
            "executed_ok": self.executed_ok,
            "correctness": self.correctness,
            "user_correction": self.user_correction,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "SelectionRecord":
        return cls(**d)


def timestamp_now() -> float:
    return time.time()


def format_datetime(ts: float) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
