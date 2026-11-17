#!/usr/bin/env python3
"""Wait for ROS stack terminal state + health check. See reference/deploy/12_wait_stack.md

Usage:
    python3 scripts/wait_and_probe.py \
        --region ap-southeast-1 \
        --stack-id "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" \
        [--has-app] \
        [--max-wait 1200] \
        [--probe-retries 15] \
        [--probe-interval 4]

Output (stdout): JSON
    Success: {"status":"ok","public_ip":"...","instance_id":"...","outputs":{...},"health":{"nginx":"pass","app":"manual"},"elapsed_seconds":180}
    Failure: {"status":"failed","stage":"...","error":"...","public_ip":"...","instance_id":"...","elapsed_seconds":...}

Heartbeat messages are printed to stderr.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.request
import urllib.error


def run_cli(cmd: list[str]) -> tuple[int, str]:
    """Run aliyun CLI command, return (returncode, stdout)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        # A single stalled CLI call is not a deployment failure (resources are
        # already being created and billed). Treat it as a transient error so the
        # caller retries instead of crashing the long-running poll loop.
        return 1, "aliyun CLI call timed out (30s), will retry"
    return result.returncode, result.stdout + result.stderr


def backoff(base: int, attempt: int, cap: int = 12) -> int:
    """Probe retry interval: dense at first, gradually longer, capped at `cap` seconds."""
    return min(base * attempt, cap)


# Permanent-error markers: once matched, retrying is pointless — fail fast instead
# of spinning until TIMEOUT. Covers auth/permission/parameter errors (expired
# credential, invalid AK, no permission, invalid region/parameter, etc.).
FATAL_ERROR_MARKERS = (
    "InvalidAccessKeyId", "SignatureDoesNotMatch", "Forbidden",
    "NoPermission", "Unauthorized", "InvalidSecurityToken",
    "AccessDenied", "InvalidRegionId", "MissingParameter",
    "InvalidParameter", "SDK.InvalidCredential", "SDK.CanNotResolveEndpoint",
)


def get_stack(region: str, stack_id: str) -> tuple[str, dict]:
    """Call GetStack.

    Returns (kind, data):
      - ("ok", <parsed JSON>)      stack fetched normally
      - ("not_found", {})           explicit StackNotFound / 404
      - ("fatal", {"error": ...})   permanent error (auth/permission/param), no retry
      - ("transient", {})           transient error (network), caller should retry
    """
    rc, out = run_cli([
        "aliyun", "ros", "GetStack",
        "--RegionId", region,
        "--StackId", stack_id,
    ])
    if rc != 0:
        if any(marker in out for marker in FATAL_ERROR_MARKERS):
            return "fatal", {"error": out.strip()[:500]}
        if "StackNotFound" in out or "404" in out:
            return "not_found", {}
        # Transient error — let caller retry
        return "transient", {}
    try:
        return "ok", json.loads(out)
    except json.JSONDecodeError:
        return "transient", {}


def extract_outputs(stack_data: dict) -> dict:
    """Extract key-value pairs from GetStack Outputs."""
    outputs = {}
    for item in stack_data.get("Outputs", []):
        key = item.get("OutputKey", "")
        val = item.get("OutputValue", "")
        outputs[key] = val
    return outputs


def heartbeat(msg: str):
    """Print heartbeat to stderr."""
    print(f"[heartbeat] {msg}", file=sys.stderr, flush=True)


def probe_url(url: str, timeout: int = 10) -> tuple[bool, int | None]:
    """HTTP GET health probe.

    Returns (reachable, status_code):
      - reachable=True means an HTTP response was received (incl. 4xx/5xx)
      - reachable=False means a connection-level failure (timeout/refused/DNS)
    Used only to probe nginx /healthz; the caller decides pass/fail (only 2xx/3xx
    counts as nginx ready).
    """
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, resp.status
    except urllib.error.HTTPError as e:
        # Got an HTTP response (e.g. 404/500); reachable=True, caller decides.
        return True, e.code
    except Exception:
        return False, None


def wait_for_terminal(region: str, stack_id: str, max_wait: int) -> tuple[str, dict]:
    """Poll GetStack until terminal state. Return (terminal_status, stack_data)."""
    terminal_states = {
        "CREATE_COMPLETE", "UPDATE_COMPLETE",
        "CREATE_FAILED", "ROLLBACK_COMPLETE", "ROLLBACK_FAILED",
        "DELETE_COMPLETE", "DELETE_FAILED",
    }
    start = time.time()
    # Transient StackNotFound: right after CreateStack the control plane may briefly
    # not find the stack (eventual consistency). Do not treat the first not_found as
    # DELETE_COMPLETE; only conclude deletion after several consecutive not_found.
    not_found_streak = 0
    NOT_FOUND_TOLERANCE = 3

    while True:
        elapsed = int(time.time() - start)
        if elapsed > max_wait:
            return "TIMEOUT", {}
        # Poll densely for the first 2 minutes (ECS+EIP is usually ready within
        # that window), then slow down to save API calls.
        poll_interval = 5 if elapsed < 120 else 10

        kind, data = get_stack(region, stack_id)
        if kind == "fatal":
            # Permanent error (credential/permission/param): fail immediately
            # instead of spinning until TIMEOUT.
            return "FATAL_ERROR", data
        if kind == "not_found":
            not_found_streak += 1
            if not_found_streak >= NOT_FOUND_TOLERANCE:
                return "DELETE_COMPLETE", {}
            heartbeat(f"Waited {elapsed}s, stack not found yet (attempt {not_found_streak}), likely control-plane lag, retrying...")
            time.sleep(poll_interval)
            continue
        not_found_streak = 0
        if kind == "transient":
            heartbeat(f"Waited {elapsed}s, error fetching stack status, retrying...")
            time.sleep(poll_interval)
            continue

        status = data.get("Status", "")
        if status in terminal_states:
            return status, data

        heartbeat(f"Waited {elapsed}s, current status: {status}")
        time.sleep(poll_interval)


