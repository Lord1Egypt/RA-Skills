"""Agent Memory Playground — Interactive Web UI for testing memory operations."""
from __future__ import annotations

import hmac
import logging
import os
import sqlite3
import tempfile
import time
from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# Optional playground authentication via environment variable
_PLAYGROUND_API_KEY = os.environ.get("AGENT_MEMORY_PLAYGROUND_API_KEY", "")

# IP-based rate limiter for playground
class _IPRateLimiter:
    """Simple in-memory IP-based rate limiter."""
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self._max = max_requests
        self._window = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, ip: str) -> bool:
        now = time.time()
        self._requests[ip] = [t for t in self._requests[ip] if now - t < self._window]
        if len(self._requests[ip]) >= self._max:
            return False
        self._requests[ip].append(now)
        return True

_ip_rate_limiter = _IPRateLimiter()

if not _PLAYGROUND_API_KEY:
    logger.warning(
        "AGENT_MEMORY_PLAYGROUND_API_KEY is not set — Playground authentication is DISABLED. "
        "Anyone with network access can use the Playground API. "
        "Set AGENT_MEMORY_PLAYGROUND_API_KEY to enable authentication."
    )
    _env = os.environ.get("AGENT_MEMORY_ENV", "").lower()
    if _env in ("production", "prod"):
        raise ValueError(
            "AGENT_MEMORY_PLAYGROUND_API_KEY must be set in production environment. "
            "Refusing to start Playground without authentication in production."
        )


async def verify_playground_auth(api_key: str = Header(None, alias="X-API-Key")):
    """Optional playground authentication.

    If AGENT_MEMORY_PLAYGROUND_API_KEY is not set, auth is disabled (backward compatible).
    If set, all API endpoints require the matching key via X-API-Key header.
    """
    if not _PLAYGROUND_API_KEY:
        return  # Auth not configured, allow all
    if not hmac.compare_digest(api_key, _PLAYGROUND_API_KEY):
        raise HTTPException(status_code=401, detail="API Key 无效")


class RememberRequest(BaseModel):
    content: str = Field(min_length=1, max_length=50000)
    metadata: dict = {}


class RecallRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=100)


class PIITextRequest(BaseModel):
    text: str


