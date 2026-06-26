# PDCA+ISO9001 质量管理决策系统技能
__version__ = "1.0.0"
__author__ = "小Q"
__description__ = "基于PDCA循环和ISO9001质量管理体系的决策系统，实现全流程质量管控、循证决策、知识沉淀和持续改进"

# 导出核心模块
from .scripts.pdca_engine import PDCAEngine, PDCAPhase, ProjectStatus, Project
from .scripts.iso9001_validator import ISO9001Validator, ComplianceLevel, CheckResult, ValidationReport
from .scripts.decision_checker import DecisionChecker, DecisionRiskLevel, DecisionQuality, CheckItemResult, DecisionCheckReport
from .scripts.knowledge_manager import KnowledgeManager
from .scripts.report_generator import ReportGenerator
from .scripts.utils import load_config, save_config, generate_id, get_current_time

__all__ = [
    "PDCAEngine", "PDCAPhase", "ProjectStatus", "Project",
    "ISO9001Validator", "ComplianceLevel", "CheckResult", "ValidationReport",
    "DecisionChecker", "DecisionRiskLevel", "DecisionQuality", "CheckItemResult", "DecisionCheckReport",
    "KnowledgeManager",
    "ReportGenerator",
    "load_config", "save_config", "generate_id", "get_current_time"
]