def health_check(public_ip: str, has_app: bool, retries: int, interval: int) -> dict:
    """Nginx-only health check. Return {"nginx": "pass"/"fail", "app": "manual"/"skip"}.

    Nginx readiness is probed via HTTP /healthz. App liveness is NOT probed over
    HTTP (external probing of /api/ etc. gives false negatives, e.g. Spring Boot
    returns 500 for an unmapped path while the app is actually up). Instead, verify
    the app by reading its log on the instance via Cloud Assistant and judging
    manually -- see reference/rules/rule_error_handling.md.
    """
    result = {"nginx": "fail", "app": "skip"}

    # Nginx readiness: /healthz -- served directly by nginx via `return 200 "ok"`.
    # Only 2xx/3xx counts as nginx ready; 4xx/5xx means the nginx config did not
    # take effect or is broken, so a 404 must NOT be treated as pass.
    healthz_url = f"http://{public_ip}/healthz"
    for i in range(1, retries + 1):
        reachable, code = probe_url(healthz_url, timeout=10)
        if reachable and code is not None and code < 400:
            result["nginx"] = "pass"
            heartbeat(f"Nginx health check passed (attempt {i}, status={code})")
            break
        heartbeat(f"Nginx health check attempt {i}/{retries} failed (status={code})")
        if i < retries:
            time.sleep(backoff(interval, i))

    if result["nginx"] != "pass":
        return result

    # App liveness: not probed over HTTP. Flag it for manual verification via
    # Cloud Assistant (read the app log on the instance and judge).
    if has_app:
        result["app"] = "manual"
    return result


def main():
    parser = argparse.ArgumentParser(description="Wait for ROS stack + health check")
    parser.add_argument("--region", required=True, help="Region ID")
    parser.add_argument("--stack-id", required=True, help="Stack ID")
    parser.add_argument("--has-app", action="store_true",
                        help="Flag app:\"manual\" so the agent verifies the app via Cloud Assistant")
    parser.add_argument("--max-wait", type=int, default=1200,
                        help="Max wait seconds (default 1200=20min; pass 2700=45min with RDS)")
    parser.add_argument("--probe-retries", type=int, default=15, help="Health check retry count (default 15)")
    parser.add_argument("--probe-interval", type=int, default=4,
                        help="Base health check retry interval seconds (default 4, grows per attempt, capped at 12s)")
    args = parser.parse_args()

    start_time = time.time()

    # Phase 1: Wait for terminal state
    heartbeat("Starting stack status polling...")
    terminal_status, stack_data = wait_for_terminal(args.region, args.stack_id, args.max_wait)
    elapsed = int(time.time() - start_time)

    # Failed / deleted / timeout / fatal
    if terminal_status not in ("CREATE_COMPLETE", "UPDATE_COMPLETE"):
        if terminal_status == "FATAL_ERROR":
            output = {
                "status": "failed",
                "stage": "stack_query",
                "error": "Permanent error while querying stack (auth/permission/param); aborted early. "
                         "Check aliyun CLI credentials/permissions/region config.",
                "stack_status": terminal_status,
                "detail": stack_data.get("error", ""),
                "elapsed_seconds": elapsed,
            }
        else:
            output = {
                "status": "failed",
                "stage": "stack_create",
                "error": f"Stack terminal state: {terminal_status}",
                "stack_status": terminal_status,
                "elapsed_seconds": elapsed,
            }
            if stack_data:
                output["status_reason"] = stack_data.get("StatusReason", "")
        print(json.dumps(output, ensure_ascii=False))
        sys.exit(1)

    # Stack success — extract Outputs
    outputs = extract_outputs(stack_data)
    public_ip = outputs.get("PublicIp", outputs.get("EipAddress", ""))
    # Template Output is EcsInstanceIds (comma-separated list); take the first as the
    # display instance ID. Also accept InstanceId / EcsInstanceId keys.
    ecs_ids_raw = outputs.get("EcsInstanceIds") or outputs.get("InstanceId") \
        or outputs.get("EcsInstanceId") or ""
    instance_id = str(ecs_ids_raw).split(",")[0].strip() if ecs_ids_raw else ""

    if not public_ip:
        output = {
            "status": "failed",
            "stage": "extract_outputs",
            "error": "Stack succeeded but PublicIp/EipAddress not found in Outputs",
            "outputs": outputs,
            "elapsed_seconds": int(time.time() - start_time),
        }
        print(json.dumps(output, ensure_ascii=False))
        sys.exit(1)

    heartbeat(f"Stack created successfully! IP: {public_ip}, starting health check...")

    # Phase 2: Health check
    health = health_check(public_ip, args.has_app, args.probe_retries,
                          args.probe_interval)
    elapsed = int(time.time() - start_time)

    if health["nginx"] != "pass":
        output = {
            "status": "failed",
            "stage": "health_check",
            "error": f"Nginx health check failed after {args.probe_retries} retries",
            "public_ip": public_ip,
            "instance_id": instance_id,
            "outputs": outputs,
            "health": health,
            "elapsed_seconds": elapsed,
        }
        print(json.dumps(output, ensure_ascii=False))
        sys.exit(1)

    # Nginx passed. App liveness (health["app"] == "manual") is verified out-of-band
    # via Cloud Assistant -- see reference/rules/rule_error_handling.md.
    output = {
        "status": "ok",
        "public_ip": public_ip,
        "instance_id": instance_id,
        "outputs": outputs,
        "health": health,
        "elapsed_seconds": elapsed,
    }
    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
