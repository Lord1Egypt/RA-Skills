"""
api_v3.py - Async HTTP API v3 with SSE — tenant-isolated FastAPI service (v8.8)

Endpoints:
  POST   /v1/tenants              - Create tenant (requires admin)
  DELETE /v1/tenants/{tenant_id}  - Delete tenant (requires admin)
  POST   /v1/auth/token           - Issue JWT token
  POST   /v1/memories             - Async write with tenant isolation
  POST   /v1/recall               - Async recall with tenant isolation
  GET    /v1/events/{tenant_id}   - SSE stream of real-time memory events
  GET    /v1/health               - Health check with tenant stats
  GET    /v1/metrics              - Prometheus metrics with per-tenant breakdown
  GET    /docs                    - Swagger UI (auto-generated)

Features:
  - AuthMiddleware integration (JWT + API Key)
  - TenantContext dependency injection
  - Per-tenant rate limiting (token bucket)
  - SSE streaming via MemoryEventBus
  - Pydantic v2 models (v1 fallback)
  - RFC 7807 Problem Details error responses
  - CORS, Swagger / ReDoc, OpenAPI schema

Usage:
  uvicorn agent_memory.api_v3:app --host 127.0.0.1 --port 8988
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
import threading
import time
import uuid
from contextlib import asynccontextmanager
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
from fastapi import FastAPI, Request, HTTPException, Depends, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, StreamingResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import agent_memory.auth_middleware as _auth_mod
from agent_memory.auth_middleware import (
    AuthConfig,
    AuthMiddleware,
    TenantAuth,
    TenantContext,
    _DEFAULT_JWT_SECRET,
    get_tenant_context,
    require_permission,
)
from agent_memory.event_bus import MemoryEventBus, SSEAdapter

try:
    from .document_parser import DocumentParser
    _HAS_DOCUMENT_PARSER = True
except ImportError:
    _HAS_DOCUMENT_PARSER = False

try:
    from .semantic_chunker import SemanticChunker
    _HAS_SEMANTIC_CHUNKER = True
except ImportError:
    _HAS_SEMANTIC_CHUNKER = False

try:
    from .chunk_indexer import ChunkIndexer
    _HAS_CHUNK_INDEXER = True
except ImportError:
    _HAS_CHUNK_INDEXER = False

try:
    from .chunk_retriever import ChunkRetriever
    _HAS_CHUNK_RETRIEVER = True
except ImportError:
    _HAS_CHUNK_RETRIEVER = False

try:
    from .chat_parser import ChatParser
    from .personality_analyzer import PersonalityAnalyzer
    from .personality_memory import PersonalityMemory
    _HAS_PERSONALITY = True
except ImportError:
    _HAS_PERSONALITY = False

logger = logging.getLogger(__name__)

MAX_DOCUMENT_TEXT_LENGTH = 500000  # 500KB max text length

_ALLOW_INSECURE: bool = os.environ.get("AGENT_MEMORY_ALLOW_INSECURE", "").strip() in ("1", "true", "yes")

# ═══════════════════════════════════════════════════════════
# RFC 7807 helpers
# ═══════════════════════════════════════════════════════════

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
# Pydantic Models (v2‑compatible, v1 fallback)
# ═══════════════════════════════════════════════════════════

_VALID_IMPORTANCE = frozenset({"high", "medium", "low"})
_VALID_SIGNIFICANCE = frozenset({"trivial", "notable", "important", "breakthrough", "crisis", "milestone"})
_VALID_VISIBILITY = frozenset({"private", "team", "public"})


def _create_model_config() -> dict:
    if _PYDANTIC_V2:
        return {"populate_by_name": True, "extra": "forbid"}
    return {}


class PaginationParams:
    def __init__(
        self,
        offset: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(50, ge=1, le=500, description="Maximum number of records to return"),
    ):
        self.offset = offset
        self.limit = limit


# ── Request Models ───────────────────────────────────────

class CreateTenantRequest(_BaseModel):
    tenant_id: str = Field(..., min_length=1, max_length=128, description="Unique tenant identifier")
    agent_id: str = Field("admin", description="Initial admin agent identifier")
    permissions: List[str] = Field(default_factory=lambda: ["admin", "read", "write"])
    metadata: Optional[Dict[str, Any]] = Field(None, description="Arbitrary tenant metadata")

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


class TokenRequest(_BaseModel):
    tenant_id: str = Field(..., min_length=1, max_length=128)
    agent_id: str = Field(..., min_length=1, max_length=128)
    permissions: List[str] = Field(default_factory=lambda: ["read", "write"])
    expiry_seconds: Optional[int] = Field(None, ge=60, le=86400, description="Token TTL in seconds")

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


class WriteMemoryRequest(_BaseModel):
    content: str = Field(..., min_length=1, max_length=50000, description="Memory content to store")
    importance: str = Field("medium", description="Priority: high / medium / low")
    topics: Optional[List[str]] = Field(None, description="Explicit topic path list")
    nature_code: Optional[str] = Field(None, description="Nature code")
    tool_codes: Optional[List[str]] = Field(None, description="Tool code list")
    knowledge_codes: Optional[List[str]] = Field(None, description="Knowledge type code list")
    person_code: str = Field("main", description="Persona port code")
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
    team_id: str = Field("default", description="Team ID for permission filtering")
    limit: int = Field(20, ge=1, le=200, description="Max primary results")
    semantic_weight: float = Field(0.5, ge=0.0, le=1.0, description="Semantic vs structured weight")

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


# ── Response Models ──────────────────────────────────────

class TenantResponse(_BaseModel):
    tenant_id: str
    agent_id: str
    permissions: List[str]
    created_at: float

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


class TokenResponse(_BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    tenant_id: str
    agent_id: str
    permissions: List[str]

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


class HealthResponse(_BaseModel):
    status: str
    version: str
    memories: int
    tenants: int
    timestamp: int
    uptime_sec: float

    if _PYDANTIC_V2:
        model_config = ConfigDict(**_create_model_config())


# ═══════════════════════════════════════════════════════════
# Rate Limiter — per-tenant token bucket
# ═══════════════════════════════════════════════════════════

class TenantRateLimiter:
    """
    In-memory per-tenant token bucket rate limiter.

    Each tenant gets ``rate`` tokens that refill at ``rate`` / ``period``.
    A request consumes 1 token.  Returns 429 when empty.
    """

    def __init__(self, rate: int = 100, period: float = 60.0, max_buckets: int = 10000):
        self._rate = rate
        self._period = period
        self._max_buckets = max_buckets
        self._buckets: Dict[str, dict] = {}
        self._lock = threading.Lock()
        self._cleanup_interval = 300.0
        self._last_cleanup = time.monotonic()

    def acquire(self, tenant_id: str) -> bool:
        now = time.monotonic()
        with self._lock:
            self._maybe_cleanup(now)

            bucket = self._buckets.get(tenant_id)
            if bucket is None:
                if len(self._buckets) >= self._max_buckets:
                    stale = sorted(self._buckets.keys(), key=lambda k: self._buckets[k]["last_refill"])[0]
                    del self._buckets[stale]
                bucket = {"tokens": float(self._rate), "last_refill": now}
                self._buckets[tenant_id] = bucket
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

    def status(self, tenant_id: str) -> dict:
        with self._lock:
            bucket = self._buckets.get(tenant_id)
            if bucket is None:
                return {"tokens": self._rate, "limit": self._rate, "period_sec": self._period}
            return {
                "tokens": round(max(0, bucket["tokens"]), 1),
                "limit": self._rate,
                "period_sec": self._period,
            }


_tenant_rate_limiter = TenantRateLimiter(rate=100, period=60.0)


# ═══════════════════════════════════════════════════════════
# Singleton components
# ═══════════════════════════════════════════════════════════

_STORE = None
_ENCODER = None
_PIPELINE = None
_RECALL_ENGINE = None
_EMBEDDING_STORE = None
_METRICS = None
_EVENT_BUS = None
_SSE_ADAPTER = None
_ISOLATION_MANAGER = None
_TENANT_AUTH = None
_DOCUMENT_PARSER = None
_SEMANTIC_CHUNKER = None
_CHUNK_INDEXER = None
_CHUNK_RETRIEVER = None
_INIT_LOCK = threading.Lock()
_MEMORY_INSTANCES: Dict[str, 'AgentMemory'] = {}
_MEMORY_INSTANCES_LOCK = threading.Lock()

def _get_memory(db_path: str) -> 'AgentMemory':
    if db_path not in _MEMORY_INSTANCES:
        with _MEMORY_INSTANCES_LOCK:
            if db_path not in _MEMORY_INSTANCES:
                from memory_system import AgentMemory
                _MEMORY_INSTANCES[db_path] = AgentMemory(db_path=db_path)
    return _MEMORY_INSTANCES[db_path]

def _shutdown_memory_instances():
    with _MEMORY_INSTANCES_LOCK:
        for key, mem in list(_MEMORY_INSTANCES.items()):
            try:
                mem.close()
            except Exception as e:
                logger.warning("api_v3: closing memory instance %s: %s", key, e)
        _MEMORY_INSTANCES.clear()

_SERVER_START = time.time()
_DB_PATH: Optional[str] = None
_APP_VERSION = "8.8"

# In-memory tenant registry for the API layer
_tenant_registry: Dict[str, dict] = {}
_tenant_registry_lock = threading.Lock()

_AUTH_CONFIG = AuthConfig(
    jwt_secret=os.environ.get("AGENT_MEMORY_JWT_SECRET", _DEFAULT_JWT_SECRET),
    api_keys={},
    token_expiry_seconds=int(os.environ.get("AGENT_MEMORY_TOKEN_EXPIRY", "3600")),
)

_jwt_secret = os.environ.get("AGENT_MEMORY_JWT_SECRET", _DEFAULT_JWT_SECRET)
if _jwt_secret == _DEFAULT_JWT_SECRET:
    _env = os.environ.get("AGENT_MEMORY_ENV", "production").lower()
    if _env in ("production", "prod", "staging"):
        raise ValueError("JWT secret must be changed from default in production. Set AGENT_MEMORY_JWT_SECRET.")

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

    # 空字符串 → JWT 认证已禁用（开发模式）
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
            logger.critical(
                f"FATAL: {msg} "
                "如需在开发环境强制启动，请设置: AGENT_MEMORY_ALLOW_INSECURE=1"
            )
            raise RuntimeError(msg)


_check_jwt_secret()


def _init_components():
    global _STORE, _ENCODER, _PIPELINE, _RECALL_ENGINE
    global _EMBEDDING_STORE, _METRICS, _EVENT_BUS, _SSE_ADAPTER
    global _ISOLATION_MANAGER, _TENANT_AUTH
    global _DOCUMENT_PARSER, _SEMANTIC_CHUNKER, _CHUNK_INDEXER, _CHUNK_RETRIEVER

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
            logger.warning("api_v3: %s", e)
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

        _METRICS = MetricsCollector(store=_STORE, pipeline=_PIPELINE, embedding_store=_EMBEDDING_STORE)

        _EVENT_BUS = MemoryEventBus()
        _SSE_ADAPTER = SSEAdapter(_EVENT_BUS)

        try:
            from tenant import TenantIsolationManager
            _ISOLATION_MANAGER = TenantIsolationManager(
                store=_STORE,
                config={"strategy": "shared_db"},
            )
            logger.info("Tenant isolation manager loaded")
        except Exception as e:
            logger.warning("api_v3: %s", e)
            _ISOLATION_MANAGER = None

        _TENANT_AUTH = TenantAuth(_AUTH_CONFIG)

        if _HAS_DOCUMENT_PARSER:
            try:
                _DOCUMENT_PARSER = DocumentParser()
                logger.info("Document parser loaded")
            except Exception as e:
                logger.warning("api_v3: DocumentParser init failed: %s", e)
                _DOCUMENT_PARSER = None

        if _HAS_SEMANTIC_CHUNKER:
            try:
                _SEMANTIC_CHUNKER = SemanticChunker()
                logger.info("Semantic chunker loaded")
            except Exception as e:
                logger.warning("api_v3: SemanticChunker init failed: %s", e)
                _SEMANTIC_CHUNKER = None

        if _HAS_CHUNK_INDEXER:
            try:
                _CHUNK_INDEXER = ChunkIndexer(
                    store=_STORE,
                    encoder=_ENCODER,
                    embedding_store=_EMBEDDING_STORE,
                )
                logger.info("Chunk indexer loaded")
            except Exception as e:
                logger.warning("api_v3: ChunkIndexer init failed: %s", e)
                _CHUNK_INDEXER = None

        if _HAS_CHUNK_RETRIEVER:
            try:
                _CHUNK_RETRIEVER = ChunkRetriever(
                    store=_STORE,
                    embedding_store=_EMBEDDING_STORE,
                )
                logger.info("Chunk retriever loaded")
            except Exception as e:
                logger.warning("api_v3: ChunkRetriever init failed: %s", e)
                _CHUNK_RETRIEVER = None

        logger.info("API v3 components initialized")


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


def get_event_bus() -> MemoryEventBus:
    _init_components()
    return _EVENT_BUS


def get_sse_adapter() -> SSEAdapter:
    _init_components()
    return _SSE_ADAPTER


def get_isolation_manager():
    _init_components()
    return _ISOLATION_MANAGER


def get_tenant_auth() -> TenantAuth:
    _init_components()
    return _TENANT_AUTH


def get_auth_config() -> AuthConfig:
    return _AUTH_CONFIG


def get_document_parser():
    _init_components()
    return _DOCUMENT_PARSER


def get_semantic_chunker():
    _init_components()
    return _SEMANTIC_CHUNKER


def get_chunk_indexer():
    _init_components()
    return _CHUNK_INDEXER


def get_chunk_retriever():
    _init_components()
    return _CHUNK_RETRIEVER


# ═══════════════════════════════════════════════════════════
# FastAPI app factory
# ═══════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("api_v3 lifespan startup — initializing components")
    _init_components()
    try:
        event_bus = _EVENT_BUS
        if event_bus is not None:
            await event_bus._ensure_started()
        logger.info("Event bus started for lifespan")
    except Exception as e:
        logger.warning("api_v3: %s", e)
    yield
    logger.info("api_v3 lifespan shutdown — cleaning up")
    try:
        _shutdown_memory_instances()
    except Exception as e:
        logger.warning("api_v3: %s", e)
    try:
        event_bus = _EVENT_BUS
        if event_bus is not None:
            await event_bus.close()
    except Exception as e:
        logger.warning("api_v3: %s", e)
    try:
        app_store = _STORE
        if app_store is not None:
            app_store.close_all()
    except Exception as e:
        logger.warning("api_v3: %s", e)
    try:
        isolation = _ISOLATION_MANAGER
        if isolation is not None:
            isolation.close()
    except Exception as e:
        logger.warning("api_v3: %s", e)


app = FastAPI(
    title="Agent Memory API v3",
    description="Async, tenant-isolated REST + SSE API for the agent memory system (v12)",
    version=_APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ── CORS middleware ───────────────────────────────────────

_cors_origins_str = os.environ.get("AGENT_MEMORY_CORS_ORIGINS", "")
if _cors_origins_str.strip():
    _cors_origins = [o.strip() for o in _cors_origins_str.split(",") if o.strip()]
    _cors_allow_credentials = True
else:
    _cors_origins = ["*"]
    _cors_allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=_cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Remaining", "X-RateLimit-Limit", "Retry-After"],
)

# ── Auth middleware ───────────────────────────────────────

_AUTH_EXCLUDED: List[str] = [
    "/docs",
    "/redoc",
    "/openapi.json",
    "/v1/health",
    "/v1/health/live",
    "/v1/health/ready",
]

from agent_memory.auth_middleware import FastAPIAuthMiddleware

app.add_middleware(
    FastAPIAuthMiddleware,
    config=_AUTH_CONFIG,
    exclude_paths=_AUTH_EXCLUDED,
)


# ── Trace Context Middleware ───────────────────────────────

@app.middleware("http")
async def trace_context_middleware(request: Request, call_next):
    """Auto-propagate trace context for request correlation."""
    # Generate or extract trace_id
    trace_id = request.headers.get("traceparent", "").split("-")[-1] if request.headers.get("traceparent") else str(uuid.uuid4())[:16]
    request_id = str(uuid.uuid4())[:8]

    # Store in request state for downstream use
    request.state.trace_id = trace_id
    request.state.request_id = request_id

    # Process request
    response = await call_next(request)

    # Add trace headers to response
    response.headers["X-Trace-ID"] = trace_id
    response.headers["X-Request-ID"] = request_id

    return response


# ═══════════════════════════════════════════════════════════
# Per-tenant Rate Limiting Middleware
# ═══════════════════════════════════════════════════════════

_RATE_LIMITED_PATHS_V3: frozenset = frozenset({
    "/v1/memories",
    "/v1/recall",
    "/v1/documents/upload",
    "/v1/documents/text",
    "/v1/documents/search",
})
_RATE_LIMIT_EXEMPT_V3: frozenset = frozenset({
    "/v1/health",
    "/v1/health/live",
    "/v1/health/ready",
    "/v1/metrics",
    "/v1/auth/token",
    "/docs",
    "/redoc",
    "/openapi.json",
})


@app.middleware("http")
async def tenant_rate_limit_middleware(request: Request, call_next):
    _allow_insecure = _ALLOW_INSECURE

    path = request.url.path.rstrip("/")

    if path in _RATE_LIMIT_EXEMPT_V3 or not any(
        path.startswith(p) for p in _RATE_LIMITED_PATHS_V3
    ):
        response = await call_next(request)
    else:
        tenant_id = request.scope.get("_auth_tenant_id", getattr(request.state, "tenant_id", None))

        if tenant_id is None:
            response = await call_next(request)
        elif not _tenant_rate_limiter.acquire(tenant_id):
            return _problem_detail(
                request=request,
                status=HTTP_429_TOO_MANY_REQUESTS,
                title="Too Many Requests",
                detail=f"Rate limit exceeded: 100 requests/minute per tenant. Tenant: {tenant_id}",
                type_uri="https://tools.ietf.org/html/rfc6585#section-4",
            )
        else:
            rl_status = _tenant_rate_limiter.status(tenant_id)
            response = await call_next(request)
            response.headers["X-RateLimit-Remaining"] = str(rl_status["tokens"])
            response.headers["X-RateLimit-Limit"] = str(rl_status["limit"])

    if _allow_insecure:
        response.headers["X-Insecure-Mode"] = "true"

    return response


# ═══════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════

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

# ── Health Check ─────────────────────────────────────────

@app.get("/v1/health", response_model=HealthResponse, tags=["System"])
async def health_check(request: Request):
    store = get_store()
    count = 0
    try:
        count = await asyncio.to_thread(
            lambda: store.conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        )
    except Exception as e:
        logger.warning("api_v3: %s", e)

    tenant_count = 0
    try:
        isolation = get_isolation_manager()
        if isolation is not None:
            tenant_count = len(isolation.list_tenants())
    except Exception as e:
        logger.warning("api_v3: %s", e)

    return HealthResponse(
        status="ok",
        version=_APP_VERSION,
        memories=count,
        tenants=tenant_count,
        timestamp=int(time.time()),
        uptime_sec=round(time.time() - _SERVER_START, 1),
    )


@app.get("/v1/health/live", tags=["System"])
async def liveness_probe():
    """Liveness probe — is the process alive?"""
    return {"status": "alive"}


@app.get("/v1/health/ready", tags=["System"])
async def readiness_probe():
    """Readiness probe — is the system ready to serve requests?"""
    if not memory_system or not memory_system.store:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "reason": "Memory system not initialized"}
        )

    health = memory_system.health_check()
    if health.get("status") == "unhealthy":
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "health": health}
        )

    return {"status": "ready", "health": health}


# ── Metrics ──────────────────────────────────────────────

@app.get("/v1/metrics", tags=["System"])
async def metrics_endpoint(
    request: Request,
    fmt: str = Query("prometheus", description="Format: prometheus or json"),
):
    collector = get_metrics_collector()
    if fmt == "json":
        summary = collector.get_summary()
        isolation = get_isolation_manager()
        if isolation is not None:
            try:
                summary["tenants"] = isolation.get_all_tenant_stats()
            except Exception as e:
                logger.warning("api_v3: %s", e)
        return JSONResponse(content=summary)

    prom_lines = [
        collector.export_prometheus(),
    ]

    isolation = get_isolation_manager()
    if isolation is not None:
        prom_lines.append("")
        prom_lines.append("# HELP agent_memory_tenants_total Number of registered tenants")
        prom_lines.append("# TYPE agent_memory_tenants_total gauge")
        prom_lines.append(f"agent_memory_tenants_total {len(isolation.list_tenants())}")
        prom_lines.append("")

        try:
            for stats in isolation.get_all_tenant_stats():
                tid = stats.get("tenant_id", "")
                prom_lines.append(f'agent_memory_tenant_memory_count{{tenant_id="{tid}"}} {stats.get("memory_count", 0)}')
                prom_lines.append(f'agent_memory_tenant_storage_bytes{{tenant_id="{tid}"}} {stats.get("storage_size_bytes", 0)}')
        except Exception as e:
            logger.warning("api_v3: %s", e)
        prom_lines.append("")

    return PlainTextResponse(content="\n".join(prom_lines), media_type="text/plain; version=0.0.4; charset=utf-8")


# ── Tenant Management ────────────────────────────────────

@app.post(
    "/v1/tenants",
    response_model=TenantResponse,
    status_code=201,
    tags=["Tenants"],
)
async def create_tenant(
    request: Request,
    body: CreateTenantRequest,
    _perm=require_permission("admin"),
):
    isolation = get_isolation_manager()
    auth = get_tenant_auth()

    if isolation is None:
        raise HTTPException(status_code=503, detail="Tenant isolation not available")

    try:
        isolation.create_tenant(body.tenant_id, metadata=body.metadata)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail="Tenant creation conflict")

    token = auth.create_token(
        tenant_id=body.tenant_id,
        agent_id=body.agent_id,
        permissions=body.permissions,
    )

    bus = get_event_bus()
    if bus is not None:
        await bus.emit(
            "team.shared",
            {"action": "tenant.created", "tenant_id": body.tenant_id},
            tenant_id=body.tenant_id,
        )

    return JSONResponse(
        status_code=201,
        content={
            "tenant_id": body.tenant_id,
            "agent_id": body.agent_id,
            "permissions": body.permissions,
            "created_at": time.time(),
            "access_token": token,
        },
    )


@app.delete(
    "/v1/tenants/{tenant_id}",
    status_code=200,
    tags=["Tenants"],
)
async def delete_tenant(
    request: Request,
    tenant_id: str,
    _perm=require_permission("admin"),
):
    isolation = get_isolation_manager()

    if isolation is None:
        raise HTTPException(status_code=503, detail="Tenant isolation not available")

    deleted = isolation.delete_tenant(tenant_id)
    if not deleted:
        return _problem_detail(
            request=request,
            status=HTTP_404_NOT_FOUND,
            title="Tenant Not Found",
            detail=f"No tenant found with id '{tenant_id}'.",
        )

    bus = get_event_bus()
    if bus is not None:
        await bus.emit(
            "team.shared",
            {"action": "tenant.deleted", "tenant_id": tenant_id},
            tenant_id=tenant_id,
        )

    return JSONResponse(status_code=200, content={"tenant_id": tenant_id, "deleted": True})


# ── Auth ─────────────────────────────────────────────────

@app.post(
    "/v1/auth/token",
    response_model=TokenResponse,
    tags=["Auth"],
)
async def issue_token(request: Request, body: TokenRequest):
    allow_insecure = _ALLOW_INSECURE

    # 使用默认密钥时拒绝签发管理员 token
    if _AUTH_CONFIG.is_default_secret() and "admin" in body.permissions:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Cannot issue admin tokens with default JWT secret. "
                   "Set AGENT_MEMORY_JWT_SECRET environment variable to a strong random key first.",
        )

    if allow_insecure:
        client_host = request.client.host if request.client else "unknown"
        if client_host not in ("127.0.0.1", "::1", "localhost"):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Insecure mode token issuance only allowed from localhost",
            )

    if not allow_insecure:
        api_key = request.headers.get("x-api-key", "")
        auth_header = request.headers.get("authorization", "")
        auth = get_tenant_auth()

        if api_key:
            key_info = auth.verify_key(api_key)
            if key_info is None or "admin" not in key_info.get("permissions", []):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="API Key must have admin permission to issue tokens",
                )
        elif auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
            token_info = auth.verify_token(token)
            if token_info is None:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="JWT token is invalid",
                )
            if token_info.get("_expired"):
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="JWT token has expired",
                )
            if "admin" not in token_info.get("permissions", []):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="JWT token must have admin permission to issue tokens",
                )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Authentication required to issue tokens. Provide x-api-key or Authorization header.",
            )

    auth = get_tenant_auth()

    token = auth.create_token(
        tenant_id=body.tenant_id,
        agent_id=body.agent_id,
        permissions=body.permissions,
        expiry_seconds=body.expiry_seconds,
    )

    return JSONResponse(content={
        "access_token": token,
        "token_type": "bearer",
        "expires_in": body.expiry_seconds if body.expiry_seconds else _AUTH_CONFIG.token_expiry_seconds,
        "tenant_id": body.tenant_id,
        "agent_id": body.agent_id,
        "permissions": body.permissions,
    })


# ── Memory CRUD ──────────────────────────────────────────

@app.post(
    "/v1/memories",
    response_model=WriteMemoryResponse,
    status_code=201,
    tags=["Memories"],
)
async def write_memory(
    request: Request,
    body: WriteMemoryRequest,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")

    pipeline = get_pipeline()
    metrics = get_metrics_collector()
    bus = get_event_bus()

    try:
        t_start = time.monotonic()
        result = await asyncio.to_thread(
            pipeline.ingest,
            content=body.content,
            person_code=body.person_code,
            ts=body.ts,
            topics=body.topics,
            nature_code=body.nature_code,
            tool_codes=body.tool_codes,
            knowledge_codes=body.knowledge_codes,
            importance=body.importance,
            owner_agent_id=ctx.agent_id,
            visibility=body.visibility,
        )
        elapsed_ms = (time.monotonic() - t_start) * 1000
        metrics.record_write(latency_ms=elapsed_ms, success=True)

        safe_result: dict = {}
        if hasattr(WriteMemoryResponse, 'model_fields'):
            fields = WriteMemoryResponse.model_fields
        else:
            fields = WriteMemoryResponse.__fields__
        for key in fields:
            if key in result:
                safe_result[key] = result[key]

        if "skipped" in result and result["skipped"]:
            return JSONResponse(
                status_code=200,
                content={"memory_id": None, "skipped": True, "reason": result.get("reason")},
            )

        content_preview = body.content[:200].replace("\n", " ").replace("\r", "")

        logger.info("remember_success", extra={
            "event": "remember_success",
            "tenant_id": ctx.tenant_id,
            "importance": body.importance,
        })

        logger.info(
            "memory_created: mid=%s nature=%s importance=%s topics=%s tenant=%s content=%.200s",
            result.get("memory_id"),
            result.get("nature_id"),
            body.importance,
            body.topics,
            ctx.tenant_id,
            content_preview,
        )

        if bus is not None:
            await bus.emit(
                "memory.created",
                {
                    "memory_id": result.get("memory_id"),
                    "agent_id": ctx.agent_id,
                    "importance": body.importance,
                    "content_preview": content_preview[:80],
                },
                tenant_id=ctx.tenant_id,
            )

        return JSONResponse(status_code=201, content=safe_result)

    except RuntimeError as exc:
        logger.error(f"Write transaction failed: {exc}")
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Write Transaction Failed",
            detail="Write transaction failed",
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


# ── Recall ───────────────────────────────────────────────

@app.post(
    "/v1/recall",
    response_model=RecallResponse,
    tags=["Recall"],
)
async def recall(
    request: Request,
    body: RecallRequest,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    engine = get_recall_engine()
    metrics = get_metrics_collector()
    embedding_store = get_embedding_store()
    store = get_store()
    encoder = get_encoder()
    bus = get_event_bus()

    try:
        t_start = time.monotonic()

        nature_id = None
        if body.nature_code:
            try:
                nature_id = await asyncio.to_thread(encoder.encode_nature, body.nature_code)
            except ValueError as e:
                logger.debug("api_v3: invalid nature_code: %s", e)

        if embedding_store is not None:
            result = await asyncio.to_thread(
                engine.recall,
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
                query_agent_id=ctx.agent_id,
                team_id=body.team_id,
            )
        else:
            effective_keyword = body.keyword or body.query
            structured_results = await asyncio.to_thread(
                store.query,
                keyword=effective_keyword,
                time_from=body.time_from,
                time_to=body.time_to,
                person_id=body.person_id,
                nature_id=nature_id,
                topic_code=body.topic_code,
                importance=body.importance,
                significance=body.significance,
                limit=body.top_k * 2,
                query_agent_id=ctx.agent_id,
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

        # Track recall empty results
        if not result.get("primary"):
            # This is a key business metric - empty recall means poor search quality
            logger.info("recall_empty_result", extra={
                "event": "recall_empty_result",
                "query_length": len(body.query),
                "tenant_id": ctx.tenant_id,
            })

        primary = result.get("primary", [])
        for mem in primary:
            c = mem.get("content", "")
            if c:
                mem["content"] = _safe_content_preview(c, 500)

        if bus is not None:
            await bus.emit(
                "memory.recalled",
                {
                    "query": body.query,
                    "result_count": primary_count,
                    "agent_id": ctx.agent_id,
                },
                tenant_id=ctx.tenant_id,
            )

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


# ── SSE Streaming ────────────────────────────────────────

_sse_connections = 0
_sse_lock = asyncio.Lock()
_MAX_SSE_CONNECTIONS = 100

@app.get("/v1/events/{tenant_id}", tags=["Streaming"])
async def stream_events(
    request: Request,
    tenant_id: str,
    event_types: Optional[str] = Query(None, description="Comma-separated event types to stream"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    async with _sse_lock:
        if _sse_connections >= _MAX_SSE_CONNECTIONS:
            raise HTTPException(status_code=429, detail="Too many SSE connections")
        _sse_connections += 1

    try:
        if not ctx.can_read():
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

        if ctx.tenant_id != tenant_id and not ctx.can_admin():
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="You may only stream events for your own tenant unless you have admin permissions",
            )

        sse = get_sse_adapter()

        selected_types = None
        if event_types:
            selected_types = [et.strip() for et in event_types.split(",") if et.strip()]

        async def _sse_generator():
            try:
                async for line in sse.events_to_sse(event_types=selected_types):
                    if await request.is_disconnected():
                        break
                    yield line
            except asyncio.CancelledError as e:
                logger.debug("api_v3: SSE generator cancelled: %s", e)

        return StreamingResponse(
            _sse_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    finally:
        async with _sse_lock:
            _sse_connections -= 1


# ── Rate Limiter Status ──────────────────────────────────

@app.get("/v1/ratelimit-status", tags=["System"])
async def ratelimit_status(
    request: Request,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    return JSONResponse(content=_tenant_rate_limiter.status(ctx.tenant_id))


# ── Document Deep Reading (V9.2) ────────────────────────

@app.post("/v1/documents/upload", tags=["Documents"])
async def upload_document(
    request: Request,
    content_b64: str = Body(..., description="Base64 encoded file content"),
    filename: str = Body("", description="Original filename with extension"),
    title: str = Body(""),
    importance: str = Body("high"),
    strategy: str = Body("auto"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """上传文档并自动分段索引（文件内容需 Base64 编码）"""
    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")

    MAX_UPLOAD_SIZE_B64 = 52428800
    if len(content_b64) > MAX_UPLOAD_SIZE_B64:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 50MB.")

    doc_parser = get_document_parser()
    chunker = get_semantic_chunker()
    indexer = get_chunk_indexer()

    if not doc_parser or not chunker or not indexer:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Document Processing Unavailable",
            detail="Document processing modules are not loaded.",
        )

    try:
        import base64
        file_bytes = base64.b64decode(content_b64)
        file_content = file_bytes.decode("utf-8", errors="ignore")
    except Exception as exc:
        return _problem_detail(
            request=request,
            status=HTTP_400_BAD_REQUEST,
            title="File Decode Error",
            detail=f"Failed to decode base64 content: {exc}",
        )

    try:
        import tempfile
        suffix = os.path.splitext(filename or ".txt")[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="wb") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            parsed = await asyncio.to_thread(doc_parser.parse, tmp_path)
        finally:
            os.unlink(tmp_path)

        doc_title = title or parsed.title or filename or "untitled"

        chunk_result = await asyncio.to_thread(
            chunker.chunk_document,
            parsed.sections,
            "pending",
            strategy,
        )

        index_result = await asyncio.to_thread(
            indexer.index_document,
            chunk_result,
            title=doc_title,
            source_path=filename or "",
            source_type=parsed.source_type,
            importance=importance,
        )

        return JSONResponse(status_code=201, content={
            "doc_id": index_result.doc_id,
            "title": doc_title,
            "source_type": parsed.source_type,
            "total_sections": len(parsed.sections),
            "total_chunks": index_result.total_chunks,
            "indexed_chunks": index_result.indexed_chunks,
            "failed_chunks": index_result.failed_chunks,
            "total_vectors": index_result.total_vectors,
            "strategy_used": chunk_result.strategy_used,
            "errors": index_result.errors,
        })

    except Exception as exc:
        logger.error(f"Document upload failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Document Upload Failed",
            detail="Internal error during document processing.",
        )


@app.post("/v1/documents/text", tags=["Documents"])
async def index_text_document(
    request: Request,
    text: str = Body(...),
    title: str = Body(""),
    source_type: str = Body("text"),
    importance: str = Body("high"),
    strategy: str = Body("auto"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """直接索引文本内容"""
    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")

    if text and len(text) > MAX_DOCUMENT_TEXT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Document text exceeds maximum length of {MAX_DOCUMENT_TEXT_LENGTH} characters"
        )

    doc_parser = get_document_parser()
    chunker = get_semantic_chunker()
    indexer = get_chunk_indexer()

    if not doc_parser or not chunker or not indexer:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Document Processing Unavailable",
            detail="Document processing modules are not loaded.",
        )

    try:
        if source_type == "markdown":
            parsed = await asyncio.to_thread(doc_parser._parse_markdown, text, "")
        elif source_type == "html":
            parsed = await asyncio.to_thread(doc_parser._parse_html, text, "")
        else:
            parsed = await asyncio.to_thread(doc_parser._parse_text, text, "")

        doc_title = title or parsed.title or "untitled"

        chunk_result = await asyncio.to_thread(
            chunker.chunk_document,
            parsed.sections,
            "pending",
            strategy,
        )

        index_result = await asyncio.to_thread(
            indexer.index_document,
            chunk_result,
            title=doc_title,
            source_path="",
            source_type=source_type,
            importance=importance,
        )

        return JSONResponse(status_code=201, content={
            "doc_id": index_result.doc_id,
            "title": doc_title,
            "source_type": source_type,
            "total_sections": len(parsed.sections),
            "total_chunks": index_result.total_chunks,
            "indexed_chunks": index_result.indexed_chunks,
            "failed_chunks": index_result.failed_chunks,
            "total_vectors": index_result.total_vectors,
            "strategy_used": chunk_result.strategy_used,
            "errors": index_result.errors,
        })

    except Exception as exc:
        logger.error(f"Text document indexing failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Text Indexing Failed",
            detail="Internal error during text document indexing.",
        )


@app.get("/v1/documents/{doc_id}", tags=["Documents"])
async def get_document(
    request: Request,
    doc_id: str,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """获取文档信息和所有分段"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    retriever = get_chunk_retriever()
    if not retriever:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Document Retrieval Unavailable",
            detail="Chunk retriever module is not loaded.",
        )

    try:
        doc_meta = await asyncio.to_thread(retriever._get_document_meta, doc_id)
        if not doc_meta:
            return _problem_detail(
                request=request,
                status=HTTP_404_NOT_FOUND,
                title="Document Not Found",
                detail=f"No document found with id '{doc_id}'.",
            )

        chunks = await asyncio.to_thread(retriever.get_document_chunks, doc_id)

        return JSONResponse(content={
            "doc_id": doc_id,
            "title": doc_meta.get("title", ""),
            "source_path": doc_meta.get("source_path", ""),
            "source_type": doc_meta.get("source_type", ""),
            "total_chunks": doc_meta.get("total_chunks", 0),
            "total_chars": doc_meta.get("total_chars", 0),
            "created_at": doc_meta.get("created_at", 0),
            "updated_at": doc_meta.get("updated_at", 0),
            "chunks": [
                {
                    "chunk_id": c.chunk_id,
                    "memory_id": c.memory_id,
                    "chapter": c.chapter,
                    "section": c.section,
                    "page_num": c.page_num,
                    "position": c.position,
                    "content_preview": c.content[:200],
                }
                for c in chunks
            ],
        })

    except Exception as exc:
        logger.error(f"Get document failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Get Document Failed",
            detail="Internal error retrieving document.",
        )


