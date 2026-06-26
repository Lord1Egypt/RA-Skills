"""
Permission scope extractors for SKILL.md content.

Extracts what resources a skill actually uses (detected)
and what it declares (from YAML frontmatter).
"""

import re

import yaml

# ── Env var references: $VAR, ${VAR} ───────────────────────────────────────

_ENV_VAR_RE = re.compile(r"\$\{?\s*([A-Z][A-Z0-9_]{1,50})\s*\}?")

# ── CLI tools: "Run: <tool>" or common tool names after shell indicators ───

_CLI_TOOL_RE = re.compile(
    r"(?:"
    r"(?:^|\n)\s*(?:Run:|Execute:|run:|execute:|`|\$)\s*"
    r"|(?:\busing\s+|\bwith\s+|\bvia\s+)"
    r")"
    r"([a-z][a-z0-9_-]*)",
)

# ── Filesystem paths: /absolute or ~/home ──────────────────────────────────

_FS_PATH_RE = re.compile(
    r"(?:~/?|/(?:etc|tmp|var|usr|home|root|opt|dev|proc|sys))"
    r"[/\w._-]*",
)

# ── Network URLs ───────────────────────────────────────────────────────────

_URL_RE = re.compile(r"https?://[^\s\"'`,)>\]]+")


def extract_env_vars(content: str) -> list[str]:
    """Extract environment variable names from skill content."""
    return sorted(set(_ENV_VAR_RE.findall(content)))


def extract_cli_tools(content: str) -> list[str]:
    """Extract CLI tool names from run/execute commands."""
    return sorted(set(_CLI_TOOL_RE.findall(content)))


def extract_filesystem_paths(content: str) -> list[str]:
    """Extract filesystem paths referenced in content."""
    return sorted(set(_FS_PATH_RE.findall(content)))


def extract_network_urls(content: str) -> list[str]:
    """Extract network URLs from content."""
    return sorted(set(_URL_RE.findall(content)))


def extract_declared(content: str) -> dict[str, list[str]]:
    """Extract declared requirements from YAML frontmatter."""
    result: dict[str, list[str]] = {"env": [], "bins": []}

    # Extract YAML frontmatter
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return result

    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return result

    if not isinstance(fm, dict):
        return result

    # Look in metadata.openclaw.requires (or aliases)
    metadata = fm.get("metadata", {})
    if not isinstance(metadata, dict):
        return result

    for key in ("openclaw", "clawdbot", "clawdis"):
        oc = metadata.get(key, {})
        if isinstance(oc, dict):
            requires = oc.get("requires", {})
            if isinstance(requires, dict):
                env = requires.get("env", [])
                if isinstance(env, list):
                    result["env"] = [str(e) for e in env]
                bins = requires.get("bins", [])
                if isinstance(bins, list):
                    result["bins"] = [str(b) for b in bins]
            break

    return result
