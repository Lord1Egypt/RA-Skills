#!/usr/bin/env python3
"""skill-to-http FastAPI Server

将已安装的 OpenClaw Skill 暴露为 HTTP/HTTPS REST API 服务。
启动后每个 Skill 自动生成对应的 API 端点。
"""

import argparse
import json
import logging
import os
import random
import socket
import sys
import threading
import time
from pathlib import Path

# 自适应：无论从哪个目录调用 server.py，都把 scripts/ 加入 sys.path
# 使 `python3 /any/path/skill-to-http/scripts/server.py` 不报 ModuleNotFoundError
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse

from skill_registry import SkillRegistry
from skill_runner import SkillRunner, SKILL_MD_MAX_CHARS_DEFAULT, SkillTimeoutError, _error_info, _get_gateway_token as _read_gateway_token, _check_openclaw_available, _validate_webhook_url

try:
    from history_store import init_db as _hs_init_db, upsert_job as _hs_upsert_job
    _history_available = True
except ImportError:
    _history_available = False

# ── Logging ──────────────────────────────────────────────────────────
from _paths import LOG_FILE
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(LOG_FILE), mode="a", encoding="utf-8"),
    ],
)
logger = logging.getLogger("skill-to-http")

# ── Defaults ─────────────────────────────────────────────────────────
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORTS = [8080, 8090, 3000, 5000]
from _paths import DATA_DIR as DEFAULT_DATA_DIR
from tls_auth import CERT_DIR as DEFAULT_CERT_DIR
from _paths import CONFIG_PATH as DEFAULT_CONFIG_PATH

# ── API Key Auth ─────────────────────────────────────────────────────
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


def _key_matches(provided: str | None, expected: str) -> bool:
    """常量时间比较 API Key，防 timing attack。"""
    import hmac as _hmac
    return _hmac.compare_digest((provided or "").encode(), expected.encode())


def make_auth_dependency(api_key: str):
    """生成认证 dependency，api_key 为空时不校验。"""
    async def verify_api_key(key: str = Security(API_KEY_HEADER)):
        if not api_key:
            return  # 未配置 key，跳过认证
        if not _key_matches(key, api_key):
            raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return verify_api_key


def _load_server_config() -> dict:
    """从 ~/.skill-to-http/config.json 加载服务配置。"""
    cfg_path = DEFAULT_CONFIG_PATH
    if cfg_path.exists():
        try:
            return json.loads(cfg_path.read_text())
        except (FileNotFoundError, PermissionError, json.JSONDecodeError):
            logger.warning("Failed to parse config.json, using defaults")
    return {}


# ── Request Size Limit ───────────────────────────────────────────────
class LimitRequestSizeMiddleware(BaseHTTPMiddleware):
    """限制请求体大小。"""

    def __init__(self, app, max_bytes: int = 1024 * 1024):  # 默认 1MB
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: StarletteRequest, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_bytes:
            return JSONResponse(
                {"error": f"Request body too large (max {self.max_bytes} bytes)"},
                status_code=413,
            )
        return await call_next(request)


# ── LAN IPs ──────────────────────────────────────────────────────────
def _get_lan_ips() -> list[str]:
    """获取本机所有非回环 IPv4 地址。"""
    ips: list[str] = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            ip = info[4][0]
            if not ip.startswith("127.") and ":" not in ip:  # 只取 IPv4 非回环
                if ip not in ips:
                    ips.append(ip)
    except Exception:
        pass
    return ips


# ── Port Helpers ─────────────────────────────────────────────────────
def find_free_port(host: str = "0.0.0.0") -> int:
    """依次尝试默认端口，全占用则随机选择。"""
    for port in DEFAULT_PORTS:
        if _port_is_free(port, host):
            return port
    port = random.randint(10000, 65535)
    while not _port_is_free(port, host):
        port = random.randint(10000, 65535)
    return port


