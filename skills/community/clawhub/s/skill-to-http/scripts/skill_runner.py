#!/usr/bin/env python3
"""skill-to-http 多环境执行引擎

自动检测最优执行方式，按优先级尝试：
1. OpenClaw CLI (openclaw agent --local；HTTP sessions_spawn API 可用时优先)
2. Claude Code (claude_agent_sdk)
3. Codex CLI (subprocess)
4. LLM Fallback (OpenAI 兼容 API)
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import logging
import os
import re
import shutil
import socket
import subprocess
import threading
import time
import uuid
from pathlib import Path
from typing import Any

logger = logging.getLogger("skill-to-http.runner")


def _error_info(exc: BaseException) -> tuple[str, str]:
    """将异常映射为 (error_type, safe_message)，安全不暴露 traceback。
    
    - 已知类型：返回标准 type + 脱敏 message
    - 未知类型：返回异常类名 + sanitized message（不含路径）
    """
    # 已知异常类型 → 标准分类
    import asyncio
    from subprocess import TimeoutExpired
    if isinstance(exc, asyncio.CancelledError):
        return ("cancelled", "Execution cancelled")
    if isinstance(exc, TimeoutExpired):
        return ("timeout", f"Execution timed out after {exc.timeout}s")
    if isinstance(exc, SkillTimeoutError):
        return ("timeout", str(exc))
    if isinstance(exc, ConnectionError):
        return ("network_error", _sanitize_msg(str(exc)))
    if isinstance(exc, OSError):
        # OSError 不都是网络问题（磁盘满/权限/文件不存在等），单独归类避免误导排障
        return ("os_error", _sanitize_msg(str(exc)))
    if isinstance(exc, RuntimeError):
        return ("execution_failed", _sanitize_msg(str(exc)))
    if isinstance(exc, ValueError):
        return ("invalid_params", _sanitize_msg(str(exc)))
    if isinstance(exc, ImportError) or isinstance(exc, ModuleNotFoundError):
        return ("config_error", _sanitize_msg(str(exc)))
    # 未知类型（含 KeyboardInterrupt、SystemExit 等，但 server 端会 re-raise）
    return (type(exc).__name__, _sanitize_msg(str(exc)))


def _sanitize_msg(msg: str) -> str:
    """脱敏：移除常见路径前缀（/home/, /app/, /tmp/ 等），截断过长消息。"""
    cleaned = re.sub(r'(/home/[^\s"]+|/app/[^\s"]+|/tmp/[^\s"]+)', '[path]', msg)
    if len(cleaned) > 500:
        cleaned = cleaned[:500] + "…"
    return cleaned


def _get_openclaw_api_url() -> str:
    """动态读取 OpenClaw Gateway URL。

    优先级：
    1. 环境变量 OPENCLAW_API_URL（最高优先级，显式覆盖）
    2. ~/.openclaw/openclaw.json 中的 gateway.port
    3. 默认值 http://localhost:18789
    """
    if url := os.environ.get("OPENCLAW_API_URL"):
        return url.rstrip("/")
    try:
        cfg_path = Path.home() / ".openclaw" / "openclaw.json"
        if cfg_path.exists():
            cfg = json.loads(cfg_path.read_text())
            port = cfg.get("gateway", {}).get("port")
            if port:
                return f"http://localhost:{port}"
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        logger.debug("Failed to read gateway.port from openclaw.json, using default")
    return "http://localhost:18789"


def _get_gateway_token() -> str:
    """动态读取 OpenClaw Gateway Bearer Token（只存内存，不落盘）。

    优先级：
    1. 环境变量 OPENCLAW_GATEWAY_TOKEN（显式覆盖）
    2. ~/.openclaw/openclaw.json 中的 gateway.auth.token
    3. 返回空字符串（无认证模式）
    """
    if token := os.environ.get("OPENCLAW_GATEWAY_TOKEN"):
        return token
    try:
        cfg_path = Path.home() / ".openclaw" / "openclaw.json"
        if cfg_path.exists():
            cfg = json.loads(cfg_path.read_text())
            token = cfg.get("gateway", {}).get("auth", {}).get("token", "")
            if token:
                return token
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        logger.debug("Failed to read gateway.auth.token from openclaw.json")
    return ""


try:
    from context_meta import load_context_meta as _load_context_meta
except ImportError:
    def _load_context_meta(name: str):  # type: ignore[misc]
        return None


class SkillTimeoutError(RuntimeError):
    """Skill 执行超时异常，由各执行器在超时时抛出。"""
    pass


# ── Webhook 安全：URL 校验（防 SSRF）+ HMAC 回调签名 ─────────────────
def _validate_webhook_url(url: str) -> tuple[bool, str]:
    """校验 webhook_url，阻断明显的 SSRF 向量。

    策略（内网工具的平衡取舍）：
    - 仅允许 http/https scheme
    - 拒绝回环地址（localhost/127.x）——防止回打本机 Gateway/控制台等敏感端口
    - 拒绝链路本地地址（169.254.x，含云 metadata 169.254.169.254）
    - 私网地址放行（内网部署的正常回调目标）
    """
    from urllib.parse import urlparse
    import ipaddress
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "unparsable URL"
    if parsed.scheme not in ("http", "https"):
        return False, f"scheme '{parsed.scheme}' not allowed"
    host = parsed.hostname or ""
    if not host:
        return False, "empty host"
    if host.lower() in ("localhost",):
        return False, "loopback host not allowed"
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError:
        return False, "host does not resolve"
    for info in infos:
        try:
            ip = ipaddress.ip_address(info[4][0])
        except ValueError:
            continue
        if ip.is_loopback:
            return False, "resolves to loopback"
        if ip.is_link_local:
            return False, "resolves to link-local (metadata)"
    return True, ""


def _webhook_signature_headers(job_id: str) -> dict[str, str]:
    """生成 HMAC 回调签名 header（X-Callback-Sig / X-Callback-Ts）。

    config.callback_auth_enabled=false 时返回空 dict（不签名）。
    secret 缺失时自动生成并持久化到 <HTTP_ROOT>/secrets/skill-to-http.hmac，
    接收方从同路径读取 secret 做 verify（见 tls_auth.verify_callback_signature）。
    """
    cfg = _load_config()
    if not cfg.get("callback_auth_enabled", True):
        return {}
    try:
        from tls_auth import (
            load_hmac_secret, save_hmac_secret,
            generate_hmac_secret, compute_callback_signature,
        )
        secret = cfg.get("callback_secret") or load_hmac_secret("skill-to-http")
        if not secret:
            secret = generate_hmac_secret()
            save_hmac_secret("skill-to-http", secret)
            logger.info("Callback HMAC secret auto-generated and persisted")
        ts = int(time.time())
        sig = compute_callback_signature(secret, job_id, ts)
        return {"X-Callback-Sig": sig, "X-Callback-Ts": str(ts)}
    except Exception as e:
        logger.warning(f"Failed to build webhook signature (sending unsigned): {e}")
        return {}


# _EXECUTION_RULES 被 _build_skill_prompt 注入到所有四条执行路径：
#   _call_openclaw / _call_claude_code_async / _call_codex / _call_llm_fallback
# 修改此常量会同时影响全部执行器，请谨慎。
#
# Rule 3（spawn subagent）仅对 openclaw executor 有效；
# 其他执行器无 sessions_spawn 工具，该规则在它们内部会被忽略（无副作用）。
#
# ⚠️ 安全提示：Rule 1（无需确认）对所有 skill 一视同仁。
# 如需对高风险 skill（发邮件、删数据等）保留确认步骤，
# 请在 SKILL.md frontmatter 设置 requires_confirmation: true，
# 并在 _build_skill_prompt 中按该标记决定是否注入 Rule 1。
_EXECUTION_RULES = """\
=== EXECUTION RULES ===
1. Execute immediately. Do NOT ask for confirmation or clarification.
2. If parameters are ambiguous, make reasonable assumptions and proceed.
3. If the skill requires sub-tasks or background work, spawn a subagent
   via sessions_spawn (context: isolated) and wait for the result.
   (Note: only applicable when running under the openclaw executor.)
