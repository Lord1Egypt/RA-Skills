"""
Phase Manager - 数据契约定义
schemas.py

定义 Phase 数据管理的核心数据结构。
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import hashlib


# ============================================================================
# 常量定义
# ============================================================================

PHASE_NAMES = {
    1: "规划与定稿",
    2: "逐节点写作",
    3: "整合",
    3.5: "深度学术评审",
    4: "整合修订",
    5: "终审与输出",
}

CONTENT_TYPE_INTEGRATED = "integrated"  # 整合版正文（.md）
CONTENT_TYPE_REVIEW = "review"          # 审核报告（.json）
CONTENT_TYPE_SUMMARY = "summary"        # 结构化摘要（.json）

# 有效状态
STATUS_PENDING = "pending"
STATUS_RUNNING = "running"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"
STATUS_MODIFIED = "modified"  # 用户修改过文件

# 触发来源
TRIGGERED_BY_AUTO = "auto"
TRIGGERED_BY_USER_CONFIRM = "user_confirm"
TRIGGERED_BY_USER_MODIFY = "user_modify"

# ============================================================================
# PhaseSummary - Phase 执行结果的结构化摘要
# ============================================================================

@dataclass
class PhaseSummary:
    """
    Phase 执行结果的结构化摘要。

    不包含正文内容，只包含元数据。
    用于 HIL 消息渲染和跨 Phase 流转判断。
    """

    phase: float                           # Phase 编号（1/2/3/3.5/4/5）
    status: str                            # pending/running/completed/failed/modified
    timestamp: str                         # ISO timestamp
    file_path: str                         # 产出文件路径
    content_hash: str                      # 内容 MD5 哈希（检测用户是否改过）
    word_count: int                        # 中文字数
    chapter_count: int                     # 章节数
    key_metrics: Dict[str, Any]            # 关键指标（Phase 类型不同内容不同）
    user_modifications: bool               # 用户是否手动修改过文件
    message: str                           # 一句话摘要

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> "PhaseSummary":
        return cls(**d)

    def summary_text(self) -> str:
        """生成简短摘要文本"""
        metrics_str = ", ".join(f"{k}={v}" for k, v in self.key_metrics.items())
        return (
            f"Phase {self.phase} [{self.status}] "
            f"字数:{self.word_count} | 章节:{self.chapter_count} | "
            f"{metrics_str}"
        )


# ============================================================================
# PhaseFile - 文件元数据
# ============================================================================

@dataclass
class PhaseFile:
    """
    Phase 产出文件的元数据记录。
    """

    phase: float                           # Phase 编号
    content_type: str                      # integrated/review/summary
    file_path: str                         # 文件绝对路径
    hash: str                              # 内容哈希
    size_bytes: int                        # 文件大小
    created_at: str                        # ISO timestamp
    updated_at: str                        # ISO timestamp
    backup_path: Optional[str] = None      # 备份文件路径（上一版本）

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> "PhaseFile":
        return cls(**d)


# ============================================================================
# GateResult - 门禁检查结果
# ============================================================================

@dataclass
class GateResult:
    """
    Phase 流转门禁检查结果。
    """

    passed: bool                           # 是否通过
    phase: float                           # 检查的 Phase
    checks: Dict[str, Tuple[bool, str]]    # {check_name: (passed, detail)}
    blocking_issues: List[str] = field(default_factory=list)  # 阻塞性问题

    def to_dict(self) -> Dict:
        # checks 的 value 是 tuple，需要转成 list
        return {
            "passed": self.passed,
            "phase": self.phase,
            "checks": {k: list(v) for k, v in self.checks.items()},
            "blocking_issues": self.blocking_issues,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> "GateResult":
        # checks 的 value 是 list，需要转回 tuple
        checks = {k: tuple(v) for k, v in d.get("checks", {}).items()}
        return cls(
            passed=d["passed"],
            phase=d["phase"],
            checks=checks,
            blocking_issues=d.get("blocking_issues", []),
        )

    def add_blocking_issue(self, issue: str):
        self.blocking_issues.append(issue)
        self.passed = False

    def summary(self) -> str:
        """生成人类可读的 gate 结果摘要"""
        if self.passed:
            return f"✅ Phase {self.phase} 门禁通过"
        lines = [f"❌ Phase {self.phase} 门禁未通过"]
        for issue in self.blocking_issues:
            lines.append(f"  - {issue}")
        return "\n".join(lines)


# ============================================================================
# PhaseTransition - Phase 流转记录
# ============================================================================

@dataclass
class PhaseTransition:
    """
    Phase 流转记录。
    用于追踪论文在各个 Phase 之间的流转历史。
    """

    from_phase: float                      # 来源 Phase
    to_phase: float                        # 目标 Phase
    triggered_by: str                      # auto/user_confirm/user_modify
    triggered_at: str                      # ISO timestamp
    triggered_session: str                 # 触发时的 session ID
    content_hash: str                      # 触发时的文件哈希
    gate_passed: bool                      # 门禁是否通过

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> "PhaseTransition":
        return cls(**d)


# ============================================================================
# 辅助函数
# ============================================================================

def calculate_content_hash(content: str) -> str:
    """
    计算内容的 MD5 哈希。

    用于检测用户是否修改过文件。
    """
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.md5(content).hexdigest()


def calculate_word_count(content: str) -> int:
    """
    计算中文字数（不含标点、空格、英文）。

    简单实现：总字符数 - ASCII 字符数。
    更精确的实现需要识别中文 Unicode 范围。
    """
    if not content:
        return 0

    count = 0
    for char in content:
        # 中文 Unicode 范围：\u4e00-\u9fff（常用汉字）
        # 标点符号范围较广，这里简单处理：非 ASCII printable 都算中文
        code = ord(char)
        if code > 127 or ('\u4e00' <= char <= '\u9fff'):
            count += 1
    return count


def extract_chapter_count(content: str) -> int:
    """
    从正文中提取章节数。

    匹配模式：# 第X章 或 ## 第X章
    """
    import re
    # 匹配一级或二级标题的"第X章"模式
    pattern = r'^#{1,2}\s*第[一二三四五六七八九十\d]+章'
    matches = re.findall(pattern, content, re.MULTILINE)
    return len(matches)


def now_iso() -> str:
    """返回当前时间的 ISO 格式字符串"""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")


def build_file_path(workspace: str, phase: float, content_type: str) -> str:
    """
    构建 Phase 产出文件的路径。

    Args:
        workspace: 工作区目录
        phase: Phase 编号
        content_type: integrated/review/summary

    Returns:
        文件绝对路径
    """
    ext = "md" if content_type == CONTENT_TYPE_INTEGRATED else "json"
    return f"{workspace}/_phase{phase}_{content_type}.{ext}"