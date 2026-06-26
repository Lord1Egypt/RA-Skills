"""OAuth 2.0 authorization flow for QuickBooks Online."""

import base64
import secrets
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional
from urllib.parse import urlencode, urlparse, parse_qs

import httpx

AUTHORIZATION_URL = "https://appcenter.intuit.com/connect/oauth2"
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
REVOKE_URL = "https://developer.api.intuit.com/v2/oauth2/tokens/revoke"
CALLBACK_PORT = 8844
REDIRECT_URI = f"https://officially-nonfatalistic-baylee.ngrok-free.dev/callback"
SCOPES = "com.intuit.quickbooks.accounting"


class OAuthError(Exception):
    """Error during OAuth flow."""
    pass


class _CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler that captures the OAuth redirect callback."""

    auth_code: Optional[str] = None
    realm_id: Optional[str] = None
    state: Optional[str] = None
    error: Optional[str] = None

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return

        params = parse_qs(parsed.query)
        _CallbackHandler.auth_code = params.get("code", [None])[0]
        _CallbackHandler.realm_id = params.get("realmId", [None])[0]
        _CallbackHandler.state = params.get("state", [None])[0]
        _CallbackHandler.error = params.get("error", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(
            b"<html><body>"
            b"<h2>Authorization complete!</h2>"
            b"<p>You can close this window and return to your terminal.</p>"
            b"</body></html>"
        )

    def log_message(self, format, *args):
        """Suppress HTTP server access logs."""
        pass


def generate_auth_url(client_id: str) -> tuple[str, str]:
    """Generate authorization URL and state token.

    Returns:
        Tuple of (authorization_url, state_token)
    """
    state = secrets.token_hex(16)
    params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "state": state,
    }
    url = f"{AUTHORIZATION_URL}?{urlencode(params)}"
    return url, state


def parse_callback_url(callback_url: str) -> dict:
    """Parse a callback URL pasted by the user (headless/SSH flow).

    Returns:
        Dict with 'code' and 'realm_id' keys.
    """
    parsed = urlparse(callback_url)
    params = parse_qs(parsed.query)

    code = params.get("code", [None])[0]
    realm_id = params.get("realmId", [None])[0]
    error = params.get("error", [None])[0]

    if error:
        raise OAuthError(f"Authorization denied: {error}")
    if not code:
        raise OAuthError(
            "No authorization code found in URL. "
            "Make sure you copied the full redirect URL."
        )

    return {"code": code, "realm_id": realm_id}


def wait_for_callback(expected_state: str, timeout: int = 120) -> dict:
    """Start local server and wait for OAuth callback.

    Returns:
        Dict with 'code' and 'realm_id' keys.
    """
    # Reset class-level state
    _CallbackHandler.auth_code = None
    _CallbackHandler.realm_id = None
    _CallbackHandler.state = None
    _CallbackHandler.error = None

    server = HTTPServer(("localhost", CALLBACK_PORT), _CallbackHandler)
    server.timeout = timeout
    server.handle_request()
    server.server_close()

    if _CallbackHandler.error:
        raise OAuthError(f"Authorization denied: {_CallbackHandler.error}")
    if _CallbackHandler.state != expected_state:
        raise OAuthError("State token mismatch — possible CSRF attack.")
    if not _CallbackHandler.auth_code:
        raise OAuthError("No authorization code received (timeout?).")

    return {
        "code": _CallbackHandler.auth_code,
        "realm_id": _CallbackHandler.realm_id,
    }


def _basic_auth_header(client_id: str, client_secret: str) -> str:
    """Build HTTP Basic Auth header value."""
    credentials = base64.b64encode(
        f"{client_id}:{client_secret}".encode()
    ).decode()
    return f"Basic {credentials}"


def exchange_code_for_tokens(
    client_id: str,
    client_secret: str,
    auth_code: str,
) -> dict:
    """Exchange authorization code for access and refresh tokens.

    Returns:
        Token response dict with access_token, refresh_token, expires_in, etc.
    """
    response = httpx.post(
        TOKEN_URL,
        headers={
            "Authorization": _basic_auth_header(client_id, client_secret),
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
        },
        timeout=30.0,
    )
    if response.status_code != 200:
        raise OAuthError(
            f"Token exchange failed ({response.status_code}): {response.text}"
        )
    return response.json()


def refresh_access_token(
    client_id: str,
    client_secret: str,
    refresh_token: str,
) -> dict:
    """Refresh an expired access token.

    Returns:
        New token response dict (includes new refresh_token — must be saved).
    """
    response = httpx.post(
        TOKEN_URL,
        headers={
            "Authorization": _basic_auth_header(client_id, client_secret),
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=30.0,
    )
    if response.status_code != 200:
        raise OAuthError(
            f"Token refresh failed ({response.status_code}): {response.text}"
        )
    return response.json()


def revoke_token(
    client_id: str,
    client_secret: str,
    token: str,
) -> None:
    """Revoke an access or refresh token."""
    response = httpx.post(
        REVOKE_URL,
        headers={
            "Authorization": _basic_auth_header(client_id, client_secret),
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={"token": token},
        timeout=30.0,
    )
    # Intuit returns 200 even if token is already revoked
    if response.status_code not in (200, 204):
        raise OAuthError(
            f"Token revocation failed ({response.status_code}): {response.text}"
        )
