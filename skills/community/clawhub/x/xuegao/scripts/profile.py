#!/usr/bin/env python3
"""Account-bound, versioned preferences. Standard library only; no network calls."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile
import uuid


def read_profile(path, account):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("account_id") != account:
        raise ValueError("schema or account mismatch")
    return data


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".profile-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def locked(path):
    lock = Path(str(path) + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError("profile is busy; retry after the other writer finishes") from None
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink()


def initialize(path, account):
    if not account.strip():
        raise ValueError("account is required")
    with locked(path):
        if Path(path).exists():
            raise ValueError("profile already exists")
        data = {"schema_version": 1, "account_id": account, "revision": 0, "rules": []}
        atomic_json(path, data)
        return data


def record(path, account, expected, key, value, scope, evidence, confirmed=False, replaces=None):
    if not all(str(x).strip() for x in (key, value, scope, evidence)):
        raise ValueError("key, value, scope and evidence must be nonempty")
    if not re.fullmatch(r"[a-z][a-z0-9_.-]{0,63}", key):
        raise ValueError("key must be a stable lowercase identifier")
    with locked(path):
        data = read_profile(path, account)
        if data["revision"] != expected:
            raise ValueError("stale revision; read the latest profile first")
        active = [r for r in data["rules"] if r["status"] == "confirmed"
                  and r["key"] == key and r["scope"] == scope]
        if replaces:
            old = next((r for r in active if r["id"] == replaces), None)
            if not confirmed or old is None:
                raise ValueError("replacement requires confirmed evidence and an active matching rule")
        elif confirmed and active:
            raise ValueError("conflicting active rule; explicitly replace its id")
        archive = Path(str(path) + ".history") / f"{data['revision']}.json"
        if archive.exists():
            if json.loads(archive.read_text()) != data:
                raise ValueError("history collision")
        else:
            atomic_json(archive, data)
        new_id = uuid.uuid4().hex[:12]
        if replaces:
            old["status"] = "superseded"
            old["superseded_by"] = new_id
        data["rules"].append({"id": new_id, "key": key, "value": value, "scope": scope,
                              "evidence": evidence, "status": "confirmed" if confirmed else "proposed",
                              "replaces": replaces, "created_at": datetime.now(timezone.utc).isoformat()})
        data["revision"] += 1
        atomic_json(path, data)
        return data


def context(path, account, scope):
    data = read_profile(path, account)
    rules = [r for r in data["rules"] if r["status"] == "confirmed" and r["scope"] in (scope, "*")]
    keys = [r["key"] for r in rules]
    if len(set(keys)) != len(keys):
        raise ValueError("overlapping scope conflict; resolve before generating")
    return {"account_id": account, "profile_version": data["revision"], "scope": scope,
            "confirmed_preferences": rules}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--account", required=True, help="Trusted account identity supplied by the caller")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    show = sub.add_parser("context")
    show.add_argument("--scope", required=True)
    add = sub.add_parser("record")
    for field in ("key", "value", "scope", "evidence"):
        add.add_argument("--" + field, required=True)
    add.add_argument("--expected-revision", type=int, required=True)
    add.add_argument("--confirmed", action="store_true", help="Use only for explicit author instructions/confirmation")
    add.add_argument("--replaces", help="ID of the confirmed rule being superseded")
    args = parser.parse_args()
    try:
        if args.command == "init":
            result = initialize(args.profile, args.account)
        elif args.command == "context":
            result = context(args.profile, args.account, args.scope)
        else:
            result = record(args.profile, args.account, args.expected_revision, args.key, args.value,
                            args.scope, args.evidence, args.confirmed, args.replaces)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        parser.exit(2, f"profile error: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
