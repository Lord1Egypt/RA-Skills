#!/usr/bin/env python3
"""
check_services.py — Health check all configured services.

Reads services.json config. For each service:
  - HTTP GET to health endpoint (checks status code)
  - Ping test (ICMP via system ping command)
  - Response time measurement

Outputs JSON with status (up/down/degraded), response time, last checked.

Usage:
    python3 check_services.py --config assets/services.json
    python3 check_services.py --config assets/services.json --output /tmp/status.json
    python3 check_services.py --config assets/services.json --timeout 5
"""

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone


DEFAULT_TIMEOUT = 10  # seconds
PING_TIMEOUT = 3      # seconds per ping attempt


def load_config(config_path: str) -> dict:
    """Load and validate the services config file."""
    if not os.path.exists(config_path):
        print(f"ERROR: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in config: {e}", file=sys.stderr)
            sys.exit(1)

    if "services" not in data:
        print("ERROR: Config must have a 'services' array.", file=sys.stderr)
        sys.exit(1)

    return data


def ping_host(host: str, timeout: int = PING_TIMEOUT) -> tuple[bool, float]:
    """
    Ping a host using the system ping command.
    Returns (success: bool, rtt_ms: float).
    """
    # -c 1 = one packet, -W timeout = wait seconds (Linux), -t timeout (macOS)
    # Try macOS syntax first, fall back to Linux
    for flag in ["-t", "-W"]:
        try:
            cmd = ["ping", "-c", "1", flag, str(timeout), host]
            start = time.perf_counter()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout + 1,
            )
            elapsed = (time.perf_counter() - start) * 1000
            if result.returncode == 0:
                return True, round(elapsed, 2)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
        except Exception:
            continue

    return False, 0.0


def http_check(
    url: str,
    health_endpoint: str = "/",
    expected_status: int = 200,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """
    Perform HTTP GET to health endpoint.
    Returns dict with: ok, status_code, response_time_ms, error.
    """
    # Build full URL
    base = url.rstrip("/")
    endpoint = health_endpoint if health_endpoint.startswith("/") else "/" + health_endpoint
    full_url = base + endpoint

    result = {
        "url": full_url,
        "ok": False,
        "status_code": None,
        "response_time_ms": None,
        "error": None,
    }

    req = urllib.request.Request(
        full_url,
        headers={"User-Agent": "status-page-gen/1.0"},
        method="GET",
    )

    try:
        start = time.perf_counter()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = (time.perf_counter() - start) * 1000
            result["status_code"] = resp.status
            result["response_time_ms"] = round(elapsed, 2)
            result["ok"] = (resp.status == expected_status)
    except urllib.error.HTTPError as e:
        elapsed = (time.perf_counter() - start) * 1000
        result["status_code"] = e.code
        result["response_time_ms"] = round(elapsed, 2)
        result["ok"] = (e.code == expected_status)
        if not result["ok"]:
            result["error"] = f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        result["error"] = str(e.reason)
    except TimeoutError:
        result["error"] = f"Timed out after {timeout}s"
    except Exception as e:
        result["error"] = str(e)

    return result


def derive_ping_host(url: str) -> str:
    """Extract hostname from a URL."""
    # Remove scheme
    host = url.split("://", 1)[-1]
    # Remove path and port
    host = host.split("/")[0].split(":")[0]
    return host


def check_service(service: dict, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """
    Run all checks for a single service.
    Returns a result dict.
    """
    name = service.get("name", "Unknown")
    url = service.get("url", "")
    health_endpoint = service.get("health_endpoint", "/")
    expected_status = service.get("expected_status", 200)
    ping_host_override = service.get("ping_host")
    tags = service.get("tags", [])

    host_to_ping = ping_host_override or derive_ping_host(url)

    now = datetime.now(timezone.utc).isoformat()

    # Run HTTP check
    http = http_check(url, health_endpoint, expected_status, timeout)

    # Run ping
    ping_ok, ping_rtt = ping_host(host_to_ping, PING_TIMEOUT)

    # Determine overall status
    if http["ok"] and ping_ok:
        status = "up"
    elif http["ok"] and not ping_ok:
        # HTTP works but ping failed — likely firewall blocking ICMP, still up
        status = "up"
    elif not http["ok"] and ping_ok:
        # Ping works but HTTP fails — service is degraded
        status = "degraded"
    else:
        status = "down"

    return {
        "name": name,
        "url": url,
        "health_endpoint": health_endpoint,
        "tags": tags,
        "status": status,
        "http": {
            "ok": http["ok"],
            "status_code": http["status_code"],
            "response_time_ms": http["response_time_ms"],
            "error": http["error"],
            "checked_url": http["url"],
        },
        "ping": {
            "host": host_to_ping,
            "ok": ping_ok,
            "rtt_ms": ping_rtt,
        },
        "last_checked": now,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Check health of all configured services."
    )
    parser.add_argument(
        "--config",
        default="assets/services.json",
        help="Path to services.json config (default: assets/services.json)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Write JSON output to this file (default: stdout)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"HTTP request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress to stderr",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    services = config["services"]

    results = []
    for svc in services:
        if args.verbose:
            print(f"Checking: {svc.get('name', svc.get('url', '?'))}...", file=sys.stderr)

        result = check_service(svc, timeout=args.timeout)
        results.append(result)

        if args.verbose:
            status_icon = {"up": "✓", "degraded": "~", "down": "✗"}.get(result["status"], "?")
            rtt = result["http"]["response_time_ms"]
            rtt_str = f"{rtt}ms" if rtt is not None else "n/a"
            print(
                f"  {status_icon} {result['name']}: {result['status']} ({rtt_str})",
                file=sys.stderr,
            )

    summary = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "up": sum(1 for r in results if r["status"] == "up"),
        "degraded": sum(1 for r in results if r["status"] == "degraded"),
        "down": sum(1 for r in results if r["status"] == "down"),
        "services": results,
    }

    output_json = json.dumps(summary, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        if args.verbose:
            print(f"\nResults written to: {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
