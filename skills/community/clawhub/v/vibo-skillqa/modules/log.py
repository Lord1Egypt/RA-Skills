"""Log audit module: logging presence, rotation, error quality, secret leaks.

Secret scanning only inspects *contents* (script outputs, log files and
skill text files) — never file names or paths — so a path like
/home/user/skillqa/fixtures/good_skill/script.py can never be mistaken for
a secret.  Exact fake-token values injected by the sandbox are ignored.
"""

import re
from pathlib import Path

from modules.sandbox import FAKE_VALUES

SECRET_PATTERNS = [
    (re.compile(r"Bearer\s+\S{8,}"), "bearer_token"),
    (re.compile(r"sk-[A-Za-z0-9]{16,}"), "sk_token"),
    (re.compile(r"(?i)(token|api[_-]?key|key|password|passwd|secret|auth|credential)"
                r"\s*[=:]\s*(?![A-Za-z_]\w*(?:\.|\())"
                r"\S{8,}"), "assignment"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "aws_key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private_key"),
    (re.compile(r"(?i)ghp_[A-Za-z0-9]{20,}"), "github_token"),
    (re.compile(r"(?i)xox[baprs]-[A-Za-z0-9-]{10,}"), "slack_token"),
]

PLACEHOLDER_VALUE_RE = re.compile(
    r"^(user[-_]?(pass|password|passphrase)|password|pwd|example|dummy|test|your[-_][a-z]+|change[-_]?me|123456|qwerty|demo|fake|placeholder|redacted|sample|xxx+|passphrase)[\"'<>]*$",
    re.I)


def _is_template(snippet):
    """True when the matched value is an env-var template / config placeholder
    ($UPSTREAM_API_KEY, ${PRIVACY_ADMIN_TOKEN:-}, Bearer {UPSTREAM_KEY}),
    a doc example (<token>, sk-123...cdef), or a backtick-wrapped example —
    code/docs, not a leak."""
    if "$" in snippet or "{" in snippet or "}" in snippet:
        return True
    if "..." in snippet or "<token>" in snippet.lower() or "<ключ>" in snippet.lower():
        return True
    if "`" in snippet:
        return True
    return False


def _is_placeholder_assignment(name, snippet):
    """True for assignment hits whose value is an obvious placeholder
    (password="user-pass", API_KEY="sk-you...-key") or an env template
    ($UPSTREAM_API_KEY, ${PRIVACY_ADMIN_TOKEN:-}) — not a real leak."""
    if name != "assignment":
        return False
    raw = snippet.split("=", 1)[-1].split(":", 1)[-1].strip()
    if "<" in raw or "[" in raw or "(" in raw:
        return True  # placeholder <...>, dict-access d["key"], call f(...) — not a literal secret
    if raw.lower().startswith(("http://", "https://")):
        return True  # URL after key:/key= is a link, not a secret value
    val = raw.strip("\"'(),;<> ")
    if not val:
        return True
    # bare lowercase identifier (agent_key, api_key) is a variable name, not a value
    if re.match(r"^[a-z_][a-z0-9_]*$", val):
        return True
    # env-var / constant name (L3_SECRET, UPSTREAM_API_KEY) is not a value
    if re.match(r"^[A-Z][A-Z0-9_]{2,}$", val):
        return True
    # env-var template / placeholder: $VAR, ${VAR:-}, {UPSTREAM_KEY}, sk-you...-key
    if any(c in val for c in ("$", "{", "}")):
        return True
    if re.search(r"sk-[a-z]+\.\.\.[a-z]+$", val, re.I):
        return True
    if re.match(r"sk-your[a-z-]*", val, re.I):
        return True
    return bool(PLACEHOLDER_VALUE_RE.match(val))


# --- env-file secret scanning (ТЗ 20.08: .env* coverage + classification) ---
ENV_FILE_RE = re.compile(
    r"(?:^|/)\.[^/]*env(?:\.|$)"                                   # .env, .env.production, .env.local
    r"|(?:^|/)[^/]*env[^/]*\.(?:prod|production|local|test|stage)$",  # *env*.prod / roomtalk.env.production
    re.I)

