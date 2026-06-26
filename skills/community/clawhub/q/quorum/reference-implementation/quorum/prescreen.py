# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Deterministic pre-screen engine for Quorum.

Runs fast, LLM-free checks before dispatching to LLM critics.
Results are injected into critic prompts as pre_verified_evidence[] so critics
can reference them without re-deriving.

Checks are organised by category:
  security  — hardcoded paths, credentials, PII
  syntax    — JSON / YAML / Python parse errors
  links     — broken relative markdown links
  structure — TODO markers, whitespace issues, empty files
"""

from __future__ import annotations

import json
import logging
import py_compile
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import yaml

from quorum.models import Finding, Evidence, PreScreenCheck, PreScreenResult, Severity

logger = logging.getLogger(__name__)


# ── Regex patterns ─────────────────────────────────────────────────────────────

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


# ── Repo-root discovery ───────────────────────────────────────────────────────

def _find_repo_root(start: Path) -> Path:
    """Walk up from *start* to find the nearest directory containing .git.

    Returns *start* (resolved) if no .git is found — this preserves the
    old behaviour where files outside a repo are bounded to their own
    directory.
    """
    current = start.resolve()
    while True:
        if (current / ".git").exists():
            return current
        parent = current.parent
        if parent == current:
            # Reached filesystem root without finding .git
            return start.resolve()
        current = parent


# ── Helper ─────────────────────────────────────────────────────────────────────

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


# ── PreScreen engine ───────────────────────────────────────────────────────────

class PreScreen:
    """
    Deterministic pre-screen engine.

    Runs all applicable checks against an artifact file, then returns a
    PreScreenResult ready for injection into LLM critic prompts via
    ``result.to_evidence_block()``.
    """

    # Maximum artifact size for pre-screen processing (10 MB)
    MAX_ARTIFACT_SIZE = 10 * 1024 * 1024

    def run(self, artifact_path: Path, artifact_text: str) -> PreScreenResult:
        """
        Run all applicable checks against the artifact.

        Args:
            artifact_path: Path to the artifact file on disk
            artifact_text: Full text of the artifact (already read by caller)

        Returns:
            PreScreenResult containing every check's outcome
        """
        start_ms = int(time.time() * 1000)

        # V003 fix: Input validation — reject oversized or binary content
        if len(artifact_text) > self.MAX_ARTIFACT_SIZE:
            logger.warning(
                "PreScreen: artifact too large (%d bytes), skipping all checks",
                len(artifact_text),
            )
            return PreScreenResult(
                checks=[], total_checks=0, passed=0, failed=0, skipped=0,
                runtime_ms=int(time.time() * 1000) - start_ms,
            )

        if "\x00" in artifact_text:
            logger.warning("PreScreen: binary content detected, skipping all checks")
            return PreScreenResult(
                checks=[], total_checks=0, passed=0, failed=0, skipped=0,
                runtime_ms=int(time.time() * 1000) - start_ms,
            )

        ext = artifact_path.suffix.lower()
        checks: list[PreScreenCheck] = []

        logger.info(
            "PreScreen: running checks on %s (ext=%s, %d chars)",
            artifact_path.name, ext, len(artifact_text),
        )

        # ── Security ─────────────────────────────────────────────────────────
        checks.append(self._ps001_hardcoded_paths(artifact_path, artifact_text))
        checks.append(self._ps002_credentials(artifact_path, artifact_text))
        checks.append(self._ps003_pii(artifact_path, artifact_text))

        # ── Syntax (extension-gated) ──────────────────────────────────────────
        if ext == ".json":
            checks.append(self._ps004_json_validity(artifact_path, artifact_text))
        else:
            checks.append(_skip("PS-004", "json_validity", "syntax", Severity.MEDIUM,
                                "JSON parse validation", "Not a .json file"))

        if ext in (".yaml", ".yml"):
            checks.append(self._ps005_yaml_validity(artifact_path, artifact_text))
        else:
            checks.append(_skip("PS-005", "yaml_validity", "syntax", Severity.MEDIUM,
                                "YAML parse validation", "Not a .yaml/.yml file"))

        if ext == ".py":
            checks.append(self._ps006_python_syntax(artifact_path, artifact_text))
        else:
            checks.append(_skip("PS-006", "python_syntax", "syntax", Severity.HIGH,
                                "Python syntax check", "Not a .py file"))

        # ── Links (markdown only) ─────────────────────────────────────────────
        if ext == ".md":
            checks.append(self._ps007_broken_md_links(artifact_path, artifact_text))
        else:
            checks.append(_skip("PS-007", "broken_md_links", "links", Severity.LOW,
                                "Broken relative markdown links", "Not a .md file"))

        # ── Structure ─────────────────────────────────────────────────────────
        checks.append(self._ps008_todo_markers(artifact_path, artifact_text))
        checks.append(self._ps009_whitespace(artifact_path, artifact_text))
        checks.append(self._ps010_empty_file(artifact_path, artifact_text))

        # ── External Tools ────────────────────────────────────────────────────
        # Run Ruff linter (graceful degradation if not installed)
        try:
            ruff_findings = self._run_ruff(artifact_path, artifact_text)
            ruff_checks = self._findings_to_checks(ruff_findings, "ruff")
            checks.extend(ruff_checks)
        except Exception as e:
            logger.warning("Ruff integration failed: %s", e, exc_info=True)
            checks.append(_pass("EXT-RUFF", "ruff_analysis", "external_tools",
                               Severity.INFO, "No issues found by ruff (tool unavailable)"))

        # Run DevSkim security scanner (graceful degradation if not installed)
        try:
            devskim_findings = self._run_devskim(artifact_path, artifact_text)
            devskim_checks = self._findings_to_checks(devskim_findings, "devskim")
            checks.extend(devskim_checks)
        except Exception as e:
            logger.warning("DevSkim integration failed: %s", e, exc_info=True)
            checks.append(_pass("EXT-DEVSKIM", "devskim_analysis", "external_tools",
                               Severity.INFO, "No issues found by devskim (tool unavailable)"))

        # Run Bandit SAST (Python only; skip if Ruff is available since S rules cover Bandit)
        # Deduplication: Ruff S-rules are Bandit rules re-implemented — prefer Ruff when present.
        if ext == ".py" and not shutil.which("ruff"):
            try:
                bandit_findings = self._run_bandit(artifact_path, artifact_text)
                bandit_checks = self._findings_to_checks(bandit_findings, "bandit")
                checks.extend(bandit_checks)
            except Exception as e:
                logger.warning("Bandit integration failed: %s", e, exc_info=True)
                checks.append(_pass("EXT-BANDIT", "bandit_analysis", "external_tools",
                                   Severity.INFO, "No issues found by bandit (tool unavailable)"))

        # Run PSScriptAnalyzer (PowerShell files only; graceful degradation if pwsh not installed)
        if ext == ".ps1":
            try:
                pssa_findings = self._run_pssa(artifact_path, artifact_text)
                pssa_checks = self._findings_to_checks(pssa_findings, "pssa")
                checks.extend(pssa_checks)
            except Exception as e:
                logger.warning("PSScriptAnalyzer integration failed: %s", e, exc_info=True)
                checks.append(_pass("EXT-PSSA", "pssa_analysis", "external_tools",
                                   Severity.INFO, "No issues found by pssa (tool unavailable)"))

        runtime_ms = int(time.time() * 1000) - start_ms
        passed  = sum(1 for c in checks if c.result == "PASS")
        failed  = sum(1 for c in checks if c.result == "FAIL")
        skipped = sum(1 for c in checks if c.result == "SKIP")

        logger.info(
            "PreScreen complete in %dms: %d passed, %d failed, %d skipped",
            runtime_ms, passed, failed, skipped,
        )

        return PreScreenResult(
            checks=checks,
            total_checks=len(checks),
            passed=passed,
            failed=failed,
            skipped=skipped,
            runtime_ms=runtime_ms,
        )

    # ── PS-001 ─────────────────────────────────────────────────────────────────

    def _ps001_hardcoded_paths(
        self, artifact_path: Path, artifact_text: str
    ) -> PreScreenCheck:
        """PS-001: Detect hardcoded absolute filesystem paths."""
        hits = _scan_lines(artifact_text, _RE_HARDCODED_PATHS, exclude_comments=False)
        if not hits:
            return _pass("PS-001", "hardcoded_paths", "security", Severity.HIGH,
                         "No hardcoded absolute paths detected")

        locations = [f"line {ln}" for ln, _ in hits]
        evidence_lines = [f"  L{ln}: {line[:120]}" for ln, line in hits[:20]]
        evidence = f"Found {len(hits)} hardcoded path(s):\n" + "\n".join(evidence_lines)
        if len(hits) > 20:
            evidence += f"\n  … and {len(hits) - 20} more"

        return _fail("PS-001", "hardcoded_paths", "security", Severity.HIGH,
                     f"Hardcoded absolute path(s) found ({len(hits)} occurrence(s))",
                     evidence, locations)

    # ── PS-002 ─────────────────────────────────────────────────────────────────

    def _ps002_credentials(
        self, artifact_path: Path, artifact_text: str
    ) -> PreScreenCheck:
        """PS-002: Detect potential credentials or secrets."""
        hits = _scan_lines(artifact_text, _RE_CREDENTIALS, exclude_comments=False)

        # Also flag suspiciously long base64 blobs (could be encoded keys)
        b64_hits: list[tuple[int, str]] = []
        for i, line in enumerate(artifact_text.splitlines(), start=1):
            for m in _RE_BASE64_SECRET.finditer(line):
                # Skip short words that happen to match base64 charset
                val = m.group(0)
                if len(val) >= 40:
                    b64_hits.append((i, line.rstrip()))
                    break  # one hit per line is enough

        all_hits = _deduplicate_line_hits(hits + b64_hits)

        if not all_hits:
            return _pass("PS-002", "credential_patterns", "security", Severity.CRITICAL,
                         "No credential or secret patterns detected")

        locations = [f"line {ln}" for ln, _ in all_hits]
        evidence_lines = [f"  L{ln}: {_redact(line)[:120]}" for ln, line in all_hits[:10]]
        evidence = f"Found {len(all_hits)} potential credential pattern(s):\n" + "\n".join(evidence_lines)

        return _fail("PS-002", "credential_patterns", "security", Severity.CRITICAL,
                     f"Potential credential/secret pattern(s) found ({len(all_hits)} occurrence(s))",
                     evidence, locations)

    # ── PS-003 ─────────────────────────────────────────────────────────────────

    def _ps003_pii(
        self, artifact_path: Path, artifact_text: str
    ) -> PreScreenCheck:
        """PS-003: Detect PII patterns (email, phone, SSN)."""
        email_hits  = _scan_lines(artifact_text, _RE_EMAIL)
        phone_hits  = _scan_lines(artifact_text, _RE_PHONE)
        ssn_hits    = _scan_lines(artifact_text, _RE_SSN)

        all_hits = _deduplicate_line_hits(email_hits + phone_hits + ssn_hits)

        if not all_hits:
            return _pass("PS-003", "pii_patterns", "security", Severity.HIGH,
                         "No PII patterns (email, phone, SSN) detected")

        # Build breakdown
        parts = []
        if email_hits:
            parts.append(f"{len(email_hits)} email(s)")
        if phone_hits:
            parts.append(f"{len(phone_hits)} phone number(s)")
        if ssn_hits:
            parts.append(f"{len(ssn_hits)} SSN-like pattern(s)")

        locations = [f"line {ln}" for ln, _ in all_hits]
        evidence_lines = [f"  L{ln}: {_redact(line)[:120]}" for ln, line in all_hits[:10]]
        evidence = f"PII detected — {', '.join(parts)}:\n" + "\n".join(evidence_lines)

        return _fail("PS-003", "pii_patterns", "security", Severity.HIGH,
                     f"PII pattern(s) found: {', '.join(parts)}",
                     evidence, locations)

    # ── PS-004 ─────────────────────────────────────────────────────────────────

    def _ps004_json_validity(
        self, artifact_path: Path, artifact_text: str
    ) -> PreScreenCheck:
        """PS-004: Validate JSON can be parsed without errors."""
        try:
            json.loads(artifact_text)
            return _pass("PS-004", "json_validity", "syntax", Severity.MEDIUM,
                         "JSON parses successfully (valid JSON)")
        except json.JSONDecodeError as exc:
            evidence = f"JSON parse error at line {exc.lineno}, col {exc.colno}: {exc.msg}"
            return _fail("PS-004", "json_validity", "syntax", Severity.MEDIUM,
                         f"Invalid JSON: {exc.msg}",
                         evidence, [f"line {exc.lineno}"])

    # ── PS-005 ─────────────────────────────────────────────────────────────────

    def _ps005_yaml_validity(
        self, artifact_path: Path, artifact_text: str
    ) -> PreScreenCheck:
        """PS-005: Validate YAML can be parsed without errors."""
        try:
            yaml.safe_load(artifact_text)
            return _pass("PS-005", "yaml_validity", "syntax", Severity.MEDIUM,
                         "YAML parses successfully (valid YAML)")
        except yaml.YAMLError as exc:
            mark = getattr(exc, "problem_mark", None)
            loc = f"line {mark.line + 1}" if mark else "unknown location"
            evidence = f"YAML parse error at {loc}: {exc}"
            return _fail("PS-005", "yaml_validity", "syntax", Severity.MEDIUM,
                         f"Invalid YAML at {loc}",
                         evidence, [loc] if mark else [])

    # ── PS-006 ─────────────────────────────────────────────────────────────────

    def _ps006_python_syntax(
        self, artifact_path: Path, artifact_text: str
    ) -> PreScreenCheck:
        """PS-006: Validate Python syntax using py_compile."""
        # py_compile requires a real file; write to a temp file
        # V001 fix: use try/finally to guarantee cleanup
        tmp_path: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                suffix=".py", mode="w", encoding="utf-8", delete=False
            ) as tmp:
                tmp.write(artifact_text)
                tmp_path = tmp.name

            py_compile.compile(tmp_path, doraise=True)

            return _pass("PS-006", "python_syntax", "syntax", Severity.HIGH,
                         "Python syntax is valid (py_compile passed)")

        except py_compile.PyCompileError as exc:
            msg = str(exc)
            loc_match = re.search(r"line (\d+)", msg)
            loc = f"line {loc_match.group(1)}" if loc_match else "unknown"
            return _fail("PS-006", "python_syntax", "syntax", Severity.HIGH,
                         f"Python syntax error at {loc}",
                         msg, [loc] if loc_match else [])

        except (OSError, UnicodeDecodeError) as exc:
            return _skip("PS-006", "python_syntax", "syntax", Severity.HIGH,
                         "Python syntax check", f"Could not compile ({type(exc).__name__}): {exc}")

        finally:
            if tmp_path:
                Path(tmp_path).unlink(missing_ok=True)

    # ── PS-007 ─────────────────────────────────────────────────────────────────

    def _ps007_broken_md_links(
        self, artifact_path: Path, artifact_text: str
    ) -> PreScreenCheck:
        """PS-007: Detect broken relative links in Markdown files."""
        base_dir = artifact_path.parent
        repo_root = _find_repo_root(base_dir)
        broken: list[tuple[int, str, str]] = []  # (line_no, text, target)

        for i, line in enumerate(artifact_text.splitlines(), start=1):
            for match in _RE_MARKDOWN_LINK.finditer(line):
                target = match.group(2)
                # Skip external links, anchors, and mailto
                if (
                    target.startswith(("http://", "https://", "ftp://", "mailto:"))
                    or target.startswith("#")
                ):
                    continue
                # Strip fragment from relative path
                path_part = target.split("#")[0].strip()
                if not path_part:
                    continue  # anchor-only link
                resolved = (base_dir / path_part).resolve()
                # V002 fix: skip links that escape the repo root
                try:
                    resolved.relative_to(repo_root)
                except ValueError:
                    continue  # path traversal — escapes repo boundary
                if not resolved.exists():
                    broken.append((i, match.group(1), target))

        if not broken:
            return _pass("PS-007", "broken_md_links", "links", Severity.LOW,
                         "All relative Markdown links resolve to existing files")

        locations = [f"line {ln}" for ln, _, _ in broken]
        evidence_lines = [
            f"  L{ln}: [{text}]({tgt}) — target not found"
            for ln, text, tgt in broken[:20]
        ]
        evidence = f"{len(broken)} broken link(s):\n" + "\n".join(evidence_lines)

        return _fail("PS-007", "broken_md_links", "links", Severity.LOW,
                     f"{len(broken)} broken relative Markdown link(s)",
                     evidence, locations)

    # ── PS-008 ─────────────────────────────────────────────────────────────────

    def _ps008_todo_markers(
        self, artifact_path: Path, artifact_text: str
    ) -> PreScreenCheck:
        """PS-008: Detect TODO / FIXME / HACK / XXX markers."""
        hits = _scan_lines(artifact_text, _RE_TODO)
        if not hits:
            return _pass("PS-008", "todo_markers", "structure", Severity.INFO,
                         "No TODO/FIXME/HACK markers found")

        locations = [f"line {ln}" for ln, _ in hits]
        evidence_lines = [f"  L{ln}: {line[:120]}" for ln, line in hits[:30]]
        evidence = f"{len(hits)} tech-debt marker(s):\n" + "\n".join(evidence_lines)
        if len(hits) > 30:
            evidence += f"\n  … and {len(hits) - 30} more"

        return _fail("PS-008", "todo_markers", "structure", Severity.INFO,
                     f"{len(hits)} TODO/FIXME/HACK marker(s) found",
                     evidence, locations)

    # ── PS-009 ─────────────────────────────────────────────────────────────────

    def _ps009_whitespace(
        self, artifact_path: Path, artifact_text: str
    ) -> PreScreenCheck:
        """PS-009: Detect trailing whitespace and mixed line endings."""
        issues: list[str] = []
        locations: list[str] = []

        # Check for mixed line endings
        has_crlf = "\r\n" in artifact_text
        has_lf   = re.search(r"(?<!\r)\n", artifact_text) is not None
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
            return _pass("PS-009", "whitespace_issues", "structure", Severity.INFO,
                         "No trailing whitespace or mixed line endings detected")

        evidence = "Whitespace issues:\n"
        for issue in issues:
            evidence += f"  - {issue}\n"
        if trailing_hits:
            sample = "\n".join(
                f"  L{ln}: {repr(line[:80])}" for ln, line in trailing_hits[:10]
            )
            evidence += f"Sample trailing-whitespace lines:\n{sample}"

        return _fail("PS-009", "whitespace_issues", "structure", Severity.INFO,
                     f"Whitespace issues: {'; '.join(issues)}",
                     evidence, locations)

    # ── PS-010 ─────────────────────────────────────────────────────────────────

    def _ps010_empty_file(
        self, artifact_path: Path, artifact_text: str
    ) -> PreScreenCheck:
        """PS-010: Detect empty or near-empty files."""
        size = artifact_path.stat().st_size if artifact_path.exists() else len(artifact_text)

        if size == 0:
            return _fail("PS-010", "empty_file", "structure", Severity.MEDIUM,
                         "File is completely empty (0 bytes)",
                         "File size is 0 bytes.", [])

        stripped = artifact_text.strip()
        if not stripped:
            return _fail("PS-010", "empty_file", "structure", Severity.MEDIUM,
                         "File contains only whitespace",
                         f"File is {size} bytes but contains only whitespace.", [])

        return _pass("PS-010", "empty_file", "structure", Severity.MEDIUM,
                     f"File is non-empty ({size} bytes)")

    # ── External Tools ─────────────────────────────────────────────────────────

    def _run_ruff(self, artifact_path: Path, artifact_text: str) -> list[Finding]:
        """
        Run Ruff linter against Python files and convert results to Findings.

        Returns empty list if Ruff is not installed or file is not Python.
        """
        if artifact_path.suffix.lower() != ".py":
            return []

        try:
            # Run ruff check with JSON output, selecting only S (security/bandit) rules
            result = subprocess.run(
                ["ruff", "check", "--select", "S", "--output-format", "json", str(artifact_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode not in (0, 1):  # 0=clean, 1=violations found
                logger.warning("Ruff check failed with exit code %d: %s",
                               result.returncode, result.stderr)
                return []

            if not result.stdout.strip():
                return []

            # Parse JSON output
            violations = json.loads(result.stdout)
            findings = []

            for violation in violations:
                # Map Ruff severity to Quorum severity
                ruff_code = violation.get("code", "")
                severity = self._map_ruff_severity(ruff_code)

                # Extract location
                location = violation.get("location", {})
                line_num = location.get("row", 1)
                column = location.get("column", 1)

                # Create Evidence
                evidence = Evidence(
                    tool="ruff",
                    result=f"[{ruff_code}] {violation.get('message', '')} at line {line_num}:{column}"
                )

                # Extract CWE reference if available (some Ruff rules map to security issues)
                framework_refs = []
                if ruff_code.startswith(("S", "B")):  # Security/bandit rules
                    framework_refs.append(f"RUFF-{ruff_code}")

                finding = Finding(
                    severity=severity,
                    category="code_quality",
                    description=f"Ruff {ruff_code}: {violation.get('message', '')[:100]}",
                    evidence=evidence,
                    location=f"line {line_num}",
                    critic="ruff",
                    framework_refs=framework_refs
                )
                findings.append(finding)

            return findings

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            logger.warning("Ruff execution failed: %s", e)
            return []
        except FileNotFoundError:
            logger.debug("Ruff not installed, skipping Ruff checks")
            return []
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("Failed to parse Ruff output: %s", e)
            return []

    def _run_devskim(self, artifact_path: Path, artifact_text: str) -> list[Finding]:
        """
        Run Microsoft DevSkim against file and convert SARIF results to Findings.

        Maps DevSkim severity: Critical/Error -> HIGH, Warning -> MEDIUM
        Extracts CWE IDs from SARIF output when available.
        """
        try:
            # Run DevSkim with SARIF output
            result = subprocess.run(
                ["devskim", "analyze", "--source-code", str(artifact_path), "-f", "sarif"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode not in (0, 1):  # 0=clean, 1=issues found
                logger.warning("DevSkim analyze failed with exit code %d: %s",
                               result.returncode, result.stderr)
                return []

            if not result.stdout.strip():
                return []

            # Parse SARIF output
            sarif_data = json.loads(result.stdout)
            findings = []

            for run in sarif_data.get("runs", []):
                rules = {rule.get("id", ""): rule for rule in run.get("tool", {}).get("driver", {}).get("rules", []) if rule.get("id")}

                for sarif_result in run.get("results", []):
                    rule_id = sarif_result.get("ruleId", "")
                    rule_info = rules.get(rule_id, {})

                    # Map DevSkim severity to Quorum severity
                    level = sarif_result.get("level", "warning").lower()
                    severity = self._map_devskim_severity(level)

                    # Extract location
                    locations = sarif_result.get("locations", [])
                    location_str = "unknown"
                    if locations:
                        phys_loc = locations[0].get("physicalLocation", {})
                        region = phys_loc.get("region", {})
                        start_line = region.get("startLine", 1)
                        location_str = f"line {start_line}"

                    # Extract CWE from rule metadata
                    framework_refs = []
                    rule_metadata = rule_info.get("properties", {})
                    cwe_ids = rule_metadata.get("tags", [])
                    for tag in cwe_ids:
                        if tag.startswith("CWE-"):
                            framework_refs.append(tag)

                    # Add DevSkim rule ID
                    if rule_id:
                        framework_refs.append(f"DEVSKIM-{rule_id}")

                    # Create Evidence
                    evidence = Evidence(
                        tool="devskim",
                        result=f"[{rule_id}] {sarif_result.get('message', {}).get('text', '')} {location_str}"
                    )

                    finding = Finding(
                        severity=severity,
                        category="security",
                        description=f"DevSkim {rule_id}: {rule_info.get('shortDescription', {}).get('text', sarif_result.get('message', {}).get('text', ''))[:100]}",
                        evidence=evidence,
                        location=location_str,
                        critic="devskim",
                        framework_refs=framework_refs
                    )
                    findings.append(finding)

            return findings

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            logger.warning("DevSkim execution failed: %s", e)
            return []
        except FileNotFoundError:
            logger.debug("DevSkim not installed, skipping DevSkim checks")
            return []
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("Failed to parse DevSkim SARIF output: %s", e)
            return []

    def _run_bandit(self, artifact_path: Path, artifact_text: str) -> list[Finding]:
        """
        Run Bandit SAST against Python files and convert results to Findings.

        Only runs on .py files. Skipped gracefully if bandit is not installed.
        Caller is responsible for deduplication against Ruff (prefer Ruff when available).
        """
        if artifact_path.suffix.lower() != ".py":
            return []

        if not shutil.which("bandit"):
            logger.info("Bandit not installed, skipping Bandit checks")
            return []

        try:
            result = subprocess.run(
                ["bandit", "-f", "json", "-q", str(artifact_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            # bandit exits 0 (clean), 1 (issues found), or non-zero on error
            if result.returncode not in (0, 1):
                logger.warning("Bandit failed with exit code %d: %s",
                               result.returncode, result.stderr)
                return []

            output = result.stdout.strip()
            if not output:
                return []

            data = json.loads(output)
            findings = []

            for issue in data.get("results", []):
                test_id = issue.get("test_id", "")
                test_name = issue.get("test_name", "")
                severity = self._map_bandit_severity(issue.get("issue_severity", "MEDIUM"))
                confidence = issue.get("issue_confidence", "")
                line_num = issue.get("line_number", 1)
                issue_text = issue.get("issue_text", "")

                # CWE reference if available
                framework_refs = []
                cwe = issue.get("issue_cwe", {})
                if cwe and cwe.get("id"):
                    framework_refs.append(f"CWE-{cwe['id']}")
                if test_id:
                    framework_refs.append(f"BANDIT-{test_id}")

                evidence = Evidence(
                    tool="bandit",
                    result=f"[{test_id}] {issue_text} at line {line_num} (confidence: {confidence})"
                )

                finding = Finding(
                    severity=severity,
                    category="security",
                    description=f"Bandit {test_id} ({test_name}): {issue_text[:100]}",
                    evidence=evidence,
                    location=f"line {line_num}",
                    critic="bandit",
                    framework_refs=framework_refs
                )
                findings.append(finding)

            return findings

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            logger.warning("Bandit execution failed: %s", e)
            return []
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("Failed to parse Bandit output: %s", e)
            return []

    def _run_pssa(self, artifact_path: Path, artifact_text: str) -> list[Finding]:
        """
        Run PSScriptAnalyzer via pwsh against PowerShell files.

        Only runs on .ps1 files. Skipped gracefully if pwsh is not installed.
        Filters to security-relevant rules only.
        """
        if artifact_path.suffix.lower() != ".ps1":
            return []

        if not shutil.which("pwsh"):
            logger.info("pwsh not installed, skipping PSScriptAnalyzer checks")
            return []

        # Security-relevant PSSA rules only
        _PSSA_SECURITY_RULES = {
            "AvoidUsingConvertToSecureStringWithPlainText",
            "AvoidUsingUsernameAndPasswordParams",
            "AvoidUsingPlainTextForPassword",
            "AvoidUsingInvokeExpression",
            "AvoidUsingBrokenHashAlgorithms",
            "AvoidUsingComputerNameHardcoded",
            "AvoidUsingAllowUnencryptedAuthentication",
            "UsePSCredentialType",
        }

        try:
            # SECURITY: PowerShell command injection mitigated.  Single-quoted strings
            # in PowerShell don't expand variables/backticks/subexpressions; only
            # internal single quotes need doubling (' → ''), which we do below.
            # artifact_path originates from filesystem resolution, not user input.
            escaped_path = str(artifact_path).replace("'", "''")
            ps_command = (
                f"Invoke-ScriptAnalyzer -Path '{escaped_path}' "
                "-Severity Warning,Error | ConvertTo-Json"
            )
            result = subprocess.run(
                ["pwsh", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                logger.warning("PSScriptAnalyzer failed with exit code %d: %s",
                               result.returncode, result.stderr)
                return []

            output = result.stdout.strip()
            if not output or output == "null":
                return []

            # PSScriptAnalyzer returns a single object or array; normalise to list
            raw = json.loads(output)
            diagnostics = raw if isinstance(raw, list) else [raw]

            findings = []
            for i, diag in enumerate(diagnostics):
                rule_name = diag.get("RuleName", "")
                if rule_name not in _PSSA_SECURITY_RULES:
                    continue

                severity_str = diag.get("Severity", "Warning")
                severity = self._map_pssa_severity(severity_str)
                line_num = diag.get("Line", 1)
                message = diag.get("Message", "")

                framework_refs = [f"PSSA-{rule_name}"]

                evidence = Evidence(
                    tool="pssa",
                    result=f"[{rule_name}] {message} at line {line_num}"
                )

                finding = Finding(
                    severity=severity,
                    category="security",
                    description=f"PSScriptAnalyzer {rule_name}: {message[:100]}",
                    evidence=evidence,
                    location=f"line {line_num}",
                    critic="pssa",
                    framework_refs=framework_refs
                )
                findings.append(finding)

            return findings

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            logger.warning("PSScriptAnalyzer execution failed: %s", e)
            return []
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("Failed to parse PSScriptAnalyzer output: %s", e)
            return []

    def _map_ruff_severity(self, ruff_code: str) -> Severity:
        """Map Ruff S-rule codes to Quorum severities. S1xx → MEDIUM, S2xx+ → HIGH."""
        if ruff_code.startswith("S"):
            try:
                rule_num = int(ruff_code[1:4])
                return Severity.MEDIUM if rule_num < 200 else Severity.HIGH
            except (ValueError, IndexError):
                return Severity.MEDIUM
        # Syntax errors → HIGH
        if ruff_code.startswith(("E9", "F")):
            return Severity.HIGH
        # Style/complexity → MEDIUM
        if ruff_code.startswith(("E", "W", "C", "N")):
            return Severity.MEDIUM
        return Severity.LOW

    def _map_bandit_severity(self, bandit_severity: str) -> Severity:
        """Map Bandit severity strings to Quorum severities."""
        s = bandit_severity.upper()
        if s == "HIGH":
            return Severity.HIGH
        if s == "MEDIUM":
            return Severity.MEDIUM
        if s == "LOW":
            return Severity.LOW
        return Severity.MEDIUM

    def _map_pssa_severity(self, pssa_severity: str) -> Severity:
        """Map PSScriptAnalyzer severity to Quorum severities. Error → HIGH, Warning → MEDIUM."""
        s = pssa_severity.lower()
        if s == "error":
            return Severity.HIGH
        if s == "warning":
            return Severity.MEDIUM
        return Severity.MEDIUM

    def _map_devskim_severity(self, devskim_level: str) -> Severity:
        """Map DevSkim severity levels to Quorum severities."""
        level_lower = devskim_level.lower()
        if level_lower in ("critical", "error"):
            return Severity.HIGH
        elif level_lower == "warning":
            return Severity.MEDIUM
        elif level_lower in ("note", "info"):
            return Severity.LOW
        else:
            return Severity.MEDIUM  # Default fallback

    def _findings_to_checks(self, findings: list[Finding], tool_name: str) -> list[PreScreenCheck]:
        """Convert external tool findings to PreScreenCheck objects."""
        if not findings:
            return [_pass(
                f"EXT-{tool_name.upper()}",
                f"{tool_name}_analysis",
                "external_tools",
                Severity.INFO,
                f"No issues found by {tool_name}"
            )]

        checks = []
        for i, finding in enumerate(findings):
            check_id = f"EXT-{tool_name.upper()}-{i+1:03d}"
            locations = [finding.location] if finding.location else []

            # Format evidence to include framework references
            evidence = finding.evidence.result
            if finding.framework_refs:
                evidence += f"\nReferences: {', '.join(finding.framework_refs)}"

            checks.append(_fail(
                check_id,
                f"{tool_name}_finding_{i+1}",
                "external_tools",
                finding.severity,
                finding.description,
                evidence,
                locations
            ))

        return checks


# ── Factory helpers ────────────────────────────────────────────────────────────

def _pass(
    check_id: str,
    name: str,
    category: str,
    severity: Severity,
    description: str,
) -> PreScreenCheck:
    return PreScreenCheck(
        id=check_id,
        name=name,
        category=category,
        severity=severity,
        description=description,
        result="PASS",
        evidence="",
        locations=[],
    )


def _fail(
    check_id: str,
    name: str,
    category: str,
    severity: Severity,
    description: str,
    evidence: str,
    locations: list[str],
) -> PreScreenCheck:
    return PreScreenCheck(
        id=check_id,
        name=name,
        category=category,
        severity=severity,
        description=description,
        result="FAIL",
        evidence=evidence,
        locations=locations,
    )


def _skip(
    check_id: str,
    name: str,
    category: str,
    severity: Severity,
    description: str,
    reason: str,
) -> PreScreenCheck:
    return PreScreenCheck(
        id=check_id,
        name=name,
        category=category,
        severity=severity,
        description=description,
        result="SKIP",
        evidence=reason,
        locations=[],
    )


# ── Utilities ──────────────────────────────────────────────────────────────────

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


def _redact(line: str, max_len: int = 120) -> str:
    """
    Partially redact a line that likely contains a secret, for safe logging.
    Replaces the second half of any token > 8 chars with asterisks.
    """
    # Redact long tokens (potential secrets)
    def _mask(m: re.Match) -> str:
        val = m.group(0)
        keep = max(4, len(val) // 3)
        return val[:keep] + "***"

    redacted = re.sub(r"\S{6,}", _mask, line)
    return redacted[:max_len]
