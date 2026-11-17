#!/usr/bin/env python3
"""
safeclaw.py — Token Safety Checker (a.k.a. tightlip) for OpenClaw and Claude Code

Subcommands:

  scan            Detect plaintext secrets in openclaw.json.
                  Returns field paths, lengths, risk levels and fingerprints — never secret values.
                  --deep   also scans git history for past exposures.
                  --memory also scans agent memory + session transcripts (see `memory`).

  memory          Scan agent memory for leaked secrets:
                    long-term : OpenClaw MEMORY.md / USER.md / DREAMS.md ..., Claude Code CLAUDE.md,
                                CLAUDE.local.md, .claude/rules, auto memory (~/.claude/projects/*/memory)
                    short-term: OpenClaw daily notes (memory/YYYY-MM-DD.md), Claude Code prompt history
                    transcript: OpenClaw sessions (*.jsonl, *.sqlite), Claude Code transcripts (*.jsonl)
                    log       : OpenClaw logs (e.g. config-audit.jsonl records `openclaw config set` argv)
                  Read-only. Reports file + line + detector + fingerprint, never the value.

  migrate         Migrate plaintext secrets in openclaw.json to env vars + SecretRef.
                  Reads secret values directly from the config file — never via CLI args.
                  Secrets go to a private secrets file (mode 600); the shell profile only gets
                  a line that loads it. A read-only verify follows a successful migration.

  verify          Post-migration health check (plaintext left, permissions, env vars, backups).

  install-guard   Install leak prevention:
                    Claude Code: PreToolUse hook that blocks Write/Edit of secrets into memory files
                    OpenClaw   : git pre-commit hook in the workspace repo that blocks committing secrets
  uninstall-guard Remove what install-guard added.

  guard-hook      (internal) Claude Code PreToolUse hook entry point — reads hook JSON on stdin.
  guard-git       (internal) git pre-commit entry point — scans staged files.

Usage:
  python3 safeclaw.py scan    [--config PATH] [--deep] [--memory]
  python3 safeclaw.py memory  [--platform auto|openclaw|claude|all] [--project DIR] [--no-transcripts]
  python3 safeclaw.py migrate --findings '[...]' [--config PATH] [--secrets-file PATH] [--profile PATH | --no-profile] [--dry-run]
  python3 safeclaw.py migrate --restore [--backup PATH] | --list-backups
  python3 safeclaw.py verify  [--config PATH] [--clean-backup]
  python3 safeclaw.py install-guard   --platform openclaw|claude|all [--scope memory|all]
  python3 safeclaw.py uninstall-guard [--platform auto|openclaw|claude|all]

Exit codes:
  scan:    0 = no findings, 1 = findings present, 2 = config not found (without --memory)
  memory:  0 = clean, 1 = leaked secrets found
  migrate: 0 = success, 1 = error
  verify:  0 = all clear, 1 = issues found
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import os
import re
import shlex
import shutil
import sqlite3
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION = "3.0.2"

# -- Constants ---

SENSITIVE_KEYS = {"token", "apikey", "key", "password", "secret", "credential",
                  "authorization", "bearer"}
MIN_SECRET_LEN = 16

ENV_HINTS = {
    "gateway.auth.token":             "OPENCLAW_GATEWAY_TOKEN",
    "gateway.remote.token":           "OPENCLAW_GATEWAY_TOKEN",
    "channels.discord.token":         "OPENCLAW_DISCORD_TOKEN",
    "channels.telegram.token":        "OPENCLAW_TELEGRAM_TOKEN",
    "channels.telegram.botToken":     "OPENCLAW_TELEGRAM_TOKEN",
    "channels.whatsapp.token":        "OPENCLAW_WHATSAPP_TOKEN",
    "channels.slack.botToken":        "OPENCLAW_SLACK_BOT_TOKEN",
    "channels.slack.appToken":        "OPENCLAW_SLACK_APP_TOKEN",
    "channels.slack.signingSecret":   "OPENCLAW_SLACK_SIGNING_SECRET",
    "tools.web.search.gemini.apiKey": "OPENCLAW_GEMINI_API_KEY",
    "tools.web.search.openai.apiKey": "OPENCLAW_OPENAI_API_KEY",
    "tools.web.search.brave.apiKey":  "OPENCLAW_BRAVE_API_KEY",
}

# Paths that directly control the agent or expose it to the internet = HIGH
HIGH_RISK_PATHS = {
    "channels.discord.token",
    "channels.telegram.token",
    "channels.whatsapp.token",
    "gateway.auth.token",
    "gateway.remote.token",
}
# API keys for third-party services = MEDIUM
MEDIUM_RISK_PATHS = {
    "tools.web.search.openai.apiKey",
    "tools.web.search.gemini.apiKey",
    "tools.web.search.brave.apiKey",
}

# Keys that look sensitive but hold a pointer, not a secret (e.g. channels.telegram.tokenFile)
POINTER_KEY_SUFFIXES = ("file", "path", "dir", "env", "url", "name", "id", "ref")

ENV_VAR_RE = re.compile(r'^[A-Z_][A-Z0-9_]*$')
ENV_TEMPLATE_RE = re.compile(r'^\$\{?[A-Za-z_][A-Za-z0-9_]*\}?$')
PATH_TOKEN_RE = re.compile(r'([^.\[\]]+)|\[(\d+)\]')

SHELL_PROFILES = {
    "zsh":  ["~/.zshrc", "~/.zprofile"],
    "bash": ["~/.bashrc", "~/.bash_profile", "~/.profile"],
    "fish": ["~/.config/fish/config.fish"],
    "dash": ["~/.profile"],
    "sh":   ["~/.profile"],
}

RISK_ICON = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
RISK_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

# -- Value-based secret detectors (used for memory, transcripts, guard, config) ─
# (name, regex, risk, capture group holding the secret)
DETECTORS = [
    ("private-key",        r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----", "HIGH", 0),
    ("anthropic-api-key",  r"\bsk-ant-[A-Za-z0-9_\-]{20,}", "HIGH", 0),
    ("openai-api-key",     r"\bsk-(?:proj-|svcacct-|admin-)?[A-Za-z0-9_\-]{20,}", "HIGH", 0),
    ("github-token",       r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})", "HIGH", 0),
    ("slack-token",        r"\bxox[abposr]-[A-Za-z0-9\-]{10,}", "HIGH", 0),
    ("aws-access-key-id",  r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b", "HIGH", 0),
    ("stripe-live-key",    r"\b(?:sk|rk)_live_[A-Za-z0-9]{20,}", "HIGH", 0),
    ("discord-bot-token",  r"\b[MNO][A-Za-z0-9_\-]{23,27}\.[A-Za-z0-9_\-]{6}\.[A-Za-z0-9_\-]{27,}", "HIGH", 0),
    ("telegram-bot-token", r"\b\d{8,10}:AA[A-Za-z0-9_\-]{33}\b", "HIGH", 0),
    ("google-api-key",     r"\bAIza[0-9A-Za-z_\-]{35}", "MEDIUM", 0),
    ("huggingface-token",  r"\bhf_[A-Za-z0-9]{30,}", "MEDIUM", 0),
    ("jwt",                r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}", "MEDIUM", 0),
    ("bearer-token",       r"(?i)\bbearer\s+([A-Za-z0-9._~+/\-]{20,}=*)", "MEDIUM", 1),
    ("url-credentials",    r"\b[a-zA-Z][a-zA-Z0-9+.\-]*://[^\s:/@'\"]+:([^\s@/'\"]{6,})@", "MEDIUM", 1),
    ("generic-secret",     r"(?i)\b(?:api[_\-]?key|apikey|secret|token|passw(?:or)?d|pwd|access[_\-]?key|"
                           r"client[_\-]?secret)\b[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_\-./+=~]{16,})", "LOW", 1),
]
_COMPILED = [(n, re.compile(rx), risk, g) for n, rx, risk, g in DETECTORS]
PROVIDER_DETECTORS = {n for n, _, _, _ in DETECTORS} - {"generic-secret", "bearer-token", "url-credentials"}

PLACEHOLDER_HINTS = ("example", "your", "xxxx", "placeholder", "redacted", "changeme",
                     "dummy", "sample", "<", ">", "***", "…", "${", "{{")

# Plain navigation text, no URLs: the script never contacts or names a remote host.
ROTATE_HINTS = {
    "anthropic-api-key":  "Anthropic Console → Settings → API keys: revoke it and create a new one",
    "openai-api-key":     "OpenAI platform → API keys: revoke it and create a new one",
    "github-token":       "GitHub → Settings → Developer settings → Tokens: revoke it",
    "slack-token":        "Rotate in your Slack app settings (OAuth & Permissions)",
    "aws-access-key-id":  "Deactivate + delete the access key in AWS IAM",
    "stripe-live-key":    "Roll the key in the Stripe dashboard (Developers → API keys)",
    "discord-bot-token":  "Discord Developer Portal → your app → Bot → Reset Token",
    "telegram-bot-token": "Message @BotFather → /revoke",
    "google-api-key":     "Regenerate in Google Cloud Console → APIs & Services → Credentials",
    "huggingface-token":  "Hugging Face → Settings → Tokens: invalidate it",
    "private-key":        "Generate a new key pair and remove the old public key everywhere it is trusted",
}
ROTATE_DEFAULT = "Rotate this credential at its provider — it has already been sent to a model provider"

# Memory / instruction file names the guard protects
MEMORY_FILENAMES = {"CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", "MEMORY.md", "memory.md", "USER.md",
                    "SOUL.md", "DREAMS.md", "TOOLS.md", "IDENTITY.md", "HEARTBEAT.md", "BOOT.md",
                    "BOOTSTRAP.md"}
OPENCLAW_LONG_TERM = ["MEMORY.md", "memory.md", "USER.md", "DREAMS.md", "SOUL.md", "IDENTITY.md",
                      "AGENTS.md", "TOOLS.md", "HEARTBEAT.md", "BOOT.md", "BOOTSTRAP.md"]
TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".log", ".yaml", ".yml"}

GUARD_MARKER = "token-safety-guard"

# -- Generic helpers ---

def home() -> Path:
    return Path.home()


def tilde(p) -> str:
    """Shorten a path under $HOME to ~/... for compact, privacy-friendly output."""
    s = str(p)
    h = str(home())
    return "~" + s[len(h):] if h and s.startswith(h + os.sep) else s


def fingerprint(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8", "surrogatepass")).hexdigest()[:8]


def entropy(s: str) -> float:
    if not s:
        return 0.0
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    return -sum(c / len(s) * math.log2(c / len(s)) for c in counts.values())


def is_placeholder(value: str) -> bool:
    low = value.lower()
    if any(h in low for h in PLACEHOLDER_HINTS):
        return True
    return len(set(value)) < 6


def mode_of(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


def is_private(path: Path) -> bool:
    """True when neither group nor others have any permission (e.g. 600 / 400 / 700)."""
    return (mode_of(path) & 0o077) == 0


def now_stamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def atomic_write_bytes(path: Path, data: bytes, mode: int = 0o600):
    """Write via an exclusive, private (0600) temp file in the same directory, then rename into place."""
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def atomic_write_text(path: Path, text: str, mode: int | None = None):
    atomic_write_bytes(path, text.encode("utf-8"), 0o600 if mode is None else mode)


def unique_path(p: Path) -> Path:
    if not p.exists():
        return p
    n = 1
    while p.with_name(f"{p.name}-{n}").exists():
        n += 1
    return p.with_name(f"{p.name}-{n}")


def private_copy(src: Path, dst: Path):
    """Copy src to a new file dst that is created exclusively with mode 0600 (never readable by others)."""
    fd = os.open(str(dst), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(src.read_bytes())

# -- Secret detection ---

def detect_secrets(text: str, known: dict | None = None) -> list:
    """
    Find secrets in free text. Returns [{detector, risk, value, start, end, live_match}].
    `value` is only for internal use (fingerprinting / matching) — callers must never print it.
    `known` maps exact live secret values → label (e.g. config path) for "live secret" matching.
    """
    hits = []
    for name, rx, risk, group in _COMPILED:
        for m in rx.finditer(text):
            value = m.group(group)
            if not value:
                continue
            if name in ("generic-secret", "bearer-token", "url-credentials"):
                if is_placeholder(value) or ENV_TEMPLATE_RE.match(value):
                    continue
            if name == "generic-secret" and (entropy(value) < 3.5 or not re.search(r"\d", value)):
                continue
            if name in ("openai-api-key",) and is_placeholder(value):
                continue
            hits.append({"detector": name, "risk": risk, "value": value,
                         "start": m.start(group), "end": m.end(group), "live_match": None})
    if known:
        for value, label in known.items():
            start = text.find(value)
            while start != -1:
                hits.append({"detector": "live-secret", "risk": "HIGH", "value": value,
                             "start": start, "end": start + len(value), "live_match": label})
                start = text.find(value, start + 1)

    # Resolve overlaps: live matches first, then provider detectors in declared order, then generic
    # detector_hint keeps the provider name (e.g. discord-bot-token) when a live match wins the overlap
    order = {n: i for i, (n, _, _, _) in enumerate(DETECTORS)}
    hits.sort(key=lambda h: (0 if h["detector"] == "live-secret" else 1, order.get(h["detector"], 99), h["start"]))
    accepted = []
    for h in hits:
        h["detector_hint"] = None
        clash = next((a for a in accepted if h["start"] < a["end"] and a["start"] < h["end"]), None)
        if clash is None:
            accepted.append(h)
        elif clash["detector"] == "live-secret" and h["detector"] != "live-secret" and clash["detector_hint"] is None:
            clash["detector_hint"] = h["detector"]
    for a in accepted:
        if known and a["live_match"] is None and a["value"] in known:
            a["live_match"] = known[a["value"]]
            a["risk"] = "HIGH"
    accepted.sort(key=lambda h: h["start"])
    return accepted

# -- Config helpers ---

def openclaw_state_dir() -> Path:
    env = os.environ.get("OPENCLAW_STATE_DIR")
    return Path(env).expanduser() if env else home() / ".openclaw"


def default_config_path() -> Path:
    env = os.environ.get("OPENCLAW_CONFIG_PATH")
    return Path(env).expanduser() if env else openclaw_state_dir() / "openclaw.json"


def claude_config_dir() -> Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(env).expanduser() if env else home() / ".claude"


def json5_to_json(text: str) -> str:
    """
    Minimal JSON5 → JSON conversion: // and /* */ comments, trailing commas,
    single-quoted strings and unquoted object keys. Enough for hand-edited configs.
    """
    out = []
    i, n = 0, len(text)

    def skip_ws_comments(j):
        while j < n:
            if text[j].isspace():
                j += 1
            elif text.startswith("//", j):
                j = text.find("\n", j)
                j = n if j == -1 else j
            elif text.startswith("/*", j):
                j = text.find("*/", j + 2)
                j = n if j == -1 else j + 2
            else:
                break
        return j

    while i < n:
        ch = text[i]
        if ch in "\"'":
            quote, j, buf = ch, i + 1, []
            while j < n and text[j] != quote:
                if text[j] == "\\" and j + 1 < n:
                    nxt = text[j + 1]
                    if quote == "'" and nxt == "'":
                        buf.append("'")
                    elif nxt == "\n":
                        pass
                    else:
                        buf.append("\\" + nxt)
                    j += 2
                    continue
                buf.append('\\"' if (text[j] == '"' and quote == "'") else text[j])
                j += 1
            out.append('"' + "".join(buf) + '"')
            i = j + 1
        elif text.startswith("//", i) or text.startswith("/*", i):
            i = skip_ws_comments(i)
        elif ch == ",":
            j = skip_ws_comments(i + 1)
            if j < n and text[j] in "}]":
                i += 1
                continue
            out.append(ch)
            i += 1
        elif ch.isalpha() or ch in "_$":
            j = i
            while j < n and (text[j].isalnum() or text[j] in "_$"):
                j += 1
            word = text[i:j]
            k = skip_ws_comments(j)
            if k < n and text[k] == ":" and word not in ("true", "false", "null"):
                out.append(json.dumps(word))
            else:
                out.append(word)
            i = j
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def load_config(path: Path):
    """Returns (config, strict_json, indent). Accepts JSON5 (read-only)."""
    text = path.read_text(encoding="utf-8")
    try:
        config = json.loads(text)
        strict = True
    except json.JSONDecodeError:
        config = json.loads(json5_to_json(text))
        strict = False
    m = re.search(r'\n([ \t]+)["\w]', text)
    indent = (m.group(1) if m and "\t" in m.group(1) else len(m.group(1))) if m else 2
    return config, strict, indent


def write_config(path: Path, config: dict, indent):
    original = path.read_text(encoding="utf-8")
    text = json.dumps(config, indent=indent, ensure_ascii=False)
    if original.endswith("\n"):
        text += "\n"
    atomic_write_text(path, text, mode_of(path))


def parse_path(dot_path: str) -> list:
    tokens = []
    for key, idx in PATH_TOKEN_RE.findall(dot_path):
        tokens.append(int(idx) if idx else key)
    return tokens


def get_nested(d, dot_path: str):
    for tok in parse_path(dot_path):
        if isinstance(tok, int):
            if not isinstance(d, list) or tok >= len(d):
                return None
            d = d[tok]
        else:
            if not isinstance(d, dict):
                return None
            d = d.get(tok)
    return d


def set_nested(d, dot_path: str, value):
    tokens = parse_path(dot_path)
    for tok in tokens[:-1]:
        d = d[tok]
    d[tokens[-1]] = value


SECRETS_MARKER = "token-safety-checker secrets"


def default_secrets_file(shell_name: str) -> Path:
    """Dedicated private file for migrated secrets (never the shell profile itself)."""
    return openclaw_state_dir() / ("tightlip.fish" if shell_name == "fish" else "tightlip.env")


def profile_source_line(shell_name: str, secrets_path: Path) -> str:
    q = shlex.quote(str(secrets_path))
    if shell_name == "fish":
        return f"test -f {q}; and source {q}  # {SECRETS_MARKER}"
    return f"[ -f {q} ] && . {q}  # {SECRETS_MARKER}"


def append_private(path: Path, text: str):
    """Append to a file that is (and stays) private: created 0600, permissions fixed before any write."""
    if not path.parent.exists():
        path.parent.mkdir(parents=True, mode=0o700)
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(path), flags, 0o600)
    try:
        if stat.S_IMODE(os.fstat(fd).st_mode) & 0o077:
            os.fchmod(fd, 0o600)
        os.write(fd, text.encode("utf-8"))
    finally:
        os.close(fd)


def detect_shell() -> dict:
    shell_name = Path(os.environ.get("SHELL", "bash")).name
    candidates = SHELL_PROFILES.get(shell_name, SHELL_PROFILES["bash"])
    profile = next((p for p in candidates if Path(p).expanduser().exists()), candidates[0])
    return {
        "name":         shell_name,
        "profile":      profile,
        "secrets_file": tilde(default_secrets_file(shell_name)),
        "source_cmd":   f"source {profile}",
    }


def generic_env_name(path: str) -> str:
    parts = [str(t) for t in parse_path(path) if not isinstance(t, int)]
    last = re.sub(r'(?<!^)(?=[A-Z])', '_', parts[-1]).upper()
    prefix = re.sub(r'[^A-Z0-9]', '_', parts[-2].upper()) if len(parts) >= 2 else ""
    name = f"OPENCLAW_{prefix}_{last}" if prefix else f"OPENCLAW_{last}"
    name = re.sub(r'[^A-Z0-9_]', '_', name)
    return re.sub(r'_+', '_', name)


def to_env_name(path: str) -> str:
    return ENV_HINTS.get(path) or generic_env_name(path)


def get_risk_level(path: str) -> str:
    # Channel bot tokens (incl. multi-account channels.<x>.accounts.<id>.*) and gateway auth control the agent
    if path in HIGH_RISK_PATHS or path.startswith(("channels.", "gateway.")):
        return "HIGH"
    if path in MEDIUM_RISK_PATHS:
        return "MEDIUM"
    return "LOW"


def is_secretref(value) -> bool:
    return isinstance(value, dict) and value.get("source") in ("env", "file", "exec")


def collect_secretrefs(config, refs: list | None = None) -> list:
    """Collect all SecretRef objects in the config."""
    if refs is None:
        refs = []
    if isinstance(config, dict):
        if is_secretref(config):
            refs.append(config)
            return refs
        for v in config.values():
            collect_secretrefs(v, refs)
    elif isinstance(config, list):
        for v in config:
            collect_secretrefs(v, refs)
    return refs


def scan_config(config, path: str = "", findings: list | None = None) -> list:
    """
    Recursively scan config for plaintext secrets.
    Returns list of { path, env_var, length, risk[, detector] } — NO secret values.
    A string is a secret when its key looks sensitive, or when its value matches a provider pattern.
    """
    if findings is None:
        findings = []
    if isinstance(config, dict):
        if is_secretref(config):
            return findings
        for k, v in config.items():
            scan_config(v, f"{path}.{k}" if path else str(k), findings)
    elif isinstance(config, list):
        for i, v in enumerate(config):
            scan_config(v, f"{path}[{i}]", findings)
    elif isinstance(config, str):
        if len(config) < MIN_SECRET_LEN or ENV_TEMPLATE_RE.match(config):
            return findings
        last = parse_path(path)
        key = next((str(t) for t in reversed(last) if not isinstance(t, int)), "").lower()
        key_hit = any(s in key for s in SENSITIVE_KEYS) and not key.endswith(POINTER_KEY_SUFFIXES)
        detector = None
        if not key_hit:
            hits = [h for h in detect_secrets(config) if h["detector"] in PROVIDER_DETECTORS]
            detector = hits[0]["detector"] if hits else None
        if key_hit or detector:
            risk = get_risk_level(path)
            if detector and risk == "LOW":
                risk = "MEDIUM"
            f = {"path": path, "env_var": to_env_name(path), "length": len(config),
                 "risk": risk, "fingerprint": fingerprint(config)}
            if detector:
                f["detector"] = detector
            findings.append(f)
    return findings


def assign_env_names(findings: list, config) -> list:
    """
    Make env var names unique per distinct secret value. Two paths that share an env var
    hint (e.g. gateway.auth.token / gateway.remote.token) keep sharing it only if the values are equal.
    """
    taken = {}  # env_var -> fingerprint
    for f in findings:
        fp = f.get("fingerprint") or fingerprint(get_nested(config, f["path"]) or "")
        name = f["env_var"]
        if name in taken and taken[name] != fp:
            name = generic_env_name(f["path"])
            n = 2
            base = name
            while name in taken and taken[name] != fp:
                name = f"{base}_{n}"
                n += 1
        taken[name] = fp
        f["env_var"] = name
    return findings


def config_known_secrets(config) -> dict:
    """value → label map of live secrets (plaintext in config + values behind env SecretRefs)."""
    known = {}
    if not isinstance(config, (dict, list)):
        return known
    for f in scan_config(config):
        v = get_nested(config, f["path"])
        if isinstance(v, str) and len(v) >= 12:
            known[v] = f["path"]
    for ref in collect_secretrefs(config):
        if ref.get("source") == "env" and ref.get("id"):
            v = os.environ.get(ref["id"])
            if v and len(v) >= 12:
                known[v] = f"${ref['id']}"
    return known

# -- Git history scan ---

def scan_git_history(config_path: Path) -> dict:
    """
    Scan git history of config_path for past plaintext secret exposures.
    Returns { "supported": bool, "commits_scanned": int, "exposed_commits": [...] }
    Never returns secret values — only paths, risk levels, and commit metadata.
    """
    result = {"supported": False, "commits_scanned": 0, "exposed_commits": []}

    if not shutil.which("git"):
        result["error"] = "git not found in PATH"
        return result

    try:
        r = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, cwd=config_path.parent
        )
        if r.returncode != 0:
            result["error"] = "Not a git repository"
            return result
        git_root = r.stdout.strip()
    except Exception as e:
        result["error"] = str(e)
        return result

    result["supported"] = True

    try:
        rel_path = str(config_path.resolve().relative_to(Path(git_root).resolve()))
    except ValueError:
        result["error"] = "Config file is not inside a git repository"
        result["supported"] = False
        return result

    log = subprocess.run(
        ["git", "log", "--all", "--format=%H|%ai|%an", "--", rel_path],
        capture_output=True, text=True, cwd=git_root
    )
    commit_lines = [l for l in log.stdout.strip().split("\n") if l]
    result["commits_scanned"] = len(commit_lines)

    for line in commit_lines:
        parts = line.split("|", 2)
        if len(parts) < 3:
            continue
        commit_hash, date, author = parts
        show = subprocess.run(
            ["git", "show", f"{commit_hash}:{rel_path}"],
            capture_output=True, text=True, cwd=git_root
        )
        if show.returncode != 0:
            continue
        try:
            content = json.loads(show.stdout)
        except json.JSONDecodeError:
            try:
                content = json.loads(json5_to_json(show.stdout))
            except json.JSONDecodeError:
                continue
        findings = scan_config(content)
        if findings:
            result["exposed_commits"].append({
                "commit":   commit_hash[:8],
                "date":     date,
                "author":   author,
                "findings": [{"path": f["path"], "risk": f["risk"]} for f in findings],
            })
    return result

# -- Memory targets ---

def _target(platform, scope, path, kind="text"):
    return {"platform": platform, "scope": scope, "path": Path(path), "kind": kind}


def _kind_for(p: Path) -> str:
    if p.suffix == ".sqlite" or p.suffix == ".db":
        return "sqlite"
    return "text"


def openclaw_workspaces(state_dir: Path, config) -> list:
    candidates = []
    env = os.environ.get("OPENCLAW_WORKSPACE_DIR")
    if env:
        candidates.append(Path(env).expanduser())
    if isinstance(config, dict):
        ws = get_nested(config, "agents.defaults.workspace")
        if isinstance(ws, str):
            candidates.append(Path(ws).expanduser())
        agents = get_nested(config, "agents.list")
        if isinstance(agents, list):
            for a in agents:
                if isinstance(a, dict) and isinstance(a.get("workspace"), str):
                    candidates.append(Path(a["workspace"]).expanduser())
    candidates.append(state_dir / "workspace")
    if state_dir.is_dir():
        candidates.extend(sorted(p for p in state_dir.glob("workspace-*") if p.is_dir()))
    seen, result = set(), []
    for c in candidates:
        try:
            key = c.resolve()
        except OSError:
            continue
        if c.is_dir() and key not in seen:
            seen.add(key)
            result.append(c)
    return result


def openclaw_targets(state_dir: Path, config, include_transcripts=True) -> list:
    targets = []
    for ws in openclaw_workspaces(state_dir, config):
        for name in OPENCLAW_LONG_TERM:
            p = ws / name
            if p.is_file():
                targets.append(_target("openclaw", "long_term", p))
        mem = ws / "memory"
        if mem.is_dir():
            for p in sorted(mem.rglob("*")):
                if p.is_file() and p.suffix in TEXT_SUFFIXES:
                    scope = "long_term" if "imports" in p.relative_to(mem).parts else "short_term"
                    targets.append(_target("openclaw", scope, p))
    if include_transcripts and state_dir.is_dir():
        agents = state_dir / "agents"
        if agents.is_dir():
            for p in sorted(agents.rglob("*")):
                if not p.is_file():
                    continue
                if p.suffix == ".jsonl" or (p.suffix in (".sqlite", ".db") and "codex-home" not in p.parts):
                    targets.append(_target("openclaw", "transcript", p, _kind_for(p)))
        logs = state_dir / "logs"
        if logs.is_dir():
            for p in sorted(logs.rglob("*")):
                if p.is_file() and p.suffix in (".jsonl", ".log", ".txt"):
                    targets.append(_target("openclaw", "log", p))
    return targets


def claude_auto_memory_dirs(cfg: Path) -> list:
    dirs = []
    projects = cfg / "projects"
    if projects.is_dir():
        dirs.extend(sorted(p for p in projects.glob("*/memory") if p.is_dir()))
    settings = cfg / "settings.json"
    if settings.is_file():
        try:
            custom = json.loads(settings.read_text(encoding="utf-8")).get("autoMemoryDirectory")
            if isinstance(custom, str) and Path(custom).expanduser().is_dir():
                dirs.append(Path(custom).expanduser())
        except (json.JSONDecodeError, OSError, AttributeError):
            pass
    agent_mem = cfg / "agent-memory"
    if agent_mem.is_dir():
        dirs.append(agent_mem)
    return dirs


def claude_project_files(project: Path) -> list:
    files = []
    stop = home().parent
    d = project.resolve()
    chain = [d] + list(d.parents)
    for i, cur in enumerate(chain):
        if cur == stop or (i > 0 and cur == Path(cur.anchor)):
            break
        for name in ("CLAUDE.md", "CLAUDE.local.md", ".claude/CLAUDE.md"):
            p = cur / name
            if p.is_file():
                files.append(p)
        if i == 0:
            p = cur / "AGENTS.md"
            if p.is_file():
                files.append(p)
            rules = cur / ".claude" / "rules"
            if rules.is_dir():
                files.extend(sorted(r for r in rules.rglob("*.md") if r.is_file()))
    return files


def claude_targets(cfg: Path, project: Path | None, include_transcripts=True) -> list:
    targets = []
    if (cfg / "CLAUDE.md").is_file():
        targets.append(_target("claude", "long_term", cfg / "CLAUDE.md"))
    rules = cfg / "rules"
    if rules.is_dir():
        targets.extend(_target("claude", "long_term", p) for p in sorted(rules.rglob("*.md")) if p.is_file())
    for d in claude_auto_memory_dirs(cfg):
        targets.extend(_target("claude", "long_term", p) for p in sorted(d.rglob("*"))
                       if p.is_file() and p.suffix in TEXT_SUFFIXES)
    if project is not None and project.is_dir():
        targets.extend(_target("claude", "long_term", p) for p in claude_project_files(project))
    if include_transcripts:
        history = cfg / "history.jsonl"
        if history.is_file():
            targets.append(_target("claude", "short_term", history))
        projects = cfg / "projects"
        if projects.is_dir():
            for p in sorted(projects.rglob("*")):
                if not p.is_file() or "memory" in p.relative_to(projects).parts[1:2]:
                    continue
                if p.suffix == ".jsonl" or ("tool-results" in p.parts and p.suffix in (".txt", ".json", ".md")):
                    targets.append(_target("claude", "transcript", p))
    return targets


def resolve_platforms(choice: str, state_dir: Path, cfg: Path, project: Path | None) -> list:
    if choice == "all":
        return ["openclaw", "claude"]
    if choice in ("openclaw", "claude"):
        return [choice]
    found = []
    if state_dir.is_dir():
        found.append("openclaw")
    if cfg.is_dir() or (project is not None and claude_project_files(project)):
        found.append("claude")
    return found

# -- Memory scan ---

def _iter_text_records(target):
    """Yield (location, text) for a target. Location is a line number or 'table:rowid'."""
    path = target["path"]
    if target["kind"] == "sqlite":
        con, tables = None, []
        # read-only; fall back to immutable mode when the gateway holds a lock
        for qs in ("mode=ro", "mode=ro&immutable=1"):
            try:
                con = sqlite3.connect(f"file:{path}?{qs}", uri=True)
                tables = [r[0] for r in con.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
                break
            except sqlite3.Error:
                if con is not None:
                    con.close()
                con = None
        if con is None:
            return
        try:
            for t in tables:
                try:
                    cur = con.execute(f'SELECT rowid, * FROM "{t}"')
                    with_rowid = True
                except sqlite3.Error:
                    cur = con.execute(f'SELECT * FROM "{t}"')
                    with_rowid = False
                for n, row in enumerate(cur, 1):
                    rowid = row[0] if with_rowid else n
                    for v in (row[1:] if with_rowid else row):
                        if isinstance(v, bytes):
                            v = v.decode("utf-8", "ignore")
                        if isinstance(v, str) and len(v) >= 16:
                            yield f"{t}:rowid={rowid}", v
        except sqlite3.Error:
            pass
        finally:
            con.close()
        return
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, 1):
                yield lineno, line
    except OSError:
        return


def scan_memory(platforms: list, state_dir: Path, cfg: Path, project: Path | None,
                config=None, include_transcripts=True) -> dict:
    known = config_known_secrets(config) if config is not None else {}
    targets = []
    if "openclaw" in platforms:
        targets += openclaw_targets(state_dir, config, include_transcripts)
    if "claude" in platforms:
        targets += claude_targets(cfg, project, include_transcripts)

    secrets = {}  # fingerprint -> record
    files_scanned, bytes_scanned, errors = 0, 0, []
    seen_paths = set()
    for t in targets:
        try:
            rp = t["path"].resolve()
        except OSError:
            continue
        if rp in seen_paths:
            continue
        seen_paths.add(rp)
        try:
            bytes_scanned += t["path"].stat().st_size
        except OSError as e:
            errors.append(f"{tilde(t['path'])}: {e.strerror}")
            continue
        files_scanned += 1
        for loc, text in _iter_text_records(t):
            for h in detect_secrets(text, known):
                fp = fingerprint(h["value"])
                rec = secrets.get(fp)
                if rec is None:
                    detector = h["detector_hint"] or h["detector"]
                    rec = secrets[fp] = {
                        "fingerprint": fp, "detector": detector, "risk": h["risk"],
                        "length": len(h["value"]), "live_match": h["live_match"],
                        "occurrences": 0, "scopes": [], "locations": [],
                        "rotate": ROTATE_HINTS.get(detector, ROTATE_DEFAULT),
                    }
                rec["occurrences"] += 1
                if h["live_match"] and not rec["live_match"]:
                    rec["live_match"] = h["live_match"]
                    rec["risk"] = "HIGH"
                if t["scope"] not in rec["scopes"]:
                    rec["scopes"].append(t["scope"])
                if len(rec["locations"]) < 10:
                    loc_rec = {"platform": t["platform"], "scope": t["scope"], "file": tilde(t["path"]), "line": loc}
                    rec["locations"].append(loc_rec)

    out = sorted(secrets.values(),
                 key=lambda r: (RISK_ORDER[r["risk"]], r["live_match"] is None, -r["occurrences"]))
    for r in out:
        r["more_locations"] = max(0, r["occurrences"] - len(r["locations"]))
    by_scope = {}
    for r in out:
        for s in r["scopes"]:
            by_scope[s] = by_scope.get(s, 0) + 1
    result = {
        "platforms": platforms,
        "files_scanned": files_scanned,
        "bytes_scanned": bytes_scanned,
        "roots": {
            **({"openclaw": tilde(state_dir)} if "openclaw" in platforms else {}),
            **({"claude": tilde(cfg)} if "claude" in platforms else {}),
            **({"project": tilde(project)} if project is not None and "claude" in platforms else {}),
        },
        "secrets": out,
        "summary": {
            "unique_secrets": len(out),
            "occurrences": sum(r["occurrences"] for r in out),
            "high": sum(1 for r in out if r["risk"] == "HIGH"),
            "live_matches": sum(1 for r in out if r["live_match"]),
            "by_scope": by_scope,
        },
    }
    if errors:
        result["errors"] = errors[:20]
    if out:
        result["advice"] = [
            "Rotate every listed secret: anything in memory or a transcript was already sent to a model provider.",
            "Do NOT open or print the flagged files in this chat — that would copy the secret into a new transcript.",
            "Remove the secret from memory files by hand (or wait for `redact` in a future release), "
            "then run `install-guard` to stop new leaks.",
        ]
    return result


def print_memory_summary(mem: dict):
    s = mem["summary"]
    print(f"\n-- Memory scan: {mem['files_scanned']} file(s), platforms: {', '.join(mem['platforms']) or 'none'}",
          file=sys.stderr)
    if not mem["secrets"]:
        print("    ✅ No secrets found in agent memory or transcripts", file=sys.stderr)
        return
    print(f"[!] {s['unique_secrets']} unique secret(s), {s['occurrences']} occurrence(s):", file=sys.stderr)
    for r in mem["secrets"]:
        icon = RISK_ICON.get(r["risk"], "⚪")
        live = f"  ← live: {r['live_match']}" if r["live_match"] else ""
        print(f"    {icon} [{r['risk']}] {r['detector']} {r['fingerprint']} ×{r['occurrences']} "
              f"({', '.join(r['scopes'])}){live}", file=sys.stderr)
        for loc in r["locations"][:3]:
            print(f"        {loc['file']}:{loc['line']}", file=sys.stderr)
        if r["occurrences"] > 3:
            print(f"        … {r['occurrences'] - 3} more", file=sys.stderr)
    print("\n    ⚠️  Rotate these credentials — memory and transcripts are sent to the model provider.",
          file=sys.stderr)

# -- Shell profile helpers ---

def validate_env_var(name: str) -> str:
    if not ENV_VAR_RE.match(name):
        raise ValueError(
            f"Invalid env var name {name!r} — only A-Z, 0-9 and _ allowed, must start with a letter or _"
        )
    return name


def shell_single_quote(value: str) -> str:
    """
    Wrap value in single quotes for safe shell assignment.
    Single quotes prevent ALL interpolation ($, backtick, etc.).
    Literal ' is handled by: 'before'"'"'after' → before'after
    """
    return "'" + value.replace("'", "'\\''") + "'"


def export_line(shell: str, env_var: str, value: str) -> str:
    safe_value = shell_single_quote(value)
    if shell == "fish":
        return f"set -gx {env_var} {safe_value}"
    return f"export {env_var}={safe_value}"


def profile_exports(profile_text: str) -> dict:
    """Parse `export NAME=...` / `set -gx NAME ...` lines → {NAME: value} (exact name match)."""
    found = {}
    for line in profile_text.splitlines():
        m = re.match(r'^\s*(?:export\s+([A-Za-z_][A-Za-z0-9_]*)=(.*)|set\s+-gx\s+([A-Za-z_][A-Za-z0-9_]*)\s+(.*))$', line)
        if not m:
            continue
        name = m.group(1) or m.group(3)
        raw = m.group(2) if m.group(1) else m.group(4)
        try:
            parts = shlex.split(raw, comments=True)
            found[name] = parts[0] if parts else ""
        except ValueError:
            found[name] = None
    return found


OUR_BACKUP_RE = re.compile(r"\.bak-\d{8}-\d{6}(?:-\d+)?$")


def list_backups(config_path: Path, ours_only: bool = False) -> list:
    """
    Our timestamped backups (newest first), then other *.bak* files — the legacy v2 `.bak`
    and OpenClaw's own rotating backups (`openclaw.json.bak`, `.bak.1`, …).
    """
    files = [p for p in config_path.parent.glob(config_path.name + ".bak*") if p.is_file()]
    ours = sorted((p for p in files if OUR_BACKUP_RE.search(p.name)), key=lambda p: p.name, reverse=True)
    if ours_only:
        return ours
    others = sorted((p for p in files if p not in ours), key=lambda p: p.stat().st_mtime, reverse=True)
    return ours + others


def backup_has_plaintext(path: Path) -> bool:
    try:
        return bool(scan_config(load_config(path)[0]))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return False

# -- Verify ---

def run_verify(config_path: Path, clean_backup: bool = False, profile: str | None = None,
               secrets_file: str | None = None) -> int:
    """
    Run post-migration health checks. Returns 0 if all clear, 1 if issues found.
    """
    issues = []
    ok = []

    print("\n-- SafeClaw Verify ---")

    if not config_path.exists():
        print(f"[ERROR] Config not found: {config_path}", file=sys.stderr)
        return 1

    config, _, _ = load_config(config_path)

    # 1. Remaining plaintext secrets
    findings = scan_config(config)
    if findings:
        for f in findings:
            icon = RISK_ICON.get(f["risk"], "⚪")
            issues.append(f"  {icon} [{f['risk']}] Plaintext secret still present: {f['path']}")
    else:
        ok.append("  ✅ No plaintext secrets in config")

    # 2. Config file permissions
    if not is_private(config_path):
        issues.append(f"  🟡 [MEDIUM] {config_path.name} permissions are {oct(mode_of(config_path))[2:]}"
                      f" — run: chmod 600 {config_path}")
    else:
        ok.append("  ✅ Config permissions OK (no group/other access)")

    # 3. SecretRefs resolve
    refs = collect_secretrefs(config)
    env_refs = [r["id"] for r in refs if r.get("source") == "env" and r.get("id")]
    missing = [r for r in env_refs if not os.environ.get(r)]
    for m in missing:
        issues.append(f"  🔴 [HIGH] ${m} is referenced in config but NOT set in current environment")
    for r in refs:
        if r.get("source") == "file" and r.get("id"):
            fp = Path(r["id"]).expanduser()
            if not fp.is_file():
                issues.append(f"  🔴 [HIGH] file SecretRef points to a missing file: {fp}")
            elif not is_private(fp):
                issues.append(f"  🟡 [MEDIUM] secret file {fp} is readable by others — run: chmod 600 {fp}")
    if refs and not any("SecretRef" in i or "NOT set" in i or "secret file" in i for i in issues):
        ok.append(f"  ✅ All {len(refs)} SecretRef(s) resolve")
    elif not refs:
        ok.append("  ✅ No SecretRefs found (nothing to check)")

    # 4. Where the secret values live: private secrets file; older versions wrote them into the profile
    shell = detect_shell()
    sec = Path(secrets_file).expanduser() if secrets_file else default_secrets_file(shell["name"])
    if sec.is_file() and not is_private(sec):
        issues.append(f"  🟡 [MEDIUM] secrets file {tilde(sec)} is readable by others — run: chmod 600 {sec}")
    prof = Path(profile or shell["profile"]).expanduser()
    if prof.is_file() and env_refs:
        exports = profile_exports(prof.read_text(encoding="utf-8", errors="replace"))
        if any(r in exports for r in env_refs) and not is_private(prof):
            issues.append(f"  🟡 [MEDIUM] {tilde(prof)} holds secrets (written by an older version) and is readable "
                          f"by others ({oct(mode_of(prof))[2:]}) — move those export lines into {tilde(sec)} "
                          f"(chmod 600), or run: chmod 600 {prof}")

    # 5. Backup files still holding plaintext (ours + OpenClaw's own rotating .bak files)
    ours = list_backups(config_path, ours_only=True)
    leaky = [b for b in list_backups(config_path) if backup_has_plaintext(b)]
    removable = list(dict.fromkeys(ours + leaky))
    if removable:
        if clean_backup:
            for b in removable:
                b.unlink()
            ok.append(f"  ✅ Removed {len(removable)} backup file(s)")
        elif leaky:
            foreign = [b.name for b in leaky if b not in ours]
            note = f" ({len(foreign)} created by OpenClaw itself: {', '.join(foreign)})" if foreign else ""
            issues.append(
                f"  🟡 [MEDIUM] {len(leaky)} backup file(s) still contain plaintext secrets{note} — "
                f"run with --clean-backup once you no longer need rollback"
            )

    for line in ok:
        print(line)
    if issues:
        print(f"\n  ⚠️  {len(issues)} issue(s) found:")
        for line in issues:
            print(line)
        print()
        return 1

    print("\n  🦀 All checks passed — your config looks clean!\n")
    return 0

# -- Guard (leak prevention) ---

def is_memory_path(file_path: str) -> bool:
    p = file_path.replace("\\", "/")
    name = p.rsplit("/", 1)[-1]
    if name in MEMORY_FILENAMES:
        return True
    if "/.claude/rules/" in p or "/agent-memory/" in p:
        return True
    if "/memory/" in p and ("." + name.rsplit(".", 1)[-1]) in TEXT_SUFFIXES:
        return True
    return False


def _guard_reason(hits, file_path) -> str:
    kinds = ", ".join(sorted({f"{h['detector_hint'] or h['detector']} ({fingerprint(h['value'])})" for h in hits}))
    return (f"token-safety-checker blocked this write: it would store a secret [{kinds}] in "
            f"{tilde(file_path)}. Memory and instruction files are loaded into every session and sent to "
            f"the model provider. Keep the secret in an environment variable or secret manager and write a "
            f"placeholder such as ${{MY_API_KEY}} instead. Do not retry with the same value.")


def cmd_guard_hook(args):
    """Claude Code PreToolUse hook. Fail-open on any internal error so it never breaks a session."""
    try:
        data = json.load(sys.stdin)
        tool = data.get("tool_name", "")
        ti = data.get("tool_input") or {}
        file_path = ti.get("file_path") or ti.get("notebook_path") or ""
        if tool == "Write":
            content = ti.get("content", "")
        elif tool == "Edit":
            content = ti.get("new_string", "")
        elif tool == "MultiEdit":
            content = "\n".join(e.get("new_string", "") for e in ti.get("edits", []))
        elif tool == "NotebookEdit":
            content = ti.get("new_source", "")
        else:
            return 0
        if not content or not file_path:
            return 0
        if args.scope == "memory" and not is_memory_path(file_path):
            return 0
        hits = detect_secrets(content)
        if not hits:
            return 0
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": _guard_reason(hits, file_path),
        }}))
        return 0
    except Exception:
        return 0


def cmd_guard_git(args):
    """git pre-commit hook: block commits that add secrets."""
    r = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
                       capture_output=True)
    if r.returncode != 0:
        return 0
    blocked = []
    for name in [n for n in r.stdout.decode("utf-8", "replace").split("\0") if n]:
        show = subprocess.run(["git", "show", f":{name}"], capture_output=True)
        if show.returncode != 0 or b"\0" in show.stdout[:8000]:
            continue
        text = show.stdout.decode("utf-8", "replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for h in detect_secrets(line):
                blocked.append((name, lineno, h["detector"], fingerprint(h["value"])))
    if not blocked:
        return 0
    print("🦀 token-safety-checker: commit blocked — staged files contain secrets:", file=sys.stderr)
    for name, lineno, det, fp in blocked[:20]:
        print(f"    {name}:{lineno}  {det}  {fp}", file=sys.stderr)
    print("  Move the secret out of the workspace (env var / secret manager), then commit again.\n"
          "  To remove this guard: safeclaw.py uninstall-guard --platform openclaw", file=sys.stderr)
    return 1


def _guard_script_dest_claude(cfg: Path) -> Path:
    return cfg / "hooks" / f"{GUARD_MARKER}.py"


def _guard_script_dest_openclaw(state_dir: Path) -> Path:
    return state_dir / "token-safety-checker" / f"{GUARD_MARKER}.py"


def _install_script_copy(dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_bytes(dest, Path(__file__).resolve().read_bytes(), 0o700)


def _strip_guard_hooks(settings: dict) -> int:
    removed = 0
    pre = settings.get("hooks", {}).get("PreToolUse")
    if not isinstance(pre, list):
        return 0
    kept = []
    for entry in pre:
        hooks = [h for h in entry.get("hooks", []) if GUARD_MARKER not in str(h.get("command", ""))]
        removed += len(entry.get("hooks", [])) - len(hooks)
        if hooks:
            entry["hooks"] = hooks
            kept.append(entry)
    settings["hooks"]["PreToolUse"] = kept
    if not kept:
        del settings["hooks"]["PreToolUse"]
    if not settings["hooks"]:
        del settings["hooks"]
    return removed


def _load_settings(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    return json.loads(text) if text.strip() else {}


def install_guard_claude(cfg: Path, scope: str, settings_path: Path | None) -> str:
    settings_path = settings_path or cfg / "settings.json"
    settings = _load_settings(settings_path)
    dest = _guard_script_dest_claude(cfg)
    _install_script_copy(dest)
    if settings_path.exists():
        private_copy(settings_path, unique_path(settings_path.with_name(settings_path.name + f".bak-{now_stamp()}")))
    _strip_guard_hooks(settings)
    settings.setdefault("hooks", {}).setdefault("PreToolUse", []).append({
        "matcher": "Write|Edit|MultiEdit|NotebookEdit",
        "hooks": [{"type": "command",
                   "command": f'python3 "{dest}" guard-hook --scope {scope}',
                   "timeout": 10}],
    })
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(settings_path, json.dumps(settings, indent=2) + "\n",
                      mode_of(settings_path) if settings_path.exists() else 0o600)
    return (f"[OK] Claude Code guard installed → {tilde(settings_path)} "
            f"(PreToolUse: Write|Edit, scope={scope}); hook script: {tilde(dest)}")


def uninstall_guard_claude(cfg: Path, settings_path: Path | None) -> str:
    settings_path = settings_path or cfg / "settings.json"
    if not settings_path.exists():
        return "[OK] Claude Code: no settings.json — nothing to remove"
    settings = _load_settings(settings_path)
    removed = _strip_guard_hooks(settings)
    if removed:
        atomic_write_text(settings_path, json.dumps(settings, indent=2) + "\n", mode_of(settings_path))
    dest = _guard_script_dest_claude(cfg)
    if dest.exists():
        dest.unlink()
    return f"[OK] Claude Code: removed {removed} guard hook(s) from {tilde(settings_path)}"


GIT_HOOK_TEMPLATE = """#!/bin/sh
# {marker}: installed by token-safety-checker (safeclaw.py install-guard)
# Blocks commits that contain secrets. Remove with: safeclaw.py uninstall-guard --platform openclaw
exec python3 "{script}" guard-git
"""


def install_guard_openclaw(state_dir: Path, config) -> list:
    msgs = []
    dest = _guard_script_dest_openclaw(state_dir)
    workspaces = [w for w in openclaw_workspaces(state_dir, config) if (w / ".git").is_dir()]
    if not workspaces:
        return ["[SKIP] OpenClaw: no git-backed workspace found (nothing to guard)"]
    _install_script_copy(dest)
    for ws in workspaces:
        hook = ws / ".git" / "hooks" / "pre-commit"
        if hook.exists() and GUARD_MARKER not in hook.read_text(encoding="utf-8", errors="replace"):
            msgs.append(f"[SKIP] {tilde(hook)} already exists (not ours) — add this line to it manually:\n"
                        f"         python3 \"{dest}\" guard-git || exit 1")
            continue
        hook.parent.mkdir(parents=True, exist_ok=True)
        hook.write_text(GIT_HOOK_TEMPLATE.format(marker=GUARD_MARKER, script=dest), encoding="utf-8")
        os.chmod(hook, 0o755)
        msgs.append(f"[OK] OpenClaw guard installed → {tilde(hook)}")
    return msgs


def uninstall_guard_openclaw(state_dir: Path, config) -> list:
    msgs = []
    for ws in openclaw_workspaces(state_dir, config):
        hook = ws / ".git" / "hooks" / "pre-commit"
        if hook.exists() and GUARD_MARKER in hook.read_text(encoding="utf-8", errors="replace"):
            hook.unlink()
            msgs.append(f"[OK] Removed {tilde(hook)}")
    dest = _guard_script_dest_openclaw(state_dir)
    if dest.exists():
        dest.unlink()
    return msgs or ["[OK] OpenClaw: no guard hooks found"]

# -- Subcommands ---

def _try_load_config(config_path: Path):
    if not config_path.exists():
        return None
    try:
        return load_config(config_path)[0]
    except (json.JSONDecodeError, OSError):
        return None


def _memory_from_args(args, config) -> dict:
    state_dir = Path(args.openclaw_dir).expanduser() if args.openclaw_dir else openclaw_state_dir()
    cfg = Path(args.claude_dir).expanduser() if args.claude_dir else claude_config_dir()
    project = Path(args.project).expanduser() if args.project else Path.cwd()
    platforms = resolve_platforms(args.platform, state_dir, cfg, project)
    return scan_memory(platforms, state_dir, cfg, project, config,
                       include_transcripts=not args.no_transcripts)


def cmd_scan(args):
    config_path = Path(args.config).expanduser()
    if not config_path.exists() and not args.memory:
        print(json.dumps({"error": f"Config not found: {config_path}"}))
        sys.exit(2)

    output = {"version": VERSION}
    findings = []
    perm_ok = True
    config = None
    if config_path.exists():
        config, strict, _ = load_config(config_path)
        findings = assign_env_names(scan_config(config), config)
        perm_ok = is_private(config_path)
        mode = oct(mode_of(config_path))[2:]
        output.update({
            "findings": findings,
            "shell":    detect_shell(),
            "checks": {
                "file_permissions": {
                    "ok":   perm_ok,
                    "mode": mode,
                    "note": None if perm_ok else f"Should be 600 — run: chmod 600 {config_path}",
                },
                "format": {"strict_json": strict,
                           "note": None if strict else "JSON5 detected — scan works, migrate needs plain JSON"},
            },
        })
    else:
        output["config"] = {"found": False, "path": str(config_path)}

    if args.deep and config_path.exists():
        print("[~] Scanning git history...", file=sys.stderr)
        output["git_history"] = scan_git_history(config_path)

    mem = None
    if args.memory:
        print("[~] Scanning agent memory + transcripts...", file=sys.stderr)
        mem = output["memory"] = _memory_from_args(args, config)

    print(json.dumps(output, indent=2, ensure_ascii=False))

    if findings:
        print(f"\n[!] {len(findings)} plaintext secret(s) found in config:", file=sys.stderr)
        for f in findings:
            icon = RISK_ICON.get(f["risk"], "⚪")
            print(f"    {icon} [{f['risk']}] {f['path']}", file=sys.stderr)
    if not perm_ok:
        print(f"\n[!] Config permissions: {output['checks']['file_permissions']['mode']} (should be 600)",
              file=sys.stderr)
    if args.deep and output.get("git_history", {}).get("exposed_commits"):
        exposed = output["git_history"]["exposed_commits"]
        print(f"\n[!] git history: {len(exposed)} commit(s) contained plaintext secrets:", file=sys.stderr)
        for c in exposed:
            paths = ", ".join(x["path"] for x in c["findings"])
            print(f"    {c['commit']}  {c['date'][:10]}  [{paths}]", file=sys.stderr)
        print("\n    ⚠️  These commits are permanent in git history.", file=sys.stderr)
        print("    Consider rotating the affected tokens.", file=sys.stderr)
    if mem is not None:
        print_memory_summary(mem)

    sys.exit(1 if findings or (mem and mem["secrets"]) else 0)


def cmd_memory(args):
    config_path = Path(args.config).expanduser()
    config = _try_load_config(config_path)
    mem = _memory_from_args(args, config)
    print(json.dumps({"version": VERSION, "memory": mem}, indent=2, ensure_ascii=False))
    print_memory_summary(mem)
    sys.exit(1 if mem["secrets"] else 0)


def cmd_migrate(args):
    config_path = Path(args.config).expanduser()

    # -- Backup listing / restore ---
    if args.list_backups:
        backups = list_backups(config_path)
        if not backups:
            print("No backups found.")
        for b in backups:
            ts = datetime.datetime.fromtimestamp(b.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"  {ts}  {b}")
        return

    if args.restore:
        if args.backup:
            src = Path(args.backup).expanduser()
        else:
            # Only our own backups; fall back to the v2-era `.bak` when none exist
            ours = list_backups(config_path, ours_only=True)
            legacy = config_path.with_name(config_path.name + ".bak")
            src = ours[0] if ours else (legacy if legacy.exists() else None)
        if src is None or not src.exists():
            print(f"[ERROR] No backup found for {config_path}", file=sys.stderr)
            sys.exit(1)
        atomic_write_bytes(config_path, src.read_bytes(), mode_of(config_path) if config_path.exists() else 0o600)
        print(f"[OK] Restored {config_path} from {src}")
        return

    if not args.findings:
        print("[ERROR] --findings required", file=sys.stderr)
        sys.exit(1)

    findings = json.loads(args.findings)

    if not config_path.exists():
        print(f"[ERROR] Config not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    config, strict, indent = load_config(config_path)
    if not strict:
        print(f"[ERROR] {config_path.name} uses JSON5 syntax (comments / trailing commas). migrate will not "
              f"rewrite it and lose your comments. Convert it to plain JSON first, or set each SecretRef with "
              f"`openclaw config set`.", file=sys.stderr)
        sys.exit(1)

    current_findings = {f["path"]: f for f in scan_config(config)}
    to_migrate = [f for f in findings if f["path"] in current_findings]

    if not to_migrate:
        print("[OK] Nothing to migrate — all findings already resolved.")
        return

    # Validate env var names before touching any file
    for f in to_migrate:
        try:
            validate_env_var(f["env_var"])
        except ValueError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)

    # Two different secrets must never share one env var
    by_var = {}
    for f in to_migrate:
        value = get_nested(config, f["path"])
        prev = by_var.setdefault(f["env_var"], (f["path"], value))
        if prev[1] != value:
            print(f"[ERROR] {prev[0]} and {f['path']} hold different secrets but both map to "
                  f"{f['env_var']}. Rename one env_var in --findings (scan suggests unique names).",
                  file=sys.stderr)
            sys.exit(1)

    shell_name = Path(os.environ.get("SHELL", "bash")).name
    profile_path = Path(args.profile or detect_shell()["profile"]).expanduser()
    if profile_path.name == "config.fish":
        shell_name = "fish"
    secrets_path = Path(args.secrets_file).expanduser() if args.secrets_file else default_secrets_file(shell_name)
    # Existing exports: the secrets file, plus the profile for exports written by older versions
    existing = {}
    for src in (profile_path, secrets_path):
        if src.is_file():
            existing.update(profile_exports(src.read_text(encoding="utf-8", errors="replace")))
    profile_text = profile_path.read_text(encoding="utf-8", errors="replace") if profile_path.exists() else ""
    hook_line = profile_source_line(shell_name, secrets_path)
    needs_hook = not args.no_profile and SECRETS_MARKER not in profile_text

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Migration plan:")
    print(f"  config  : {config_path}")
    print(f"  backup  : {config_path.name}.bak-<timestamp> (mode 600)")
    print(f"  secrets : {secrets_path} (mode 600)")
    print(f"  profile : {profile_path} (" + ("adds one line that loads the secrets file — no secrets"
          if needs_hook else "unchanged") + ")")
    print()

    vars_to_add = []
    for f in to_migrate:
        env_var = f["env_var"]
        value = get_nested(config, f["path"])
        if env_var in existing:
            if existing[env_var] != value:
                print(f"[ERROR] {env_var} is already exported (in {tilde(secrets_path)} or {tilde(profile_path)}) "
                      f"with a DIFFERENT value. Rename the env_var for {f['path']}, or remove the old line if you "
                      f"rotated the token.", file=sys.stderr)
                sys.exit(1)
            print(f"  [secrets =] {env_var} already present with the same value, skipping")
        elif env_var not in vars_to_add:
            vars_to_add.append(env_var)
            print(f"  [secrets +] {export_line(shell_name, env_var, '***')}")
        if os.environ.get(env_var) not in (None, value):
            print(f"  [warn     ] ${env_var} is currently set to a different value in this shell")
        print(f"  [config  →] {f['path']}  →  SecretRef({env_var})")
    if needs_hook:
        print(f"  [profile +] {hook_line}")
    if secrets_path.exists() and not is_private(secrets_path):
        print(f"  [perm     ] {tilde(secrets_path)} is {oct(mode_of(secrets_path))[2:]} — will be set to 600 before writing")
    if args.secure_profile:
        print("  [note     ] --secure-profile is no longer needed: secrets are never written to the shell profile")

    if args.dry_run:
        print("\n[DRY RUN] No files modified.")
        return

    # 1. Backup (timestamped, created private, never overwritten)
    bak_path = unique_path(config_path.with_name(f"{config_path.name}.bak-{now_stamp()}"))
    private_copy(config_path, bak_path)
    print(f"\n[OK] Backup: {bak_path}")

    # 2. Secrets → private secrets file (0600 before the first byte is written)
    if vars_to_add:
        lines = [f"\n# Added by token-safety-checker v{VERSION} ({datetime.date.today()})"]
        written = set()
        for f in to_migrate:
            if f["env_var"] in vars_to_add and f["env_var"] not in written:
                value = get_nested(config, f["path"])
                if value and isinstance(value, str):
                    lines.append(export_line(shell_name, f["env_var"], value))
                    written.add(f["env_var"])
        append_private(secrets_path, "\n".join(lines) + "\n")
        print(f"[OK] Wrote {len(lines) - 1} secret(s) to {secrets_path} (mode 600)")

    # 3. Profile gets only the loader line (no secret values)
    if needs_hook:
        with open(profile_path, "a", encoding="utf-8") as pf:
            pf.write(f"\n{hook_line}\n")
        print(f"[OK] {profile_path}: added a line that loads {secrets_path}")

    # 4. Update config with SecretRefs (atomic, private temp file, keeps permissions + indentation)
    for f in to_migrate:
        set_nested(config, f["path"], {"source": "env", "provider": "default", "id": f["env_var"]})
    write_config(config_path, config, indent)
    print(f"[OK] Updated {config_path} with {len(to_migrate)} SecretRef(s)")

    print(f"""
