#!/usr/bin/env python3
"""skill-to-http 管理控制台

独立 FastAPI 后端，默认监听 0.0.0.0:9000。
提供 Skill 管理、Job 历史、服务日志、启停控制等能力。
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import uvicorn

# Ensure scripts/ dir is on path so history_store can always be imported
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

# ── 可选模块（import 失败不影响核心功能）────────────────────────────
try:
    from dep_scanner import scan as _dep_scan, get_skill_deps as _dep_get, set_skill_deps as _dep_set
    _dep_available = True
except ImportError:
    _dep_available = False
    _dep_scan = _dep_get = _dep_set = None  # type: ignore[assignment]

try:
    from history_store import get_jobs as _hs_list, get_job as _hs_one, get_stats as _hs_stats
    _history_available = True
except ImportError:
    _history_available = False
    _hs_list = _hs_one = _hs_stats = None  # type: ignore[assignment]
from fastapi.responses import FileResponse, JSONResponse

# ── Paths ────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
UI_DIR = SCRIPT_DIR / "console_ui"
SERVER_SCRIPT = SCRIPT_DIR / "server.py"
from _paths import CONFIG_PATH
from _paths import PID_FILE
from _paths import PORT_FILE
from _paths import LOG_FILE

# ── Logging ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("skill-to-http.console")

# ── Helpers ──────────────────────────────────────────────────────────


def _load_config() -> dict:
    """Load config.json, return empty dict on failure."""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except (FileNotFoundError, PermissionError, json.JSONDecodeError):
            logger.warning("Failed to parse config.json, using defaults")
    return {}


def _save_config(cfg: dict) -> None:
    """Save config.json."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))


def _read_pid() -> tuple[int, int] | None:
    """Read (pid, port) from PID/PORT files."""
    try:
        pid = int(PID_FILE.read_text().strip())
        port = int(PORT_FILE.read_text().strip()) if PORT_FILE.exists() else 0
        return pid, port
    except Exception:
        return None


def _clear_pid() -> None:
    """清除 PID/PORT 文件（进程已确认退出后调用）。"""
    for f in (PID_FILE, PORT_FILE):
        try:
            f.unlink(missing_ok=True)
        except OSError:
            pass


def _reap_children() -> None:
    """回收本进程下已退出的子进程（防僵尸：主服务由控制台 Popen 启动时是子进程）。"""
    try:
        while True:
            pid, _status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
    except ChildProcessError:
        pass  # 没有子进程
    except OSError:
        pass


def _is_server_alive() -> bool:
    """Check if the main skill-to-http server is running."""
    info = _read_pid()
    if not info:
        return False
    pid, _ = info
    _reap_children()
    try:
        os.kill(pid, 0)
    except (ProcessLookupError, PermissionError):
        return False
    # os.kill(pid, 0) 对僵尸进程也会成功，需要看 /proc 状态排除 Z
    try:
        stat = Path(f"/proc/{pid}/stat").read_text()
        # stat 格式：pid (comm) state ...，comm 可能含空格/括号，取右括号后第一个字段
        state = stat.rsplit(")", 1)[1].split()[0]
        if state == "Z":
            return False
    except (OSError, IndexError):
        pass  # /proc 不可用（非 Linux）时维持原判断
    return True


def _server_health_ok(port: int) -> bool:
    """HTTP GET /health on the server, 2s timeout."""
    try:
        req = urllib.request.Request(
            f"http://localhost:{port}/health", method="GET"
        )
        proxy_handler = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(proxy_handler)
        with opener.open(req, timeout=2) as resp:
            return resp.status == 200
    except Exception:
        return False


def _server_running_status() -> dict:
    """Return comprehensive server running status."""
    pid_alive = _is_server_alive()
    info = _read_pid()
    port = info[1] if info else 0
    health_ok = _server_health_ok(port) if pid_alive and port else False
    return {
        "running": pid_alive and health_ok,
        "port": port,
        "pid_alive": pid_alive,
        "health_ok": health_ok,
    }


def _read_log_tail(lines: int = 100) -> str:
    """Read last N lines of server.log."""
    try:
        if not LOG_FILE.exists():
            return ""
        content = LOG_FILE.read_text(errors="replace")
        all_lines = content.splitlines()
        return "\n".join(all_lines[-lines:])
    except Exception as e:
        return f"(Failed to read log: {e})"


