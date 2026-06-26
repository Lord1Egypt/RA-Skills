from typing import List, Dict, Any


def _matches(actual: str, pattern: str) -> bool:
    """Check if actual matches pattern. Supports * as wildcard."""
    if pattern == "*":
        return True
    if "*" in pattern:
        import fnmatch
        return fnmatch.fnmatch(actual, pattern)
    return actual.startswith(pattern.rstrip("*")) if pattern.endswith("*") else actual == pattern


def check_permission(rules: List[Dict], from_agent: str, to_agent: str, msg_type: str) -> bool:
    """
    Check if a message from from_agent to to_agent with msg_type is allowed.
    Returns True if allowed, False otherwise.
    Supports * wildcard in from/to fields.
    """
    for rule in rules:
        if not _matches(from_agent, rule.get("from", "")):
            continue
        if not _matches(to_agent, rule.get("to", "")):
            continue
        if msg_type in rule.get("allowed_types", []):
            return True
    return False
