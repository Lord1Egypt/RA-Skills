#!/usr/bin/env python3
"""Initialize local UCP Gateway identity files using Python stdlib only."""

import argparse
import base64
import json
import os
import secrets
import sys
from pathlib import Path

MIN_PYTHON = (3, 8)
SCRIPT_NAME = "init_ucpgateway.py"
UCP_VERSION = "2026-04-08"

# NIST P-256 / secp256r1 constants.
P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
A = P - 3
B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
G = (GX, GY)

PRIVATE_FIELDS = {"d", "p", "q", "dp", "dq", "qi", "k"}


def require_supported_python():
    if sys.version_info >= MIN_PYTHON:
        return
    required = ".".join(str(part) for part in MIN_PYTHON)
    current = ".".join(str(part) for part in sys.version_info[:3])
    print(
        f"{SCRIPT_NAME} requires Python {required}+; current Python is {current}. "
        f"Run it with `uv run python scripts/{SCRIPT_NAME} ...` or a Python {required}+ interpreter.",
        file=sys.stderr,
    )
    sys.exit(2)


require_supported_python()


class UcpInitError(Exception):
    """Raised for safe, user-facing initialization failures."""


def _print(message, stream):
    stream.write(f"{message}\n")


def base64url_uint(value):
    return base64.urlsafe_b64encode(value.to_bytes(32, "big")).decode("ascii").rstrip("=")


def base64url_to_uint(value, field_name):
    if not isinstance(value, str) or not value:
        raise UcpInitError(f"JWK field {field_name} must be a non-empty base64url string.")
    padding = "=" * (-len(value) % 4)
    try:
        decoded = base64.urlsafe_b64decode((value + padding).encode("ascii"))
    except Exception as exc:  # noqa: BLE001 - keep CLI error concise
        raise UcpInitError(f"JWK field {field_name} is not valid base64url.") from exc
    if len(decoded) != 32:
        raise UcpInitError(f"JWK field {field_name} must encode exactly 32 bytes for P-256.")
    return int.from_bytes(decoded, "big")


def is_on_curve(point):
    if point is None:
        return False
    x, y = point
    if not (0 <= x < P and 0 <= y < P):
        return False
    return (y * y - (x * x * x + A * x + B)) % P == 0


def point_add(left, right):
    if left is None:
        return right
    if right is None:
        return left

    x1, y1 = left
    x2, y2 = right

    if x1 == x2 and (y1 + y2) % P == 0:
        return None

    if left == right:
        if y1 == 0:
            return None
        slope = ((3 * x1 * x1 + A) * pow(2 * y1, -1, P)) % P
    else:
        slope = ((y2 - y1) * pow((x2 - x1) % P, -1, P)) % P

    x3 = (slope * slope - x1 - x2) % P
    y3 = (slope * (x1 - x3) - y1) % P
    return (x3, y3)


def scalar_multiply(scalar, point=G):
    if scalar % N == 0 or point is None:
        return None
    if not is_on_curve(point):
        raise UcpInitError("Cannot multiply a point that is not on the P-256 curve.")

    result = None
    addend = point
    k = scalar
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result


def jwk_public_from_xy(x, y, source=None):
    jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": base64url_uint(x),
        "y": base64url_uint(y),
        "kid": "local-key-1",
        "alg": "ES256",
        "use": "sig",
    }
    if source:
        for field in ("kid", "alg", "use"):
            if source.get(field) is not None:
                jwk[field] = source[field]
        if source.get("ext") is not None:
            jwk["ext"] = source["ext"]
        if source.get("key_ops") is not None:
            # A public JWK should only expose verification operations.
            key_ops = source["key_ops"]
            if isinstance(key_ops, list) and "verify" in key_ops and "sign" not in key_ops:
                jwk["key_ops"] = key_ops
    return jwk


def generate_keypair():
    d = secrets.randbelow(N - 1) + 1
    public_point = scalar_multiply(d, G)
    if public_point is None or not is_on_curve(public_point):
        raise UcpInitError("Generated invalid P-256 key material; refusing to write files.")
    x, y = public_point
    private_jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": base64url_uint(x),
        "y": base64url_uint(y),
        "d": base64url_uint(d),
        "kid": "local-key-1",
        "alg": "ES256",
        "use": "sig",
        "ext": True,
        "key_ops": ["sign"],
    }
    public_jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": private_jwk["x"],
        "y": private_jwk["y"],
        "kid": "local-key-1",
        "alg": "ES256",
        "use": "sig",
        "ext": True,
        "key_ops": ["verify"],
    }
    return private_jwk, public_jwk


def validate_public_jwk(public_jwk):
    if not isinstance(public_jwk, dict):
        raise UcpInitError("public_key.jwk must contain a JSON object.")
    leaked = sorted(PRIVATE_FIELDS.intersection(public_jwk))
    if leaked:
        raise UcpInitError(f"public_key.jwk contains private JWK field(s): {', '.join(leaked)}; refusing to continue.")
    if public_jwk.get("kty") != "EC" or public_jwk.get("crv") != "P-256":
        raise UcpInitError("public_key.jwk must be an EC P-256 public JWK.")
    x = base64url_to_uint(public_jwk.get("x"), "x")
    y = base64url_to_uint(public_jwk.get("y"), "y")
    if not is_on_curve((x, y)):
        raise UcpInitError("public_key.jwk coordinates are not on the P-256 curve.")
    return (x, y)


