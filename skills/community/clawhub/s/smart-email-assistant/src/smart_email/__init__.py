"""
Smart Email - AI智能邮件管理助手
"""

__version__ = "2.0.0"

from .config import config
from .database import MailTracker
from .mail_handler import EmailClient, EmailStorage
from .ai_analyzer import AIAnalyzer
from .outbox import OutboxManager
from .logger import setup_logging, get_logger, restore_print

__all__ = [
    'config',
    'MailTracker',
    'EmailClient',
    'EmailStorage',
    'AIAnalyzer',
    'OutboxManager',
    'setup_logging',
    'get_logger',
    'restore_print'
]
