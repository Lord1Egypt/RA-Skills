"""Shared CLI plumbing for the sanmar skill scripts.

The single entrypoint (`sanmar.py`) dispatches on `argv[1]` (the action) and
reads an optional JSON object from stdin. Results are printed as a single JSON
object on stdout; failures print `{"error": {...}}` and exit non-zero.

Credentials are resolved inside the tool functions: they fall back to the
`SANMAR_*` environment variables when no credential fields are passed in the
stdin JSON, so the CLI layer stays thin.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable

from ftp_resolver import (  # noqa: E402  (sibling module, scripts dir on sys.path)
    SanMarFTPConfigError,
    SanMarFTPError,
)
from pdf_parser import PDFParseError  # noqa: E402  (sibling module)
from sanmar_client import (  # noqa: E402  (sibling module)
    SanMarAPIError,
    SanMarConfigError,
    SanMarError,
    SanMarTransportError,
)


def emit(payload: Any) -> None:
    print(json.dumps(payload, default=str))


def fail(error_type: str, message: str, exit_code: int = 1, **extra: Any) -> None:
    print(json.dumps({"error": {"type": error_type, "message": message, **extra}}))
    sys.exit(exit_code)


def read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail("validation_error", f"Invalid JSON on stdin: {exc}", exit_code=1)
    if not isinstance(payload, dict):
        fail("validation_error", "Input must be a JSON object.", exit_code=1)
    return payload  # type: ignore[return-value]


def run(actions: dict[str, Callable[..., Any]], *, usage: str) -> None:
    """Dispatch `argv[1]` against `actions`, reading kwargs from stdin JSON.

    Each handler is a `sanmar_*` tool function. The stdin JSON object is
    splatted in as keyword arguments, so its keys must match the tool's
    parameter names (e.g. `style`, `color`, `size`, `lines`,
    `purchase_order`, `po_number`, `confirm`). Credential fields
    (`customer_number`, `username`, `password`, `environment`,
    `ftp_password`) may also be supplied this way; otherwise the tools read
    the `SANMAR_*` environment variables.
    """

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        fail("usage", usage, exit_code=2, actions=sorted(actions))

    action = sys.argv[1]
    handler = actions.get(action)
    if handler is None:
        fail(
            "unknown_action",
            f"Unknown action {action!r}.",
            exit_code=2,
            actions=sorted(actions),
        )

    args = read_stdin_json()
    try:
        result = handler(**args)
    except (SanMarConfigError, SanMarFTPConfigError) as exc:
        fail("config_error", str(exc), exit_code=2)
    except SanMarTransportError as exc:
        fail("connection_error", str(exc), retryable=True)
    except SanMarAPIError as exc:
        fail(
            "api_error",
            str(exc),
            surface=getattr(exc, "surface", "sanmar"),
            operation=getattr(exc, "operation", ""),
            retryable=getattr(exc, "retryable", False),
        )
    except SanMarFTPError as exc:
        fail("connection_error", str(exc))
    except PDFParseError as exc:
        fail("validation_error", str(exc))
    except SanMarError as exc:
        fail("api_error", str(exc))
    except (KeyError, ValueError, TypeError) as exc:
        fail("validation_error", str(exc))
    emit(result)
