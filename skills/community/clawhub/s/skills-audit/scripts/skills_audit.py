#!/usr/bin/env python3
"""skills-audit/scripts/skills_audit.py  (v2.0.0)

Strict-template skills audit logger with file-level diff, SHA-256 integrity,
baseline approval, and git-based content diff.

Subcommands:
  init      - Initialize audit directory (~/.openclaw/skills-audit/)
  scan      - Scan workspace/skills, detect changes, log + git snapshot
  show      - Show human-readable change summary for a skill
  approve   - Mark skill(s) as approved in baseline
  baseline  - List or revoke baseline approvals

Outputs:
  ~/.openclaw/skills-audit/logs.ndjson   (append-only audit log)
  ~/.openclaw/skills-audit/state.json    (snapshot for diff)
  ~/.openclaw/skills-audit/baseline.json (approved skills)
  ~/.openclaw/skills-audit/snapshots/    (git repo for content diff)
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen
import platform
import subprocess
import uuid


# ---------------------------------------------------------------------------
# Version gate
# ---------------------------------------------------------------------------
if sys.version_info < (3, 9):
    print("Error: skills-audit requires Python >= 3.9", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
AUDIT_DIR = Path.home() / ".openclaw" / "skills-audit"
LOG_PATH = AUDIT_DIR / "logs.ndjson"
STATE_PATH = AUDIT_DIR / "state.json"
BASELINE_PATH = AUDIT_DIR / "baseline.json"
SNAPSHOTS_DIR = AUDIT_DIR / "snapshots"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def iso_utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_cmd(argv: list[str], cwd: str | Path | None = None) -> tuple[int, str, str]:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, check=False, cwd=cwd)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except FileNotFoundError as e:
        return 127, "", str(e)


# DEPRECATED: use sha256_file() instead. Kept for backward compatibility.
# DEPRECATED: md5_file removed in v2.0. Use sha256_file() instead.


def sha256_file(path: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def safe_read_text(path: Path, max_bytes: int = 512_000) -> str:
    try:
        with path.open("rb") as f:
            data = f.read(max_bytes)
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(safe_read_text(path))
    except Exception:
        return None


def list_files(dir_path: Path) -> list[Path]:
    files: list[Path] = []
    for p in dir_path.rglob("*"):
        if p.is_file():
            if "/.git/" in str(p) or "/__pycache__/" in str(p):
                continue
            if p.suffix == ".pyc":
                continue
            files.append(p)
    files.sort(key=lambda x: str(x))
    return files


# ---------------------------------------------------------------------------
# Risk scanning (rules loaded from config/risk-rules.json)
# ---------------------------------------------------------------------------

def load_risk_rules(workspace_dir: Path | None = None) -> tuple[list[tuple[str, str, list[str]]], dict]:
    """Load risk rules and context profiles from config/risk-rules.json.
    Returns (rules, context_profiles). Raises warning if config not found."""
    candidates = []
    if workspace_dir:
        candidates.append(workspace_dir / "skills" / "skills-audit" / "config" / "risk-rules.json")
    script_dir = Path(__file__).resolve().parent.parent
    candidates.append(script_dir / "config" / "risk-rules.json")

    for path in candidates:
        if path.exists():
            try:
                data = json.loads(path.read_text("utf-8"))
                rules = []
                for r in data.get("rules", []):
                    rules.append((r["id"], r["severity"], r["needles"]))
                profiles = data.get("context_profiles", {})
                # Remove meta keys
                profiles.pop("_comment", None)
                if rules:
                    return rules, profiles
            except Exception:
                continue

    print("Warning: config/risk-rules.json not found, risk scanning disabled", file=sys.stderr)
    return [], {}


def match_context_profiles(description: str, profiles: dict) -> list[str]:
    """Match a skill's description against context profiles. Return matched profile names."""
    if not description:
        return []
    desc_lower = description.lower()
    matched = []
    for name, profile in profiles.items():
        keywords = profile.get("keywords", [])
        for kw in keywords:
            if kw.lower() in desc_lower:
                matched.append(name)
                break
    return matched


def apply_context_scoring(
    findings: list[dict],
    profiles: dict,
    matched_profiles: list[str],
) -> list[dict]:
    """Apply context-aware scoring: ignore or downgrade rules based on matched profiles."""
    if not matched_profiles:
        return findings

    ignore_rules: set[str] = set()
    downgrade_map: dict[str, str] = {}

    for pname in matched_profiles:
        profile = profiles.get(pname, {})
        for rule_id in profile.get("ignore_rules", []):
            ignore_rules.add(rule_id)
        for rule_id, new_sev in profile.get("downgrade_rules", {}).items():
            # Keep the lowest severity if multiple profiles downgrade
            if rule_id not in downgrade_map:
                downgrade_map[rule_id] = new_sev

    adjusted = []
    for f in findings:
        rid = f["rule_id"]
        if rid in ignore_rules:
            continue  # Skip this finding entirely
        if rid in downgrade_map:
            f = dict(f)  # shallow copy
            f["severity"] = downgrade_map[rid]
            f["context_downgraded"] = True
        adjusted.append(f)

    return adjusted


# ---------------------------------------------------------------------------
# QianXin SafeSkill remote scanning
# ---------------------------------------------------------------------------

QIANXIN_DEFAULT_BASE_URL = "https://safeskill.qianxin.com"
QIANXIN_QUERY_TIMEOUT = 10      # seconds for intel query request
QIANXIN_MAX_RETRIES = 2         # remote intel query attempts
QIANXIN_RETRY_DELAY = 3         # seconds between remote attempts
QIANXIN_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "intelligent.json"

# Stable archive hashing excludes noisy/runtime files so the same skill tree yields the same MD5.
_QX_HASH_EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}
_QX_HASH_EXCLUDE_EXTS = {".pyc", ".pyo", ".so", ".dylib", ".dll"}
_QX_HASH_EXCLUDE_FILES = {"risk-rules.json"}


def load_qianxin_config() -> dict:
    cfg = {
        "token": "",
        "base_url": QIANXIN_DEFAULT_BASE_URL,
        "enabled": True,
        "mode": "md5-query",
    }
    try:
        if QIANXIN_CONFIG_PATH.exists():
            raw = json.loads(QIANXIN_CONFIG_PATH.read_text("utf-8"))
            if isinstance(raw, dict):
                cfg.update(raw)
    except Exception:
        pass
    return cfg


