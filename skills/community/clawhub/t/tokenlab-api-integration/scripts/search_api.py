#!/usr/bin/env python3
"""Read-only TokenLab public model discovery and detail inspection."""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


DEFAULT_API_BASE = "https://api.tokenlab.sh"
OWNER_NATIVE_FORMAT = {
    "anthropic": "anthropic_messages",
    "google": "gemini_generate_content",
    "openai": "openai_responses",
}
FORMAT_ENDPOINT = {
    "systemone": "/v1/systemone",
    "anthropic_messages": "/v1/messages",
    "gemini_generate_content": "/v1beta/models/{model}:generateContent",
    "openai_responses": "/v1/responses",
    "openai_chat_completions": "/v1/chat/completions",
}
HARNESS_FORMATS = {
    "anthropic_messages",
    "openai_responses",
    "openai_chat_completions",
}


def api_base() -> str:
    return os.getenv("TOKENLAB_API_BASE", DEFAULT_API_BASE).rstrip("/")


def request_json(path: str, query: dict[str, str] | None = None) -> dict[str, Any]:
    suffix = f"?{urlencode(query)}" if query else ""
    request = Request(f"{api_base()}{path}{suffix}", headers={"Accept": "application/json"})
    api_key = os.getenv("TOKENLAB_API_KEY")
    if api_key:
        request.add_header("Authorization", f"Bearer {api_key}")
    try:
        with urlopen(request, timeout=30) as response:  # noqa: S310 - fixed/explicit TokenLab base
            body = response.read().decode("utf-8")
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"TokenLab HTTP {error.code}: {body[:1000]}") from error
    except URLError as error:
        raise RuntimeError(f"TokenLab request failed: {error.reason}") from error
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as error:
        raise RuntimeError("TokenLab returned a non-JSON response") from error
    if not isinstance(parsed, dict):
        raise RuntimeError("TokenLab response must be a JSON object")
    return parsed


def tokenlab_extension(model: dict[str, Any]) -> dict[str, Any]:
    value = model.get("tokenlab")
    return value if isinstance(value, dict) else {}


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def request_contract(model: dict[str, Any]) -> dict[str, Any]:
    """Keep the published operation contract, preferring full detail over summaries."""
    extension = tokenlab_extension(model)
    for name in ("request_format_details", "public_contract", "request_format_summary", "public_contract_summary"):
        value = extension.get(name)
        if isinstance(value, dict) and value:
            return value
    return {}


def model_search_text(model: dict[str, Any]) -> str:
    extension = tokenlab_extension(model)
    fields = [
        model.get("id"),
        model.get("owned_by"),
        extension.get("category"),
        *string_list(extension.get("capabilities")),
        *string_list(extension.get("badges")),
    ]
    return " ".join(str(value) for value in fields if value is not None).lower()


def preferred_endpoint(model: dict[str, Any], client: str) -> tuple[str | None, str]:
    extension = tokenlab_extension(model)
    formats = string_list(extension.get("accepted_request_formats"))
    owner = str(model.get("owned_by", "")).lower()
    owner_native = OWNER_NATIVE_FORMAT.get(owner)
    allowed = set(formats)
    if client == "harness":
        allowed &= HARNESS_FORMATS
    elif client == "chat":
        allowed &= {"openai_chat_completions"}

    if owner_native in allowed:
        selected = owner_native
        return FORMAT_ENDPOINT[selected].format(model=model.get("id", "{model}")), "owner-native"
    for candidate in (
        "openai_chat_completions",
        "openai_responses",
        "anthropic_messages",
        "gemini_generate_content",
        "systemone",
    ):
        if candidate in allowed:
            return FORMAT_ENDPOINT[candidate].format(model=model.get("id", "{model}")), "declared-fallback"
    if client == "harness" and "gemini_generate_content" in formats:
        return None, "Gemini native is declared but current DeepSeek Harness cannot configure it"
    if not formats:
        endpoint = request_contract(model).get("request_endpoint")
        if isinstance(endpoint, str) and endpoint:
            return endpoint, "public-operation-contract (API/MCP, not a chat-provider route)"
        return None, "inspect --detail MODEL_ID for operation endpoints and request constraints"
    return None, "no declared format supported by this client"


