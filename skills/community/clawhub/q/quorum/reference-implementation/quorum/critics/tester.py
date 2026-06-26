# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Tester Critic — Finding verifier for Quorum.

Unlike traditional critics that evaluate artifacts directly, the Tester takes
OTHER critics' findings as input and independently verifies whether the cited
evidence actually exists and supports the claim.

Verification levels:
  Level 1 (deterministic, zero API cost):
    - Read the actual file at the cited path
    - Read the cited line number(s)
    - Fuzzy match the cited evidence against actual file content
  Level 2 (light LLM claim check):
    - One focused LLM call per finding: "Given this excerpt and this claim,
      is the claim accurate?"
    - Only for CRITICAL/HIGH findings by default (cost control)

Output: VerificationStatus tags per finding (VERIFIED, UNVERIFIED, CONTRADICTED)
"""

from __future__ import annotations

import logging
import re
import time
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from quorum.config import QuorumConfig
from quorum.models import (
    CriticResult,
    Evidence,
    Finding,
    Locus,
    Severity,
    TesterResult,
    VerificationResult,
    VerificationStatus,
    VerifiedLocus,
)
from quorum.providers.base import BaseProvider

logger = logging.getLogger(__name__)

# ── Configuration defaults ──────────────────────────────────────────────────

# Fuzzy match threshold: above this → VERIFIED, below → UNVERIFIED/CONTRADICTED
FUZZY_MATCH_VERIFIED = 0.65
# Below this threshold with content present → CONTRADICTED
FUZZY_MATCH_CONTRADICTED = 0.30
# Maximum lines to read around a cited line for context
CONTEXT_WINDOW = 10
# Maximum file size (bytes) to attempt reading — skip binary/huge files
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
# Default severity filter for Level 2 (LLM) verification
L2_DEFAULT_SEVERITIES = frozenset({Severity.CRITICAL, Severity.HIGH})

# ── Locus parsing ───────────────────────────────────────────────────────────

# Patterns for extracting file:line from finding location strings
_LOCATION_PATTERNS = [
    # "path/to/file.py:42" or "path/to/file.py:42-50"
    re.compile(r"(?P<file>[^\s:]+\.\w+):(?P<start>\d+)(?:-(?P<end>\d+))?"),
    # "line 42 of path/to/file.py" or "lines 42-50 of path/to/file.py"
    re.compile(r"lines?\s+(?P<start>\d+)(?:\s*[-–]\s*(?P<end>\d+))?\s+(?:of|in)\s+(?P<file>[^\s,]+\.\w+)", re.IGNORECASE),
    # "path/to/file.py, line 42"
    re.compile(r"(?P<file>[^\s,]+\.\w+),?\s+lines?\s+(?P<start>\d+)(?:\s*[-–]\s*(?P<end>\d+))?", re.IGNORECASE),
    # "in file.py (line 42)"
    re.compile(r"(?:in\s+)?(?P<file>[^\s(]+\.\w+)\s*\(\s*lines?\s+(?P<start>\d+)(?:\s*[-–]\s*(?P<end>\d+))?\s*\)", re.IGNORECASE),
]

# Bare file path pattern (no line number)
_FILE_ONLY_PATTERN = re.compile(r"(?P<file>[^\s:,()]+\.\w{1,10})(?:\s|$|,|;|\))")


class ParsedLocus:
    """Structured locus extracted from a finding's location/evidence text."""

    __slots__ = ("file_path", "start_line", "end_line")

    def __init__(self, file_path: str, start_line: int | None = None, end_line: int | None = None):
        self.file_path = file_path
        self.start_line = start_line
        self.end_line = end_line or start_line

    def __repr__(self) -> str:
        if self.start_line:
            lines = f":{self.start_line}" if self.start_line == self.end_line else f":{self.start_line}-{self.end_line}"
            return f"ParsedLocus({self.file_path}{lines})"
        return f"ParsedLocus({self.file_path})"


def parse_locus_from_text(text: str) -> ParsedLocus | None:
    """
    Extract a file path and optional line number(s) from free-form text.

    Tries multiple regex patterns in priority order. Returns the first match
    or None if no parseable locus is found.
    """
    if not text:
        return None

    for pattern in _LOCATION_PATTERNS:
        m = pattern.search(text)
        if m:
            file_path = m.group("file")
            start = int(m.group("start"))
            end_str = m.group("end")
            end = int(end_str) if end_str else None
            return ParsedLocus(file_path, start, end)

    # Fall back: try to find just a file path (no line numbers)
    m = _FILE_ONLY_PATTERN.search(text)
    if m:
        return ParsedLocus(m.group("file"))

    return None


