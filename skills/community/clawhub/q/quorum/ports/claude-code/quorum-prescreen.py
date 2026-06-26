#!/usr/bin/env python3
"""Quorum Pre-Screen — Standalone pre-screen for Copilot CLI.

Runs fast, LLM-free deterministic checks against an artifact file and
outputs a JSON report to stdout. Stdlib-first with optional PyYAML for
YAML validation (degrades gracefully if unavailable).

Checks (PS-001 through PS-010):
  security  — hardcoded paths, credentials, PII
  syntax    — JSON / YAML / Python parse errors
  links     — broken relative markdown links
  structure — TODO markers, whitespace issues, empty files

Usage:
    python3 quorum-prescreen.py <target-file>
"""

from __future__ import annotations

import json
import py_compile
import re
import sys
import tempfile
from pathlib import Path

# Try optional PyYAML — degrade gracefully if unavailable
try:
    import yaml  # type: ignore[import-untyped]

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ── Constants ─────────────────────────────────────────────────────────────────

# Maximum artifact size for pre-screen processing (10 MB)
MAX_ARTIFACT_SIZE = 10 * 1024 * 1024

# Display limits for evidence in findings
MAX_EVIDENCE_LINES = 20
MAX_EVIDENCE_DISPLAY_WIDTH = 120
MAX_TODO_EVIDENCE_LINES = 30
MAX_TRAILING_WS_SAMPLE = 10
MAX_LINE_REPR_WIDTH = 80


# ── Regex patterns ────────────────────────────────────────────────────────────

_RE_HARDCODED_PATHS = re.compile(
    r"""
    (?:
        /Users/[A-Za-z0-9._-]+   # macOS user home paths
      | /home/[A-Za-z0-9._-]+    # Linux user home paths
      | /etc/[A-Za-z0-9._/-]+    # Unix system paths
      | /var/[A-Za-z0-9._/-]+    # Unix var paths
      | /tmp/[A-Za-z0-9._/-]+    # Unix temp paths
      | C:\\(?:Users|Windows|Program\ Files)[\\A-Za-z0-9._() -]+ # Windows paths
    )
    """,
    re.VERBOSE,
)

