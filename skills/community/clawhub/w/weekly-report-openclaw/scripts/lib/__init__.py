"""Weekly report skill library modules."""

from .config import Settings
from .models import (
    WeeklyReportData,
    WeeklyReportItem,
    DateRange,
    SummarizedReport,
    WorkCategories,
    CategoryItem,
)
from .date_utils import get_week_range, get_last_week_range, parse_date_input
from .login import LoginResult, get_or_refresh_token, login_with_browser
from .fetcher import ReportFetcher, fetch_reports
from .summarizer import ReportSummarizer, summarize_reports
from .generator import DocumentGenerator, generate_report_document
from .llm_client import create_llm_client, DeepSeekClient

__all__ = [
    # Config
    "Settings",
    # Models
    "WeeklyReportData",
    "WeeklyReportItem",
    "DateRange",
    "SummarizedReport",
    "WorkCategories",
    "CategoryItem",
    # Utils
    "get_week_range",
    "get_last_week_range",
    "parse_date_input",
    # Login
    "LoginResult",
    "get_or_refresh_token",
    "login_with_browser",
    # Fetcher
    "ReportFetcher",
    "fetch_reports",
    # Summarizer
    "ReportSummarizer",
    "summarize_reports",
    # Generator
    "DocumentGenerator",
    "generate_report_document",
    # LLM
    "create_llm_client",
    "DeepSeekClient",
]