def _iter_qianxin_hash_files(root_dir: Path):
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = sorted(d for d in dirs if d not in _QX_HASH_EXCLUDE_DIRS)
        for fname in sorted(files):
            if fname in _QX_HASH_EXCLUDE_FILES:
                continue
            fpath = Path(root) / fname
            if fpath.suffix.lower() in _QX_HASH_EXCLUDE_EXTS:
                continue
            if fpath.stat().st_size > 5_000_000:
                continue
            yield fpath


def compute_qianxin_bundle_md5(root_dir: Path) -> str:
    """Compute a stable MD5 for the whole skills bundle.

    We intentionally hash normalized path metadata + file bytes rather than relying
    on zip container metadata, so repeated runs are deterministic.
    """
    h = hashlib.md5()
    for fpath in _iter_qianxin_hash_files(root_dir):
        rel = str(fpath.relative_to(root_dir)).replace(os.sep, "/")
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        with open(fpath, "rb") as fh:
            while True:
                chunk = fh.read(1024 * 1024)
                if not chunk:
                    break
                h.update(chunk)
        h.update(b"\0")
    return h.hexdigest()


def _qianxin_query_by_md5(bundle_md5: str, token: str, base_url: str) -> dict | None:
    """Query QianXin SafeSkill intel by MD5. Returns parsed JSON or None on error."""
    url = f"{base_url.rstrip('/')}/api/intel/md5/{bundle_md5}"
    req = Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Referer": f"{base_url.rstrip('/')}/",
        },
        method="GET",
    )
    try:
        with urlopen(req, timeout=QIANXIN_QUERY_TIMEOUT) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body)
    except URLError:
        return None
    except Exception:
        return None


def _map_qianxin_severity(qx_level: str) -> str:
    """Map QianXin severity to our internal levels."""
    mapping = {
        "CRITICAL": "extreme",
        "HIGH": "high",
        "MEDIUM": "medium",
        "LOW": "low",
        "INFO": "low",
    }
    return mapping.get(qx_level.upper(), "medium")


def _map_qianxin_decision(action: str) -> str:
    """Map QianXin recommended_action to our decision."""
    mapping = {
        "BLOCK": "deny",
        "REVIEW": "require_sandbox",
        "ALLOW": "allow",
    }
    return mapping.get(action.upper(), "allow_with_caution")


def qianxin_scan(skill_dir: Path, workspace_skills_dir: Path | None = None) -> dict | None:
    """Query QianXin SafeSkill by the MD5 of the whole skills bundle.

    Token is read from config/intelligent.json and defaults to empty. If the token is
    unset, this function returns None so callers fall back to local scanning.
    """
    cfg = load_qianxin_config()
    if not cfg.get("enabled", True):
        return None

    token = str(cfg.get("token", "") or "").strip()
    if not token:
        return None

    root_dir = (workspace_skills_dir or skill_dir.parent).resolve()
    try:
        bundle_md5 = compute_qianxin_bundle_md5(root_dir)
    except Exception:
        return None

    base_url = str(cfg.get("base_url", QIANXIN_DEFAULT_BASE_URL) or QIANXIN_DEFAULT_BASE_URL)
    result = _qianxin_query_by_md5(bundle_md5, token, base_url)
    if not result:
        return None

    summary = result.get("report_summary") or result.get("summary") or result
    if not isinstance(summary, dict):
        return None

    qx_level = summary.get("level", "LOW")
    level = _map_qianxin_severity(str(qx_level))
    decision = _map_qianxin_decision(str(summary.get("recommended_action", "ALLOW")))

    findings = []
    by_severity = summary.get("by_severity", {}) if isinstance(summary.get("by_severity", {}), dict) else {}
    by_category = summary.get("by_category", {}) if isinstance(summary.get("by_category", {}), dict) else {}
    for category, count in by_category.items():
        try:
            count_num = int(count)
        except Exception:
            count_num = 0
        if count_num > 0:
            findings.append({
                "rule_id": f"QIANXIN_{str(category).upper()}",
                "severity": level,
                "evidence": {
                    "file": "(remote md5 intel)",
                    "line": None,
                    "snippet": f"bundle_md5={bundle_md5} {category}: {count_num} finding(s)",
                },
            })

    return {
        "level": level,
        "decision": decision,
        "risk_signals": findings,
        "source": "qianxin-md5",
        "qianxin": {
            "mode": "md5-query",
            "bundle_md5": bundle_md5,
            "verdict": summary.get("verdict", result.get("verdict", "UNKNOWN")),
            "level": qx_level,
            "recommended_action": summary.get("recommended_action", result.get("recommended_action", "")),
            "total_findings": summary.get("total_findings", result.get("total_findings", 0)),
            "by_severity": by_severity,
            "by_category": by_category,
            "confidence": summary.get("confidence", result.get("confidence", 0)),
            "summary": summary.get("summary", result.get("summary", "")),
        },
        "dependencies": {"added": [], "removed": [], "changed": []},
        "network": {"domains": [], "ips": [], "evidence_files": []},
    }


