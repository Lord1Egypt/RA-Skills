"""
SkillGuard — Agent Skill Security Scanner
Base detector and shared types. v1.0.0 | MIT License
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import abc


@dataclass
class Finding:
    """A single security finding discovered by a detector."""
    id: str                    # Unique ID: DETECTOR-XXX
    detector: str              # Detector name
    severity: str              # CRITICAL / HIGH / MEDIUM / LOW
    confidence: float          # 0.0–1.0
    owasp_asi_id: str = ""     # e.g., ASI-01
    cwe_id: str = ""           # e.g., CWE-94
    title: str = ""
    description: str = ""
    code_snippet: str = ""     # Relevant code snippet
    file_path: str = ""
    line_number: int = 0
    remediation: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


@dataclass
class SkillContext:
    """Extracted skill context passed through the pipeline."""
    skill_name: str = ""
    skill_version: str = ""
    skill_description: str = ""
    skill_md_content: str = ""
    requirements_content: str = ""
    python_files: Dict[str, str] = field(default_factory=dict)  # path→content
    all_files: Dict[str, bytes] = field(default_factory=dict)   # path→bytes
    package_path: str = ""


class PipelineContext:
    """Shared context across detectors in a pipeline run."""

    def __init__(self):
        self.ast_cache: Dict[str, Any] = {}         # file_path → AST
        self.secrets_found: List[str] = []          # Already known secrets
        self.url_registry: Dict[str, str] = {}      # url → status (allowed/blocked)
        self.skill_context: Optional[SkillContext] = None
        self.metadata: Dict[str, Any] = {}


class BaseDetector(abc.ABC):
    """Abstract base for all security detectors."""

    name: str = "base"
    description: str = "Base detector"
    owasp_asi_ids: List[str] = []
    severity_default: str = "MEDIUM"

    def analyze(self, skill_ctx: SkillContext, pipeline_ctx: PipelineContext) -> List[Finding]:
        """Run detection. Must be implemented by subclasses."""
        raise NotImplementedError

    def _make_finding(self, finding_id: str, severity: str, confidence: float,
                      owasp_asi_id: str, cwe_id: str, title: str, description: str,
                      code_snippet: str = "", file_path: str = "", line_number: int = 0,
                      remediation: str = "", extra: dict = None) -> Finding:
        return Finding(
            id=finding_id,
            detector=self.name,
            severity=severity,
            confidence=min(max(confidence, 0.0), 1.0),
            owasp_asi_id=owasp_asi_id,
            cwe_id=cwe_id,
            title=title,
            description=description,
            code_snippet=code_snippet,
            file_path=file_path,
            line_number=line_number,
            remediation=remediation,
            extra=extra or {},
        )
