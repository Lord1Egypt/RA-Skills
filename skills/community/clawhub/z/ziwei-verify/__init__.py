"""
ziwei_verify 技能包
生时校正与命盘验证引擎
"""

__version__ = "0.1.0"
__author__ = "基于倪海厦紫微斗数体系"
__skill_id__ = "ziwei_verify"

from .main import run
from .calibrator import calibrate, CorrectionResult
from .dialogue_handler import VerificationDialogueHandler
from .output_formatter import format_calibration_result, format_comparison_table
from .prompt_generator import generate_verification_prompt, generate_verification_summary, format_point_as_json

__all__ = [
    "run",
    "calibrate",
    "CorrectionResult",
    "VerificationDialogueHandler",
    "format_calibration_result",
    "format_comparison_table",
    "validate_input",
    "STANDARD_DATA_PACKET_SCHEMA",
    # P3 新增
    "generate_verification_prompt",
    "generate_verification_summary",
    "format_point_as_json",
]