def _port_free(port: int) -> bool:
    """检测端口是否可绑定（0.0.0.0，与主服务监听一致）。"""
    import socket as _socket
    s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
    s.setsockopt(_socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1)
    try:
        s.bind(("0.0.0.0", port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def _pick_server_port(config: dict) -> int:
    """为主服务挑选端口：上次运行端口 > config 端口 > 常用默认 > 随机。

    修复：config 端口被其他进程占用时（如 8080 被别的服务占），
    直接用 config 端口会导致「停止后重启永远失败」。
    """
    candidates: list[int] = []
    info = _read_pid()
    if info and info[1]:
        candidates.append(info[1])  # 上次实际运行的端口（最可能可用）
    cfg_port = config.get("port")
    if cfg_port:
        candidates.append(int(cfg_port))
    candidates.extend([8080, 8888, 8899, 18080])
    for p in candidates:
        if _port_free(p):
            return p
    import random as _random
    for _ in range(50):  # 最多试 50 个随机端口，避免极端情况下死循环
        p = _random.randint(10000, 65535)
        if _port_free(p):
            return p
    raise RuntimeError("找不到可用端口（已尝试候选端口 + 50 个随机端口，全部被占用）")


def _now_iso() -> str:
    """UTC ISO timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get_lan_ips() -> list[str]:
    """Get non-loopback IPv4 addresses of this pod."""
    import socket
    ips: list[str] = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            ip = info[4][0]
            if not ip.startswith("127.") and ":" not in ip:
                if ip not in ips:
                    ips.append(ip)
    except Exception:
        pass
    return ips


def _is_allowed_origin(origin: str, lan_ips: list[str]) -> bool:
    """Check if origin is localhost or a pod LAN IP on any port."""
    import re
    ip_group = "|".join(lan_ips) if lan_ips else ""
    if ip_group:
        pattern = rf"^https?://(localhost|127\.0\.0\.1|{ip_group}):\d+$"
    else:
        pattern = r"^https?://(localhost|127\.0\.0\.1):\d+$"
    return bool(re.match(pattern, origin))


# ── App ──────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(title="skill-to-http Console", version="1.0.0")

    # CORS — allow localhost + pod LAN IPs
    _lan_ips = _get_lan_ips()
    _ip_group = "|".join(_lan_ips) if _lan_ips else ""
    if _ip_group:
        _origin_pattern = rf"^https?://(localhost|127\.0\.0\.1|{_ip_group}):\d+$"
    else:
        _origin_pattern = r"^https?://(localhost|127\.0\.0\.1):\d+$"
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=_origin_pattern,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Auth middleware
    config = _load_config()
    api_key = config.get("api_key", "") or ""

    @app.middleware("http")
    async def auth_or_origin_middleware(request: Request, call_next):
        # Only protect /api/* routes
        if not request.url.path.startswith("/api"):
            return await call_next(request)

        # API Key check
        if api_key:
            import hmac as _hmac
            provided = request.headers.get("X-API-Key", "")
            if not _hmac.compare_digest(provided.encode(), api_key.encode()):
                return JSONResponse(
                    {"detail": "Invalid or missing X-API-Key"},
                    status_code=403,
                )
        else:
            # No API key configured: check Origin for CSRF protection
            origin = request.headers.get("Origin", "")
            if origin and not _is_allowed_origin(origin, _lan_ips):
                return JSONResponse(
                    {"detail": "Origin not allowed"},
                    status_code=403,
                )

        return await call_next(request)

    # ── Static files ─────────────────────────────────────────────
    def _no_cache_headers():
        return {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }

    def _static_v():
        """给 static 引用加 mtime 版本号，防止浏览器磁盘缓存 hit。"""
        try:
            files = [UI_DIR / n for n in ("style.css", "app.js", "i18n.js", "index.html")]
            return str(int(max(f.stat().st_mtime for f in files if f.exists())))
        except Exception:
            return "0"

    @app.get("/", response_class=FileResponse)
    @app.get("/index.html")
    async def serve_index():
        # 读 index.html 并注入 ?v=<mtime> 让 CSS/JS 引用带版本号
        html = (UI_DIR / "index.html").read_text(encoding="utf-8")
        v = _static_v()
        html = html.replace('href="/style.css"', f'href="/style.css?v={v}"')
        html = html.replace('src="/i18n.js"', f'src="/i18n.js?v={v}"')
        html = html.replace('src="/app.js"', f'src="/app.js?v={v}"')
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html, headers=_no_cache_headers())

    @app.get("/app.js", response_class=FileResponse)
    async def serve_js():
        return FileResponse(UI_DIR / "app.js", media_type="application/javascript", headers=_no_cache_headers())

    @app.get("/i18n.js", response_class=FileResponse)
    async def serve_i18n():
        return FileResponse(UI_DIR / "i18n.js", media_type="application/javascript", headers=_no_cache_headers())

    @app.get("/style.css", response_class=FileResponse)
    async def serve_css():
        return FileResponse(UI_DIR / "style.css", media_type="text/css", headers=_no_cache_headers())

    @app.get("/assets/logo.jpg", response_class=FileResponse)
    async def serve_logo():
        return FileResponse(UI_DIR / "assets" / "logo.jpg", media_type="image/jpeg")

    # ── API: Status ──────────────────────────────────────────────
    @app.get("/api/status")
    async def api_status():
        status = _server_running_status()
        config = _load_config()
        # Count skills via server if running
        skills_count = 0
        active_jobs = 0
        if status["running"]:
            try:
                req = urllib.request.Request(
                    f"http://localhost:{status['port']}/health", method="GET"
                )
                proxy_handler = urllib.request.ProxyHandler({})
                opener = urllib.request.build_opener(proxy_handler)
                with opener.open(req, timeout=2) as resp:
                    h = json.loads(resp.read().decode())
                    skills_count = h.get("skills_count", 0)
                    active_jobs = h.get("active_jobs", 0)
            except Exception:
                logger.debug("Could not fetch health metrics from main server (non-critical)")

        # Estimate uptime from PID file mtime
        uptime_s = 0
        if status["running"] and PID_FILE.exists():
            try:
                uptime_s = int(time.time() - PID_FILE.stat().st_mtime)
            except Exception:
                logger.debug("Could not estimate uptime from PID file mtime")

        return {
            "running": status["running"],
            "port": status["port"],
            "uptime_seconds": uptime_s,
            "executor": config.get("executor", "auto"),
            "skills_count": skills_count,
            "active_jobs": active_jobs,
            "server_version": "1.0.0",
            "tls_enabled": config.get("tls_enabled", False),
        }

    @app.get("/api/tls")
    async def api_tls_status():
        """HTTPS 证书状态卡片数据源。"""
        config = _load_config()
        result = {
            "tls_enabled": config.get("tls_enabled", False),
            "cert_path": config.get("cert_path", ""),
            "key_path": config.get("key_path", ""),
            "cert_status": None,
        }
        if result["tls_enabled"]:
            try:
                import sys as _sys
                from pathlib import Path as _P
                _scripts_dir = _P(__file__).resolve().parent
                if str(_scripts_dir) not in _sys.path:
                    _sys.path.insert(0, str(_scripts_dir))
                from gen_cert import get_cert_status
                result["cert_status"] = get_cert_status()
            except Exception as e:
                result["cert_status"] = {"error": str(e)}
        return result

    @app.post("/api/tls/renew")
    async def api_tls_renew():
        """触发证书续期。"""
        import subprocess as _sp
        from pathlib import Path as _P
        script = str(_P(__file__).resolve().parent / "gen_cert.py")
        try:
            result = _sp.run(
                [sys.executable, script, "renew", "--san", "auto"],
                capture_output=True, text=True, timeout=30,
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout[-2000:],
                "stderr": result.stderr[-2000:],
            }
        except _sp.TimeoutExpired:
            return {"success": False, "error": "renew timeout (30s)"}

    # ── API: Service control ─────────────────────────────────────
    @app.post("/api/service/start")
    async def api_service_start():
        # 先 stop 旧服务（如果有残留 PID 但端口已被占）
        if _is_server_alive():
            info = _read_pid()
            if info:
                pid, _ = info
                try:
                    os.kill(pid, signal.SIGTERM)
                    for _ in range(5):
                        await asyncio.sleep(1)
                        if not _is_server_alive():
                            break
                    if _is_server_alive():
                        os.kill(pid, signal.SIGKILL)
                        await asyncio.sleep(1)
                except ProcessLookupError:
                    pass
                _clear_pid()

        status = _server_running_status()
        if status["running"]:
            return {"ok": True, "message": "Server already running"}

        config = _load_config()
        # 端口选择：上次运行端口 > config 端口 > 默认候选，全部做占用检测
        try:
            port = _pick_server_port(config)
        except RuntimeError as e:
            return {"ok": False, "message": str(e)}

        # Build command
        cmd = [
            sys.executable,
            str(SERVER_SCRIPT),
            "--non-interactive",
            "--host", "0.0.0.0",
            "--port", str(port),
        ]
        executor = config.get("executor")
        if executor:
            cmd.extend(["--executor", executor])
        # API Key 通过环境变量传递（--api-key 命令行会在进程列表中泄漏）
        child_env = dict(os.environ)
        api_key = config.get("api_key", "")
        if api_key:
            child_env["SKILL_HTTP_API_KEY"] = api_key
        expose = config.get("expose_skills")
        if expose:
            for s in expose:
                cmd.extend(["--expose-skill", s])
        if config.get("no_docs"):
            cmd.append("--no-docs")

        logger.info("Starting server: %s", " ".join(cmd))

        try:
            # Ensure log file directory
            LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(LOG_FILE, "a") as log_fp:
                log_fp.write(f"\n--- Console start at {_now_iso()} ---\n")
                proc = subprocess.Popen(
                    cmd,
                    stdout=log_fp,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                    env=child_env,
                )
        except Exception as e:
            logger.exception("Failed to start server")
            return {
                "ok": False,
                "message": f"Failed to start: {e}",
                "log_tail": _read_log_tail(20),
            }

        # Poll health endpoint for up to 30s (scanning many skills can take time)
        for i in range(30):
            await asyncio.sleep(1)
            info = _read_pid()
            if info:
                _, port = info
                if _server_health_ok(port):
                    logger.info("Server ready after %ds", i + 1)
                    return {"ok": True, "message": "Server started"}

        # Timeout
        logger.warning("Server start timed out after 30s")
        return {
            "ok": False,
            "message": "Server did not become ready within 30s",
            "log_tail": _read_log_tail(20),
        }

    @app.post("/api/service/stop")
    async def api_service_stop():
        if not _is_server_alive():
            return {"ok": True, "message": "Server already stopped"}

        info = _read_pid()
        if not info:
            return {"ok": True, "message": "No PID file, server already stopped"}

        pid, _ = info
        try:
            os.kill(pid, signal.SIGTERM)
            # Wait up to 10s for graceful shutdown (non-blocking)
            for _ in range(10):
                await asyncio.sleep(1)
                if not _is_server_alive():
                    return {"ok": True, "message": "Server stopped"}
            # Force kill if still alive
            os.kill(pid, signal.SIGKILL)
            await asyncio.sleep(1)
            if not _is_server_alive():
                return {"ok": True, "message": "Server killed (force)"}
            return {"ok": False, "message": "Failed to kill server process"}
        except ProcessLookupError:
            return {"ok": True, "message": "Server already stopped"}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    @app.post("/api/service/reload")
    async def api_service_reload():
        status = _server_running_status()
        if not status["running"]:
            raise HTTPException(503, "Server not running")

        try:
            req = urllib.request.Request(
                f"http://localhost:{status['port']}/admin/reload",
                method="POST",
            )
            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy_handler)
            with opener.open(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                return {"ok": True, **data}
        except Exception as e:
            raise HTTPException(502, f"Reload failed: {e}")

    # ── API: Skills ──────────────────────────────────────────────
    @app.get("/api/skills")
    async def api_skills():
        """Return ALL skills from local skill_dirs (not filtered by whitelist),
        enriched with expose status and call stats."""
        config = _load_config()
        expose = config.get("expose_skills", [])
        is_wildcard = "*" in expose
        skill_dirs = config.get("skill_dirs", [])

        # Scan skill dirs locally — independent of whether server is running
        all_skills: list[dict] = []
        seen: set[str] = set()
        for sd in skill_dirs:
            # 修复：config 里的路径可能带 ~ 前缀，必须 expanduser 才能识别到
            sd_path = Path(sd).expanduser()
            if not sd_path.is_dir():
                continue
            for skill_dir in sorted(sd_path.iterdir()):
                if not skill_dir.is_dir() or skill_dir.name in seen:
                    continue
                # 兼容两种布局：
                # 1. <skill>/SKILL.md
                # 2. <skill>/<same-name>/SKILL.md（部分 skill 多嵌套一层）
                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    nested = skill_dir / skill_dir.name / "SKILL.md"
                    if nested.exists():
                        skill_md = nested
                    else:
                        continue
                seen.add(skill_dir.name)
                # Parse description from SKILL.md front-matter
                desc = ""
                try:
                    first_lines = skill_md.read_text(errors="replace")[:1024]
                    import re as _re
                    m = _re.search(r'description:\s*(.+)', first_lines)
                    if m:
                        desc = m.group(1).strip().rstrip('"').lstrip('"')
                except Exception:
                    logger.debug("Could not read description for skill %s", skill_dir.name)
                all_skills.append({"name": skill_dir.name, "description": desc})

        # Enrich with expose status and stats
        # 可选依赖守卫：history_store / context_meta 不可用时降级，不应 500
        try:
            from context_meta import load_context_meta
        except ImportError:
            def load_context_meta(_name):  # type: ignore[misc]
                return None
        stats = {}
        if _history_available:
            try:
                stats = _hs_stats()
            except Exception as e:
                logger.warning("Failed to load history stats (non-critical): %s", e)

        enriched = []
        for s in all_skills:
            name = s["name"]
            exposed = is_wildcard or name in expose
            meta = load_context_meta(name) or {}
            enriched.append({
                **s,
                "exposed": exposed,
                "stats": stats.get(name, {"total": 0, "today": 0}),
                "context_level": meta.get("context_level", "full"),
                "context_level_source": meta.get("context_level_source", "auto"),
            })
        return enriched

    @app.post("/api/skills/{name}/expose")
    async def api_expose_skill(name: str):
        config = _load_config()
        expose = config.get("expose_skills", [])
        is_wildcard = "*" in expose

        if is_wildcard:
            return {"ok": True, "message": "All skills already exposed (wildcard)"}

        if name in expose:
            return {"ok": True, "message": f"'{name}' already exposed"}

        expose.append(name)
        config["expose_skills"] = expose
        _save_config(config)

        # 扫描依赖（如果 dep_scanner 可用）
        dep_scan_result = None
        if _dep_available:
            skill_dirs = config.get("skill_dirs", [])
            skill_meta = None
            try:
                status = _server_running_status()
                if status["running"]:
                    try:
                        req = urllib.request.Request(
                            f"http://localhost:{status['port']}/skills/{name}",
                            method="GET",
                        )
                        api_key = config.get("api_key", "")
                        if api_key:
                            req.add_header("X-API-Key", api_key)
                        proxy_handler = urllib.request.ProxyHandler({})
                        opener = urllib.request.build_opener(proxy_handler)
                        with opener.open(req, timeout=5) as resp:
                            skill_meta = json.loads(resp.read().decode())
                    except Exception:
                        logger.debug("Could not fetch skill meta from main server, falling back to disk")
                if not skill_meta:
                    for d in [str(Path(p).expanduser()) for p in skill_dirs]:
                        sm = Path(d) / name / "SKILL.md"
                        if sm.exists():
                            skill_meta = {"name": name, "path": str(Path(d) / name), "skill_md": sm.read_text(errors="replace")}
                            break
                if skill_meta:
                    scan_result = _dep_scan(name, skill_meta, [str(Path(p).expanduser()) for p in skill_dirs])
                    existing = _dep_get(name) or {}
                    if not existing.get("confirmed_by_user"):
                        existing.update(scan_result)
                        existing["confirmed_by_user"] = False
                        existing["use_speed_mode"] = len(scan_result.get("deps", [])) == 0
                        _dep_set(name, existing)
                    dep_scan_result = scan_result
            except Exception as e:
                logger.warning("Dep scan failed for '%s': %s", name, e)

        # Reload server
        status = _server_running_status()
        if status["running"]:
            try:
                req = urllib.request.Request(
                    f"http://localhost:{status['port']}/admin/reload",
                    method="POST",
                )
                proxy_handler = urllib.request.ProxyHandler({})
                opener = urllib.request.build_opener(proxy_handler)
                with opener.open(req, timeout=5):
                    pass
            except Exception:
                logger.warning("Reload after expose failed (non-critical)")

        return {
            "ok": True,
            "message": f"'{name}' exposed",
            "dep_scan": dep_scan_result,
            # needs_confirm=True 时前端应弹依赖确认弹窗
            "needs_confirm": bool(dep_scan_result and dep_scan_result.get("deps")),
        }

    @app.post("/api/skills/{name}/hide")
    async def api_hide_skill(name: str):
        config = _load_config()
        expose = config.get("expose_skills", [])
        is_wildcard = "*" in expose

        if is_wildcard:
            # Can't hide a specific skill in wildcard mode
            # Replace wildcard with all other skills
            status = _server_running_status()
            if status["running"]:
                try:
                    req = urllib.request.Request(
                        f"http://localhost:{status['port']}/skills",
                        method="GET",
                    )
                    api_key = config.get("api_key", "")
                    if api_key:
                        req.add_header("X-API-Key", api_key)
                    proxy_handler = urllib.request.ProxyHandler({})
                    opener = urllib.request.build_opener(proxy_handler)
                    with opener.open(req, timeout=5) as resp:
                        all_skills = [s["name"] for s in json.loads(resp.read().decode())]
                    new_expose = [s for s in all_skills if s != name]
                    config["expose_skills"] = new_expose
                except Exception:
                    config["expose_skills"] = []
            else:
                config["expose_skills"] = []
            _save_config(config)
        else:
            if name not in expose:
                return {"ok": True, "message": f"'{name}' not exposed"}
            expose.remove(name)
            config["expose_skills"] = expose
            _save_config(config)

        # Reload server
        status = _server_running_status()
        if status["running"]:
            try:
                req = urllib.request.Request(
                    f"http://localhost:{status['port']}/admin/reload",
                    method="POST",
                )
                proxy_handler = urllib.request.ProxyHandler({})
                opener = urllib.request.build_opener(proxy_handler)
                with opener.open(req, timeout=5):
                    pass
            except Exception:
                logger.warning("Reload after hide failed (non-critical)")

        return {"ok": True, "message": f"'{name}' hidden"}

    # ── Context Level ───────────────────────────────────────
    @app.get("/api/skills/{name}/context-level")
    async def api_get_context_level(name: str):
        import re
        if not re.match(r'^[\w\-\.]+$', name):
            raise HTTPException(400, "Invalid skill name")
        from context_meta import load_context_meta
        meta = load_context_meta(name)
        if meta is None:
            return {
                "context_level": "full",
                "context_level_reason": "未检测",
                "context_level_updated": None,
                "context_level_source": "auto",
            }
        return meta

    @app.post("/api/skills/{name}/context-level")
    async def api_set_context_level(name: str, body: dict = None):
        import re
        if not re.match(r'^[\w\-\.]+$', name):
            raise HTTPException(400, "Invalid skill name")
        from context_meta import update_context_level, load_context_meta
        level = (body or {}).get("level", "")
        if level not in ("light", "full"):
            raise HTTPException(400, "level must be 'light' or 'full'")
        update_context_level(name, level)
        meta = load_context_meta(name) or {}
        return {"ok": True, **meta}

    @app.post("/api/skills/{name}/run")
    async def api_run_skill(name: str, body: dict = None):
        status = _server_running_status()
        if not status["running"]:
            raise HTTPException(503, "Server not running")

        message = (body or {}).get("message", "").strip()
        if not message:
            raise HTTPException(400, "message is required")

        config = _load_config()
        api_key = config.get("api_key", "")

        payload = json.dumps({
            "message": message,
            "params": (body or {}).get("params", {}),
            "timeout_seconds": (body or {}).get("timeout_seconds", 120),
        }).encode("utf-8")

        try:
            req = urllib.request.Request(
                f"http://localhost:{status['port']}/skills/{name}/run/async",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            if api_key:
                req.add_header("X-API-Key", api_key)
            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy_handler)
            try:
                with opener.open(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode())
                    return data
            except urllib.error.HTTPError as e:
                body = e.read().decode(errors="replace")
                try:
                    detail = json.loads(body).get("detail", body)
                except Exception:
                    detail = body
                if e.code == 404:
                    raise HTTPException(404, f"Skill '{name}' not found on server (not exposed or not installed)")
                elif e.code == 403:
                    raise HTTPException(403, f"Skill '{name}' is not exposed. Please expose it first.")
                else:
                    raise HTTPException(e.code, f"Server error: {detail}")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(502, f"Run failed: {e}")

    # ── API: Jobs ────────────────────────────────────────────────
    @app.get("/api/jobs")
    async def api_jobs(skill: str = None, limit: int = 50, offset: int = 0):
        try:
            jobs = _hs_list(skill_name=skill, limit=limit, offset=offset)
            return jobs
        except ImportError:
            return []

    @app.get("/api/jobs/{job_id}")
    async def api_job_detail(job_id: str):
        if not _history_available:
            raise HTTPException(500, "history_store not available")
        job = _hs_one(job_id)
        if not job:
            raise HTTPException(404, f"Job '{job_id}' not found")
        return job


    # ── API: Config ──────────────────────────────────────────────
    # ── API: Skill Deps ──────────────────────────────────────────
    @app.get("/api/skills/{name}/deps")
    async def api_get_deps(name: str):
        """返回该 skill 的依赖扫描记录。"""
        if not _dep_available:
            return {"deps": [], "confidence": "high", "evidence": [], "confirmed_by_user": False}
        record = _dep_get(name)
        if not record:
            return {"deps": [], "confidence": "high", "evidence": [], "confirmed_by_user": False}
        return record

    @app.put("/api/skills/{name}/deps")
    async def api_set_deps(name: str, body: dict = None):
        """用户确认/修改依赖记录。body: {deps, confirmed_by_user, use_speed_mode}"""
        if not _dep_available:
            raise HTTPException(500, "dep_scanner not available")
        existing = _dep_get(name) or {}
        update = body or {}
        # 白名单字段合并：只允许改 deps/confirmed_by_user/use_speed_mode
        allowed = {"deps", "confirmed_by_user", "use_speed_mode"}
        filtered = {k: v for k, v in update.items() if k in allowed}
        # 类型校验：deps 必须是 list，元素必须是 str
        if "deps" in filtered:
            deps_val = filtered["deps"]
            if not isinstance(deps_val, list) or not all(isinstance(d, str) for d in deps_val):
                raise HTTPException(422, "deps must be a list of strings")
        existing.update(filtered)
        _dep_set(name, existing)
        return {"ok": True, "record": existing}

    @app.post("/api/skills/{name}/scan_deps")
    async def api_scan_deps(name: str):
        """主动触发依赖扫描，返回扫描结果（不自动写入，需用户确认后调 PUT /deps）。"""
        if not _dep_available:
            raise HTTPException(500, "dep_scanner not available")
        # 获取 skill_meta
        status = _server_running_status()
        config = _load_config()
        skill_dirs = config.get("skill_dirs", [])
        # 从主服务获取 skill_meta
        skill_meta = None
        if status["running"]:
            try:
                req = urllib.request.Request(
                    f"http://localhost:{status['port']}/skills/{name}",
                    method="GET",
                )
                api_key = config.get("api_key", "")
                if api_key:
                    req.add_header("X-API-Key", api_key)
                proxy_handler = urllib.request.ProxyHandler({})
                opener = urllib.request.build_opener(proxy_handler)
                with opener.open(req, timeout=5) as resp:
                    skill_meta = json.loads(resp.read().decode())
            except Exception:
                logger.debug("Could not fetch skill meta from main server, falling back to disk")
        if not skill_meta:
            # 尝试直接从 skill_dirs 扫描
            for d in [str(Path(p).expanduser()) for p in skill_dirs]:
                sm = Path(d) / name / "SKILL.md"
                if sm.exists():
                    skill_meta = {"name": name, "path": str(Path(d) / name), "skill_md": sm.read_text(errors="replace")}
                    break
        if not skill_meta:
            raise HTTPException(404, f"Skill '{name}' not found")
        result = _dep_scan(name, skill_meta, [str(Path(p).expanduser()) for p in skill_dirs])
        return result

    @app.get("/api/config")
    async def api_config():
        config = _load_config()
        # Sanitize: mask api_key
        safe = dict(config)
        if safe.get("api_key"):
            safe["api_key"] = "***"
        else:
            safe["api_key"] = None
        return safe

    # ── API: Logs ────────────────────────────────────────────────
    @app.get("/api/logs")
    async def api_logs():
        content = _read_log_tail(100)
        # Fallback: if server.log is empty, try to fetch from the main server's /api/logs
        if not content:
            status = _server_running_status()
            if status["running"] and status["port"]:
                try:
                    req = urllib.request.Request(
                        f"http://localhost:{status['port']}/api/logs?lines=100",
                        method="GET",
                    )
                    proxy_handler = urllib.request.ProxyHandler({})
                    opener = urllib.request.build_opener(proxy_handler)
                    with opener.open(req, timeout=3) as resp:
                        data = json.loads(resp.read().decode())
                        content = data.get("content", "")
                except Exception:
                    pass
        return {"content": content or "暂无日志。服务日志仅在通过控制台启动服务时记录到 ~/.skill-to-http/server.log。"}

    # ── API: Metrics ─────────────────────────────────────────────
    @app.get("/api/metrics")
    async def api_metrics():
        """返回执行统计：调用次数/成功率/延迟分布。"""
        result: dict = {
            "generated_at": _now_iso(),
            "history_available": _history_available,
            "per_skill": {},
            "totals": {"total": 0, "completed": 0, "failed": 0, "success_rate": 0.0},
            "server": {},
        }
        status = _server_running_status()
        if status["running"]:
            try:
                req = urllib.request.Request(
                    f"http://localhost:{status['port']}/health", method="GET"
                )
                proxy_handler = urllib.request.ProxyHandler({})
                opener = urllib.request.build_opener(proxy_handler)
                with opener.open(req, timeout=3) as resp:
                    health = json.loads(resp.read().decode())
                result["server"] = {
                    "running": True,
                    "executor": health.get("executor", "unknown"),
                    "skills_count": health.get("skills_count", 0),
                    "active_jobs": health.get("active_jobs", 0),
                    "uptime_seconds": health.get("uptime_seconds", 0),
                    "port": status["port"],
                }
            except Exception:
                result["server"] = {"running": True, "port": status["port"]}
        else:
            result["server"] = {"running": False}
        if _history_available:
            try:
                all_jobs = _hs_list(limit=1000)
                by_skill: dict = {}
                latencies: list = []
                for j in all_jobs:
                    sn = j.get("skill_name", "unknown")
                    st = j.get("status", "")
                    ms = j.get("elapsed_ms")
                    if sn not in by_skill:
                        by_skill[sn] = {"total": 0, "completed": 0, "failed": 0, "latencies": []}
                    by_skill[sn]["total"] += 1
                    if st == "completed":
                        by_skill[sn]["completed"] += 1
                    elif st == "failed":
                        by_skill[sn]["failed"] += 1
                    if ms is not None:
                        by_skill[sn]["latencies"].append(ms)
                        latencies.append(ms)

                def _pct(lst: list, p: float):
                    if not lst:
                        return None
                    s = sorted(lst)
                    return s[min(int(len(s) * p / 100), len(s) - 1)]

                for sn, d in by_skill.items():
                    lats = d.pop("latencies")
                    d["success_rate"] = round(d["completed"] / d["total"] * 100, 1) if d["total"] else 0.0
                    d["p50_ms"] = _pct(lats, 50)
                    d["p95_ms"] = _pct(lats, 95)
                    d["avg_ms"] = round(sum(lats) / len(lats)) if lats else None

                result["per_skill"] = by_skill
                total = len(all_jobs)
                completed = sum(1 for j in all_jobs if j.get("status") == "completed")
                failed = sum(1 for j in all_jobs if j.get("status") == "failed")
                result["totals"] = {
                    "total": total,
                    "completed": completed,
                    "failed": failed,
                    "success_rate": round(completed / total * 100, 1) if total else 0.0,
                    "p50_ms": _pct(latencies, 50),
                    "p95_ms": _pct(latencies, 95),
                    "avg_ms": round(sum(latencies) / len(latencies)) if latencies else None,
                }
            except Exception as e:
                result["metrics_error"] = str(e)
        return result

    # ── API: Doctor ─────────────────────────────────────────────
    @app.get("/api/doctor")
    async def api_doctor():
        """运行 doctor 扫描，返回 JSON 报告（不执行修复）。"""
        try:
            import sys as _sys
            if SCRIPT_DIR not in _sys.path:
                _sys.path.insert(0, str(SCRIPT_DIR))
            from doctor import run_scan, to_json_dict
            report = run_scan()
            return to_json_dict(report)
        except ImportError:
            raise HTTPException(500, "doctor module not available")
        except Exception as e:
            raise HTTPException(500, f"Doctor scan failed: {e}")

    @app.post("/api/doctor/fix")
    async def api_doctor_fix():
        """运行 doctor 扫描并自动修复所有 fixable 项，返回修复日志 + 最终报告。"""
        try:
            import sys as _sys
            if SCRIPT_DIR not in _sys.path:
                _sys.path.insert(0, str(SCRIPT_DIR))
            from doctor import run_scan, run_fix, to_json_dict
        except ImportError:
            raise HTTPException(500, "doctor module not available")
        try:
            report = run_scan()
            fix_log = run_fix(report)
            # 修复后重新扫描，返回最新报告
            report2 = run_scan()
            return {
                "fix_log": fix_log,
                "report": to_json_dict(report2),
            }
        except Exception as e:
            raise HTTPException(500, f"Doctor fix failed: {e}")

    # ── API: Speed Mode ──────────────────────────────────────────
    @app.get("/api/speed_mode/status")
    async def api_speed_mode_status():
        try:
            import sys as _sys
            if SCRIPT_DIR not in _sys.path:
                _sys.path.insert(0, str(SCRIPT_DIR))
            from speed_mode import status as sm_status
            st = sm_status()
            st["estimated_speedup"] = "2-4x" if st.get("applicable") else "N/A"
            return st
        except Exception as e:
            return {"enabled": False, "error": str(e)}

    @app.post("/api/speed_mode/enable")
    async def api_speed_mode_enable():
        """SSE stream: 逐步返回初始化进度。"""
        import asyncio as _asyncio
        from fastapi.responses import StreamingResponse
        import sys as _sys
        if SCRIPT_DIR not in _sys.path:
            _sys.path.insert(0, str(SCRIPT_DIR))
        from speed_mode import setup as sm_setup

        async def event_stream():
            loop = _asyncio.get_event_loop()
            # 在线程池中运行同步 generator，避免阻塞事件循环
            import queue, threading
            q = queue.Queue()

            def _run():
                try:
                    for progress in sm_setup():
                        q.put(progress)
                except Exception as e:
                    q.put({"error": True, "msg": str(e)})
                finally:
                    q.put(None)  # sentinel

            t = threading.Thread(target=_run, daemon=True)
            t.start()

            while True:
                try:
                    item = await loop.run_in_executor(None, lambda: q.get(timeout=60))
                except Exception:
                    break
                if item is None:
                    break
                yield f"data: {json.dumps(item, ensure_ascii=False)}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    @app.post("/api/speed_mode/disable")
    async def api_speed_mode_disable():
        import sys as _sys
        if SCRIPT_DIR not in _sys.path:
            _sys.path.insert(0, str(SCRIPT_DIR))
        from speed_mode import teardown as sm_teardown
        result = sm_teardown()
        return result

    return app


# ── CLI ──────────────────────────────────────────────────────────────

from _paths import CONSOLE_PID_FILE
from _paths import CONSOLE_PORT_FILE

def _cmd_start(port: int = 9000, host: str = "0.0.0.0") -> None:
    """Start the console FastAPI server."""
    # 脱离 exec 工具的进程组，防止被 Gateway 超时 SIGTERM 杀掉。
    # setsid() 创建新 session + 进程组，彻底脱离原进程组控制范围。
    try:
        if os.getpid() != os.getsid(0):
            os.setsid()
            logger.debug("Console: setsid() 成功，脱离进程组控制")
    except OSError:
        pass  # 已是 session leader 或无权限，忽略

    from history_store import init_db, cleanup_old_jobs
    init_db()
    cleanup_old_jobs()

    # 写入 PID + PORT 文件，供主服务根路径引导页读取
    CONSOLE_PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONSOLE_PID_FILE.write_text(str(os.getpid()))
    CONSOLE_PORT_FILE.write_text(str(port))

    logger.info("Console starting on http://%s:%d", host, port)
    uvicorn.run(create_app(), host=host, port=port, log_level="info")


def _wait_console_ready(port: int, timeout: int = 15) -> bool:
    """轮询控制台 /api/status 直到就绪，返回是否成功。"""
    url = f"http://127.0.0.1:{port}/api/status"
    for _ in range(timeout * 2):
        try:
            import urllib.request
            req = urllib.request.Request(url, method="GET")
            proxy = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy)
            with opener.open(req, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def _cmd_status() -> None:
    """Print server status and exit."""
    status = _server_running_status()
    if status["running"]:
        print(f"✅ skill-to-http server: running (port {status['port']})")
    else:
        print("❌ skill-to-http server: stopped")
    print(f"   Console: http://0.0.0.0:9000 (use 'start' to launch)")


def _cmd_stop() -> None:
    """Stop the main server and exit."""
    if not _is_server_alive():
        print("Server already stopped.")
        return
    info = _read_pid()
    if not info:
        print("No PID file.")
        return
    pid, _ = info
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Sent SIGTERM to PID {pid}, waiting...")
        for _ in range(10):
            time.sleep(1)
            if not _is_server_alive():
                print("Server stopped.")
                return
        os.kill(pid, signal.SIGKILL)
        print("Server killed (force).")
    except ProcessLookupError:
        print("Server already stopped.")


def _cmd_restart() -> None:
    """Restart the main server."""
    _cmd_stop()
    time.sleep(1)
    # Use the same logic as api_service_start
    config = _load_config()
    try:
        port = _pick_server_port(config)
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)
    cmd = [
        sys.executable, str(SERVER_SCRIPT),
        "--non-interactive", "--host", "0.0.0.0", "--port", str(port),
    ]
    executor = config.get("executor")
    if executor:
        cmd.extend(["--executor", executor])
    # API Key 通过环境变量传递（--api-key 命令行会在进程列表中泄漏）
    child_env = dict(os.environ)
    api_key = config.get("api_key", "")
    if api_key:
        child_env["SKILL_HTTP_API_KEY"] = api_key
    expose = config.get("expose_skills")
    if expose:
        for s in expose:
            cmd.extend(["--expose-skill", s])

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG_FILE, "a") as log_fp:
            log_fp.write(f"\n--- Console restart at {_now_iso()} ---\n")
            subprocess.Popen(cmd, stdout=log_fp, stderr=subprocess.STDOUT, start_new_session=True, env=child_env)
        print("Server restarted.")
    except OSError as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)


def main(argv: list[str] | None = None) -> None:
    args = argv or sys.argv[1:]
    cmd = args[0] if args else "start"
    port = 9000
    host = "0.0.0.0"
    # Parse --port and --host flags
    for i, a in enumerate(args):
        if a == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
        elif a == "--host" and i + 1 < len(args):
            host = args[i + 1]

    if cmd == "status":
        _cmd_status()
    elif cmd == "stop":
        _cmd_stop()
    elif cmd == "restart":
        _cmd_restart()
    elif cmd in ("start",):
        # 前台阻塞运行：先打印访问地址再交给 uvicorn（uvicorn.run 会阻塞到进程退出）。
        # 后台启动 + readiness probe 请用 start-console.sh。
        print(f"🚀 控制台启动中... (http://{host}:{port})")
        print(f"   本机访问: http://127.0.0.1:{port}")
        for lan_ip in _get_lan_ips():
            print(f"   内网访问: http://{lan_ip}:{port}")
        print(f"   （后台启动/就绪探测请用 start-console.sh）")
        _cmd_start(port=port, host=host)
    else:
        print(f"Unknown command: {cmd}. Use: start (default), status, stop, restart")
        sys.exit(1)


if __name__ == "__main__":
    main()