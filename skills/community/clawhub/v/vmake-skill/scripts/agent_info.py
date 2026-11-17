"""Optional caller metadata for v2 WAPI requests; no product-specific identity inference."""
import os
import unicodedata


def resolve_agent_info(name=None, version=None, model=None):
    """Explicit values override environment; empty/invalid values suppress that field."""
    result = {}
    for field, value, limit in (("name", name, 64), ("version", version, 128), ("model", model, 256)):
        if value is None:
            value = os.environ.get("SKILL_AGENT_" + field.upper(), "")
        value = str(value)
        if any(unicodedata.category(c) == "Cc" for c in value):
            value = ""
        value = value.strip()
        if field == "name":
            value = value.lower()
        try:
            # requests/http.client require header values encodable as Latin-1.
            value.encode("latin-1")
            if len(value.encode("utf-8")) > limit:
                value = ""
        except UnicodeError:
            value = ""
        result[field] = value
    return result


def agent_headers(info):
    """Only nonempty, normalized metadata becomes a WAPI header."""
    return {"X-Agent-" + field.title(): value for field, value in info.items() if value}
