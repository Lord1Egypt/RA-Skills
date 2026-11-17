"""Small security helpers shared by the runtime modules."""

import re
from pathlib import Path
from typing import Any


SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
_CONTROL_SEQUENCES = (
    ("ignore", "all"),
    ("ignore", "previous"),
    ("ignore", "earlier"),
    ("system", "prompt"),
    ("developer", "message"),
    ("override", "all"),
    ("override", "safety"),
    ("override", "instructions"),
    ("run", "shell"),
    ("run", "command"),
    ("run", "tool"),
    ("write", "to", "file"),
    ("delete", "file"),
    ("grant", "access"),
)
CONTROL_TEXT = re.compile(
    "|".join(r"\s+".join(map(re.escape, sequence)) for sequence in _CONTROL_SEQUENCES),
    re.IGNORECASE,
)


def validate_identifier(value: str, field_name: str) -> str:
    """Validate an identifier before it participates in a filesystem path."""
    if not isinstance(value, str) or not SAFE_IDENTIFIER.fullmatch(value):
        raise ValueError(
            f"{field_name} must match [A-Za-z0-9][A-Za-z0-9_-]{{0,63}}"
        )
    return value


def resolve_child_path(base_dir: Path, relative_path: str, field_name: str) -> Path:
    """Resolve a path and require it to remain below the given directory."""
    if not isinstance(relative_path, str) or not relative_path:
        raise ValueError(f"{field_name} must be a non-empty relative path")

    raw_path = Path(relative_path)
    if raw_path.is_absolute():
        raise ValueError(f"{field_name} must be relative")

    base = Path(base_dir).expanduser().resolve()
    candidate = (base / raw_path).resolve()
    try:
        candidate.relative_to(base)
    except ValueError as exc:
        raise ValueError(f"{field_name} escapes its allowed directory") from exc
    return candidate


def validate_bounded_data(value: Any, field_name: str = "value", depth: int = 0) -> None:
    """Reject oversized or structurally hostile imported JSON data."""
    if depth > 8:
        raise ValueError(f"{field_name} is nested too deeply")

    if isinstance(value, str):
        if len(value) > 4000:
            raise ValueError(f"{field_name} is too long")
        if "\x00" in value:
            raise ValueError(f"{field_name} contains a null byte")
        return

    if isinstance(value, dict):
        if len(value) > 128:
            raise ValueError(f"{field_name} has too many fields")
        for key, item in value.items():
            if not isinstance(key, str) or len(key) > 128:
                raise ValueError(f"{field_name} contains an invalid field name")
            validate_bounded_data(item, f"{field_name}.{key}", depth + 1)
        return

    if isinstance(value, list):
        if len(value) > 256:
            raise ValueError(f"{field_name} has too many items")
        for index, item in enumerate(value):
            validate_bounded_data(item, f"{field_name}[{index}]", depth + 1)
        return

    if value is None or isinstance(value, (bool, int, float)):
        return

    raise ValueError(f"{field_name} contains an unsupported value")


def safe_prompt_text(value: Any, field_name: str, max_length: int = 500) -> str:
    """Return bounded persona text, filtering instruction-like control language."""
    if not isinstance(value, str):
        return ""
    text = value.replace("\x00", "").strip()
    if len(text) > max_length:
        text = text[:max_length]
    if CONTROL_TEXT.search(text):
        return "[persona text filtered]"
    return text
