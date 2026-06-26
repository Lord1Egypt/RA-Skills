"""
SkillGuard — Detector Registry
"""

from skillguard.detectors.base import BaseDetector
from skillguard.pipeline import DetectorRegistry

from skillguard.detectors.prompt_injection import PromptInjectionDetector
from skillguard.detectors.secret_exposure import SecretExposureDetector
from skillguard.detectors.code_execution import CodeExecutionDetector
from skillguard.detectors.dependency_audit import DependencyAuditDetector
from skillguard.detectors.permission_analysis import PermissionAnalysisDetector
from skillguard.detectors.sensitive_file_access import SensitiveFileAccessDetector
from skillguard.detectors.network_whitelist import NetworkWhitelistDetector
from skillguard.detectors.memory_pollution import MemoryPollutionDetector

# Auto-register all
DetectorRegistry.register(PromptInjectionDetector())
DetectorRegistry.register(SecretExposureDetector())
DetectorRegistry.register(CodeExecutionDetector())
DetectorRegistry.register(DependencyAuditDetector())
DetectorRegistry.register(PermissionAnalysisDetector())
DetectorRegistry.register(SensitiveFileAccessDetector())
DetectorRegistry.register(NetworkWhitelistDetector())
DetectorRegistry.register(MemoryPollutionDetector())