def scan_risk(
    skill_dir: Path,
    risk_rules: list[tuple[str, str, list[str]]] | None = None,
    context_profiles: dict | None = None,
    skill_description: str = "",
    use_qianxin: bool = True,
    workspace_skills_dir: Path | None = None,
) -> dict:
    """Scan a skill directory for risk signals.

    Strategy: try QianXin MD5 intel first, but keep it on a tight budget so
    cron jobs stay responsive. If token is unset, or remote intelligence is
    unavailable, fall back to local rule-based scanning immediately.
    """
    # Try QianXin MD5 intel first, but keep remote intelligence best-effort and fast.
    if use_qianxin:
        for attempt in range(1, QIANXIN_MAX_RETRIES + 1):
            qx_result = qianxin_scan(skill_dir, workspace_skills_dir=workspace_skills_dir)
            if qx_result is not None:
                return qx_result
            if attempt < QIANXIN_MAX_RETRIES:
                time.sleep(QIANXIN_RETRY_DELAY)

    # Fallback: local rule-based scanning after the remote fast-path misses.
    if risk_rules is None:
        risk_rules, context_profiles = load_risk_rules()
    if context_profiles is None:
        context_profiles = {}

    findings = []
    domains: set[str] = set()

    def extract_domains(text: str) -> None:
        for proto in ("http://", "https://"):
            start = 0
            while True:
                i = text.find(proto, start)
                if i == -1:
                    break
                j = i + len(proto)
                k = j
                while k < len(text) and text[k] not in "/\"' \n\r\t)":
                    k += 1
                host = text[j:k]
                if host and len(host) < 200:
                    domains.add(host)
                start = k

    for p in list_files(skill_dir):
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip", ".tar", ".gz", ".bin"}:
            continue
        rel = str(p.relative_to(skill_dir)).replace(os.sep, "/")
        file_context = classify_file_context(skill_dir, p)
        # Skip low-signal config/rule files from high-risk string scanning.
        if rel == "config/risk-rules.json" or rel.endswith("/risk-rules.json") or is_low_signal_file(skill_dir, p):
            continue
        if p.stat().st_size > 1_500_000:
            continue
        text = safe_read_text(p)
        if not text:
            continue
        extract_domains(text)
        for rule_id, severity, needles in risk_rules:
            for n in needles:
                if n in text:
                    hit_context = "real_execution"
                    effective_severity = severity
                    if file_context != "code":
                        hit_context = file_context
                        if severity in {"high", "extreme"}:
                            effective_severity = "medium"
                    elif p.name == "skills_audit.py":
                        quoted = f'"{n}"' in text or f"'{n}'" in text
                        if quoted:
                            hit_context = "rule_sample"
                            if severity in {"high", "extreme"}:
                                effective_severity = "medium"
                    findings.append(
                        {
                            "rule_id": rule_id,
                            "severity": effective_severity,
                            "context": hit_context,
                            "evidence": {
                                "file": str(p.relative_to(skill_dir)),
                                "line": None,
                                "snippet": n,
                            },
                        }
                    )
                    break

    # Apply context-aware scoring based on skill description
    matched_profiles = match_context_profiles(skill_description, context_profiles)
    if matched_profiles:
        findings = apply_context_scoring(findings, context_profiles, matched_profiles)

    # Also try to extract description from SKILL.md frontmatter if not provided
    if not matched_profiles and not skill_description:
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            text = safe_read_text(skill_md, max_bytes=2000)
            # Simple frontmatter extraction
            if text.startswith("---"):
                end = text.find("---", 3)
                if end > 0:
                    fm = text[3:end]
                    for line in fm.splitlines():
                        if line.strip().startswith("description:"):
                            desc = line.split(":", 1)[1].strip().strip("'\"")
                            matched_profiles = match_context_profiles(desc, context_profiles)
                            if matched_profiles:
                                findings = apply_context_scoring(findings, context_profiles, matched_profiles)
                            break

    level = "low"
    if any(f["severity"] == "extreme" for f in findings):
        level = "extreme"
    elif any(f["severity"] == "high" for f in findings):
        level = "high"
    elif any(f["severity"] == "medium" for f in findings):
        level = "medium"

    decision = {
        "low": "allow",
        "medium": "allow_with_caution",
        "high": "require_sandbox",
        "extreme": "deny",
    }.get(level, "allow_with_caution")

    return {
        "level": level,
        "decision": decision,
        "risk_signals": findings[:200],
        "source": "local",
        "dependencies": {"added": [], "removed": [], "changed": []},
        "network": {
            "domains": sorted(domains)[:200],
            "ips": [],
            "evidence_files": [],
        },
    }


# ---------------------------------------------------------------------------
# Tree hashing and file manifest
# ---------------------------------------------------------------------------

def compute_tree_sha256(skill_dir: Path) -> str:
    h = hashlib.sha256()
    for f in list_files(skill_dir):
        rel = str(f.relative_to(skill_dir))
        h.update(rel.encode())
        try:
            st = f.stat()
            h.update(str(st.st_size).encode())
        except Exception:
            h.update(b"0")
        sh = sha256_file(f) or ""
        h.update(sh.encode())
    return h.hexdigest()


def build_file_manifest(skill_dir: Path) -> dict[str, str]:
    """Return {relative_path: sha256} for all files in skill_dir."""
    manifest: dict[str, str] = {}
    for f in list_files(skill_dir):
        rel = str(f.relative_to(skill_dir))
        manifest[rel] = sha256_file(f) or ""
    return manifest


# ---------------------------------------------------------------------------
# Semantic analysis (LLM-style heuristic)
# ---------------------------------------------------------------------------

SEMANTIC_PATTERNS_PATH = Path(__file__).resolve().parent.parent / "config" / "semantic-patterns.json"


def load_semantic_patterns() -> tuple[list[tuple[str, str, list[str]]], list[tuple[str, list[str]]], list[str]]:
    data = load_json(SEMANTIC_PATTERNS_PATH) or {}
    dangerous = []
    for item in data.get("dangerous_patterns", []):
        if not isinstance(item, dict):
            continue
        dangerous.append((
            str(item.get("name", "")),
            str(item.get("severity", "medium")),
            [str(x) for x in item.get("needles", [])],
        ))
    capabilities = []
    for item in data.get("capability_patterns", []):
        if not isinstance(item, dict):
            continue
        capabilities.append((
            str(item.get("tag", "")),
            [str(x) for x in item.get("needles", [])],
        ))
    shell_markers = [str(x) for x in data.get("shell_markers", [])]
    return dangerous, capabilities, shell_markers

HIGH_CONFIDENCE_CODE_EXTS = {".py", ".sh", ".bash", ".zsh", ".js", ".ts", ".mjs", ".cjs"}
LOW_SIGNAL_FILES = {
    "SKILL.md",
    "SKILL_zh-CN.md",
    "log-template.json",
    "config/risk-rules.json",
    "config/semantic-patterns.json",
}


def is_low_signal_file(skill_dir: Path, p: Path) -> bool:
    rel = str(p.relative_to(skill_dir)).replace(os.sep, "/")
    return rel in LOW_SIGNAL_FILES


def classify_file_context(skill_dir: Path, p: Path) -> str:
    rel = str(p.relative_to(skill_dir)).replace(os.sep, "/")
    if rel in {"SKILL.md", "SKILL_zh-CN.md", "README.md", "scripts/README.md", "templates/README.md"}:
        return "doc_example"
    if rel.startswith("config/") or rel == "log-template.json":
        return "config_sample"
    if p.suffix.lower() in HIGH_CONFIDENCE_CODE_EXTS:
        return "code"
    return "other"


