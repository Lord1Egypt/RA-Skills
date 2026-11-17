"""contracts package — Pydantic v2 Schemas"""
from contracts.search_schema import SearchRequest, SearchHit, SearchBatch, SearchOutput, QueryIntent, QueryLanguage
from contracts.crawl_schema import CrawlRequest, CrawledPage, CrawlOutput, AntiBlockConfig
from contracts.llm_schema import (
    LLMRequest, LLMResponse, LLMProvider, ProviderStatus,
    FallbackChain, CrossValidation, SentimentAnalysis,
)
from contracts.nlp_schema import (
    NLPAnalysisRequest, EntityList, NLPAnalysisOutput,
)
from contracts.state_schema import (
    PipelinePhase, PipelineState, PhaseContext, WALEntry,
    VALID_TRANSITIONS,
)
from contracts.report_schema import (
    ReportRequest, ReportOutput, ReportFormat, DeliveryStatus, SourceEntry,
)
from contracts.alert_schema import AlertRule, AlertEvent, AlertLevel, CronConfig
from contracts.analysis_schema import (
    AnalysisOutput, NLPResults, CredibilityResults, CredibilityScore,
    LLMAnalysis, SentimentResult, CrossValidationResult,
)
from contracts.context_schema import (
    StageContext, PipelineBus,
    StageNotExecutedError, StageTypeError,
)

__all__ = [
    # search
    "SearchRequest", "SearchHit", "SearchBatch", "SearchOutput",
    "QueryIntent", "QueryLanguage",
    # crawl
    "CrawlRequest", "CrawledPage", "CrawlOutput", "AntiBlockConfig",
    # llm
    "LLMRequest", "LLMResponse", "LLMProvider", "ProviderStatus",
    "FallbackChain", "CrossValidation", "SentimentAnalysis",
    # nlp
    "NLPAnalysisRequest", "EntityList", "NLPAnalysisOutput",
    # state
    "PipelinePhase", "PipelineState", "PhaseContext", "WALEntry",
    "VALID_TRANSITIONS",
    # report
    "ReportRequest", "ReportOutput", "ReportFormat", "DeliveryStatus", "SourceEntry",
    # alert
    "AlertRule", "AlertEvent", "AlertLevel", "CronConfig",
    # analysis
    "AnalysisOutput", "NLPResults", "CredibilityResults", "CredibilityScore",
    "LLMAnalysis", "SentimentResult", "CrossValidationResult",
    # context bus (Phase 4.1)
    "StageContext", "PipelineBus",
    "StageNotExecutedError", "StageTypeError",
]
