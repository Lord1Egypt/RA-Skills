#!/usr/bin/env python3
"""Sync the current Codex CLI OAuth login into OpenClaw auth profiles.

Advanced mode: reads ~/.codex/auth.json token fields and writes an OpenClaw
openai-codex OAuth profile. Never prints token values.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import tempfile
import time
from pathlib import Path

PROVIDER = "openai-codex"
OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", str(Path.home() / ".openclaw")))
OPENCLAW_AGENT_ID = os.environ.get("OPENCLAW_AGENT_ID", "main")
OPENCLAW_AGENT_DIR = Path(os.environ.get("OPENCLAW_AGENT_DIR", str(OPENCLAW_HOME / "agents" / OPENCLAW_AGENT_ID / "agent")))
STATE_PATH = Path(os.environ.get("OPENCLAW_AUTH_STATE", str(OPENCLAW_AGENT_DIR / "auth-state.json")))
PROFILES_PATH = Path(os.environ.get("OPENCLAW_AUTH_PROFILES", str(OPENCLAW_AGENT_DIR / "auth-profiles.json")))
CODEX_AUTH_PATH = Path(os.environ.get("CODEX_AUTH_PATH", str(Path.home() / ".codex" / "auth.json")))


def load_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        if default is not None:
            return default
        raise SystemExit(f"missing file: {path}")
    except Exception as exc:
        raise SystemExit(f"failed to read {path}: {type(exc).__name__}")


def atomic_write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    finally:
        try:
            if os.path.exists(tmp):
                os.unlink(tmp)
        except Exception:
            pass


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    backup = path.with_name(f"{path.name}.bak-{time.strftime('%Y%m%d-%H%M%S')}")
    backup.write_bytes(path.read_bytes())
    return backup


def decode_jwt_payload(token: str | None) -> dict:
    if not token or token.count(".") < 2:
        return {}
    try:
        payload = token.split(".", 2)[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload.encode("ascii")))
    except Exception:
        return {}


def normalize_email(value: str | None) -> str:
    value = (value or "").strip().lower()
    if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value):
        return value
    return ""


def extract_tokens(codex_auth: dict) -> dict:
    tokens = codex_auth.get("tokens") if isinstance(codex_auth.get("tokens"), dict) else codex_auth
    access = tokens.get("access_token") or tokens.get("access")
    refresh = tokens.get("refresh_token") or tokens.get("refresh")
    id_token = tokens.get("id_token") or tokens.get("idToken")
    account_id = tokens.get("account_id") or tokens.get("accountId") or codex_auth.get("account_id") or codex_auth.get("accountId")
    if not access or not refresh:
        raise SystemExit("Codex auth file does not contain access_token and refresh_token.")
    return {"access": access, "refresh": refresh, "id_token": id_token, "account_id": account_id}


def identity_from_tokens(tokens: dict) -> dict:
    claims = {}
    for key in ("id_token", "access"):
        claims.update({k: v for k, v in decode_jwt_payload(tokens.get(key)).items() if k not in claims})
    email = normalize_email(claims.get("email") or claims.get("preferred_username") or claims.get("https://api.openai.com/profile/email"))
    user_id = str(claims.get("sub") or claims.get("user_id") or claims.get("https://api.openai.com/profile/user_id") or "").strip()
    account_id = str(tokens.get("account_id") or claims.get("https://api.openai.com/profile/account_id") or "").strip()
    expires_candidates = []
    for key in ("access", "id_token"):
        exp = decode_jwt_payload(tokens.get(key)).get("exp")
        if isinstance(exp, (int, float)) and exp > 0:
            expires_candidates.append(int(exp * 1000))
    expires = max(expires_candidates) if expires_candidates else 0
    if email:
        profile_tail = email
    elif user_id:
        profile_tail = "user-" + hashlib.sha256(user_id.encode()).hexdigest()[:12]
    elif account_id:
        profile_tail = "account-" + hashlib.sha256(account_id.encode()).hexdigest()[:12]
    else:
        profile_tail = "codex-" + hashlib.sha256(tokens["access"].encode()).hexdigest()[:12]
    return {"email": email, "user_id": user_id, "account_id": account_id, "expires": expires, "profile_id": f"{PROVIDER}:{profile_tail}"}


def build_credential(tokens: dict, identity: dict) -> dict:
    cred = {
        "type": "oauth",
        "provider": PROVIDER,
        "access": tokens["access"],
        "refresh": tokens["refresh"],
        "expires": identity.get("expires") or 0,
    }
    if identity.get("email"):
        cred["email"] = identity["email"]
    if identity.get("account_id"):
        cred["accountId"] = identity["account_id"]
    return cred


def set_first_order(state: dict, profile_id: str):
    state.setdefault("version", 1)
    state.setdefault("order", {})
    order = state["order"].get(PROVIDER)
    if not isinstance(order, list):
        order = []
    state["order"][PROVIDER] = [profile_id] + [pid for pid in order if pid != profile_id]


def main():
    parser = argparse.ArgumentParser(description="Sync current Codex CLI login into OpenClaw openai-codex auth profiles.")
    parser.add_argument("--codex-auth", default=str(CODEX_AUTH_PATH), help="Path to Codex CLI auth.json")
    parser.add_argument("--profile-id", help="Override OpenClaw profile id, e.g. openai-codex:user@example.com")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--no-set-first", action="store_true", help="Do not make the synced profile first in auth order")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing profile id even if identity differs")
    args = parser.parse_args()

    codex_auth_path = Path(args.codex_auth).expanduser()
    codex_auth = load_json(codex_auth_path)
    tokens = extract_tokens(codex_auth)
    identity = identity_from_tokens(tokens)
    profile_id = args.profile_id or identity["profile_id"]
    if not profile_id.startswith(PROVIDER + ":"):
        raise SystemExit(f"profile id must start with {PROVIDER}:")
    credential = build_credential(tokens, identity)

    store = load_json(PROFILES_PATH, {"version": 1, "profiles": {}})
    store.setdefault("version", 1)
    store.setdefault("profiles", {})
    existing = store["profiles"].get(profile_id)
    if existing and not args.force:
        old_email = normalize_email(existing.get("email"))
        new_email = normalize_email(credential.get("email"))
        old_account = str(existing.get("accountId") or "").strip()
        new_account = str(credential.get("accountId") or "").strip()
        if old_email and new_email and old_email != new_email:
            raise SystemExit(f"refusing to overwrite {profile_id}: existing email differs; use --force")
        if old_account and new_account and old_account != new_account:
            raise SystemExit(f"refusing to overwrite {profile_id}: existing accountId differs; use --force")

    state = load_json(STATE_PATH, {"version": 1})
    if not args.no_set_first:
        set_first_order(state, profile_id)

    label = credential.get("email") or profile_id
    if args.dry_run:
        print("Codex CLI sync dry-run OK.")
        print(f"Profile: {profile_id}")
        print(f"Identity: {label}")
        print(f"Would write: {PROFILES_PATH}")
        if not args.no_set_first:
            print(f"Would set first in: {STATE_PATH}")
        return 0

    prof_backup = backup_file(PROFILES_PATH)
    state_backup = backup_file(STATE_PATH) if not args.no_set_first else None
    store["profiles"][profile_id] = credential
    atomic_write_json(PROFILES_PATH, store)
    if not args.no_set_first:
        atomic_write_json(STATE_PATH, state)

    print("Codex CLI sync completed.")
    print(f"Profile: {profile_id}")
    print(f"Identity: {label}")
    if prof_backup:
        print(f"Backup: {prof_backup}")
    if state_backup:
        print(f"State backup: {state_backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