def _port_is_free(port: int, host: str = "0.0.0.0") -> bool:
    """检测端口是否可用（按实际监听地址探测，避免 127.0.0.1 通过但 0.0.0.0 绑定失败）。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


# ── Request Model ────────────────────────────────────────────────────
class RunRequest(BaseModel):
    """Run Skill 请求体。"""
    message: str
    params: dict = {}
    timeout_seconds: int = Field(default=120, ge=1, le=3600)
    webhook_url: str | None = None


def build_app(
    skill_dirs: list[str],
    data_dir: str,
    executor: str = "auto",
    api_key: str = "",
    auth_dep=None,
    expose_skills: list[str] | None = None,
    deny_skills: list[str] | None = None,
    max_concurrent: int = 0,
    max_request_size_mb: int = 1,
    skill_md_max_chars: int = SKILL_MD_MAX_CHARS_DEFAULT,
    no_docs: bool = False,
    config: dict | None = None,
):
    """构建 FastAPI 应用实例。"""
    # 根据配置决定是否启用文档
    if no_docs or (api_key and (config or {}).get("disable_docs_without_auth", False)):
        app = FastAPI(docs_url=None, redoc_url=None, title="skill-to-http")
    else:
        app = FastAPI(
            title="skill-to-http",
            description="OpenClaw Skill HTTP API Gateway",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc",
        )

    # 请求体大小限制 middleware
    app.add_middleware(
        LimitRequestSizeMiddleware,
        max_bytes=max_request_size_mb * 1024 * 1024,
    )

    # CORS：默认 ["*"]（配合 API Key 已挡 CSRF）；通过 config.cors.allow_origins 可自定义
    _cors_cfg = (config or {}).get("cors", {})
    _cors_origins = _cors_cfg.get("allow_origins", ["*"])
    if not isinstance(_cors_origins, list) or not _cors_origins:
        _cors_origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if _cors_origins != ["*"]:
        logger.info(f"CORS allow_origins: {_cors_origins}")

    # ── 初始化 ──────────────────────────────────────────────────────
    registry = SkillRegistry(
        skill_dirs=skill_dirs,
        data_dir=data_dir,
        expose_skills=expose_skills,
        deny_skills=deny_skills,
    )
    registry.scan()

    # ── 增量扫描 context_level（仅 OpenClaw 环境有效） ──────────
    # CC/Codex/LLM 没有 workspace context 概念，天然只传 SKILL.md + prompt
    # context_level 只被 _call_openclaw 消费，其他 executor 无需扫描
    # 只有当 executor 是 openclaw 或 auto（可能落到 openclaw）时才扫描
    _needs_context_scan = executor in ("openclaw", "auto") and _check_openclaw_available()
    if _needs_context_scan:
        from context_meta import scan_missing
        skill_md_map = {name: registry._skills.get(name, {}).get("skill_md", "") for name in registry._skills}
        scanned = scan_missing(list(skill_md_map.keys()), skill_md_map)
        if scanned:
            logger.info(f"Context level scan: {scanned} new skills scanned")
    else:
        logger.info(f"Context level scan skipped (executor={executor}, only OpenClaw uses workspace context)")

    gateway_token = _read_gateway_token()
    if gateway_token:
        logger.info("Gateway token loaded (HTTP API path enabled)")
    else:
        logger.info("Gateway token not found, HTTP API path disabled (CLI fallback only)")

    # 极速模式：通过 speed_mode 模块检查（兼容重启后自动恢复）
    speed_mode_agent = ""
    speed_mode_fallback = config.get("speed_mode_fallback", "disable") if config else "disable"
    if executor in ("auto", "openclaw"):
        try:
            from speed_mode import status as _sm_status
            sm = _sm_status()
            if sm.get("enabled"):
                speed_mode_agent = sm.get("agent_id", "stt-runner")
                logger.info(f"Speed mode auto-detected: agent={speed_mode_agent}, fallback={speed_mode_fallback}")
        except ImportError:
            # 向后兼容：speed_mode.py 不存在时读 config.json
            if config.get("speed_mode") and config.get("speed_mode_agent"):
                speed_mode_agent = config["speed_mode_agent"]
                logger.info(f"Speed mode enabled (from config), using agent: {speed_mode_agent}")
    runner = SkillRunner(
        executor=executor,
        max_concurrent=max_concurrent,
        skill_md_max_chars=skill_md_max_chars,
        gateway_token=gateway_token,
        speed_mode_agent=speed_mode_agent,
        skill_dirs=skill_dirs,
        speed_mode_fallback=speed_mode_fallback,
    )
    app.state.runner = runner
    app.state.registry = registry  # 供启动 banner 复用，避免二次扫描

    # ── History tracking hook (event-driven via runner.on_job_update) ──
    if _history_available:
        _hs_init_db()
        import datetime as _dt
        _orig_submit = runner.submit_async
        _job_started_at: dict[str, float] = {}
        _job_messages: dict[str, str] = {}

        def _hooked_submit(
            skill_name: str,
            skill_meta: dict,
            message: str,
            params: dict,
            timeout: int = 120,
            webhook_url: str | None = None,
        ) -> str:
            job_id = _orig_submit(skill_name, skill_meta, message, params, timeout, webhook_url)
            created_at = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            _job_started_at[job_id] = time.time()
            _job_messages[job_id] = message
            # 竞态守卫：submit 后 worker 线程可能已推进到 running/completed，
            # 此时跳过 pending 写入，避免把新状态覆盖回 pending。
            try:
                from history_store import get_job as _hs_probe
                _exists = _hs_probe(job_id) is not None
            except Exception:
                _exists = False
            if not _exists:
                _hs_upsert_job(job_id, skill_name, message, "pending", created_at=created_at)
            return job_id

        def _on_job_update(job_id: str, status: str, job: dict) -> None:
            """runner 状态变更回调：直接写 history，无轮询延迟。"""
            skill_name = job.get("skill", "")
            message = _job_messages.get(job_id)
            if status == "running":
                _hs_upsert_job(job_id, skill_name, message, "running")
            elif status in ("completed", "failed"):
                start = _job_started_at.pop(job_id, None)
                _job_messages.pop(job_id, None)
                elapsed = int((time.time() - start) * 1000) if start else None
                finished = job.get("finished_at") or _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                _hs_upsert_job(
                    job_id, skill_name, message, status,
                    result=job.get("result"),
                    error=job.get("error"),
                    error_type=job.get("error_type"),
                    finished_at=finished,
                    elapsed_ms=elapsed,
                )

        runner.submit_async = _hooked_submit
        runner.on_job_update = _on_job_update
        logger.info("History tracking enabled (SQLite, event-driven)")

    # ── 根路径引导页 ────────────────────────────────────────────────
    @app.get("/", include_in_schema=False)
    async def root_redirect():
        console_port = _read_pid_console() or 9000
        html = f"""<!DOCTYPE html>
