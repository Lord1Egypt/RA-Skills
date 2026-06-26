#!/usr/bin/env python3
"""Billing, top-up, and 402 recovery helpers for OpenMarlin."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from openclaw_skill_config import (
    DEFAULT_SERVER_URL,
    build_server_connection_error,
    get_skill_env,
    probe_server_openapi,
    require_server_url,
)
from openclaw_billing_state import (
    get_last_balance_snapshot,
    list_topup_sessions,
    record_balance_snapshot,
    record_topup_session,
)
from openclaw_platform_auth import DEFAULT_AGENT_ID, DEFAULT_PROFILE_ID, resolve_platform_api_key


DEFAULT_TIMEOUT_SECONDS = 300.0
DEFAULT_POLL_INTERVAL_SECONDS = 2.0


def parse_args() -> argparse.Namespace:
    default_server_url, server_url_source = get_skill_env("OPENMARLIN_SERVER_URL")
    default_api_key, _api_key_source = get_skill_env("OPENMARLIN_PLATFORM_API_KEY")
    common = argparse.ArgumentParser(add_help=False)
    common.set_defaults(_server_url_source=server_url_source)
    common.add_argument(
        "--server-url",
        default=(default_server_url or "").strip(),
        help=f"Base URL for the OpenMarlin server. Defaults to OPENMARLIN_SERVER_URL, then OpenClaw skill config, then {DEFAULT_SERVER_URL}. Do not include /v1.",
    )
    common.add_argument(
        "--api-key",
        default=(default_api_key or "").strip(),
        help="Platform API key. Defaults to OPENMARLIN_PLATFORM_API_KEY, then OpenClaw auth-profiles.json.",
    )
    common.add_argument(
        "--profile-id",
        default=DEFAULT_PROFILE_ID,
        help=f"OpenClaw auth profile ID used when resolving a stored platform key. Default: {DEFAULT_PROFILE_ID}.",
    )
    common.add_argument(
        "--agent-id",
        default=DEFAULT_AGENT_ID,
        help=f"OpenClaw agent ID used when resolving a stored platform key. Default: {DEFAULT_AGENT_ID}.",
    )
    common.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON output when possible.",
    )
    common.add_argument(
        "--dry-run",
        action="store_true",
        help="Show resolved configuration and a lightweight connectivity check without executing the command.",
    )

    parser = argparse.ArgumentParser(
        description="Handle OpenMarlin billing, top-up, and structured 402 recovery flows.",
        parents=[common],
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    explain = subparsers.add_parser("explain-402", help="Explain a structured 402 response.", parents=[common])
    explain.add_argument("--response-json", help="Raw JSON object payload for the 402 response.")
    explain.add_argument("--response-file", help="Path to a JSON file containing the 402 response.")
    explain.add_argument(
        "--auto-recover",
        action="store_true",
        help="Immediately create a top-up session for the shortfall after explaining the 402.",
    )

    create = subparsers.add_parser("create-topup", help="Create a top-up session.", parents=[common])
    create.add_argument("--amount", type=float, help="Requested top-up amount in credits.")
    create.add_argument("--response-json", help="Optional 402 response JSON used to derive a suggested amount.")
    create.add_argument("--response-file", help="Optional 402 response JSON file used to derive a suggested amount.")

    balance = subparsers.add_parser(
        "balance",
        help="Show the authoritative current balance for the authenticated workspace.",
        parents=[common],
    )
    balance.add_argument("--workspace-id", help="Optional workspace ID used only for local fallback context.")
    balance.add_argument("--response-json", help="Optional structured 402 response JSON used to refresh local context first.")
    balance.add_argument("--response-file", help="Optional structured 402 response JSON file used to refresh local context first.")

    history = subparsers.add_parser("history", help="Show tracked top-up sessions for a workspace.", parents=[common])
    history.add_argument("--workspace-id", help="Optional workspace ID filter.")
    history.add_argument("--limit", type=int, default=10, help="Maximum sessions to show. Default: 10.")

    activity = subparsers.add_parser(
        "activity",
        help="Show recent caller billing activity from /v1/usage-events and /v1/ledger.",
        parents=[common],
    )
    activity.add_argument("--limit", type=int, default=10, help="Maximum usage events and ledger entries to show. Default: 10.")

    subparsers.add_parser(
        "referral-link",
        help="Fetch the caller's referral code, invite link, and current attribution summary.",
        parents=[common],
    )

    status = subparsers.add_parser("status", help="Fetch the current top-up session state.", parents=[common])
    status.add_argument("--session-id", required=True, help="Top-up session ID.")

    watch = subparsers.add_parser("watch", help="Wait for a top-up session to complete or fail.", parents=[common])
    watch.add_argument("--session-id", required=True, help="Top-up session ID.")
    watch.add_argument(
        "--interval-seconds",
        type=float,
        default=DEFAULT_POLL_INTERVAL_SECONDS,
        help=f"Polling interval in seconds. Default: {DEFAULT_POLL_INTERVAL_SECONDS}.",
    )
    watch.add_argument(
        "--timeout-seconds",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Maximum total wait time in seconds. Default: {DEFAULT_TIMEOUT_SECONDS}.",
    )

    return parser.parse_args()


def require_non_empty(value: str, message: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise SystemExit(message)
    return normalized


def resolve_api_key(raw_api_key: str, profile_id: str, agent_id: str) -> tuple[str | None, str | None, str | None]:
    if raw_api_key.strip():
        return raw_api_key.strip(), "env-or-flag", None

    key, _profile, auth_store_path = resolve_platform_api_key(profile_id=profile_id, agent_id=agent_id)
    if key:
        return key, f"auth-profiles:{auth_store_path}", None

    return None, None, (
        "Missing platform API key. Set OPENMARLIN_PLATFORM_API_KEY, pass --api-key, "
        "or bootstrap and store a key first."
    )


def resolve_api_key_or_exit(raw_api_key: str, profile_id: str, agent_id: str) -> tuple[str, str]:
    key, source, error = resolve_api_key(raw_api_key, profile_id, agent_id)
    if error:
        raise SystemExit(error)
    assert key is not None and source is not None
    return key, source


def load_json_object(raw: str, *, source: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON in {source}: {error}") from error
    if not isinstance(parsed, dict):
        raise SystemExit(f"{source} must decode to a JSON object.")
    return parsed


def load_json_object_from_option(raw: str | None, path: str | None, *, source_name: str) -> dict[str, Any]:
    if bool(raw) == bool(path):
        raise SystemExit(f"Provide exactly one of {source_name}-json or {source_name}-file.")
    if raw:
        return load_json_object(raw, source=f"--{source_name}-json")
    with open(path, "r", encoding="utf-8") as handle:
        return load_json_object(handle.read(), source=f"--{source_name}-file")


def request_json(url: str, method: str = "GET", headers: dict[str, str] | None = None, payload: dict[str, Any] | None = None) -> tuple[int, dict[str, Any] | str]:
    body = None
    merged_headers = {"Accept": "application/json"}
    if headers:
        merged_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        merged_headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=body, method=method, headers=merged_headers)
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        try:
            payload_obj = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload_obj = raw
        return error.code, payload_obj
    except urllib.error.URLError as error:
        parsed = urllib.parse.urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else url
        raise SystemExit(build_server_connection_error(base_url, str(error.reason))) from error


def parse_workspace_balance(payload: dict[str, Any]) -> dict[str, Any] | None:
    workspace_id = payload.get("workspace_id")
    available = payload.get("available_balance")
    updated_at = payload.get("updated_at")
    if not isinstance(workspace_id, str) or not isinstance(available, dict):
        return None

    amount = available.get("amount")
    unit = available.get("unit")
    if not isinstance(amount, (int, float)) or not isinstance(unit, str):
        return None
    if updated_at is not None and not isinstance(updated_at, str):
        return None

    return {
        "workspace_id": workspace_id,
        "available_balance": {
            "amount": float(amount),
            "unit": unit,
        },
        "updated_at": updated_at,
    }


def parse_insufficient_balance(payload: dict[str, Any]) -> dict[str, Any] | None:
    if payload.get("error_code") != "insufficient_balance":
        return None

    current = payload.get("current_balance")
    required = payload.get("required_balance")
    if not isinstance(current, dict) or not isinstance(required, dict):
        return None

    current_amount = current.get("amount")
    required_amount = required.get("amount")
    unit = current.get("unit")
    if not isinstance(current_amount, (int, float)) or not isinstance(required_amount, (int, float)):
        return None
    if not isinstance(unit, str) or unit != required.get("unit"):
        return None

    shortfall = max(float(required_amount) - float(current_amount), 0.0)
    return {
        "workspace_id": payload.get("workspace_id"),
        "message": payload.get("message"),
        "current_balance": {"amount": float(current_amount), "unit": unit},
        "required_balance": {"amount": float(required_amount), "unit": unit},
        "shortfall": {"amount": shortfall, "unit": unit},
    }


def build_recovery_commands(summary: dict[str, Any]) -> list[str]:
    amount = summary["shortfall"]["amount"]
    rendered_amount = int(amount) if float(amount).is_integer() else amount
    return [
        f"python3 scripts/billing.py create-topup --amount {rendered_amount}",
        "python3 scripts/billing.py watch --session-id <topup-session-id>",
    ]


def derive_topup_amount(args: argparse.Namespace) -> float:
    if args.amount is not None:
        if args.amount <= 0:
            raise SystemExit("--amount must be greater than 0.")
        return args.amount

    payload = load_json_object_from_option(args.response_json, args.response_file, source_name="response")
    summary = parse_insufficient_balance(payload)
    if not summary:
        raise SystemExit("The provided response is not a structured insufficient_balance payload.")
    amount = summary["shortfall"]["amount"]
    return amount if amount > 0 else summary["required_balance"]["amount"]


def derive_topup_amount_from_summary(summary: dict[str, Any]) -> float:
    amount = summary["shortfall"]["amount"]
    return amount if amount > 0 else summary["required_balance"]["amount"]


def remember_402_summary(summary: dict[str, Any], *, agent_id: str) -> dict[str, Any]:
    workspace_id = summary.get("workspace_id")
    if not isinstance(workspace_id, str) or not workspace_id.strip():
        raise SystemExit("Structured insufficient_balance payload is missing workspace_id.")
    return record_balance_snapshot(
        workspace_id=workspace_id,
        amount=summary["current_balance"]["amount"],
        unit=summary["current_balance"]["unit"],
        agent_id=agent_id,
        source="structured_402",
        estimated=False,
        message=summary.get("message"),
        required_amount=summary["required_balance"]["amount"],
        reference={"error_code": "insufficient_balance"},
    )


def remember_authoritative_balance(balance: dict[str, Any], *, agent_id: str) -> dict[str, Any]:
    return record_balance_snapshot(
        workspace_id=balance["workspace_id"],
        amount=balance["available_balance"]["amount"],
        unit=balance["available_balance"]["unit"],
        agent_id=agent_id,
        source="authoritative_balance_api",
        estimated=False,
        message="Fetched from GET /v1/balance.",
        reference={"updated_at": balance.get("updated_at")},
    )


def fetch_authoritative_balance(server_url: str, auth_headers: dict[str, str]) -> tuple[int, dict[str, Any] | str]:
    return request_json(f"{server_url}/v1/balance", headers=auth_headers)


def fetch_usage_events(server_url: str, auth_headers: dict[str, str]) -> tuple[int, dict[str, Any] | str]:
    return request_json(f"{server_url}/v1/usage-events", headers=auth_headers)


def fetch_ledger_entries(server_url: str, auth_headers: dict[str, str]) -> tuple[int, dict[str, Any] | str]:
    return request_json(f"{server_url}/v1/ledger", headers=auth_headers)


def fetch_referral_link(server_url: str, auth_headers: dict[str, str]) -> tuple[int, dict[str, Any] | str]:
    return request_json(f"{server_url}/v1/referrals/me", headers=auth_headers)


def update_balance_from_completed_topup(
    session: dict[str, Any],
    *,
    agent_id: str,
) -> dict[str, Any] | None:
    if session.get("status") != "credit_applied":
        return None

    workspace_id = session.get("workspace_id")
    requested_amount = session.get("requested_amount")
    if not isinstance(workspace_id, str) or not isinstance(requested_amount, dict):
        return None
    amount = requested_amount.get("amount")
    unit = requested_amount.get("unit")
    if not isinstance(amount, (int, float)) or not isinstance(unit, str):
        return None

    previous_snapshot, _state_path = get_last_balance_snapshot(workspace_id=workspace_id, agent_id=agent_id)
    if not previous_snapshot:
        return None
    previous_amount = previous_snapshot.get("amount")
    previous_unit = previous_snapshot.get("unit")
    if not isinstance(previous_amount, (int, float)) or previous_unit != unit:
        return None

    return record_balance_snapshot(
        workspace_id=workspace_id,
        amount=float(previous_amount) + float(amount),
        unit=unit,
        agent_id=agent_id,
        source="topup_session_credit_applied",
        estimated=bool(previous_snapshot.get("estimated")),
        message="Updated from a completed Stripe top-up session.",
        reference={
            "topup_session_id": session.get("topup_session_id"),
            "credited_ledger_entry_id": session.get("credited_ledger_entry_id"),
            "base_observed_at": previous_snapshot.get("observed_at"),
        },
    )


def print_402_summary(summary: dict[str, Any]) -> None:
    print(summary.get("message") or "Workspace balance is insufficient for this request.")
    print(f"Workspace ID: {summary.get('workspace_id', '<unknown>')}")
    print(
        f"Current balance: {summary['current_balance']['amount']} {summary['current_balance']['unit']}"
    )
    print(
        f"Required balance: {summary['required_balance']['amount']} {summary['required_balance']['unit']}"
    )
    print(f"Shortfall: {summary['shortfall']['amount']} {summary['shortfall']['unit']}")
    print("Recovery:")
    for command in build_recovery_commands(summary):
        print(f"  {command}")


def create_topup_session(server_url: str, auth_headers: dict[str, str], amount: float) -> tuple[int, dict[str, Any] | str]:
    return request_json(
        f"{server_url}/v1/topup/sessions",
        method="POST",
        headers=auth_headers,
        payload={"amount": amount},
    )


def print_topup_session(payload: dict[str, Any]) -> None:
    print(f"Top-up session ID: {payload.get('topup_session_id', '<unknown>')}")
    print(f"Workspace ID: {payload.get('workspace_id', '<unknown>')}")
    requested_amount = payload.get("requested_amount")
    if isinstance(requested_amount, dict):
        print(
            f"Requested amount: {requested_amount.get('amount', '<unknown>')} {requested_amount.get('unit', '<unknown>')}"
        )
    print(f"Status: {payload.get('status', '<unknown>')}")
    print(f"Created at: {payload.get('created_at', '<unknown>')}")
    print(f"Completed at: {payload.get('completed_at', '<unknown>')}")
    print(f"Stripe reference: {payload.get('stripe_reference', '<unknown>')}")
    print(f"Checkout URL: {payload.get('checkout_url', '<unknown>')}")
    print(f"Credited ledger entry ID: {payload.get('credited_ledger_entry_id', '<unknown>')}")
    print("Next step: open the checkout URL only for the Stripe payment step, then return to OpenClaw and watch the session.")


def print_balance_snapshot(snapshot: dict[str, Any], state_path: str) -> None:
    print(f"Workspace ID: {snapshot.get('workspace_id', '<unknown>')}")
    label = "Authoritative balance" if snapshot.get("source") == "authoritative_balance_api" else "Last known balance"
    print(f"{label}: {snapshot.get('amount', '<unknown>')} {snapshot.get('unit', '<unknown>')}")
    print(f"Observed at: {snapshot.get('observed_at', '<unknown>')}")
    print(f"Source: {snapshot.get('source', '<unknown>')}")
    print(f"Estimated: {'yes' if snapshot.get('estimated') else 'no'}")
    updated_at = (snapshot.get("reference") or {}).get("updated_at")
    if updated_at:
        print(f"Server updated at: {updated_at}")
    required_amount = snapshot.get("required_amount")
    if required_amount is not None:
        print(f"Required balance from last 402: {required_amount} {snapshot.get('unit', '<unknown>')}")
    message = snapshot.get("message")
    if message:
        print(f"Message: {message}")
    print(f"Billing state path: {state_path}")


def print_history(sessions: list[dict[str, Any]], state_path: str) -> None:
    print(f"Billing state path: {state_path}")
    if not sessions:
        print("Tracked top-up sessions: none")
        return
    print("Tracked top-up sessions:")
    for session in sessions:
        amount = session.get("requested_amount")
        rendered_amount = "<unknown>"
        if isinstance(amount, dict):
            rendered_amount = f"{amount.get('amount', '<unknown>')} {amount.get('unit', '<unknown>')}"
        print(
            f"- {session.get('topup_session_id', '<unknown>')} "
            f"workspace={session.get('workspace_id', '<unknown>')} "
            f"status={session.get('status', '<unknown>')} "
            f"amount={rendered_amount} "
            f"credited_ledger_entry_id={session.get('credited_ledger_entry_id', '<unknown>')}"
        )


def list_payload_data(payload: dict[str, Any] | str, *, field_name: str) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        raise SystemExit(f"Server returned a non-object payload for {field_name}.")
    data = payload.get("data")
    if not isinstance(data, list):
        raise SystemExit(f"Server returned an invalid list payload for {field_name}.")
    return [item for item in data if isinstance(item, dict)]


def sort_records_by_created_at(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(records, key=lambda item: str(item.get("created_at", "")), reverse=True)


def trim_records(records: list[dict[str, Any]], *, limit: int) -> list[dict[str, Any]]:
    if limit <= 0:
        return []
    return sort_records_by_created_at(records)[:limit]


def format_amount_object(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    amount = value.get("amount")
    unit = value.get("unit")
    if isinstance(amount, (int, float)) and isinstance(unit, str) and unit.strip():
        return f"{amount} {unit}"
    return None


def format_converted_final_debit(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    amount = value.get("amount")
    unit = value.get("unit")
    usd_per_credit = value.get("usdPerCredit")
    if isinstance(amount, (int, float)) and isinstance(unit, str) and unit.strip():
        if isinstance(usd_per_credit, (int, float)):
            return f"{amount} {unit} (usdPerCredit={usd_per_credit})"
        return f"{amount} {unit}"
    return None


def print_usage_events(events: list[dict[str, Any]]) -> None:
    if not events:
        print("Recent usage events: none")
        return
    print("Recent usage events:")
    for event in events:
        measured_units = event.get("measured_units")
        measured_text = "<unknown>"
        if isinstance(measured_units, dict):
            requests = measured_units.get("requests")
            if isinstance(requests, (int, float)):
                measured_text = f"requests={requests}"
            else:
                measured_text = json.dumps(measured_units, sort_keys=True)
        elif isinstance(measured_units, (int, float)):
            measured_text = str(measured_units)
        settlement = event.get("settlement")
        settlement_parts: list[str] = []
        if isinstance(settlement, dict):
            converted_final_debit = format_converted_final_debit(settlement.get("convertedFinalDebit"))
            if converted_final_debit:
                settlement_parts.append(f"final_debit={converted_final_debit}")
            final_total = format_amount_object(settlement.get("finalTotal"))
            if final_total:
                settlement_parts.append(f"final_total={final_total}")
            provider_subtotal = format_amount_object(settlement.get("providerReportedSubtotal"))
            if provider_subtotal:
                settlement_parts.append(f"provider_subtotal={provider_subtotal}")
            platform_fee_total = format_amount_object(settlement.get("platformFeeTotal"))
            if platform_fee_total:
                settlement_parts.append(f"platform_fee={platform_fee_total}")
        settlement_text = f" {' '.join(settlement_parts)}" if settlement_parts else ""
        print(
            f"- {event.get('created_at', '<unknown>')} "
            f"capability={event.get('capability', '<unknown>')} "
            f"status={event.get('status', '<unknown>')} "
            f"provider={event.get('provider_id', '<unknown>')} "
            f"request={event.get('request_id', '<unknown>')} "
            f"units={measured_text}{settlement_text}"
        )


def print_ledger_entries(entries: list[dict[str, Any]]) -> None:
    if not entries:
        print("Recent ledger entries: none")
        return
    print("Recent ledger entries:")
    for entry in entries:
        amount = entry.get("amount")
        amount_text = "<unknown>"
        if isinstance(amount, dict):
            amount_text = f"{amount.get('amount', '<unknown>')} {amount.get('unit', '<unknown>')}"
        print(
            f"- {entry.get('created_at', '<unknown>')} "
            f"type={entry.get('type', '<unknown>')} "
            f"status={entry.get('status', '<unknown>')} "
            f"amount={amount_text} "
            f"reference_id={entry.get('reference_id', '<unknown>')}"
        )


def parse_referral_link(payload: dict[str, Any]) -> dict[str, Any] | None:
    referral_code = payload.get("referral_code")
    referral_link = payload.get("referral_link")
    summary = payload.get("summary")
    if not isinstance(referral_code, str) or not referral_code.strip():
        return None
    if referral_link is not None and not isinstance(referral_link, str):
        return None
    if not isinstance(summary, dict):
        return None

    signed_up_count = summary.get("signed_up_count")
    qualified_count = summary.get("qualified_count")
    rewarded_count = summary.get("rewarded_count")
    if not all(isinstance(value, int) for value in (signed_up_count, qualified_count, rewarded_count)):
        return None

    return {
        "referral_code": referral_code,
        "referral_link": referral_link,
        "summary": {
            "signed_up_count": signed_up_count,
            "qualified_count": qualified_count,
            "rewarded_count": rewarded_count,
        },
    }


def print_referral_link(payload: dict[str, Any]) -> None:
    print(f"Referral code: {payload['referral_code']}")
    print(f"Referral link: {payload.get('referral_link') or '<unavailable>'}")
    summary = payload["summary"]
    print(
        "Attribution summary: "
        f"signed_up={summary['signed_up_count']} "
        f"qualified={summary['qualified_count']} "
        f"rewarded={summary['rewarded_count']}"
    )


def print_dry_run(args: argparse.Namespace) -> int:
    server_url = require_server_url(args.server_url)
    reachable, detail = probe_server_openapi(server_url)
    payload: dict[str, Any] = {
        "ok": reachable,
        "dry_run": True,
        "command": args.command,
        "server_url": server_url,
        "server_url_source": args._server_url_source or "flag-or-arg",
        "connectivity": detail,
    }

    needs_api_key = args.command in {"create-topup", "status", "watch", "balance", "activity", "referral-link"} or (
        args.command == "explain-402" and args.auto_recover
    )
    if needs_api_key:
        api_key, api_key_source, api_key_error = resolve_api_key(args.api_key, args.profile_id, args.agent_id)
        payload["api_key_source"] = api_key_source
        payload["api_key_error"] = api_key_error
        payload["ok"] = payload["ok"] and api_key_error is None

    if args.command == "explain-402":
        parsed = load_json_object_from_option(args.response_json, args.response_file, source_name="response")
        summary = parse_insufficient_balance(parsed)
        if not summary:
            raise SystemExit("The provided response is not a structured insufficient_balance payload.")
        payload["workspace_id"] = summary.get("workspace_id")
        payload["shortfall"] = summary["shortfall"]
        payload["auto_recover"] = args.auto_recover
    elif args.command == "create-topup":
        payload["amount"] = derive_topup_amount(args)
    elif args.command == "status":
        payload["session_id"] = args.session_id
    elif args.command == "watch":
        payload["session_id"] = args.session_id
        payload["interval_seconds"] = args.interval_seconds
        payload["timeout_seconds"] = args.timeout_seconds
    elif args.command == "balance":
        payload["workspace_id"] = args.workspace_id
    elif args.command == "history":
        payload["workspace_id"] = args.workspace_id
        payload["limit"] = args.limit
    elif args.command == "activity":
        payload["limit"] = args.limit
        payload["operations"] = ["GET /v1/usage-events", "GET /v1/ledger"]
    elif args.command == "referral-link":
        payload["operations"] = ["GET /v1/referrals/me"]

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("Dry run only. No payment recovery action was executed.")
        print(f"Command: {args.command}")
        print(f"Resolved server URL: {server_url}")
        print(f"Server URL source: {payload['server_url_source']}")
        print(f"Connectivity check: {detail}")
        if "api_key_error" in payload:
            if payload["api_key_error"]:
                print(f"API key: missing ({payload['api_key_error']})")
            else:
                print(f"API key source: {payload['api_key_source']}")
        if args.command == "explain-402":
            shortfall = payload["shortfall"]
            print(f"Workspace ID: {payload.get('workspace_id', '<unknown>')}")
            print(f"Shortfall: {shortfall['amount']} {shortfall['unit']}")
            print(f"Auto-recover: {'yes' if args.auto_recover else 'no'}")
        elif args.command == "create-topup":
            print(f"Requested amount: {payload['amount']}")
        elif "session_id" in payload:
            print(f"Session ID: {payload['session_id']}")
        elif args.command == "history":
            print(f"Limit: {payload['limit']}")
        elif args.command == "activity":
            print(f"Limit: {payload['limit']}")
            print("Operations: GET /v1/usage-events, GET /v1/ledger")
        elif args.command == "referral-link":
            print("Operation: GET /v1/referrals/me")
    return 0 if payload["ok"] else 1


def main() -> int:
    args = parse_args()
    if args.dry_run:
        return print_dry_run(args)

    if args.command == "explain-402":
        payload = load_json_object_from_option(args.response_json, args.response_file, source_name="response")
        summary = parse_insufficient_balance(payload)
        if not summary:
            raise SystemExit("The provided response is not a structured insufficient_balance payload.")
        stored = remember_402_summary(summary, agent_id=args.agent_id)
        auto_recovered = None
        auto_recovered_session = None
        if args.auto_recover:
            server_url = require_server_url(args.server_url)
            api_key, api_key_source = resolve_api_key_or_exit(args.api_key, args.profile_id, args.agent_id)
            auth_headers = {"Authorization": f"Bearer {api_key}"}
            amount = derive_topup_amount_from_summary(summary)
            status, topup_payload = create_topup_session(server_url, auth_headers, amount)
            if status >= 400:
                if args.json:
                    print(
                        json.dumps(
                            {
                                "ok": False,
                                "status": status,
                                "api_key_source": api_key_source,
                                "recovery": summary,
                                "commands": build_recovery_commands(summary),
                                "stored": stored,
                                "response": topup_payload,
                            },
                            indent=2,
                            sort_keys=True,
                        )
                    )
                else:
                    print_402_summary(summary)
                    print(f"Saved billing snapshot to: {stored['billing_state_path']}")
                    print(f"Auto-recover failed with HTTP {status}: {topup_payload}", file=sys.stderr)
                return 1
            if isinstance(topup_payload, dict):
                auto_recovered = {
                    "ok": True,
                    "status": status,
                    "api_key_source": api_key_source,
                    "response": topup_payload,
                }
                auto_recovered_session = record_topup_session(session=topup_payload, agent_id=args.agent_id)
        if args.json:
            payload_out: dict[str, Any] = {
                "recovery": summary,
                "commands": build_recovery_commands(summary),
                "stored": stored,
            }
            if auto_recovered:
                payload_out["auto_recovered"] = auto_recovered
            if auto_recovered_session:
                payload_out["stored_session"] = auto_recovered_session
            print(json.dumps(payload_out, indent=2, sort_keys=True))
        else:
            print_402_summary(summary)
            print(f"Saved billing snapshot to: {stored['billing_state_path']}")
            if auto_recovered and isinstance(auto_recovered["response"], dict):
                print("Auto-recovery:")
                print_topup_session(auto_recovered["response"])
                print(
                    "Continue in OpenClaw with: "
                    f"python3 scripts/billing.py watch --session-id {auto_recovered['response'].get('topup_session_id', '<topup-session-id>')}"
                )
        return 0

    if args.command == "balance":
        summary = None
        if args.response_json or args.response_file:
            payload = load_json_object_from_option(args.response_json, args.response_file, source_name="response")
            summary = parse_insufficient_balance(payload)
            if not summary:
                raise SystemExit("The provided response is not a structured insufficient_balance payload.")
            remember_402_summary(summary, agent_id=args.agent_id)
        server_url = require_server_url(args.server_url)
        api_key, api_key_source = resolve_api_key_or_exit(args.api_key, args.profile_id, args.agent_id)
        auth_headers = {"Authorization": f"Bearer {api_key}"}

        status, payload = fetch_authoritative_balance(server_url, auth_headers)
        fallback_workspace_id = args.workspace_id or (summary.get("workspace_id") if summary else None)
        fallback_snapshot = None
        fallback_state_path = None
        if fallback_workspace_id:
            fallback_snapshot, fallback_state_path = get_last_balance_snapshot(
                workspace_id=fallback_workspace_id,
                agent_id=args.agent_id,
            )

        if status >= 400:
            if fallback_snapshot:
                if args.json:
                    print(
                        json.dumps(
                            {
                                "ok": False,
                                "status": status,
                                "api_key_source": api_key_source,
                                "response": payload,
                                "fallback_balance": fallback_snapshot,
                                "billing_state_path": fallback_state_path,
                            },
                            indent=2,
                            sort_keys=True,
                        )
                    )
                else:
                    print(f"Unable to fetch authoritative balance (HTTP {status}). Showing local fallback.", file=sys.stderr)
                    print_balance_snapshot(fallback_snapshot, fallback_state_path or "<unknown>")
                return 1
            if args.json:
                print(json.dumps({"ok": False, "status": status, "api_key_source": api_key_source, "response": payload}, indent=2, sort_keys=True))
            else:
                raise SystemExit(f"Unable to fetch authoritative balance (HTTP {status}): {payload}")
            return 1

        if not isinstance(payload, dict):
            raise SystemExit("Server returned a non-object payload for GET /v1/balance.")
        balance = parse_workspace_balance(payload)
        if not balance:
            raise SystemExit("Server returned an invalid workspace balance payload.")
        stored = remember_authoritative_balance(balance, agent_id=args.agent_id)
        if args.json:
            print(
                json.dumps(
                    {
                        "ok": True,
                        "status": status,
                        "api_key_source": api_key_source,
                        "response": payload,
                        "billing_state_path": stored["billing_state_path"],
                        "balance": stored["snapshot"],
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print_balance_snapshot(stored["snapshot"], stored["billing_state_path"])
        return 0

    if args.command == "history":
        sessions, state_path = list_topup_sessions(workspace_id=args.workspace_id, agent_id=args.agent_id)
        sessions = sessions[: max(args.limit, 0)]
        if args.json:
            print(json.dumps({"ok": True, "billing_state_path": state_path, "sessions": sessions}, indent=2, sort_keys=True))
        else:
            print_history(sessions, state_path)
        return 0

    if args.command == "activity":
        server_url = require_server_url(args.server_url)
        api_key, api_key_source = resolve_api_key_or_exit(args.api_key, args.profile_id, args.agent_id)
        auth_headers = {"Authorization": f"Bearer {api_key}"}

        usage_status, usage_payload = fetch_usage_events(server_url, auth_headers)
        ledger_status, ledger_payload = fetch_ledger_entries(server_url, auth_headers)

        if usage_status >= 400 or ledger_status >= 400:
            if args.json:
                print(
                    json.dumps(
                        {
                            "ok": False,
                            "api_key_source": api_key_source,
                            "usage_events_status": usage_status,
                            "usage_events_response": usage_payload,
                            "ledger_status": ledger_status,
                            "ledger_response": ledger_payload,
                        },
                        indent=2,
                        sort_keys=True,
                    )
                )
            else:
                raise SystemExit(
                    "Unable to fetch recent billing activity: "
                    f"usage-events HTTP {usage_status}, ledger HTTP {ledger_status}."
                )
            return 1

        usage_events = trim_records(list_payload_data(usage_payload, field_name="GET /v1/usage-events"), limit=args.limit)
        ledger_entries = trim_records(list_payload_data(ledger_payload, field_name="GET /v1/ledger"), limit=args.limit)

        if args.json:
            print(
                json.dumps(
                    {
                        "ok": True,
                        "api_key_source": api_key_source,
                        "usage_events_status": usage_status,
                        "usage_events": usage_events,
                        "ledger_status": ledger_status,
                        "ledger_entries": ledger_entries,
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(f"API key source: {api_key_source}")
            print_usage_events(usage_events)
            print_ledger_entries(ledger_entries)
        return 0

    if args.command == "referral-link":
        server_url = require_server_url(args.server_url)
        api_key, api_key_source = resolve_api_key_or_exit(args.api_key, args.profile_id, args.agent_id)
        auth_headers = {"Authorization": f"Bearer {api_key}"}

        status, payload = fetch_referral_link(server_url, auth_headers)
        if status >= 400:
            if args.json:
                print(
                    json.dumps(
                        {
                            "ok": False,
                            "status": status,
                            "api_key_source": api_key_source,
                            "response": payload,
                        },
                        indent=2,
                        sort_keys=True,
                    )
                )
            else:
                raise SystemExit(f"Unable to fetch referral link (HTTP {status}): {payload}")
            return 1

        if not isinstance(payload, dict):
            raise SystemExit("Server returned a non-object payload for GET /v1/referrals/me.")
        referral = parse_referral_link(payload)
        if not referral:
            raise SystemExit("Server returned an invalid referral payload.")

        if args.json:
            print(
                json.dumps(
                    {
                        "ok": True,
                        "status": status,
                        "api_key_source": api_key_source,
                        "referral": referral,
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(f"API key source: {api_key_source}")
            print_referral_link(referral)
        return 0

    server_url = require_server_url(args.server_url)

    api_key, api_key_source = resolve_api_key_or_exit(args.api_key, args.profile_id, args.agent_id)
    auth_headers = {"Authorization": f"Bearer {api_key}"}

    if args.command == "create-topup":
        amount = derive_topup_amount(args)
        status, payload = create_topup_session(server_url, auth_headers, amount)
    elif args.command == "status":
        status, payload = request_json(
            f"{server_url}/v1/topup/sessions/{urllib.parse.quote(args.session_id)}",
            headers=auth_headers,
        )
    elif args.command == "watch":
        deadline = time.monotonic() + args.timeout_seconds
        payload = {}
        status = 0
        while True:
            status, payload = request_json(
                f"{server_url}/v1/topup/sessions/{urllib.parse.quote(args.session_id)}",
                headers=auth_headers,
            )
            if status >= 400:
                break
            if isinstance(payload, dict) and payload.get("status") in {"credit_applied", "payment_failed"}:
                break
            if time.monotonic() >= deadline:
                raise SystemExit(
                    f"Timed out after {args.timeout_seconds:.1f}s waiting for top-up session {args.session_id}."
                )
            time.sleep(args.interval_seconds)
    else:
        raise SystemExit(f"Unsupported command: {args.command}")

    if status >= 400:
        if args.json:
            print(json.dumps({"ok": False, "status": status, "api_key_source": api_key_source, "response": payload}, indent=2, sort_keys=True))
        else:
            print(f"HTTP {status}: {payload}", file=sys.stderr)
        return 1

    if args.json:
        structured: dict[str, Any] = {"ok": True, "status": status, "api_key_source": api_key_source, "response": payload}
        if isinstance(payload, dict):
            stored_session = record_topup_session(session=payload, agent_id=args.agent_id)
            structured["stored_session"] = stored_session
            refreshed_balance = None
            if payload.get("status") == "credit_applied":
                balance_status, balance_payload = fetch_authoritative_balance(server_url, auth_headers)
                if balance_status < 400 and isinstance(balance_payload, dict):
                    authoritative_balance = parse_workspace_balance(balance_payload)
                    if authoritative_balance:
                        refreshed_balance = remember_authoritative_balance(authoritative_balance, agent_id=args.agent_id)
                        structured["authoritative_balance_status"] = balance_status
                        structured["authoritative_balance_response"] = balance_payload
                if not refreshed_balance:
                    refreshed_balance = update_balance_from_completed_topup(payload, agent_id=args.agent_id)
            if refreshed_balance:
                structured["refreshed_balance"] = refreshed_balance
        print(json.dumps(structured, indent=2, sort_keys=True))
    else:
        if isinstance(payload, dict):
            record_topup_session(session=payload, agent_id=args.agent_id)
            refreshed_balance = None
            if payload.get("status") == "credit_applied":
                balance_status, balance_payload = fetch_authoritative_balance(server_url, auth_headers)
                if balance_status < 400 and isinstance(balance_payload, dict):
                    authoritative_balance = parse_workspace_balance(balance_payload)
                    if authoritative_balance:
                        refreshed_balance = remember_authoritative_balance(authoritative_balance, agent_id=args.agent_id)
                if not refreshed_balance:
                    refreshed_balance = update_balance_from_completed_topup(payload, agent_id=args.agent_id)
            print_topup_session(payload)
            if refreshed_balance:
                snapshot = refreshed_balance["snapshot"]
                print(
                    "Refreshed balance: "
                    f"{snapshot['amount']} {snapshot['unit']} "
                    f"(estimated={'yes' if snapshot['estimated'] else 'no'})"
                )
        else:
            print(payload)

    return 0


if __name__ == "__main__":
    sys.exit(main())