def parse_loci_from_finding(finding: Finding) -> list[ParsedLocus]:
    """
    Extract all parseable loci from a Finding.

    Sources checked in order:
    1. Structured loci (finding.loci) — already have file/line
    2. finding.location text — parsed via regex
    3. finding.evidence.result text — parsed via regex as fallback
    """
    results: list[ParsedLocus] = []
    seen_files: set[str] = set()

    # 1. Structured Locus objects (highest confidence)
    for locus in finding.loci:
        pl = ParsedLocus(locus.file, locus.start_line, locus.end_line)
        key = f"{pl.file_path}:{pl.start_line}"
        if key not in seen_files:
            results.append(pl)
            seen_files.add(key)

    # 2. Location text
    if finding.location:
        pl = parse_locus_from_text(finding.location)
        if pl:
            key = f"{pl.file_path}:{pl.start_line}"
            if key not in seen_files:
                results.append(pl)
                seen_files.add(key)

    # 3. Evidence result text (fallback)
    if finding.evidence and finding.evidence.result:
        pl = parse_locus_from_text(finding.evidence.result)
        if pl:
            key = f"{pl.file_path}:{pl.start_line}"
            if key not in seen_files:
                results.append(pl)
                seen_files.add(key)

    return results


# ── Level 1: Deterministic locus verification ──────────────────────────────


def _is_binary_content(data: bytes, sample_size: int = 8192) -> bool:
    """Heuristic: file is binary if it contains null bytes in the first N bytes."""
    return b"\x00" in data[:sample_size]


def _read_file_lines(
    file_path: Path,
) -> tuple[list[str], None] | tuple[None, str]:
    """
    Read a file and return (lines, None) on success, or (None, error_reason) on failure.

    Handles: file not found, too large, binary, encoding errors.
    """
    if not file_path.exists():
        return None, f"File not found: {file_path}"

    if not file_path.is_file():
        return None, f"Not a regular file: {file_path}"

    try:
        size = file_path.stat().st_size
    except OSError as e:
        return None, f"Cannot stat file: {e}"

    if size > MAX_FILE_SIZE:
        return None, f"File too large ({size} bytes, max {MAX_FILE_SIZE})"

    try:
        raw = file_path.read_bytes()
    except OSError as e:
        return None, f"Cannot read file: {e}"

    if _is_binary_content(raw):
        return None, "Binary file — cannot verify text loci"

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = raw.decode("latin-1")
        except UnicodeDecodeError:
            return None, "Cannot decode file (not UTF-8 or Latin-1)"

    return text.splitlines(keepends=True), None


def _extract_cited_text(finding: Finding) -> str:
    """
    Extract the text a critic claims to have seen at the locus.

    Pulls from evidence.result (primary) and description (fallback).
    """
    parts: list[str] = []
    if finding.evidence and finding.evidence.result:
        parts.append(finding.evidence.result)
    return "\n".join(parts).strip()


def _fuzzy_match_in_lines(
    cited_text: str,
    file_lines: list[str],
    start_line: int | None = None,
    end_line: int | None = None,
    context_window: int = CONTEXT_WINDOW,
) -> tuple[float, str]:
    """
    Fuzzy-match cited text against actual file content.

    If start_line is given, checks the specific region first (with context),
    then falls back to a full-file scan if the local match is poor.

    Returns (best_similarity_score, matched_content).
    """
    if not cited_text or not file_lines:
        return 0.0, ""

    full_content = "".join(file_lines)
    cited_normalized = cited_text.strip().lower()

    best_score = 0.0
    best_content = ""

    # Phase 1: Check the cited line region (if specified)
    if start_line is not None:
        idx_start = max(0, start_line - 1)
        idx_end = (end_line or start_line) if end_line else start_line
        # Expand with context
        ctx_start = max(0, idx_start - context_window)
        ctx_end = min(len(file_lines), idx_end + context_window)

        region = "".join(file_lines[idx_start:idx_end])
        region_with_ctx = "".join(file_lines[ctx_start:ctx_end])

        # Exact region match
        score = SequenceMatcher(None, cited_normalized, region.strip().lower()).ratio()
        if score > best_score:
            best_score = score
            best_content = region

        # Region with context (sliding window over context)
        if len(cited_normalized) > 0:
            score_ctx = _best_subsequence_match(cited_normalized, region_with_ctx.lower())
            if score_ctx > best_score:
                best_score = score_ctx
                best_content = region_with_ctx

    # Phase 2: Full-file scan if local match is insufficient
    if best_score < FUZZY_MATCH_VERIFIED:
        score_full = _best_subsequence_match(cited_normalized, full_content.lower())
        if score_full > best_score:
            best_score = score_full
            best_content = full_content[:500]  # truncate for storage

    return best_score, best_content