<html>
<head><title>skill-to-http API Server</title>
<style>
body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 600px; margin: 80px auto; padding: 20px; line-height: 1.6; color: #333; }}
h1 {{ font-size: 28px; margin-bottom: 8px; }}
.status {{ color: #22c55e; font-weight: 600; }}
.card {{ background: #f5f5f5; border-radius: 8px; padding: 20px; margin: 20px 0; }}
a {{ color: #3b82f6; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
code {{ background: #e8e8e8; padding: 2px 6px; border-radius: 4px; font-size: 14px; }}
</style>
</head>
<body>
<h1>🚀 skill-to-http API Server</h1>
<p class="status">● 运行中</p>
<div class="card">
<p><strong>控制台（管理 UI）：</strong><br>
<a href="http://{_get_lan_ips()[0] if _get_lan_ips() else 'localhost'}:{console_port}">
    http://{_get_lan_ips()[0] if _get_lan_ips() else 'localhost'}:{console_port}
</a></p>
<p><strong>API 文档：</strong><br>
<a href="/docs">/docs</a>（Swagger UI） | <a href="/redoc">/redoc</a>（ReDoc）</p>
<p><strong>健康检查：</strong><code>GET /health</code></p>
</div>
<p style="color:#888;font-size:13px;">skill-to-http 将 OpenClaw Skill 暴露为 HTTP REST API</p>
</body>
</html>"""
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html)

    # ── 健康检查 ────────────────────────────────────────────────────
    @app.get("/health")
    async def health_check(
        key: str = Security(API_KEY_HEADER),
    ) -> dict:
        base: dict = {"status": "ok"}
        # 未配置 api_key，或者 key 匹配，返回详情
        if not api_key or _key_matches(key, api_key):
            base.update({
                "executor": runner.effective_executor,
                "executor_description": _executor_desc(runner.effective_executor),
                "skills_count": len(registry.list_skills()),
                "active_jobs": len([j for j in runner._jobs.values() if j["status"] == "running"]),
                "job_ttl_seconds": 3600,
            })
        return base

    # ── 列出 Skills ─────────────────────────────────────────────────
    @app.get("/skills", dependencies=[Depends(auth_dep)])
    async def list_skills() -> list[dict]:
        result: list[dict] = []
        for name in registry.list_skills():
            meta = registry.get_skill(name)
            if meta:
                info: dict = {
                    "name": meta["name"],
                    "description": meta.get("description", ""),
                }
                params_schema = registry.get_params_schema(name)
                if params_schema:
                    info["params"] = params_schema
                result.append(info)
        return result

    # ── 单个 Skill 元信息 ────────────────────────────────────────────
    @app.get("/skills/{name}", dependencies=[Depends(auth_dep)])
    async def get_skill(name: str) -> dict:
        # 先检查 skill 是否存在（内部，不受白名单限制）
        exists = name in registry._skills
        meta = registry.get_skill(name)  # 白名单过滤后
        if meta is None:
            if exists:
                raise HTTPException(status_code=403, detail=f"Skill '{name}' is not exposed")
            else:
                raise HTTPException(status_code=404, detail=f"Skill '{name}' not found")
        info: dict = {
            "name": meta["name"],
            "description": meta.get("description", ""),
            "path": meta.get("path", ""),
        }
        params_schema = registry.get_params_schema(name)
        if params_schema:
            info["params"] = params_schema
        return info

    # ── 同步执行 ────────────────────────────────────────────────────
    @app.post("/skills/{name}/run", dependencies=[Depends(auth_dep)])
    async def run_skill(name: str, request: RunRequest) -> dict:
        exists = name in registry._skills
        meta = registry.get_skill(name)
        if not meta:
            if exists:
                raise HTTPException(status_code=403, detail=f"Skill '{name}' is not exposed")
            else:
                raise HTTPException(status_code=404, detail=f"Skill '{name}' not found")

        if not request.message.strip():
            raise HTTPException(status_code=400, detail="message field is required and cannot be empty")

        if request.webhook_url:
            _wh_ok, _wh_reason = _validate_webhook_url(request.webhook_url)
            if not _wh_ok:
                raise HTTPException(status_code=400, detail=f"Invalid webhook_url: {_wh_reason}")

        message: str = request.message
        params: dict = request.params
        timeout: int = request.timeout_seconds
        webhook_url: str | None = request.webhook_url

        try:
            result = await runner.run(
                skill_name=name,
                skill_meta=meta,
                message=message,
                params=params,
                timeout=timeout,
                webhook_url=webhook_url,
            )
            return {"success": True, "skill": name, "result": result}
        except SkillTimeoutError as e:
            logger.warning(f"Skill '{name}' timed out: {e}")
            return {"success": False, "skill": name, "error": str(e), "error_type": "timeout"}
        except BaseException as e:
            # 用 BaseException 而非 Exception，确保 CancelledError 等也能归类
            if isinstance(e, (KeyboardInterrupt, SystemExit)):
                raise
            error_type, error_msg = _error_info(e)
            logger.exception(f"Skill '{name}' execution failed: [{error_type}] {error_msg}")
            return {"success": False, "skill": name, "error": error_msg, "error_type": error_type}

    # ── 异步执行 ────────────────────────────────────────────────────
    @app.post("/skills/{name}/run/async", dependencies=[Depends(auth_dep)])
    async def run_skill_async(name: str, request: RunRequest) -> dict:
        exists = name in registry._skills
        meta = registry.get_skill(name)
        if not meta:
            if exists:
                raise HTTPException(status_code=403, detail=f"Skill '{name}' is not exposed")
            else:
                raise HTTPException(status_code=404, detail=f"Skill '{name}' not found")

        if not request.message.strip():
            raise HTTPException(status_code=400, detail="message field is required and cannot be empty")

        if request.webhook_url:
            _wh_ok, _wh_reason = _validate_webhook_url(request.webhook_url)
            if not _wh_ok:
                raise HTTPException(status_code=400, detail=f"Invalid webhook_url: {_wh_reason}")

        message: str = request.message
        params: dict = request.params
        webhook_url: str | None = request.webhook_url

        job_id = runner.submit_async(
            skill_name=name,
            skill_meta=meta,
            message=message,
            params=params,
            timeout=request.timeout_seconds,
            webhook_url=webhook_url,
        )
        return {"job_id": job_id, "status": "pending"}

    # ── 查询任务状态 ────────────────────────────────────────────────
    @app.get("/jobs/{job_id}", dependencies=[Depends(auth_dep)])
    async def get_job(job_id: str) -> dict:
        with runner._lock:
            job = runner._jobs.get(job_id)
            if job is None:
                # 区分：已过期（在历史中）vs 完全不存在
                _expired = False
                try:
                    from history_store import get_job as _hs_get_job_detail
                    _expired = _hs_get_job_detail(job_id) is not None
                except Exception:
                    pass  # history_store 不可用或 DB 损坏，走兜底文案
                if _expired:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Job '{job_id}' has expired (TTL: 1 hour). "
                                f"Use GET /history/{job_id} to view the persistent record."
                    )
                raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found (invalid or expired)")
            return dict(job)

    # ── 历史记录查询（仅当 history_store 可用时） ──────────────────
    if _history_available:
        from history_store import get_jobs as _hs_get_jobs, get_job as _hs_get_job, get_stats as _hs_get_stats, cleanup_old_jobs as _hs_cleanup

        @app.get("/history", dependencies=[Depends(auth_dep)])
        async def list_history(
            skill: str | None = None,
            limit: int = 50,
            offset: int = 0,
        ) -> dict:
            """查询历史执行记录（持久化到 SQLite）。"""
            rows = _hs_get_jobs(skill_name=skill, limit=min(limit, 200), offset=max(offset, 0))
            return {"jobs": rows, "count": len(rows)}

        @app.get("/history/stats", dependencies=[Depends(auth_dep)])
        async def history_stats() -> dict:
            """每个 Skill 的执行次数统计。"""
            return _hs_get_stats()

        @app.get("/history/{job_id}", dependencies=[Depends(auth_dep)])
        async def get_history_job(job_id: str) -> dict:
            """查询单条历史记录（job 过期后仍可查）。"""
            row = _hs_get_job(job_id)
            if row is None:
                raise HTTPException(status_code=404, detail=f"History record '{job_id}' not found")
            return row

        @app.delete("/history", dependencies=[Depends(auth_dep)])
        async def cleanup_history(retention_days: int = 7) -> dict:
            """清理超过 retention_days 天的历史记录。"""
            deleted = _hs_cleanup(retention_days=retention_days)
            return {"deleted": deleted}

        # 启动时注册定时清理（每 24h 清一次 7 天前的记录）
        import threading as _cleanup_thr

        def _scheduled_history_cleanup():
            import time as _time
            while True:
                _time.sleep(86400)  # 24h
                try:
                    deleted = _hs_cleanup(retention_days=7)
                    if deleted:
                        logger.info(f"Scheduled history cleanup: removed {deleted} old records")
                except Exception as _ce:
                    logger.warning(f"Scheduled history cleanup failed: {_ce}")

        _cleanup_thr.Thread(target=_scheduled_history_cleanup, daemon=True).start()
        logger.info("History endpoints registered: GET /history, GET /history/stats, GET /history/{job_id}, DELETE /history")

    # ── 管理接口 ────────────────────────────────────────────────────
    @app.get("/api/logs", dependencies=[Depends(auth_dep)])
    async def api_logs(lines: int = 100) -> dict:
        """返回 server.log 最后 N 行（控制台用）。"""
        log_path = LOG_FILE
        try:
            if not log_path.exists():
                return {"content": ""}
            content = log_path.read_text(errors="replace")
            all_lines = content.splitlines()
            return {"content": "\n".join(all_lines[-lines:])}
        except Exception as e:
            return {"content": f"(Failed to read log: {e})"}

    @app.post("/admin/reload", dependencies=[Depends(auth_dep)])
    async def reload_skills() -> dict:
        """重新扫描并注册所有 Skill（不重启服务）。同时重读 config 更新 deny_skills / expose_skills。"""
        old_count = len(registry.list_skills())

        # 重读最新 config，更新 deny_skills / expose_skills（不重启生效）
        fresh_cfg = _load_server_config()

        env_deny = os.environ.get("SKILL_HTTP_DENY_SKILLS", "").strip()
        if env_deny:
            new_deny = {s.strip() for s in env_deny.split(",") if s.strip()}
        else:
            cfg_deny = fresh_cfg.get("deny_skills") or []
            new_deny = {str(s).strip() for s in cfg_deny if str(s).strip()}
        if registry.deny_skills != new_deny:
            logger.info(f"deny_skills updated: {registry.deny_skills} -> {new_deny}")
            registry.deny_skills = new_deny

        env_expose = os.environ.get("SKILL_HTTP_EXPOSE_SKILLS", "").strip()
        if env_expose:
            new_expose = [s.strip() for s in env_expose.split(",") if s.strip()]
        else:
            cfg_expose = fresh_cfg.get("expose_skills") or []
            new_expose = [str(s).strip() for s in cfg_expose if str(s).strip()]
        if new_expose and new_expose != registry.expose_skills:
            logger.info(f"expose_skills updated: {registry.expose_skills} -> {new_expose}")
            registry.expose_skills = new_expose

        registry.scan()
        new_count = len(registry.list_skills())
        logger.info(f"Skills reloaded: {old_count} -> {new_count}")

        # 增量扫描新增 skill 的 context_level（仅 OpenClaw 有效）
        if getattr(app.state.runner, 'effective_executor', '') == 'openclaw':
            from context_meta import scan_missing as _scan_missing_reload
            skill_md_map_reload = {name: registry._skills.get(name, {}).get("skill_md", "") for name in registry._skills}
            scanned_reload = _scan_missing_reload(list(skill_md_map_reload.keys()), skill_md_map_reload)
            if scanned_reload:
                logger.info(f"Context level scan (reload): {scanned_reload} new skills scanned")

        return {"status": "ok", "skills_count": new_count}

    # ── 优雅停机：等待运行中 job 完成（最多 30s）──────────────────
    # 注意：不能用 signal.signal 注册——uvicorn 在 serve() 时会安装自己的
    # SIGTERM/SIGINT 处理器覆盖掉外部注册。uvicorn 收到信号后走 graceful
    # shutdown → 触发 ASGI lifespan shutdown → 本钩子生效。
    @app.on_event("shutdown")
    async def _graceful_drain():
        deadline = time.time() + 30
        while time.time() < deadline:
            with runner._lock:
                running = [j for j in runner._jobs.values() if j["status"] == "running"]
            if not running:
                break
            logger.info(f"Shutdown: waiting for {len(running)} active job(s)...")
            import asyncio as _aio
            await _aio.sleep(1)
        logger.info("Shutdown complete.")

    return app


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="skill-to-http server")
    p.add_argument("--port", type=int, default=None, help="监听端口")
    p.add_argument("--host", default=None, help="监听地址（默认读 config.listen_host 或 0.0.0.0）")
    p.add_argument("--https", action="store_true", help="启用 HTTPS")
    p.add_argument("--cert", type=str, help="HTTPS 证书路径")
    p.add_argument("--key", type=str, help="HTTPS 私钥路径")
    p.add_argument("--skill-dir", action="append", default=[], dest="skill_dirs", help="Skill 目录（可重复）")
    p.add_argument("--data-dir", type=str, help="params 存储目录")
    p.add_argument("--executor", type=str, default=None,
                   choices=["auto", "openclaw", "cc", "claude_cli", "codex", "llm"],
                   help="强制执行器")
    p.add_argument("--no-docs", action="store_true", help="禁用 /docs 和 /redoc 接口")
    p.add_argument("--api-key", type=str, default=None, help="API Key 认证")
    p.add_argument("--expose-skill", action="append", default=None, dest="expose_skills",
                   help="暴露的 Skill（可重复，支持 *）")
    p.add_argument("--max-concurrent", type=int, default=None, help="最大并发数（0=不限）")
    p.add_argument("--max-request-size", type=int, default=None, help="请求体大小限制（MB）")
    p.add_argument("--skill-md-max-chars", type=int, default=None,
                   help="SKILL.md 传入 prompt 的最大字符数（默认 10000，超出截断）")
    p.add_argument("--non-interactive", action="store_true", help="跳过向导，自动创建默认配置（Agent 环境用）")
    p.add_argument("command", nargs="?",
                   choices=["start", "status", "stop", "restart", "doctor",
                            "upgrade-to-https", "cert"],
                   default="start",
                   help="服务控制命令（默认 start）。cert 子命令需配合 --cert-action info/renew/import")
    p.add_argument("--cert-action", choices=["info", "renew", "import"],
                   help="cert 子命令操作类型")
    p.add_argument("--cert-src", help="cert import 模式：源证书路径")
    p.add_argument("--key-src", help="cert import 模式：源私钥路径")
    p.add_argument("--san", help="cert renew 模式：SAN 列表（逗号分隔或 'auto'）")
    p.add_argument("--fix",  action="store_true", help="doctor 模式：自动修复可修复项")
    p.add_argument("--json-output", action="store_true", dest="json_output", help="doctor 模式：JSON 输出")
    return p.parse_args(argv)


# ── Executor 描述 ─────────────────────────────────────
def _executor_desc(name: str) -> str:
    return {
        "openclaw": "OpenClaw — 优先 /tools/invoke，fallback CLI",
        "cc": "Claude Code SDK (claude_agent_sdk.query)",
        "claude_cli": "Claude CLI (claude --print，无 Gateway 限制)",
        "codex": "Codex CLI (subprocess stdin)",
        "llm": "LLM API Fallback (OpenAI 兼容)",
        "auto": "auto-detected",
    }.get(name, name)


# ── PID 管理 ─────────────────────────────────────
from _paths import PID_FILE
from _paths import PORT_FILE


def _write_pid(port: int) -> None:
    """写入 PID + PORT 文件，启动前清理旧进程残留。"""
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    # 如果旧 PID 文件存在且进程已死，清理残留
    info = _read_pid()
    if info:
        old_pid, _ = info
        try:
            os.kill(old_pid, 0)
        except (ProcessLookupError, PermissionError):
            logger.warning("Cleaning stale PID file (old PID %d not running)", old_pid)
            _clear_pid()
    PID_FILE.write_text(str(os.getpid()))
    PORT_FILE.write_text(str(port))


def _clear_pid() -> None:
    for f in (PID_FILE, PORT_FILE):
        try:
            f.unlink(missing_ok=True)
        except Exception:
            pass


from _paths import CONSOLE_PID_FILE
from _paths import CONSOLE_PORT_FILE

def _read_pid() -> tuple[int, int] | None:
    try:
        pid = int(PID_FILE.read_text().strip())
        port = int(PORT_FILE.read_text().strip()) if PORT_FILE.exists() else 0
        return pid, port
    except Exception:
        return None

def _read_pid_console() -> int | None:
    try:
        return int(CONSOLE_PORT_FILE.read_text().strip())
    except Exception:
        return None


def _is_running() -> bool:
    info = _read_pid()
    if not info:
        return False
    pid, _ = info
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def cmd_status() -> None:
    info = _read_pid()
    if info and _is_running():
        pid, port = info
        print(f"✅ skill-to-http 运行中 (PID {pid})")
        print(f"   本机： http://localhost:{port}")
        for lan_ip in _get_lan_ips():
            print(f"   内网： http://{lan_ip}:{port}")
    else:
        print("❌ skill-to-http 未运行")
        _clear_pid()


def cmd_stop() -> None:
    import signal as _signal
    info = _read_pid()
    if not info or not _is_running():
        print("❌ skill-to-http 未运行")
        _clear_pid()
        return
    pid, _ = info
    try:
        os.kill(pid, _signal.SIGTERM)
        print(f"✅ 已发送停止信号给进程 {pid}，等待中...", flush=True)
        for _ in range(30):
            time.sleep(1)
            if not _is_running():
                print("✅ 服务已停止")
                _clear_pid()
                return
        print("⚠️  超时，尝试强杀...")
        os.kill(pid, _signal.SIGKILL)
        _clear_pid()
    except ProcessLookupError:
        print("✅ 服务已停止")
        _clear_pid()


def cmd_cert(args) -> None:
    """证书管理：info / renew / import"""
    import subprocess as _sp
    script = str(Path(__file__).parent / "gen_cert.py")
    action = getattr(args, 'cert_action', None) or 'info'

    cmd = [sys.executable, script]
    if action == "info":
        cmd.append("info")
    elif action == "renew":
        cmd.append("renew")
        san_val = getattr(args, 'san', None) or 'auto'
        cmd.extend(["--san", san_val])
    elif action == "import":
        cmd.append("import")
        cert_src = getattr(args, 'cert_src', None)
        key_src = getattr(args, 'key_src', None)
        if not cert_src or not key_src:
            print("❌ cert import 需要 --cert-src <path> --key-src <path>")
            sys.exit(1)
        cmd.extend(["--cert", cert_src, "--key", key_src])
    else:
        print(f"❌ 未知 cert-action: {action}")
        sys.exit(1)

    try:
        _sp.run(cmd, check=True)
    except _sp.CalledProcessError as e:
        sys.exit(e.returncode)


def cmd_upgrade_to_https() -> None:
    """一键 HTTP → HTTPS 升级：停服 → 改 config → 生成证书 → 启动"""
    print("🔄 开始 HTTP → HTTPS 升级流程")
    print("─" * 60)

    # 1. 停止服务（如果在跑）
    if _is_running():
        print("📌 步骤 1/4: 停止当前服务")
        cmd_stop()
    else:
        print("📌 步骤 1/4: 当前未运行，跳过停止")

    # 2. 改 config.json：tls_enabled = true
    print()
    print("📌 步骤 2/4: 更新 config.json")
    if not DEFAULT_CONFIG_PATH.exists():
        print(f"⚠️  配置文件不存在：{DEFAULT_CONFIG_PATH}")
        print(f"   请先跑 init wizard：python3 server.py")
        sys.exit(1)
    config = _load_server_config()
    config["tls_enabled"] = True
    from tls_auth import DEFAULT_CERT_PATH as _DC, DEFAULT_KEY_PATH as _DK
    config["cert_path"] = str(_DC)
    config["key_path"] = str(_DK)
    DEFAULT_CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2))
    print(f"   ✅ tls_enabled = true")
    print(f"   ✅ cert_path = {_DC}")

    # 3. 生成证书（如果还没有）
    print()
    print("📌 步骤 3/4: 检查/生成 TLS 证书")
    if not _DC.exists() or not _DK.exists():
        import subprocess as _sp
        script = str(Path(__file__).parent / "gen_cert.py")
        _sp.run([sys.executable, script, "--san", "auto", "--force"], check=True)
    else:
        print(f"   ✅ 已有证书：{_DC}")
        from gen_cert import get_cert_status
        st = get_cert_status()
        if st.get("san_mismatch"):
            print("   ⚠️  检测到 SAN 与本机 IP 不匹配，重新生成...")
            import subprocess as _sp
            script = str(Path(__file__).parent / "gen_cert.py")
            _sp.run([sys.executable, script, "--san", "auto", "--force"], check=True)

    # 4. 提示用户重启
    print()
    print("📌 步骤 4/4: 升级完成")
    print("─" * 60)
    print()
    print("✅ HTTPS 升级完成！下一步：")
    print("   启动服务：python3 server.py")
    print("   或：    python3 server.py --https")
    print()
    print("📋 客户端访问方式变化：")
    print("   旧：http://<host>:<port>")
    print("   新：https://<host>:<port>")
    print()
    print("📋 客户端如何信任自签证书：")
    print(f"   curl --cacert {_DC} https://<host>:<port>/health")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    # 子命令分发
    if args.command == "doctor":
        from doctor import main as doctor_main
        argv_doctor: list[str] = []
        if getattr(args, 'fix', False):
            argv_doctor.append("--fix")
        if getattr(args, 'json_output', False):
            argv_doctor.append("--json")
        doctor_main(argv_doctor)
        return
    if args.command == "cert":
        cmd_cert(args)
        return
    if args.command == "upgrade-to-https":
        cmd_upgrade_to_https()
        return
    if args.command == "status":
        cmd_status()
        return
    if args.command == "stop":
        cmd_stop()
        return
    if args.command == "restart":
        cmd_stop()
        time.sleep(1)
        # 继续走 start 流程

    # 首次运行检测
    if getattr(args, 'non_interactive', False):
        # Agent 模式：无配置时自动创建默认，不退出
        if not DEFAULT_CONFIG_PATH.exists():
            DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            import shutil as _shutil
            _template = Path(__file__).parent.parent / "assets" / "config.example.json"
            if _template.exists():
                _shutil.copy(_template, DEFAULT_CONFIG_PATH)
            logger.info(f"Non-interactive: created default config at {DEFAULT_CONFIG_PATH}")

        # 修复 Bug3：确保 api_key 非空，防止裸奔
        try:
            _ni_cfg = json.loads(DEFAULT_CONFIG_PATH.read_text())
            if not _ni_cfg.get("api_key"):
                from tls_auth import generate_api_key, save_api_key, load_api_key
                _existing_key = load_api_key("skill-to-http")
                if not _existing_key:
                    _existing_key = generate_api_key()
                    save_api_key("skill-to-http", _existing_key)
                _ni_cfg["api_key"] = _existing_key
                DEFAULT_CONFIG_PATH.write_text(json.dumps(_ni_cfg, ensure_ascii=False, indent=2))
                logger.info(f"Non-interactive: API Key auto-generated ({len(_existing_key)} chars, stored in <HTTP_ROOT>/secrets/api-keys/)")
        except Exception as _e:
            logger.warning(f"Non-interactive: failed to auto-generate API Key: {_e}")
    else:
        from init_wizard import maybe_run_wizard
        maybe_run_wizard()

    # ── 优先加载 config.json（其他配置项依赖它）───────────────
    config = _load_server_config()
    if DEFAULT_CONFIG_PATH.exists():
        logger.info(f"Config loaded from {DEFAULT_CONFIG_PATH}")
    else:
        logger.info("No config.json found, using defaults")

    # 监听地址：命令行 > 环境变量 > config.json > 默认值 0.0.0.0
    listen_host: str = (
        args.host
        or os.environ.get("SKILL_HTTP_HOST", "")
        or config.get("listen_host", "")
        or DEFAULT_HOST
    )
    # 端口：命令行 > 环境变量 > config.json > 自动选择
    if args.port:
        port = args.port
    elif env_port := os.environ.get("SKILL_HTTP_PORT", "").strip():
        port = int(env_port)
    elif cfg_port := config.get("port"):
        port = int(cfg_port)
    else:
        port = find_free_port(listen_host)

    # 端口占用提前检测（避免绑定失败后才报错）
    if not _port_is_free(port, listen_host):
        logger.error(f"Port {port} is already in use. Please stop the existing server or choose a different port.")
        print(f"\n❌ 端口 {port} 已被占用。请先停止现有服务，或指定其他端口（--port）。\n")
        sys.exit(1)

    # HTTPS：命令行 > 环境变量 > config.json (tls_enabled)
    # 与 references/tls-auth-standard.md 第 2 节 / init_wizard 第 5 步保持一致
    use_https: bool = (
        args.https
        or (os.environ.get("SKILL_HTTP_HTTPS", "0") == "1")
        or bool(config.get("tls_enabled", False))
    )
    # 证书路径：命令行 > 环境变量 > config.json > 标准默认（HTTP_ROOT/certs/server.crt）
    from tls_auth import DEFAULT_CERT_PATH as _STD_CERT, DEFAULT_KEY_PATH as _STD_KEY
    cert_file: str = (
        args.cert
        or os.environ.get("SKILL_HTTP_CERT", "")
        or config.get("cert_path", "")
        or str(_STD_CERT)
    )
    key_file: str = (
        args.key
        or os.environ.get("SKILL_HTTP_KEY", "")
        or config.get("key_path", "")
        or str(_STD_KEY)
    )

    if use_https:
        # 证书不存在或需要重新生成时自动生成
        from gen_cert import generate_cert, _cert_needs_regeneration
        from pathlib import Path as _Path
        needs_regen = (
            not _Path(cert_file).exists()
            or not _Path(key_file).exists()
            or _cert_needs_regeneration(_Path(cert_file), _Path(key_file))
        )
        if needs_regen:
            cert_file, key_file = generate_cert(
                cert_path=cert_file,
                key_path=key_file,
            )

    # Skill 目录：命令行 > 环境变量 > config.json > 默认值
    workspace = os.environ.get("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw" / "workspace"))
    skill_dirs: list[str] = (
        args.skill_dirs
        or [s for s in os.environ.get("SKILL_HTTP_SKILL_DIRS", "").split(",") if s.strip()]
        or [str(Path(p).expanduser()) for p in config.get("skill_dirs", []) if p]
        or [
            str(Path(workspace) / "skills"),
            "/app/skills",
        ]
    )

    # Data 目录：命令行 > 环境变量 > config.json > 默认值
    data_dir: str = (
        args.data_dir
        or os.environ.get("SKILL_TO_HTTP_DATA_DIR", "")
        or config.get("data_dir", "")
        or str(DEFAULT_DATA_DIR)
    )

    # 执行器：命令行 > 环境变量 > config.json > 默认值
    executor: str = (
        args.executor
        or os.environ.get("SKILL_HTTP_EXECUTOR", "")
        or config.get("executor", "auto")
    )

    # API Key: 命令行 > 环境变量 > <HTTP_ROOT>/secrets/api-keys/ > config.json
    # 新规范优先从持久化目录读取（与 agent-easy-http 统一，路径在 workspace 内）
    _file_api_key = ""
    try:
        from tls_auth import load_api_key as _load_api_key
        _file_api_key = _load_api_key("skill-to-http") or ""
    except ImportError:
        pass

    api_key: str = (
        args.api_key
        or os.environ.get("SKILL_HTTP_API_KEY", "")
        or _file_api_key
        or config.get("api_key", "")
    )

    if args.api_key:
        logger.warning("Security: --api-key passed via command line is visible in process list. "
                       "Consider using SKILL_HTTP_API_KEY env var or <HTTP_ROOT>/secrets/api-keys/skill-to-http.key instead.")

    # expose_skills: 命令行 > 环境变量 > config.json
    expose_skills: list[str] | None = None
    if args.expose_skills is not None:
        # 支持逗号分隔：--expose-skill "a,b,c" 等价于 --expose-skill a --expose-skill b --expose-skill c
        expose_skills = list(dict.fromkeys(
            s.strip()
            for item in args.expose_skills
            for s in item.split(",")
            if s.strip()
        ))
    else:
        env_expose = os.environ.get("SKILL_HTTP_EXPOSE_SKILLS", "")
        if env_expose:
            expose_skills = [s.strip() for s in env_expose.split(",") if s.strip()]
        else:
            config_expose = config.get("expose_skills")
            if config_expose is not None:
                expose_skills = config_expose

    # deny_skills: 环境变量 > config.json（仅 config 层支持；命令行不暴露此项以保持简单）
    deny_skills: list[str] = []
    env_deny = os.environ.get("SKILL_HTTP_DENY_SKILLS", "")
    if env_deny:
        deny_skills = [s.strip() for s in env_deny.split(",") if s.strip()]
    else:
        cfg_deny = config.get("deny_skills") or []
        if isinstance(cfg_deny, list):
            deny_skills = [str(s).strip() for s in cfg_deny if str(s).strip()]

    # max_concurrent: 命令行 > 环境变量 > config.json
    max_concurrent: int = 0
    if args.max_concurrent is not None:
        max_concurrent = args.max_concurrent
    else:
        env_mc = os.environ.get("SKILL_HTTP_MAX_CONCURRENT", "")
        if env_mc:
            max_concurrent = int(env_mc)
        else:
            max_concurrent = config.get("max_concurrent", 0)

    # max_request_size_mb: 命令行 > config.json
    max_request_size_mb: int = 1
    if args.max_request_size is not None:
        max_request_size_mb = args.max_request_size
    else:
        max_request_size_mb = config.get("max_request_size_mb", 1)

    # skill_md_max_chars: 命令行 > config.json > 默认 SKILL_MD_MAX_CHARS_DEFAULT
    skill_md_max_chars: int = SKILL_MD_MAX_CHARS_DEFAULT
    if args.skill_md_max_chars is not None:
        skill_md_max_chars = args.skill_md_max_chars
    else:
        skill_md_max_chars = config.get("skill_md_max_chars", SKILL_MD_MAX_CHARS_DEFAULT)
    # 合理性校验：防止 0/-1 导致截断为空，也防止超大值耗尽 token
    SKILL_MD_MAX_CHARS_UPPER = 200_000
    if skill_md_max_chars <= 0:
        logger.warning(f"skill_md_max_chars={skill_md_max_chars} 无效，使用默认值 {SKILL_MD_MAX_CHARS_DEFAULT}")
        skill_md_max_chars = SKILL_MD_MAX_CHARS_DEFAULT
    elif skill_md_max_chars > SKILL_MD_MAX_CHARS_UPPER:
        logger.warning(f"skill_md_max_chars={skill_md_max_chars} 超出上限 {SKILL_MD_MAX_CHARS_UPPER}，已截断")
        skill_md_max_chars = SKILL_MD_MAX_CHARS_UPPER

    # ── 启动前 TLS 硬校验（references/tls-auth-standard.md 第 6 节）──
    # 只对 TLS 路径硬校验（cert/key 文件必须存在）；api_key 留 INFO，
    # 保持 SKILL.md "未配置时跳过认证" 的内网默认语义。
    if use_https:
        from pathlib import Path as _CP
        _errors: list[str] = []
        if not _CP(cert_file).exists():
            _errors.append(
                f"TLS 已启用（tls_enabled=true）但证书不存在：{cert_file}\n"
                f"    生成命令：python3 scripts/gen_cert.py --san auto --force"
            )
        if not _CP(key_file).exists():
            _errors.append(f"TLS 已启用但私钥不存在：{key_file}")
        if _errors:
            print()
            print("=" * 60)
            print("  ❌ 启动前 TLS 校验失败")
            print("=" * 60)
            for err in _errors:
                print(f"  • {err}")
            print()
            sys.exit(1)
    if not api_key:
        logger.info(
            "API Key 未配置 — 服务将以无鉴权模式启动（仅适合本机/受信内网测试）。"
            "建议跑 `python3 scripts/init_wizard.py` 自动生成并启用。"
        )

    # ── 认证 ────────────────────────────────────────────────────
    auth_dep = make_auth_dependency(api_key)

    # 确保目录存在
    os.makedirs(data_dir, exist_ok=True)
    if use_https:
        # 证书目录已在 generate_cert / 标准默认中确保存在；再保险一次
        os.makedirs(str(Path(cert_file).parent), exist_ok=True)

    logger.info(f"Skill dirs: {skill_dirs}")
    logger.info(f"Listen: {listen_host}:{port} ({'HTTPS' if use_https else 'HTTP'})")
    logger.info(f"Executor: {executor} ({_executor_desc(executor)})")
    logger.info(f"API Key: {'configured' if api_key else 'disabled'}")
    logger.info(f"Deny skills: {deny_skills if deny_skills else '(none)'}")
    logger.info(f"Max concurrent: {max_concurrent if max_concurrent > 0 else 'unlimited'}")

    # api_key 和 /docs 安全警告
    if api_key and not args.no_docs:
        logger.warning("API Key is configured but /docs is publicly accessible. Use --no-docs to disable.")

    # 构建应用
    app = build_app(
        skill_dirs=skill_dirs,
        data_dir=data_dir,
        executor=executor,
        api_key=api_key,
        auth_dep=auth_dep,
        expose_skills=expose_skills,
        deny_skills=deny_skills,
        max_concurrent=max_concurrent,
        max_request_size_mb=max_request_size_mb,
        skill_md_max_chars=skill_md_max_chars,
        no_docs=args.no_docs,
        config=config,
    )

    # ── 启动 Banner：展示真实暴露信息（复用 build_app 内已扫描的 registry）──
    _reg = app.state.registry
    exposed_names = _reg.list_skills()
    total_scanned = len(_reg._skills)
    hidden = total_scanned - len(exposed_names)

    schema = "https" if use_https else "http"
    print("\n" + "=" * 56)
    print("  ✨  skill-to-http 启动成功")
    print("=" * 56)
    print(f"  本机访问 : {schema}://localhost:{port}")
    print( "              ↑ 仅限本机进程访问")
    lan_ips = _get_lan_ips()
    for lan_ip in lan_ips:
        print(f"  内网访问 : {schema}://{lan_ip}:{port}")
    if lan_ips:
        print( "              ↑ 其他服务调用此地址（Pod IP，容器重启后可能变化）")
    if not args.no_docs:
        print(f"  API 文档 : {schema}://localhost:{port}/docs")
    print(f"  执行器  : {executor} → {_executor_desc(executor)}")
    # 检测 claude CLI 是否安装，未安装时提示（仅 executor=claude_cli 或 auto 时才提示）
    import shutil as _shutil
    _claude_installed = _shutil.which("claude") is not None
    if not _claude_installed and executor in ("claude_cli", "auto"):
        print()
        print("  ⚠️  claude CLI 未安装，claude_cli executor 不可用")
        print("  安装方法:")
        print("    npm install -g @anthropic-ai/claude-code")
        print("    # 或: pip install claude-code (如有 Python 版本)")
        print("  安装后重启服务即可自动使用 claude_cli executor")
        if executor == "claude_cli":
            print("  ⛔ executor 强制指定为 claude_cli 但未安装，调用将失败")
        print()
    if exposed_names:
        if len(exposed_names) <= 5:
            skills_str = ", ".join(exposed_names)
        else:
            skills_str = ", ".join(exposed_names[:5]) + f" ... 共 {len(exposed_names)} 个"
        print(f"  已暴露  : {skills_str}")
    else:
        print("  已暴露  : 无——请在 config.json 中配置 expose_skills")
    if hidden > 0:
        print(f"  未开放  : {hidden} 个 Skill 已安装但未暴露，如需请在 expose_skills 中添加")
    if deny_skills:
        _deny_preview = ", ".join(deny_skills[:3]) + (f" ... 共 {len(deny_skills)} 个" if len(deny_skills) > 3 else "")
        print(f"  反向黑名单: {_deny_preview}（即使在 expose 内也被拒绝）")
    print(f"  认证    : {'API Key 已启用 (X-API-Key header)' if api_key else '未启用（内网公开）'}")
    print("=" * 56)
    # 安全提示：0.0.0.0 暴露但裸 HTTP（默认模式提醒，不强制必开）
    if listen_host == "0.0.0.0" and not use_https:
        print()
        print("  ⚠️  当前监听 0.0.0.0（局域网可达）但 TLS 未启用，调用方走明文 HTTP。")
        print("     仅限信任网络使用。要切回 HTTPS：")
        print("     1. python3 scripts/gen_cert.py --san auto")
        print(f"     2. 编辑 {DEFAULT_CONFIG_PATH} 把 tls_enabled 改 true")
        print("     3. python3 scripts/server.py restart")
    print()

    # 写入 PID 文件（供 status/stop 子命令使用）
    _write_pid(port)

    # 启动 uvicorn
    config_obj = uvicorn.Config(
        app=app,
        host=listen_host,
        port=port,
        log_level="info",
    )
    if use_https:
        config_obj.ssl_certfile = cert_file
        config_obj.ssl_keyfile = key_file

    # Graceful shutdown 由 build_app 内的 ASGI shutdown 钩子处理
    # （uvicorn 会覆盖外部 signal.signal 注册，故不能在此注册 SIGTERM/SIGINT）。

    server = uvicorn.Server(config_obj)
    try:
        server.run()
    finally:
        _clear_pid()


if __name__ == "__main__":
    main()