def derive_public_from_private(private_jwk):
    if not isinstance(private_jwk, dict):
        raise UcpInitError("private_key.jwk must contain a JSON object.")
    if private_jwk.get("kty") != "EC" or private_jwk.get("crv") != "P-256":
        raise UcpInitError("private_key.jwk must be an EC P-256 private JWK.")
    for field in ("d", "x", "y"):
        if not private_jwk.get(field):
            raise UcpInitError(f"private_key.jwk is missing required P-256 field {field}.")

    d = base64url_to_uint(private_jwk["d"], "d")
    if not (1 <= d < N):
        raise UcpInitError("private_key.jwk scalar d is outside the valid P-256 range.")

    stored_x = base64url_to_uint(private_jwk["x"], "x")
    stored_y = base64url_to_uint(private_jwk["y"], "y")
    if not is_on_curve((stored_x, stored_y)):
        raise UcpInitError("private_key.jwk public coordinates are not on the P-256 curve.")

    derived = scalar_multiply(d, G)
    if derived != (stored_x, stored_y):
        raise UcpInitError("private_key.jwk public coordinates do not match scalar d; refusing to derive public_key.jwk.")
    return jwk_public_from_xy(derived[0], derived[1], private_jwk)


def same_public_coordinates(left, right):
    return validate_public_jwk(left) == validate_public_jwk(right)


def read_json(path):
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise UcpInitError(f"Missing {path}.") from exc
    except json.JSONDecodeError as exc:
        raise UcpInitError(f"{path} is not valid JSON: {exc.msg}.") from exc


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


def profile_draft(public_jwk, env):
    return {
        "ucp": {
            "version": UCP_VERSION,
            "capabilities": {
                "dev.ucp.shopping.catalog.search": [{"version": UCP_VERSION}],
                "dev.ucp.shopping.catalog.lookup": [{"version": UCP_VERSION}],
                "dev.ucp.shopping.catalog": [{"version": UCP_VERSION}],
                "dev.ucp.shopping.cart": [{"version": UCP_VERSION}],
                "dev.ucp.shopping.checkout": [{"version": UCP_VERSION}],
            },
            "payment_handlers": {},
        },
        "signing_keys": [public_jwk],
        "metadata": {
            "name": env.get("UCP_AGENT_NAME") or "OpenClaw UCP Shopping Agent",
            "description": "Open-source agent using The Agent Times UCP Gateway for UCP Shopping handoff.",
            "runtime": "openclaw",
            "skill": "ucp-gateway-skill",
        },
    }


def dry_run_message(stdout):
    _print("Would initialize ./.ucpgateway/ local identity. No files changed.", stdout)
    _print(
        "Partial-state handling: private-only derives public_key.jwk from private scalar; public-only fails unless --public-only; existing private_key.jwk is never overwritten unless --force-rotate.",
        stdout,
    )
    _print("profile.draft.json is legacy-only; pass --legacy-draft to create it.", stdout)


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Initialize local UCP Gateway EC P-256 identity files.")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without writing files.")
    parser.add_argument("--legacy-draft", action="store_true", help="Also create profile.draft.json when absent.")
    parser.add_argument("--public-only", action="store_true", help="Allow public_key.jwk without a local private key.")
    parser.add_argument("--force-rotate", action="store_true", help="Intentionally overwrite both key files with a fresh local keypair.")
    return parser.parse_args(argv)


def run(argv=None, cwd=None, env=None, stdout=None, stderr=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    env = env or os.environ
    root = Path(cwd or os.getcwd())
    directory = root / ".ucpgateway"
    private_path = directory / "private_key.jwk"
    public_path = directory / "public_key.jwk"
    draft_path = directory / "profile.draft.json"

    if args.dry_run:
        dry_run_message(stdout)
        return 0

    directory.mkdir(parents=True, exist_ok=True)

    private_exists = private_path.exists()
    public_exists = public_path.exists()
    public_jwk = None

    if args.force_rotate:
        _print("--force-rotate requested: overwriting both private_key.jwk and public_key.jwk with a fresh local keypair.", stderr)
        private_jwk, public_jwk = generate_keypair()
        write_json(private_path, private_jwk, 0o600)
        write_json(public_path, public_jwk, 0o644)
    elif private_exists and public_exists:
        private_jwk = read_json(private_path)
        public_jwk = read_json(public_path)
        derived_public = derive_public_from_private(private_jwk)
        if not same_public_coordinates(public_jwk, derived_public):
            raise UcpInitError("Existing public_key.jwk does not match private_key.jwk; fix the files or use --force-rotate to intentionally replace both.")
        _print("Reusing existing local keypair.", stdout)
    elif not private_exists and not public_exists:
        private_jwk, public_jwk = generate_keypair()
        write_json(private_path, private_jwk, 0o600)
        write_json(public_path, public_jwk, 0o644)
        _print("Generated new local keypair.", stdout)
    elif private_exists and not public_exists:
        private_jwk = read_json(private_path)
        public_jwk = derive_public_from_private(private_jwk)
        write_json(public_path, public_jwk, 0o644)
        _print("Derived public_key.jwk from existing private_key.jwk.", stdout)
    elif public_exists:
        public_jwk = read_json(public_path)
        validate_public_jwk(public_jwk)
        if not args.public_only:
            raise UcpInitError("Found public_key.jwk but no private_key.jwk; re-run with --public-only only if the matching private key is managed elsewhere.")
        _print("Continuing with public-only state because --public-only was provided. Ensure the matching private key is managed elsewhere.", stderr)

    if args.legacy_draft and not draft_path.exists():
        write_json(draft_path, profile_draft(public_jwk, env), 0o644)

    _print(f"Initialized {directory.relative_to(root)}", stdout)
    _print(
        "Private key stays local and must never be uploaded. Next: uv run python scripts/register_profile.py (sends public_key_jwk; gateway builds the UCP profile).",
        stdout,
    )
    return 0


def main():
    try:
        return run()
    except UcpInitError as exc:
        print(f"init_ucpgateway: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
