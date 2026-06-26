#!/usr/bin/env python3
"""
Salesforce OAuth Token Exchange Helper

Three authentication methods:
  1. exchange  — OAuth 2.0 authorization-code flow (Connected App)
  2. refresh   — Refresh an existing access token
  3. platform  — Extract token from Salesforce Platform CLI (sf / sfdx)
               No secrets needed — reads the token the CLI already stored.

SECURITY DESIGN:
- Library functions accept all values as parameters (no env reads, no argv).
- The CLI reads ALL sensitive values from environment variables or secure
  stdin prompt (getpass). Nothing sensitive is ever in sys.argv.
- argv is used ONLY for command name and flags — never for secret values.
- Token exchange POSTs only to the hard-coded Salesforce allowlist.

Author: Sawera Khadium
"""

import os
import sys
import json
import getpass
import subprocess
import shutil
from typing import Dict, Optional, Tuple

import requests
from dotenv import load_dotenv

# Only these endpoints may ever receive OAuth credential POSTs.
_ALLOWED_ENDPOINTS = frozenset([
    "https://login.salesforce.com/services/oauth2/token",
    "https://test.salesforce.com/services/oauth2/token",
])


def _safe_post(endpoint: str, form: dict, timeout: int = 30) -> requests.Response:
    """POST only to allowlisted Salesforce endpoints; raise on anything else."""
    if endpoint not in _ALLOWED_ENDPOINTS:
        raise ValueError(f"Endpoint not in Salesforce allowlist: {endpoint}")
    return requests.post(endpoint, data=form, timeout=timeout)


# ─────────────────────────────────────────────────────────────────────────────
# Method 1 — Authorization-code exchange (Connected App OAuth flow)
# ─────────────────────────────────────────────────────────────────────────────

def exchange_code(
    code: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str = "http://localhost:8080/oauth/callback",
    sandbox: bool = False,
) -> Tuple[bool, str, Optional[Dict]]:
    """Exchange a one-time authorization code for an access token.

    Typical flow:
      1. Call connect.py oauth <client_id> → user authorizes in browser
      2. Browser redirects with ?code=...
      3. Call this function with that code.

    Returns (success, message, safe_metadata).
    Raw access/refresh tokens are NOT included in the returned dict.
    """
    endpoint = (
        "https://test.salesforce.com/services/oauth2/token"
        if sandbox else
        "https://login.salesforce.com/services/oauth2/token"
    )
    try:
        resp = _safe_post(endpoint, {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        })
        resp.raise_for_status()
        payload = resp.json()
        return True, "OAuth exchange successful", {
            "instance_url": payload.get("instance_url", ""),
            "scope": payload.get("scope"),
            "token_type": payload.get("token_type"),
            "method": "authorization_code",
        }
    except Exception as exc:
        return False, f"OAuth exchange failed: {exc}", None


# ─────────────────────────────────────────────────────────────────────────────
# Method 2 — Refresh token
# ─────────────────────────────────────────────────────────────────────────────

def refresh_token(
    token: str,
    client_id: str,
    client_secret: str,
    sandbox: bool = False,
) -> Tuple[bool, str, Optional[Dict]]:
    """Obtain a new access token using a refresh token.

    Use this when your access token has expired but you still have a
    valid refresh token from a prior authorization-code flow.

    Returns metadata only — the new access token is NOT returned.
    Write it to your .env by calling connect.py connect afterward.
    """
    endpoint = (
        "https://test.salesforce.com/services/oauth2/token"
        if sandbox else
        "https://login.salesforce.com/services/oauth2/token"
    )
    try:
        resp = _safe_post(endpoint, {
            "grant_type": "refresh_token",
            "refresh_token": token,
            "client_id": client_id,
            "client_secret": client_secret,
        })
        resp.raise_for_status()
        payload = resp.json()
        return True, "Token refreshed — update SALESFORCE_ACCESS_TOKEN in your .env", {
            "instance_url": payload.get("instance_url", ""),
            "token_type": payload.get("token_type"),
            "method": "refresh_token",
        }
    except Exception as exc:
        return False, f"Token refresh failed: {exc}", None


# ─────────────────────────────────────────────────────────────────────────────
# Method 3 — Salesforce Platform CLI token extraction (sf / sfdx)
# ─────────────────────────────────────────────────────────────────────────────