def _severity_rank(level: str) -> int:
    return {"low": 1, "medium": 2, "high": 3, "extreme": 4}.get(level, 1)


def _semantic_real_execution_signals(rel: str, text: str, shell_markers: list[str]) -> list[dict]:
    signals = []

    # Distinguish controlled local execution from risky shell/dynamic execution.
    controlled_subprocess_needles = [
        "subprocess.run(argv",
        "subprocess.run(argv,",
        "subprocess.run([",
        "capture_output=True",
        "text=True",
    ]
    risky_exec_checks = [
        ("subprocess_shell", "high", ["shell=True", "subprocess.Popen(", "subprocess.call("]),
        ("os_system", "high", ["os.system("]),
        ("network_fetch", "medium", ["urlopen(", "Request(", "requests.get(", "requests.post("]),
        ("file_write", "medium", ["write_text(", ".open(\"a\"", ".open(\"w\"", "open(\"a\"", "open(\"w\""]),
    ]

    if "subprocess.run(" in text:
        controlled = any(n in text for n in controlled_subprocess_needles) and "shell=True" not in text
        signals.append({
            "name": "subprocess_controlled" if controlled else "subprocess_shell",
            "severity": "medium" if controlled else "high",
            "file": rel,
            "snippet": "subprocess.run(",
        })

    for name, severity, needles in risky_exec_checks:
        for needle in needles:
            if needle in text:
                if needle == "subprocess.Popen(" and "shell=True" not in text:
                    continue
                signals.append({
                    "name": name,
                    "severity": severity,
                    "file": rel,
                    "snippet": needle,
                })
                break

    # Shell-pipe execution should only count when it appears as command content, not as a bare rule sample.
    medium_markers = set(load_json(SEMANTIC_PATTERNS_PATH).get("medium_shell_markers", ["base64 -d"]))
    for marker in shell_markers:
        quoted = f'"{marker}"' in text or f"'{marker}'" in text
        if marker in text and not quoted:
            signals.append({
                "name": "shell_payload_pattern",
                "severity": "medium" if marker in medium_markers else "high",
                "file": rel,
                "snippet": marker,
            })

    return signals


def semantic_analyze_skill(skill_dir: Path) -> dict:
    dangerous_patterns, capability_patterns, shell_markers = load_semantic_patterns()
    dangerous_signals = []
    capability_tags: set[str] = set()
    malicious_indicators: list[dict] = []

    for p in list_files(skill_dir):
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip", ".tar", ".gz", ".bin"}:
            continue
        if p.stat().st_size > 1_500_000:
            continue
        text = safe_read_text(p)
        if not text:
            continue
        rel = str(p.relative_to(skill_dir)).replace(os.sep, "/")
        low_signal = is_low_signal_file(skill_dir, p)
        code_weight = p.suffix.lower() in HIGH_CONFIDENCE_CODE_EXTS and not low_signal

        if code_weight:
            if p.name == "skills_audit.py":
                dangerous_signals.extend(_semantic_real_execution_signals(rel, text, shell_markers))
            else:
                for name, severity, needles in dangerous_patterns:
                    for needle in needles:
                        if needle in text:
                            dangerous_signals.append({
                                "name": name,
                                "severity": severity,
                                "file": rel,
                                "snippet": needle,
                            })
                            if severity in {"high", "extreme"} and name not in {"subprocess_controlled", "network_fetch", "file_write"}:
                                malicious_indicators.append({
                                    "name": name,
                                    "severity": severity,
                                    "file": rel,
                                    "snippet": needle,
                                })
                            break

        for tag, needles in capability_patterns:
            if any(needle in text for needle in needles):
                capability_tags.add(tag)

    dangerous_signals = sorted(
        dangerous_signals,
        key=lambda x: (_severity_rank(x.get("severity", "low")) * -1, x.get("file", ""), x.get("name", ""))
    )[:50]
    capability_list = sorted(capability_tags)
    malicious_indicators = sorted(
        malicious_indicators,
        key=lambda x: (_severity_rank(x.get("severity", "low")) * -1, x.get("file", ""), x.get("name", ""))
    )[:20]

    capability_risk = "low"
    if len(capability_list) >= 5:
        capability_risk = "medium"
    elif len(capability_list) >= 3:
        capability_risk = "low"

    intent_risk = "low"
    if any(s["severity"] == "extreme" for s in malicious_indicators):
        intent_risk = "extreme"
    elif any(s["severity"] == "high" for s in malicious_indicators):
        intent_risk = "high"
    elif any(s["severity"] == "medium" for s in malicious_indicators):
        intent_risk = "medium"

    # Intent is the primary dimension. Capability is secondary unless intent is absent.
    if intent_risk == "extreme":
        level = "extreme"
    elif intent_risk == "high":
        level = "high"
    elif intent_risk == "medium":
        level = "medium"
    else:
        level = capability_risk

    decision = {
        "low": "allow",
        "medium": "allow_with_caution",
        "high": "require_sandbox",
        "extreme": "deny",
    }.get(level, "allow_with_caution")

    danger_summary = "未检测到明显危险函数" if not dangerous_signals else f"检测到 {len(dangerous_signals)} 个潜在危险函数/模式"
    capability_summary = "未识别出明显功能特征" if not capability_list else f"识别到功能标签：{', '.join(capability_list)}"
    reason = (
        f"以语义意图为主判维度：恶意倾向风险={intent_risk}，能力风险={capability_risk}；"
        f"danger={len(dangerous_signals)}，malicious={len(malicious_indicators)}，"
        f"capabilities={','.join(capability_list) or 'none'}"
    )

    status = "ok"

    return {
        "engine": "local-llm-style-heuristic",
        "status": status,
        "dangerous_functions": {
            "summary": danger_summary,
            "signals": dangerous_signals,
        },
        "capability_analysis": {
            "summary": capability_summary,
            "tags": capability_list,
        },
        "intent_analysis": {
            "summary": "未发现明显恶意意图" if not malicious_indicators else f"发现 {len(malicious_indicators)} 个高风险恶意倾向信号",
            "signals": malicious_indicators,
            "risk": intent_risk
        },
        "result": {
            "level": level,
            "decision": decision,
            "reason": reason,
        },
    }


