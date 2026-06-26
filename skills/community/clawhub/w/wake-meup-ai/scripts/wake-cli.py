#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["x402[svm]>=2.0.0,<3", "httpx>=0.27,<1"]
# ///
"""Reference client for wake.meup.ai using x402 USDC payments.

Usage:
    uv run wake-cli.py verify --phone +15551234567 --keypair key.json
    uv run wake-cli.py schedule --phone +15551234567 --keypair key.json \
        --time 2026-04-01T07:00:00Z --voice ash --hints "Wake Brian gently"
"""

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

import httpx

from x402.client import x402Client
from x402.http.clients.httpx import x402HttpxClient
from x402.mechanisms.svm.exact.register import register_exact_svm_client
from x402.mechanisms.svm.signers import KeypairSigner
from solders.keypair import Keypair  # type: ignore

# Exit codes
EXIT_OK = 0
EXIT_API_ERROR = 1
EXIT_INVALID_INPUT = 2
EXIT_PAYMENT_FAILED = 3
EXIT_TIMEOUT = 4
EXIT_KEYPAIR_ERROR = 5
EXIT_TRANSPORT_ERROR = 6
EXIT_UNEXPECTED_ERROR = 7

VALID_VOICES = {"alloy", "ash", "ballad", "cedar", "coral", "echo", "marin", "sage", "shimmer", "verse"}


def load_signer(keypair_path: str) -> KeypairSigner:
    """Load a KeypairSigner from a Solana keypair JSON file.

    Accepts a path to a solana-keygen JSON file (64-byte array).
    Generate one with: solana-keygen new -o keypair.json

    Also checks SOLANA_KEYPAIR_PATH env var as a fallback if no --keypair
    argument is provided.
    """
    path = Path(keypair_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Keypair file not found: {path}. "
            f"Generate one with: solana-keygen new -o {path}"
        )
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Keypair file is not valid JSON: {path}. "
            f"Expected a solana-keygen JSON file (byte array). Parse error: {e}"
        )
    if not isinstance(data, list):
        raise ValueError(
            f"Unsupported keypair file format in {path}: expected a JSON byte array, "
            f"got {type(data).__name__}. Generate one with: solana-keygen new -o {path}"
        )
    try:
        kp = Keypair.from_bytes(bytes(data))
    except Exception as e:
        raise ValueError(
            f"Keypair file contains a JSON array but it is not a valid Solana keypair: {e}. "
            f"Expected 64-byte array from 'solana-keygen new'."
        )
    return KeypairSigner(kp)


def log(msg: str) -> None:
    """Print diagnostic message to stderr."""
    print(msg, file=sys.stderr)


def output(data: dict) -> None:
    """Print structured JSON to stdout."""
    print(json.dumps(data, indent=2))


async def cmd_verify(args: argparse.Namespace) -> int:
    """Run the verify flow: POST /verify, then poll until resolved."""
    signer = load_signer(args.keypair)
    log(f"Signer address: {signer.address}")

    x402 = x402Client()
    register_exact_svm_client(x402, signer)

    async with x402HttpxClient(x402, base_url=args.base_url) as client:
        # Step 1: POST /api/v1/verify
        log(f"POST {args.base_url}/api/v1/verify")
        resp = await client.post(
            "/api/v1/verify",
            json={"phone": args.phone},
        )

        if resp.status_code != 200:
            output({"error": resp.text, "status_code": resp.status_code})
            if resp.status_code == 402:
                return EXIT_PAYMENT_FAILED
            if resp.status_code == 422:
                return EXIT_INVALID_INPUT
            return EXIT_API_ERROR

        body = resp.json()

        # Already verified — no call needed
        if body.get("verified"):
            output(body)
            return EXIT_OK

        # Calling — poll for result
        attempt_id = body.get("attempt_id")
        if not attempt_id:
            output({"error": "No attempt_id in response", "response": body})
            return EXIT_API_ERROR

        log(f"Verification call initiated: {attempt_id}")
        log("Polling every 5s...")

        timeout = args.timeout
        start = time.monotonic()

        while time.monotonic() - start < timeout:
            await asyncio.sleep(5)
            poll_resp = await client.get(f"/api/v1/verify/attempts/{attempt_id}")

            if poll_resp.status_code != 200:
                output({"error": poll_resp.text, "status_code": poll_resp.status_code})
                return EXIT_API_ERROR

            poll_body = poll_resp.json()
            status = poll_body.get("status", "")
            log(f"  status: {status}")

            if poll_body.get("verified"):
                output(poll_body)
                return EXIT_OK

            if status in ("expired", "rejected"):
                output(poll_body)
                return EXIT_API_ERROR

        output({"error": "timeout", "detail": f"Verification did not complete within {timeout}s"})
        return EXIT_TIMEOUT


