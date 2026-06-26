"""Token persistence and auto-refresh logic."""

import json
import os
import time
from pathlib import Path
from typing import Optional

from qb.auth.oauth import refresh_access_token, OAuthError

TOKEN_FILE = "tokens.json"

# Refresh 5 minutes before expiry to avoid race conditions
REFRESH_BUFFER_SECONDS = 300


class AuthNotConfiguredError(Exception):
    """Raised when no tokens are stored."""
    pass


class TokenManager:
    """Manages OAuth token storage, loading, and auto-refresh."""

    def __init__(self, config_dir: Optional[Path] = None):
        from qb.config import get_config_dir

        self.config_dir = get_config_dir(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.token_path = self.config_dir / TOKEN_FILE
        self._tokens: Optional[dict] = None

    def save_tokens(
        self,
        token_response: dict,
        realm_id: str,
        environment: str,
    ) -> None:
        """Save tokens from OAuth response to disk."""
        data = {
            "access_token": token_response["access_token"],
            "refresh_token": token_response["refresh_token"],
            "realm_id": realm_id,
            "token_type": token_response.get("token_type", "bearer"),
            "expires_at": int(time.time()) + token_response.get("expires_in", 3600),
            "refresh_token_expires_at": (
                int(time.time())
                + token_response.get("x_refresh_token_expires_in", 8726400)
            ),
            "environment": environment,
        }
        self.token_path.write_text(json.dumps(data, indent=2))
        self.token_path.chmod(0o600)
        self._tokens = data

    def load_tokens(self) -> dict:
        """Load tokens from disk. Raises if not found."""
        if self._tokens:
            return self._tokens
        if not self.token_path.exists():
            raise AuthNotConfiguredError(
                "Not authenticated. Run 'qb auth login' first."
            )
        self._tokens = json.loads(self.token_path.read_text())
        return self._tokens

    def get_access_token(self, client_id: str, client_secret: str) -> str:
        """Get a valid access token, refreshing automatically if needed."""
        tokens = self.load_tokens()

        if time.time() >= tokens["expires_at"] - REFRESH_BUFFER_SECONDS:
            # Token expired or about to expire — refresh
            try:
                new_tokens = refresh_access_token(
                    client_id, client_secret, tokens["refresh_token"]
                )
                self.save_tokens(
                    new_tokens, tokens["realm_id"], tokens["environment"]
                )
                tokens = self.load_tokens()
            except OAuthError as e:
                raise AuthNotConfiguredError(
                    f"Token refresh failed: {e}. Run 'qb auth login' to re-authenticate."
                )

        return tokens["access_token"]

    @property
    def realm_id(self) -> str:
        """Get the stored realm ID (QuickBooks company ID)."""
        return self.load_tokens()["realm_id"]

    @property
    def environment(self) -> str:
        """Get the stored environment (sandbox or production)."""
        return self.load_tokens()["environment"]

    @property
    def is_authenticated(self) -> bool:
        """Check if valid tokens exist."""
        try:
            tokens = self.load_tokens()
            return bool(tokens.get("refresh_token"))
        except AuthNotConfiguredError:
            return False

    @property
    def token_status(self) -> dict:
        """Get detailed token status for display."""
        try:
            tokens = self.load_tokens()
            now = time.time()
            access_expires = tokens.get("expires_at", 0)
            refresh_expires = tokens.get("refresh_token_expires_at", 0)
            return {
                "authenticated": True,
                "realm_id": tokens.get("realm_id", "unknown"),
                "environment": tokens.get("environment", "unknown"),
                "access_token_valid": now < access_expires,
                "access_token_expires_in": max(0, int(access_expires - now)),
                "refresh_token_expires_in": max(0, int(refresh_expires - now)),
            }
        except AuthNotConfiguredError:
            return {"authenticated": False}

    def clear_cache(self) -> None:
        """Clear in-memory token cache, forcing reload from disk on next access."""
        self._tokens = None

    def clear(self) -> None:
        """Delete stored tokens from disk and memory."""
        if self.token_path.exists():
            self.token_path.unlink()
        self._tokens = None
