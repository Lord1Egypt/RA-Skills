"""Error code extraction and classification."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ErrorCode:
    code: str
    category: str  # http_client, http_server, app_error, grpc, etc.
    description: str
    line_number: int | None = None


# HTTP status code descriptions
_HTTP_CODES: dict[int, str] = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    413: "Payload Too Large",
    415: "Unsupported Media Type",
    422: "Unprocessable Entity",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
}

# HTTP status pattern with context (e.g., "HTTP 500", "status: 404", "returned 503")
_HTTP_PATTERN = re.compile(
    r"(?:HTTP/?[\d.]*\s+|status[:\s_=]+|returned?\s+|code[:\s_=]+|response\s+)(\d{3})\b",
    re.IGNORECASE,
)

# Standalone HTTP codes in error context
_HTTP_STANDALONE = re.compile(r"\b([45]\d{2})\b")

# Application error codes: ERR_001, E1234, ERROR-5001, ERR_TIMEOUT_5001
_APP_ERROR_PATTERN = re.compile(
    r"\b(ERR(?:OR)?[_\-]?(?:\w+[_\-])?\d+|E\d{3,}|ERRNO[_\-]?\d+)\b",
    re.IGNORECASE,
)

# gRPC codes
_GRPC_PATTERN = re.compile(
    r"\b(CANCELLED|UNKNOWN|INVALID_ARGUMENT|DEADLINE_EXCEEDED|NOT_FOUND"
    r"|ALREADY_EXISTS|PERMISSION_DENIED|RESOURCE_EXHAUSTED|FAILED_PRECONDITION"
    r"|ABORTED|OUT_OF_RANGE|UNIMPLEMENTED|INTERNAL|UNAVAILABLE|DATA_LOSS"
    r"|UNAUTHENTICATED)\b"
)


def extract_error_codes(text: str) -> list[ErrorCode]:
    """Extract and classify error codes from text."""
    results: list[ErrorCode] = []
    seen: set[str] = set()

    for line_num, line in enumerate(text.splitlines(), start=1):
        # HTTP codes with context
        for m in _HTTP_PATTERN.finditer(line):
            code = int(m.group(1))
            key = f"http_{code}_{line_num}"
            if key not in seen and code in _HTTP_CODES:
                seen.add(key)
                category = "http_client" if 400 <= code < 500 else "http_server"
                results.append(ErrorCode(
                    code=str(code),
                    category=category,
                    description=_HTTP_CODES[code],
                    line_number=line_num,
                ))

        # Application error codes
        for m in _APP_ERROR_PATTERN.finditer(line):
            code = m.group(1).upper()
            key = f"app_{code}"
            if key not in seen:
                seen.add(key)
                results.append(ErrorCode(
                    code=code,
                    category="app_error",
                    description="Application error code",
                    line_number=line_num,
                ))

        # gRPC codes
        for m in _GRPC_PATTERN.finditer(line):
            code = m.group(1)
            key = f"grpc_{code}"
            if key not in seen:
                seen.add(key)
                results.append(ErrorCode(
                    code=code,
                    category="grpc",
                    description=f"gRPC status: {code}",
                    line_number=line_num,
                ))

    return results
