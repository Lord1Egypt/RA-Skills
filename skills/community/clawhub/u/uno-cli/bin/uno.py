#!/usr/bin/env python3
"""Uno CLI — Agent Tool Gateway command line client.

Zero external dependencies (Python 3.8+ stdlib only).
Credentials stored at ~/.uno/credentials.json.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

__version__ = "0.1.0"

DEFAULT_BASE = "https://clawdtools.uno"
CRED_DIR = os.path.expanduser("~/.uno")
CRED_FILE = os.path.join(CRED_DIR, "credentials.json")


# ── HTTP Client ────────────────────────────────────────────────────


class APIError(Exception):
    def __init__(self, status, body):
        self.status = status
        self.body = body
        super().__init__(f"HTTP {status}: {body}")


class UnoAPI:
    """Thin HTTP wrapper around Uno REST API."""

    def __init__(self, api_key="", base_url=DEFAULT_BASE):
        self.api_key = api_key
        self.base = base_url.rstrip("/")

    def _headers(self):
        h = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def _request(self, method, path, data=None, params=None, timeout=60):
        url = f"{self.base}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(
                {k: v for k, v in params.items() if v is not None}
            )
        body = json.dumps(data).encode() if data is not None else None
        req = urllib.request.Request(url, data=body, headers=self._headers(), method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            raw = e.read().decode() if e.fp else ""
            try:
                err = json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                err = raw
            raise APIError(e.code, err)
        except urllib.error.URLError as e:
            reason = str(e.reason) if hasattr(e, "reason") else str(e)
            if "SSL" in reason or "EOF" in reason:
                raise APIError(0, f"SSL/TLS error connecting to {self.base}. Check network/proxy settings.")
            elif "Name or service not known" in reason or "nodename nor servname" in reason:
                raise APIError(0, f"DNS resolution failed for {self.base}. Check network connection.")
            else:
                raise APIError(0, f"Connection failed: {reason}. Server may be down or unreachable.")
        except OSError as e:
            raise APIError(0, f"Network error: {e}. Check connectivity to {self.base}.")

    def get(self, path, params=None):
        return self._request("GET", path, params=params)

    def post(self, path, data=None, timeout=60):
        return self._request("POST", path, data=data, timeout=timeout)

    def delete(self, path):
        return self._request("DELETE", path)


# ── Auth Manager ───────────────────────────────────────────────────


class AuthManager:
    """Manage credentials: device code login, direct key, multi-account."""

    def __init__(self, base_url=DEFAULT_BASE):
        self.base_url = base_url

    def _ensure_dir(self):
        os.makedirs(CRED_DIR, mode=0o700, exist_ok=True)

    def _read_creds(self):
        if not os.path.exists(CRED_FILE):
            return []
        try:
            with open(CRED_FILE) as f:
                data = json.load(f)
            if isinstance(data, dict):
                return [data]
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _write_creds(self, creds):
        self._ensure_dir()
        with open(CRED_FILE, "w") as f:
            json.dump(creds, f, indent=2, ensure_ascii=False)
        os.chmod(CRED_FILE, 0o600)

    def load_key(self):
        """Load API key: env var > active account > first account."""
        env_key = os.environ.get("UNO_API_KEY", "")
        if env_key:
            return env_key
        creds = self._read_creds()
        if not creds:
            return ""
        active = next((c for c in creds if c.get("active")), None)
        return (active or creds[0]).get("api_key", "")

    def save_account(self, api_key, user_name, user_email="", user_id=""):
        """Add or update account, set as active."""
        creds = self._read_creds()
        for c in creds:
            c.pop("active", None)

        identifier = user_email or user_name
        existing = next((c for c in creds if c.get("email") == identifier or c.get("name") == identifier), None)
        if existing:
            existing["api_key"] = api_key
            existing["name"] = user_name
            existing["email"] = user_email
            existing["user_id"] = user_id
            existing["active"] = True
        else:
            creds.append({
                "api_key": api_key,
                "name": user_name,
                "email": user_email,
                "user_id": user_id,
                "active": True,
            })
        self._write_creds(creds)

    def remove_account(self, name=None, all_=False):
        if all_:
            self._write_creds([])
            return True
        creds = self._read_creds()
        if name:
            creds = [c for c in creds if c.get("name") != name and c.get("email") != name]
        else:
            creds = [c for c in creds if not c.get("active")]
        self._write_creds(creds)
        return True

    def switch(self, name):
        creds = self._read_creds()
        found = False
        for c in creds:
            if c.get("name") == name or c.get("email") == name:
                c["active"] = True
                found = True
            else:
                c.pop("active", None)
        if not found:
            return None
        self._write_creds(creds)
        return name

    def list_accounts(self):
        return self._read_creds()

    def login_with_key(self, key):
        """Verify key via /v1/auth/me and save."""
        api = UnoAPI(api_key=key, base_url=self.base_url)
        try:
            resp = api.get("/v1/auth/me")
        except APIError as e:
            return {"error": f"API Key verification failed: {e.body}"}

        name = resp.get("name", "")
        email = resp.get("email", "")
        user_id = resp.get("id", "")
        if not email and not name:
            return {"error": "API Key invalid or user not found"}

        self.save_account(key, name, email, user_id)
        return {"success": True, "name": name, "email": email}

    def login_device_start(self):
        """Step 1: request device code. Returns JSON with verification URL.

        Non-blocking — agent can relay the URL to the user before polling.
        """
        api = UnoAPI(base_url=self.base_url)
        try:
            resp = api.post("/oauth/device/code", {"client_id": "uno-cli", "scope": "mcp:*"})
        except APIError as e:
            return {"error": f"Failed to get device code: {e.body}"}

        verification_uri = resp.get("verification_uri", "")
        user_code = resp.get("user_code", "")
        verification_uri_complete = f"{verification_uri}?code={user_code}" if verification_uri else ""

        return {
            "status": "pending",
            "device_code": resp.get("device_code", ""),
            "user_code": user_code,
            "verification_uri": verification_uri,
            "verification_uri_complete": verification_uri_complete,
            "expires_in": resp.get("expires_in", 600),
            "interval": resp.get("interval", 5),
            "message": (
                "Please have the user open the verification_uri_complete link "
                "in a browser to authorize, then run: uno login --poll <device_code>"
            ),
        }

    def login_device_poll(self, device_code, timeout=None):
        """Step 2: poll until device code is authorized or expired."""
        api = UnoAPI(base_url=self.base_url)
        deadline = time.time() + (timeout or 600)
        interval = 5

        while time.time() < deadline:
            try:
                result = api.post("/oauth/token", {
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "device_code": device_code,
                    "client_id": "uno-cli",
                })
            except APIError as e:
                detail = ""
                if isinstance(e.body, dict):
                    detail = e.body.get("detail", "")
                elif isinstance(e.body, str):
                    detail = e.body
                return {"error": detail or str(e)}

            error = result.get("error", "")
            if error == "authorization_pending":
                _eprint(".", end="", flush=True)
                time.sleep(interval)
                continue
            elif error == "expired_token":
                return {"error": "Device code expired. Please restart login."}
            elif error == "access_denied":
                return {"error": "Authorization denied."}
            elif error:
                return {"error": error}

            access_token = result.get("access_token", "")
            if not access_token:
                return {"error": "No access token in response"}

            # Verify and get user info
            verify_api = UnoAPI(api_key=access_token, base_url=self.base_url)
            try:
                me = verify_api.get("/v1/auth/me")
                name = me.get("name", "")
                email = me.get("email", "")
                user_id = me.get("id", "")
                self.save_account(access_token, name, email, user_id)
                return {
                    "success": True,
                    "name": name,
                    "email": email,
                    "api_key": access_token,
                }
            except APIError:
                self.save_account(access_token, "user", "", "")
                return {"success": True, "api_key": access_token}

        return {"error": "Authorization timeout"}

    def login_device_interactive(self):
        """One-shot flow: request code, show URL on stderr, poll.

        Kept for interactive terminal use where the human can see stderr.
        """
        start = self.login_device_start()
        if start.get("error"):
            return start

        uri = start["verification_uri_complete"]
        user_code = start["user_code"]
        expires_in = start["expires_in"]
        device_code = start["device_code"]

        _eprint(f"\n\033[1;36m🔐 Please open this link to authorize:\033[0m\n")
        _eprint(f"   \033[4m{uri}\033[0m\n")
        _eprint(f"   Code: \033[1m{user_code}\033[0m")
        _eprint(f"   (Valid for {expires_in // 60} minutes)\n")
        _eprint("⏳ Waiting for authorization...", end="", flush=True)

        result = self.login_device_poll(device_code, timeout=expires_in)
        if result.get("success"):
            _eprint(f"\r✅ Authorized! Welcome, {result.get('name', result.get('email', ''))}                    ")
        elif result.get("error"):
            _eprint(f"\r❌ {result['error']}                ")
        return result


def _eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# ── Output Helpers ─────────────────────────────────────────────────


_ERROR_HINTS = {
    "unauthorized": "Login required. Run: uno login",
    "invalid credentials": "Login required. Run: uno login",
    "invalid api key": "API key expired or invalid. Run: uno login",
    "not found": "Resource not found. Check the ID/slug.",
    "not_found": "Resource not found. Check the ID/slug.",
    "tool_not_found": "Tool not found. Try: uno search <keyword>",
    "insufficient_credits": "Out of credits. Visit the billing page.",
    "auth_required": "OAuth required. Open the auth_url in a browser.",
    "rate limit": "Rate limited. Please wait and retry.",
}


def _match_hint(error_str):
    lower = error_str.lower()
    for key, hint in _ERROR_HINTS.items():
        if key in lower:
            return hint
    return ""


def _format_api_error(status, body):
    if isinstance(body, dict):
        detail = body.get("detail", body.get("error", body.get("message", "")))
    elif isinstance(body, str):
        detail = body
    else:
        detail = str(body)

    # Pydantic validation errors come as list — extract human-readable messages
    if isinstance(detail, list):
        msgs = []
        for err in detail:
            if isinstance(err, dict):
                loc = " → ".join(str(x) for x in err.get("loc", []))
                msgs.append(f"{loc}: {err.get('msg', '')}")
            else:
                msgs.append(str(err))
        detail = "; ".join(msgs) if msgs else str(detail)

    result = {"error": str(detail), "status": status}
    hint = _match_hint(str(detail))
    if hint:
        result["hint"] = hint
    return result


def _ok(data):
    _out({"success": True, "data": data})


def _fail(msg, **extra):
    out = {"error": msg}
    hint = _match_hint(msg)
    if hint:
        out["hint"] = hint
    out.update(extra)
    _out(out)
    sys.exit(1)


def _out(obj):
    indent = None if getattr(_out, "compact", False) else 2
    print(json.dumps(obj, indent=indent, ensure_ascii=False, default=str))


def _get_api(args):
    """Build authenticated API client from args/env/creds."""
    auth = AuthManager(base_url=args.base_url)
    key = auth.load_key()
    if not key:
        _fail("Not logged in. Run: uno login")
    return UnoAPI(api_key=key, base_url=args.base_url)


def _get_public_api(args):
    """Build unauthenticated API client (for public endpoints)."""
    return UnoAPI(base_url=args.base_url)


# ── Commands ───────────────────────────────────────────────────────


def cmd_login(args):
    auth = AuthManager(base_url=args.base_url)

    if getattr(args, "key", None):
        result = auth.login_with_key(args.key)
        _out(result)
        sys.exit(0 if result.get("success") else 1)

    if getattr(args, "start", False):
        result = auth.login_device_start()
        _out(result)
        sys.exit(0 if not result.get("error") else 1)

    if getattr(args, "poll", None):
        result = auth.login_device_poll(args.poll)
        _out(result)
        sys.exit(0 if result.get("success") else 1)

    # Interactive mode
    result = auth.login_device_interactive()
    _out(result)
    sys.exit(0 if result.get("success") else 1)


def cmd_logout(args):
    auth = AuthManager(base_url=args.base_url)
    auth.remove_account(all_=getattr(args, "all", False))
    _ok({"logged_out": True})


def cmd_use(args):
    auth = AuthManager(base_url=args.base_url)
    name = getattr(args, "account", None)
    if not name:
        accounts = auth.list_accounts()
        _ok({"accounts": [
            {"name": a.get("name", ""), "email": a.get("email", ""), "active": a.get("active", False)}
            for a in accounts
        ]})
        return

    result = auth.switch(name)
    if result:
        _ok({"switched_to": result})
    else:
        _fail(f"Account not found: {name}")


def cmd_whoami(args):
    api = _get_api(args)
    try:
        me = api.get("/v1/auth/me")
        _ok(me)
    except APIError as e:
        _out(_format_api_error(e.status, e.body))
        sys.exit(1)


def cmd_search(args):
    api = _get_public_api(args)
    params = {"q": args.query, "limit": args.limit}
    if getattr(args, "mode", None):
        params["mode"] = args.mode
    if getattr(args, "category", None):
        params["category"] = args.category
    if getattr(args, "server", None):
        params["server"] = args.server

    try:
        result = api.get("/v1/tools", params=params)
        _ok(result)
    except APIError as e:
        _out(_format_api_error(e.status, e.body))
        sys.exit(1)


def cmd_tool(args):
    action = getattr(args, "action", None)
    if not action:
        _fail("Subcommand required. Usage: uno tool get <slug>")
    if action == "get":
        api = _get_public_api(args)
        slug = getattr(args, "slug", "")
        if not slug:
            _fail("Tool slug required. Usage: uno tool get <slug>")
        try:
            result = api.get(f"/v1/tools/{slug}")
            # Unwrap nested {"data": {...}, "error": null} from API
            if isinstance(result, dict) and "data" in result and "error" in result:
                result = result["data"]
            if result is None:
                _fail(f"Tool not found: {slug}")
            _ok(result)
        except APIError as e:
            _out(_format_api_error(e.status, e.body))
            sys.exit(1)
    else:
        _fail(f"Unknown tool action: {action}")


def cmd_call(args):
    api = _get_api(args)
    tool_slug = args.tool
    arguments = {}
    raw_args = getattr(args, "args", None)
    if raw_args:
        # Sanitize: strip null bytes
        raw_args = raw_args.replace("\x00", "")
        # Limit argument size (100KB)
        if len(raw_args) > 102400:
            _fail("Arguments too large (max 100KB)")
        try:
            arguments = json.loads(raw_args)
            if not isinstance(arguments, dict):
                _fail("--args must be a JSON object, e.g. '{\"key\": \"value\"}'")
        except json.JSONDecodeError as e:
            _fail(f"Invalid JSON in --args: {e}")

    timeout = getattr(args, "timeout", 60) or 60
    try:
        result = api.post("/v1/call", {"tool": tool_slug, "arguments": arguments}, timeout=timeout)
        if result.get("error"):
            out = {"success": False, "error": result["error"]}
            # Pass through all auth-related fields for agent decision-making
            for key in ("auth_url", "auth_type", "auth_provider",
                        "get_key_url", "fields", "message", "recharge_url"):
                if result.get(key):
                    out[key] = result[key]
            # Include meta (latency, credits) when available
            if result.get("meta"):
                out["meta"] = result["meta"]
            # Add contextual hint
            auth_type = result.get("auth_type", "")
            if result.get("auth_url"):
                out["hint"] = "OAuth required. Open auth_url in a browser to authorize."
            elif auth_type == "api_key":
                out["hint"] = "API key required. Show get_key_url to the user."
            elif result.get("recharge_url"):
                out["hint"] = "Insufficient credits. Show recharge_url to the user."
            _out(out)
            sys.exit(1)
        # Flatten: keep data + meta at top level for easy agent access
        flat = {"success": True}
        if isinstance(result, dict):
            if "data" in result:
                flat["data"] = result["data"]
            if "meta" in result:
                flat["meta"] = result["meta"]
            if not flat.get("data") and "data" not in result:
                flat["data"] = result
        else:
            flat["data"] = result
        _out(flat)
    except APIError as e:
        _out(_format_api_error(e.status, e.body))
        sys.exit(1)


def cmd_rate(args):
    api = _get_api(args)
    rating = float(args.rating)
    if rating < 0 or rating > 5:
        _fail("Rating must be between 0 and 5")
    try:
        result = api.post("/v1/rate", {
            "tool": args.tool,
            "rating": rating,
            "comment": getattr(args, "comment", ""),
        })
        _ok(result)
    except APIError as e:
        _out(_format_api_error(e.status, e.body))
        sys.exit(1)


def cmd_disconnect(args):
    api = _get_api(args)
    try:
        result = api.delete(f"/v1/auth/disconnect/{args.server}")
        # API may return {"success": false, "message": "..."} — don't wrap as success
        if isinstance(result, dict) and result.get("success") is False:
            _fail(result.get("message", "Disconnect failed"))
        _ok(result)
    except APIError as e:
        _out(_format_api_error(e.status, e.body))
        sys.exit(1)


def cmd_servers(args):
    api = _get_public_api(args)
    params = {"limit": args.limit}
    if getattr(args, "query", None):
        params["q"] = args.query
    if getattr(args, "category", None):
        params["category"] = args.category

    try:
        result = api.get("/v1/servers", params=params)
        _ok(result)
    except APIError as e:
        _out(_format_api_error(e.status, e.body))
        sys.exit(1)


def cmd_keys(args):
    api = _get_api(args)
    action = getattr(args, "action", None) or "list"

    try:
        if action == "list":
            result = api.get("/v1/auth/keys")
            _ok(result)
        elif action == "create":
            name = getattr(args, "name", "Default") or "Default"
            result = api.post("/v1/auth/keys", {"name": name})
            _ok(result)
        elif action == "delete":
            key_id = getattr(args, "key_id", "")
            if not key_id:
                _fail("Key ID required. Usage: uno keys delete <key_id>")
            result = api.delete(f"/v1/auth/keys/{key_id}")
            _ok(result)
        else:
            _fail(f"Unknown keys action: {action}")
    except APIError as e:
        _out(_format_api_error(e.status, e.body))
        sys.exit(1)


def cmd_health(args):
    api = _get_public_api(args)
    try:
        result = api.get("/health")
        _ok(result)
    except APIError as e:
        _out(_format_api_error(e.status, e.body))
        sys.exit(1)


# ── Argparse Setup ─────────────────────────────────────────────────


def build_parser():
    p = argparse.ArgumentParser(
        prog="uno",
        description="Uno — Agent Tool Gateway CLI",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("--compact", action="store_true", help="Output compact (single-line) JSON instead of formatted")
    p.add_argument(
        "--base-url",
        default=os.environ.get("UNO_API_URL", DEFAULT_BASE),
        help=f"API base URL (default: {DEFAULT_BASE}, env: UNO_API_URL)",
    )

    sub = p.add_subparsers(dest="command")

    # login
    login_p = sub.add_parser("login", help="Authenticate with Uno (via ClawdChat SSO)")
    login_p.add_argument("--start", action="store_true", help="Step 1: get device code (non-blocking, for agents)")
    login_p.add_argument("--poll", metavar="DEVICE_CODE", help="Step 2: poll for authorization")
    login_p.add_argument("--key", metavar="API_KEY", help="Login with API key directly")

    # logout
    logout_p = sub.add_parser("logout", help="Remove stored credentials")
    logout_p.add_argument("--all", action="store_true", help="Remove all accounts")

    # use
    use_p = sub.add_parser("use", help="List or switch accounts")
    use_p.add_argument("account", nargs="?", help="Account name or email to switch to")

    # whoami
    sub.add_parser("whoami", help="Show current user info")

    # search
    search_p = sub.add_parser("search", help="Search tools")
    search_p.add_argument("query", help="Search query")
    search_p.add_argument("--limit", type=int, default=10, help="Max results (default: 10, max: 50)")
    search_p.add_argument("--mode", choices=["keyword", "semantic", "hybrid"], help="Search mode (default: hybrid)")
    search_p.add_argument("--category", help="Filter by category")
    search_p.add_argument("--server", help="Filter by server slug")

    # tool
    tool_p = sub.add_parser("tool", help="Get tool details")
    tool_sub = tool_p.add_subparsers(dest="action")
    tool_get = tool_sub.add_parser("get", help="Get tool detail by slug")
    tool_get.add_argument("slug", help="Tool slug (e.g. amap-maps.maps_weather)")

    # call
    call_p = sub.add_parser("call", help="Call a tool",
        epilog='Examples:\n'
               '  uno call time.get_current_time --args \'{"timezone":"Asia/Shanghai"}\'\n'
               '  uno call weather-cn.weatherArea --args \'{"area":"北京"}\'\n'
               '  uno call twelve-data.quote --args \'{"symbol":"AAPL"}\' --timeout 30',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    call_p.add_argument("tool", help="Tool slug (e.g. weather-cn.weatherArea)")
    call_p.add_argument("--args", help='JSON arguments (e.g. \'{"city":"Beijing"}\')')
    call_p.add_argument("--timeout", type=int, default=60, help="Request timeout in seconds (default: 60)")

    # rate
    rate_p = sub.add_parser("rate", help="Rate a tool (0-5)")
    rate_p.add_argument("tool", help="Tool slug")
    rate_p.add_argument("rating", type=float, help="Rating 0.0-5.0")
    rate_p.add_argument("--comment", default="", help="Optional comment")

    # servers
    servers_p = sub.add_parser("servers", help="List servers")
    servers_p.add_argument("--query", "-q", help="Search query")
    servers_p.add_argument("--category", help="Filter by category")
    servers_p.add_argument("--limit", type=int, default=50, help="Max results (default: 50)")

    # keys
    keys_p = sub.add_parser("keys", help="Manage API keys")
    keys_sub = keys_p.add_subparsers(dest="action")
    keys_sub.add_parser("list", help="List active API keys")
    keys_create = keys_sub.add_parser("create", help="Create a new API key")
    keys_create.add_argument("--name", default="Default", help="Key name (default: Default)")
    keys_del = keys_sub.add_parser("delete", help="Delete an API key")
    keys_del.add_argument("key_id", help="API key ID to delete")

    # health
    sub.add_parser("health", help="Check server health")

    # disconnect
    disc_p = sub.add_parser("disconnect", help="Revoke third-party OAuth/API-key authorization")
    disc_p.add_argument("server", help="Server slug to disconnect (e.g. github, canva)")

    return p


COMMAND_MAP = {
    "login": cmd_login,
    "logout": cmd_logout,
    "use": cmd_use,
    "whoami": cmd_whoami,
    "search": cmd_search,
    "tool": cmd_tool,
    "call": cmd_call,
    "rate": cmd_rate,
    "servers": cmd_servers,
    "keys": cmd_keys,
    "health": cmd_health,
    "disconnect": cmd_disconnect,
}


def _preprocess_argv(argv):
    """Fix two argparse limitations before parsing:

    1. Top-level flags (--compact, --base-url) anywhere: argparse only recognises
       them *before* the subcommand, so hoist them to the front.
    2. --poll <value-starting-with-dash>: argparse treats leading-dash values as
       new flags; rewrite `--poll -xxx` -> `--poll=-xxx` to avoid that.
    """
    # Flags that take no value — hoist as-is
    bool_flags = {"--compact"}
    # Flags that take one value — hoist flag + value together
    value_flags = {"--base-url"}

    result = []
    hoisted = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in bool_flags:
            hoisted.append(arg)
            i += 1
        elif arg in value_flags and i + 1 < len(argv):
            hoisted.extend([arg, argv[i + 1]])
            i += 2
        elif arg == "--poll" and i + 1 < len(argv) and argv[i + 1].startswith("-"):
            result.append(f"--poll={argv[i + 1]}")
            i += 2
        else:
            result.append(arg)
            i += 1
    return hoisted + result


def main():
    parser = build_parser()
    args = parser.parse_args(_preprocess_argv(sys.argv[1:]))

    if args.compact:
        _out.compact = True

    if not args.command:
        parser.print_help(sys.stderr)
        sys.exit(1)

    handler = COMMAND_MAP.get(args.command)
    if not handler:
        parser.print_help(sys.stderr)
        sys.exit(1)

    try:
        handler(args)
    except APIError as e:
        _out(_format_api_error(e.status, e.body))
        sys.exit(1)
    except KeyboardInterrupt:
        _eprint("\nAborted.")
        sys.exit(130)
    except Exception as e:
        _fail(str(e))


if __name__ == "__main__":
    main()
