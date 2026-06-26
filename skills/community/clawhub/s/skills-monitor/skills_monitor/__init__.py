"""
Skills Monitor v0.6.0 — 本地 Skills 监控评估系统

核心模块:
  - identity: 身份管理 (agent_id + API Key + Keychain + 生命周期)
  - secure_store: OS Keychain 安全凭证存储
  - interceptor: SDK 拦截器 (@skill_monitor 装饰器 + 实时上报)
  - implicit_feedback: 隐性对话语义评分引擎
  - feedback: 轻量情感分析工具
  - benchmark: 基准运行器
  - comparator: 对比分析器
  - evaluator: 7因子综合评估引擎（+社区热度/评分）
  - recommender: Skill 推荐引擎
  - reporter: 报告生成器
  - diagnostic: 诊断报告生成器
  - sanitizer: 敏感信息自动脱敏引擎
  - auto_reporter: 后台自动上报（定时诊断 + 增量同步）
  - realtime_reporter: 实时调用反馈上报（异步队列 + 批量）
  - scheduler: 定时任务管理 + 首次启动交互式确认
  - llm_baseline: 大模型基准线测试 + TOP50×6模型批量评测 🆕
  - store: SQLite 数据存储
  - gdpr_manager: GDPR 合规管理
  - category_mapping: 官方标签分类映射
  - benchmark_prompts: 分类基准评测 Prompt 模板 🆕
  - clawhub_client: ClawHub 社区数据采集器
  - skill_registry: Skill 注册与发现
  - runners: Skill 运行适配器
"""

__version__ = "0.6.1"

# 便捷导入
from skills_monitor.core.identity import IdentityManager
from skills_monitor.core.secure_store import SecureStore
from skills_monitor.core.interceptor import configure, run_skill_function
from skills_monitor.core.implicit_feedback import (
    ImplicitFeedbackEngine,
    ConversationSignal,
)
from skills_monitor.core.feedback import analyze_sentiment_simple
from skills_monitor.core.benchmark import BenchmarkRunner
from skills_monitor.core.comparator import SkillComparator
from skills_monitor.core.evaluator import SkillEvaluator
from skills_monitor.core.recommender import SkillRecommender
from skills_monitor.core.reporter import ReportGenerator
from skills_monitor.core.diagnostic import DiagnosticReporter
from skills_monitor.core.sanitizer import DataSanitizer
from skills_monitor.core.uploader import DataUploader
from skills_monitor.core.auto_reporter import AutoReporter
from skills_monitor.core.realtime_reporter import RealtimeReporter
from skills_monitor.core.scheduler import ScheduleManager
from skills_monitor.core.llm_baseline import LLMBaselineTester, BatchBenchmark
from skills_monitor.data.store import DataStore
from skills_monitor.data.gdpr_manager import GDPRManager
from skills_monitor.data.category_mapping import get_category, match_tags
from skills_monitor.data.benchmark_prompts import get_benchmark_prompt
from skills_monitor.adapters.skill_registry import SkillRegistry
from skills_monitor.adapters.runners import SkillRunner, get_adapter
from skills_monitor.adapters.clawhub_client import ClawHubClient

__all__ = [
    "IdentityManager",
    "SecureStore",
    "configure",
    "run_skill_function",
    "ImplicitFeedbackEngine",
    "ConversationSignal",
    "analyze_sentiment_simple",
    "BenchmarkRunner",
    "SkillComparator",
    "SkillEvaluator",
    "SkillRecommender",
    "ReportGenerator",
    "DiagnosticReporter",
    "DataSanitizer",
    "DataStore",
    "SkillRegistry",
    "DataUploader",
    "AutoReporter",
    "RealtimeReporter",
    "ScheduleManager",
    "LLMBaselineTester",
    "BatchBenchmark",
    "GDPRManager",
    "ClawHubClient",
    "SkillRunner",
    "get_adapter",
    "get_category",
    "match_tags",
    "get_benchmark_prompt",
]