SEVERE_KEY_RE = re.compile(
    r"(?:ENCRYPTION|PASSWORD|PASSWD|API[_-]?KEY|TOKEN|SECRET|PEPPER|"
    r"AUTH[_-]?TOKEN|PRIVATE[_-]?KEY|SID|BEARER)"
    r"|(?:password|passwd|secret|token|api[_-]?key|auth)",
    re.I)

DEV_VALUE_RE = re.compile(
    r"^(?:test|changeme|change[-_]?me|placeholder|your[-_][a-z0-9_-]*|example|"
    r"dummy|fake|sample|xxx+|\*+|password|passwd|pwd|secret|token|key|none|"
    r"null|nil|true|false|0|1|local|dev|development|staging|demo)$",
    re.I)

ENV_LINE_RE = re.compile(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")
TOKEN_LIKE_RE = re.compile(r"^(?:sk-|AKIA|ghp_|xox[baprs]-|eyJ[A-Za-z0-9_-]{10,})")


def _mask(value):
    """first4***last3 mask (ТЗ 20.08) — never expose full values in reports."""
    v = (value or "").strip()
    if len(v) <= 7:
        return "***"
    return v[:4] + "***" + v[-3:]


def _mask_snippet(s):
    """Mask the value part of a KEY=value / KEY: value / Bearer <token> snippet."""
    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*\s*[=:])\s*(\S+)$", s)
    if m:
        return m.group(1) + _mask(m.group(2))
    m = re.match(r"^(Bearer\s+)(\S+)$", s, re.I)
    if m:
        return m.group(1) + _mask(m.group(2))
    return _mask(s)


def classify_env_secret(name, value):
    """Classify one KEY=value pair from an env file.

    Returns one of:
      severe — production-looking secret (real token / critical key name)
      dev    — obvious dev/test placeholder or empty value
      unknown— cannot tell (warn: check manually)
    """
    val = (value or "").strip().strip("'\"")
    if not val or DEV_VALUE_RE.match(val) or _is_template(val):
        return "dev"
    if TOKEN_LIKE_RE.search(val):
        return "severe"
    if SEVERE_KEY_RE.search(name):
        return "severe"
    return "unknown"


def scan_env_files(env_texts):
    """Scan (label, text) env-file pairs. Returns {severe, dev, unknown} lists
    of (key, masked_value, label). Full values never leave this function."""
    out = {"severe": [], "dev": [], "unknown": []}
    for label, text in env_texts:
        for line in text.splitlines():
            m = ENV_LINE_RE.match(line.strip())
            if not m:
                continue
            name, value = m.group(1), m.group(2)
            cls = classify_env_secret(name, value)
            out[cls].append((name, _mask(value), label))
    return out


TRACEBACK_FILE_LINE = re.compile(r'File "[^"]+", line \d+')
BARE_ERROR = re.compile(r"\b[A-Za-z]\w*(?:Error|Exception)\b")
APPEND_OPEN = re.compile(r'open\s*\([^)]*["\']a[+"\'"]')
ROTATION_HANDLER = re.compile(r"RotatingFileHandler|TimedRotatingFileHandler")
LOGGING_USE = re.compile(r"(?m)^\s*(import logging|from logging)|"
                         r"logging\.|getLogger|logger\s*=")
MAX_TEXT_SIZE = 1024 * 1024