@app.get("/v1/documents/{doc_id}/chunks", tags=["Documents"])
async def get_document_chunks(
    request: Request,
    doc_id: str,
    chapter: str = Query(None),
    page: int = Query(None),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """获取文档分段列表（可按章节/页码过滤）"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    retriever = get_chunk_retriever()
    if not retriever:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Document Retrieval Unavailable",
            detail="Chunk retriever module is not loaded.",
        )

    try:
        chunks = await asyncio.to_thread(retriever.get_document_chunks, doc_id)

        if chapter:
            chunks = [c for c in chunks if chapter in c.chapter]
        if page is not None:
            chunks = [c for c in chunks if c.page_num == page]

        return JSONResponse(content={
            "doc_id": doc_id,
            "total": len(chunks),
            "chunks": [
                {
                    "chunk_id": c.chunk_id,
                    "memory_id": c.memory_id,
                    "chapter": c.chapter,
                    "section": c.section,
                    "page_num": c.page_num,
                    "position": c.position,
                    "content": c.content,
                    "score": c.score,
                }
                for c in chunks
            ],
        })

    except Exception as exc:
        logger.error(f"Get document chunks failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Get Chunks Failed",
            detail="Internal error retrieving document chunks.",
        )


@app.post("/v1/documents/search", tags=["Documents"])
async def search_documents(
    request: Request,
    query: str = Body(...),
    top_k: int = Body(5),
    expand_context: int = Body(1),
    doc_id: str = Body(None),
    strategy: str = Body("auto"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """文档分段检索（支持向量+关键词+混合）"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    retriever = get_chunk_retriever()
    if not retriever:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Document Retrieval Unavailable",
            detail="Chunk retriever module is not loaded.",
        )

    try:
        result = await asyncio.to_thread(
            retriever.search,
            query=query,
            top_k=top_k,
            expand_context=expand_context,
            doc_id=doc_id,
            strategy=strategy,
        )

        return JSONResponse(content={
            "query": result.query,
            "total_hits": result.total_hits,
            "context_expanded": result.context_expanded,
            "strategy": result.strategy,
            "hits": [
                {
                    "memory_id": h.memory_id,
                    "chunk_id": h.chunk_id,
                    "doc_id": h.doc_id,
                    "chapter": h.chapter,
                    "section": h.section,
                    "page_num": h.page_num,
                    "position": h.position,
                    "content": h.content,
                    "score": round(h.score, 4),
                    "is_cold": h.is_cold,
                }
                for h in result.hits
            ],
        })

    except Exception as exc:
        logger.error(f"Document search failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Document Search Failed",
            detail="Internal error during document search.",
        )