def create_app(db_path: str = None) -> FastAPI:
    app = FastAPI(
        title="Agent Memory Playground",
        version="12.0.0",
        dependencies=[Depends(verify_playground_auth)],
    )

    # IP-based rate limiting middleware
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        if not _ip_rate_limiter.is_allowed(client_ip):
            return JSONResponse(status_code=429, content={"error": "请求过于频繁，请稍后重试"})
        response = await call_next(request)
        return response

    @app.exception_handler(Exception)
    async def validation_exception_handler(request: Request, exc: Exception):
        from pydantic import ValidationError
        if isinstance(exc, ValidationError):
            errors = exc.errors()
            msgs = []
            for e in errors:
                field = ".".join(str(x) for x in e.get("loc", []))
                msgs.append(f"{field}: {e.get('msg', '输入有误，请检查内容格式后重试')}")
            return JSONResponse(status_code=422, content={"success": False, "error": "; ".join(msgs)})
        return JSONResponse(status_code=500, content={"success": False, "error": "系统开小差了，请稍后再试"})

    @app.exception_handler(sqlite3.OperationalError)
    async def db_error_handler(request: Request, exc: sqlite3.OperationalError):
        if "locked" in str(exc).lower():
            return JSONResponse(status_code=503, content={
                "error": "系统繁忙，请稍后重试",
                "retry_after": 5,
            })
        return JSONResponse(status_code=500, content={"error": "数据库错误，请稍后重试"})

    db_path = db_path or os.environ.get(
        "AGENT_MEMORY_DB_PATH",
        os.path.join(tempfile.gettempdir(), "agent_memory_playground.db"),
    )
    if db_path != ":memory:":
        from agent_memory.utils import _validate_path
        db_path = _validate_path(db_path)

    from agent_memory import AgentMemory

    memory = AgentMemory(db_path=db_path)

    @app.get("/", response_class=HTMLResponse)
    async def playground_ui():
        return _HTML

    @app.post("/api/remember")
    async def api_remember(req: RememberRequest):
        try:
            result = memory.remember(req.content)
            response = {
                "success": result.get("written", False),
                "memory_id": result.get("memory_id"),
                "status": result.get("status"),
                "reason": result.get("reason"),
            }
            if result.get("_warnings"):
                response["_warnings"] = result["_warnings"]
            return response
        except Exception as e:
            logger.error("API error: %s", e, exc_info=True)
            return {"success": False, "error": "系统开小差了，请稍后再试"}

    @app.post("/api/recall")
    async def api_recall(req: RecallRequest):
        try:
            if req.top_k > 100:
                req.top_k = 100
            result = memory.recall(query=req.query, limit=req.top_k)
            primary = result.get("primary", [])
            formatted = []
            for r in primary:
                if isinstance(r, dict):
                    formatted.append(
                        {
                            "content": r.get("content", ""),
                            "score": r.get("score", r.get("relevance_score", 0)),
                            "memory_id": r.get("memory_id", ""),
                        }
                    )
                else:
                    formatted.append({"content": str(r), "score": 0})
            response = {"results": formatted}
            if result.get("_warnings"):
                response["_warnings"] = result["_warnings"]
            return response
        except Exception as e:
            logger.error("API error: %s", e, exc_info=True)
            return {"results": [], "error": "系统开小差了，请稍后再试"}

    @app.post("/api/detect-pii")
    async def api_detect_pii(req: PIITextRequest):
        try:
            from agent_memory.privacy.guard import PrivacyGuard

            guard = PrivacyGuard()
            findings = guard.detect_pii(req.text)
            return {"findings": findings}
        except Exception as e:
            logger.error("API error: %s", e, exc_info=True)
            return {"findings": [], "error": "系统开小差了，请稍后再试"}

    @app.post("/api/redact")
    async def api_redact(req: PIITextRequest):
        try:
            from agent_memory.privacy.guard import PrivacyGuard

            guard = PrivacyGuard()
            redacted = guard.redact(req.text)
            return {"redacted": redacted}
        except Exception as e:
            logger.error("API error: %s", e, exc_info=True)
            return {"redacted": req.text, "error": "系统开小差了，请稍后再试"}

    @app.get("/api/health")
    async def api_health():
        try:
            health = memory.health_check()
            return health
        except Exception as e:
            logger.error("API error: %s", e, exc_info=True)
            return {"healthy": False, "error": "系统开小差了，请稍后再试"}

    @app.get("/api/stats")
    async def api_stats():
        try:
            stats = memory.get_stats()
            return {"total_memories": stats.get("total_memories", 0)}
        except Exception:
            return {"total_memories": 0}

    @app.get("/api/onboarding/status")
    async def api_onboarding_status():
        """返回首次运行状态信息"""
        from agent_memory.onboarding import WelcomeGuide, get_progress

        progress = get_progress()
        is_first = not progress.get("onboarding_completed", False)
        is_configured = WelcomeGuide.is_configured()

        steps_completed = []
        if progress.get("step", 0) >= 1:
            steps_completed.append("seed_memories")
        if is_configured:
            steps_completed.append("configuration")

        return {
            "is_first_time": is_first,
            "is_configured": is_configured,
            "steps_completed": steps_completed,
            "step": progress.get("step", 0),
            "onboarding_completed": progress.get("onboarding_completed", False),
        }

    @app.get("/api/timeline")
    async def timeline(limit: int = 20):
        """Get recent memory timeline."""
        try:
            memories = memory.store.query(limit=limit)
            return {"memories": memories, "total": len(memories)}
        except Exception as e:
            logger.error("API error: %s", e, exc_info=True)
            return {"error": "系统开小差了，请稍后再试"}

    @app.get("/api/spirit/report")
    async def spirit_report(report_type: str = "daily"):
        """Get Spirit butler report."""
        try:
            spirit = memory.spirit
            if spirit is None:
                return {"error": "Spirit 管家不可用", "status": "disabled"}
            report = spirit.report(report_type=report_type)
            return {"report": report, "type": report_type}
        except Exception as e:
            logger.error("API error: %s", e, exc_info=True)
            return {"error": "系统开小差了，请稍后再试"}

    @app.get("/api/graph")
    async def memory_graph(limit: int = 50):
        """Get memory relationship graph data."""
        try:
            memories = memory.store.query(limit=limit)
            nodes = []
            edges = []
            for m in memories:
                mid = m.get("memory_id", "")
                nodes.append({"id": mid, "label": (m.get("content") or "")[:30]})
                links = memory.store.get_linked(mid)
                for link in links:
                    edges.append({
                        "source": mid,
                        "target": link.get("memory_id", ""),
                        "type": link.get("_link_type", "related"),
                    })
            return {"nodes": nodes, "edges": edges}
        except Exception as e:
            logger.error("API error: %s", e, exc_info=True)
            return {"error": "系统开小差了，请稍后再试"}

    @app.get("/api/onboarding/progress")
    async def api_onboarding_progress_get():
        """获取 onboarding 进度"""
        from agent_memory.onboarding import get_progress

        progress = get_progress()
        return {"step": progress.get("step", 0), "completed": progress.get("onboarding_completed", False)}

    class OnboardingProgressRequest(BaseModel):
        step: int

    @app.post("/api/onboarding/progress")
    async def api_onboarding_progress_post(req: OnboardingProgressRequest):
        """保存 onboarding 进度"""
        from agent_memory.onboarding import WelcomeGuide

        WelcomeGuide.mark_step_completed(req.step)
        return {"success": True, "step": req.step}

    @app.post("/api/onboarding/complete")
    async def api_onboarding_complete():
        """标记 onboarding 完成"""
        from agent_memory.onboarding import WelcomeGuide

        WelcomeGuide.mark_onboarding_completed()
        return {"success": True}

    @app.post("/api/onboarding/seed")
    async def api_onboarding_seed():
        """注入种子记忆"""
        from agent_memory.onboarding import seed_memories as get_seed_memories

        seeds = get_seed_memories()
        injected = 0
        errors = []
        for s in seeds:
            try:
                result = memory.remember(
                    content=s["content"],
                    importance="medium",
                    force=True,
                )
                if result.get("written"):
                    injected += 1
            except Exception as e:
                logger.error("API error: %s", e, exc_info=True)
                errors.append("系统开小差了，请稍后再试")

        return {
            "success": injected > 0,
            "injected": injected,
            "total": len(seeds),
            "errors": errors,
        }

    return app


