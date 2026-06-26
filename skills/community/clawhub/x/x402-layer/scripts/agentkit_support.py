#!/usr/bin/env python3
"""
Helpers for World AgentKit support in x402-layer.

This module keeps the skill Python-first while generating the same
AgentKit header shape the worker validates.
"""

import base64
import json
from typing import Any, Dict, List, Optional

from wallet_signing import sign_evm_message

AGENTKIT_HEADER = "agentkit"
BASE_AGENTKIT_CHAIN = "eip155:8453"


def extract_agentkit_extension(challenge: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    extensions = challenge.get("extensions") or {}
    extension = extensions.get(AGENTKIT_HEADER)
    return extension if isinstance(extension, dict) else None


def summarize_agentkit_extension(extension: Dict[str, Any]) -> str:
    mode = ((extension.get("mode") or {}).get("type") or "").strip().lower()

    if mode == "free":
        return "free access for verified human-backed agent wallets"
    if mode == "free-trial":
        uses = (extension.get("mode") or {}).get("uses") or 1
        return f"{uses} free request{'s' if uses != 1 else ''} for verified human-backed agent wallets"
    if mode == "discount":
        percent = (extension.get("mode") or {}).get("percent") or 0
        return f"{percent}% discount for verified human-backed agent wallets"

    return "a human-backed agent wallet benefit"


def get_supported_base_agentkit_chain(extension: Dict[str, Any]) -> Optional[Dict[str, str]]:
    supported = extension.get("supportedChains") or []
    for item in supported:
        if not isinstance(item, dict):
            continue
        if item.get("chainId") == BASE_AGENTKIT_CHAIN and item.get("type") == "eip191":
            return {"chainId": item["chainId"], "type": item["type"]}
    return None


def _format_siwe_message(
    *,
    domain: str,
    address: str,
    statement: Optional[str],
    uri: str,
    version: str,
    chain_id: str,
    nonce: str,
    issued_at: str,
    expiration_time: Optional[str] = None,
    not_before: Optional[str] = None,
    request_id: Optional[str] = None,
    resources: Optional[List[str]] = None,
) -> str:
    numeric_chain_id = chain_id.split(":", 1)[1]
    lines = [f"{domain} wants you to sign in with your Ethereum account:", address, ""]

    if statement:
        lines.extend([statement, ""])

    lines.extend(
        [
            f"URI: {uri}",
            f"Version: {version}",
            f"Chain ID: {numeric_chain_id}",
            f"Nonce: {nonce}",
            f"Issued At: {issued_at}",
        ]
    )

    if expiration_time:
        lines.append(f"Expiration Time: {expiration_time}")
    if not_before:
        lines.append(f"Not Before: {not_before}")
    if request_id:
        lines.append(f"Request ID: {request_id}")
    if resources:
        lines.append("Resources:")
        for resource in resources:
            lines.append(f"- {resource}")

    return "\n".join(lines)


def build_agentkit_header(extension: Dict[str, Any], wallet_address: str) -> str:
    info = extension.get("info") or {}
    supported = get_supported_base_agentkit_chain(extension)
    if not supported:
        raise ValueError("This AgentKit challenge does not support Base eip191 signing")

    payload: Dict[str, Any] = {
        "domain": info.get("domain"),
        "address": wallet_address,
        "statement": info.get("statement"),
        "uri": info.get("uri"),
        "version": info.get("version", "1"),
        "chainId": supported["chainId"],
        "type": supported["type"],
        "nonce": info.get("nonce"),
        "issuedAt": info.get("issuedAt"),
        "resources": info.get("resources") or [info.get("uri")],
    }

    if info.get("expirationTime"):
        payload["expirationTime"] = info["expirationTime"]
    if info.get("notBefore"):
        payload["notBefore"] = info["notBefore"]
    if info.get("requestId"):
        payload["requestId"] = info["requestId"]

    required = ["domain", "address", "uri", "version", "chainId", "type", "nonce", "issuedAt"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        raise ValueError(f"AgentKit challenge is missing required fields: {', '.join(missing)}")

    message = _format_siwe_message(
        domain=str(payload["domain"]),
        address=str(payload["address"]),
        statement=str(payload.get("statement")) if payload.get("statement") else None,
        uri=str(payload["uri"]),
        version=str(payload["version"]),
        chain_id=str(payload["chainId"]),
        nonce=str(payload["nonce"]),
        issued_at=str(payload["issuedAt"]),
        expiration_time=str(payload.get("expirationTime")) if payload.get("expirationTime") else None,
        not_before=str(payload.get("notBefore")) if payload.get("notBefore") else None,
        request_id=str(payload.get("requestId")) if payload.get("requestId") else None,
        resources=[str(item) for item in (payload.get("resources") or []) if item],
    )
    payload["signature"] = sign_evm_message(message)

    return base64.b64encode(json.dumps(payload).encode()).decode()


def registration_guidance(wallet_address: str) -> str:
    return "\n".join(
        [
            "Human-backed agent benefit is available for this endpoint.",
            f"Register the wallet that signs agent requests in AgentBook: npx @worldcoin/agentkit-cli register {wallet_address}",
            "A human must complete the World App verification flow during registration.",
            "After registration succeeds, retry this request with AgentKit enabled.",
        ]
    )
