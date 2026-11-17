"""
规则自动提取器 - 从追踪记录和学习记录中提取 avoid/prefer 规则
"""
import re
import os
from dataclasses import dataclass
from typing import List, Optional
from collections import Counter


@dataclass
class Rule:
    """规则定义"""
    rule_id: str
    category: str  # avoid / prefer
    description: str
    pattern: Optional[str] = None
    confidence: float = 0.0
    source_count: int = 0


class RuleExtractor:
    """规则自动提取器"""

    def __init__(self):
        self.error_patterns = Counter()
        self.success_patterns = Counter()

    def extract_from_traces(self, traces: List[dict]) -> List[Rule]:
        """从追踪记录中提取规则

        Args:
            traces: 追踪记录列表，每条包含:
                - operation_name: 操作名称
                - status: success / error
                - error_type: 错误类型（可选）
                - duration_ms: 耗时（可选）

        Returns:
            提取的规则列表
        """
        rules = []

        # 分类统计
        failures = [t for t in traces if t.get("status") == "error"]
        successes = [t for t in traces if t.get("status") == "success"]

        # 从失败中提取 avoid 规则
        rules.extend(self._extract_from_failures(failures))

        # 从成功中提取 prefer 规则
        rules.extend(self._extract_from_successes(successes))

        return rules

    def _extract_from_failures(self, failures: List[dict]) -> List[Rule]:
        """从失败中提取 avoid 规则"""
        # 按操作名统计错误
        error_by_op = Counter()
        for f in failures:
            op = f.get("operation_name", "unknown")
            error_by_op[op] += 1

        total = len(failures) if failures else 1
        rules = []

        for op, count in error_by_op.most_common(10):  # 最多10条
            confidence = count / total
            if confidence >= 0.1:  # 至少10%的错误率
                rules.append(Rule(
                    rule_id=f"avoid_{op}",
                    category="avoid",
                    description=f"避免在 {op} 中出现错误",
                    pattern=op,
                    confidence=round(confidence, 2),
                    source_count=count,
                ))

        return rules

    def _extract_from_successes(self, successes: List[dict]) -> List[Rule]:
        """从成功中提取 prefer 规则"""
        # 按操作名统计成功
        success_by_op = Counter()
        for s in successes:
            op = s.get("operation_name", "unknown")
            success_by_op[op] += 1

        total = len(successes) if successes else 1
        rules = []

        for op, count in success_by_op.most_common(10):  # 最多10条
            confidence = count / total
            if confidence >= 0.2:  # 至少20%的成功率
                rules.append(Rule(
                    rule_id=f"prefer_{op}",
                    category="prefer",
                    description=f"优先使用 {op} 的成功模式",
                    pattern=op,
                    confidence=round(confidence, 2),
                    source_count=count,
                ))

        return rules

    def extract_from_learnings(self, learnings_dir: str) -> List[Rule]:
        """从 .learnings/ 目录提取规则

        Args:
            learnings_dir: .learnings/ 目录路径

        Returns:
            提取的规则列表
        """
        rules = []

        if not os.path.exists(learnings_dir):
            return rules

        for filename in os.listdir(learnings_dir):
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(learnings_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # 提取标题作为规则描述
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
                # 判断是 avoid 还是 prefer
                if any(kw in title.lower() for kw in ["错误", "失败", "避免", "error", "fail", "avoid"]):
                    category = "avoid"
                else:
                    category = "prefer"

                rules.append(Rule(
                    rule_id=f"learning_{filename.replace('.md', '')}",
                    category=category,
                    description=title,
                    confidence=0.8,  # 学习记录默认高置信度
                    source_count=1,
                ))

        return rules
