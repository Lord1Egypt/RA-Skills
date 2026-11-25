#!/usr/bin/env python3
"""use_credential.py — safely use a credential from local MGC in sealed mode

Core principle: credentials stay in their domain.
  Credentials live permanently in the executor's local MGC (info_type=text).
  This script is sealed as a .py file and handed to the executor agent. At
  run time it reads the credential through the MGC REST API, uses it once,
  and outputs only a summary — the credential itself is never printed and
  never written back.

Why credentials never go inside a sub-package:
  MGC chain mode encrypts scripts only. CSV / JSON / config files are
  plaintext inside the sub-package. So a credential can never be shipped
  as a file to the other side. It must be stored locally by the executor.

Usage:
  1) The executor first stores its credential in local MGC (local read only):
     mgc_save(
         info_type="text",
         info_owner="local_credentials",
         diff_2="credential",
         diff_3="api_token.txt",
         content="sk-your-token",
     )

  2) Sealed run (script delivered via chain-mode sub-package):
     mgc_run(
         info_type="script",
         info_owner="<info_owner inside package>",
         diff_3="use_credential.py",
         ext02='["--owner","local_credentials","--name","api_token.txt"]',
     )

  3) Local debug (plaintext, reads a disk file directly):
     python3 use_credential.py --local --token-file ./api_token.txt

Zero third-party dependencies (stdlib urllib).
"""

import argparse
import hashlib
import hmac
import json
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

MGC = "http://127.0.0.1:57219"
TOKEN_PATH = Path.home() / ".mgc/database/mgc_black_box/.mgc_token"


def _mgc_post(path, payload):
    """Call local MGC REST API."""
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    req = Request(
        f"{MGC}{path}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "X-MGC-Token": token,
        },
        method="POST",
    )
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def read_credential_from_mgc(info_owner, diff_2, diff_3):
    """Read a text-type credential from local MGC, return its string content."""
    resp = _mgc_post(
        "/api/mgc/sensitive/get",
        {
            "info_type": "text",
            "info_owner": info_owner,
            "diff_2": diff_2,
            "diff_3": diff_3,
        },
    )
    data = resp.get("data", "")
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        return data.get("content", "")
    raise RuntimeError(f"unexpected data type: {type(data)}")


def fingerprint(secret):
    """Credential fingerprint: a short irreversible summary for debugging without exposing the secret."""
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()[:12]


def use_credential(secret, payload):
    """Use the credential to perform a signed call (HMAC-SHA256 example; replace with your real API call)."""
    signature = hmac.new(
        secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return {
        "ok": True,
        "credential_fingerprint": fingerprint(secret),
        "payload": payload,
        "signature_prefix": signature[:16],
        "signed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


def main():
    parser = argparse.ArgumentParser(description="Safely use a local MGC credential in sealed mode")
    parser.add_argument("--owner", default="local_credentials",
                        help="info_owner of the credential in local MGC")
    parser.add_argument("--diff-2", default="credential",
                        help="diff_2 of the credential in local MGC")
    parser.add_argument("--name", default="api_token.txt",
                        help="diff_3 of the credential in local MGC")
    parser.add_argument("--token-file", default=None,
                        help="Local debug only: read credential directly from this disk file")
    parser.add_argument("--local", action="store_true",
                        help="Plaintext debug mode (read disk, do not touch MGC)")
    parser.add_argument("--payload", default="demo-task-payload",
                        help="Task content to sign")
    parser.add_argument("--output", default=None,
                        help="Result output path (default: Desktop)")
    args = parser.parse_args()

    if args.local or args.token_file:
        if not args.token_file:
            parser.error("--local mode also requires --token-file")
        secret = Path(args.token_file).read_text(encoding="utf-8").strip()
        mode = "local"
    else:
        secret = read_credential_from_mgc(args.owner, args.diff_2, args.name).strip()
        mode = "mgc-rest"

    if not secret:
        raise RuntimeError("credential is empty")

    result = use_credential(secret, args.payload)
    result["mode"] = mode

    out = Path(args.output) if args.output else (Path.home() / "Desktop" / "credential_use_result.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[use_credential] mode={mode} fingerprint={result['credential_fingerprint']} -> {out}",
          file=sys.stderr, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
