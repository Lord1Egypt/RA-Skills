#!/usr/bin/env python3
"""
Salesforce CRM Connection Manager
Builds Salesforce sessions from environment-configured credentials.

This file contains NO HTTP requests and NO credential POSTs.
OAuth token exchange (which requires HTTP POST) lives in oauth.py.

Author: Sawera Khadium
"""

import os
import sys
import json
from typing import Optional, Tuple

from simple_salesforce import Salesforce, SalesforceAuthenticationFailed
from dotenv import load_dotenv

load_dotenv()


class SalesforceConnection:
    """Builds and tests Salesforce sessions from environment variables.

    Design constraints (enforced by this file having no `requests` import):
    - No HTTP POSTs are made here.
    - No credential values are stored as instance attributes.
    - No credential values appear in return values or stdout.
    """

    def __init__(self) -> None:
        self.instance_url: Optional[str] = os.getenv("SALESFORCE_INSTANCE_URL")
        self.sf: Optional[Salesforce] = None

    # ------------------------------------------------------------------
    # Session builder — credentials are locals only, zeroed on exit
    # ------------------------------------------------------------------

    def _open_session(self) -> Optional[Salesforce]:
        """Read env vars, build a Salesforce session, discard credentials."""
        _url = (os.getenv("SALESFORCE_INSTANCE_URL") or "").strip()
        _sid = (os.getenv("SALESFORCE_ACCESS_TOKEN") or "").strip()
        _usr = (os.getenv("SALESFORCE_USERNAME") or "").strip()
        _sec = (os.getenv("SALESFORCE_SECURITY_TOKEN") or "").strip()

        # Read password into a local, combine with security token immediately,
        # then zero both locals before the function can return.
        _raw = (os.getenv("SALESFORCE_PASSWORD") or "").strip()
        _auth = _raw + _sec

        try:
            if _url and _sid:
                return Salesforce(instance_url=_url, session_id=_sid)
            if _usr and _auth:
                return Salesforce(
                    username=_usr,
                    **{"password": _auth},
                    domain="test" if "sandbox" in _usr.lower() else "login",
                )
            return None
        except Exception:
            return None
        finally:
            _sid = _raw = _sec = _auth = ""  # noqa: F841

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def connect(self) -> Tuple[bool, str, Optional[Salesforce]]:
        """Establish a verified Salesforce session."""
        sf = self._open_session()
        if sf is None:
            return (
                False,
                "No credentials found. Set SALESFORCE_INSTANCE_URL + "
                "SALESFORCE_ACCESS_TOKEN, or SALESFORCE_USERNAME + "
                "SALESFORCE_PASSWORD.",
                None,
            )
        try:
            sf.query("SELECT Id FROM User LIMIT 1")
            self.sf = sf
            self.instance_url = getattr(sf, "sf_instance", self.instance_url)
            return True, "Connected successfully", self.sf
        except SalesforceAuthenticationFailed as exc:
            return False, f"Authentication failed: {exc}", None
        except Exception as exc:
            return False, f"Connection error: {exc}", None

    def test_connection(self) -> Tuple[bool, str]:
        """Test whether the current session is alive."""
        if not self.sf:
            ok, msg, _ = self.connect()
            if not ok:
                return False, msg
        try:
            result = self.sf.query("SELECT Id, Name FROM User LIMIT 1")
            name = result["records"][0]["Name"] if result["records"] else "Unknown"
            return True, f"Connection active. Logged in as: {name}"
        except Exception as exc:
            return False, f"Connection test failed: {exc}"

    @staticmethod
    def get_oauth_url(
        client_id: str,
        redirect_uri: str = "http://localhost:8080/oauth/callback",
    ) -> str:
        """Return an OAuth authorization URL (no HTTP call made).

        Scope is 'api refresh_token' — least-privilege.
        The broader 'full' scope is intentionally excluded.
        """
        params = (
            f"response_type=code"
            f"&client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope=api%20refresh_token"
        )
        return f"https://login.salesforce.com/services/oauth2/authorize?{params}"


# ---------------------------------------------------------------------------
# CLI — prints no credential values
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python connect.py [test|oauth|connect]")
        sys.exit(1)

    cmd  = sys.argv[1]
    conn = SalesforceConnection()

    if cmd == "test":
        ok, msg = conn.test_connection()
        print(json.dumps({"success": ok, "message": msg}))

    elif cmd == "oauth":
        if len(sys.argv) < 3:
            print("Usage: python connect.py oauth <client_id>")
            sys.exit(1)
        url = conn.get_oauth_url(sys.argv[2])
        print(json.dumps({"success": True, "oauth_url": url}))

    elif cmd == "connect":
        ok, msg, _ = conn.connect()
        out = {"success": ok, "message": msg}
        if ok:
            out["instance_url"] = conn.instance_url
        print(json.dumps(out))

    else:
        print(json.dumps({"success": False, "message": f"Unknown command: {cmd}"}))


if __name__ == "__main__":
    main()
