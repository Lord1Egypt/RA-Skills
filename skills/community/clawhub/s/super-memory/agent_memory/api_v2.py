"""
api_v2.py - FastAPI-based REST API for the agent memory system (v12)

Endpoints:
  POST /v1/memories           - Write a memory
  GET  /v1/memories/{memory_id} - Get a memory by ID
  POST /v1/recall             - Search/recall memories
  GET  /v1/agents/{agent_id}/profile - Get agent personality profile
  GET  /v1/health             - Health check
  GET  /v1/metrics            - Prometheus metrics endpoint
  GET  /docs                  - Swagger UI (auto)

Features:
  - Pydantic v2 models (with v1 fallback)
  - Rate limiting middleware (100 req/min per agent, token bucket)
  - Pagination (offset/limit on list endpoints)
  - RFC 7807 Problem Details error responses
  - Dependency injection for store / pipeline / recall components
  - CORS middleware enabled

Usage:
  uvicorn agent_memory.api_v2:app --host 127.0.0.1 --port 8978
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
import threading
import time
from contextlib import asynccontextmanager
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# ── Pydantic v2 / v1 compatibility ────────────────────────
try:
    from pydantic import BaseModel as _BaseModel, Field, ConfigDict, field_validator
    from pydantic import ValidationError as PydanticValidationError
    _PYDANTIC_V2 = True
except ImportError:
    from pydantic import BaseModel as _BaseModel, Field, validator
    from pydantic import ValidationError as PydanticValidationError
    _PYDANTIC_V2 = False

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from .auth_middleware import AuthConfig, AuthMiddleware

import warnings
warnings.warn(
    "API v2 is deprecated and will be removed in a future version. "
    "Please migrate to API v3. See UPGRADE_PLAN.md for migration guide.",
    DeprecationWarning,
    stacklevel=2,
)

# Ensure the package directory is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

# ── RFC 7807 helpers ─────────────────────────────────────

def _problem_detail(
    request: Request,
    status: int,
    title: str,
    detail: str,
    type_uri: str = "about:blank",
    errors: Optional[list] = None,
) -> JSONResponse:
    body: dict = {
        "type": type_uri,
        "title": title,
        "status": status,
        "detail": detail,
        "instance": str(request.url),
    }
    if errors:
        body["errors"] = errors
    return JSONResponse(status_code=status, content=body)


# ═══════════════════════════════════════════════════════════
# Pydantic Models (v2-compatible, v1 fallback)
# ═══════════════════════════════════════════════════════════

_VALID_IMPORTANCE = frozenset({"high", "medium", "low"})
_VALID_SIGNIFICANCE = frozenset({"trivial", "notable", "important", "breakthrough", "crisis", "milestone"})
_VALID_VISIBILITY = frozenset({"private", "team", "public"})


def _create_model_config() -> dict:
    if _PYDANTIC_V2:
        return {"populate_by_name": True, "extra": "forbid"}
    return {}


class PaginationParams:
    """Reusable pagination dependency."""
    def __init__(
        self,
        offset: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(50, ge=1, le=500, description="Maximum number of records to return"),
    ):
        self.offset = offset
        self.limit = limit


# ── Request Models ───────────────────────────────────────

class WriteMemoryRequest(_BaseModel):
    content: str = Field(..., min_length=1, max_length=50000, description="Memory content to store")
    importance: str = Field("medium", description="Priority: high / medium / low")
    topics: Optional[List[str]] = Field(None, description="Explicit topic path list")
    nature_code: Optional[str] = Field(None, description="Nature code (explore, decision, etc.)")
    tool_codes: Optional[List[str]] = Field(None, description="Tool code list")
    knowledge_codes: Optional[List[str]] = Field(None, description="Knowledge type code list")
    person_code: str = Field("main", description="Persona port code")
    owner_agent_id: str = Field("_system", description="Owner agent identifier")
    visibility: str = Field("team", description="Visibility: private / team / public")
    ts: Optional[float] = Field(None, description="Unix timestamp override")

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())

        @field_validator("importance")
        @classmethod
        def _validate_importance_v2(cls, v: str) -> str:
            if v not in _VALID_IMPORTANCE:
                raise ValueError(f"importance must be one of {sorted(_VALID_IMPORTANCE)}")
            return v

    if not _PYDANTIC_V2:
        @validator("importance", allow_reuse=True)
        def _validate_importance_v1(cls, v):
            if v not in _VALID_IMPORTANCE:
                raise ValueError(f"importance must be one of {sorted(_VALID_IMPORTANCE)}")
            return v


class BatchWriteRequest(_BaseModel):
    messages: List[WriteMemoryRequest] = Field(..., min_length=1, max_length=50)

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


class RecallRequest(_BaseModel):
    query: str = Field(..., min_length=1, max_length=10000, description="Search query text")
    top_k: int = Field(10, ge=1, le=100, description="Number of results to return")
    importance: Optional[str] = Field(None, description="Filter by importance")
    topic_code: Optional[str] = Field(None, description="Filter by topic code")
    nature_code: Optional[str] = Field(None, description="Filter by nature code")
    person_id: Optional[str] = Field(None, description="Filter by person ID")
    keyword: Optional[str] = Field(None, description="Structured keyword filter")
    significance: Optional[str] = Field(None, description="Filter by significance")
    time_from: Optional[int] = Field(None, description="Start timestamp filter")
    time_to: Optional[int] = Field(None, description="End timestamp filter")
    query_agent_id: Optional[str] = Field(None, description="Agent ID for permission filtering")
    team_id: str = Field("default", description="Team ID for permission filtering")
    limit: int = Field(20, ge=1, le=200, description="Max primary results")
    semantic_weight: float = Field(0.5, ge=0.0, le=1.0, description="Semantic vs structured weight")

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


# ── Response Models ──────────────────────────────────────

class MemoryResponse(_BaseModel):
    memory_id: str
    time_id: str
    time_ts: int
    person_id: str
    nature_id: str
    content: str
    content_hash: str
    importance: str
    topics: List[dict] = []
    tools: List[str] = []
    knowledge: List[str] = []
    valence: Optional[float] = None
    arousal: Optional[float] = None
    dominance: Optional[float] = None
    significance: Optional[str] = None
    confidence: Optional[float] = None
    primary_emotions: Optional[dict] = None
    compound_emotions: Optional[list] = None

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


class WriteMemoryResponse(_BaseModel):
    memory_id: str
    time_id: Optional[str] = None
    person_id: Optional[str] = None
    nature_id: Optional[str] = None
    topics: Optional[List[str]] = None
    tools: Optional[List[str]] = None
    knowledge: Optional[List[str]] = None
    importance: Optional[str] = None
    task_id: Optional[str] = None
    emotion: Optional[dict] = None

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


class BatchWriteResponse(_BaseModel):
    written: int
    results: List[WriteMemoryResponse]

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


class RecallResultItem(_BaseModel):
    memory_id: str
    content: str
    importance: Optional[str] = None
    topics: Any = []
    time_ts: Optional[int] = None
    quality_score: Optional[float] = None
    rank_score: Optional[float] = None

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


class RecallResponse(_BaseModel):
    query: str
    search_mode: str
    total: int
    primary: List[dict]
    related: List[dict] = []
    causal_expansion: List[dict] = []
    cultural_associations: List[dict] = []
    phonetic_similar: List[dict] = []
    intent: str = "general"

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


class AgentProfileResponse(_BaseModel):
    agent_id: str
    agent_name: Optional[str] = None
    team_id: Optional[str] = None
    capabilities: List[str] = []
    status: Optional[str] = None
    memory_count: int = 0
    valence_avg: Optional[float] = None
    arousal_avg: Optional[float] = None
    dominance_avg: Optional[float] = None
    top_emotions: dict = {}
    top_topics: List[tuple] = []
    importance_distribution: dict = {}
    significance_distribution: dict = {}
    nature_distribution: dict = {}

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


class HealthResponse(_BaseModel):
    status: str
    version: str
    memories: int
    timestamp: int
    uptime_sec: float

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


# ═══════════════════════════════════════════════════════════
# Rate Limiter — time-based token bucket per agent_id
# ═══════════════════════════════════════════════════════════

class TokenBucketRateLimiter:
    """
    In-memory token bucket rate limiter.

    Each agent gets 100 tokens that refill at 100 tokens/minute.
    A request consumes 1 token.  When empty, 429 is returned.
    Stale buckets are expired every 300s via background thread.
    """

    def __init__(self, rate: int = 100, period: float = 60.0, max_buckets: int = 10000):
        self._rate = rate
        self._period = period
        self._max_buckets = max_buckets
        self._buckets: Dict[str, dict] = {}
        self._lock = threading.Lock()
        self._cleanup_interval = 300.0
        self._last_cleanup = time.monotonic()

    def acquire(self, agent_id: str) -> bool:
        now = time.monotonic()
        with self._lock:
            self._maybe_cleanup(now)

            bucket = self._buckets.get(agent_id)
            if bucket is None:
                if len(self._buckets) >= self._max_buckets:
                    stale = sorted(self._buckets.keys(), key=lambda k: self._buckets[k]["last_refill"])[0]
                    del self._buckets[stale]
                bucket = {"tokens": float(self._rate), "last_refill": now}
                self._buckets[agent_id] = bucket
            else:
                elapsed = now - bucket["last_refill"]
                refill = elapsed * (self._rate / self._period)
                bucket["tokens"] = min(float(self._rate), bucket["tokens"] + refill)
                bucket["last_refill"] = now

            if bucket["tokens"] >= 1.0:
                bucket["tokens"] -= 1.0
                return True
            return False

    def _maybe_cleanup(self, now: float):
        if now - self._last_cleanup < self._cleanup_interval:
            return
        cutoff = now - self._period * 2
        stale = [k for k, v in self._buckets.items() if v["last_refill"] < cutoff]
        for k in stale:
            del self._buckets[k]
        self._last_cleanup = now

    def status(self, agent_id: str) -> dict:
        with self._lock:
            bucket = self._buckets.get(agent_id)
            if bucket is None:
                return {"tokens": self._rate, "limit": self._rate, "period_sec": self._period}
            return {
                "tokens": round(max(0, bucket["tokens"]), 1),
                "limit": self._rate,
                "period_sec": self._period,
            }


_rate_limiter = TokenBucketRateLimiter(rate=100, period=60.0)


# ═══════════════════════════════════════════════════════════
# Component singletons (lazy init, thread-safe)
# ═══════════════════════════════════════════════════════════

_STORE = None
_ENCODER = None
_PIPELINE = None
_RECALL_ENGINE = None
_EMBEDDING_STORE = None
_QUALITY = None
_METRICS = None
_INIT_LOCK = threading.Lock()
_SERVER_START = time.time()
_DB_PATH: Optional[str] = None
_APP_VERSION = "12.0.0"


def _init_components():
    global _STORE, _ENCODER, _PIPELINE, _RECALL_ENGINE, _EMBEDDING_STORE, _QUALITY, _METRICS
    if _STORE is not None:
        return
    with _INIT_LOCK:
        if _STORE is not None:
            return

        from store import MemoryStore
        from encoder import DimensionEncoder
        from pipeline import IngestPipeline
        from recall import RecallEngine
        from metrics import MetricsCollector

        _STORE = MemoryStore(db_path=_DB_PATH)
        _ENCODER = DimensionEncoder()

        try:
            from embedding_store import EmbeddingStore
            _EMBEDDING_STORE = EmbeddingStore(
                db_path=_DB_PATH,
                conn_provider=lambda: _STORE.conn,
            )
            logger.info("Embedding store loaded")
        except Exception as e:
            logger.warning("api_v2: %s", e)
            _EMBEDDING_STORE = None

        _PIPELINE = IngestPipeline(
            store=_STORE,
            encoder=_ENCODER,
            embedding_store=_EMBEDDING_STORE,
        )

        _RECALL_ENGINE = RecallEngine(
            store=_STORE,
            encoder=_ENCODER,
            embedding_store=_EMBEDDING_STORE,
        )

        try:
            from quality import MemoryQuality
            _QUALITY = MemoryQuality(store=_STORE)
        except Exception as e:
            logger.warning("api_v2: %s", e)
            _QUALITY = None

        _METRICS = MetricsCollector(store=_STORE, pipeline=_PIPELINE, embedding_store=_EMBEDDING_STORE)
        logger.info("API v2 components initialized")


def get_store():
    _init_components()
    return _STORE


def get_encoder():
    _init_components()
    return _ENCODER


def get_pipeline():
    _init_components()
    return _PIPELINE


def get_recall_engine():
    _init_components()
    return _RECALL_ENGINE


def get_metrics_collector():
    _init_components()
    return _METRICS


def get_embedding_store():
    _init_components()
    return _EMBEDDING_STORE


# ═══════════════════════════════════════════════════════════
# FastAPI app factory
# ═══════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("api_v2 lifespan startup — initializing components")
    _init_components()
    yield
    logger.info("api_v2 lifespan shutdown — cleaning up")
    try:
        app_store = _STORE
        if app_store is not None:
            app_store.close_all()
    except Exception as e:
        logger.warning("api_v2: %s", e)


app = FastAPI(
    title="Agent Memory API v2",
    description="Production-grade REST API for the agent memory system (v8.7)",
    version=_APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.middleware("http")
async def add_deprecation_header(request, call_next):
    response = await call_next(request)
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "2025-12-31"
    response.headers["Link"] = '</v1/>; rel="successor-version"'
    return response


# ── Auth config ──────────────────────────────────────────

_AUTH_CONFIG = AuthConfig(
    jwt_secret=os.environ.get("AGENT_MEMORY_JWT_SECRET", ""),
    api_keys={},
    token_expiry_seconds=int(os.environ.get("AGENT_MEMORY_TOKEN_EXPIRY", "3600")),
)

_DEFAULT_JWT_SECRETS = {
    "xK9mP2vR7wL4nQ8jT5sF1yB6dH0cA3eG",
    "agent-memory-default-secret-change-in-production",
    "secret",
    "changeme",
    "my-secret-key",
    "my-secret",
    "default",
}


def _check_jwt_secret():
    s = _AUTH_CONFIG.jwt_secret
    allow_insecure = os.environ.get("AGENT_MEMORY_ALLOW_INSECURE", "").strip() in ("1", "true", "yes")

    if not s:
        logger.warning(
            "JWT_SECRET 为空，JWT 认证已禁用！"
            "请设置环境变量 AGENT_MEMORY_JWT_SECRET 为至少32字符的随机字符串以启用 JWT 认证。"
        )
        return

    if s in _DEFAULT_JWT_SECRETS or len(s) < 32:
        msg = (
            f"JWT_SECRET 使用默认值或过短(长度 {len(s)} < 32)! "
            f"请设置环境变量 AGENT_MEMORY_JWT_SECRET 为至少32字符的随机字符串。"
            f" 生成方式: python -c \"import secrets; print(secrets.token_urlsafe(48))\""
        )
        logger.critical(msg)
        if allow_insecure:
            logger.warning(
                "JWT_SECRET 正使用不安全默认值! "
                "请在启动前设置: export AGENT_MEMORY_JWT_SECRET=<random-64-char-string> "
                "AGENT_MEMORY_ALLOW_INSECURE 已设置，跳过启动阻止"
            )
        else:
            _env = os.environ.get("AGENT_MEMORY_ENV", "production").lower()
            if _env in ("production", "prod", "staging"):
                logger.critical(
                    f"FATAL: {msg} "
                    "如需在开发环境强制启动，请设置: AGENT_MEMORY_ALLOW_INSECURE=1"
                )
                raise RuntimeError(msg)
            logger.warning(
                "JWT_SECRET 正使用不安全默认值! "
                "请在启动前设置: export AGENT_MEMORY_JWT_SECRET=<random-64-char-string>"
            )


_check_jwt_secret()

# ── CORS middleware ───────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Remaining", "X-RateLimit-Limit", "Retry-After"],
)

# ── Auth middleware ───────────────────────────────────────

app.add_middleware(
    AuthMiddleware,
    config=_AUTH_CONFIG,
    exclude_paths=["/v1/health", "/docs", "/redoc", "/openapi.json"],
)


# ═══════════════════════════════════════════════════════════
# Rate Limiting Middleware (pure ASGI)
# ═══════════════════════════════════════════════════════════

_RATE_LIMITED_PATHS: frozenset = frozenset({
    "/v1/memories",
    "/v1/recall",
    "/v1/memories/batch",
})
_RATE_LIMIT_EXEMPT: frozenset = frozenset({"/v1/health", "/v1/metrics", "/docs", "/redoc", "/openapi.json"})


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    path = request.url.path.rstrip("/")

    if path in _RATE_LIMIT_EXEMPT or not any(
        path.startswith(p) for p in _RATE_LIMITED_PATHS
    ):
        return await call_next(request)

    agent_id = request.headers.get("X-Agent-ID", request.client.host if request.client else "unknown")

    if not _rate_limiter.acquire(agent_id):
        return _problem_detail(
            request=request,
            status=HTTP_429_TOO_MANY_REQUESTS,
            title="Too Many Requests",
            detail=f"Rate limit exceeded: 100 requests/minute per agent. Agent: {agent_id}",
            type_uri="https://tools.ietf.org/html/rfc6585#section-4",
        )

    status = _rate_limiter.status(agent_id)
    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(status["tokens"])
    response.headers["X-RateLimit-Limit"] = str(status["limit"])
    return response


# ═══════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════

def _extract_agent_id(request: Request) -> str:
    return request.headers.get("X-Agent-ID", "_system")


def _safe_content_preview(content: str, max_len: int = 500) -> str:
    return content[:max_len]


# ═══════════════════════════════════════════════════════════
# Exception Handlers
# ═══════════════════════════════════════════════════════════

@app.exception_handler(PydanticValidationError)
async def _pydantic_handler(request: Request, exc: Exception):
    errors = []
    raw_errors = getattr(exc, "errors", None)
    if raw_errors is None:
        raw_errors = []
    for err in raw_errors:
        errors.append({
            "loc": list(err.get("loc", [])),
            "msg": err.get("msg", "validation error"),
            "type": err.get("type", "value_error"),
        })
    return _problem_detail(
        request=request,
        status=HTTP_400_BAD_REQUEST,
        title="Validation Error",
        detail="The request body failed validation.",
        type_uri="https://docs.pydantic.dev/latest/errors/validation_errors/",
        errors=errors,
    )


@app.exception_handler(HTTPException)
async def _http_exception_handler(request: Request, exc: HTTPException):
    return _problem_detail(
        request=request,
        status=exc.status_code,
        title="Request Error",
        detail=str(exc.detail),
    )


@app.exception_handler(Exception)
async def _generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    return _problem_detail(
        request=request,
        status=HTTP_500_INTERNAL_SERVER_ERROR,
        title="Internal Server Error",
        detail="An unexpected error occurred.",
    )


# ═══════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════

@app.get("/v1/health", response_model=HealthResponse, tags=["System"])
async def health_check(request: Request):
    store = get_store()
    count = 0
    try:
        count = store.conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    except Exception as e:
        logger.warning("api_v2: %s", e)
    return HealthResponse(
        status="ok",
        version=_APP_VERSION,
        memories=count,
        timestamp=int(time.time()),
        uptime_sec=round(time.time() - _SERVER_START, 1),
    )


@app.get("/v1/metrics", tags=["System"])
async def metrics_endpoint(
    request: Request,
    fmt: str = Query("prometheus", description="Format: prometheus or json"),
):
    collector = get_metrics_collector()
    if fmt == "json":
        summary = collector.get_summary()
        return JSONResponse(content=summary)
    prom = collector.export_prometheus()
    return PlainTextResponse(content=prom, media_type="text/plain; version=0.0.4; charset=utf-8")


# ── Memory CRUD ───────────────────────────────────────────

@app.post(
    "/v1/memories",
    response_model=WriteMemoryResponse,
    status_code=201,
    tags=["Memories"],
)
async def write_memory(request: Request, body: WriteMemoryRequest):
    pipeline = get_pipeline()
    metrics = get_metrics_collector()

    try:
        t_start = time.monotonic()
        result = pipeline.ingest(
            content=body.content,
            person_code=body.person_code,
            ts=body.ts,
            topics=body.topics,
            nature_code=body.nature_code,
            tool_codes=body.tool_codes,
            knowledge_codes=body.knowledge_codes,
            importance=body.importance,
            owner_agent_id=body.owner_agent_id,
            visibility=body.visibility,
        )
        elapsed_ms = (time.monotonic() - t_start) * 1000
        metrics.record_write(latency_ms=elapsed_ms, success=True)

        safe_result: dict = {}
        for key in WriteMemoryResponse.__fields__ if hasattr(WriteMemoryResponse, '__fields__') else WriteMemoryResponse.model_fields:
            if key in result:
                safe_result[key] = result[key]

        if "skipped" in result and result["skipped"]:
            return JSONResponse(
                status_code=200,
                content={"memory_id": None, "skipped": True, "reason": result.get("reason")},
            )

        content_preview = body.content[:200]
        safe_content = content_preview.replace("\n", " ").replace("\r", "")

        logger.info(
            "memory_created: mid=%s nature=%s importance=%s topics=%s content=%.200s",
            result.get("memory_id"),
            result.get("nature_id"),
            body.importance,
            body.topics,
            safe_content,
        )

        return JSONResponse(status_code=201, content=result)

    except RuntimeError as exc:
        logger.error(f"Write transaction failed: {exc}")
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Write Transaction Failed",
            detail=str(exc),
        )
    except Exception as exc:
        logger.error(f"Write failed: {exc}", exc_info=True)
        metrics.record_write(success=False)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Memory Write Failed",
            detail="Internal error during memory write.",
        )


@app.post(
    "/v1/memories/batch",
    response_model=BatchWriteResponse,
    status_code=201,
    tags=["Memories"],
)
async def batch_write(request: Request, body: BatchWriteRequest):
    pipeline = get_pipeline()
    metrics = get_metrics_collector()
    results: list = []

    try:
        for msg in body.messages:
            t_start = time.monotonic()
            result = pipeline.ingest(
                content=msg.content,
                person_code=msg.person_code,
                ts=msg.ts,
                topics=msg.topics,
                nature_code=msg.nature_code,
                tool_codes=msg.tool_codes,
                knowledge_codes=msg.knowledge_codes,
                importance=msg.importance,
                owner_agent_id=msg.owner_agent_id,
                visibility=msg.visibility,
                skip_throttle=True,
            )
            elapsed_ms = (time.monotonic() - t_start) * 1000
            metrics.record_write(latency_ms=elapsed_ms, success=True)
            results.append(result)

        return JSONResponse(
            status_code=201,
            content=BatchWriteResponse(written=len(results), results=results).model_dump()
            if _PYDANTIC_V2 else
            {"written": len(results), "results": results},
        )
    except Exception as exc:
        logger.error(f"Batch write failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Batch Write Failed",
            detail="Internal error during batch write.",
        )


@app.get(
    "/v1/memories/{memory_id}",
    response_model=MemoryResponse,
    tags=["Memories"],
)
async def get_memory(request: Request, memory_id: str):
    store = get_store()
    mem = store.get_memory(memory_id)
    if mem is None:
        return _problem_detail(
            request=request,
            status=HTTP_404_NOT_FOUND,
            title="Memory Not Found",
            detail=f"No memory found with id '{memory_id}'.",
        )
    content = _safe_content_preview(mem.get("content", ""))
    mem["content"] = content
    return JSONResponse(content=mem)


# ── Recall ────────────────────────────────────────────────

@app.post(
    "/v1/recall",
    response_model=RecallResponse,
    tags=["Recall"],
)
async def recall(request: Request, body: RecallRequest):
    engine = get_recall_engine()
    metrics = get_metrics_collector()
    embedding_store = get_embedding_store()
    store = get_store()
    encoder = get_encoder()

    try:
        t_start = time.monotonic()

        nature_id = None
        if body.nature_code:
            try:
                nature_id = encoder.encode_nature(body.nature_code)
            except ValueError as e:
                logger.debug("api_v2: invalid nature_code: %s", e)

        query_agent_id = body.query_agent_id or _extract_agent_id(request)

        if embedding_store is not None:
            result = engine.recall(
                query=body.query,
                keyword=body.keyword,
                time_from=body.time_from,
                time_to=body.time_to,
                person_id=body.person_id,
                nature_code=body.nature_code,
                topic_path=body.topic_code,
                importance=body.importance,
                significance=body.significance,
                limit=body.limit,
                semantic_weight=body.semantic_weight,
                query_agent_id=query_agent_id,
                team_id=body.team_id,
            )
        else:
            effective_keyword = body.keyword or body.query
            structured_results = store.query(
                keyword=effective_keyword,
                time_from=body.time_from,
                time_to=body.time_to,
                person_id=body.person_id,
                nature_id=nature_id,
                topic_code=body.topic_code,
                importance=body.importance,
                significance=body.significance,
                limit=body.top_k * 2,
                query_agent_id=query_agent_id,
                team_id=body.team_id,
            )

            for mem in structured_results:
                mem["_rank_score"] = 0.5

            result = {
                "search_mode": "structured",
                "total": len(structured_results),
                "primary": structured_results[:body.top_k],
                "related": [],
                "causal_expansion": [],
                "cultural_associations": [],
                "phonetic_similar": [],
                "query": body.query,
                "intent": "general",
            }

        elapsed_ms = (time.monotonic() - t_start) * 1000
        primary_count = len(result.get("primary", []))
        metrics.record_recall(latency_ms=elapsed_ms, result_count=primary_count)

        primary = result.get("primary", [])
        for mem in primary:
            c = mem.get("content", "")
            if c:
                mem["content"] = _safe_content_preview(c, 500)

        return JSONResponse(content={
            "query": body.query,
            "search_mode": result.get("search_mode", "hybrid"),
            "total": result.get("total", 0),
            "primary": primary,
            "related": result.get("related", [])[:10],
            "causal_expansion": result.get("causal_expansion", []),
            "cultural_associations": result.get("cultural_associations", []),
            "phonetic_similar": result.get("phonetic_similar", []),
            "intent": result.get("intent", "general"),
        })

    except Exception as exc:
        logger.error(f"Recall failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Recall Failed",
            detail="Internal error during memory recall.",
        )


# ── Agent Profile ────────────────────────────────────────

@app.get(
    "/v1/agents/{agent_id}/profile",
    response_model=AgentProfileResponse,
    tags=["Agents"],
)
async def agent_profile(request: Request, agent_id: str):
    store = get_store()

    try:
        agent = store.get_agent(agent_id)
        if agent is None:
            store.register_agent(agent_id, agent_id, team_id="default")
            agent = store.get_agent(agent_id)

        agent_name = agent.get("agent_name", agent_id) if agent else agent_id
        team_id = agent.get("team_id", "default") if agent else "default"
        capabilities = agent.get("capabilities", []) if agent else []
        status = agent.get("status", "active") if agent else "active"

        stats = store.get_aggregated_stats(owner_agent_id=agent_id)

        n = max(stats["total_memories"], 1)
        top_emotions = {
            e: round(v / n, 4)
            for e, v in sorted(stats["emotion_sums"].items(), key=lambda x: -x[1])[:4]
        }
        sorted_topics = sorted(stats["topic_distribution"].items(), key=lambda x: -x[1])[:10]

        return JSONResponse(content={
            "agent_id": agent_id,
            "agent_name": agent_name,
            "team_id": team_id,
            "capabilities": capabilities,
            "status": status,
            "memory_count": stats["total_memories"],
            "valence_avg": round(stats["avg_valence"], 4) if stats["total_memories"] > 0 else None,
            "arousal_avg": round(stats["avg_arousal"], 4) if stats["total_memories"] > 0 else None,
            "dominance_avg": round(stats["avg_dominance"], 4) if stats["total_memories"] > 0 else None,
            "top_emotions": top_emotions,
            "top_topics": [(t, c) for t, c in sorted_topics],
            "importance_distribution": stats["importance_distribution"],
            "significance_distribution": stats["significance_distribution"],
            "nature_distribution": stats["nature_distribution"],
        })

    except Exception as exc:
        logger.error(f"Agent profile failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Profile Retrieval Failed",
            detail="Internal error building agent profile.",
        )


# ── Rate Limiter Status ─────────────────────────────────

@app.get("/v1/ratelimit-status", tags=["System"])
async def ratelimit_status(request: Request):
    agent_id = _extract_agent_id(request)
    return JSONResponse(content=_rate_limiter.status(agent_id))


# ═══════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════

def main():
    import argparse
    argp = argparse.ArgumentParser(description="Agent Memory API v2 (FastAPI)")
    argp.add_argument("--host", default="127.0.0.1", help="Bind address")
    argp.add_argument("--port", type=int, default=8978, help="Bind port")
    argp.add_argument("--db", default=None, help="SQLite database path override")
    argp.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = argp.parse_args()

    from logging_config import configure_logging
    configure_logging(level=args.log_level)

    global _DB_PATH
    _DB_PATH = args.db

    logger.info(f"Agent Memory API v2 ({_APP_VERSION}) starting on http://{args.host}:{args.port}")
    logger.info(f"  Docs:    http://localhost:{args.port}/docs")
    logger.info(f"  Health:  http://localhost:{args.port}/v1/health")
    logger.info(f"  Metrics: http://localhost:{args.port}/v1/metrics")

    uvicorn.run(
        "agent_memory.api_v2:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level.lower(),
        reload=False,
    )


if __name__ == "__main__":
    main()