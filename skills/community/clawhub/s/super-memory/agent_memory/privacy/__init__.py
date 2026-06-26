"""Privacy Guard — V12 记忆隐私守门系统"""

from .guard import PrivacyGuard, RequestContext
from .rules import AccessLevel, PrivacyRule, PrivacyRuleSet
from .analyzer import SensitivityAnalyzer
from .consent import ConsentManager
from .eraser import MemoryEraser, ErasureReport, BulkErasureReport
from .patterns import PIIPattern, get_all_patterns, get_patterns_by_category

__all__ = [
    'PrivacyGuard',
    'AccessLevel',
    'PrivacyRule',
    'PrivacyRuleSet',
    'RequestContext',
    'SensitivityAnalyzer',
    'ConsentManager',
    'MemoryEraser',
    'ErasureReport',
    'BulkErasureReport',
    'PIIPattern',
    'get_all_patterns',
    'get_patterns_by_category',
]