def _check(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def _module_status(checks):
    if any(c["status"] == "fail" for c in checks):
        return "fail"
    if any(c["status"] == "warn" for c in checks):
        return "warn"
    return "pass"


def _is_text_file(path, limit=MAX_TEXT_SIZE):
    try:
        if path.stat().st_size > limit:
            return False
        with open(path, "rb") as fh:
            head = fh.read(64)
        if b"\x00" in head:
            return False  # binary blob (ELF/compiled) — control/NUL bytes
        head.decode("utf-8")
        return True
    except Exception:
        return False


def scan_secrets(texts, fake_values=None):
    """Scan (label, text) pairs for secret-like patterns.

    Returns up to 8 hits as (pattern_name, snippet, label).
    Matches containing an exact fake-token value are ignored, as are
    obvious placeholder values (password="user-pass", key="example").
    """
    fake_values = fake_values or FAKE_VALUES
    hits = []
    for label, text in texts:
        for pat, name in SECRET_PATTERNS:
            for m in pat.finditer(text):
                snippet = m.group(0)
                if any(fv in snippet for fv in fake_values):
                    continue
                if _is_template(snippet):
                    continue
                if _is_placeholder_assignment(name, snippet):
                    continue
                disp = re.sub(r"\s+", " ", snippet).strip()
                disp = _mask_snippet(disp)   # ТЗ 20.08: never expose full values
                if len(disp) > 60:
                    disp = disp[:57] + "..."
                hits.append((name, disp, label))
                if len(hits) >= 8:
                    return hits
    return hits


class LogAudit:
    name = "log"
    title = {"ru": "Аудит логов", "en": "Log audit"}

    def run(self, ctx):
        t = ctx.t
        checks = []
        skill_dir = Path(ctx.sandbox.skill_dir)

        # ---- collect texts: run outputs, skill text files, *.log files ----
        run_texts = []
        for i, r in enumerate(ctx.run_outputs):
            if r["stdout"]:
                run_texts.append((f"stdout[{i}]", r["stdout"]))
            if r["stderr"]:
                run_texts.append((f"stderr[{i}]", r["stderr"]))

        file_texts = []
        env_texts = []
        log_files = []
        for p in sorted(skill_dir.rglob("*")):
            if not p.is_file():
                continue
            if ENV_FILE_RE.search(p.name):
                if _is_text_file(p):
                    try:
                        env_texts.append(
                            (str(p.relative_to(skill_dir)),
                             p.read_text(encoding="utf-8", errors="replace")))
                    except OSError:
                        pass
                continue
            if p.suffix.lower() == ".log":
                log_files.append(p)
            if _is_text_file(p):
                try:
                    file_texts.append(
                        (str(p.relative_to(skill_dir)),
                         p.read_text(encoding="utf-8", errors="replace")))
                except OSError:
                    pass
        # logs written by scripts anywhere inside the sandbox temp root
        for p in sorted(ctx.sandbox.tmp_root.rglob("*.log")):
            if p.resolve().is_relative_to(skill_dir.resolve()):
                continue
            if _is_text_file(p):
                try:
                    file_texts.append(
                        (f"log:{p.name}", p.read_text(encoding="utf-8", errors="replace")))
                except OSError:
                    pass

        code_files = [p for p in skill_dir.rglob("*.py") if p.is_file()]

        # 1. logging present
        logging_used = any(
            LOGGING_USE.search(p.read_text(errors="replace"))
            for p in code_files if _is_text_file(p)
        )
        if logging_used or log_files:
            checks.append(_check("logging_present", "pass",
                                 t("check.logging_present.yes")))
        else:
            checks.append(_check("logging_present", "pass",
                                 t("check.logging_present.no")))

        # 2. log rotation (append without rotation -> warn)
        append_no_rotation = []
        for p in code_files:
            if not _is_text_file(p):
                continue
            src = p.read_text(errors="replace")
            if APPEND_OPEN.search(src) and not ROTATION_HANDLER.search(src):
                append_no_rotation.append(p.name)
        if append_no_rotation:
            checks.append(_check("log_rotation", "warn",
                                 t("check.log_rotation.warn",
                                   files=", ".join(append_no_rotation[:5]))))
        else:
            checks.append(_check("log_rotation", "pass",
                                 t("check.log_rotation.ok")))

        # 3. error quality: tracebacks must carry file:line
        err_texts = [txt for _, txt in run_texts]
        err_texts += [txt for lbl, txt in file_texts
                      if lbl.startswith("log:")
                      or (("Traceback" in txt)
                          and not lbl.endswith((".md", ".rst")))]
        tb_texts = [txt for txt in err_texts if "Traceback" in txt]
        # skip binary blobs (compiled modules may contain the string)
        tb_texts = [txt for txt in tb_texts
                    if "\x00" not in txt[:256] and not txt.startswith("\x7f")]
        if tb_texts:
            if all(TRACEBACK_FILE_LINE.search(txt) for txt in tb_texts):
                checks.append(_check("error_quality", "pass",
                                     t("check.error_quality.ok")))
            else:
                checks.append(_check("error_quality", "fail",
                                     t("check.error_quality.fail")))
        else:
            bare = [txt for txt in err_texts
                    if BARE_ERROR.search(txt)
                    and not re.search(r"usage:", txt, re.I)
                    and not re.search(r"licen[cs]e|not found|denied|missing|не найден|лиценз|permission", txt, re.I)]
            if bare:
                checks.append(_check("error_quality", "warn",
                                     t("check.error_quality.warn")))
            else:
                checks.append(_check("error_quality", "pass",
                                     t("check.error_quality.none")))

        # 4a. env-file secrets (.env*) — classified, masked (ТЗ 20.08)
        env_findings = scan_env_files(env_texts)
        if env_texts:
            if env_findings["severe"]:
                items = ", ".join(
                    f"{k}={masked}" for k, masked, _ in env_findings["severe"][:5])
                checks.append(_check("env_secrets", "fail",
                                     t("check.env_secrets.fail", items=items)))
            elif env_findings["unknown"]:
                items = ", ".join(
                    f"{k}={masked}" for k, masked, _ in env_findings["unknown"][:5])
                checks.append(_check("env_secrets", "warn",
                                     t("check.env_secrets.unknown", items=items)))
            elif env_findings["dev"]:
                checks.append(_check("env_secrets", "warn",
                                     t("check.env_secrets.dev")))
            else:
                checks.append(_check("env_secrets", "pass",
                                     t("check.env_secrets.ok")))
        else:
            checks.append(_check("env_secrets", "pass",
                                 t("check.env_secrets.ok")))

        # 4b. hardcoded secrets in code/logs (separate signal — ТЗ 20.08)
        all_texts = run_texts + file_texts
        hits = scan_secrets(all_texts)
        if hits:
            items = ", ".join(f"{name}:{disp}" for name, disp, _ in hits[:5])
            # internal skills legitimately document example tokens — warn only
            _internal = False
            try:
                _md = Path(ctx.skill_path) / "SKILL.md"
                _head = _md.read_text(encoding="utf-8", errors="replace").split("---", 2)
                _internal = len(_head) >= 2 and re.search(r"(?m)^internal:\s*true", _head[1]) is not None
            except Exception:
                pass
            checks.append(_check("secret_leak", "warn" if _internal else "fail",
                                 t("check.secret_leak.fail", items=items)))
        else:
            checks.append(_check("secret_leak", "pass",
                                 t("check.secret_leak.ok")))

        # 5. log growth: file logs without rotation / size limit -> warn
        if log_files and not any(
                ROTATION_HANDLER.search(p.read_text(errors="replace"))
                for p in code_files if _is_text_file(p)):
            checks.append(_check("log_growth", "warn",
                                 t("check.log_growth.warn",
                                   files=", ".join(p.name for p in log_files[:5]))))
        else:
            checks.append(_check("log_growth", "pass",
                                 t("check.log_growth.ok")))

        status = _module_status(checks)
        n_fail = sum(1 for c in checks if c["status"] == "fail")
        n_warn = sum(1 for c in checks if c["status"] == "warn")
        details = t("module.summary", total=len(checks), fail=n_fail, warn=n_warn)
        return {"module": self.name, "status": status, "checks": checks,
                "details": details}
