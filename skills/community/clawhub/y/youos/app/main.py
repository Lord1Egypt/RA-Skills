import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.facts_routes import router as facts_router
from app.api.feedback_routes import _BOOKMARKLET_ROUTER as bookmarklet_router
from app.api.feedback_routes import router as feedback_router
from app.api.history_routes import router as history_router
from app.api.review_queue_routes import router as review_queue_router
from app.api.routes import router
from app.api.sender_routes import router as sender_router
from app.api.stats_routes import router as stats_router
from app.api.stream_routes import router as stream_router
from app.core.auth import (
    LoginRateLimiter,
    compute_allowed_origins,
    compute_token_allowed_origins,
    create_session_token,
    is_auth_enabled,
    load_sessions,
    persist_new_session,
    request_origin_allowed,
    token_request_origin_allowed,
    verify_api_token,
    verify_pin,
)
from app.core.config import load_config
from app.core.data_safety import run_startup_safety_checks, validate_instance_paths
from app.core.settings import get_settings

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
SESSION_COOKIE = "youos_session"
SESSION_MAX_AGE = 86400  # 24 hours


class PinAuthMiddleware(BaseHTTPMiddleware):
    """Redirect unauthenticated requests to /login when PIN is configured.

    Two Origin checks on state-changing requests:

    1. **Cookie path** — Origin/Referer must match
       ``compute_allowed_origins`` (defense-in-depth on top of
       ``SameSite=Lax``).
    2. **Token path** — if ``server.token_allowed_origins`` is
       configured, Origin must match that allowlist. When unconfigured
       (the default), token requests authenticate from any origin
       (preserves historical behaviour and back-compat with existing
       extension installs that haven't opted in yet).
    """

    SKIP_PREFIXES = ("/login", "/static")

    def __init__(self, app, config: dict):
        super().__init__(app)
        self.config = config
        # Load persisted sessions (already pruned of expired tokens on load).
        # Keep the creation timestamps in memory so expiry can be enforced
        # server-side — storing only the keys let captured tokens replay
        # indefinitely until process restart, ignoring SESSION_MAX_AGE.
        self.sessions: dict[str, float] = dict(load_sessions())
        self.limiter = LoginRateLimiter()
        self.allowed_origins: set[str] = compute_allowed_origins(config)
        # `None` means "not configured" — token requests aren't origin-
        # checked. A configured (non-empty) set narrows token auth to those
        # origins. Computed once at construction; restart to change.
        self.token_allowed_origins: set[str] | None = compute_token_allowed_origins(config)

    def _origin_check_passes(self, request: Request) -> bool:
        return request_origin_allowed(
            method=request.method,
            origin=request.headers.get("origin"),
            referer=request.headers.get("referer"),
            allowed_origins=self.allowed_origins,
        )

    def _token_origin_check_passes(self, request: Request) -> bool:
        return token_request_origin_allowed(
            method=request.method,
            origin=request.headers.get("origin"),
            allowed_origins=self.token_allowed_origins,
        )

    async def dispatch(self, request: Request, call_next):
        if not is_auth_enabled(self.config):
            return await call_next(request)

        path = request.url.path
        if any(path.startswith(p) for p in self.SKIP_PREFIXES):
            return await call_next(request)

        token = request.cookies.get(SESSION_COOKIE)
        if token:
            created_at = self.sessions.get(token)
            if created_at is not None:
                if time.time() - created_at < SESSION_MAX_AGE:
                    if not self._origin_check_passes(request):
                        return JSONResponse(
                            {"detail": "origin not allowed"},
                            status_code=403,
                        )
                    return await call_next(request)
                # Expired — evict so it can't be reused.
                self.sessions.pop(token, None)

        # Non-cookie clients (the browser extension) authenticate with an API
        # token sent as `X-YouOS-Token` or `Authorization: Bearer <token>`.
        # Token auth is not CSRF-prone: an attacker can't make the browser
        # attach a token they don't already know. We do still check Origin
        # *when the user has configured an allowlist* — that narrows the
        # surface so a compromised page that exfiltrated the token can't
        # also reuse it from any origin. Default (no allowlist) preserves
        # the historical token-authenticates-anywhere behaviour.
        api_token = request.headers.get("x-youos-token")
        if not api_token:
            auth_header = request.headers.get("authorization", "")
            if auth_header[:7].lower() == "bearer ":
                api_token = auth_header[7:].strip()
        if api_token and verify_api_token(api_token):
            if not self._token_origin_check_passes(request):
                return JSONResponse(
                    {"detail": "origin not allowed for token auth"},
                    status_code=403,
                )
            return await call_next(request)

        return RedirectResponse(url="/login", status_code=303)


