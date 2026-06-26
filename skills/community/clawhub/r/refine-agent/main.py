#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                     R E F I N E  v1.3                       ║
║       Adaptive Session Diagnostics · ClawHub / SkillPay     ║
╚══════════════════════════════════════════════════════════════╝

Dual-mode skill engine: captures error patterns and feedback labels,
and (in PRO mode) synthesises System Prompt Patches from local analysis.

All environment variables are optional:
  REFINE_MODE           — "BASIC" (default) or "PRO"
  SKILLPAY_TOKEN_HASH   — SHA-256 hex of SkillPay token (PRO only)
  LOG_LEVEL             — "DEBUG" | "INFO" (default) | "WARNING" | "ERROR"

Data written to disk (refine_memory.json):
  · Error type names and truncated first-line messages
  · Short feedback labels (truncated)
  · Context dicts — sanitized: string values truncated, sensitive keys
    blocked, nested objects rejected, max 8 keys enforced
  · No stack traces, no raw prompts, no credentials

No network calls are made by this skill.
"""

# ─── Standard Library Only ────────────────────────────────────────────────────
import os
import re
import hmac
import json
import uuid
import hashlib
import logging
import datetime
from pathlib import Path

# ─── Configuration ────────────────────────────────────────────────────────────
MEMORY_FILE  = Path("refine_memory.json")
REFINE_MODE  = os.getenv("REFINE_MODE", "BASIC").upper()   # Optional, defaults to BASIC
SKILLPAY_HDR = "x-skillpay-auth"
LOG_LEVEL    = os.getenv("LOG_LEVEL", "INFO").upper()

# Storage limits
_MAX_TEXT       = 300    # Max chars for any single text value
_MAX_CTX_KEYS   = 8      # Max keys allowed in a context dict
_MAX_CTX_STRLEN = 200    # Max chars for any context string value

# Blocked context key patterns — prevent accidentally storing credentials
# 禁止的上下文键名模式，防止意外存储凭证或敏感数据
_BLOCKED_KEY_RE = re.compile(
    r"(token|key|secret|password|passwd|credential|auth|api.?key|bearer|"
    r"private|seed|salt|hash|ssn|credit|card|cvv|pin\b)",
    re.IGNORECASE,
)

# ─── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level   = getattr(logging, LOG_LEVEL, logging.INFO),
    format  = "%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt = "%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("refine")


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — INPUT SANITIZATION
#  输入清洗层：在任何数据写入磁盘前执行
# ══════════════════════════════════════════════════════════════════════════════

def _safe(text: str) -> str:
    """
    Truncate a string to _MAX_TEXT characters before storage.
    截断字符串至最大长度，防止大量内容写入磁盘。
    """
    s = str(text).strip()
    return (s[:_MAX_TEXT] + "…") if len(s) > _MAX_TEXT else s


def _sanitize_context(ctx: dict | None) -> dict:
    """
    Clean a caller-supplied context dict before writing to disk.
    在写入磁盘前清洗调用方提供的上下文字典。

    Rules applied (in order):
      1. Reject non-dict input — return empty dict.
      2. Limit to _MAX_CTX_KEYS entries — extras silently dropped.
      3. Block keys matching _BLOCKED_KEY_RE (token, key, secret, etc.)
         — replaced with a redaction notice.
      4. Flatten nested dicts/lists — replaced with a type notice.
      5. Truncate all string values to _MAX_CTX_STRLEN chars.
      6. Allow only str, int, float, bool scalar values; others replaced.

    This ensures that even if a caller accidentally passes sensitive data
    (prompts, API keys, PII), it cannot reach the JSON file.
    即使调用方误传敏感数据（提示词、API 密钥、个人信息），
    也无法写入 JSON 文件。

    Args:
        ctx: Arbitrary dict from the caller.

    Returns:
        A clean, safe dict suitable for persistent storage.
    """
    if not isinstance(ctx, dict):
        return {}

    clean: dict = {}
    blocked_count   = 0
    nested_count    = 0
    truncated_count = 0

    for k, v in list(ctx.items())[:_MAX_CTX_KEYS]:
        key = str(k)

        # Rule 3 — block sensitive key names
        # 规则 3：拦截敏感键名
        if _BLOCKED_KEY_RE.search(key):
            clean[key] = "[REDACTED — sensitive key name]"
            blocked_count += 1
            continue

        # Rule 4 — flatten nested structures
        # 规则 4：拒绝嵌套结构
        if isinstance(v, (dict, list)):
            clean[key] = f"[REMOVED — nested {type(v).__name__} not stored]"
            nested_count += 1
            continue

        # Rule 5 & 6 — scalar values only, strings truncated
        # 规则 5 & 6：仅允许标量值，字符串截断
        if isinstance(v, str):
            orig_len = len(v)
            v = v[:_MAX_CTX_STRLEN]
            if len(v) < orig_len:
                v += "…"
                truncated_count += 1
        elif isinstance(v, (int, float, bool)):
            pass   # Safe scalar — keep as-is / 安全标量，原样保留
        else:
            clean[key] = f"[REMOVED — unsupported type {type(v).__name__}]"
            continue

        clean[key] = v

    # Log a summary of sanitization actions (no values, only counts)
    # 仅记录清洗操作计数，不记录具体值
    if blocked_count or nested_count or truncated_count:
        log.debug(
            "Context sanitized: %d blocked key(s), %d nested removed, %d truncated.",
            blocked_count, nested_count, truncated_count,
        )

    return clean


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — PERSISTENCE
#  持久化层：本地原子写入，无网络调用
# ══════════════════════════════════════════════════════════════════════════════

def load_memory() -> dict:
    """
    Load memory from disk; return a fresh scaffold if missing or corrupt.
    从磁盘加载记忆；文件缺失或损坏时返回空白结构。
    """
    if not MEMORY_FILE.exists():
        log.info("No memory file — initialising fresh store.")
        return _empty_memory()
    try:
        data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        log.debug("Memory loaded: %d session(s).", len(data.get("sessions", [])))
        return data
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("Memory unreadable (%s) — starting clean.", exc)
        return _empty_memory()


def save_memory(data: dict) -> None:
    """
    Persist memory atomically via temp-file rename. No network calls.
    原子写入：先写临时文件再重命名。无网络调用。
    """
    tmp = MEMORY_FILE.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(MEMORY_FILE)
        log.debug("Memory saved → %s", MEMORY_FILE)
    except OSError as exc:
        log.error("Failed to save memory: %s", exc)
        raise


def _empty_memory() -> dict:
    return {
        "schema_version": "1.3",
        "created_at":     _ts(),
        "sessions":       [],
        "error_log":      [],
        "patches":        [],
        "stats": {
            "total_sessions":  0,
            "total_errors":    0,
            "patches_applied": 0,
        },
    }


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — PAYMENT VERIFICATION
#  支付验证：完全离线，hmac.compare_digest 防时序攻击
# ══════════════════════════════════════════════════════════════════════════════

def verify_payment(headers: dict) -> bool:
    """
    Verify SkillPay token via offline SHA-256 + constant-time comparison.
    离线 SHA-256 + 恒定时间比较验证令牌。原始令牌永不入日志或磁盘。

    Requires SKILLPAY_TOKEN_HASH env var set to SHA-256 hex of the token.
    """
    token = (headers or {}).get(SKILLPAY_HDR, "").strip()
    if not token:
        log.warning("PRO gate: '%s' header missing.", SKILLPAY_HDR)
        return False

    token_hash = hashlib.sha256(token.encode()).hexdigest()
    log.debug("PRO gate: hash prefix = %s…", token_hash[:8])   # 8 chars only

    expected = os.getenv("SKILLPAY_TOKEN_HASH", "")
    if not expected:
        log.error(
            "SKILLPAY_TOKEN_HASH not set. "
            "Export SHA-256 hex of your token before running in PRO mode."
        )
        return False

    # hmac.compare_digest — stdlib hmac module, constant-time, timing-attack resistant
    # 标准库 hmac 模块，恒定时间比较，防止时序攻击
    ok = hmac.compare_digest(token_hash.encode(), expected.encode())
    log.info("PRO gate: %s", "authorised ✓" if ok else "denied ✗")
    return ok


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — BASIC ENGINE (ClawHub)
#  基础引擎：反馈捕获、错误记录、会话历史
# ══════════════════════════════════════════════════════════════════════════════

class RefineBASIC:
    """
    REFINE Basic — ClawHub free tier.

    What is stored in refine_memory.json:
      ┌─────────────────────┬────────────────────────────────────────┐
      │ Field               │ Content                                │
      ├─────────────────────┼────────────────────────────────────────┤
      │ feedback text       │ Truncated to 300 chars                 │
      │ error type          │ Exception class name only              │
      │ error message       │ First line only, truncated 300 chars   │
      │ context dict        │ Sanitized: blocked keys → [REDACTED],  │
      │                     │ nested → [REMOVED], strings truncated  │
      │                     │ to 200 chars, max 8 keys               │
      │ stack traces        │ Never stored                           │
      └─────────────────────┴────────────────────────────────────────┘

    Safe usage:
      Pass short diagnostic labels as feedback (e.g. "verbosity-high").
      Pass only non-sensitive metadata as context (e.g. {"prompt_id": "p1"}).
      Do NOT pass raw prompts, API responses, credentials, or PII.
      The sanitizer will redact/remove suspicious content, but the best
      practice is to never send sensitive data in the first place.
    """

    def __init__(self) -> None:
        self.memory  = load_memory()
        self.session = self._new_session()
        log.info("REFINE BASIC ready — session %s", self.session["id"][:8])

    def capture_feedback(self, feedback: str, context: dict | None = None) -> dict:
        """
        Record a short diagnostic label. Context is sanitized before storage.
        记录简短诊断标签。context 在写入前经过完整清洗。

        Args:
            feedback: Short label, e.g. "verbosity-high". Not raw prompt text.
            context:  Optional metadata. Sanitized automatically:
                      · Sensitive keys (token, key, secret…) → [REDACTED]
                      · Nested dicts/lists → [REMOVED]
                      · Strings truncated to 200 chars
                      · Max 8 keys stored
        """
        record = {
            "id":        _uid(),
            "timestamp": _ts(),
            "feedback":  _safe(feedback),
            "context":   _sanitize_context(context),   # ← sanitized before storage
        }
        self.session["feedback"].append(record)
        log.info("Feedback captured [%s]", record["id"][:8])
        return record

    def log_error(self, error: Exception, context: dict | None = None) -> dict:
        """
        Record error type + first message line. Context sanitized. No traceback.
        记录异常类型名和消息首行。context 经清洗。不存储堆栈跟踪。

        Args:
            error:   The caught exception.
            context: Optional metadata. Sanitized automatically (same rules
                     as capture_feedback context).

        Note:
            Full stack traces are intentionally not stored to prevent
            sensitive prompt fragments from reaching the JSON file.
            故意不存储完整堆栈跟踪，防止敏感内容写入磁盘。
        """
        first_line = str(error).split("\n")[0]   # First line only — no traceback
        record = {
            "id":        _uid(),
            "timestamp": _ts(),
            "type":      type(error).__name__,
            "message":   _safe(first_line),
            "context":   _sanitize_context(context),   # ← sanitized before storage
        }
        self.session["errors"].append(record)
        self.memory["error_log"].append(record)
        self.memory["stats"]["total_errors"] += 1
        log.error("Error [%s]: %s — %s", record["id"][:8], record["type"], record["message"])
        return record

    def get_history(self, limit: int = 10) -> list[dict]:
        """
        Return N most recent session count summaries (no raw text).
        返回最近 N 次会话统计摘要（不含原始内容）。
        """
        sessions = self.memory.get("sessions", [])
        return sessions[-limit:][::-1]

    def close(self) -> None:
        """Finalise session; write to refine_memory.json (local disk only)."""
        self.session["closed_at"] = _ts()
        self.session["summary"] = (
            f"{len(self.session['feedback'])} feedback, "
            f"{len(self.session['errors'])} error(s)."
        )
        self.memory["sessions"].append(self.session)
        self.memory["stats"]["total_sessions"] += 1
        save_memory(self.memory)
        log.info("Session %s closed.", self.session["id"][:8])

    def _new_session(self) -> dict:
        return {
            "id":        _uid(),
            "opened_at": _ts(),
            "closed_at": None,
            "summary":   "",
            "feedback":  [],
            "errors":    [],
        }


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — PRO ENGINE (SkillPay)
#  专业引擎：失败聚类分析 + 补丁合成
# ══════════════════════════════════════════════════════════════════════════════

class RefinePRO(RefineBASIC):
    """
    REFINE Pro — SkillPay paid tier. Extends RefineBASIC.

    Adds local failure analysis and patch synthesis.
    All operations are local — no outbound network calls.
    全部操作在本地完成，不发起任何外部网络请求。

    Requires:
      · REFINE_MODE=PRO
      · SKILLPAY_TOKEN_HASH env var (SHA-256 hex of your token)
      · x-skillpay-auth header passed at runtime
    """

    def __init__(self, auth_headers: dict) -> None:
        if not verify_payment(auth_headers):
            raise PermissionError(
                "REFINE PRO: invalid or missing SkillPay token. "
                "Set SKILLPAY_TOKEN_HASH and pass the token via x-skillpay-auth header."
            )
        super().__init__()
        log.info("REFINE PRO ready — patch synthesis enabled.")

    def analyse_failures(self) -> dict:
        """
        Cluster stored errors by type; rank by frequency.
        按异常类型聚类本地错误日志，按频率排序。
        Reads only from local memory — no network calls.
        """
        error_log = self.memory.get("error_log", [])
        if not error_log:
            return {"clusters": [], "analysed_at": _ts(), "total": 0, "types": 0}

        clusters: dict[str, dict] = {}
        for err in error_log:
            t = err.get("type", "Unknown")
            if t not in clusters:
                clusters[t] = {"type": t, "count": 0, "samples": []}
            clusters[t]["count"] += 1
            if len(clusters[t]["samples"]) < 2:
                clusters[t]["samples"].append(_safe(err.get("message", "")))

        ranked = sorted(clusters.values(), key=lambda x: x["count"], reverse=True)
        log.info("Analysis: %d error(s), %d type(s).", len(error_log), len(ranked))
        return {
            "total":       len(error_log),
            "types":       len(ranked),
            "clusters":    ranked,
            "analysed_at": _ts(),
        }

    def synthesise_patch(self, analysis: dict) -> dict | None:
        """
        Generate a System Prompt Patch directive string from failure analysis.
        根据分析结果生成系统提示补丁字符串（本地生成，无外部调用）。

        Usage: prepend patch["patch_body"] to the next session's system prompt.
        用法：将 patch_body 前置到下次会话的系统提示词中。
        """
        clusters = analysis.get("clusters", [])
        if not clusters:
            log.info("No clusters — no patch needed.")
            return None

        lines: list[str] = []
        for c in clusters[:5]:
            sample = c["samples"][0] if c["samples"] else "(no detail)"
            lines.append(
                f"[REFINE·PATCH] Avoid `{c['type']}` ({c['count']}x). "
                f"Last trigger: {sample[:100]}"
            )

        patch = {
            "id":           _uid(),
            "generated_at": _ts(),
            "version":      f"patch-{len(self.memory['patches']) + 1:04d}",
            "stats":        {"errors": analysis.get("total", 0), "types": analysis.get("types", 0)},
            "patch_body":   "\n".join(lines),
            "applied":      False,
        }
        self.memory["patches"].append(patch)
        self.memory["stats"]["patches_applied"] += 1
        save_memory(self.memory)
        log.info("Patch %s synthesised.", patch["version"])
        return patch

    def evolve(self) -> dict:
        """
        Run full cycle: analyse local errors → synthesise patch → persist.
        完整流程：分析本地错误 → 合成补丁 → 写入磁盘。
        Call before close() at end of each PRO session.
        """
        log.info("── Patch synthesis starting ──")
        analysis = self.analyse_failures()
        patch    = self.synthesise_patch(analysis)
        log.info("── Patch synthesis complete ──")
        return {
            "evolved_at": _ts(),
            "analysis":   analysis,
            "patch":      patch,
            "message": (
                f"{patch['version']} ready — prepend patch_body to next system prompt."
                if patch else "No patch needed — no failures recorded."
            ),
        }

    def get_latest_patch(self) -> dict | None:
        """Return the most recent patch, or None. / 返回最新补丁（如有）。"""
        patches = self.memory.get("patches", [])
        return patches[-1] if patches else None


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — FACTORY
#  工厂函数：根据 REFINE_MODE 路由至正确引擎
# ══════════════════════════════════════════════════════════════════════════════

def build_engine(auth_headers: dict | None = None) -> RefineBASIC | RefinePRO:
    """
    Instantiate the correct engine from REFINE_MODE (optional, default BASIC).
    根据可选环境变量 REFINE_MODE 实例化引擎（默认 BASIC）。

    Raises:
        PermissionError — PRO mode with invalid/missing token.
        ValueError      — Unrecognised REFINE_MODE value.
    """
    if REFINE_MODE == "BASIC":
        log.info("Mode: BASIC (ClawHub)")
        return RefineBASIC()
    elif REFINE_MODE == "PRO":
        log.info("Mode: PRO (SkillPay)")
        return RefinePRO(auth_headers or {})
    else:
        raise ValueError(
            f"Unrecognised REFINE_MODE='{REFINE_MODE}'. Use 'BASIC' or 'PRO'."
        )


# ── Utilities ─────────────────────────────────────────────────────────────────
def _uid() -> str:
    return str(uuid.uuid4())

def _ts() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n╔══ REFINE v1.3 Demo ═══════════════════════════╗")
    print(f"   Mode: {REFINE_MODE}")
    print( "   All context dicts are sanitized before storage.\n")

    auth_token   = os.getenv("SKILLPAY_AUTH_TOKEN", "")
    demo_headers = {SKILLPAY_HDR: auth_token} if auth_token else {}

    try:
        engine = build_engine(auth_headers=demo_headers)

        # Safe usage: short labels + non-sensitive metadata only
        engine.capture_feedback(
            "verbosity-high",
            context={"prompt_id": "p001", "model": "claude-3"}
        )

        # Demonstrate sanitizer — this key will be redacted
        engine.capture_feedback(
            "test-sanitize",
            context={"prompt_id": "p002", "api_key": "sk-should-be-redacted"}
        )

        try:
            raise ConnectionError("Upstream timeout after 30s")
        except ConnectionError as exc:
            engine.log_error(exc, {"endpoint": "/v1/completions", "attempt": 3})

        if isinstance(engine, RefinePRO):
            report = engine.evolve()
            print("── Patch Report ─────────────────────────────")
            print(json.dumps(report, indent=2))

        print("\n── History (last 3) ─────────────────────────")
        print(json.dumps(engine.get_history(3), indent=2))

        engine.close()
        print("\n╚══ Done. Data written to refine_memory.json ╝\n")
        print("Note: check refine_memory.json — api_key field")
        print("should show [REDACTED — sensitive key name]\n")

    except PermissionError as exc:
        print(f"\n🔒 {exc}\n")
    except ValueError as exc:
        print(f"\n⚠  {exc}\n")