def _find_sf_cli() -> Optional[str]:
    """Return the path to the sf or sfdx CLI binary, or None if not installed."""
    return shutil.which("sf") or shutil.which("sfdx")


def list_platform_cli_orgs() -> Tuple[bool, str, Optional[Dict]]:
    """List all orgs the Salesforce Platform CLI knows about.

    Requires the Salesforce CLI to be installed and at least one org
    to have been authenticated with:
      sf org login web   (or: sfdx auth:web:login)

    No credentials or secrets needed — reads from the CLI's local keychain.
    """
    cli = _find_sf_cli()
    if not cli:
        return False, (
            "Salesforce Platform CLI (sf/sfdx) is not installed or not on PATH. "
            "Install from: https://developer.salesforce.com/tools/salesforcecli"
        ), None

    try:
        result = subprocess.run(
            [cli, "org", "list", "--json"],
            capture_output=True, text=True, timeout=15,
        )
        data = json.loads(result.stdout)
        orgs = (
            data.get("result", {}).get("nonScratchOrgs", []) +
            data.get("result", {}).get("scratchOrgs", [])
        )
        if not orgs:
            return False, (
                "No orgs found in Salesforce CLI. "
                "Authenticate first with: sf org login web"
            ), None

        safe_orgs = [
            {
                "alias":        o.get("alias", ""),
                "username":     o.get("username", ""),
                "instance_url": o.get("instanceUrl", ""),
                "is_default":   o.get("isDefaultUsername", False),
                "org_type":     "scratch" if o.get("isScratch") else "standard",
            }
            for o in orgs
        ]
        return True, f"Found {len(safe_orgs)} org(s) in Salesforce CLI", {
            "orgs": safe_orgs,
            "method": "platform_cli",
        }
    except json.JSONDecodeError:
        return False, "Could not parse Salesforce CLI output as JSON", None
    except subprocess.TimeoutExpired:
        return False, "Salesforce CLI timed out — check your network", None
    except Exception as exc:
        return False, f"Salesforce CLI error: {exc}", None


def extract_platform_cli_token(
    username_or_alias: str = "",
    sandbox: bool = False,
) -> Tuple[bool, str, Optional[Dict]]:
    """Extract an access token from the Salesforce Platform CLI's keychain.

    The Salesforce CLI (sf/sfdx) stores tokens locally after you run:
      sf org login web --alias myorg

    This function retrieves that stored token without asking for any
    credentials. It is the safest method — no secrets are ever typed,
    stored in .env, or passed via command line.

    Args:
        username_or_alias: The org alias or username to retrieve the token for.
                           Leave empty to use the CLI's default org.
        sandbox:           Set True if this is a sandbox org.

    Returns (success, message, safe_metadata).
    The access token is written directly to SALESFORCE_ACCESS_TOKEN env var
    in the current process and printed as a masked value only.
    """
    cli = _find_sf_cli()
    if not cli:
        return False, (
            "Salesforce Platform CLI (sf/sfdx) is not installed. "
            "Install from: https://developer.salesforce.com/tools/salesforcecli  "
            "Then run: sf org login web --alias myorg"
        ), None

    # Build command — username/alias is not a secret (it's a label)
    cmd = [cli, "org", "display", "--json"]
    if username_or_alias:
        cmd += ["--target-org", username_or_alias]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip()
            return False, (
                f"Salesforce CLI returned error: {err}\n"
                "Make sure you have authenticated: sf org login web"
            ), None

        data = json.loads(result.stdout)
        org  = data.get("result", {})

        access_token  = org.get("accessToken", "")
        instance_url  = org.get("instanceUrl", "")
        org_username  = org.get("username", "")
        org_alias     = org.get("alias", "")

        if not access_token:
            return False, (
                "No access token found for this org. "
                "Re-authenticate with: sf org login web"
            ), None

        # Write to environment for use by connect.py in this process session.
        # The raw token is never printed in full — masked for security.
        os.environ["SALESFORCE_ACCESS_TOKEN"] = access_token
        os.environ["SALESFORCE_INSTANCE_URL"] = instance_url

        masked = access_token[:6] + "..." + access_token[-4:] if len(access_token) > 12 else "***"

        return True, (
            f"Token extracted from Salesforce CLI for '{org_alias or org_username}'. "
            "SALESFORCE_ACCESS_TOKEN and SALESFORCE_INSTANCE_URL are set in this session."
        ), {
            "instance_url":    instance_url,
            "username":        org_username,
            "alias":           org_alias,
            "access_token":    masked,   # masked — never the full value
            "method":          "platform_cli",
            "note": (
                "Token is set in the current process environment. "
                "To persist it, add SALESFORCE_ACCESS_TOKEN and "
                "SALESFORCE_INSTANCE_URL to your .env file."
            ),
        }
    except json.JSONDecodeError:
        return False, "Could not parse Salesforce CLI output — is sf/sfdx up to date?", None
    except subprocess.TimeoutExpired:
        return False, "Salesforce CLI timed out", None
    except Exception as exc:
        return False, f"Platform CLI extraction failed: {exc}", None


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# All secrets from env or getpass. argv = command + flags only.
# ─────────────────────────────────────────────────────────────────────────────

