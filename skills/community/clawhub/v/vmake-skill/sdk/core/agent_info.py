"""Optional caller metadata for SDK WAPI requests."""

import os
import unicodedata


def resolve_agent_info(name=None, version=None, model=None):
    """Normalize explicit or environment-provided Agent metadata."""
    result = {}
    for field, value, limit in (
        ("name", name, 64),
        ("version", version, 128),
        ("model", model, 256),
    ):
        if value is None:
            value = os.environ.get("SKILL_AGENT_" + field.upper(), "")
        value = str(value)
        if any(unicodedata.category(char) == "Cc" for char in value):
            value = ""
        value = value.strip()
        if field == "name":
            value = value.lower()
        try:
            value.encode("latin-1")
            if len(value.encode("utf-8")) > limit:
                value = ""
        except UnicodeError:
            value = ""
        result[field] = value
    return result


def agent_headers(info):
    """Return WAPI headers for nonempty normalized Agent metadata."""
    return {
        "X-Agent-" + field.title(): value
        for field, value in info.items()
        if value
    }
