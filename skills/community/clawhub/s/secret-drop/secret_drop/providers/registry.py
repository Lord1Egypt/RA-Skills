"""Provider selection without exposing returned plaintext."""

from __future__ import annotations

from secret_drop.errors import SecretDropError
from secret_drop.providers import pwpush, snappwd

PROVIDERS = ("pwpush", "snappwd")


def detect_provider(url: str) -> str:
    if snappwd.matches(url):
        return "snappwd"
    if pwpush.matches(url):
        return "pwpush"
    raise SecretDropError("Could not detect the provider. Pass --provider pwpush|snappwd.")


def retrieve_secret(
    url: str,
    *,
    provider: str = "auto",
    api_base: str | None = None,
    allow_private: bool = False,
) -> tuple[str, str]:
    selected = detect_provider(url) if provider == "auto" else provider
    if selected not in PROVIDERS:
        raise SecretDropError(f"Unsupported provider: {selected}")
    if selected == "pwpush":
        return selected, pwpush.retrieve(url, allow_private=allow_private, api_base=api_base)
    return selected, snappwd.retrieve(url, allow_private=allow_private, api_base=api_base)
