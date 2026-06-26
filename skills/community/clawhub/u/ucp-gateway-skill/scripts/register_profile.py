#!/usr/bin/env python3
"""Register a local UCP Gateway public key with the MCP endpoint."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_GATEWAY = "https://ucpgateway.theagenttimes.com/mcp"
PACKAGE_VERSION = "0.2.3"
PRIVATE_FIELDS = {"d", "p", "q", "dp", "dq", "qi", "k"}


class RegisterProfileError(Exception):
    """Raised for safe, user-facing registration failures."""


def read_json(path):
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise RegisterProfileError(
            "Missing ./.ucpgateway/public_key.jwk. Run python3 scripts/init_ucpgateway.py first or provide a local EC P-256 public JWK."
        ) from exc
    except json.JSONDecodeError as exc:
        raise RegisterProfileError(f"{path} is not valid JSON: {exc.msg}.") from exc


def read_json_if_exists(path):
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def write_json(path, value, mode):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, indent=2) + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)
    try:
        os.chmod(path, mode)
    except PermissionError:
        pass


def ensure_public_jwk(public_jwk):
    if not isinstance(public_jwk, dict):
        raise RegisterProfileError("public_key.jwk must contain a JSON object.")
    leaked = sorted(PRIVATE_FIELDS.intersection(public_jwk))
    if leaked:
        raise RegisterProfileError(f"public_key.jwk contains private JWK field(s): {', '.join(leaked)}; refusing to send it.")
    if public_jwk.get("kty") != "EC" or public_jwk.get("crv") != "P-256" or not public_jwk.get("x") or not public_jwk.get("y"):
        raise RegisterProfileError("public_key.jwk must be an EC P-256 public JWK with x and y coordinates.")


def post_json(url, payload, timeout=60):
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"content-type": "application/json", "accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            raise RegisterProfileError(f"Gateway HTTP {exc.code}: {body[:1000]}") from exc
        return parsed
    except urllib.error.URLError as exc:
        raise RegisterProfileError(f"Could not reach UCP Gateway MCP endpoint: {exc.reason}") from exc

    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise RegisterProfileError("Gateway response was not valid JSON.") from exc


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Register the local UCP Gateway public key and save agent.json.")
    parser.add_argument("--namespace", default=os.environ.get("UCP_NAMESPACE") or "openclaw")
    parser.add_argument("--agent-name", default=os.environ.get("UCP_AGENT_NAME") or "OpenClaw UCP Shopping Agent")
    parser.add_argument(
        "--description",
        default=os.environ.get("UCP_AGENT_DESCRIPTION")
        or "Open-source agent using The Agent Times UCP Gateway for UCP Shopping handoff.",
    )
    parser.add_argument("--skill-version", default=os.environ.get("npm_package_version") or PACKAGE_VERSION)
    return parser.parse_args(argv)


def run(argv=None, cwd=None, stdout=None, stderr=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    root = Path(cwd or os.getcwd())
    gateway = os.environ.get("UCP_GATEWAY_MCP_URL") or DEFAULT_GATEWAY
    directory = root / ".ucpgateway"
    public_key_path = directory / "public_key.jwk"
    agent_path = directory / "agent.json"

    public_key_jwk = read_json(public_key_path)
    ensure_public_jwk(public_key_jwk)

    request_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "register_ucp_profile",
            "arguments": {
                "namespace": args.namespace,
                "agent_name": args.agent_name,
                "description": args.description,
                "public_key_jwk": public_key_jwk,
                "metadata": {"runtime": "openclaw"},
                "skill_name": "ucp-gateway-skill",
                "skill_version": args.skill_version,
            },
        },
    }

    response = post_json(gateway, request_payload)
    payload = (((response or {}).get("result") or {}).get("structuredContent") or {})
    if not payload.get("ok"):
        print(json.dumps(response, indent=2), file=stderr)
        error = payload.get("error") or (response or {}).get("error") or {}
        message = error.get("message") if isinstance(error, dict) else None
        raise RegisterProfileError(message or "register_ucp_profile failed")

    saved_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    canonical_agent = {
        "agent_id": payload.get("agent_id"),
        "namespace": payload.get("namespace"),
        "profile_url": payload.get("profile_url"),
        "registry_url": payload.get("registry_url"),
        "gateway_mcp_url": gateway,
        "profile_json": payload.get("profile_json"),
        "created": payload.get("created"),
        "existing_profile": payload.get("existing_profile"),
        "message": payload.get("message"),
        "saved_at": saved_at,
    }

    existing_agent = read_json_if_exists(agent_path)
    should_preserve_local = payload.get("existing_profile") is True and isinstance(existing_agent, dict) and existing_agent.get("agent_id") == payload.get("agent_id")
    if should_preserve_local:
        agent = dict(existing_agent)
        agent.update(
            {
                "created": payload.get("created"),
                "existing_profile": payload.get("existing_profile"),
                "message": payload.get("message"),
                "saved_at": saved_at,
            }
        )
    else:
        agent = canonical_agent

    write_json(agent_path, agent, 0o600)
    print(json.dumps(agent, indent=2), file=stdout)
    if payload.get("existing_profile") is True:
        print(f"Existing active profile reused (idempotent); hosted profile not modified. Using agent_id {payload.get('agent_id')}.", file=stdout)
    print("Saved ./.ucpgateway/agent.json. Gateway built profile_json; use agent_id in every Shopping tool call.", file=stdout)
    return 0


def main():
    try:
        return run()
    except RegisterProfileError as exc:
        print(f"register_profile: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
