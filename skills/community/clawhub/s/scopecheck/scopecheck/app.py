"""
ScopeCheck API — FastAPI application.

Single endpoint: POST /v1/check-scope
Accepts SKILL.md content, returns permission scope analysis.
"""

import re

from fastapi import FastAPI

from .extractors import (
    extract_cli_tools,
    extract_declared,
    extract_env_vars,
    extract_filesystem_paths,
    extract_network_urls,
)
from .models import (
    CheckScopeRequest,
    CheckScopeResponse,
    DeclaredScope,
    DetectedScope,
)

app = FastAPI(
    title="ScopeCheck API",
    description="OpenClaw SKILL.md permission scope analyzer.",
    version="0.1.0",
)

_NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)


def _extract_name(content: str) -> str:
    match = _NAME_RE.search(content)
    return match.group(1).strip() if match else "unknown"


def _find_undeclared(
    declared: dict[str, list[str]],
    detected_env: list[str],
    detected_cli: list[str],
    detected_fs: list[str],
    detected_urls: list[str],
) -> list[str]:
    """Find resources that are detected but not declared."""
    undeclared = []

    declared_env_set = set(declared.get("env", []))
    for env in detected_env:
        if env not in declared_env_set:
            undeclared.append(f"env:{env}")

    declared_bins_set = set(declared.get("bins", []))
    for tool in detected_cli:
        if tool not in declared_bins_set:
            undeclared.append(f"bin:{tool}")

    # Filesystem and network are never declared in SKILL.md metadata,
    # so any detection is flagged as undeclared
    for path in detected_fs:
        undeclared.append(f"fs:{path}")

    for url in detected_urls:
        undeclared.append(f"net:{url}")

    return undeclared


@app.post("/v1/check-scope", response_model=CheckScopeResponse)
async def check_scope(request: CheckScopeRequest) -> CheckScopeResponse:
    """Analyze a SKILL.md file for permission scope."""
    content = request.skill_content

    declared_raw = extract_declared(content)
    detected_env = extract_env_vars(content)
    detected_cli = extract_cli_tools(content)
    detected_fs = extract_filesystem_paths(content)
    detected_urls = extract_network_urls(content)

    # Remove declared env vars from detected (they're expected)
    # But keep them in detected for full visibility
    undeclared = _find_undeclared(
        declared_raw, detected_env, detected_cli, detected_fs, detected_urls
    )

    return CheckScopeResponse(
        skill_name=_extract_name(content),
        declared=DeclaredScope(
            env=declared_raw.get("env", []),
            bins=declared_raw.get("bins", []),
        ),
        detected=DetectedScope(
            env_vars=detected_env,
            cli_tools=detected_cli,
            filesystem_paths=detected_fs,
            network_urls=detected_urls,
        ),
        undeclared_access=undeclared,
    )