def diff_file_manifests(
    prev_files: dict[str, str], now_files: dict[str, str]
) -> tuple[list[str], list[str], list[str]]:
    """Return (files_added, files_removed, files_changed)."""
    prev_set = set(prev_files.keys())
    now_set = set(now_files.keys())
    added = sorted(now_set - prev_set)
    removed = sorted(prev_set - now_set)
    changed = sorted(
        k for k in (prev_set & now_set) if prev_files[k] != now_files[k]
    )
    return added, removed, changed


# ---------------------------------------------------------------------------
# Git snapshots for content diff
# ---------------------------------------------------------------------------

def ensure_snapshots_repo() -> Path:
    """Initialize git repo at SNAPSHOTS_DIR if needed. Return the path."""
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    git_dir = SNAPSHOTS_DIR / ".git"
    if not git_dir.exists():
        run_cmd(["git", "init"], cwd=SNAPSHOTS_DIR)
        run_cmd(["git", "config", "user.email", "skills-audit@openclaw.local"], cwd=SNAPSHOTS_DIR)
        run_cmd(["git", "config", "user.name", "skills-audit"], cwd=SNAPSHOTS_DIR)
    return SNAPSHOTS_DIR


def sync_and_commit(skills_dir: Path, timestamp: str) -> dict | None:
    """
    Rsync skills_dir into snapshots, commit, and return diff info.
    Returns None if no changes or git not available.
    """
    repo = ensure_snapshots_repo()
    dest = repo / "skills"

    # rsync: mirror skills_dir to snapshots/skills, excluding .git and __pycache__
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        skills_dir,
        dest,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )

    # git add + commit
    run_cmd(["git", "add", "-A"], cwd=repo)

    # Check if there are staged changes
    rc, status_out, _ = run_cmd(["git", "status", "--porcelain"], cwd=repo)
    if not status_out:
        return None  # no changes

    commit_msg = f"scan: {timestamp}"
    run_cmd(["git", "commit", "-m", commit_msg, "--allow-empty"], cwd=repo)

    # Get commit hash
    _, commit_hash, _ = run_cmd(["git", "rev-parse", "HEAD"], cwd=repo)
    _, parent_hash, _ = run_cmd(["git", "rev-parse", "HEAD~1"], cwd=repo)

    # Get diff stat
    _, diff_stat, _ = run_cmd(["git", "diff", "--stat", "HEAD~1", "HEAD"], cwd=repo)
    _, diff_numstat, _ = run_cmd(["git", "diff", "--numstat", "HEAD~1", "HEAD"], cwd=repo)
    _, diff_full, _ = run_cmd(["git", "diff", "HEAD~1", "HEAD"], cwd=repo)

    stat_entries = []
    total_added = 0
    total_deleted = 0
    for line in diff_numstat.splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            add_str, del_str, filepath = parts
            a = int(add_str) if add_str != "-" else 0
            d = int(del_str) if del_str != "-" else 0
            total_added += a
            total_deleted += d
            # Determine status
            status = "modified"
            if a > 0 and d == 0:
                # could be new file, check
                rc2, _, _ = run_cmd(["git", "cat-file", "-e", f"HEAD~1:{filepath}"], cwd=repo)
                if rc2 != 0:
                    status = "added"
            elif a == 0 and d > 0:
                rc2, _, _ = run_cmd(["git", "cat-file", "-e", f"HEAD:{filepath}"], cwd=repo)
                if rc2 != 0:
                    status = "deleted"
            stat_entries.append({
                "file": filepath,
                "added": a,
                "deleted": d,
                "status": status,
            })

    full_diff_lines = len(diff_full.splitlines()) if diff_full else 0

    return {
        "commit": commit_hash or "",
        "parent_commit": parent_hash or "",
        "stat": stat_entries,
        "total_added": total_added,
        "total_deleted": total_deleted,
        "total_files_changed": len(stat_entries),
        "full_diff_lines": full_diff_lines,
    }


# ---------------------------------------------------------------------------
# Baseline (approved skills)
# ---------------------------------------------------------------------------

def load_baseline() -> dict:
    if not BASELINE_PATH.exists():
        return {"approved": {}}
    try:
        data = json.loads(BASELINE_PATH.read_text("utf-8"))
        if "approved" not in data:
            data["approved"] = {}
        return data
    except Exception:
        return {"approved": {}}


def save_baseline(baseline: dict) -> None:
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", "utf-8")


def is_approved(baseline: dict, skill_name: str, tree_sha256: str) -> bool:
    """Check if a skill is approved and its tree hash still matches."""
    entry = baseline.get("approved", {}).get(skill_name)
    if not entry:
        return False
    return entry.get("tree_sha256") == tree_sha256


# ---------------------------------------------------------------------------
# Template / NDJSON / state
# ---------------------------------------------------------------------------

def load_template(workspace_dir: Path) -> dict:
    tpl_path = workspace_dir / "skills" / "skills-audit" / "log-template.json"
    tpl = load_json(tpl_path)
    if not isinstance(tpl, dict):
        raise RuntimeError(f"template not found or invalid json: {tpl_path}")
    return tpl


def append_ndjson(path: Path, rec: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"skills": {}}
    try:
        return json.loads(path.read_text("utf-8"))
    except Exception:
        return {"skills": {}}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", "utf-8")


def skill_meta(skill_dir: Path) -> dict:
    meta = load_json(skill_dir / "_meta.json") or {}
    owner_id = meta.get("ownerId") or meta.get("owner_id") or ""
    slug = meta.get("slug") or skill_dir.name
    version = meta.get("version") or "unknown"
    return {"owner_id": owner_id, "slug": slug, "version": version, "raw": meta}


def tool_versions() -> dict:
    rc, out, _ = run_cmd(["openclaw", "--version"])
    openclaw_ver = out.splitlines()[0] if rc == 0 and out else "unknown"

    sh_rc, sh_out, _ = run_cmd(["skillhub", "--version"])
    skillhub_ver = sh_out.splitlines()[0] if sh_rc == 0 and sh_out else "unknown"

    ch_rc, ch_out, _ = run_cmd(["clawhub", "--version"])
    clawhub_ver = ch_out.splitlines()[0] if ch_rc == 0 and ch_out else "unknown"

    return {
        "openclaw_version": openclaw_ver,
        "skillhub_version": skillhub_ver,
        "clawhub_cli_version": clawhub_ver,
        "platform": platform.platform(),
    }


