#!/usr/bin/env python3
"""Static security audit for Telegram Mini App projects.

The auditor is intentionally conservative. It finds evidence that should be
reviewed before a Mini App is connected to real bot tokens, BotFather, or public
Telegram channels.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


UTC = dt.timezone.utc

TEXT_EXTENSIONS = {
    "",
    ".cfg",
    ".conf",
    ".css",
    ".env",
    ".example",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}

MAX_FILE_BYTES = 1_000_000

TELEGRAM_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_])(?:bot)?\d{7,12}:[A-Za-z0-9_-]{32,64}(?![A-Za-z0-9_])")
GENERIC_SECRET_ASSIGN_RE = re.compile(
    r"(?i)\b(api[_-]?key|token|secret|password|private[_-]?key)\b\s*[:=]\s*['\"][^'\"\n]{16,}['\"]"
)
URL_WITH_BOT_TOKEN_RE = re.compile(r"https://api\.telegram\.org/bot\d{7,12}:[A-Za-z0-9_-]{32,64}", re.I)
PLACEHOLDER_WORD_RE = re.compile(r"(?i)\b(dummy|example|fake|fixture|placeholder|test[-_ ]?token|your[-_ ]?token)\b")


@dataclass(frozen=True)
class FileInfo:
    path: str
    sha256: str
    bytes: int


@dataclass(frozen=True)
class Finding:
    severity: str
    decision_impact: str
    rule_id: str
    file: str
    line: int
    evidence: str
    recommendation: str


@dataclass
class Signals:
    telegram_webapp_client: bool = False
    initdata_client: bool = False
    initdata_server_reference: bool = False
    initdata_hmac_validation: bool = False
    constant_time_compare: bool = False
    auth_freshness_check: bool = False
    insecure_initdata_bypass: bool = False
    admin_endpoint: bool = False
    admin_guard: bool = False
    cors_wildcard: bool = False
    cors_credentials: bool = False
    contact_policy_client: bool = False
    contact_policy_server: bool = False
    health_endpoint: bool = False
    https_launch_doc: bool = False


def now_iso() -> str:
    return dt.datetime.now(UTC).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rel_path(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace(os.sep, "/")


def iter_text_files(root: Path) -> Iterable[Tuple[Path, str, bytes]]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            if path.is_symlink() or path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            try:
                raw = path.read_bytes()
            except OSError:
                continue
            if len(raw) > MAX_FILE_BYTES:
                continue
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    text = raw.decode("utf-8", errors="replace")
                except Exception:
                    continue
            yield path, text, raw


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def excerpt(text: str, start: int, end: int, limit: int = 180) -> str:
    left = max(0, start - 60)
    right = min(len(text), end + 80)
    out = " ".join(text[left:right].split())
    if len(out) > limit:
        out = out[: limit - 1].rstrip() + "..."
    return out


def is_test_path(rel: str) -> bool:
    parts = set(rel.lower().split("/"))
    base = rel.lower().rsplit("/", 1)[-1]
    return (
        "test" in parts
        or "tests" in parts
        or base.startswith("test_")
        or "_test." in base
        or rel.lower().endswith((".test.js", ".test.ts", ".spec.js", ".spec.ts"))
    )


def is_probable_server_file(rel: str, text: str) -> bool:
    lower_rel = rel.lower()
    lower_text = text.lower()
    if lower_rel.endswith(".py"):
        return True
    if any(part in lower_rel.split("/") for part in ("server", "api", "functions", "routes", "backend")):
        return True
    if lower_rel.endswith((".js", ".ts", ".mjs")) and any(
        marker in lower_text
        for marker in (
            "express(",
            "fastify(",
            "app.post",
            "app.get",
            "router.post",
            "router.get",
            "createapp(",
            "fastapi(",
        )
    ):
        return True
    return False


def token_looks_placeholder(token: str, surrounding_text: str, rel: str) -> bool:
    if PLACEHOLDER_WORD_RE.search(surrounding_text):
        return True
    if is_test_path(rel):
        return True
    if token.startswith("1234567:") or token.startswith("bot1234567:"):
        return True
    suffix = token.split(":", 1)[-1]
    return suffix in {
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    }


def add_finding(
    findings: List[Finding],
    *,
    severity: str,
    decision_impact: str,
    rule_id: str,
    file: str,
    line: int = 1,
    evidence: str,
    recommendation: str,
) -> None:
    key = (rule_id, file, line)
    for existing in findings:
        if (existing.rule_id, existing.file, existing.line) == key:
            return
    findings.append(
        Finding(
            severity=severity,
            decision_impact=decision_impact,
            rule_id=rule_id,
            file=file,
            line=line,
            evidence=evidence,
            recommendation=recommendation,
        )
    )


def update_signals(signals: Signals, rel: str, text: str) -> None:
    lower = text.lower()
    is_server = is_probable_server_file(rel, text)
    if "telegram-web-app.js" in lower or "telegram.webapp" in lower or "telegram.webapp" in text:
        signals.telegram_webapp_client = True
    if "initdata" in lower:
        if rel.endswith((".html", ".js", ".jsx", ".ts", ".tsx", ".mjs")):
            signals.initdata_client = True
        if is_server:
            signals.initdata_server_reference = True
    if "webappdata" in lower and "hmac" in lower and "sha256" in lower:
        signals.initdata_hmac_validation = True
    if "compare_digest" in lower or "timingsafeequal" in lower or "crypto.timingSafeEqual" in text:
        signals.constant_time_compare = True
    if "auth_date" in lower and ("max_age" in lower or "too old" in lower or "fresh" in lower):
        signals.auth_freshness_check = True
    if "insecure-skip-initdata-check" in lower or "skip initdata" in lower or "skip-initdata" in lower:
        signals.insecure_initdata_bypass = True
    if "/api/admin" in lower or "x-admin-key" in lower or "admin_key" in lower:
        signals.admin_endpoint = True
    if is_server and ("x-admin-key" in lower or "admin_key" in lower or "admin-key" in lower):
        signals.admin_guard = True
    if "allow_origins=[\"*\"]" in lower or "allow_origins = [\"*\"]" in lower or "cors_origins == \"*\"" in lower:
        signals.cors_wildcard = True
    if "allow_credentials=true" in lower or "allow_credentials = true" in lower:
        signals.cors_credentials = True
    if "emailre" in lower or "phone_re" in lower or "handlere" in lower or "brief_contains_email" in lower:
        if rel.endswith((".html", ".js", ".jsx", ".ts", ".tsx", ".mjs")) and not is_server:
            signals.contact_policy_client = True
        if is_server:
            signals.contact_policy_server = True
    if "/healthz" in lower or "healthz" in lower:
        signals.health_endpoint = True
    if "https" in lower and ("botfather" in lower or "mini app" in lower or "webapp" in lower or "tunnel" in lower):
        signals.https_launch_doc = True


def scan_text_file(root: Path, path: Path, text: str, findings: List[Finding], signals: Signals) -> None:
    rel = rel_path(path, root)
    update_signals(signals, rel, text)

    for regex, rule_id in (
        (TELEGRAM_TOKEN_RE, "hardcoded-telegram-token"),
        (URL_WITH_BOT_TOKEN_RE, "telegram-api-url-with-token"),
    ):
        for match in regex.finditer(text):
            token_text = match.group(0)
            ev = excerpt(text, match.start(), match.end())
            if token_looks_placeholder(token_text, ev, rel):
                add_finding(
                    findings,
                    severity="low",
                    decision_impact="review",
                    rule_id="placeholder-telegram-token",
                    file=rel,
                    line=line_number(text, match.start()),
                    evidence=ev,
                    recommendation="Keep placeholder tokens visibly fake and out of production launch commands.",
                )
                break
            add_finding(
                findings,
                severity="critical",
                decision_impact="block",
                rule_id=rule_id,
                file=rel,
                line=line_number(text, match.start()),
                evidence=ev,
                recommendation="Remove committed token material, rotate any real token, and load credentials from environment or secret storage.",
            )
            break

    for match in GENERIC_SECRET_ASSIGN_RE.finditer(text):
        if ".example" in rel or rel.endswith(".md") or is_test_path(rel):
            continue
        add_finding(
            findings,
            severity="high",
            decision_impact="review",
            rule_id="possible-hardcoded-secret",
            file=rel,
            line=line_number(text, match.start()),
            evidence=excerpt(text, match.start(), match.end()),
            recommendation="Verify this is not a real secret. Prefer environment variables or secret storage.",
        )
        break

    if "innerhtml" in text.lower():
        safe_markers = ("escapeHtml", "sanitize", "DOMPurify", "mdToHtml(cleaned)", "mdToHtml(")
        if not any(marker in text for marker in safe_markers):
            idx = text.lower().find("innerhtml")
            add_finding(
                findings,
                severity="medium",
                decision_impact="review",
                rule_id="unsafe-innerhtml",
                file=rel,
                line=line_number(text, idx),
                evidence=excerpt(text, idx, idx + len("innerHTML")),
                recommendation="Confirm all content assigned to innerHTML is escaped or sanitized.",
            )

    if "x-frame-options" in text.lower() and ("deny" in text.lower() or "sameorigin" in text.lower()):
        idx = text.lower().find("x-frame-options")
        add_finding(
            findings,
            severity="medium",
            decision_impact="review",
            rule_id="telegram-embedding-frame-header",
            file=rel,
            line=line_number(text, idx),
            evidence=excerpt(text, idx, idx + len("x-frame-options")),
            recommendation="Telegram Mini Apps must be embeddable by Telegram clients. Verify frame headers do not break launch.",
        )

    if "frame-ancestors" in text.lower() and "telegram" not in text.lower():
        idx = text.lower().find("frame-ancestors")
        add_finding(
            findings,
            severity="medium",
            decision_impact="review",
            rule_id="restrictive-frame-ancestors",
            file=rel,
            line=line_number(text, idx),
            evidence=excerpt(text, idx, idx + len("frame-ancestors")),
            recommendation="Verify Content-Security-Policy frame ancestors allow Telegram Mini App embedding.",
        )

    lower = text.lower()
    if ("sendmessage" in lower or "setchatmenubutton" in lower or "pinchatmessage" in lower) and (
        "review-ticket" not in lower and "dry-run" not in lower and "draft" not in lower
    ):
        if is_test_path(rel):
            return
        idx = min([i for i in (lower.find("sendmessage"), lower.find("setchatmenubutton"), lower.find("pinchatmessage")) if i >= 0])
        add_finding(
            findings,
            severity="medium",
            decision_impact="review",
            rule_id="live-telegram-action-without-gate",
            file=rel,
            line=line_number(text, idx),
            evidence=excerpt(text, idx, idx + 24),
            recommendation="Gate live Bot API actions behind explicit user intent, dry-run defaults, and review tickets where governance requires it.",
        )


def apply_cross_file_rules(root: Path, findings: List[Finding], signals: Signals) -> None:
    if signals.telegram_webapp_client or signals.initdata_client:
        if not signals.initdata_hmac_validation:
            add_finding(
                findings,
                severity="high",
                decision_impact="block",
                rule_id="initdata-no-server-validation",
                file=".",
                evidence="Telegram WebApp/initData references were found, but no HMAC/WebAppData validation pattern was detected.",
                recommendation="Validate Telegram initData server-side before accepting requests or trusting user identity.",
            )
        elif not signals.constant_time_compare:
            add_finding(
                findings,
                severity="medium",
                decision_impact="review",
                rule_id="initdata-no-constant-time-compare",
                file=".",
                evidence="HMAC validation exists, but no constant-time hash comparison pattern was detected.",
                recommendation="Use hmac.compare_digest, crypto.timingSafeEqual, or an equivalent constant-time comparison.",
            )
        if signals.initdata_hmac_validation and not signals.auth_freshness_check:
            add_finding(
                findings,
                severity="low",
                decision_impact="review",
                rule_id="initdata-no-freshness-check",
                file=".",
                evidence="initData validation pattern exists, but no auth_date freshness check was detected.",
                recommendation="Reject stale initData with a bounded max age when feasible.",
            )

    if signals.insecure_initdata_bypass:
        add_finding(
            findings,
            severity="medium",
            decision_impact="review",
            rule_id="insecure-initdata-bypass",
            file=".",
            evidence="An initData bypass or skip flag is present.",
            recommendation="Confirm the bypass is disabled by default, documented as local-dev only, and never used for production launch.",
        )

    if signals.admin_endpoint and not signals.admin_guard:
        add_finding(
            findings,
            severity="high",
            decision_impact="block",
            rule_id="admin-endpoint-without-guard",
            file=".",
            evidence="Admin endpoint patterns were found without an obvious server-side admin guard.",
            recommendation="Protect admin routes with server-side authorization before launch.",
        )

    if signals.cors_wildcard:
        add_finding(
            findings,
            severity="high" if signals.cors_credentials else "medium",
            decision_impact="block" if signals.cors_credentials else "review",
            rule_id="cors-wildcard-with-credentials" if signals.cors_credentials else "cors-wildcard",
            file=".",
            evidence="Wildcard CORS was detected%s." % (" with credentials" if signals.cors_credentials else ""),
            recommendation="Restrict CORS origins for production. Never combine wildcard origins with credentials.",
        )

    if (signals.telegram_webapp_client or signals.initdata_client) and not signals.https_launch_doc:
        add_finding(
            findings,
            severity="low",
            decision_impact="review",
            rule_id="missing-https-launch-notes",
            file=".",
            evidence="Telegram Mini App code was found, but no HTTPS/BotFather/tunnel launch notes were detected.",
            recommendation="Document the production HTTPS URL requirement and launch verification steps.",
        )

    if signals.telegram_webapp_client and not signals.health_endpoint:
        add_finding(
            findings,
            severity="low",
            decision_impact="review",
            rule_id="missing-health-check",
            file=".",
            evidence="Telegram Mini App code was found, but no health endpoint was detected.",
            recommendation="Expose a health endpoint so launch and tunnel checks can fail fast.",
        )

    if signals.initdata_client and not (signals.contact_policy_client and signals.contact_policy_server):
        add_finding(
            findings,
            severity="medium",
            decision_impact="review",
            rule_id="contact-policy-not-enforced-both-sides",
            file=".",
            evidence="Request/initData flow detected without obvious contact/secret rejection on both client and server.",
            recommendation="Enforce PII/contact/token rejection on the server; client-side checks are only user feedback.",
        )


def decide(findings: Sequence[Finding]) -> str:
    if any(f.decision_impact == "block" for f in findings):
        return "BLOCK"
    if any(f.decision_impact == "review" for f in findings):
        return "REVIEW"
    return "PASS"


def severity_rank(finding: Finding) -> Tuple[int, str, str]:
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    return (order.get(finding.severity, 9), finding.file, finding.rule_id)


def audit(root: Path) -> Dict[str, object]:
    root = root.expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError("target does not exist: %s" % root)
    if not root.is_dir():
        raise NotADirectoryError("target must be a directory: %s" % root)

    findings: List[Finding] = []
    files: List[FileInfo] = []
    signals = Signals()

    for path, text, raw in iter_text_files(root):
        rel = rel_path(path, root)
        files.append(FileInfo(path=rel, sha256=sha256_bytes(raw), bytes=len(raw)))
        scan_text_file(root, path, text, findings, signals)

    apply_cross_file_rules(root, findings, signals)
    findings.sort(key=severity_rank)
    files.sort(key=lambda x: x.path)

    detected_tma = signals.telegram_webapp_client or signals.initdata_client or signals.initdata_server_reference
    if not detected_tma:
        add_finding(
            findings,
            severity="low",
            decision_impact="review",
            rule_id="tma-not-detected",
            file=".",
            evidence="No Telegram WebApp/initData patterns were detected.",
            recommendation="Verify the target path points at the Telegram Mini App frontend/backend.",
        )
        findings.sort(key=severity_rank)

    return {
        "schema": "telegram-miniapp-security-audit-v1",
        "target": str(root),
        "generated_at_utc": now_iso(),
        "decision": decide(findings),
        "detected_tma": detected_tma,
        "signals": asdict(signals),
        "summary": {
            "files_scanned": len(files),
            "findings": len(findings),
            "blockers": sum(1 for f in findings if f.decision_impact == "block"),
            "reviews": sum(1 for f in findings if f.decision_impact == "review"),
        },
        "findings": [asdict(f) for f in findings],
        "file_manifest": [asdict(f) for f in files],
    }


def md_escape_cell(value: object) -> str:
    text = str(value if value is not None else "")
    return text.replace("|", "\\|").replace("\n", " ")


def render_markdown(report: Dict[str, object]) -> str:
    summary = report["summary"]  # type: ignore[index]
    findings = report["findings"]  # type: ignore[index]
    signals = report["signals"]  # type: ignore[index]
    lines: List[str] = []
    lines.append("# Telegram Mini App Security Audit")
    lines.append("")
    lines.append("- Decision: `%s`" % report["decision"])
    lines.append("- Target: `%s`" % report["target"])
    lines.append("- Generated: `%s`" % report["generated_at_utc"])
    lines.append("- Files scanned: `%s`" % summary["files_scanned"])  # type: ignore[index]
    lines.append("- Findings: `%s` (`%s` blockers, `%s` review)" % (summary["findings"], summary["blockers"], summary["reviews"]))  # type: ignore[index]
    lines.append("")
    lines.append("## Signals")
    lines.append("")
    for key in sorted(signals.keys()):  # type: ignore[union-attr]
        lines.append("- `%s`: `%s`" % (key, signals[key]))  # type: ignore[index]
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    if not findings:
        lines.append("No findings.")
    else:
        lines.append("| Severity | Impact | Rule | File | Line | Evidence | Recommendation |")
        lines.append("| --- | --- | --- | --- | ---: | --- | --- |")
        for f in findings:  # type: ignore[assignment]
            lines.append(
                "| %s | %s | `%s` | `%s` | %s | %s | %s |"
                % (
                    md_escape_cell(f["severity"]),
                    md_escape_cell(f["decision_impact"]),
                    md_escape_cell(f["rule_id"]),
                    md_escape_cell(f["file"]),
                    md_escape_cell(f["line"]),
                    md_escape_cell(f["evidence"]),
                    md_escape_cell(f["recommendation"]),
                )
            )
    lines.append("")
    lines.append("## Launch Recommendation")
    lines.append("")
    decision = str(report["decision"])
    if decision == "BLOCK":
        lines.append("Do not connect production bot tokens, BotFather, or public channels until blockers are fixed and the audit is rerun.")
    elif decision == "REVIEW":
        lines.append("Proceed only after a human reviews the flagged risks and confirms they are dev-only, mitigated, or intentionally accepted.")
    else:
        lines.append("No static blockers were detected. Still run browser/mobile QA before launch.")
    lines.append("")
    lines.append("## Limitations")
    lines.append("")
    lines.append("- Static heuristics can miss framework-specific auth and runtime configuration.")
    lines.append("- This report does not prove Telegram production launch, browser rendering, or BotFather configuration.")
    lines.append("- Treat token-like findings as leaks until verified otherwise.")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Audit Telegram Mini App security posture.")
    p.add_argument("target", help="Project or Mini App directory to audit")
    p.add_argument("--out-dir", default="", help="Directory for JSON/Markdown reports")
    p.add_argument("--json-out", default="", help="Explicit JSON output path")
    p.add_argument("--md-out", default="", help="Explicit Markdown output path")
    p.add_argument("--format", choices=("both", "json", "markdown"), default="both")
    return p.parse_args()


def write_outputs(report: Dict[str, object], args: argparse.Namespace) -> None:
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    json_out = Path(args.json_out).expanduser().resolve() if args.json_out else (out_dir / "tma_security_audit.json" if out_dir else None)
    md_out = Path(args.md_out).expanduser().resolve() if args.md_out else (out_dir / "tma_security_audit.md" if out_dir else None)

    if args.format in ("both", "json"):
        payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if json_out:
            json_out.write_text(payload, encoding="utf-8")
            print("Wrote %s" % json_out)
        else:
            print(payload)

    if args.format in ("both", "markdown"):
        md = render_markdown(report)
        if md_out:
            md_out.write_text(md, encoding="utf-8")
            print("Wrote %s" % md_out)
        else:
            print(md)


def main() -> int:
    args = parse_args()
    report = audit(Path(args.target))
    write_outputs(report, args)
    decision = str(report["decision"])
    return 2 if decision == "BLOCK" else 1 if decision == "REVIEW" else 0


if __name__ == "__main__":
    raise SystemExit(main())
