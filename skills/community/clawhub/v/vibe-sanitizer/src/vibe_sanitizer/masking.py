from __future__ import annotations

import re


def mask_token(value: str, *, keep_prefix: int = 4, keep_suffix: int = 4) -> str:
    if len(value) <= keep_prefix + keep_suffix + 3:
        return value[:keep_prefix] + "***"
    return value[:keep_prefix] + "***" + value[-keep_suffix:]


def mask_bearer_token(token: str) -> str:
    return "Bearer " + mask_token(token, keep_prefix=3, keep_suffix=4)


def sanitize_credential_url(url: str, user_placeholder: str, password_placeholder: str) -> str:
    pattern = re.compile(
        r"(?P<scheme>[A-Za-z][A-Za-z0-9+.-]{1,20})://"
        r"(?P<user>[^/\s:@]+):(?P<password>[^@\s/]+)@(?P<rest>[^\s'\"`<>]+)"
    )
    match = pattern.search(url)
    if not match:
        return url
    return (
        f"{match.group('scheme')}://{user_placeholder}:{password_placeholder}"
        f"@{match.group('rest')}"
    )


def preview_credential_url(url: str) -> str:
    return sanitize_credential_url(url, "***", "***")