@app.get("/v1/documents/{doc_id}/locate/{memory_id}", tags=["Documents"])
async def locate_in_document(
    request: Request,
    doc_id: str,
    memory_id: str,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """精准回溯 — 从 memory_id 定位到原文位置"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    retriever = get_chunk_retriever()
    if not retriever:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Document Retrieval Unavailable",
            detail="Chunk retriever module is not loaded.",
        )

    try:
        location = await asyncio.to_thread(retriever.locate_source, memory_id)

        if not location.get("found"):
            return _problem_detail(
                request=request,
                status=HTTP_404_NOT_FOUND,
                title="Memory Not Located",
                detail=f"Could not locate memory '{memory_id}' in any document.",
            )

        if location.get("doc_id") != doc_id:
            return _problem_detail(
                request=request,
                status=HTTP_404_NOT_FOUND,
                title="Memory Not In Document",
                detail=f"Memory '{memory_id}' belongs to document '{location.get('doc_id')}', not '{doc_id}'.",
            )

        return JSONResponse(content=location)

    except Exception as exc:
        logger.error(f"Locate in document failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Locate Failed",
            detail="Internal error during memory location lookup.",
        )


# ── Personality Analysis (V9.3) ────────────────────────

@app.post("/v1/personality/analyze", tags=["Personality"])
async def analyze_personality(
    request: Request,
    chat_text: str = Body(..., description="聊天记录文本"),
    self_name: str = Body("", description="自己的昵称"),
    source_type: str = Body("wechat_txt", description="数据源类型"),
    privacy_level: str = Body("team", description="隐私级别"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """分析聊天记录生成人格画像"""
    if not _HAS_PERSONALITY:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Personality Analysis Unavailable",
            detail="Personality analysis modules (chat_parser / personality_analyzer / personality_memory) are not loaded.",
        )

    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")

    try:
        parser = ChatParser()
        analyzer = PersonalityAnalyzer()
        pmem = PersonalityMemory(store=get_store())

        parsed = await asyncio.to_thread(
            parser.parse,
            chat_text,
            source_type=source_type,
            self_name=self_name or None,
        )

        profile = await asyncio.to_thread(
            analyzer.analyze,
            parsed,
            privacy_level=privacy_level,
        )

        await asyncio.to_thread(
            pmem.save,
            profile,
            tenant_id=ctx.tenant_id,
        )

        return JSONResponse(status_code=201, content=profile)

    except Exception as exc:
        logger.error(f"Personality analysis failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Personality Analysis Failed",
            detail="Internal error during personality analysis.",
        )


@app.get("/v1/personality/{person_id}", tags=["Personality"])
async def get_personality(
    request: Request,
    person_id: str,
    access_level: str = Query("team", description="访问级别"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """获取人格画像"""
    if not _HAS_PERSONALITY:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Personality Analysis Unavailable",
            detail="Personality analysis modules are not loaded.",
        )

    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    try:
        pmem = PersonalityMemory(store=get_store())
        profile = await asyncio.to_thread(
            pmem.get,
            person_id,
            access_level=access_level,
            tenant_id=ctx.tenant_id,
        )

        if not profile:
            return _problem_detail(
                request=request,
                status=HTTP_404_NOT_FOUND,
                title="Personality Not Found",
                detail=f"No personality profile found for person '{person_id}'.",
            )

        return JSONResponse(content=profile)

    except Exception as exc:
        logger.error(f"Get personality failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Get Personality Failed",
            detail="Internal error retrieving personality profile.",
        )


@app.get("/v1/personality/{person_id}/versions", tags=["Personality"])
async def get_personality_versions(
    request: Request,
    person_id: str,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """获取人格画像版本历史"""
    if not _HAS_PERSONALITY:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Personality Analysis Unavailable",
            detail="Personality analysis modules are not loaded.",
        )

    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    try:
        pmem = PersonalityMemory(store=get_store())
        versions = await asyncio.to_thread(
            pmem.get_versions,
            person_id,
            tenant_id=ctx.tenant_id,
        )

        return JSONResponse(content={
            "person_id": person_id,
            "versions": versions,
        })

    except Exception as exc:
        logger.error(f"Get personality versions failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Get Personality Versions Failed",
            detail="Internal error retrieving personality version history.",
        )


@app.get("/v1/personality/{person_id}/evidence", tags=["Personality"])
async def get_personality_evidence(
    request: Request,
    person_id: str,
    trait: str = Query(None, description="特质名称过滤"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """获取人格特质推断的证据来源"""
    if not _HAS_PERSONALITY:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Personality Analysis Unavailable",
            detail="Personality analysis modules are not loaded.",
        )

    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    try:
        pmem = PersonalityMemory(store=get_store())
        evidence = await asyncio.to_thread(
            pmem.get_evidence,
            person_id,
            trait=trait,
            tenant_id=ctx.tenant_id,
        )

        return JSONResponse(content={
            "person_id": person_id,
            "trait_filter": trait,
            "evidence": evidence,
        })

    except Exception as exc:
        logger.error(f"Get personality evidence failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Get Personality Evidence Failed",
            detail="Internal error retrieving personality evidence.",
        )


@app.delete("/v1/personality/{person_id}", tags=["Personality"])
async def delete_personality(
    request: Request,
    person_id: str,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """删除人格画像"""
    if not _HAS_PERSONALITY:
        return _problem_detail(
            request=request,
            status=HTTP_503_SERVICE_UNAVAILABLE,
            title="Personality Analysis Unavailable",
            detail="Personality analysis modules are not loaded.",
        )

    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")

    try:
        pmem = PersonalityMemory(store=get_store())
        deleted = await asyncio.to_thread(
            pmem.delete,
            person_id,
            tenant_id=ctx.tenant_id,
        )

        if not deleted:
            return _problem_detail(
                request=request,
                status=HTTP_404_NOT_FOUND,
                title="Personality Not Found",
                detail=f"No personality profile found for person '{person_id}'.",
            )

        return JSONResponse(content={"person_id": person_id, "deleted": True})

    except Exception as exc:
        logger.error(f"Delete personality failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Delete Personality Failed",
            detail="Internal error deleting personality profile.",
        )


# ── Spirit (V8.3) ───────────────────────────────────────

@app.get("/v1/spirit/health", tags=["Spirit"])
async def spirit_health(
    fix: bool = Query(False, description="Auto-fix issues"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Run Spirit health check"""
    mem = _get_memory(ctx.db_path)
    result = mem.spirit.check_health(fix=fix)
    if hasattr(result, 'to_dict'):
        result = result.to_dict()
    elif hasattr(result, '__dict__'):
        result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}
    return result