def _best_subsequence_match(needle: str, haystack: str) -> float:
    """
    Find the best fuzzy match of needle within haystack using a sliding window.

    For short needles, uses SequenceMatcher on the full strings.
    For longer needles, slides a window of needle-length across haystack.
    """
    if not needle or not haystack:
        return 0.0

    # Fast path: exact substring match (works for any length)
    if needle in haystack:
        return 1.0

    # For very short citations, compare against the whole haystack
    if len(needle) < 30:
        return SequenceMatcher(None, needle, haystack).ratio()

    # Sliding window: check chunks of haystack that are ~needle length
    window_size = len(needle)
    best = 0.0

    # Fine-grained step to avoid missing alignments
    step = max(1, min(window_size // 8, 5))
    for i in range(0, max(1, len(haystack) - window_size + 1), step):
        chunk = haystack[i : i + window_size]
        score = SequenceMatcher(None, needle, chunk).ratio()
        if score > best:
            best = score
            if best > 0.95:  # Early exit on near-perfect match
                break

    return best


def verify_finding_l1(
    finding: Finding,
    base_dir: Path,
) -> VerificationResult:
    """
    Level 1 (deterministic) verification of a single finding.

    Steps:
    1. Parse loci from the finding
    2. For each locus: read the file, check line range exists, fuzzy match content
    3. Return VERIFIED / UNVERIFIED / CONTRADICTED based on match quality

    Args:
        finding:  The Finding to verify
        base_dir: Root directory to resolve relative file paths against

    Returns:
        VerificationResult with status, explanation, and optional VerifiedLocus
    """
    parsed_loci = parse_loci_from_finding(finding)

    # No parseable locus → UNVERIFIED (not the finding's fault, just can't check)
    if not parsed_loci:
        return VerificationResult(
            status=VerificationStatus.UNVERIFIED,
            original_finding_id=finding.id,
            explanation="No parseable file:line locus found in finding — cannot verify deterministically.",
            level=1,
        )

    cited_text = _extract_cited_text(finding)
    best_result: VerificationResult | None = None
    best_score = -1.0

    for pl in parsed_loci:
        file_path = _resolve_file_path(pl.file_path, base_dir)
        lines, read_error = _read_file_lines(file_path)

        if read_error:
            result = VerificationResult(
                status=VerificationStatus.CONTRADICTED,
                original_finding_id=finding.id,
                explanation=f"Cannot read cited file: {read_error}",
                verified_locus=VerifiedLocus(
                    file_path=str(pl.file_path),
                    line_start=pl.start_line,
                    line_end=pl.end_line,
                    actual_content="",
                    similarity_score=0.0,
                ),
                level=1,
            )
            if best_result is None:
                best_result = result
            continue

        if lines is None:
            raise ValueError(f"Expected file lines after successful read of {file_path}")

        # Check line range validity
        if pl.start_line is not None:
            if pl.start_line > len(lines):
                result = VerificationResult(
                    status=VerificationStatus.CONTRADICTED,
                    original_finding_id=finding.id,
                    explanation=(
                        f"Cited line {pl.start_line} is beyond file length ({len(lines)} lines)."
                    ),
                    verified_locus=VerifiedLocus(
                        file_path=str(pl.file_path),
                        line_start=pl.start_line,
                        line_end=pl.end_line,
                        actual_content=f"[file has {len(lines)} lines]",
                        similarity_score=0.0,
                    ),
                    level=1,
                )
                if best_result is None or best_score < 0:
                    best_result = result
                continue

        # If there's cited text, fuzzy match it
        if cited_text:
            score, actual = _fuzzy_match_in_lines(
                cited_text, lines, pl.start_line, pl.end_line
            )
        else:
            # No cited text to compare — if file and line exist, that's partial verification
            if pl.start_line is not None:
                idx = pl.start_line - 1
                end_idx = (pl.end_line or pl.start_line)
                actual = "".join(lines[idx:min(end_idx, len(lines))])
                score = 0.5  # File and line exist but nothing to compare
            else:
                actual = ""
                score = 0.4  # File exists but no line to check

        verified_locus = VerifiedLocus(
            file_path=str(pl.file_path),
            line_start=pl.start_line,
            line_end=pl.end_line,
            actual_content=actual[:2000],  # cap storage
            similarity_score=round(score, 4),
        )

        if score >= FUZZY_MATCH_VERIFIED:
            status = VerificationStatus.VERIFIED
            explanation = f"Cited evidence matches actual content (similarity={score:.2f})."
        elif score >= FUZZY_MATCH_CONTRADICTED:
            status = VerificationStatus.UNVERIFIED
            explanation = (
                f"Cited evidence partially matches (similarity={score:.2f}) — "
                "could not confidently confirm or deny."
            )
        else:
            status = VerificationStatus.CONTRADICTED
            explanation = (
                f"Cited evidence does not match actual content (similarity={score:.2f})."
            )

        result = VerificationResult(
            status=status,
            original_finding_id=finding.id,
            explanation=explanation,
            verified_locus=verified_locus,
            level=1,
        )

        if score > best_score:
            best_score = score
            best_result = result

    if best_result is None:
        raise ValueError("No verification result produced — at least one locus must be evaluated")
    return best_result


def _resolve_file_path(file_path_str: str, base_dir: Path) -> Path:
    """
    Resolve a file path against the base directory.

    Handles both relative and absolute paths. Strips leading ./ if present.
    """
    fp = Path(file_path_str)

    # If absolute and exists, use it directly
    if fp.is_absolute():
        return fp

    # Try relative to base_dir
    candidate = base_dir / fp
    if candidate.exists():
        return candidate

    # Try stripping common prefixes critics might add
    for prefix in ("./", "../", "src/", "lib/"):
        if file_path_str.startswith(prefix):
            stripped = file_path_str[len(prefix):]
            candidate = base_dir / stripped
            if candidate.exists():
                return candidate

    # Try finding the file anywhere under base_dir by filename
    name = fp.name
    for match in base_dir.rglob(name):
        if match.is_file():
            return match

    # Return the original relative resolution (will fail at read time)
    return base_dir / fp


# ── Level 2: LLM claim verification ────────────────────────────────────────

# JSON schema for the LLM verification response
_L2_SCHEMA = {
    "type": "object",
    "required": ["verdict", "explanation"],
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["VERIFIED", "UNVERIFIED", "CONTRADICTED"],
            "description": "Is the critic's claim accurate given the actual code?",
        },
        "explanation": {
            "type": "string",
            "description": "Brief explanation of your verification decision.",
        },
    },
}