_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Memory 体验中心</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #0f172a; color: #e2e8f0; min-height: 100vh; }
        .container { max-width: 900px; margin: 0 auto; padding: 2rem; }
        h1 { font-size: 1.8rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { color: #94a3b8; margin-bottom: 2rem; }
        .card { background: #1e293b; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; border: 1px solid #334155; }
        .card h2 { font-size: 1.1rem; color: #60a5fa; margin-bottom: 1rem; }
        textarea, input[type="text"] { width: 100%; background: #0f172a; border: 1px solid #475569; border-radius: 8px; padding: 0.75rem; color: #e2e8f0; font-size: 0.9rem; resize: vertical; }
        textarea:focus, input:focus { outline: none; border-color: #60a5fa; }
        button { background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; border: none; border-radius: 8px; padding: 0.6rem 1.5rem; cursor: pointer; font-size: 0.9rem; font-weight: 500; }
        button:hover { opacity: 0.9; }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .result { background: #0f172a; border-radius: 8px; padding: 1rem; margin-top: 0.75rem; font-family: 'Fira Code', monospace; font-size: 0.85rem; white-space: pre-wrap; max-height: 300px; overflow-y: auto; }
        .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1rem; }
        .stat { background: #1e293b; border-radius: 8px; padding: 1rem; text-align: center; border: 1px solid #334155; cursor: pointer; transition: border-color 0.2s; }
        .stat:hover { border-color: #60a5fa; }
        .stat-value { font-size: 1.5rem; font-weight: 700; color: #60a5fa; }
        .stat-label { font-size: 0.75rem; color: #94a3b8; margin-top: 0.25rem; }
        .stat-hint { font-size: 0.7rem; color: #64748b; margin-top: 0.25rem; }

        /* Welcome overlay */
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15,23,42,0.95); z-index: 1000; display: flex; align-items: center; justify-content: center; }
        .overlay.hidden { display: none; }
        .welcome-card { background: #1e293b; border-radius: 16px; padding: 2.5rem; max-width: 520px; width: 90%; border: 1px solid #334155; text-align: center; }
        .welcome-card h2 { font-size: 1.6rem; background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }
        .welcome-card p { color: #94a3b8; margin-bottom: 1.5rem; line-height: 1.6; }
        .welcome-step { text-align: left; background: #0f172a; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
        .welcome-step h3 { color: #60a5fa; font-size: 0.95rem; margin-bottom: 0.5rem; }
        .welcome-step p { color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0.75rem; }
        .welcome-step .step-input { width: 100%; background: #1e293b; border: 1px solid #475569; border-radius: 6px; padding: 0.5rem; color: #e2e8f0; font-size: 0.85rem; margin-bottom: 0.5rem; }
        .welcome-step .step-result { color: #4ade80; font-size: 0.8rem; }
        .btn-primary { background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; border: none; border-radius: 8px; padding: 0.7rem 2rem; cursor: pointer; font-size: 0.95rem; font-weight: 600; margin-top: 0.5rem; }
        .btn-primary:hover { opacity: 0.9; }
        .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
        .btn-skip { background: transparent; color: #64748b; border: 1px solid #475569; border-radius: 8px; padding: 0.5rem 1.5rem; cursor: pointer; font-size: 0.85rem; margin-top: 0.5rem; }
        .btn-skip:hover { border-color: #94a3b8; color: #94a3b8; }

        /* Loading indicator */
        .loading::after { content: '...'; animation: dots 1.5s steps(3, end) infinite; }
        @keyframes dots { 0% { content: '.'; } 33% { content: '..'; } 66% { content: '...'; } }

        /* Degradation warning banner */
        .warning-banner { background: #854d0e; color: #fef08a; padding: 0.6rem 1rem; border-radius: 8px; margin-bottom: 1rem; font-size: 0.85rem; display: none; }
        .warning-banner.visible { display: block; }
        .warning-banner ul { margin: 0.25rem 0 0 1.2rem; padding: 0; }
        .warning-banner li { margin-bottom: 0.15rem; }
    </style>
</head>
<body>
    <!-- Welcome Overlay -->
    <div class="overlay hidden" id="welcome-overlay">
        <div class="welcome-card">
            <div id="welcome-step-1">
                <h2>欢迎使用 Agent Memory V12！</h2>
                <p>你的智能记忆系统，3步轻松上手。</p>
                <div class="welcome-step">
                    <h3>第1步：记住你的第一条记忆</h3>
                    <p>点击按钮，存入你的第一条记忆：</p>
                    <input type="text" class="step-input" id="first-memory-content" value="我是一个使用 Agent Memory V12 管理知识的智能体。">
                    <button class="btn-primary" id="btn-add-first" onclick="addFirstMemory()">写入第一条记忆</button>
                    <div id="first-memory-result" class="step-result"></div>
                </div>
            </div>

            <div id="welcome-step-2" style="display:none;">
                <h2>太好了！现在来搜索</h2>
                <p>记忆已存储，来找到它！</p>
                <div class="welcome-step">
                    <h3>第2步：搜索你的记忆</h3>
                    <p>点击按钮，搜索刚才存入的记忆：</p>
                    <button class="btn-primary" id="btn-search-first" onclick="searchFirstMemory()">搜索我的记忆</button>
                    <div id="search-memory-result" class="step-result"></div>
                </div>
            </div>

            <div id="welcome-step-3" style="display:none;">
                <h2>一切就绪！</h2>
                <p>Agent Memory V12 已准备就绪。几个小提示：</p>
                <div class="welcome-step">
                    <h3>快捷提示</h3>
                    <p>• 使用 <strong>记住</strong> 存储任何你想记住的信息<br>
                       • 使用 <strong>回忆</strong> 搜索你的记忆库<br>
                       • <strong>隐私检测</strong> 保护你的敏感信息<br>
                       • 运行 <code>agent-memory init</code> 完成完整配置</p>
                </div>
                <button class="btn-primary" onclick="closeWelcome()">开始使用</button>
            </div>
        </div>
    </div>

    <div class="container">
        <h1>🧠 Agent Memory 体验中心</h1>
        <p class="subtitle">交互式演示 — 记住、回忆、探索你的智能记忆</p>

        <div class="warning-banner" id="degradation-banner">
            ⚠️ 部分组件不可用，系统运行在降级模式：
            <ul id="degradation-warnings"></ul>
        </div>

        <div class="stats" id="stats">
            <div class="stat" id="stat-memories" onclick="document.getElementById('remember-content').focus()">
                <div class="stat-value" id="total-memories">—</div>
                <div class="stat-label">记忆总数</div>
                <div class="stat-hint" id="memories-hint"></div>
            </div>
            <div class="stat" id="stat-health" onclick="checkHealth()">
                <div class="stat-value" id="health-status">—</div>
                <div class="stat-label">系统状态</div>
                <div class="stat-hint" id="health-hint"></div>
            </div>
            <div class="stat" id="stat-pii">
                <div class="stat-value" id="pii-count">—</div>
                <div class="stat-label">隐私检测</div>
                <div class="stat-hint" id="pii-hint"></div>
            </div>
        </div>

        <div class="card">
            <h2>📝 记住内容</h2>
            <textarea id="remember-content" rows="3" placeholder="输入要记住的内容..." aria-label="输入要记住的内容">小明是一名数据科学家，专注于NLP项目。手机号是13912345678。</textarea>
            <div style="margin-top: 0.75rem; display: flex; gap: 0.5rem; align-items: center;">
                <button id="btn-remember" onclick="remember()" aria-label="记住内容">记住</button>
                <span id="remember-result" style="color: #4ade80; font-size: 0.85rem;"></span>
            </div>
        </div>

        <div class="card">
            <h2>🔍 回忆记忆</h2>
            <div style="display: flex; gap: 0.5rem;">
                <input type="text" id="recall-query" placeholder="回忆你的记忆..." value="NLP" style="flex: 1;" aria-label="输入搜索关键词">
                <button id="btn-recall" onclick="recall()" aria-label="回忆记忆">回忆</button>
            </div>
            <div class="result" id="recall-result" role="status" aria-live="polite">回忆结果将显示在这里...</div>
        </div>

        <div class="card">
            <h2>🔒 隐私检测</h2>
            <textarea id="pii-text" rows="2" placeholder="输入要检测隐私信息的文本...">联系小王：手机13812345678，邮箱wang@company.com</textarea>
            <div style="margin-top: 0.75rem;">
                <button id="btn-detect-pii" onclick="detectPII()" aria-label="检测隐私信息">检测隐私</button>
                <button id="btn-redact-pii" onclick="redactPII()" aria-label="脱敏处理" style="margin-left: 0.5rem; background: linear-gradient(135deg, #ef4444, #dc2626);">脱敏</button>
            </div>
            <div class="result" id="pii-result" role="status" aria-live="polite">隐私分析结果将显示在这里...</div>
        </div>

        <div class="card">
            <h2>🏥 系统状态</h2>
            <button id="btn-health" onclick="checkHealth()">健康检查</button>
            <div class="result" id="health-result" role="status" aria-live="polite">健康检查结果...</div>
        </div>
    </div>

    <script>
        const API = '';
        let _isFirstTime = false;
        let onboardingInProgress = false;

        // --- Debounce utility ---
        function debounce(fn, delay=500) {
            let timer = null;
            return function(...args) {
                if (timer) clearTimeout(timer);
                timer = setTimeout(() => fn.apply(this, args), delay);
            };
        }

        // --- Loading helpers ---
        function setLoading(btnId, loading) {
            const btn = document.getElementById(btnId);
            if (!btn) return;
            if (loading) {
                btn._origText = btn.textContent;
                btn.disabled = true;
                btn.textContent = btn._origText + '...';
            } else {
                btn.disabled = false;
                btn.textContent = btn._origText || btn.textContent.replace(/\\.\\.\\.+/g, '');
            }
        }

        // --- Degradation warning display ---
        function showDegradationWarnings(warnings) {
            if (!warnings || warnings.length === 0) {
                document.getElementById('degradation-banner').classList.remove('visible');
                return;
            }
            const ul = document.getElementById('degradation-warnings');
            ul.innerHTML = warnings.map(w => '<li>' + w + '</li>').join('');
            document.getElementById('degradation-banner').classList.add('visible');
        }

        // --- Onboarding ---
        async function checkOnboarding() {
            try {
                const res = await fetch(API + '/api/onboarding/status');
                const data = await res.json();
                _isFirstTime = data.is_first_time;

                // Update stat hints based on state
                if (_isFirstTime) {
                    document.getElementById('total-memories').textContent = '0';
                    document.getElementById('memories-hint').textContent = '还没有记忆 — 写入你的第一条吧！→';
                    document.getElementById('health-status').textContent = '—';
                    document.getElementById('health-hint').textContent = '未初始化';
                    document.getElementById('pii-count').textContent = '0';
                    document.getElementById('pii-hint').textContent = '隐私保护已就绪';
                    // Show welcome overlay and resume from saved step
                    document.getElementById('welcome-overlay').classList.remove('hidden');
                    const savedStep = data.step || 0;
                    if (savedStep >= 1) {
                        document.getElementById('welcome-step-1').style.display = 'none';
                        if (savedStep >= 2) {
                            document.getElementById('welcome-step-2').style.display = 'none';
                            document.getElementById('welcome-step-3').style.display = 'block';
                        } else {
                            document.getElementById('welcome-step-2').style.display = 'block';
                        }
                    }
                } else {
                    updateStats();
                }
            } catch(e) {
                // Fallback: just load stats
                updateStats();
            }
        }

        async function saveOnboardingProgress(step) {
            try {
                await fetch(API + '/api/onboarding/progress', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({step})
                });
            } catch(e) { console.warn('Failed to save onboarding progress:', e); }
        }

        async function addFirstMemory() {
            if (onboardingInProgress) return;
            onboardingInProgress = true;
            const content = document.getElementById('first-memory-content').value;
            const btn = document.getElementById('btn-add-first');
            btn.disabled = true;
            setLoading('btn-add-first', true);
            try {
                // Also inject seed memories
                await fetch(API + '/api/onboarding/seed', { method: 'POST' });
                const res = await fetch(API + '/api/remember', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({content})
                });
                const data = await res.json();
                document.getElementById('first-memory-result').textContent =
                    data.success ? '✅ 已记住！ID: ' + (data.memory_id || 'OK') : '✗ ' + (data.error || '操作失败');
                // Move to step 2
                saveOnboardingProgress(1);
                setTimeout(() => {
                    document.getElementById('welcome-step-1').style.display = 'none';
                    document.getElementById('welcome-step-2').style.display = 'block';
                }, 800);
            } catch(e) {
                document.getElementById('first-memory-result').textContent = '✗ 错误: ' + e.message;
            } finally {
                setLoading('btn-add-first', false);
                onboardingInProgress = false;
            }
        }

        async function searchFirstMemory() {
            setLoading('btn-search-first', true);
            try {
                const res = await fetch(API + '/api/recall', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: 'Agent Memory', top_k: 3})
                });
                const data = await res.json();
                const results = data.results || [];
                document.getElementById('search-memory-result').textContent =
                    results.length ? '✅ 找到 ' + results.length + ' 条记忆！' : '暂无结果';
                // Move to step 3
                saveOnboardingProgress(2);
                setTimeout(() => {
                    document.getElementById('welcome-step-2').style.display = 'none';
                    document.getElementById('welcome-step-3').style.display = 'block';
                    updateStats();
                }, 800);
            } catch(e) {
                document.getElementById('search-memory-result').textContent = '✗ 错误: ' + e.message;
            } finally {
                setLoading('btn-search-first', false);
            }
        }

        function closeWelcome() {
            document.getElementById('welcome-overlay').classList.add('hidden');
            _isFirstTime = false;
            // Mark onboarding as completed
            fetch(API + '/api/onboarding/complete', { method: 'POST' }).catch(() => {});
            updateStats();
        }

        // --- API calls with loading indicators ---
        async function _doRemember() {
            const content = document.getElementById('remember-content').value;
            if (!content || !content.trim()) {
                document.getElementById('remember-result').textContent = '请输入记忆内容';
                document.getElementById('remember-result').style.color = '#f87171';
                return;
            }
            const btn = document.getElementById('btn-remember');
            btn.disabled = true;
            setLoading('btn-remember', true);
            try {
                const res = await fetch(API + '/api/remember', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({content})
                });
                const data = await res.json();
                document.getElementById('remember-result').style.color = '#4ade80';
                document.getElementById('remember-result').textContent =
                    data.success ? '✅ 已记住！ID: ' + (data.memory_id || 'OK') : '✗ ' + (data.error || '操作失败');
                if (data._warnings) showDegradationWarnings(data._warnings);
                updateStats();
                // Focus management: move focus to result
                document.getElementById('remember-result').focus();
            } catch(e) {
                document.getElementById('remember-result').style.color = '#f87171';
                document.getElementById('remember-result').textContent = '✗ 网络错误: ' + e.message;
            } finally {
                setLoading('btn-remember', false);
            }
        }

        async function _doRecall() {
            const query = document.getElementById('recall-query').value;
            if (!query || !query.trim()) {
                document.getElementById('recall-result').textContent = '请输入搜索关键词';
                return;
            }
            const btn = document.getElementById('btn-recall');
            btn.disabled = true;
            setLoading('btn-recall', true);
            try {
                const res = await fetch(API + '/api/recall', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query, top_k: 5})
                });
                const data = await res.json();
                const results = data.results || [];
                document.getElementById('recall-result').textContent = results.length ?
                    results.map((r, i) => `${i+1}. [${r.score?.toFixed(2) || '-'}] ${r.content?.substring(0, 120)}`).join('\\n') :
                    '未找到相关记忆';
                if (data._warnings) showDegradationWarnings(data._warnings);
                // Focus management: move focus to results area
                document.getElementById('recall-result').focus();
            } catch(e) {
                document.getElementById('recall-result').textContent = '✗ 网络错误: ' + e.message;
            } finally {
                setLoading('btn-recall', false);
            }
        }

        const remember = debounce(_doRemember, 500);
        const recall = debounce(_doRecall, 500);

        async function detectPII() {
            const text = document.getElementById('pii-text').value;
            setLoading('btn-detect-pii', true);
            try {
                const res = await fetch(API + '/api/detect-pii', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text})
                });
                const data = await res.json();
                const findings = data.findings || [];
                document.getElementById('pii-count').textContent = findings.length;
                document.getElementById('pii-hint').textContent = findings.length ? findings.length + ' 项发现' : '';
                document.getElementById('pii-result').textContent = findings.length ?
                    findings.map(f => `• [${f.category}] "${f.value}" at position ${f.start}-${f.end}`).join('\\n') :
                    '✅ 未检测到隐私信息';
            } finally {
                setLoading('btn-detect-pii', false);
            }
        }

        async function redactPII() {
            const text = document.getElementById('pii-text').value;
            setLoading('btn-redact-pii', true);
            try {
                const res = await fetch(API + '/api/redact', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text})
                });
                const data = await res.json();
                document.getElementById('pii-result').textContent = '脱敏结果: ' + (data.redacted || text);
            } finally {
                setLoading('btn-redact-pii', false);
            }
        }

        async function checkHealth() {
            setLoading('btn-health', true);
            try {
                const res = await fetch(API + '/api/health');
                const data = await res.json();
                document.getElementById('health-status').textContent = data.healthy ? '✓' : '✗';
                document.getElementById('health-hint').textContent = data.healthy ? '一切正常' : '发现问题';
                const components = data.components || {};
                document.getElementById('health-result').textContent = Object.entries(components)
                    .map(([k, v]) => `${v ? '✓' : '✗'} ${k}`)
                    .join('\\n');
            } finally {
                setLoading('btn-health', false);
            }
        }

        async function updateStats() {
            try {
                const res = await fetch(API + '/api/stats');
                const data = await res.json();
                const total = data.total_memories || 0;
                document.getElementById('total-memories').textContent = total;
                if (total === 0) {
                    document.getElementById('memories-hint').textContent = '还没有记忆 — 写入你的第一条吧！→';
                } else {
                    document.getElementById('memories-hint').textContent = '';
                }
            } catch(e) { console.warn('Stats update failed:', e); }
        }

        // Initialize
        checkOnboarding();
    </script>
</body>
</html>"""


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8080)