def build_record(
    template: dict,
    *,
    action: str,
    result: str,
    meta: dict,
    install_path: str | None,
    workspace_dir: str,
    sha256: str | None,
    before_tree: str | None,
    after_tree: str | None,
    who: str,
    channel: str,
    risk: dict | None,
    semantic_analysis: dict | None = None,
    semantic_analysis_required: bool = True,
    diff_info: dict | None = None,
    file_diff: dict | None = None,
    approved: bool = False,
) -> dict:
    rec = copy.deepcopy(template)

    rec["time"] = iso_utc_now()
    rec["log_id"] = str(uuid.uuid4())
    rec["action"] = action
    rec["result"] = result

    rec["owner_id"] = meta.get("owner_id", "")
    rec["slug"] = meta.get("slug", "")
    rec["version"] = meta.get("version", "unknown")
    rec["sha256"] = sha256   # Primary integrity field (v2.0)

    # observed
    obs = rec.get("observed") or {}
    tv = tool_versions()
    obs["install_path"] = install_path
    obs["workspace_dir"] = workspace_dir
    obs["openclaw_version"] = tv["openclaw_version"]
    obs["skillhub_version"] = tv["skillhub_version"]
    obs["clawhub_cli_version"] = tv["clawhub_cli_version"]
    rec["observed"] = obs

    # operator
    op = rec.get("operator") or {}
    op["who"] = who
    op["channel"] = channel
    rec["operator"] = op

    # risk
    rec["risk"] = risk

    # semantic analysis (mandatory)
    rec["semantic_analysis_required"] = semantic_analysis_required
    rec["semantic_analysis"] = semantic_analysis

    # diff (v2.0)
    rec["diff"] = diff_info

    # file-level changes (v2.0)
    rec["file_changes"] = file_diff

    # baseline approval status
    rec["approved"] = approved

    # notes
    rec["notes"] = (
        f"auto-scan. before_tree_sha256={before_tree or 'null'} "
        f"after_tree_sha256={after_tree or 'null'}. "
        f"platform={tv['platform']}"
    )

    return rec


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_init(args: argparse.Namespace) -> int:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_PATH.exists():
        save_state(STATE_PATH, {"skills": {}, "created_at": iso_utc_now()})
    if not LOG_PATH.exists():
        LOG_PATH.write_text("", "utf-8")
    if not BASELINE_PATH.exists():
        save_baseline({"approved": {}})
    ensure_snapshots_repo()
    print(f"Initialized logs at {LOG_PATH}")
    print(f"Initialized state at {STATE_PATH}")
    print(f"Initialized baseline at {BASELINE_PATH}")
    print(f"Initialized snapshots repo at {SNAPSHOTS_DIR}")
    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    workspace_dir = Path(args.workspace).resolve()
    skills_dir = workspace_dir / "skills"

    template = load_template(workspace_dir)
    baseline = load_baseline()
    risk_rules, context_profiles = load_risk_rules(workspace_dir)

    prev = load_state(STATE_PATH).get("skills", {})
    now = {}

    if skills_dir.exists():
        for p in skills_dir.iterdir():
            if not p.is_dir():
                continue
            if p.name.startswith("."):
                continue
            meta = skill_meta(p)
            sha256 = sha256_file(p / "SKILL.md") if (p / "SKILL.md").exists() else None
            tree = compute_tree_sha256(p)
            files = build_file_manifest(p)
            now[p.name] = {
                "meta": meta,
                "install_path": str(p),
                "sha256": sha256,
                "tree_sha256": tree,
                "files": files,
            }

    prev_keys = set(prev.keys())
    now_keys = set(now.keys())

    added = sorted(now_keys - prev_keys)
    removed = sorted(prev_keys - now_keys)
    common = sorted(now_keys & prev_keys)
    changed = [k for k in common if prev[k].get("tree_sha256") != now[k].get("tree_sha256")]

    # Compute file-level diffs for changed skills
    file_diffs: dict[str, dict] = {}
    for k in changed:
        prev_files = prev[k].get("files", {})
        now_files = now[k].get("files", {})
        fa, fr, fc = diff_file_manifests(prev_files, now_files)
        file_diffs[k] = {
            "files_added": fa,
            "files_removed": fr,
            "files_changed": fc,
        }

    # Git snapshot for content diff
    diff_info = None
    if skills_dir.exists() and (added or changed or removed):
        timestamp = iso_utc_now()
        diff_info = sync_and_commit(skills_dir, timestamp)

    # Emit logs
    for k in added:
        entry = now[k]
        approved = is_approved(baseline, k, entry["tree_sha256"])
        risk = scan_risk(Path(entry["install_path"]), risk_rules, context_profiles, workspace_skills_dir=skills_dir)
        semantic_analysis = semantic_analyze_skill(Path(entry["install_path"]))
        if not semantic_analysis or not isinstance(semantic_analysis, dict) or not semantic_analysis.get("result"):
            raise RuntimeError(f"semantic analysis is mandatory but missing for skill: {k}")
        rec = build_record(
            template,
            action="scan-detected",
            result="success",
            meta=entry["meta"],
            install_path=entry["install_path"],
            workspace_dir=str(workspace_dir),
            sha256=entry["sha256"],
            before_tree=None,
            after_tree=entry["tree_sha256"],
            who=args.who,
            channel=args.channel,
            risk=risk,
            semantic_analysis=semantic_analysis,
            semantic_analysis_required=True,
            diff_info=diff_info,
            approved=approved,
        )
        append_ndjson(LOG_PATH, rec)

    for k in changed:
        entry = now[k]
        # Change breaks baseline
        approved = False
        risk = scan_risk(Path(entry["install_path"]), risk_rules, context_profiles, workspace_skills_dir=skills_dir)
        semantic_analysis = semantic_analyze_skill(Path(entry["install_path"]))
        if not semantic_analysis or not isinstance(semantic_analysis, dict) or not semantic_analysis.get("result"):
            raise RuntimeError(f"semantic analysis is mandatory but missing for skill: {k}")
        rec = build_record(
            template,
            action="scan-detected",
            result="success",
            meta=entry["meta"],
            install_path=entry["install_path"],
            workspace_dir=str(workspace_dir),
            sha256=entry["sha256"],
            before_tree=prev[k].get("tree_sha256"),
            after_tree=entry["tree_sha256"],
            who=args.who,
            channel=args.channel,
            risk=risk,
            semantic_analysis=semantic_analysis,
            semantic_analysis_required=True,
            diff_info=diff_info,
            file_diff=file_diffs.get(k),
            approved=approved,
        )
        append_ndjson(LOG_PATH, rec)

    for k in removed:
        entry = prev[k]
        meta = entry.get("meta") or {
            "owner_id": entry.get("owner_id", ""),
            "slug": entry.get("slug", k),
            "version": entry.get("version", "unknown"),
        }
        rec = build_record(
            template,
            action="scan-detected",
            result="success",
            meta=meta,
            install_path=None,
            workspace_dir=str(workspace_dir),
            sha256=entry.get("sha256"),
            before_tree=entry.get("tree_sha256"),
            after_tree=None,
            who=args.who,
            channel=args.channel,
            risk=None,
            semantic_analysis=None,
            semantic_analysis_required=False,
            diff_info=diff_info,
            approved=False,
        )
        append_ndjson(LOG_PATH, rec)

    # Save state
    save_state(
        STATE_PATH,
        {
            "updated_at": iso_utc_now(),
            "skills": now,
        },
    )

    print(
        json.dumps(
            {
                "added": added,
                "changed": changed,
                "removed": removed,
                "file_diffs": file_diffs,
                "diff": {
                    "commit": diff_info["commit"] if diff_info else None,
                    "total_added": diff_info["total_added"] if diff_info else 0,
                    "total_deleted": diff_info["total_deleted"] if diff_info else 0,
                    "total_files_changed": diff_info["total_files_changed"] if diff_info else 0,
                },
                "log_path": str(LOG_PATH),
                "state_path": str(STATE_PATH),
            },
            ensure_ascii=False,
        )
    )

    return 0