_L2_SYSTEM_PROMPT = """You are a verification agent for Quorum, a code quality system.

Your job: Given an excerpt of actual source code and a critic's claim about that code,
determine whether the claim is accurate.

Rules:
- VERIFIED: The claim accurately describes what the code does.
- UNVERIFIED: The claim is ambiguous or you cannot determine its accuracy from the excerpt.
- CONTRADICTED: The claim is demonstrably wrong — the code does something different from what is claimed.

Be conservative: if unsure, choose UNVERIFIED rather than CONTRADICTED.
Only choose CONTRADICTED when the evidence clearly shows the claim is false."""


def verify_finding_l2(
    finding: Finding,
    actual_content: str,
    provider: BaseProvider,
    config: QuorumConfig,
) -> VerificationResult:
    """
    Level 2 (LLM-assisted) claim verification for a single finding.

    Sends the actual code excerpt and the critic's claim to an LLM and asks
    whether the claim is accurate.

    Args:
        finding:        The Finding to verify
        actual_content: The real source code at the cited location
        provider:       LLM provider for making the verification call
        config:         Quorum config (for model selection)

    Returns:
        VerificationResult from the LLM's judgment
    """
    claim = finding.description
    evidence_text = finding.evidence.result if finding.evidence else ""

    user_prompt = f"""## Critic's Claim
{claim}

## Critic's Cited Evidence
{evidence_text}

## Actual Source Code at the Cited Location
```
{actual_content[:4000]}
```

Based on the actual source code above, is the critic's claim accurate?
Respond with a verdict (VERIFIED, UNVERIFIED, or CONTRADICTED) and a brief explanation."""

    messages = [
        {"role": "system", "content": _L2_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    try:
        raw = provider.complete_json(
            messages=messages,
            model=config.model_tier2,  # Use cost-efficient tier
            schema=_L2_SCHEMA,
            temperature=0.05,  # Low temperature for consistent verdicts
        )

        verdict_str = raw.get("verdict", "UNVERIFIED").upper()
        explanation = raw.get("explanation", "No explanation provided.")

        try:
            status = VerificationStatus(verdict_str)
        except ValueError:
            status = VerificationStatus.UNVERIFIED
            explanation = f"LLM returned unknown verdict '{verdict_str}'; defaulting to UNVERIFIED. {explanation}"

    except (ValueError, KeyError, TypeError, RuntimeError) as e:
        logger.warning("Level 2 verification failed for finding %s: %s", finding.id, e, exc_info=True)
        status = VerificationStatus.UNVERIFIED
        explanation = "LLM verification call failed due to an internal error."
    except OSError as e:
        logger.warning("Level 2 network/IO error for finding %s: %s", finding.id, e, exc_info=True)
        status = VerificationStatus.UNVERIFIED
        explanation = "LLM verification call failed due to a connectivity error."

    return VerificationResult(
        status=status,
        original_finding_id=finding.id,
        explanation=explanation,
        level=2,
    )


# ── TesterCritic: Main orchestrator ────────────────────────────────────────


class TesterCritic:
    """
    Finding verifier that checks whether other critics' citations are grounded.

    Unlike BaseCritic subclasses, the Tester does NOT evaluate the artifact
    directly. It takes CriticResult objects and verifies their findings.

    Usage:
        tester = TesterCritic(provider=provider, config=config)
        result = tester.verify(
            critic_results=[correctness_result, security_result],
            base_dir=Path("/path/to/project"),
        )
    """

    name: str = "tester"

    def __init__(
        self,
        provider: BaseProvider | None = None,
        config: QuorumConfig | None = None,
        *,
        l2_enabled: bool = True,
        l2_severities: frozenset[Severity] | None = None,
        fuzzy_threshold_verified: float = FUZZY_MATCH_VERIFIED,
        fuzzy_threshold_contradicted: float = FUZZY_MATCH_CONTRADICTED,
    ):
        """
        Args:
            provider:       LLM provider (required only if l2_enabled=True)
            config:         Quorum config (required only if l2_enabled=True)
            l2_enabled:     Whether to run Level 2 (LLM) verification
            l2_severities:  Which severity levels to run L2 on (default: CRITICAL, HIGH)
            fuzzy_threshold_verified:    Score threshold to mark VERIFIED
            fuzzy_threshold_contradicted: Score threshold below which to mark CONTRADICTED
        """
        self.provider = provider
        self.config = config
        self.l2_enabled = l2_enabled and provider is not None and config is not None
        self.l2_severities = l2_severities or L2_DEFAULT_SEVERITIES
        self.fuzzy_threshold_verified = fuzzy_threshold_verified
        self.fuzzy_threshold_contradicted = fuzzy_threshold_contradicted

    def verify(
        self,
        critic_results: list[CriticResult],
        base_dir: Path,
    ) -> TesterResult:
        """
        Verify all findings from the given critic results.

        Args:
            critic_results: Outputs from other critics to verify
            base_dir:       Root directory for resolving file paths

        Returns:
            TesterResult with per-finding verification statuses
        """
        start_ms = int(time.time() * 1000)
        all_findings = self._collect_findings(critic_results)

        if not all_findings:
            return TesterResult(runtime_ms=int(time.time() * 1000) - start_ms)

        logger.info("[tester] Verifying %d findings from %d critics", len(all_findings), len(critic_results))

        verification_results: list[VerificationResult] = []

        for finding in all_findings:
            # Level 1: Deterministic verification
            l1_result = verify_finding_l1(finding, base_dir)

            # Level 2: LLM claim check (only for qualifying findings)
            if (
                self.l2_enabled
                and finding.severity in self.l2_severities
                and l1_result.verified_locus is not None
                and l1_result.verified_locus.actual_content
                and l1_result.status != VerificationStatus.CONTRADICTED
            ):
                l2_result = verify_finding_l2(
                    finding,
                    l1_result.verified_locus.actual_content,
                    self.provider,
                    self.config,
                )
                # L2 can override L1, but only to downgrade (conservative)
                final_result = self._merge_l1_l2(l1_result, l2_result)
            else:
                final_result = l1_result

            verification_results.append(final_result)
            logger.debug(
                "[tester] %s → %s (%s)",
                finding.id,
                final_result.status.value,
                final_result.explanation[:80],
            )

        runtime_ms = int(time.time() * 1000) - start_ms

        verified = sum(1 for r in verification_results if r.status == VerificationStatus.VERIFIED)
        unverified = sum(1 for r in verification_results if r.status == VerificationStatus.UNVERIFIED)
        contradicted = sum(1 for r in verification_results if r.status == VerificationStatus.CONTRADICTED)

        result = TesterResult(
            verification_results=verification_results,
            total_findings=len(all_findings),
            verified_count=verified,
            unverified_count=unverified,
            contradicted_count=contradicted,
            runtime_ms=runtime_ms,
        )

        logger.info(
            "[tester] Done: %d verified, %d unverified, %d contradicted (%dms)",
            verified, unverified, contradicted, runtime_ms,
        )

        return result

    def verify_findings(
        self,
        findings: list[Finding],
        base_dir: Path,
    ) -> TesterResult:
        """
        Verify a flat list of findings directly (convenience method).

        Wraps findings in a synthetic CriticResult and delegates to verify().
        """
        synthetic = CriticResult(
            critic_name="synthetic",
            findings=findings,
            confidence=1.0,
        )
        return self.verify([synthetic], base_dir)

    def _collect_findings(self, results: list[CriticResult]) -> list[Finding]:
        """Flatten all findings from all critic results, skipping skipped critics."""
        findings: list[Finding] = []
        for result in results:
            if not result.skipped:
                findings.extend(result.findings)
        return findings

    def _merge_l1_l2(
        self,
        l1: VerificationResult,
        l2: VerificationResult,
    ) -> VerificationResult:
        """
        Merge Level 1 and Level 2 results.

        Policy:
        - If L2 contradicts, trust L2 (it has semantic understanding)
        - If L1 verified and L2 verified, stay VERIFIED
        - If L1 verified but L2 unverified, downgrade to UNVERIFIED
        - If L1 unverified, L2 gets the final say
        """
        # L2 CONTRADICTED always wins — it has semantic context
        if l2.status == VerificationStatus.CONTRADICTED:
            return VerificationResult(
                status=VerificationStatus.CONTRADICTED,
                original_finding_id=l1.original_finding_id,
                explanation=f"L1: {l1.explanation} | L2 (override): {l2.explanation}",
                verified_locus=l1.verified_locus,
                level=2,
            )

        # Both agree → use that status
        if l1.status == l2.status:
            return VerificationResult(
                status=l1.status,
                original_finding_id=l1.original_finding_id,
                explanation=f"L1 and L2 agree: {l2.explanation}",
                verified_locus=l1.verified_locus,
                level=2,
            )

        # L1 VERIFIED but L2 UNVERIFIED → downgrade to UNVERIFIED
        if l1.status == VerificationStatus.VERIFIED and l2.status == VerificationStatus.UNVERIFIED:
            return VerificationResult(
                status=VerificationStatus.UNVERIFIED,
                original_finding_id=l1.original_finding_id,
                explanation=f"L1 verified content match, but L2 could not confirm claim: {l2.explanation}",
                verified_locus=l1.verified_locus,
                level=2,
            )

        # L1 UNVERIFIED but L2 VERIFIED → upgrade to VERIFIED
        if l1.status == VerificationStatus.UNVERIFIED and l2.status == VerificationStatus.VERIFIED:
            return VerificationResult(
                status=VerificationStatus.VERIFIED,
                original_finding_id=l1.original_finding_id,
                explanation=f"L1 uncertain, but L2 confirms claim: {l2.explanation}",
                verified_locus=l1.verified_locus,
                level=2,
            )

        # Fallback: prefer the more conservative status
        return VerificationResult(
            status=l2.status,
            original_finding_id=l1.original_finding_id,
            explanation=f"L1: {l1.explanation} | L2: {l2.explanation}",
            verified_locus=l1.verified_locus,
            level=2,
        )