@asynccontextmanager
async def _lifespan(app: FastAPI):
    settings = get_settings()

    # Run data safety checks at startup
    validate_instance_paths(settings)
    safety_report = run_startup_safety_checks(settings)
    if safety_report.warnings:
        for warning in safety_report.warnings:
            print(f"[YOUOS WARNING]: {warning}")
        # Optionally, block startup here if warnings are critical

    # Warn loudly if the server is reachable beyond the local machine without a
    # PIN. With no PIN, PinAuthMiddleware is a no-op and every endpoint is open.
    config = load_config()
    if not is_auth_enabled(config):
        from app.core.config import get_server_host, get_tailscale_hostname

        host = get_server_host(config)
        loopback = host in ("127.0.0.1", "localhost", "::1", "")
        if not loopback or get_tailscale_hostname(config):
            print(
                "[YOUOS SECURITY]: Server is reachable beyond localhost "
                f"(host={host or '0.0.0.0'}"
                + (", Tailscale enabled" if get_tailscale_hostname(config) else "")
                + ") but no PIN is set — the web UI and API are UNAUTHENTICATED. "
                "Set a PIN under `server.pin` in your config before exposing YouOS."
            )

    # Pre-warm the local model server (load the model once, off the request path)
    # so the first draft isn't slow. Background thread → never blocks startup; a
    # no-op when disabled or when mlx_lm is unavailable.
    try:
        from app.core import model_server

        if model_server.is_enabled():
            import threading

            threading.Thread(target=model_server.ensure_running, daemon=True).start()
    except Exception:
        pass

    yield
    # Clear embedding cache on shutdown
    from app.core.embeddings import clear_embedding_cache

    clear_embedding_cache()

    # Stop the managed model server so it doesn't outlive YouOS.
    try:
        from app.core import model_server

        model_server.stop()
    except Exception:
        pass


def create_app() -> FastAPI:
    settings = get_settings()
    config = load_config()
    instance_name = getattr(settings, "instance_name", "YouOS")
    if instance_name == "YouOS":
        instance_name = str(config.get("user", {}).get("display_name") or instance_name)

    app = FastAPI(
        title=f"{settings.app_name} ({instance_name})",
        version=settings.version,
        description="Your personal AI email copilot — learns your style from your Gmail history.",
        lifespan=_lifespan,
    )
    app.state.settings = settings
    app.state.config = config

    auth_middleware = PinAuthMiddleware(app, config)
    app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware.dispatch)
    app.state.auth = auth_middleware

    # ── Login routes ──
    @app.get("/login", response_class=HTMLResponse)
    async def login_page(request: Request):
        if not is_auth_enabled(config):
            return RedirectResponse(url="/feedback", status_code=303)
        template = (TEMPLATES_DIR / "login.html").read_text(encoding="utf-8")
        return HTMLResponse(template.replace("{{ error }}", ""))

    @app.post("/login")
    async def login_submit(request: Request):
        if not is_auth_enabled(config):
            return RedirectResponse(url="/feedback", status_code=303)

        client_ip = request.client.host if request.client else "unknown"
        if auth_middleware.limiter.is_locked(client_ip):
            template = (TEMPLATES_DIR / "login.html").read_text(encoding="utf-8")
            return HTMLResponse(
                template.replace("{{ error }}", "Too many attempts. Wait 60 seconds."),
                status_code=429,
            )

        form = await request.form()
        pin = form.get("pin", "")
        stored_hash = config.get("server", {}).get("pin", "")

        if verify_pin(str(pin), stored_hash):
            auth_middleware.limiter.reset(client_ip)
            token = create_session_token()
            auth_middleware.sessions[token] = time.time()
            persist_new_session(token)
            response = RedirectResponse(url="/feedback", status_code=303)
            response.set_cookie(SESSION_COOKIE, token, max_age=SESSION_MAX_AGE, httponly=True, samesite="lax")
            return response

        auth_middleware.limiter.record_attempt(client_ip)
        template = (TEMPLATES_DIR / "login.html").read_text(encoding="utf-8")
        return HTMLResponse(
            template.replace("{{ error }}", "Incorrect PIN."),
            status_code=401,
        )

    app.include_router(router)
    app.include_router(feedback_router)
    app.include_router(sender_router)
    app.include_router(review_queue_router)
    app.include_router(stats_router)
    app.include_router(bookmarklet_router)
    app.include_router(stream_router)
    app.include_router(history_router)
    app.include_router(facts_router)

    # Shared front-end assets (design system: youos.css + youos.js). The auth
    # middleware already skips the /static prefix.
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    return app


app = create_app()