def summarize(model: dict[str, Any], client: str, *, include_contract: bool = False) -> dict[str, Any]:
    extension = tokenlab_extension(model)
    endpoint, endpoint_reason = preferred_endpoint(model, client)
    pricing = extension.get("pricing") if isinstance(extension.get("pricing"), dict) else {}
    return {
        "id": model.get("id"),
        "owned_by": model.get("owned_by"),
        "category": extension.get("category"),
        "capabilities": string_list(extension.get("capabilities")),
        "accepted_request_formats": string_list(extension.get("accepted_request_formats")),
        "preferred_endpoint": endpoint,
        "endpoint_reason": endpoint_reason,
        "max_input_tokens": extension.get("max_input_tokens"),
        "max_output_tokens": extension.get("max_output_tokens"),
        "pricing": pricing,
        "lifecycle": extension.get("lifecycle"),
        **({"request_contract": request_contract(model)} if include_contract else {}),
    }


def print_human(models: list[dict[str, Any]], client: str, *, include_contract: bool = False) -> None:
    for index, model in enumerate(models, start=1):
        summary = summarize(model, client)
        print(f"{index}. {summary['id']} ({summary['owned_by']})")
        if summary["category"]:
            print(f"   category: {summary['category']}")
        if summary["capabilities"]:
            print(f"   capabilities: {', '.join(summary['capabilities'])}")
        if summary["accepted_request_formats"]:
            print(f"   request formats: {', '.join(summary['accepted_request_formats'])}")
        print(f"   preferred endpoint: {summary['preferred_endpoint'] or 'inspect detail'} ({summary['endpoint_reason']})")
        if include_contract and request_contract(model):
            print("   request contract: " + json.dumps(request_contract(model), ensure_ascii=False, indent=2))
        pricing = summary["pricing"]
        if pricing:
            print(
                "   pricing: "
                f"input={pricing.get('input_per_1m')} output={pricing.get('output_per_1m')} "
                f"per_request={pricing.get('per_request')} {pricing.get('currency', 'USD')}"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search TokenLab's live public model catalog without guessing categories from model names."
    )
    parser.add_argument("keyword", nargs="?", help="case-insensitive text in id, owner, category, or capability")
    parser.add_argument("--category", help="public model category, for example chat, image, video, music, 3d, audio, decision")
    parser.add_argument("--tag", help="public capability/tag filter sent to TokenLab")
    parser.add_argument("--detail", metavar="MODEL_ID", help="fetch chat formats and the complete published media operation contract")
    parser.add_argument("--client", choices=("general", "harness", "chat"), default="general",
                        help="preferred chat protocol; media API endpoints always follow the published operation contract")
    parser.add_argument("--limit", type=int, default=50, help="maximum displayed models (1-500, default 50)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.limit < 1 or args.limit > 500:
        raise RuntimeError("--limit must be from 1 through 500")

    if args.detail:
        detail = request_json(f"/v1/models/{quote(args.detail, safe='')}")
        output = summarize(detail, args.client, include_contract=True)
        if args.json:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print_human([detail], args.client, include_contract=True)
        return 0

    query = {}
    if args.category:
        query["category"] = args.category
    if args.tag:
        query["tag"] = args.tag
    listing = request_json("/v1/models", query)
    data = listing.get("data")
    if not isinstance(data, list):
        raise RuntimeError("TokenLab model listing is missing data[]")
    models = [model for model in data if isinstance(model, dict)]
    if args.keyword:
        keyword = args.keyword.lower()
        models = [model for model in models if keyword in model_search_text(model)]
    models = models[: args.limit]
    if args.json:
        print(json.dumps([summarize(model, args.client) for model in models], ensure_ascii=False, indent=2))
    else:
        print(f"TokenLab public models: {len(models)} shown")
        print_human(models, args.client)
        if models and not any(tokenlab_extension(model).get("accepted_request_formats") for model in models):
            print("\nUse --detail MODEL_ID before choosing a protocol; list responses do not guarantee format detail.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
