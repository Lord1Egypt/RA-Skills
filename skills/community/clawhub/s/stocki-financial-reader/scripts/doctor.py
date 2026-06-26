#!/usr/bin/env python3
"""stocki-financial-reader doctor: 4-check self-diagnostic.

[1/4] Env vars       — STOCKI_GATEWAY_URL + STOCKI_API_KEY presence + key format check + masked display
[2/4] Skill version  — read local SKILL.md frontmatter version; optional remote compare
[3/4] File integrity — optional SHA256 verification (skipped if scripts/checksums.sha256 absent)
[4/4] Workspace      — does NOT create ~/stocki/; reports OK only

Exit: 0 = all ok, 1 = anything failed (or auth-class problem).
stdlib-only.
"""

import hashlib
import json
import os
import re
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)


def mask_key(key):
    if not key or len(key) < 5:
        return "(empty)"
    return f"{key[:3]}...{key[-2:]}"


def check_env():
    base = os.environ.get("STOCKI_GATEWAY_URL", "")
    key = os.environ.get("STOCKI_API_KEY", "")
    missing = [n for n, v in (("STOCKI_GATEWAY_URL", base), ("STOCKI_API_KEY", key)) if not v]
    if missing:
        return False, f"{', '.join(missing)} not set"
    if not (key.startswith("sk_") or key.startswith("sk-") or key.startswith("eyJ")):
        return False, f"STOCKI_API_KEY must start with 'sk_' (legacy), 'sk-' (PAT), or 'eyJ' (JWT) (got: {mask_key(key)})"
    return True, f"{base} + {mask_key(key)}"


def read_local_version(path):
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^version:\s*(.+?)\s*$", line)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    return None


def fetch_remote_version(url, timeout=10):
    try:
        req = Request(url, method="GET")
        with urlopen(req, timeout=timeout) as resp:
            for line in resp.read().decode("utf-8").splitlines():
                m = re.match(r"^version:\s*(.+?)\s*$", line)
                if m:
                    return m.group(1).strip().strip('"').strip("'")
    except (URLError, TimeoutError, OSError):
        return None
    return None


def verify_integrity(checksum_file, base_dir):
    if not os.path.isfile(checksum_file):
        return True, "(no checksums.sha256, skipped)"
    with open(checksum_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue
            expected, name = parts
            target = os.path.join(base_dir, name)
            if not os.path.isfile(target):
                return False, f"missing: {name}"
            h = hashlib.sha256()
            with open(target, "rb") as bf:
                for chunk in iter(lambda: bf.read(8192), b""):
                    h.update(chunk)
            if h.hexdigest() != expected:
                return False, f"modified: {name}"
    return True, "all checksums match"


def main():
    print("stocki-financial-reader Doctor")
    print("=" * 48)
    ok_count = 0
    fail_count = 0

    # 1/4 Env
    ok, msg = check_env()
    if ok:
        print(f"[1/4] Env vars       OK    {msg}")
        ok_count += 1
    else:
        print(f"[1/4] Env vars       FAIL  {msg}")
        fail_count += 1

    # 2/4 Version
    skill_md = os.path.join(SKILL_DIR, "SKILL.md")
    local_v = read_local_version(skill_md)
    if not local_v:
        print("[2/4] Skill version  FAIL  cannot read local SKILL.md version")
        fail_count += 1
    else:
        # Remote compare gated on STOCKI_HOMEPAGE_RAW (graceful degrade if absent)
        remote_url = os.environ.get("STOCKI_HOMEPAGE_RAW", "")
        if remote_url:
            remote_v = fetch_remote_version(remote_url)
            if not remote_v:
                print(f"[2/4] Skill version  WARN  v{local_v} (remote unreachable)")
                ok_count += 1
            elif local_v == remote_v:
                print(f"[2/4] Skill version  OK    v{local_v} (up to date)")
                ok_count += 1
            else:
                print(f"[2/4] Skill version  WARN  v{local_v} -> v{remote_v} available")
                ok_count += 1
        else:
            print(f"[2/4] Skill version  OK    v{local_v} (no remote URL configured)")
            ok_count += 1

    # 3/4 Integrity
    checksum_file = os.path.join(SCRIPT_DIR, "checksums.sha256")
    ok, msg = verify_integrity(checksum_file, SCRIPT_DIR)
    if ok:
        print(f"[3/4] File integrity OK    {msg}")
        ok_count += 1
    else:
        print(f"[3/4] File integrity FAIL  {msg}")
        fail_count += 1

    # 4/4 Workspace (no-op, just report OK)
    print("[4/4] Workspace      OK    (no persistent workspace required)")
    ok_count += 1

    print("=" * 48)
    print(f"Result: {ok_count} OK, {fail_count} failed")
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