@app.get("/v1/spirit/daily-report", tags=["Spirit"])
async def spirit_daily_report(
    date: str = Query(None, description="Date in YYYY-MM-DD format"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Generate daily memory report"""
    import time
    mem = _get_memory(ctx.db_path)
    date_ts = None
    if date:
        import datetime
        date_ts = int(datetime.datetime.strptime(date, "%Y-%m-%d").timestamp())
    result = mem.spirit.report(report_type='daily', date=date_ts, format='markdown')
    return {"report": result}

@app.get("/v1/spirit/weekly-report", tags=["Spirit"])
async def spirit_weekly_report(
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Generate weekly memory report"""
    mem = _get_memory(ctx.db_path)
    result = mem.spirit.report(report_type='weekly', format='markdown')
    return {"report": result}

@app.get("/v1/spirit/awareness", tags=["Spirit"])
async def spirit_awareness(
    topic: str = Query(..., description="Topic to check awareness for"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Query knowledge awareness about a topic"""
    mem = _get_memory(ctx.db_path)
    result = mem.spirit.query_awareness(topic)
    if hasattr(result, 'to_dict'):
        result = result.to_dict()
    elif hasattr(result, '__dict__'):
        result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}
    return result

@app.post("/v1/spirit/execute", tags=["Spirit"])
async def spirit_execute(
    command: str = Body(..., description="Natural language command"),
    confirm: bool = Body(True, description="Require confirmation for write operations"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Execute a Spirit command

    SAFETY: confirm=True is required for write operations. Commands are
    validated for length (max 500 chars) and dangerous patterns are blocked.
    """
    # Security: validate command input
    if not command or not command.strip():
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Command cannot be empty")
    if len(command) > 500:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Command too long (max 500 characters)")
    import re as _re
    _DANGEROUS = _re.compile(
        r"(?:ignore\s+(?:previous|above|all)\s+instructions?"
        r"|system\s*:"
        r"|you\s+are\s+now"
        r"|new\s+rule\s*:",
        _re.IGNORECASE,
    )
    if _DANGEROUS.search(command):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Command contains disallowed pattern")

    if not confirm:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Spirit write operations require confirm=True")

    mem = _get_memory(ctx.db_path)
    result = mem.spirit.execute(command, confirm=confirm)
    if hasattr(result, 'to_dict'):
        result = result.to_dict()
    elif hasattr(result, '__dict__'):
        result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}
    return result


# ── Federation (V12) ───────────────────────────────────

@app.get("/v1/federation/peers", tags=["Federation"])
async def federation_peers(ctx: TenantContext = Depends(get_tenant_context())):
    """List federation peers"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")
    mem = _get_memory(ctx.db_path)
    engine = mem.federation_engine
    stats = engine.get_stats()
    return JSONResponse(content={
        "peers": stats["peer_ids"],
        "total": stats["peers"],
    })


@app.post("/v1/federation/search", tags=["Federation"])
async def federation_search(
    request: Request,
    query: str = Body(..., description="Search query text"),
    topics: Optional[List[str]] = Body(None, description="Topic filters"),
    max_per_peer: int = Body(5, ge=1, le=50, description="Max results per peer"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Search across federated agents"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")
    mem = _get_memory(ctx.db_path)
    engine = mem.federation_engine
    result = await asyncio.to_thread(
        engine.federated_search,
        query=query,
        topics=topics,
        max_per_peer=max_per_peer,
    )
    return JSONResponse(content=result)


@app.get("/v1/federation/conflicts", tags=["Federation"])
async def federation_conflicts(
    topic: Optional[str] = Query(None, description="Filter by topic"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Detect knowledge conflicts across agents"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")
    mem = _get_memory(ctx.db_path)
    engine = mem.federation_engine
    conflicts = await asyncio.to_thread(engine.detect_conflicts, topic=topic)
    return JSONResponse(content={
        "total": len(conflicts),
        "conflicts": [
            {
                "topic": c.topic,
                "agent_a": c.agent_a,
                "agent_a_claim": c.agent_a_claim,
                "agent_b": c.agent_b,
                "agent_b_claim": c.agent_b_claim,
                "conflict_type": c.conflict_type,
                "resolution": c.resolution,
                "confidence_a": c.confidence_a,
                "confidence_b": c.confidence_b,
            }
            for c in conflicts
        ],
    })


@app.post("/v1/federation/resolve", tags=["Federation"])
async def federation_resolve(
    request: Request,
    topic: str = Body(..., description="Conflict topic"),
    agent_a: str = Body(..., description="First agent ID"),
    agent_a_claim: str = Body(..., description="First agent claim"),
    agent_b: str = Body(..., description="Second agent ID"),
    agent_b_claim: str = Body(..., description="Second agent claim"),
    conflict_type: str = Body("contradiction", description="Conflict type"),
    strategy: str = Body("higher_confidence", description="Resolution strategy: higher_confidence | newer_wins | merged | both_kept"),
    confidence_a: float = Body(0.5),
    confidence_b: float = Body(0.5),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Resolve a knowledge conflict"""
    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")
    from engines.federation import KnowledgeConflict
    mem = _get_memory(ctx.db_path)
    engine = mem.federation_engine
    conflict = KnowledgeConflict(
        topic=topic,
        agent_a=agent_a,
        agent_a_claim=agent_a_claim,
        agent_b=agent_b,
        agent_b_claim=agent_b_claim,
        conflict_type=conflict_type,
        confidence_a=confidence_a,
        confidence_b=confidence_b,
    )
    resolved = await asyncio.to_thread(engine.resolve_conflict, conflict, strategy)
    return JSONResponse(content={
        "topic": resolved.topic,
        "resolution": resolved.resolution,
        "agent_a": resolved.agent_a,
        "agent_b": resolved.agent_b,
    })


@app.post("/v1/memory/batch", tags=["Memory"])
async def batch_remember(
    request: Request,
    items: list[dict] = Body(..., description="List of memory items to store"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Batch store multiple memories in a single transaction for high throughput."""
    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")

    MAX_BATCH_SIZE = 100
    if len(items) > MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Batch size {len(items)} exceeds maximum of {MAX_BATCH_SIZE}"
        )

    mem = _get_memory(ctx.db_path)
    results = await asyncio.to_thread(mem.ingest_engine.batch_remember, items)
    return {"total": len(items), "stored": sum(1 for r in results if r.get("written")), "results": results}


@app.post("/v1/memory/{memory_id}/feedback", tags=["Memories"])
async def memory_feedback(
    request: Request,
    memory_id: str,
    feedback_type: str = Body(..., description="Feedback type: helpful | unhelpful | corrected | ignored"),
    context: Optional[dict] = Body(None, description="Optional context (e.g. correction_id, query)"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Record feedback for a memory — enables continuous learning"""
    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")

    if feedback_type not in ("helpful", "unhelpful", "corrected", "ignored"):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Invalid feedback_type: {feedback_type}. Must be: helpful, unhelpful, corrected, ignored",
        )

    mem = _get_memory(ctx.db_path)
    try:
        result = mem.feedback_learner.record_feedback(
            memory_id=memory_id,
            feedback_type=feedback_type,
            context=context,
        )
        return JSONResponse(content=result)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid feedback parameters")
    except Exception as e:
        logger.error("memory_feedback failed: %s", e)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Feedback Recording Failed",
            detail="Feedback recording failed",
        )


# ── Curiosity Engine (Level 6.0) ─────────────────────────

@app.get("/v1/curiosity/targets", tags=["Curiosity"])
async def curiosity_targets(
    request: Request,
    limit: int = Query(10, ge=1, le=50, description="Maximum targets to return"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Identify topics worth exploring based on knowledge gaps, uncertainty, staleness"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    mem = _get_memory(ctx.db_path)
    try:
        targets = await asyncio.to_thread(mem.curiosity_engine.identify_targets, limit=limit)
        return JSONResponse(content={
            "total": len(targets),
            "targets": [
                {
                    "topic": t.topic,
                    "reason": t.reason,
                    "priority": round(t.priority, 3),
                    "estimated_value": round(t.estimated_value, 3),
                    "current_coverage": t.current_coverage,
                    "avg_confidence": round(t.avg_confidence, 3),
                    "last_updated": t.last_updated,
                }
                for t in targets
            ],
        })
    except Exception as exc:
        logger.error(f"Curiosity targets failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Curiosity Targets Failed",
            detail="Internal error during curiosity target identification.",
        )


@app.get("/v1/curiosity/suggestions", tags=["Curiosity"])
async def curiosity_suggestions(
    request: Request,
    limit: int = Query(5, ge=1, le=20, description="Maximum suggestions to return"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Get suggested queries the user could ask to fill knowledge gaps"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    mem = _get_memory(ctx.db_path)
    try:
        suggestions = await asyncio.to_thread(mem.curiosity_engine.get_suggested_queries, limit=limit)
        return JSONResponse(content={
            "total": len(suggestions),
            "suggestions": suggestions,
        })
    except Exception as exc:
        logger.error(f"Curiosity suggestions failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Curiosity Suggestions Failed",
            detail="Internal error during curiosity suggestion generation.",
        )


@app.post("/v1/curiosity/explore", tags=["Curiosity"])
async def curiosity_explore(
    request: Request,
    topic: str = Body(..., description="Topic to explore"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Execute an exploration action for a target topic"""
    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")

    mem = _get_memory(ctx.db_path)
    try:
        from engines.curiosity import ExplorationTarget
        targets = await asyncio.to_thread(mem.curiosity_engine.identify_targets, limit=50)
        target = None
        for t in targets:
            if t.topic == topic:
                target = t
                break
        if target is None:
            target = ExplorationTarget(
                topic=topic,
                reason="manual",
                priority=0.5,
                estimated_value=0.5,
                current_coverage=0,
                avg_confidence=0.0,
                last_updated=0.0,
            )

        result = await asyncio.to_thread(mem.curiosity_engine.explore, target)
        return JSONResponse(content={
            "topic": result.target.topic,
            "action_taken": result.action_taken,
            "new_knowledge_count": result.new_knowledge_count,
            "confidence_improvement": round(result.confidence_improvement, 3),
            "timestamp": result.timestamp,
        })
    except Exception as exc:
        logger.error(f"Curiosity explore failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Curiosity Explore Failed",
            detail="Internal error during curiosity exploration.",
        )


# ── Knowledge Validation (Level 6.0) ─────────────────────

@app.post("/v1/validation/validate/{memory_id}", tags=["Validation"])
async def validate_memory(
    request: Request,
    memory_id: str,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Validate a single memory — cross-reference, staleness, confidence decay"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    mem = _get_memory(ctx.db_path)
    try:
        result = await asyncio.to_thread(mem.knowledge_validator.validate_memory, memory_id)
        if result is None:
            return _problem_detail(
                request=request,
                status=HTTP_404_NOT_FOUND,
                title="Memory Not Found",
                detail=f"No memory found with id '{memory_id}'.",
            )
        return JSONResponse(content={
            "memory_id": result.memory_id,
            "validation_status": result.validation_status,
            "confidence_before": round(result.confidence_before, 3),
            "confidence_after": round(result.confidence_after, 3),
            "cross_references": result.cross_references,
            "contradictions": result.contradictions,
            "staleness_days": round(result.staleness_days, 1),
            "recommendation": result.recommendation,
            "evidence": result.evidence,
        })
    except Exception as exc:
        logger.error(f"Validate memory failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Validation Failed",
            detail="Internal error during memory validation.",
        )


@app.post("/v1/validation/validate-all", tags=["Validation"])
async def validate_all(
    request: Request,
    limit: int = Body(100, description="Maximum memories to validate"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Validate all memories and return summary"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")

    mem = _get_memory(ctx.db_path)
    try:
        result = await asyncio.to_thread(mem.knowledge_validator.validate_all, limit=limit)
        output = {
            "total_validated": result["total_validated"],
            "status_distribution": result["status_distribution"],
            "avg_confidence_before": result["avg_confidence_before"],
            "avg_confidence_after": result["avg_confidence_after"],
            "confidence_change": result["confidence_change"],
            "results": [
                {
                    "memory_id": r.memory_id,
                    "validation_status": r.validation_status,
                    "confidence_before": round(r.confidence_before, 3),
                    "confidence_after": round(r.confidence_after, 3),
                    "cross_references": r.cross_references,
                    "contradictions": r.contradictions,
                    "staleness_days": round(r.staleness_days, 1),
                    "recommendation": r.recommendation,
                }
                for r in result["results"]
            ],
        }
        return JSONResponse(content=output)
    except Exception as exc:
        logger.error(f"Validate all failed: {exc}", exc_info=True)
        return _problem_detail(
            request=request,
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            title="Validation Failed",
            detail="Internal error during bulk validation.",
        )


# ── Sync (V6.0 Phase 4: Distributed Consistency) ──────────

@app.get("/v1/sync/peers", tags=["Sync"])
async def sync_list_peers(
    request: Request,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """List all sync peer nodes"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")
    mem = _get_memory(ctx.db_path)
    peers = mem.sync_engine.list_peers()
    return JSONResponse(content={"peers": peers, "total": len(peers)})


@app.post("/v1/sync/with/{peer_id}", tags=["Sync"])
async def sync_with_peer(
    request: Request,
    peer_id: str,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Synchronize with a specific peer node"""
    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")
    mem = _get_memory(ctx.db_path)
    result = await asyncio.to_thread(mem.sync_engine.sync_with_peer, peer_id)
    return JSONResponse(content={
        "source_node": result.source_node,
        "target_node": result.target_node,
        "operations_applied": result.operations_applied,
        "conflicts_resolved": result.conflicts_resolved,
        "operations_rejected": result.operations_rejected,
        "duration_ms": result.duration_ms,
        "errors": result.errors,
    })


@app.post("/v1/sync/all", tags=["Sync"])
async def sync_all_peers(
    request: Request,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Synchronize with all peer nodes"""
    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")
    mem = _get_memory(ctx.db_path)
    results = await asyncio.to_thread(mem.sync_engine.sync_all)
    return JSONResponse(content={
        "total_peers": len(results),
        "results": [
            {
                "source_node": r.source_node,
                "target_node": r.target_node,
                "operations_applied": r.operations_applied,
                "conflicts_resolved": r.conflicts_resolved,
                "operations_rejected": r.operations_rejected,
                "duration_ms": r.duration_ms,
                "errors": r.errors,
            }
            for r in results
        ],
    })


@app.post("/v1/sync/apply", tags=["Sync"])
async def sync_apply_changes(
    request: Request,
    changes: list = Body(..., description="List of remote memory changes to apply"),
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Apply remote changes using CRDT merge"""
    if not ctx.can_write():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Write permission required")
    mem = _get_memory(ctx.db_path)
    result = await asyncio.to_thread(mem.sync_engine.apply_remote_changes, changes)
    return JSONResponse(content=result)


@app.get("/v1/sync/checkpoint", tags=["Sync"])
async def sync_checkpoint(
    request: Request,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Create a sync checkpoint for recovery"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")
    mem = _get_memory(ctx.db_path)
    checkpoint = mem.sync_engine.create_checkpoint()
    return JSONResponse(content=checkpoint)


@app.get("/v1/sync/stats", tags=["Sync"])
async def sync_stats(
    request: Request,
    ctx: TenantContext = Depends(get_tenant_context()),
):
    """Get sync engine statistics"""
    if not ctx.can_read():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Read permission required")
    mem = _get_memory(ctx.db_path)
    stats = mem.sync_engine.get_stats()
    return JSONResponse(content=stats)


# ═══════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════

def main():
    import argparse
    argp = argparse.ArgumentParser(description="Agent Memory API v3 (FastAPI + SSE)")
    argp.add_argument("--host", default="127.0.0.1", help="Bind address")
    argp.add_argument("--port", type=int, default=8988, help="Bind port")
    argp.add_argument("--db", default=None, help="SQLite database path override")
    argp.add_argument("--jwt-secret", default=None, help="JWT signing secret (env: AGENT_MEMORY_JWT_SECRET)")
    argp.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = argp.parse_args()

    from logging_config import configure_logging
    configure_logging(level=args.log_level)

    global _DB_PATH, _AUTH_CONFIG
    _DB_PATH = args.db

    if args.jwt_secret:
        _AUTH_CONFIG = AuthConfig(
            jwt_secret=args.jwt_secret,
            api_keys=_AUTH_CONFIG.api_keys,
            token_expiry_seconds=_AUTH_CONFIG.token_expiry_seconds,
        )
        _check_jwt_secret()

    logger.info(f"Agent Memory API v3 ({_APP_VERSION}) starting on http://{args.host}:{args.port}")
    logger.info(f"  Docs:    http://localhost:{args.port}/docs")
    logger.info(f"  Health:  http://localhost:{args.port}/v1/health")
    logger.info(f"  Metrics: http://localhost:{args.port}/v1/metrics")
    logger.info(f"  SSE:     http://localhost:{args.port}/v1/events/{{tenant_id}}")

    uvicorn.run(
        "agent_memory.api_v3:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level.lower(),
        reload=False,
    )


if __name__ == "__main__":
    main()