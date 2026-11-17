"""
Modelos de datos fuertemente tipados para Security Maintainer.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime


class EnvironmentType(str, Enum):
    WINDOWS = "windows"
    WSL = "wsl"
    MACOS = "macos"
    PROJECT = "project"


class ManagerType(str, Enum):
    WINGET = "winget"
    WINDOWS_UPDATE = "windows_update"
    REGISTRY = "registry"
    APPX = "appx"
    APT = "apt"
    DPKG = "dpkg"
    RPM = "rpm"
    APK = "apk"
    PIPX = "pipx"
    NPM = "npm"
    SCOOP = "scoop"
    CHOCO = "choco"
    HOMEBREW = "homebrew"
    MAS = "mas"
    APPLE_UPDATE = "apple_update"
    PYTHON_ENV = "python_env"
    NODE_ENV = "node_env"
    MANUAL = "manual"


class FindingCategory(str, Enum):
    GENERAL_UPDATE_AVAILABLE = "general_update_available"
    VULNERABILITY_PATCHED = "vulnerability_patched"
    CONFIG_MITIGATION = "config_mitigation"
    UNPATCHED_VULNERABILITY = "unpatched_vulnerability"
    UNSUPPORTED_EOL = "unsupported_eol"
    FUNCTIONAL_BUG = "functional_bug"
    AI_SECURITY_RISK = "ai_security_risk"


class AIThreatType(str, Enum):
    PROMPT_INJECTION = "prompt_injection"
    MCP_TOOL_POISONING = "mcp_tool_poisoning"
    CREDENTIAL_EXPOSURE = "credential_exposure"
    UNAUTHENTICATED_LLM_SERVICE = "unauthenticated_llm_service"
    EXCESSIVE_AGENCY = "excessive_agency"
    ROGUE_PERSISTENCE = "rogue_persistence"


@dataclass
class AISecurityFinding:
    threat_type: AIThreatType
    title: str
    severity: SeverityLevel
    target_component: str
    description: str
    evidence: str
    remediation_recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "threat_type": self.threat_type.value,
            "title": self.title,
            "severity": self.severity.value,
            "target_component": self.target_component,
            "description": self.description,
            "evidence": self.evidence,
            "remediation_recommendation": self.remediation_recommendation
        }


class ConfidenceLevel(str, Enum):
    CONFIRMED = "confirmed"
    LIKELY = "likely"
    NOT_EVALUABLE = "not_evaluable"


class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"


class ActionStatus(str, Enum):
    PROPOSED = "proposed"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    EXECUTED_VERIFIED = "executed_verified"
    EXECUTED_UNVERIFIED = "executed_unverified"
    PENDING_REBOOT = "pending_reboot"
    BLOCKED_PERMISSIONS = "blocked_permissions"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class InventoryItem:
    environment: EnvironmentType
    target_name: str                     # e.g., "Windows Host", distro "Ubuntu" or project path
    name: str                            # e.g., "Git", "curl", "openssl"
    id: str                              # Package ID (e.g., "Git.Git", "curl")
    installed_version: str
    manager: ManagerType
    latest_version: Optional[str] = None
    architecture: Optional[str] = None
    is_pinned: bool = False
    is_supported: bool = True
    update_mechanism_available: bool = True
    requires_manual_intervention: bool = False
    notes: Optional[str] = None
    extra_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["environment"] = self.environment.value
        d["manager"] = self.manager.value
        return d


@dataclass
class Vulnerability:
    cve_id: str                          # Primary ID (CVE-..., GHSA-..., OSV-...)
    aliases: List[str] = field(default_factory=list)
    title: str = ""
    summary: str = ""
    severity: SeverityLevel = SeverityLevel.UNKNOWN
    cvss_score: Optional[float] = None
    cvss_vector: Optional[str] = None           # CVSS Vector string (e.g. CVSS:3.1/AV:N/AC:L...)
    in_cisa_kev: bool = False
    cisa_due_date: Optional[str] = None
    in_vulncheck_kev: bool = False             # VulnCheck Community KEV
    epss_score: Optional[float] = None          # FIRST EPSS (0.0 a 1.0)
    epss_percentile: Optional[float] = None     # FIRST EPSS Percentil (0.0 a 1.0)
    nvd_summary: Optional[str] = None           # NIST NVD description
    msrc_kb: Optional[str] = None               # Microsoft KB Article ID
    msrc_severity: Optional[str] = None         # Critical, Important, Moderate, Low
    msrc_impact: Optional[str] = None           # Remote Code Execution, Elevation of Privilege...
    ubuntu_usn: Optional[str] = None            # Ubuntu Security Notice (e.g. USN-6942-1)
    fixed_version: Optional[str] = None
    source: str = "OSV"                  # OSV, CISA KEV, MSRC, Ubuntu USN, NVD, etc.
    confidence: ConfidenceLevel = ConfidenceLevel.CONFIRMED
    evidence: str = ""
    query_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["severity"] = self.severity.value
        d["confidence"] = self.confidence.value
        return d


@dataclass
class PlanAction:
    action_id: str                       # Unique action ID (e.g., "act-01")
    environment: EnvironmentType
    target: str                          # "windows", "wsl:Ubuntu", etc.
    product_name: str
    product_id: str
    manager: ManagerType
    installed_version: str
    target_version: str
    category: FindingCategory
    related_vulnerabilities: List[str]   # List of CVE / GHSA IDs
    exact_command: List[str]             # Argument list to execute
    required_privileges: str             # "user", "admin", "sudo"
    expected_reboot: bool
    verification_method: str
    rollback_available: bool
    rollback_limitations: str
    status: ActionStatus = ActionStatus.PROPOSED
    blocked_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["environment"] = self.environment.value
        d["manager"] = self.manager.value
        d["category"] = self.category.value
        d["status"] = self.status.value
        return d


@dataclass
class ActionPlan:
    plan_id: str
    created_at: str
    expires_at: str
    environment: str
    mode: str
    plan_hash: str                       # SHA-256 fingerprint of canonical action payload
    actions: List[PlanAction]
    is_approved: bool = False
    approval_token: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "environment": self.environment,
            "mode": self.mode,
            "plan_hash": self.plan_hash,
            "is_approved": self.is_approved,
            "approval_token": self.approval_token,
            "actions": [a.to_dict() for a in self.actions]
        }


@dataclass
class ExecutionResult:
    action_id: str
    product_name: str
    manager: ManagerType
    success: bool
    exit_code: int
    effective_version_detected: Optional[str] = None
    verification_passed: bool = False
    reboot_pending: bool = False
    duration_seconds: float = 0.0
    status: ActionStatus = ActionStatus.FAILED
    diagnostic_output: str = ""
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["manager"] = self.manager.value
        d["status"] = self.status.value
        return d


@dataclass
class CoverageSummary:
    total_components_detected: int = 0
    manageable_components: int = 0
    partially_manageable: int = 0
    unsupported_or_manual: int = 0
    query_sources_successful: List[str] = field(default_factory=list)
    query_sources_failed: List[str] = field(default_factory=list)
    is_coverage_complete: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