def cmd_show(args: argparse.Namespace) -> int:
    """Show a human-readable change summary for a skill (or all changed skills)."""
    repo = SNAPSHOTS_DIR
    if not (repo / ".git").exists():
        print("没有找到快照记录。请先执行一次 scan。", file=sys.stderr)
        return 1

    # Determine which commit range to diff
    commit_range = args.commit_range or "HEAD~1..HEAD"

    # If a specific skill is requested, scope the diff
    path_filter = []
    if args.skill:
        path_filter = ["--", f"skills/{args.skill}/"]

    # Get numstat for structured data
    cmd_numstat = ["git", "-C", str(repo), "diff", "--numstat"] + commit_range.split("..") + path_filter
    rc, numstat, _ = run_cmd(cmd_numstat, cwd=repo)
    if rc != 0 or not numstat.strip():
        if args.skill:
            print(f"'{args.skill}' 在最近一次扫描中没有变更。")
        else:
            print("最近一次扫描没有检测到任何变更。")
        return 0

    # Get the actual diff content
    cmd_diff = ["git", "-C", str(repo), "diff"] + commit_range.split("..") + path_filter
    _, diff_content, _ = run_cmd(cmd_diff, cwd=repo)

    # Parse numstat into per-skill groups
    skill_changes: dict[str, list[dict]] = {}
    for line in numstat.splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        add_str, del_str, filepath = parts
        a = int(add_str) if add_str != "-" else 0
        d = int(del_str) if del_str != "-" else 0

        # Extract skill name from path: skills/<name>/...
        if filepath.startswith("skills/"):
            rest = filepath[len("skills/"):]
            skill_name = rest.split("/")[0] if "/" in rest else rest
            rel_path = rest[len(skill_name)+1:] if "/" in rest else rest
        else:
            skill_name = "(other)"
            rel_path = filepath

        if skill_name not in skill_changes:
            skill_changes[skill_name] = []
        skill_changes[skill_name].append({"file": rel_path, "added": a, "deleted": d})

    # Parse diff content into per-skill chunks for summary
    # We'll show a human summary + the key changes
    lines_out: list[str] = []

    for skill_name, changes in sorted(skill_changes.items()):
        total_files = len(changes)
        total_added = sum(c["added"] for c in changes)
        total_deleted = sum(c["deleted"] for c in changes)

        lines_out.append(f"📦 {skill_name}")
        lines_out.append(f"   共变更 {total_files} 个文件，新增 {total_added} 行，删除 {total_deleted} 行")
        lines_out.append("")

        # Categorize changes
        major_changes = [c for c in changes if c["added"] + c["deleted"] >= 10]
        minor_changes = [c for c in changes if c["added"] + c["deleted"] < 10]

        if major_changes:
            lines_out.append("   主要变更：")
            for c in major_changes:
                lines_out.append(f"   • {c['file']}（+{c['added']} -{c['deleted']}）")
        if minor_changes:
            lines_out.append("   其他变更：")
            for c in minor_changes:
                lines_out.append(f"   • {c['file']}（+{c['added']} -{c['deleted']}）")
        lines_out.append("")

    # Now extract meaningful content changes from the diff
    # Parse unified diff to generate human-readable descriptions
    if diff_content:
        lines_out.append("─" * 40)
        lines_out.append("📝 具体改动内容：")
        lines_out.append("")

        current_file = None
        hunks: list[dict] = []

        for line in diff_content.splitlines():
            if line.startswith("diff --git"):
                # Save previous file hunks
                if current_file and hunks:
                    _format_file_hunks(lines_out, current_file, hunks, skill_filter=args.skill)
                    hunks = []
                # Extract filename
                parts = line.split(" b/", 1)
                current_file = parts[1] if len(parts) == 2 else None
                # Strip skills/<name>/ prefix for readability
                if current_file and current_file.startswith("skills/"):
                    rest = current_file[len("skills/"):]
                    if "/" in rest:
                        skill_prefix = rest.split("/")[0]
                        current_file = f"[{skill_prefix}] {rest[len(skill_prefix)+1:]}"
            elif line.startswith("@@"):
                hunks.append({"header": line, "added": [], "deleted": []})
            elif hunks:
                if line.startswith("+") and not line.startswith("+++"):
                    hunks[-1]["added"].append(line[1:])
                elif line.startswith("-") and not line.startswith("---"):
                    hunks[-1]["deleted"].append(line[1:])

        # Don't forget last file
        if current_file and hunks:
            _format_file_hunks(lines_out, current_file, hunks, skill_filter=args.skill)

    print("\n".join(lines_out))
    return 0


