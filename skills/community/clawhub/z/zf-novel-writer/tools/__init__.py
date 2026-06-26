import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')# 灏忚鍐欎綔楠岃瘉宸ュ叿鍖•
__version__ = '1.1'
__author__ = 'OpenClaw AI Assistant'

from .word_count import count_words
from .format_checker import check_format
from .finance_calculator import FinanceCalculator, parse_chapter_finance
from .finance_validator import parse_finance_data, validate_finance
from .system_rules_validator import parse_chapter_file, validate_system_rules
from .protagonist_checker import parse_chapter_content, check_protagonist_character
from .next_chapter_checker import parse_next_chapter_preview, validate_preview
from .logic_checker import LogicChecker

__all__ = [
    'count_words',
    'check_format',
    'FinanceCalculator',
    'parse_chapter_finance',
    'parse_finance_data',
    'validate_finance',
    'parse_chapter_file',
    'validate_system_rules',
    'parse_chapter_content',
    'check_protagonist_character',
    'parse_next_chapter_preview',
    'validate_preview',
    'LogicChecker',
]

