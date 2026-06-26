from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Sequence, Set, Tuple
from urllib.parse import urlparse

from .constants import (
    DECISION_VALUES,
    EXTERNAL_URL_PATTERN,
    NODE_LITERAL_SAFE_COMMAND_PATTERNS,
    TEST_PATH_PARTS,
    TRUSTED_BOOTSTRAP_DOMAINS,
)


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_rel(path: Path, root: Path) -> str:
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    return str(rel).replace("\\", "/")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def normalize_decision(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    candidate = value.strip().lower()
    if candidate in DECISION_VALUES:
        return candidate
    return None


def git_commit_sha(target_repo: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(target_repo), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    value = result.stdout.strip()
    if not value:
        return "unknown"
    return value


def truncate_snippet(value: str, limit: int = 200) -> str:
    stripped = value.strip()
    if len(stripped) <= limit:
        return stripped
    return stripped[: limit - 3] + "..."


def line_has_any(line: str, patterns: Sequence[re.Pattern[str]]) -> bool:
    for pattern in patterns:
        if pattern.search(line):
            return True
    return False


def extract_external_urls(text: str) -> list[str]:
    return [match.group(0) for match in EXTERNAL_URL_PATTERN.finditer(text)]


def hostname_is_trusted(url_value: str) -> bool:
    try:
        host = (urlparse(url_value).hostname or "").lower()
    except ValueError:
        return False
    if not host:
        return False
    return host in TRUSTED_BOOTSTRAP_DOMAINS or any(host.endswith(f".{item}") for item in TRUSTED_BOOTSTRAP_DOMAINS)


def line_is_trusted_bootstrap(text: str) -> bool:
    urls = extract_external_urls(text)
    if not urls:
        return False
    return all(hostname_is_trusted(url) for url in urls)


def line_looks_tainted_exec(raw_line: str) -> bool:
    taint_hints = (
        "${",
        "+",
        "process.env",
        "argv",
        "stdin",
        "input",
        "user",
        "request",
        "join(",
        "format(",
        "template",
    )
    lowered = raw_line.lower()
    return any(hint in lowered for hint in taint_hints)


def extract_literal_exec_command(raw_line: str) -> Optional[str]:
    literal_match = re.search(r"\(\s*(['\"])([^'\"]{1,180})\1", raw_line)
    if not literal_match:
        return None
    return literal_match.group(2).strip()


def is_literal_safe_exec(raw_line: str) -> bool:
    if line_looks_tainted_exec(raw_line):
        return False
    literal = extract_literal_exec_command(raw_line)
    if not literal:
        return False
    normalized = re.sub(r"\s+", " ", literal).strip()
    return any(pattern.match(normalized) for pattern in NODE_LITERAL_SAFE_COMMAND_PATTERNS)


def normalize_relative_path(path_value: str) -> str:
    normalized = path_value.strip().replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    normalized = normalized.lstrip("/")
    return normalized


def is_probably_binary(text: str) -> bool:
    return "\x00" in text


def line_number_for_substring(lines: Sequence[str], needle: str) -> int:
    if not needle:
        return 1
    for idx, line in enumerate(lines, start=1):
        if needle in line:
            return idx
    return 1


def looks_like_example_line(line: str) -> bool:
    lowered = line.lower().strip()
    if not lowered:
        return False
    if lowered.startswith(("example:", "for example", "attack pattern", "mitigation", "- example")):
        return True
    if "example" in lowered and ("`" in line or '"' in line or "'" in line):
        return True
    return False


def is_test_or_fixture_path(rel_path: Path) -> bool:
    lower_parts = {part.lower() for part in rel_path.parts}
    if lower_parts & TEST_PATH_PARTS:
        return True

    lower_name = rel_path.name.lower()
    if lower_name.startswith("test_"):
        return True
    if lower_name.endswith("_test.py") or lower_name.endswith(".spec.js") or lower_name.endswith(".spec.ts"):
        return True
    return False


def is_non_runtime_line(raw_line: str) -> bool:
    stripped = raw_line.strip()
    if not stripped:
        return True
    if stripped.startswith(("#", "//")):
        return True
    if "re.compile(" in raw_line:
        return True
    if stripped.startswith(("assert ", "self.assert", "expect(")):
        return True
    return False


def is_defensive_prompt_line(raw_line: str) -> bool:
    lowered = raw_line.lower()
    defensive_hints = (
        "treat",
        "attempts as",
        "not as actual instructions",
        "never",
        "do not",
        "don't",
        "refuse",
        "mitigation",
    )
    override_terms = (
        "ignore previous instructions",
        "override system",
        "bypass safety",
        "reveal your system prompt",
    )
    if not any(term in lowered for term in override_terms):
        return False
    return any(hint in lowered for hint in defensive_hints)


def normalize_token_set(value: str) -> Set[str]:
    tokens = re.findall(r"[a-z0-9_]+", value.lower())
    return {tok for tok in tokens if tok}


def snippets_match(assessment_snippet: str, evidence_snippet: str) -> bool:
    a_norm = re.sub(r"[^a-z0-9_]+", "", assessment_snippet.lower())
    e_norm = re.sub(r"[^a-z0-9_]+", "", evidence_snippet.lower())
    if not a_norm:
        return False
    if len(a_norm) >= 8 and (a_norm in e_norm or e_norm in a_norm):
        return True

    a_tokens = normalize_token_set(assessment_snippet)
    e_tokens = normalize_token_set(evidence_snippet)
    if not a_tokens or not e_tokens:
        return False
    overlap = len(a_tokens & e_tokens) / float(max(1, len(a_tokens)))
    return overlap >= 0.50


def nearest_distance(points_a: Sequence[int], points_b: Sequence[int]) -> Tuple[int, int]:
    best_distance = 10**9
    best_target = points_b[0]
    for a in points_a:
        for b in points_b:
            distance = abs(a - b)
            if distance < best_distance:
                best_distance = distance
                best_target = b
    return best_distance, best_target