4. Return only the final result — no meta-commentary."""


SKILL_MD_MAX_CHARS_DEFAULT = 10000


def _build_skill_prompt(
    skill_name: str,
    skill_md: str,
    message: str,
    params_str: str,
    max_chars: int = SKILL_MD_MAX_CHARS_DEFAULT,
    dep_skill_mds: list[tuple[str, str]] | None = None,
) -> str:
    """构建统一的 Skill 执行 prompt（所有执行器共用）。

    dep_skill_mds: [(dep_name, dep_skill_md), ...] 依赖 skill 描述注入
    """
    if len(skill_md) > max_chars:
        skill_md = skill_md[:max_chars] + "\n\n[... SKILL.md truncated ...]"
    base = (
        f"You are executing the Skill '{skill_name}' via HTTP API (no human present).\n"
        f"{_EXECUTION_RULES}\n\n"
        f"=== SKILL.md ===\n{skill_md}\n\n"
    )
    if dep_skill_mds:
        dep_sections = []
        for dep_name, dep_md in dep_skill_mds:
            # 每个依赖 skill 最多注入 3000 chars
            if len(dep_md) > 3000:
                dep_md = dep_md[:3000] + "\n[... truncated ...]"
            dep_sections.append(f"=== 依赖 Skill: {dep_name} ===\n{dep_md}")
        base += "\n".join(dep_sections) + "\n\n"
    base += (
        f"=== TASK ===\n{message}\n\n"
        f"=== PARAMS ===\n{params_str}\n\n"
        f"Execute now and return your final result.\n"
    )
    return base


from _paths import CONFIG_PATH as DEFAULT_CONFIG_PATH


def _check_cc_available() -> bool:
    """检测 claude_agent_sdk 是否可用且接口兼容。
    
    最低要求 0.1.0，且必须有 query() 函数（async generator）。
    """
    spec = importlib.util.find_spec("claude_agent_sdk")
    if not spec:
        return False
    MIN_CC_VERSION = (0, 1, 0)
    try:
        import claude_agent_sdk
        if not hasattr(claude_agent_sdk, "query"):
            return False
        raw = getattr(claude_agent_sdk, "__version__", "0.0.0")
        parts = raw.split(".")
        ver = tuple(int(p) for p in parts[:3]) if len(parts) >= 3 else (0, 0, 0)
        if ver < MIN_CC_VERSION:
            logger.warning(
                "claude_agent_sdk v%s < v%s, upgrade required",
                raw, ".".join(map(str, MIN_CC_VERSION)),
            )
            return False
        return True
    except (ImportError, ValueError, TypeError):
        return False


def _check_claude_cli_available() -> bool:
    """检测 claude CLI 是否可用（claude --version）。"""
    return shutil.which("claude") is not None


def _check_openclaw_available() -> bool:
    """检测 OpenClaw 是否可用（HTTP API 或 CLI）。"""
    # 方法1: 检测 HTTP API
    try:
        import urllib.request
        api_url = _get_openclaw_api_url()
        proxy_handler = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(proxy_handler)
        req = urllib.request.Request(f"{api_url}/api/health", method="GET")
        with opener.open(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        pass
    # 方法2: 检测 openclaw CLI（returncode==2 表示命令不存在；0/1 均视为找到）
    try:
        result = subprocess.run(
            ["openclaw", "agent", "--help"],
            capture_output=True, text=True, timeout=5
        )
        return result.returncode != 2
    except Exception:
        return False


def detect_executor() -> str:
    """按优先级检测可用执行器。

    优先级: openclaw > cc SDK > claude CLI > codex CLI > llm fallback
    """
    if os.environ.get("OPENCLAW_SESSION"):
        return "openclaw"
    if _check_openclaw_available():
        return "openclaw"
    if _check_cc_available():
        return "cc"
    if _check_claude_cli_available():
        return "claude_cli"
    if shutil.which("codex"):
        return "codex"
    return "llm"


def _load_config() -> dict:
    """加载配置文件。"""
    cfg_path = DEFAULT_CONFIG_PATH
    if cfg_path.exists():
        try:
            return json.loads(cfg_path.read_text())
        except (FileNotFoundError, PermissionError, json.JSONDecodeError):
            logger.warning("Failed to parse config.json, using defaults")
    return {}


def _resolve_env(value: str) -> str:
    """解析 ${ENV_VAR} 引用。"""
    if value.startswith("${") and value.endswith("}"):
        env_key = value[2:-1]
        return os.environ.get(env_key, "")
    return value


OPENCLAW_CONNECT_TIMEOUT = 30  # 连接超时固定 30s，与业务 timeout 分离


def _call_openclaw(
    skill_name: str,
    skill_meta: dict,
    message: str,
    params: dict,
    timeout: int,
    gateway_token: str = "",
    speed_mode_agent: str = "",
    dep_skill_mds: list[tuple[str, str]] | None = None,
) -> str:
    """通过 OpenClaw CLI (openclaw agent --local) 执行 Skill。

    优先尝试 HTTP API（兼容旧版 sessions_spawn 端点），
    不可用时回退到 openclaw agent --local CLI。
    """
    # 构建 prompt（注入依赖 skill 描述）
    params_str = json.dumps(params, ensure_ascii=False, indent=2)
    prompt = _build_skill_prompt(
        skill_name, skill_meta.get("skill_md", ""), message, params_str,
        max_chars=skill_meta.get("_max_chars", SKILL_MD_MAX_CHARS_DEFAULT),
        dep_skill_mds=dep_skill_mds,
    )

    # 读取 context_level，决定是否 lightContext（CLI 路径不支持，仅 HTTP API 路径生效）
    meta = _load_context_meta(skill_name)
    light = (meta or {}).get("context_level", "full") == "light"

    # 方法1: 尝试 HTTP API (/tools/invoke → sessions_spawn)
    api_url = _get_openclaw_api_url()
    invoke_url = f"{api_url}/tools/invoke"
    try:
        import urllib.request
        payload = json.dumps({
            "tool": "sessions_spawn",
            "action": "json",
            "args": {
                "task": prompt,
                "mode": "run",
                "runtime": "subagent",
                "lightContext": light,
                "timeoutSeconds": timeout,
            },
            "sessionKey": "main",
        }).encode("utf-8")
        # gateway_token 由调用方（SkillRunner）传入，不在此处重复读文件
        http_headers: dict[str, str] = {"Content-Type": "application/json"}
        if gateway_token:
            http_headers["Authorization"] = f"Bearer {gateway_token}"
        req = urllib.request.Request(
            invoke_url,
            data=payload,
            headers=http_headers,
            method="POST",
        )
        # 绕过 HTTP_PROXY 代理（直连 localhost）
        proxy_handler = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(proxy_handler)
        with opener.open(req, timeout=OPENCLAW_CONNECT_TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
        # /tools/invoke 返回 {ok: true, result: ...}
        if not data.get("ok"):
            err_type = data.get("error", {}).get("type", "unknown")
            raise RuntimeError(f"tools/invoke failed: {err_type}")
        inner = data.get("result", {})
        result = inner.get("result") or inner.get("output") or inner.get("message", "")
        if not result:
            messages = inner.get("messages", [])
            for msg in reversed(messages if isinstance(messages, list) else []):
                if msg.get("role") == "assistant":
                    result = msg.get("content", "")
                    if result:
                        break
        if result:
            logger.debug("OpenClaw HTTP API path succeeded")
            return result
    except Exception as http_err:
        logger.info(f"OpenClaw HTTP API not available ({type(http_err).__name__}: {http_err}), falling back to CLI")

    # 方法2: 回退到 openclaw agent --local CLI
    # 使用唯一 session ID 避免锁冲突
    session_id = f"stt-{uuid.uuid4().hex[:12]}"
    cmd = [
        "openclaw", "agent", "--local",
        "--agent", speed_mode_agent or os.environ.get("OPENCLAW_AGENT_ID", "main"),
        "--session-id", session_id,
        "--message", prompt,
        "--json",
        "--thinking", "off",
        "--timeout", str(max(timeout, 30)),
    ]
    logger.info(f"Running OpenClaw CLI: {' '.join(cmd[:5])}...")

    def _cleanup_session(sid: str) -> None:
        """后台删除本次调用产生的临时 session 文件，避免堆积。"""
        agent_id = speed_mode_agent or os.environ.get("OPENCLAW_AGENT_ID", "main")
        sessions_dir = Path.home() / ".openclaw" / "agents" / agent_id / "sessions"
        try:
            for f in sessions_dir.glob(f"{sid}*"):
                f.unlink(missing_ok=True)
            logger.debug(f"Cleaned up session files for {sid}")
        except Exception as e:
            logger.debug(f"Session cleanup failed (non-critical): {e}")

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 30,  # 额外30s buffer
        )
        if proc.returncode != 0:
            threading.Thread(target=_cleanup_session, args=(session_id,), daemon=True).start()
            raise RuntimeError(f"OpenClaw CLI exited with {proc.returncode}: {proc.stderr[:500]}")
        # openclaw agent --json 输出在 stderr 中（不是 stdout）
        output = proc.stderr or proc.stdout
        # 找 "payloads" 字段，然后回溯到最近的 {
        payloads_pos = output.rfind('"payloads"')
        result: str | None = None
        if payloads_pos >= 0:
            # 从 payloads_pos 往前找最近的 {
            json_start = output.rfind('{', 0, payloads_pos)
            if json_start >= 0:
                # 尝试找到匹配的闭合括号
                depth = 0
                json_end = -1
                for i in range(json_start, len(output)):
                    if output[i] == '{':
                        depth += 1
                    elif output[i] == '}':
                        depth -= 1
                        if depth == 0:
                            json_end = i + 1
                            break
                if json_end > json_start:
                    data = json.loads(output[json_start:json_end])
                    # 提取最终回复
                    payloads = data.get("payloads", [])
                    if payloads and payloads[0].get("text"):
                        result = payloads[0]["text"]
                    elif data.get("meta", {}).get("finalAssistantVisibleText"):
                        result = data["meta"]["finalAssistantVisibleText"]
        if result is None:
            # JSON 解析成功但无法提取 payloads
            logger.warning("OpenClaw CLI: JSON parsed but no 'payloads' field found")
            result = "[skill-to-http] OpenClaw returned unexpected output format"
        threading.Thread(target=_cleanup_session, args=(session_id,), daemon=True).start()
        return result
    except subprocess.TimeoutExpired as exc:
        # subprocess.run 超时时进程已被自动终止，无需手动 kill
        threading.Thread(target=_cleanup_session, args=(session_id,), daemon=True).start()
        raise SkillTimeoutError(f"Execution timed out after {timeout + 30}s")
    except json.JSONDecodeError:
        logger.warning("OpenClaw CLI: failed to parse JSON from output")
        threading.Thread(target=_cleanup_session, args=(session_id,), daemon=True).start()
        return "[skill-to-http] OpenClaw returned non-JSON output"
    except Exception as e:
        threading.Thread(target=_cleanup_session, args=(session_id,), daemon=True).start()
        raise RuntimeError(f"OpenClaw CLI failed: {e}")


async def _call_claude_code_async(
    skill_name: str,
    skill_meta: dict,
    message: str,
    params: dict,
    timeout: int,
    dep_skill_mds: list[tuple[str, str]] | None = None,
) -> str:
    """通过 Claude Code SDK 异步执行。
    
    timeout 通过 asyncio.wait_for 强制生效，超时抛出 SkillTimeoutError。
    """
    from claude_agent_sdk import query

    params_str = json.dumps(params, ensure_ascii=False, indent=2)
    prompt = _build_skill_prompt(skill_name, skill_meta.get("skill_md", ""), message, params_str, max_chars=skill_meta.get("_max_chars", SKILL_MD_MAX_CHARS_DEFAULT), dep_skill_mds=dep_skill_mds)

    async def _run_query():
        last_text = ""
        async for message_event in query(prompt=prompt):
            if hasattr(message_event, 'content'):
                for block in (message_event.content if isinstance(message_event.content, list) else [message_event.content]):
                    if hasattr(block, 'text'):
                        last_text = block.text
            elif isinstance(message_event, str):
                last_text = message_event
        return last_text or "No result"

    try:
        return await asyncio.wait_for(_run_query(), timeout=timeout)
    except asyncio.TimeoutError:
        raise SkillTimeoutError(f"Skill '{skill_name}' execution timed out after {timeout}s")


def _call_claude_code(
    skill_name: str,
    skill_meta: dict,
    message: str,
    params: dict,
    timeout: int,
    dep_skill_mds: list[tuple[str, str]] | None = None,
) -> str:
    """通过 Claude Code SDK 执行（同步包装，供线程内使用）。"""
    try:
        loop = asyncio.get_running_loop()
        # 已有运行中的 event loop，需新建隔离 loop
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(
                _call_claude_code_async(skill_name, skill_meta, message, params, timeout, dep_skill_mds=dep_skill_mds)
            )
        finally:
            new_loop.close()
    except RuntimeError:
        # 当前线程无运行中的 loop，直接新建使用
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(
                _call_claude_code_async(skill_name, skill_meta, message, params, timeout, dep_skill_mds=dep_skill_mds)
            )
        finally:
            new_loop.close()


def _call_claude_cli(
    skill_name: str,
    skill_meta: dict,
    message: str,
    params: dict,
    timeout: int,
    dep_skill_mds: list[tuple[str, str]] | None = None,
) -> str:
    """通过 claude CLI（claude --print）执行 Skill。

    不经过 OpenClaw Gateway，无 sessions_spawn 限制，支持多进程并发。
    工具能力来自 claude CLI 自带工具（bash/read/write/search 等）。
    """
    params_str = json.dumps(params, ensure_ascii=False, indent=2)
    prompt = _build_skill_prompt(
        skill_name, skill_meta.get("skill_md", ""), message, params_str,
        max_chars=skill_meta.get("_max_chars", SKILL_MD_MAX_CHARS_DEFAULT),
        dep_skill_mds=dep_skill_mds,
    )

    # --print：非交互模式输出结果后退出
    # --bare：跳过所有插件和 hooks，减少启动时间（测实比不加 --bare 快 ~1s）
    try:
        proc = subprocess.run(
            ["claude", "--print", "--bare"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        raise RuntimeError("claude CLI not found. Install: npm install -g @anthropic-ai/claude-code")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"claude CLI timed out after {timeout}s")
    if proc.stderr:
        logger.debug(f"claude CLI stderr: {proc.stderr[:500]}")
    if proc.returncode != 0:
        raise RuntimeError(f"claude CLI execution failed (rc={proc.returncode}): {proc.stderr[:500]}")
    return proc.stdout.strip() or "No result"


def _call_codex(
    skill_name: str,
    skill_meta: dict,
    message: str,
    params: dict,
    timeout: int,
    dep_skill_mds: list[tuple[str, str]] | None = None,
) -> str:
    """通过 Codex CLI 执行。"""
    params_str = json.dumps(params, ensure_ascii=False, indent=2)
    prompt = _build_skill_prompt(skill_name, skill_meta.get("skill_md", ""), message, params_str, max_chars=skill_meta.get("_max_chars", SKILL_MD_MAX_CHARS_DEFAULT), dep_skill_mds=dep_skill_mds)

    # 通过 stdin 传入 prompt，避免命令行参数 ARG_MAX 限制
    # --approval-mode full-auto 必须设置，否则 codex 在非 TTY 环境下会等待用户确认
    try:
        proc = subprocess.run(
            ["codex", "--approval-mode", "full-auto"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        raise RuntimeError("codex CLI not found. Install from https://github.com/openai/codex")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Codex execution timed out after {timeout}s")
    if proc.stderr:
        logger.debug(f"Codex stderr: {proc.stderr[:500]}")
    if proc.returncode != 0:
        raise RuntimeError(f"Codex execution failed (rc={proc.returncode}): {proc.stderr}")
    return proc.stdout.strip() or "No result"


def _call_llm(
    skill_name: str,
    skill_meta: dict,
    message: str,
    params: dict,
    timeout: int,
    dep_skill_mds: list[tuple[str, str]] | None = None,
) -> str:
    """通过 LLM Fallback 执行。"""
    import urllib.request

    cfg = _load_config()
    llm_cfg = cfg.get("llm", {})

    base_url = _resolve_env(llm_cfg.get("base_url", "https://api.openai.com/v1"))
    api_key = _resolve_env(llm_cfg.get("api_key", ""))
    model = llm_cfg.get("model", "gpt-4o")

    if not api_key:
        raise RuntimeError("LLM fallback requires api_key in config.json")

    params_str = json.dumps(params, ensure_ascii=False, indent=2)
    prompt = _build_skill_prompt(skill_name, skill_meta.get("skill_md", ""), message, params_str, max_chars=skill_meta.get("_max_chars", SKILL_MD_MAX_CHARS_DEFAULT), dep_skill_mds=dep_skill_mds)

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": f"You are a stateless skill executor. Execute tasks exactly as instructed."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }).encode("utf-8")

    chat_url = f"{base_url.rstrip('/')}/chat/completions"

    req = urllib.request.Request(
        chat_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"LLM execution failed: {e}")


# 执行器注册表。注意：cc 入口有二——
#   _do_run（async）直接 await _call_claude_code_async（并发优化）
#   _do_run_async_job（线程）走此映射 → _call_claude_code（自建 event loop）
EXECUTORS: dict[str, Any] = {
    "openclaw": _call_openclaw,
    "cc": _call_claude_code,
    "claude_cli": _call_claude_cli,
    "codex": _call_codex,
    "llm": _call_llm,
}


class SkillRunner:
    """Skill 执行引擎，支持同步/异步执行。"""

    def __init__(self, executor: str = "auto", max_concurrent: int = 0, skill_md_max_chars: int = SKILL_MD_MAX_CHARS_DEFAULT, gateway_token: str = "", speed_mode_agent: str = "", skill_dirs: list[str] | None = None, speed_mode_fallback: str = "disable") -> None:
        self._executor: str = executor
        self.effective_executor: str = executor if executor != "auto" else detect_executor()
        self._max_concurrent: int = max_concurrent
        self._skill_md_max_chars: int = skill_md_max_chars
        # Gateway token: 优先用传入值，否则动态读取（只存内存，不落盘）
        self._gateway_token: str = gateway_token or _get_gateway_token()
        # 极速模式: 使用专用轻量 agent（仅 openclaw executor 有效）
        self._speed_mode_agent: str = speed_mode_agent if self.effective_executor == "openclaw" else ""
        # 极速模式降级策略: disable=禁用极速重跑, default=用默认agent重跑
        self._speed_mode_fallback: str = speed_mode_fallback
        # skill_dirs: 用于依赖注入时读取依赖 skill 的 SKILL.md
        self._skill_dirs: list[str] = skill_dirs or []
        self._dep_md_cache: dict = {}  # cache_key=(tuple(skill_dirs), skill_name) → str|None
        self._jobs: dict[str, dict] = {}
        self._lock = threading.Lock()
        # 可选：job 状态变更回调 (job_id, status, job_dict)，由 server 侧注册（history 持久化等）
        self.on_job_update = None
        self._semaphore: asyncio.Semaphore | None = None  # 延迟初始化，在 event loop 中创建
        self._thread_semaphore = threading.Semaphore(max_concurrent) if max_concurrent > 0 else None
        self._start_cleanup_thread()
        logger.info(f"SkillRunner initialized, executor: {self.effective_executor}, max_concurrent: {max_concurrent if max_concurrent > 0 else 'unlimited'}, gateway_token: {'set' if self._gateway_token else 'not set'}, speed_mode: {'on (' + self._speed_mode_agent + ')' if self._speed_mode_agent else 'off'}, fallback: {self._speed_mode_fallback}")

    def _resolve_dep_skill_mds(self, skill_name: str) -> list[tuple[str, str]]:
        """读取该 skill 的依赖记录，加载各依赖 skill 的 SKILL.md 内容。"""
        try:
            from dep_scanner import get_skill_deps
            record = get_skill_deps(skill_name)
            if not record or not record.get("deps"):
                return []
            deps = record["deps"]
            if not deps:
                return []
        except ImportError:
            return []

        result: list[tuple[str, str]] = []
        for dep_name in deps:
            dep_md = self._load_dep_skill_md(dep_name)
            if dep_md:
                result.append((dep_name, dep_md))
        return result

    def _load_dep_skill_md(self, skill_name: str) -> str | None:
        """在 skill_dirs 里找到指定 skill 的 SKILL.md 内容（内存缓存避免重复 IO）。"""
        cache_key = (tuple(self._skill_dirs), skill_name)
        if cache_key in self._dep_md_cache:
            return self._dep_md_cache[cache_key]
        val: str | None = None
        for d in self._skill_dirs:
            p = Path(d).expanduser().resolve()
            if not p.is_dir():
                continue
            # 先按目录名查
            candidate = p / skill_name / "SKILL.md"
            if candidate.exists():
                try:
                    val = candidate.read_text(errors="replace")[:4000]
                    break
                except Exception:
                    pass
            # 再扫描 frontmatter name
            for subdir in p.iterdir():
                if not subdir.is_dir():
                    continue
                sm = subdir / "SKILL.md"
                if sm.exists():
                    try:
                        txt = sm.read_text(errors="replace")[:500]
                        if f'name: {skill_name}' in txt or f"name: '{skill_name}'" in txt:
                            val = sm.read_text(errors="replace")[:4000]
                            break
                    except Exception:
                        pass
            if val is not None:
                break
        self._dep_md_cache[cache_key] = val
        return val

    def _run_openclaw_speed_with_fallback(
        self,
        skill_name: str,
        skill_meta_with_cfg: dict,
        message: str,
        params: dict,
        timeout: int,
    ) -> str:
        """极速模式执行 openclaw skill，失败时按降级策略重试。"""
        fn = _call_openclaw
        dep_mds = self._resolve_dep_skill_mds(skill_name)

        # 第一次：极速模式（stt-runner + 注入依赖）
        try:
            result = fn(
                skill_name, skill_meta_with_cfg, message, params, timeout,
                gateway_token=self._gateway_token,
                speed_mode_agent=self._speed_mode_agent,
                dep_skill_mds=dep_mds or None,
            )
            return result
        except Exception as e:
            logger.warning(
                "Speed mode failed for '%s' (%s: %s), applying fallback strategy: %s",
                skill_name, type(e).__name__, e, self._speed_mode_fallback,
            )

        # 降级策略
        if self._speed_mode_fallback == "disable":
            # 禁用极速模式，用正常路径（不指定 agent）重跑
            logger.info("Fallback: retrying '%s' without speed mode agent", skill_name)
            return fn(
                skill_name, skill_meta_with_cfg, message, params, timeout,
                gateway_token=self._gateway_token,
                speed_mode_agent="",  # 不指定，由 env/default 决定
                dep_skill_mds=None,
            )
        elif self._speed_mode_fallback == "default":
            default_agent = _load_config().get("default_agent", "")
            logger.info("Fallback: retrying '%s' with default_agent=%s", skill_name, default_agent or "(env)")
            return fn(
                skill_name, skill_meta_with_cfg, message, params, timeout,
                gateway_token=self._gateway_token,
                speed_mode_agent=default_agent,
                dep_skill_mds=None,
            )
        else:
            raise RuntimeError(f"Unknown speed_mode_fallback strategy: {self._speed_mode_fallback}")

    def _get_semaphore(self) -> asyncio.Semaphore | None:
        """延迟创建 asyncio.Semaphore，确保在正确的 event loop 中创建。"""
        if self._max_concurrent <= 0:
            return None
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self._max_concurrent)
        return self._semaphore

    async def _do_run(
        self,
        skill_name: str,
        skill_meta: dict,
        message: str,
        params: dict,
        timeout: int = 120,
        webhook_url: str | None = None,
    ) -> str:
        """实际执行 Skill（不经过信号量）。"""
        fn = EXECUTORS.get(self.effective_executor)
        if not fn:
            raise RuntimeError(f"Unknown executor: {self.effective_executor}")

        loop = asyncio.get_running_loop()
        # 将 max_chars 注入 skill_meta，各执行函数通过 skill_meta.get('_max_chars') 读取
        skill_meta_with_cfg = {**skill_meta, "_max_chars": self._skill_md_max_chars}
        # openclaw executor: 极速模式+依赖注入+fallback；cc: 直接 await 异步实现 asyncio 并发
        # 其他 executor: run_in_executor 同步调用
        if self.effective_executor == "cc":
            _dep_mds = self._resolve_dep_skill_mds(skill_name) or None
            result = await _call_claude_code_async(skill_name, skill_meta_with_cfg, message, params, timeout, dep_skill_mds=_dep_mds)
        elif self.effective_executor == "openclaw" and self._speed_mode_agent:
            result = await loop.run_in_executor(
                None,
                lambda: self._run_openclaw_speed_with_fallback(skill_name, skill_meta_with_cfg, message, params, timeout),
            )
        elif self.effective_executor == "openclaw":
            _gw_token = self._gateway_token
            result = await loop.run_in_executor(
                None,
                lambda: fn(skill_name, skill_meta_with_cfg, message, params, timeout, gateway_token=_gw_token),
            )
        else:
            # cc / claude_cli / codex / llm: 解析依赖 skill 并注入 prompt
            _dep_mds = self._resolve_dep_skill_mds(skill_name) or None
            result = await loop.run_in_executor(
                None,
                lambda: fn(skill_name, skill_meta_with_cfg, message, params, timeout, dep_skill_mds=_dep_mds),
            )

        if webhook_url and result:
            await self._send_webhook(webhook_url, {
                "job_id": "sync",
                "skill": skill_name,
                "status": "completed",
                "result": result,
            })

        return result

    async def run(
        self,
        skill_name: str,
        skill_meta: dict,
        message: str,
        params: dict,
        timeout: int = 120,
        webhook_url: str | None = None,
    ) -> str:
        """同步执行 Skill（带并发控制）。"""
        sem = self._get_semaphore()
        if sem:
            async with sem:
                return await self._do_run(skill_name, skill_meta, message, params, timeout, webhook_url)
        return await self._do_run(skill_name, skill_meta, message, params, timeout, webhook_url)

    def submit_async(
        self,
        skill_name: str,
        skill_meta: dict,
        message: str,
        params: dict,
        timeout: int = 120,
        webhook_url: str | None = None,
    ) -> str:
        """提交异步任务，返回 job_id。"""
        job_id = str(uuid.uuid4())

        import datetime
        def _now_iso() -> str:
            return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        with self._lock:
            self._jobs[job_id] = {
                "job_id": job_id,
                "skill": skill_name,
                "status": "pending",
                "result": None,
                "error": None,
                "error_type": None,
                "created_at": _now_iso(),
                "finished_at": None,
            }

        thread = threading.Thread(
            target=self._run_async_job,
            args=(job_id, skill_name, skill_meta, message, params, timeout, webhook_url),
            daemon=True,
        )
        thread.start()

        return job_id

    def _run_async_job(
        self,
        job_id: str,
        skill_name: str,
        skill_meta: dict,
        message: str,
        params: dict,
        timeout: int,
        webhook_url: str | None,
    ) -> None:
        """在子线程中执行异步 job（带并发控制）。"""
        if self._thread_semaphore:
            self._thread_semaphore.acquire()
        try:
            self._do_run_async_job(job_id, skill_name, skill_meta, message, params, timeout, webhook_url)
        finally:
            if self._thread_semaphore:
                self._thread_semaphore.release()

    def _do_run_async_job(
        self,
        job_id: str,
        skill_name: str,
        skill_meta: dict,
        message: str,
        params: dict,
        timeout: int,
        webhook_url: str | None,
    ) -> None:
        fn = EXECUTORS.get(self.effective_executor)
        if not fn:
            with self._lock:
                self._jobs[job_id]["status"] = "failed"
                self._jobs[job_id]["error"] = f"Unknown executor: {self.effective_executor}"
            self._notify_job_update(job_id)
            return

        with self._lock:
            self._jobs[job_id]["status"] = "running"
        self._notify_job_update(job_id)

        try:
            import datetime
            skill_meta_with_cfg = {**skill_meta, "_max_chars": self._skill_md_max_chars}
            # openclaw executor: 极速模式+依赖注入+fallback；其他 executor 直接调
            if self.effective_executor == "openclaw" and self._speed_mode_agent:
                result = self._run_openclaw_speed_with_fallback(skill_name, skill_meta_with_cfg, message, params, timeout)
            elif self.effective_executor == "openclaw":
                result = fn(skill_name, skill_meta_with_cfg, message, params, timeout, gateway_token=self._gateway_token)
            else:
                dep_mds = self._resolve_dep_skill_mds(skill_name) or None
                result = fn(skill_name, skill_meta_with_cfg, message, params, timeout, dep_skill_mds=dep_mds)
            with self._lock:
                self._jobs[job_id]["status"] = "completed"
                self._jobs[job_id]["result"] = result
                self._jobs[job_id]["finished_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            self._notify_job_update(job_id)

            if webhook_url:
                self._send_webhook_sync(webhook_url, {
                    "job_id": job_id,
                    "skill": skill_name,
                    "status": "completed",
                    "result": result,
                })
        except BaseException as e:
            # KeyboardInterrupt / SystemExit 应允许进程正常退出，记录后立即重抛
            if isinstance(e, (KeyboardInterrupt, SystemExit)):
                logger.warning(f"Async job {job_id} interrupted by {type(e).__name__}, re-raising")
                raise
            import datetime
            error_type, error_msg = _error_info(e)
            logger.exception(f"Async job {job_id} failed: [{error_type}] {error_msg}")
            with self._lock:
                self._jobs[job_id]["status"] = "failed"
                self._jobs[job_id]["error"] = error_msg
                self._jobs[job_id]["error_type"] = error_type
                self._jobs[job_id]["finished_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            self._notify_job_update(job_id)

            if webhook_url:
                self._send_webhook_sync(webhook_url, {
                    "job_id": job_id,
                    "skill": skill_name,
                    "status": "failed",
                    "error": error_msg,
                    "error_type": error_type,
                })

    def _notify_job_update(self, job_id: str) -> None:
        """状态变更时触发 on_job_update 回调（事件驱动，替代外部轮询）。回调异常不影响主流程。"""
        cb = self.on_job_update
        if not cb:
            return
        with self._lock:
            job = dict(self._jobs.get(job_id) or {})
        if not job:
            return
        try:
            cb(job_id, job.get("status", ""), job)
        except Exception as e:
            logger.warning(f"on_job_update callback failed for {job_id}: {e}")

    def _start_cleanup_thread(self) -> None:
        """启动后台清理线程，每小时清理超过 1 小时的已完成 job。"""
        def cleanup():
            import datetime as _dt
            while True:
                time.sleep(3600)
                try:
                    # created_at 是 ISO 字符串（"%Y-%m-%dT%H:%M:%SZ"），
                    # 同格式字符串按字典序比较等价于时间序比较；禁止与 epoch float 混比。
                    cutoff = (_dt.datetime.now(_dt.timezone.utc) - _dt.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
                    with self._lock:
                        expired = [jid for jid, j in self._jobs.items()
                                  if (j.get("created_at") or "") < cutoff
                                  and j.get("status") in ("completed", "failed")]
                        for jid in expired:
                            del self._jobs[jid]
                    if expired:
                        logger.info(f"Cleaned up {len(expired)} expired jobs")
                except Exception as e:
                    # 清理线程绝不允许静默死亡：记录错误后继续下一轮
                    logger.warning(f"Job cleanup iteration failed: {e}")

        t = threading.Thread(target=cleanup, daemon=True)
        t.start()

    def get_job(self, job_id: str) -> dict | None:
        """查询任务状态。"""
        with self._lock:
            return self._jobs.get(job_id)

    def _send_webhook_sync(self, url: str, payload: dict) -> None:
        """同步发送 webhook 回调（用于子线程）。带 HMAC 签名 + 1 次退避重试。"""
        import urllib.request

        ok, reason = _validate_webhook_url(url)
        if not ok:
            logger.warning(f"Webhook rejected ({reason}): {url}")
            return

        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        headers.update(_webhook_signature_headers(payload.get("job_id", "")))
        last_err: Exception | None = None
        for attempt in range(2):  # 首发 + 1 次退避重试
            try:
                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                urllib.request.urlopen(req, timeout=10)
                return
            except Exception as e:
                last_err = e
                if attempt == 0:
                    time.sleep(2)
        logger.warning(f"Webhook callback failed after retry: {url} ({last_err})")

    async def _send_webhook(self, url: str, payload: dict) -> None:
        """发送 webhook 回调（异步包装，复用同步实现的校验/签名/重试）。"""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, lambda: self._send_webhook_sync(url, payload))