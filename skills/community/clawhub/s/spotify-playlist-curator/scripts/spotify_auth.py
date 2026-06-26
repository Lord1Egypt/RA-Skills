#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path

from spotipy.oauth2 import SpotifyOAuth

from spotify_client import DEFAULT_REDIRECT_URI, SCOPES, resolve_client_credentials, resolve_tokens_path


def save_tokens(token_info: dict, out_path: Path) -> Path:
    data = {
        "access_token": token_info.get("access_token"),
        "refresh_token": token_info.get("refresh_token"),
        "scope": token_info.get("scope"),
        "expires_at": token_info.get("expires_at"),
        "token_type": token_info.get("token_type"),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2))
    return out_path


def main() -> None:
    try:
        client_id, client_secret = resolve_client_credentials()
    except RuntimeError as exc:
        print(f"Error: {exc}", file=__import__("sys").stderr)
        raise SystemExit(1)

    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI", DEFAULT_REDIRECT_URI)
    tokens_path = resolve_tokens_path()

    stale_cache = Path(".cache")
    if stale_cache.exists() and stale_cache.is_file():
        stale_cache.unlink()

    oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=" ".join(SCOPES),
        open_browser=True,
        cache_path=None,
        show_dialog=True,
    )

    print("Starting Spotify OAuth flow...")
    print(f"  Redirect URI: {redirect_uri}")
    print()
    print("A browser window should open for Spotify login.")
    print("If it doesn't, copy the URL from the terminal into your browser.")
    print()

    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            token_info = oauth.get_access_token(as_dict=True, check_cache=False)
    except Exception as exc:
        error_msg = str(exc).lower()
        print("\nAuthentication failed.", file=__import__("sys").stderr)
        if "redirect" in error_msg or "mismatch" in error_msg:
            print(
                f"  The redirect URI ({redirect_uri}) may not match your Spotify app settings.",
                file=__import__("sys").stderr,
            )
            print(
                "  Check your app at https://developer.spotify.com/dashboard",
                file=__import__("sys").stderr,
            )
        elif "invalid_client" in error_msg:
            print(
                "  Your client ID or client secret is invalid.\n"
                "  This usually means:\n"
                "  1. The .env file still has placeholder values (your_client_id_here)\n"
                "  2. The credentials were copied incorrectly (extra spaces, missing characters)\n"
                "  3. The Spotify app was deleted from the developer dashboard\n\n"
                "  To fix: open the .env file in the skill root, verify your credentials\n"
                "  match what's shown at https://developer.spotify.com/dashboard, and re-run.",
                file=__import__("sys").stderr,
            )
        else:
            print(f"  {exc}", file=__import__("sys").stderr)
        raise SystemExit(1)

    if not token_info or "access_token" not in token_info:
        print(
            "Authentication failed: no access token was returned.",
            file=__import__("sys").stderr,
        )
        print(
            "This usually means the login was cancelled or consent was denied.",
            file=__import__("sys").stderr,
        )
        raise SystemExit(1)

    out_path = save_tokens(token_info, tokens_path)
    print("Authentication successful. Tokens saved to:")
    print(f"  {out_path}")
    print()
    print("You're all set! Try asking the agent:")
    print('  "Make me a playlist based on my top tracks from the past month"')
    print('  "Make a late night driving playlist"')
    print('  "Make me an hour-long playlist inspired by Karma Police and No Surprises')
    print('   by Radiohead and American Football\'s self-titled album"')


if __name__ == "__main__":
    main()
