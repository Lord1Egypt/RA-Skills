#!/usr/bin/env python3
from __future__ import annotations

from typing import Any


JOINED_CLAIM_KINDS = frozenset(
    {"granted", "already_claimed", "obtained_after_registration"}
)


def claim_response_succeeded(response: dict[str, Any]) -> bool:
    return response.get("code", 200) == 200


def claim_data_from_response(response: dict[str, Any]) -> dict[str, Any]:
    data = response.get("data")
    return data if isinstance(data, dict) else {}


def normalize_claim_data_in_place(
    response: dict[str, Any],
    requested_mobile: str,
    previous_activity_joined: bool | None,
) -> dict[str, Any]:
    """Normalize response.data in place for rendering and local state decisions."""
    data = claim_data_from_response(response)
    if not data or not claim_response_succeeded(response):
        return data

    data.setdefault("requestedMobile", requested_mobile)
    if data.get("kind") == "already_claimed" and previous_activity_joined is False:
        data["kind"] = "obtained_after_registration"

    return data


def is_joined_claim_kind(kind: Any) -> bool:
    return kind in JOINED_CLAIM_KINDS