[!] Next steps — load the secrets in this shell, then restart the gateway:

    source {secrets_path}
    openclaw gateway restart

    New shells load it automatically{" via " + str(profile_path) if needs_hook or SECRETS_MARKER in profile_text else ""}.
    systemd: put the variables in your unit's EnvironmentFile= (KEY=value lines, without `export`).
    Docker:  pass them via -e or environment: in compose.
""")

    print("-- Running post-migration verify ---")
    print("   (env var checks may show NOT SET until you source the secrets file)")
    run_verify(config_path, clean_backup=False, profile=str(profile_path), secrets_file=str(secrets_path))


def cmd_verify(args):
    config_path = Path(args.config).expanduser()
    sys.exit(run_verify(config_path, clean_backup=args.clean_backup, profile=args.profile,
                        secrets_file=args.secrets_file))


def _guard_platforms(args):
    state_dir = Path(args.openclaw_dir).expanduser() if args.openclaw_dir else openclaw_state_dir()
    cfg = Path(args.claude_dir).expanduser() if args.claude_dir else claude_config_dir()
    platforms = resolve_platforms(args.platform, state_dir, cfg, None)
    config = _try_load_config(Path(args.config).expanduser())
    return platforms, state_dir, cfg, config


def cmd_install_guard(args):
    platforms, state_dir, cfg, config = _guard_platforms(args)
    if not platforms:
        print("[ERROR] Neither OpenClaw (~/.openclaw) nor Claude Code (~/.claude) found. "
              "Use --platform claude|openclaw.", file=sys.stderr)
        sys.exit(1)
    settings = Path(args.settings).expanduser() if args.settings else None
    if "claude" in platforms:
        print(install_guard_claude(cfg, args.scope, settings))
    if "openclaw" in platforms:
        for m in install_guard_openclaw(state_dir, config):
            print(m)


def cmd_uninstall_guard(args):
    platforms, state_dir, cfg, config = _guard_platforms(args)
    settings = Path(args.settings).expanduser() if args.settings else None
    if "claude" in platforms:
        print(uninstall_guard_claude(cfg, settings))
    if "openclaw" in platforms:
        for m in uninstall_guard_openclaw(state_dir, config):
            print(m)

# -- Entry point ---

def _add_memory_args(p):
    p.add_argument("--platform", choices=["auto", "openclaw", "claude", "all"], default="auto",
                   help="Which agent memory to scan (default: auto-detect)")
    p.add_argument("--project", default=None, help="Project dir for CLAUDE.md / .claude/rules (default: cwd)")
    p.add_argument("--claude-dir", default=None, help="Claude Code config dir (default: $CLAUDE_CONFIG_DIR or ~/.claude)")
    p.add_argument("--openclaw-dir", default=None, help="OpenClaw state dir (default: $OPENCLAW_STATE_DIR or ~/.openclaw)")
    p.add_argument("--no-transcripts", action="store_true", help="Only scan memory files, skip transcripts/logs")


def main():
    parser = argparse.ArgumentParser(
        description="Token Safety Checker (tightlip) — find and fix leaked secrets in agent config + memory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"token-safety-checker {VERSION}")
    sub = parser.add_subparsers(dest="cmd")
    cfg_default = str(default_config_path())

    p_scan = sub.add_parser("scan", help="Detect plaintext secrets in openclaw.json (no values printed)")
    p_scan.add_argument("--config", default=cfg_default)
    p_scan.add_argument("--deep", action="store_true", help="Also scan git history for past plaintext secret commits")
    p_scan.add_argument("--memory", action="store_true", help="Also scan agent memory + transcripts")
    _add_memory_args(p_scan)

    p_mem = sub.add_parser("memory", help="Scan agent long/short-term memory + transcripts for secrets")
    p_mem.add_argument("--config", default=cfg_default, help="openclaw.json used to recognise live secrets")
    _add_memory_args(p_mem)

    p_mig = sub.add_parser("migrate", help="Migrate secrets to env vars + SecretRef")
    p_mig.add_argument("--findings", help="JSON list from scan output")
    p_mig.add_argument("--config", default=cfg_default)
    p_mig.add_argument("--profile", default=None, help="Shell profile that gets the line loading the secrets file")
    p_mig.add_argument("--secrets-file", default=None,
                       help="Private file for the migrated secrets (default: ~/.openclaw/tightlip.env, mode 600)")
    p_mig.add_argument("--no-profile", action="store_true", help="Do not touch the shell profile")
    p_mig.add_argument("--dry-run", action="store_true")
    p_mig.add_argument("--secure-profile", action="store_true", help=argparse.SUPPRESS)  # obsolete since 3.0.2
    p_mig.add_argument("--restore", action="store_true", help="Restore config from the newest backup")
    p_mig.add_argument("--backup", default=None, help="With --restore: restore this backup file")
    p_mig.add_argument("--list-backups", action="store_true", help="List available backups")

    p_ver = sub.add_parser("verify", help="Post-migration health check")
    p_ver.add_argument("--config", default=cfg_default)
    p_ver.add_argument("--profile", default=None)
    p_ver.add_argument("--secrets-file", default=None)
    p_ver.add_argument("--clean-backup", action="store_true", help="Delete backup files if found")

    for name, helptext in (("install-guard", "Install leak-prevention hooks"),
                           ("uninstall-guard", "Remove leak-prevention hooks")):
        p = sub.add_parser(name, help=helptext)
        if name == "install-guard":
            # Persistent hooks: the user must name the platform(s) explicitly — no auto-detection
            p.add_argument("--platform", choices=["openclaw", "claude", "all"], required=True)
        else:
            p.add_argument("--platform", choices=["auto", "openclaw", "claude", "all"], default="auto")
        p.add_argument("--scope", choices=["memory", "all"], default="memory",
                       help="Claude Code: guard memory/instruction files only (default) or every file write")
        p.add_argument("--settings", default=None, help="Claude Code settings.json to edit (default: user settings)")
        p.add_argument("--config", default=cfg_default)
        p.add_argument("--claude-dir", default=None)
        p.add_argument("--openclaw-dir", default=None)

    p_hook = sub.add_parser("guard-hook", help=argparse.SUPPRESS)
    p_hook.add_argument("--scope", choices=["memory", "all"], default="memory")
    sub.add_parser("guard-git", help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.cmd == "scan":
        cmd_scan(args)
    elif args.cmd == "memory":
        cmd_memory(args)
    elif args.cmd == "migrate":
        cmd_migrate(args)
    elif args.cmd == "verify":
        cmd_verify(args)
    elif args.cmd == "install-guard":
        cmd_install_guard(args)
    elif args.cmd == "uninstall-guard":
        cmd_uninstall_guard(args)
    elif args.cmd == "guard-hook":
        sys.exit(cmd_guard_hook(args))
    elif args.cmd == "guard-git":
        sys.exit(cmd_guard_git(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