async def cmd_schedule(args: argparse.Namespace) -> int:
    """Run the schedule flow: POST /schedule."""
    signer = load_signer(args.keypair)
    log(f"Signer address: {signer.address}")

    x402 = x402Client()
    register_exact_svm_client(x402, signer)

    body = {
        "phone": args.phone,
        "times": args.time,
        "voice": args.voice,
    }
    if args.hints:
        body["hints"] = args.hints

    async with x402HttpxClient(x402, base_url=args.base_url) as client:
        log(f"POST {args.base_url}/api/v1/schedule")
        resp = await client.post("/api/v1/schedule", json=body)

        if resp.status_code != 200:
            output({"error": resp.text, "status_code": resp.status_code})
            if resp.status_code == 402:
                return EXIT_PAYMENT_FAILED
            if resp.status_code in (403, 422):
                return EXIT_INVALID_INPUT
            return EXIT_API_ERROR

        output(resp.json())
        return EXIT_OK


def main() -> None:
    parser = argparse.ArgumentParser(
        description="wake.meup.ai reference client with x402 payments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  uv run scripts/wake-cli.py --keypair key.json --phone +15551234567 verify
  uv run scripts/wake-cli.py --keypair key.json --phone +15551234567 \\
      schedule --time 2026-04-01T07:00:00Z --voice ash
  uv run scripts/wake-cli.py --keypair key.json --phone +15551234567 \\
      schedule --time 2026-04-01T07:00:00Z --time 2026-04-02T07:00:00Z \\
      --hints "Brian has a big meeting at 9am"

exit codes:
  0  success
  1  API error (server returned non-200)
  2  invalid input (bad phone, unknown voice, past timestamp)
  3  payment failed (x402 transaction rejected)
  4  timeout (verification polling exceeded --timeout)
  5  keypair error (file not found or invalid format)
  6  transport error (DNS, connection, TLS, or HTTP failure)
  7  unexpected error (unhandled exception)
""",
    )
    parser.add_argument(
        "--base-url",
        default="https://wake.meup.ai",
        help="Base URL for the Wakeup API (default: https://wake.meup.ai)",
    )
    parser.add_argument(
        "--keypair",
        default=os.environ.get("SOLANA_KEYPAIR_PATH"),
        help="Path to solana-keygen JSON file (or set SOLANA_KEYPAIR_PATH env var)",
    )
    parser.add_argument(
        "--phone",
        required=True,
        help="Phone number in E.164 format (e.g. +15551234567)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # verify subcommand
    verify_parser = subparsers.add_parser("verify", help="Verify a phone number")
    verify_parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Polling timeout in seconds (default: 120)",
    )

    # schedule subcommand
    schedule_parser = subparsers.add_parser("schedule", help="Schedule wake-up calls")
    schedule_parser.add_argument(
        "--time",
        action="append",
        required=True,
        help="ISO 8601 timestamp (UTC). Repeatable for multiple calls.",
    )
    schedule_parser.add_argument(
        "--voice",
        default="ash",
        choices=sorted(VALID_VOICES),
        help="Voice name (default: ash)",
    )
    schedule_parser.add_argument(
        "--hints",
        help="Context about the person for a personalized call",
    )

    args = parser.parse_args()

    if not args.keypair:
        parser.error(
            "--keypair is required. Provide a path to a solana-keygen JSON file, "
            "or set the SOLANA_KEYPAIR_PATH environment variable."
        )

    try:
        if args.command == "verify":
            exit_code = asyncio.run(cmd_verify(args))
        elif args.command == "schedule":
            exit_code = asyncio.run(cmd_schedule(args))
        else:
            parser.print_help()
            exit_code = EXIT_INVALID_INPUT
    except (ValueError, FileNotFoundError) as e:
        output({"error": f"Keypair error: {e}"})
        exit_code = EXIT_KEYPAIR_ERROR
    except httpx.TimeoutException as e:
        output({"error": "Transport timeout", "detail": str(e)})
        exit_code = EXIT_TRANSPORT_ERROR
    except httpx.HTTPError as e:
        output({"error": "Transport error", "detail": str(e)})
        exit_code = EXIT_TRANSPORT_ERROR
    except Exception as e:
        output({"error": "Unexpected error", "detail": f"{type(e).__name__}: {e}"})
        exit_code = EXIT_UNEXPECTED_ERROR

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
