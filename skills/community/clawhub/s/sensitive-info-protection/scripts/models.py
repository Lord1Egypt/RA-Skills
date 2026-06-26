from dataclasses import dataclass, field
from typing import List, Optional
import re


@dataclass
class DetectionRule:
    """Detection rule for sensitive information"""
    name: str
    pattern: str
    sensitivity: str = "medium"  # high, medium, low
    description: str = ""
    enabled: bool = True
    priority: int = 0  # Higher priority rules match first
    compiled: Optional[re.Pattern] = None

    def compile(self) -> None:
        """Compile the regex pattern"""
        if self.compiled is None:
            self.compiled = re.compile(self.pattern)

    def match(self, text: str) -> List[re.Match]:
        """Find all matches in text"""
        if not self.enabled:
            return []
        if self.compiled is None:
            self.compile()
        return list(self.compiled.finditer(text))


@dataclass
class DetectionResult:
    """Result of a single sensitive detection"""
    rule: DetectionRule
    match: re.Match
    start: int
    end: int
    text: str

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "sensitive_type": self.rule.name,
            "start": self.start,
            "end": self.end,
            "text": self.text,
            "sensitivity": self.rule.sensitivity,
            "description": self.rule.description
        }


@dataclass
class ScanResult:
    """Result of scanning a text"""
    content: str
    detections: List[DetectionResult] = field(default_factory=list)
    has_sensitive: bool = False

    def add_detection(self, detection: DetectionResult) -> None:
        """Add a detection result"""
        self.detections.append(detection)
        self.has_sensitive = True

    def sort_by_priority(self) -> None:
        """Sort detections by rule priority and sensitivity"""
        sensitivity_order = {"high": 3, "medium": 2, "low": 1}
        self.detections.sort(
            key=lambda x: (-x.rule.priority, -sensitivity_order.get(x.rule.sensitivity, 0))
        )

    def to_markdown(self) -> str:
        """Format result as markdown for display"""
        if not self.has_sensitive:
            return "No sensitive information detected."

        output = ["## 检测结果"]
        for i, det in enumerate(self.detections, 1):
            output.append(f"- 敏感类型: {det.rule.name}")
            output.append(f"- 位置: {det.start}:{det.end}")
            output.append(f"- 原文: `{det.text}`")
            output.append(f"- 敏感度: {det.rule.sensitivity}")
            if det.rule.description:
                output.append(f"- 描述: {det.rule.description}")
            if i < len(self.detections):
                output.append("")

        output.append("\n## 操作选项")
        output.append("1. 确认放行")
        output.append("2. 修改后发送")
        output.append("3. 取消发送")

        return "\n".join(output)
