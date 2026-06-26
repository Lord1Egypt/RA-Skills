#!/usr/bin/env python3
"""
Modeio AI Safety Skill - instruction risk analysis.
Evaluates instructions for destructive operations, prompt injection,
irreversible actions, and compliance violations via the Modeio safety API.
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict

REQUESTS_AVAILABLE = True
try:
    import requests
except ModuleNotFoundError:
    REQUESTS_AVAILABLE = False

    class _RequestsShim:
        class RequestException(Exception):
            pass

        class MissingDependencyError(RequestException):
            pass

        class ConnectionError(RequestException):
            pass

        class Timeout(RequestException):
            pass

        class HTTPError(RequestException):
            def __init__(self, *args, response=None, **kwargs):
                super().__init__(*args)
                self.response = response

        class Response:
            def __init__(self):
                self.status_code = None

        @staticmethod
        def post(*_args, **_kwargs):
            raise _RequestsShim.MissingDependencyError(
                "requests package is required for backend-backed safety checks. "
                "Install requests to enable backend-backed safety checks."
            )

    requests = _RequestsShim()

# Backend API URL, overridable via SAFETY_API_URL environment variable
URL = os.environ.get("SAFETY_API_URL", "https://safety-cf.modeio.ai/api/cf/safety")

TOOL_NAME = "security"

MAX_RETRIES = 2
RETRY_BACKOFF = 1.0  # seconds; doubles each retry

CONTEXT_HELP = (
    "Execution context JSON for state-changing instructions. Required keys: "
    "environment, operation_intent, scope, data_sensitivity, rollback, change_control. "
    "Example: '{\"environment\":\"local-dev\",\"operation_intent\":\"cleanup\","
    "\"scope\":\"single-resource\",\"data_sensitivity\":\"internal\","
    "\"rollback\":\"easy\",\"change_control\":\"none\"}'"
)

TARGET_HELP = (
    "Concrete operation target (absolute file path, table, service name, or URL). "
    "Required for state-changing instructions."
)


def _is_requests_dependency_error(error: Exception) -> bool:
    if REQUESTS_AVAILABLE:
        return False
    missing_dependency_type = getattr(requests, "MissingDependencyError", None)
    if missing_dependency_type is not None and isinstance(error, missing_dependency_type):
        return True
    return "requests package is required" in str(error).lower()


def _post_with_retry(url, json_payload, timeout=60):
    """POST with simple exponential-backoff retry on transient failures."""
    last_exc = None
    for attempt in range(1 + MAX_RETRIES):
        try:
            resp = requests.post(url, json=json_payload, timeout=timeout)
            if resp.status_code in (502, 503, 504) and attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (2 ** attempt))
                continue
            resp.raise_for_status()
            return resp
        except (requests.ConnectionError, requests.Timeout) as e:
            last_exc = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (2 ** attempt))
                continue
            raise
    # Should not reach here, but raise last exception if it does
    raise last_exc  # type: ignore[misc]


def detect_safety(instruction: str, context: str = None, target: str = None) -> dict:
    """
    Call the Modeio safety backend and return the full response JSON.
    Response includes: approved, risk_level, risk_types, concerns, recommendation, etc.
    """
    payload = {"instruction": instruction}
    if context:
        payload["context"] = context
    if target:
        payload["target"] = target
    resp = _post_with_retry(URL, json_payload=payload)
    return resp.json()


def _success_envelope(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "success": True,
        "tool": TOOL_NAME,
        "mode": "api",
        "data": data,
    }


def _error_envelope(
    error_type: str,
    message: str,
    status_code: int = None,
    details: Dict[str, Any] = None,
) -> Dict[str, Any]:
    error: Dict[str, Any] = {
        "type": error_type,
        "message": message,
    }
    if status_code is not None:
        error["status_code"] = status_code
    if details is not None:
        error["details"] = details
    return {
        "success": False,
        "tool": TOOL_NAME,
        "mode": "api",
        "error": error,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate instructions for safety risks (destructive ops, risk level, reversibility, etc.)"
    )
    parser.add_argument("-i", "--input", type=str, required=True, help="Instruction or operation description to evaluate")
    parser.add_argument("-c", "--context", type=str, default=None, help=CONTEXT_HELP)
    parser.add_argument("-t", "--target", type=str, default=None, help=TARGET_HELP)
    parser.add_argument("--json", action="store_true", help="Output unified JSON contract for machine consumption.")
    args = parser.parse_args()

    raw_input = args.input

    def _exit_with_error(error_type: str, message: str, status_code: int = None, details: Dict[str, Any] = None) -> None:
        if args.json:
            print(
                json.dumps(
                    _error_envelope(
                        error_type=error_type,
                        message=message,
                        status_code=status_code,
                        details=details,
                    ),
                    ensure_ascii=False,
                )
            )
        else:
            print(f"Error: {message}", file=sys.stderr)
            if status_code is not None:
                print(f"Error: status_code={status_code}", file=sys.stderr)
            if details is not None:
                print(json.dumps(details, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    if not raw_input or not raw_input.strip():
        msg = "--input must not be empty."
        if args.json:
            print(json.dumps(_error_envelope(error_type="validation_error", message=msg), ensure_ascii=False))
        else:
            print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)

    try:
        result = detect_safety(
            instruction=raw_input,
            context=args.context,
            target=args.target,
        )
    except requests.HTTPError as e:
        response = getattr(e, "response", None)
        status_code = getattr(response, "status_code", None)
        _exit_with_error(
            error_type="api_error",
            message=f"safety backend returned HTTP error: {type(e).__name__}",
            status_code=status_code,
        )
    except requests.RequestException as e:
        response = getattr(e, "response", None)
        status_code = getattr(response, "status_code", None)
        dependency_error = _is_requests_dependency_error(e)
        _exit_with_error(
            error_type="dependency_error" if dependency_error else "network_error",
            message=str(e) if dependency_error else f"safety request failed: {type(e).__name__}",
            status_code=status_code,
        )
    except ValueError as e:
        _exit_with_error(
            error_type="api_error",
            message=f"safety backend returned invalid JSON: {type(e).__name__}",
        )

    if not isinstance(result, dict):
        _exit_with_error(
            error_type="api_error",
            message="safety backend returned invalid payload type",
            details={"receivedType": type(result).__name__},
        )

    normalized_result = dict(result)
    if normalized_result.get("approved") is None:
        normalized_result["approved"] = False

    if normalized_result.get("error"):
        _exit_with_error(
            error_type="api_error",
            message=str(normalized_result.get("error")),
            details=normalized_result,
        )

    if args.json:
        print(json.dumps(_success_envelope(normalized_result), ensure_ascii=False))
        return

    print("Status: success", file=sys.stderr)
    print(json.dumps(normalized_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