def _format_file_hunks(
    lines_out: list[str],
    filename: str,
    hunks: list[dict],
    skill_filter: str | None = None,
) -> None:
    """Format hunks of a single file into human-readable lines."""
    lines_out.append(f"   📄 {filename}")

    for hunk in hunks:
        added = hunk["added"]
        deleted = hunk["deleted"]

        if not added and not deleted:
            continue

        # Generate human-readable description
        if added and not deleted:
            # Pure addition
            if len(added) <= 5:
                lines_out.append("      新增内容：")
                for a in added:
                    stripped = a.strip()
                    if stripped:
                        lines_out.append(f"        + {stripped}")
            else:
                lines_out.append(f"      新增 {len(added)} 行内容")
                for a in added[:3]:
                    stripped = a.strip()
                    if stripped:
                        lines_out.append(f"        + {stripped}")
                lines_out.append(f"        ... 另外 {len(added) - 3} 行")
        elif deleted and not added:
            # Pure deletion
            if len(deleted) <= 5:
                lines_out.append("      删除内容：")
                for d in deleted:
                    stripped = d.strip()
                    if stripped:
                        lines_out.append(f"        - {stripped}")
            else:
                lines_out.append(f"      删除 {len(deleted)} 行内容")
                for d in deleted[:3]:
                    stripped = d.strip()
                    if stripped:
                        lines_out.append(f"        - {stripped}")
                lines_out.append(f"        ... 另外 {len(deleted) - 3} 行")
        else:
            # Modification (both added and deleted)
            lines_out.append("      修改内容：")
            # Show pairs where possible
            max_show = min(5, max(len(deleted), len(added)))
            for i in range(min(len(deleted), max_show)):
                stripped = deleted[i].strip()
                if stripped:
                    lines_out.append(f"        - {stripped}")
            for i in range(min(len(added), max_show)):
                stripped = added[i].strip()
                if stripped:
                    lines_out.append(f"        + {stripped}")
            remaining = max(len(added), len(deleted)) - max_show
            if remaining > 0:
                lines_out.append(f"        ... 另外 {remaining} 行")

    lines_out.append("")


def cmd_approve(args: argparse.Namespace) -> int:
    workspace_dir = Path(args.workspace).resolve()
    skills_dir = workspace_dir / "skills"
    state = load_state(STATE_PATH)
    baseline = load_baseline()

    if args.all:
        targets = list(state.get("skills", {}).keys())
    elif args.skill:
        targets = [args.skill]
    else:
        print("Error: specify --skill <name> or --all", file=sys.stderr)
        return 1

    for skill_name in targets:
        skill_state = state.get("skills", {}).get(skill_name)
        if not skill_state:
            print(f"Warning: skill '{skill_name}' not found in state, skipping", file=sys.stderr)
            continue

        rules, profiles = load_risk_rules(Path(args.workspace).resolve())
        risk = scan_risk(Path(skill_state["install_path"]), rules, profiles, workspace_skills_dir=skills_dir) if skill_state.get("install_path") else {}
        baseline["approved"][skill_name] = {
            "tree_sha256": skill_state["tree_sha256"],
            "approved_at": iso_utc_now(),
            "approved_by": args.who,
            "risk_level_at_approval": risk.get("level", "unknown") if risk else "unknown",
        }
        print(f"Approved: {skill_name} (tree_sha256={skill_state['tree_sha256'][:16]}...)")

    save_baseline(baseline)
    return 0


def cmd_baseline(args: argparse.Namespace) -> int:
    baseline = load_baseline()

    if args.revoke:
        if not args.skill:
            print("Error: --revoke requires --skill <name>", file=sys.stderr)
            return 1
        if args.skill in baseline["approved"]:
            del baseline["approved"][args.skill]
            save_baseline(baseline)
            print(f"Revoked approval for: {args.skill}")
        else:
            print(f"Skill '{args.skill}' not in baseline")
        return 0

    if args.list_all:
        approved = baseline.get("approved", {})
        if not approved:
            print("No approved skills in baseline.")
            return 0
        print(f"Approved skills ({len(approved)}):")
        print(f"{'Skill':<30} {'Approved At':<25} {'Risk Level':<12} {'Tree SHA-256 (prefix)'}")
        print("-" * 100)
        for name, info in sorted(approved.items()):
            print(
                f"{name:<30} {info.get('approved_at', '?'):<25} "
                f"{info.get('risk_level_at_approval', '?'):<12} "
                f"{info.get('tree_sha256', '?')[:20]}..."
            )
        return 0

    print("Use --list or --revoke --skill <name>", file=sys.stderr)
    return 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="skills-audit v2.0.0 — audit, diff, and baseline workspace skills"
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    # init
    ap_init = sub.add_parser("init", help="Initialize audit directory")
    ap_init.add_argument("--workspace", default=str(Path.cwd()))

    # scan
    ap_scan = sub.add_parser("scan", help="Scan workspace/skills for changes")
    ap_scan.add_argument("--workspace", default=str(Path.cwd()))
    ap_scan.add_argument("--who", default="cron")
    ap_scan.add_argument("--channel", default="local")

    # show
    ap_show = sub.add_parser("show", help="Show human-readable change summary")
    ap_show.add_argument("--skill", help="Show changes for a specific skill only")
    ap_show.add_argument("--commit-range", dest="commit_range", default="HEAD~1..HEAD",
                         help="Git commit range (default: HEAD~1..HEAD)")

    # approve
    ap_approve = sub.add_parser("approve", help="Approve skill(s) into baseline")
    ap_approve.add_argument("--workspace", default=str(Path.cwd()))
    ap_approve.add_argument("--skill", help="Skill name to approve")
    ap_approve.add_argument("--all", action="store_true", help="Approve all current skills")
    ap_approve.add_argument("--who", default="user")

    # baseline
    ap_baseline = sub.add_parser("baseline", help="Manage baseline approvals")
    ap_baseline.add_argument("--list", dest="list_all", action="store_true", help="List approved skills")
    ap_baseline.add_argument("--revoke", action="store_true", help="Revoke approval")
    ap_baseline.add_argument("--skill", help="Skill name (for --revoke)")

    args = ap.parse_args()

    if args.cmd == "init":
        return cmd_init(args)
    elif args.cmd == "scan":
        return cmd_scan(args)
    elif args.cmd == "show":
        return cmd_show(args)
    elif args.cmd == "approve":
        return cmd_approve(args)
    elif args.cmd == "baseline":
        return cmd_baseline(args)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
