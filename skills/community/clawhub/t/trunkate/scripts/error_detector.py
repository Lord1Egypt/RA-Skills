#!/usr/bin/env python3
import os
import sys

def handle_api_errors():
    """
    Reactive resilience for Trunkate API service failures.
    Reflects the specific error logic in the FastAPI server.py.
    """
    error_msg = os.environ.get("OPENCLAW_LAST_ERROR_MESSAGE", "").lower()
    
    # 1. Auth Failures (401 Unauthorized)
    if "invalid api key" in error_msg:
        print("Trunkate Fatal: The provided API key was rejected by Firestore.", file=sys.stderr)
        return

    # 2. Rate Limiting (429 Too Many Requests)
    # The API distinguishes between Key-level and Account-level budgets
    if "api key budget exceeded" in error_msg:
        print("Trunkate Bypass: Key-level rate limit hit. Skipping optimization.", file=sys.stderr)
        return
    if "account rate limit exceeded" in error_msg:
        print("Trunkate Bypass: Global account limit reached. Skipping optimization.", file=sys.stderr)
        return

    # 3. Infrastructure Failures
    if any(err in error_msg for err in ["500", "503", "connection refused"]):
        print("Trunkate Bypass: API/Redis/Firestore unreachable. Proceeding unoptimized.", file=sys.stderr)
        return

    # 4. Input/Validation Errors (422 Unprocessable Entity)
    if "unprocessable" in error_msg:
        print("Trunkate Alert: Malformed request payload. Verify prompt encoding.", file=sys.stderr)
        return

if __name__ == "__main__":
    handle_api_errors()