def _read_secret(env_key: str, prompt: str) -> str:
    """Read a secret from env var, or prompt securely via getpass."""
    val = os.getenv(env_key, "").strip()
    if val:
        return val
    return getpass.getpass(prompt).strip()


def _print_usage() -> None:
    print("""
Salesforce OAuth Helper — three methods

METHOD 1 — Authorization-code (Connected App):
  python oauth.py exchange [--sandbox]
  Env vars: SALESFORCE_CLIENT_ID, SALESFORCE_CLIENT_SECRET, SALESFORCE_OAUTH_CODE

METHOD 2 — Refresh token:
  python oauth.py refresh [--sandbox]
  Env vars: SALESFORCE_CLIENT_ID, SALESFORCE_CLIENT_SECRET, SALESFORCE_REFRESH_TOKEN

METHOD 3 — Salesforce Platform CLI (no secrets needed):
  python oauth.py platform [--alias myorg] [--list]
  Requires: sf org login web (run once, then use this forever)
  --list   Show all authenticated orgs
  --alias  Specify org alias or username (default: CLI default org)

All secret values are read from environment variables or secure stdin prompt.
Never pass secrets as command-line arguments.
""")


def main() -> None:
    load_dotenv()
    args = sys.argv[1:]

    if not args or args[0] not in ("exchange", "refresh", "platform"):
        _print_usage()
        sys.exit(1 if args else 0)

    cmd     = args[0]
    sandbox = "--sandbox" in args

    # ── Method 1: authorization-code exchange ──
    if cmd == "exchange":
        client_id     = _read_secret("SALESFORCE_CLIENT_ID",     "Client ID: ")
        client_secret = _read_secret("SALESFORCE_CLIENT_SECRET", "Client Secret: ")
        code          = _read_secret("SALESFORCE_OAUTH_CODE",    "Authorization Code: ")

        if not all([client_id, client_secret, code]):
            print(json.dumps({"success": False, "error": "client_id, client_secret, and code are required."}))
            sys.exit(1)

        ok, msg, data = exchange_code(code, client_id, client_secret, sandbox=sandbox)
        client_id = client_secret = code = ""  # noqa

    # ── Method 2: refresh token ──
    elif cmd == "refresh":
        client_id     = _read_secret("SALESFORCE_CLIENT_ID",     "Client ID: ")
        client_secret = _read_secret("SALESFORCE_CLIENT_SECRET", "Client Secret: ")
        token         = _read_secret("SALESFORCE_REFRESH_TOKEN", "Refresh Token: ")

        if not all([client_id, client_secret, token]):
            print(json.dumps({"success": False, "error": "client_id, client_secret, and refresh_token are required."}))
            sys.exit(1)

        ok, msg, data = refresh_token(token, client_id, client_secret, sandbox=sandbox)
        client_id = client_secret = token = ""  # noqa

    # ── Method 3: Salesforce Platform CLI ──
    elif cmd == "platform":
        if "--list" in args:
            ok, msg, data = list_platform_cli_orgs()
        else:
            # --alias value: next arg after --alias, not a secret
            alias = ""
            if "--alias" in args:
                idx = args.index("--alias")
                alias = args[idx + 1] if idx + 1 < len(args) else ""
            ok, msg, data = extract_platform_cli_token(alias, sandbox=sandbox)

    print(json.dumps({"success": ok, "message": msg, **(data or {})}, indent=2))


if __name__ == "__main__":
    main()