_RE_CREDENTIALS = re.compile(
    r"""
    (?:
        (?:password|passwd|pwd)\s*[:=]\s*['\"]?.{1,80}   # password= / password:
      | (?:secret|api_?key|apikey|auth_?token|access_?token|client_?secret)\s*[:=]\s*['\"]?\S{8,}
      | (?:token)\s*[:=]\s*['\"]?\S{8,}                 # token=...
      | (?:BEGIN\s+(?:RSA|DSA|EC|OPENSSH)\s+PRIVATE\s+KEY)  # PEM private keys
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Long base64 strings (>40 chars of [A-Za-z0-9+/=]) are often encoded secrets
_RE_BASE64_SECRET = re.compile(r"[A-Za-z0-9+/]{40,}={0,2}")

_RE_EMAIL = re.compile(
    r"\b[A-Za-z0-9._%+'-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

_RE_PHONE = re.compile(
    r"""
    (?:
        \+?1[-.\s]?          # optional country code
    )?
    \(?[2-9]\d{2}\)?        # area code
    [-.\s]?
    [2-9]\d{2}              # exchange
    [-.\s]?
    \d{4}                   # subscriber
    \b
    """,
    re.VERBOSE,
)

_RE_SSN = re.compile(
    r"\b(?!000|666|9\d{2})\d{3}[- ](?!00)\d{2}[- ](?!0000)\d{4}\b"
)

_RE_TODO = re.compile(
    r"\b(?:TODO|FIXME|HACK|XXX|NOCOMMIT|DO NOT COMMIT)\b",
    re.IGNORECASE,
)

_RE_MARKDOWN_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

_RE_TRAILING_SPACE = re.compile(r"[ \t]+$", re.MULTILINE)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _scan_lines(
    text: str,
    pattern: re.Pattern,
    *,
    exclude_comments: bool = False,
) -> list[tuple[int, str]]:
    """
    Return (line_number, line_text) tuples for lines matching *pattern*.

    Args:
        text:             Full artifact text
        pattern:          Compiled regex
        exclude_comments: If True, skip lines that start with # (Python/YAML)
    """
    hits: list[tuple[int, str]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if exclude_comments and stripped.startswith("#"):
            continue
        if pattern.search(line):
            hits.append((i, line.rstrip()))
    return hits


def _deduplicate_line_hits(
    hits: list[tuple[int, str]],
) -> list[tuple[int, str]]:
    """Deduplicate and sort (line_no, line_text) tuples by line number."""
    seen: set[int] = set()
    result: list[tuple[int, str]] = []
    for ln, line in sorted(hits, key=lambda x: x[0]):
        if ln not in seen:
            seen.add(ln)
            result.append((ln, line))
    return result


def _redact(line: str, max_len: int = MAX_EVIDENCE_DISPLAY_WIDTH) -> str:
    """
    Partially redact a line that likely contains a secret, for safe logging.
    Replaces the second half of any token > 8 chars with asterisks.
    """

    def _mask(m: re.Match) -> str:
        val = m.group(0)
        keep = max(4, len(val) // 3)
        return val[:keep] + "***"

    redacted = re.sub(r"\S{6,}", _mask, line)
    return redacted[:max_len]


# ── Check dict factory helpers ────────────────────────────────────────────────

def _make_pass(
    check_id: str,
    name: str,
    category: str,
    description: str,
) -> dict:
    return {
        "id": check_id,
        "name": name,
        "category": category,
        "status": "PASS",
        "details": description,
    }


def _make_fail(
    check_id: str,
    name: str,
    category: str,
    description: str,
    evidence: str,
    locations: list[str],
) -> dict:
    detail_parts = [description]
    if evidence:
        detail_parts.append(evidence)
    if locations:
        detail_parts.append(f"Locations: {', '.join(locations)}")
    return {
        "id": check_id,
        "name": name,
        "category": category,
        "status": "FAIL",
        "details": "\n".join(detail_parts),
    }


def _make_skip(
    check_id: str,
    name: str,
    category: str,
    description: str,
    reason: str,
) -> dict:
    return {
        "id": check_id,
        "name": name,
        "category": category,
        "status": "SKIP",
        "details": f"{description} — skipped: {reason}",
    }


# ── PS-001: Hardcoded paths ──────────────────────────────────────────────────

def ps001_hardcoded_paths(artifact_path: Path, artifact_text: str) -> dict:
    """PS-001: Detect hardcoded absolute filesystem paths."""
    hits = _scan_lines(artifact_text, _RE_HARDCODED_PATHS, exclude_comments=False)
    if not hits:
        return _make_pass(
            "PS-001", "hardcoded_paths", "security",
            "No hardcoded absolute paths detected",
        )

    locations = [f"line {ln}" for ln, _ in hits]
    evidence_lines = [f"  L{ln}: {line[:MAX_EVIDENCE_DISPLAY_WIDTH]}" for ln, line in hits[:MAX_EVIDENCE_LINES]]
    evidence = f"Found {len(hits)} hardcoded path(s):\n" + "\n".join(evidence_lines)
    if len(hits) > MAX_EVIDENCE_LINES:
        evidence += f"\n  ... and {len(hits) - MAX_EVIDENCE_LINES} more"

    return _make_fail(
        "PS-001", "hardcoded_paths", "security",
        f"Hardcoded absolute path(s) found ({len(hits)} occurrence(s))",
        evidence, locations,
    )


# ── PS-002: Credentials ──────────────────────────────────────────────────────

def ps002_credentials(artifact_path: Path, artifact_text: str) -> dict:
    """PS-002: Detect potential credentials or secrets."""
    hits = _scan_lines(artifact_text, _RE_CREDENTIALS, exclude_comments=False)

    # Also flag suspiciously long base64 blobs (could be encoded keys)
    b64_hits: list[tuple[int, str]] = []
    for i, line in enumerate(artifact_text.splitlines(), start=1):
        for m in _RE_BASE64_SECRET.finditer(line):
            val = m.group(0)
            if len(val) >= 40:
                b64_hits.append((i, line.rstrip()))
                break  # one hit per line is enough

    all_hits = _deduplicate_line_hits(hits + b64_hits)

    if not all_hits:
        return _make_pass(
            "PS-002", "credential_patterns", "security",
            "No credential or secret patterns detected",
        )

    locations = [f"line {ln}" for ln, _ in all_hits]
    evidence_lines = [f"  L{ln}: {_redact(line)[:MAX_EVIDENCE_DISPLAY_WIDTH]}" for ln, line in all_hits[:MAX_EVIDENCE_LINES]]
    evidence = f"Found {len(all_hits)} potential credential pattern(s):\n" + "\n".join(
        evidence_lines
    )

    return _make_fail(
        "PS-002", "credential_patterns", "security",
        f"Potential credential/secret pattern(s) found ({len(all_hits)} occurrence(s))",
        evidence, locations,
    )


# ── PS-003: PII ──────────────────────────────────────────────────────────────

def ps003_pii(artifact_path: Path, artifact_text: str) -> dict:
    """PS-003: Detect PII patterns (email, phone, SSN)."""
    email_hits = _scan_lines(artifact_text, _RE_EMAIL)
    phone_hits = _scan_lines(artifact_text, _RE_PHONE)
    ssn_hits = _scan_lines(artifact_text, _RE_SSN)

    all_hits = _deduplicate_line_hits(email_hits + phone_hits + ssn_hits)

    if not all_hits:
        return _make_pass(
            "PS-003", "pii_patterns", "security",
            "No PII patterns (email, phone, SSN) detected",
        )

    # Build breakdown
    parts = []
    if email_hits:
        parts.append(f"{len(email_hits)} email(s)")
    if phone_hits:
        parts.append(f"{len(phone_hits)} phone number(s)")
    if ssn_hits:
        parts.append(f"{len(ssn_hits)} SSN-like pattern(s)")

    locations = [f"line {ln}" for ln, _ in all_hits]
    evidence_lines = [f"  L{ln}: {_redact(line)[:MAX_EVIDENCE_DISPLAY_WIDTH]}" for ln, line in all_hits[:MAX_EVIDENCE_LINES]]
    evidence = f"PII detected — {', '.join(parts)}:\n" + "\n".join(evidence_lines)

    return _make_fail(
        "PS-003", "pii_patterns", "security",
        f"PII pattern(s) found: {', '.join(parts)}",
        evidence, locations,
    )


# ── PS-004: JSON validity ────────────────────────────────────────────────────

def ps004_json_validity(artifact_path: Path, artifact_text: str) -> dict:
    """PS-004: Validate JSON can be parsed without errors."""
    try:
        json.loads(artifact_text)
        return _make_pass(
            "PS-004", "json_validity", "syntax",
            "JSON parses successfully (valid JSON)",
        )
    except json.JSONDecodeError as exc:
        evidence = f"JSON parse error at line {exc.lineno}, col {exc.colno}: {exc.msg}"
        return _make_fail(
            "PS-004", "json_validity", "syntax",
            f"Invalid JSON: {exc.msg}",
            evidence, [f"line {exc.lineno}"],
        )


# ── PS-005: YAML validity ────────────────────────────────────────────────────

def ps005_yaml_validity(artifact_path: Path, artifact_text: str) -> dict:
    """PS-005: Validate YAML can be parsed without errors."""
    if not HAS_YAML:
        return _make_skip(
            "PS-005", "yaml_validity", "syntax",
            "YAML parse validation",
            "PyYAML not installed",
        )

    try:
        yaml.safe_load(artifact_text)
        return _make_pass(
            "PS-005", "yaml_validity", "syntax",
            "YAML parses successfully (valid YAML)",
        )
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        loc = f"line {mark.line + 1}" if mark else "unknown location"
        evidence = f"YAML parse error at {loc}: {exc}"
        return _make_fail(
            "PS-005", "yaml_validity", "syntax",
            f"Invalid YAML at {loc}",
            evidence, [loc] if mark else [],
        )


# ── PS-006: Python syntax ────────────────────────────────────────────────────

def ps006_python_syntax(artifact_path: Path, artifact_text: str) -> dict:
    """PS-006: Validate Python syntax using py_compile."""
    tmp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", encoding="utf-8", delete=False
        ) as tmp:
            tmp.write(artifact_text)
            tmp_path = tmp.name

        py_compile.compile(tmp_path, doraise=True)

        return _make_pass(
            "PS-006", "python_syntax", "syntax",
            "Python syntax is valid (py_compile passed)",
        )

    except py_compile.PyCompileError as exc:
        msg = str(exc)
        loc_match = re.search(r"line (\d+)", msg)
        loc = f"line {loc_match.group(1)}" if loc_match else "unknown"
        return _make_fail(
            "PS-006", "python_syntax", "syntax",
            f"Python syntax error at {loc}",
            msg, [loc] if loc_match else [],
        )

    except (OSError, UnicodeDecodeError) as exc:
        return _make_skip(
            "PS-006", "python_syntax", "syntax",
            "Python syntax check",
            f"Could not compile ({type(exc).__name__}): {exc}",
        )

    finally:
        if tmp_path:
            Path(tmp_path).unlink(missing_ok=True)


# ── PS-007: Broken markdown links ────────────────────────────────────────────

def ps007_broken_md_links(artifact_path: Path, artifact_text: str) -> dict:
    """PS-007: Detect broken relative links in Markdown files."""
    base_dir = artifact_path.parent
    broken: list[tuple[int, str, str]] = []  # (line_no, text, target)

    for i, line in enumerate(artifact_text.splitlines(), start=1):
        for match in _RE_MARKDOWN_LINK.finditer(line):
            target = match.group(2)
            # Skip external links, anchors, and mailto
            if target.startswith(("http://", "https://", "ftp://", "mailto:")) or target.startswith("#"):
                continue
            # Strip fragment from relative path
            path_part = target.split("#")[0].strip()
            if not path_part:
                continue  # anchor-only link
            resolved = (base_dir / path_part).resolve()
            if not resolved.exists():
                broken.append((i, match.group(1), target))

    if not broken:
        return _make_pass(
            "PS-007", "broken_md_links", "links",
            "All relative Markdown links resolve to existing files",
        )

    locations = [f"line {ln}" for ln, _, _ in broken]
    evidence_lines = [
        f"  L{ln}: [{text}]({tgt}) — target not found"
        for ln, text, tgt in broken[:20]
    ]
    evidence = f"{len(broken)} broken link(s):\n" + "\n".join(evidence_lines)

    return _make_fail(
        "PS-007", "broken_md_links", "links",
        f"{len(broken)} broken relative Markdown link(s)",
        evidence, locations,
    )


# ── PS-008: TODO markers ─────────────────────────────────────────────────────

def ps008_todo_markers(artifact_path: Path, artifact_text: str) -> dict:
    """PS-008: Detect TODO / FIXME / HACK / XXX markers."""
    hits = _scan_lines(artifact_text, _RE_TODO)
    if not hits:
        return _make_pass(
            "PS-008", "todo_markers", "structure",
            "No TODO/FIXME/HACK markers found",
        )

    locations = [f"line {ln}" for ln, _ in hits]
    evidence_lines = [f"  L{ln}: {line[:MAX_EVIDENCE_DISPLAY_WIDTH]}" for ln, line in hits[:MAX_TODO_EVIDENCE_LINES]]
    evidence = f"{len(hits)} tech-debt marker(s):\n" + "\n".join(evidence_lines)
    if len(hits) > MAX_TODO_EVIDENCE_LINES:
        evidence += f"\n  ... and {len(hits) - MAX_TODO_EVIDENCE_LINES} more"

    return _make_fail(
        "PS-008", "todo_markers", "structure",
        f"{len(hits)} TODO/FIXME/HACK marker(s) found",
        evidence, locations,
    )


# ── PS-009: Whitespace ───────────────────────────────────────────────────────

def ps009_whitespace(artifact_path: Path, artifact_text: str) -> dict:
    """PS-009: Detect trailing whitespace and mixed line endings."""
    issues: list[str] = []
    locations: list[str] = []

    # Check for mixed line endings
    has_crlf = "\r\n" in artifact_text
    has_lf = re.search(r"(?<!\r)\n", artifact_text) is not None
    if has_crlf and has_lf:
        issues.append("mixed line endings (CRLF and LF)")

    # Check for trailing whitespace
    trailing_hits = [
        (i + 1, line)
        for i, line in enumerate(artifact_text.splitlines())
        if line != line.rstrip(" \t")
    ]
    if trailing_hits:
        issues.append(f"{len(trailing_hits)} line(s) with trailing whitespace")
        locations.extend([f"line {ln}" for ln, _ in trailing_hits[:20]])

    if not issues:
        return _make_pass(
            "PS-009", "whitespace_issues", "structure",
            "No trailing whitespace or mixed line endings detected",
        )

    evidence = "Whitespace issues:\n"
    for issue in issues:
        evidence += f"  - {issue}\n"
    if trailing_hits:
        sample = "\n".join(
            f"  L{ln}: {repr(line[:MAX_LINE_REPR_WIDTH])}" for ln, line in trailing_hits[:MAX_TRAILING_WS_SAMPLE]
        )
        evidence += f"Sample trailing-whitespace lines:\n{sample}"

    return _make_fail(
        "PS-009", "whitespace_issues", "structure",
        f"Whitespace issues: {'; '.join(issues)}",
        evidence, locations,
    )


# ── PS-010: Empty file ───────────────────────────────────────────────────────

def ps010_empty_file(artifact_path: Path, artifact_text: str) -> dict:
    """PS-010: Detect empty or near-empty files."""
    size = len(artifact_text)

    if size == 0:
        return _make_fail(
            "PS-010", "empty_file", "structure",
            "File is completely empty (0 bytes)",
            "File size is 0 bytes.", [],
        )

    stripped = artifact_text.strip()
    if not stripped:
        return _make_fail(
            "PS-010", "empty_file", "structure",
            "File contains only whitespace",
            f"File is {size} bytes but contains only whitespace.", [],
        )

    return _make_pass(
        "PS-010", "empty_file", "structure",
        f"File is non-empty ({size} bytes)",
    )


# ── Empty result helper ───────────────────────────────────────────────────────

def _empty_result(target_path: Path, error: str) -> dict:
    """Return an empty result dict with an error message."""
    return {
        "target": str(target_path),
        "total_checks": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "checks": [],
        "error": error,
    }


# ── Input validation ──────────────────────────────────────────────────────────

def _validate_input(target_path: Path) -> str | None:
    """
    Validate the target path is a readable regular file within size limits.

    Returns None if valid, or an error message string if invalid.
    """
    if not target_path.exists():
        return f"File not found: {target_path.name}"

    if not target_path.is_file():
        return f"Not a regular file: {target_path.name}"

    file_size = target_path.stat().st_size
    if file_size > MAX_ARTIFACT_SIZE:
        return f"Artifact too large ({file_size} bytes, max {MAX_ARTIFACT_SIZE})"

    return None


# ── Check collection ──────────────────────────────────────────────────────────

def _collect_checks(
    target_path: Path,
    artifact_text: str,
    ext: str,
) -> list[dict]:
    """Dispatch all checks based on file extension and return results."""
    checks: list[dict] = []

    # ── Security ──────────────────────────────────────────────────────────
    checks.append(ps001_hardcoded_paths(target_path, artifact_text))
    checks.append(ps002_credentials(target_path, artifact_text))
    checks.append(ps003_pii(target_path, artifact_text))

    # ── Syntax (extension-gated) ──────────────────────────────────────────
    if ext == ".json":
        checks.append(ps004_json_validity(target_path, artifact_text))
    else:
        checks.append(_make_skip(
            "PS-004", "json_validity", "syntax",
            "JSON parse validation", "Not a .json file",
        ))

    if ext in (".yaml", ".yml"):
        checks.append(ps005_yaml_validity(target_path, artifact_text))
    else:
        checks.append(_make_skip(
            "PS-005", "yaml_validity", "syntax",
            "YAML parse validation", "Not a .yaml/.yml file",
        ))

    if ext == ".py":
        checks.append(ps006_python_syntax(target_path, artifact_text))
    else:
        checks.append(_make_skip(
            "PS-006", "python_syntax", "syntax",
            "Python syntax check", "Not a .py file",
        ))

    # ── Links (markdown only) ─────────────────────────────────────────────
    if ext == ".md":
        checks.append(ps007_broken_md_links(target_path, artifact_text))
    else:
        checks.append(_make_skip(
            "PS-007", "broken_md_links", "links",
            "Broken relative markdown links", "Not a .md file",
        ))

    # ── Structure ─────────────────────────────────────────────────────────
    checks.append(ps008_todo_markers(target_path, artifact_text))
    checks.append(ps009_whitespace(target_path, artifact_text))
    checks.append(ps010_empty_file(target_path, artifact_text))

    return checks


def _tally_results(target_path: Path, checks: list[dict]) -> dict:
    """Compute summary counts and return the final result dict."""
    passed = sum(1 for c in checks if c["status"] == "PASS")
    failed = sum(1 for c in checks if c["status"] == "FAIL")
    skipped = sum(1 for c in checks if c["status"] == "SKIP")

    return {
        "target": str(target_path),
        "total_checks": len(checks),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "checks": checks,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def run_prescreen(target_path: Path) -> dict:
    """Run all pre-screen checks against the target file and return result dict.

    Safe to call as a library function — returns an error dict on invalid input
    instead of calling sys.exit(). The 'error' key is present only when the
    pipeline could not run.
    """
    # ── Input validation ──────────────────────────────────────────────────
    error = _validate_input(target_path)
    if error is not None:
        return _empty_result(target_path, error)

    artifact_text = target_path.read_text(encoding="utf-8", errors="replace")
    ext = target_path.suffix.lower()

    if len(artifact_text) > MAX_ARTIFACT_SIZE:
        return _empty_result(
            target_path,
            f"Artifact text too large ({len(artifact_text)} bytes, max {MAX_ARTIFACT_SIZE})",
        )

    if "\x00" in artifact_text:
        return _empty_result(target_path, "Binary content detected")

    # ── Run checks ────────────────────────────────────────────────────────
    checks = _collect_checks(target_path, artifact_text, ext)

    return _tally_results(target_path, checks)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: quorum-prescreen.py <target-file>", file=sys.stderr)
        sys.exit(2)

    target = Path(sys.argv[1]).resolve()

    if not target.exists():
        print(f"Error: file not found: {target.name}", file=sys.stderr)
        sys.exit(1)

    if not target.is_file():
        print(f"Error: not a regular file: {target.name}", file=sys.stderr)
        sys.exit(1)

    result = run_prescreen(target)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    json.dump(result, sys.stdout, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
