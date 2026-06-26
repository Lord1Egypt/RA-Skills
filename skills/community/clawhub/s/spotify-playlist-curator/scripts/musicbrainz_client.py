#!/usr/bin/env python3
"""MusicBrainz client for artist genre lookups.

Free, public API — no API key required. Only rule: include a User-Agent
header and respect the 1 request/second rate limit.

Results are cached to disk to avoid redundant lookups across sessions.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests

MB_BASE = "https://musicbrainz.org/ws/2"
USER_AGENT = "SpotifyPlaylistCurator/1.0 (openclaw-skill)"
CACHE_DIR = Path(__file__).resolve().parent.parent / ".mb_cache"
RATE_LIMIT_SECONDS = 1.1  # slightly over 1s to stay safe


class MusicBrainzClient:
    """Lightweight MusicBrainz client for artist → genres lookups."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = USER_AGENT
        self._session.headers["Accept"] = "application/json"
        self._last_request_time: float = 0.0
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _rate_limit(self) -> None:
        elapsed = time.time() - self._last_request_time
        if elapsed < RATE_LIMIT_SECONDS:
            time.sleep(RATE_LIMIT_SECONDS - elapsed)
        self._last_request_time = time.time()

    def _cache_path(self, artist_name: str) -> Path:
        safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in artist_name.lower())
        return CACHE_DIR / f"{safe}.json"

    def _read_cache(self, artist_name: str) -> list[str] | None:
        path = self._cache_path(artist_name)
        if path.exists():
            try:
                data = json.loads(path.read_text())
                # Cache entries older than 30 days are stale
                if time.time() - data.get("ts", 0) < 30 * 86400:
                    return data.get("genres", [])
            except (json.JSONDecodeError, KeyError):
                pass
        return None

    def _write_cache(self, artist_name: str, genres: list[str]) -> None:
        path = self._cache_path(artist_name)
        path.write_text(json.dumps({"genres": genres, "ts": time.time()}, indent=2))

    def get_artist_genres(self, artist_name: str, top_n: int = 5) -> list[str]:
        """Look up genres for an artist by name. Returns top N genres sorted
        by community vote count, or an empty list if not found.

        Results are cached to disk for 30 days.
        """
        cached = self._read_cache(artist_name)
        if cached is not None:
            return cached[:top_n]

        try:
            # Step 1: Search for artist MBID
            self._rate_limit()
            resp = self._session.get(
                f"{MB_BASE}/artist",
                params={"query": f'artist:"{artist_name}"', "fmt": "json", "limit": "1"},
                timeout=10,
            )
            resp.raise_for_status()
            artists = resp.json().get("artists", [])
            if not artists or artists[0].get("score", 0) < 80:
                self._write_cache(artist_name, [])
                return []

            mbid = artists[0]["id"]

            # Step 2: Lookup genres by MBID
            self._rate_limit()
            resp = self._session.get(
                f"{MB_BASE}/artist/{mbid}",
                params={"inc": "genres", "fmt": "json"},
                timeout=10,
            )
            resp.raise_for_status()
            raw_genres = resp.json().get("genres", [])

            # Sort by count descending, take top N
            sorted_genres = sorted(raw_genres, key=lambda g: g.get("count", 0), reverse=True)
            genres = [g["name"].lower() for g in sorted_genres[:top_n]]

            self._write_cache(artist_name, genres)
            return genres

        except Exception:
            # MusicBrainz unavailable — return empty, don't cache failures
            return []

    def get_genres_batch(self, artist_names: list[str], top_n: int = 5) -> dict[str, list[str]]:
        """Look up genres for multiple artists. Respects rate limiting.

        Returns dict mapping artist name → list of genre strings.
        Cached results are returned instantly (no rate limit hit).
        """
        result: dict[str, list[str]] = {}
        for name in artist_names:
            result[name] = self.get_artist_genres(name, top_n=top_n)
        return result
