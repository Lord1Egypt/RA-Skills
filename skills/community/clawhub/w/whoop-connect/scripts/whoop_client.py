#!/usr/bin/env python3
"""Full WHOOP API v2 client with OAuth, auto-refresh, pagination, and local storage."""

import json
import os
import sys
import time
import threading
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs

import requests

from db import get_db, upsert_recovery, upsert_sleep, upsert_workout, upsert_cycle, upsert_profile, upsert_body, get_daily_api_calls, increment_api_calls
from formatters import format_recovery, format_sleep, format_workout, format_cycle, format_profile, format_trends

BASE_URL = "https://api.prod.whoop.com/developer"
AUTH_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
REDIRECT_URI = "http://localhost:3000/callback"

TOKEN_DIR = os.path.expanduser("~/.whoop")
TOKEN_PATH = os.path.join(TOKEN_DIR, "token.json")

ALL_SCOPES = "offline read:profile read:body_measurement read:cycles read:recovery read:sleep read:workout"


class DailyLimitExceeded(Exception):
    """Raised when daily API call limit is reached."""
    pass


class WhoopClient:
    def __init__(self):
        self.client_id = os.environ.get("WHOOP_CLIENT_ID")
        self.client_secret = os.environ.get("WHOOP_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            print("Error: WHOOP_CLIENT_ID and WHOOP_CLIENT_SECRET must be set.")
            sys.exit(1)
        self.session = requests.Session()
        self._load_token()
        self._daily_limit = self._load_daily_limit()

    def _load_daily_limit(self):
        config_path = os.path.join(TOKEN_DIR, "config.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                return json.load(f).get("daily_api_limit", 10000)
        return 10000

    def _check_api_limit(self):
        """Check if daily API limit has been reached. Raises DailyLimitExceeded."""
        conn = get_db()
        count = get_daily_api_calls(conn)
        conn.close()
        if count >= self._daily_limit:
            raise DailyLimitExceeded(
                f"Daily API limit reached ({count}/{self._daily_limit}). "
                f"Resets at UTC midnight."
            )

    def _track_api_call(self):
        """Increment the daily API call counter."""
        conn = get_db()
        new_total = increment_api_calls(conn)
        conn.close()
        return new_total

    def get_api_usage(self):
        """Return current daily API usage stats."""
        conn = get_db()
        count = get_daily_api_calls(conn)
        conn.close()
        return {"used": count, "limit": self._daily_limit, "remaining": self._daily_limit - count}

    def _load_token(self):
        self.token = None
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH) as f:
                self.token = json.load(f)

    def _save_token(self, token_data):
        os.makedirs(TOKEN_DIR, exist_ok=True)
        self.token = {
            "access_token": token_data["access_token"],
            "refresh_token": token_data.get("refresh_token"),
            "expires_at": time.time() + token_data.get("expires_in", 3600),
        }
        with open(TOKEN_PATH, "w") as f:
            json.dump(self.token, f, indent=2)
        os.chmod(TOKEN_PATH, 0o600)

    def _is_expired(self):
        if not self.token:
            return True
        return time.time() >= self.token.get("expires_at", 0) - 60

    def _refresh(self):
        if not self.token or not self.token.get("refresh_token"):
            print("Error: No refresh token. Run 'auth' first.")
            sys.exit(1)
        resp = self.session.post(TOKEN_URL, data={
            "grant_type": "refresh_token",
            "refresh_token": self.token["refresh_token"],
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        })
        resp.raise_for_status()
        self._save_token(resp.json())

    def _request(self, method, path, **kwargs):
        self._check_api_limit()
        if self._is_expired():
            self._refresh()
        headers = {"Authorization": f"Bearer {self.token['access_token']}"}
        resp = self.session.request(method, f"{BASE_URL}{path}", headers=headers, **kwargs)
        self._track_api_call()
        if resp.status_code == 401:
            self._refresh()
            headers = {"Authorization": f"Bearer {self.token['access_token']}"}
            resp = self.session.request(method, f"{BASE_URL}{path}", headers=headers, **kwargs)
            self._track_api_call()
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 5))
            time.sleep(retry_after)
            resp = self.session.request(method, f"{BASE_URL}{path}", headers=headers, **kwargs)
            self._track_api_call()
        resp.raise_for_status()
        return resp.json()

    def _get_collection(self, path, start=None, end=None, limit=25):
        """Fetch all pages from a paginated endpoint."""
        params = {"limit": limit}
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        all_records = []
        while True:
            data = self._request("GET", path, params=params)
            records = data.get("records", [])
            all_records.extend(records)
            next_token = data.get("next_token")
            if not next_token:
                break
            params["nextToken"] = next_token
        return all_records

    # --- Auth ---

    def auth(self):
        """Run OAuth authorization code flow with local callback server."""
        import secrets as _secrets
        state = _secrets.token_urlsafe(32)
        auth_params = urlencode({
            "client_id": self.client_id,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": ALL_SCOPES,
            "state": state,
        })
        auth_url = f"{AUTH_URL}?{auth_params}"
        print(f"Open this URL in your browser:\n\n{auth_url}\n")

        code_holder = {}

        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                query = parse_qs(urlparse(self.path).query)
                if "code" in query:
                    code_holder["code"] = query["code"][0]
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Authorization successful! You can close this tab.")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Missing authorization code.")

            def log_message(self, format, *args):
                pass

        server = HTTPServer(("localhost", 3000), CallbackHandler)
        print("Waiting for authorization callback...")
        server.handle_request()
        server.server_close()

        if "code" not in code_holder:
            print("Error: Did not receive authorization code.")
            sys.exit(1)

        resp = self.session.post(TOKEN_URL, data={
            "grant_type": "authorization_code",
            "code": code_holder["code"],
            "redirect_uri": REDIRECT_URI,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        })
        resp.raise_for_status()
        self._save_token(resp.json())
        print("✓ Authorization successful. Token saved.")

    # --- Data fetchers ---

    def get_recovery(self, days=1):
        start = (datetime.now(tz=timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        records = self._get_collection("/v2/recovery", start=start)
        conn = get_db()
        for r in records:
            upsert_recovery(conn, r)
        conn.close()
        return records

    def get_recovery_for_cycle(self, cycle_id):
        data = self._request("GET", f"/v2/cycle/{cycle_id}/recovery")
        conn = get_db()
        upsert_recovery(conn, data)
        conn.close()
        return data

    def get_sleep(self, days=1):
        start = (datetime.now(tz=timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        records = self._get_collection("/v2/activity/sleep", start=start)
        conn = get_db()
        for r in records:
            upsert_sleep(conn, r)
        conn.close()
        return records

    def get_sleep_by_id(self, sleep_id):
        data = self._request("GET", f"/v2/activity/sleep/{sleep_id}")
        conn = get_db()
        upsert_sleep(conn, data)
        conn.close()
        return data

    def get_workout(self, days=1):
        start = (datetime.now(tz=timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        records = self._get_collection("/v2/activity/workout", start=start)
        conn = get_db()
        for r in records:
            upsert_workout(conn, r)
        conn.close()
        return records

    def get_workout_by_id(self, workout_id):
        data = self._request("GET", f"/v2/activity/workout/{workout_id}")
        conn = get_db()
        upsert_workout(conn, data)
        conn.close()
        return data

    def get_cycle(self, days=1):
        start = (datetime.now(tz=timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        records = self._get_collection("/v2/cycle", start=start)
        conn = get_db()
        for r in records:
            upsert_cycle(conn, r)
        conn.close()
        return records

    def get_profile(self):
        data = self._request("GET", "/v2/user/profile/basic")
        conn = get_db()
        upsert_profile(conn, data)
        conn.close()
        return data

    def get_body(self):
        data = self._request("GET", "/v2/user/measurement/body")
        conn = get_db()
        upsert_body(conn, data)
        conn.close()
        return data

    def get_trends(self, days=7):
        from db import query_trends
        conn = get_db()
        metrics = ["recovery_score", "hrv", "resting_hr", "spo2", "skin_temp",
                    "strain", "sleep_duration", "sleep_efficiency"]
        results = {}
        for m in metrics:
            results[m] = query_trends(conn, m, days)
        conn.close()
        return results


def main():
    if len(sys.argv) < 2:
        print("Usage: whoop_client.py <command> [options]")
        print("Commands: auth, recovery, sleep, workout, cycle, profile, body, trends")
        print("Options: --days N, --json")
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    days = 1
    as_json = "--json" in args
    for i, a in enumerate(args):
        if a == "--days" and i + 1 < len(args):
            days = int(args[i + 1])

    client = WhoopClient()

    if cmd == "auth":
        client.auth()
        return

    if cmd == "profile":
        data = client.get_profile()
        if as_json:
            print(json.dumps(data, indent=2))
        else:
            print(format_profile(data))

    elif cmd == "body":
        data = client.get_body()
        if as_json:
            print(json.dumps(data, indent=2))
        else:
            body = data
            print(f"Height: {body.get('height_meter', 0):.2f} m")
            print(f"Weight: {body.get('weight_kilogram', 0):.1f} kg")
            print(f"Max HR: {body.get('max_heart_rate', 'N/A')} bpm")

    elif cmd == "recovery":
        records = client.get_recovery(days)
        if as_json:
            print(json.dumps(records, indent=2))
        else:
            for r in records:
                print(format_recovery(r))
                print()

    elif cmd == "sleep":
        records = client.get_sleep(days)
        if as_json:
            print(json.dumps(records, indent=2))
        else:
            for r in records:
                print(format_sleep(r))
                print()

    elif cmd == "workout":
        records = client.get_workout(days)
        if as_json:
            print(json.dumps(records, indent=2))
        else:
            for r in records:
                print(format_workout(r))
                print()

    elif cmd == "cycle":
        records = client.get_cycle(days)
        if as_json:
            print(json.dumps(records, indent=2))
        else:
            for r in records:
                print(format_cycle(r))
                print()

    elif cmd == "trends":
        results = client.get_trends(days)
        if as_json:
            print(json.dumps(results, indent=2))
        else:
            print(format_trends(results, days))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
