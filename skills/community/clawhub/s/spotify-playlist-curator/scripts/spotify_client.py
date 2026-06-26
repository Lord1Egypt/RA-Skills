#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

import re

API_BASE = "https://api.spotify.com/v1"
_SPOTIFY_URI_RE = re.compile(r"^spotify:track:[A-Za-z0-9]{22}$")
DEFAULT_REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = [
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-public",
    "playlist-modify-private",
    "user-top-read",
    "user-read-recently-played",
]


def _candidate_paths() -> list[Path]:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    cwd = Path.cwd()
    return [
        skill_dir / ".env",
        script_dir / ".env",
        cwd / ".env",
        cwd / "secrets" / "spotify.env",
    ]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def resolve_client_credentials() -> tuple[str, str]:
    env_path = os.environ.get("SPOTIFY_ENV_PATH")
    if env_path:
        load_env_file(Path(env_path).expanduser())
    else:
        for path in _candidate_paths():
            load_env_file(path)

    client_id = os.environ.get("SPOTIFY_CLIENT_ID") or os.environ.get("SPOTIPY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET") or os.environ.get("SPOTIPY_CLIENT_SECRET")

    placeholders = {"your_client_id_here", "your_client_secret_here"}
    if client_id in placeholders or client_secret in placeholders:
        raise RuntimeError(
            "Spotify credentials in .env are still set to placeholder values.\n\n"
            "Replace them with real credentials from https://developer.spotify.com/dashboard\n"
            "Then re-run the auth script."
        )

    if not client_id and not client_secret:
        searched = [str(p) for p in _candidate_paths()]
        raise RuntimeError(
            "Spotify client credentials not found.\n\n"
            "Create a .env file in the skill root with:\n"
            "  SPOTIPY_CLIENT_ID=your_client_id\n"
            "  SPOTIPY_CLIENT_SECRET=your_client_secret\n\n"
            "You can get these from https://developer.spotify.com/dashboard\n\n"
            "Searched for .env in:\n" + "\n".join(f"  - {p}" for p in searched)
        )
    if not client_id:
        raise RuntimeError(
            "SPOTIPY_CLIENT_ID (or SPOTIFY_CLIENT_ID) is missing from your .env file.\n"
            "Add it to the .env file in the skill root."
        )
    if not client_secret:
        raise RuntimeError(
            "SPOTIPY_CLIENT_SECRET (or SPOTIFY_CLIENT_SECRET) is missing from your .env file.\n"
            "Add it to the .env file in the skill root."
        )
    return client_id, client_secret


def resolve_tokens_path() -> Path:
    explicit = os.environ.get("SPOTIFY_TOKENS_PATH")
    if explicit:
        return Path(explicit).expanduser()
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    cwd = Path.cwd()
    candidates = [
        skill_dir / "spotify_tokens.json",
        script_dir / "spotify_tokens.json",
        cwd / "spotify_tokens.json",
        cwd / "secrets" / "spotify_tokens.json",
    ]
    for path in candidates:
        if path.exists():
            return path
    return skill_dir / "spotify_tokens.json"


@dataclass
class SpotifyTokens:
    access_token: str
    refresh_token: str
    scope: str
    expires_at: int
    token_type: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpotifyTokens":
        try:
            return cls(
                access_token=data["access_token"],
                refresh_token=data["refresh_token"],
                scope=data.get("scope", ""),
                expires_at=int(data.get("expires_at", 0)),
                token_type=data.get("token_type", "Bearer"),
            )
        except KeyError as exc:
            raise RuntimeError(
                f"Token file is missing the required field {exc}.\n"
                "The token file may be corrupted or from an older version.\n"
                "Re-authenticate from the skill root: cd /path/to/spotify-playlist-curator && .venv/bin/python scripts/spotify_auth.py"
            ) from exc


def _normalize_name(name: str) -> str:
    """Lowercase and strip diacritics for accent-insensitive comparison."""
    return "".join(
        c for c in unicodedata.normalize("NFD", name.lower())
        if unicodedata.category(c) != "Mn"
    )


class SpotifyClient:
    def __init__(self, sp: Spotify, oauth: SpotifyOAuth, tokens_path: Path, expires_at: int = 0):
        self._sp = sp
        self._oauth = oauth
        self._tokens_path = tokens_path
        self._expires_at = expires_at

    @classmethod
    def from_env(cls) -> "SpotifyClient":
        client_id, client_secret = resolve_client_credentials()
        tokens_path = resolve_tokens_path()
        if not tokens_path.exists():
            raise RuntimeError(
                f"Spotify token file not found at {tokens_path}.\n\n"
                "You need to authenticate first:\n"
                "  .venv/bin/python scripts/spotify_auth.py\n\n"
                "This will open a browser window for Spotify login and save your tokens."
            )

        raw = json.loads(tokens_path.read_text())
        tokens = SpotifyTokens.from_dict(raw)
        oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=os.environ.get("SPOTIFY_REDIRECT_URI", DEFAULT_REDIRECT_URI),
            scope=" ".join(SCOPES),
            cache_path=None,
        )
        oauth.refresh_token = tokens.refresh_token  # type: ignore[attr-defined]
        sp = Spotify(auth=tokens.access_token)
        return cls(sp, oauth, tokens_path=tokens_path, expires_at=tokens.expires_at)

    def _save_tokens(self, token_info: dict[str, Any]) -> None:
        data = {
            "access_token": token_info.get("access_token"),
            "refresh_token": getattr(self._oauth, "refresh_token", None),
            "scope": token_info.get("scope", ""),
            "expires_at": token_info.get("expires_at", 0),
            "token_type": token_info.get("token_type", "Bearer"),
        }
        self._tokens_path.parent.mkdir(parents=True, exist_ok=True)
        self._tokens_path.write_text(json.dumps(data, indent=2))

    def _ensure_fresh_token(self) -> None:
        import time

        if self._expires_at and time.time() < self._expires_at - 60:
            return

        token_info = self._oauth.refresh_access_token(  # type: ignore[attr-defined]
            self._oauth.refresh_token  # type: ignore[attr-defined]
        )
        new_refresh = token_info.get("refresh_token")
        if new_refresh:
            self._oauth.refresh_token = new_refresh  # type: ignore[attr-defined]
        self._sp = Spotify(auth=token_info["access_token"])
        self._expires_at = int(token_info.get("expires_at", 0))
        self._save_tokens(token_info)

    def _with_client(self) -> Spotify:
        self._ensure_fresh_token()
        return self._sp

    def _api_request(self, method: str, path: str, **kwargs) -> requests.Response:
        self._ensure_fresh_token()
        headers = {
            "Authorization": f"Bearer {self._sp._auth}",
            "Content-Type": "application/json",
        }
        response = requests.request(method, f"{API_BASE}/{path.lstrip('/')}" , headers=headers, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def _extract_track(raw: dict) -> dict:
        """Extract a consistent enriched dict from a raw Spotify track object."""
        album = raw.get("album") or {}
        return {
            "name": raw.get("name", ""),
            "artists": [a["name"] for a in raw.get("artists", [])],
            "artist_ids": [a["id"] for a in raw.get("artists", []) if a.get("id")],
            "uri": raw.get("uri", ""),
            "id": raw.get("id", ""),
            "popularity": raw.get("popularity"),
            "duration_ms": raw.get("duration_ms"),
            "explicit": raw.get("explicit"),
            "release_date": album.get("release_date", ""),
            "album": album.get("name", ""),
        }

    def _get_artists_info(self, artist_ids: list[str]) -> dict[str, dict[str, Any]]:
        """Batch-fetch artist data. Returns dict keyed by artist ID.

        IDs are embedded directly in the URL string to avoid ``requests``
        percent-encoding commas (``%2C``), which Spotify's batch endpoint
        rejects with 403. Falls back to individual ``GET /artists/{id}``
        calls on any 403 as defense-in-depth.
        """
        unique_ids = list(dict.fromkeys(artist_ids))
        result: dict[str, dict[str, Any]] = {}

        def _parse_artist(artist: dict) -> None:
            if artist:
                result[artist["id"]] = {
                    "name": artist.get("name", ""),
                    "id": artist["id"],
                    "genres": artist.get("genres", []),
                    "popularity": artist.get("popularity", 0),
                }

        # Batch endpoint — IDs inline to avoid comma encoding
        batch_works = True
        for i in range(0, len(unique_ids), 50):
            batch = unique_ids[i:i + 50]
            try:
                resp = self._api_request("GET", f"artists?ids={','.join(batch)}")
                for artist in resp.json().get("artists") or []:
                    _parse_artist(artist)
            except requests.exceptions.HTTPError as e:
                if e.response is not None and e.response.status_code == 403:
                    batch_works = False
                    break
                raise

        if not batch_works:
            # Fallback: individual artist lookups
            remaining = [aid for aid in unique_ids if aid not in result]
            for aid in remaining:
                try:
                    resp = self._api_request("GET", f"artists/{aid}")
                    _parse_artist(resp.json())
                except Exception:
                    continue

        return result

    def _get_artist_top_tracks(self, artist_id: str) -> list[dict[str, Any]]:
        """Fetch an artist's top tracks. Returns enriched track dicts."""
        try:
            resp = self._api_request("GET", f"artists/{artist_id}/top-tracks")
            return [self._extract_track(t) for t in resp.json().get("tracks", [])]
        except Exception:
            return []

    def get_artist_top_tracks(self, artist_name: str) -> list[dict[str, Any]]:
        """Get an artist's top tracks by name.

        Tries the top-tracks API first, falls back to search (the API
        endpoint often returns 403 due to Spotify regressions).
        """
        # Resolve artist name to ID
        results = self._with_client().search(
            q=f'artist:"{artist_name}"', type="artist", limit=1
        )
        items = results.get("artists", {}).get("items", [])
        if not items:
            return []
        artist_id = items[0]["id"]
        resolved_name = items[0].get("name", artist_name)

        # Try top-tracks endpoint first
        tracks = self._get_artist_top_tracks(artist_id)
        if tracks:
            return tracks

        # Fallback: search for tracks by this artist
        search_results = self.search_track(f'artist:"{resolved_name}"', limit=10)
        return [t for t in search_results if artist_id in t.get("artist_ids", [])]

    def get_artist_releases(
        self,
        artist_name: str,
        limit: int = 5,
        include_groups: str = "single,album",
    ) -> list[dict[str, Any]]:
        """Get an artist's most recent releases with lead track URIs.

        Searches for the artist by name, fetches their recent albums/singles,
        and returns the lead track from each release.
        """
        # Resolve artist name to ID (same pattern as recommend())
        results = self._with_client().search(
            q=f'artist:"{artist_name}"', type="artist", limit=1
        )
        items = results.get("artists", {}).get("items", [])
        if not items:
            return []
        artist_id = items[0]["id"]

        # Fetch recent releases — embed include_groups directly in URL to
        # avoid requests percent-encoding commas (same fix as batch artist endpoint)
        resp = self._api_request(
            "GET",
            f"artists/{artist_id}/albums?include_groups={include_groups}&limit={limit}",
        )
        albums = resp.json().get("items", [])

        releases: list[dict[str, Any]] = []
        for album in albums:
            album_id = album.get("id")
            if not album_id:
                continue
            try:
                track_resp = self._api_request(
                    "GET", f"albums/{album_id}/tracks?limit=1"
                )
                track_items = track_resp.json().get("items", [])
                if not track_items:
                    continue
                track_raw = track_items[0]
                # Inject album info so _extract_track populates release_date/album
                track_raw["album"] = {
                    "name": album.get("name", ""),
                    "release_date": album.get("release_date", ""),
                }
                enriched = self._extract_track(track_raw)
                enriched["album_type"] = album.get("album_type", "")
                enriched["release_date_precision"] = album.get(
                    "release_date_precision", ""
                )
                enriched["total_tracks"] = album.get("total_tracks", 0)
                releases.append(enriched)
            except Exception:
                continue

        return releases

    def get_playlist_info(self, playlist_id: str) -> dict[str, Any]:
        """Fetch playlist metadata (name, owner, declared track total).

        Spotify renamed the ``tracks`` key to ``items`` in playlist responses.
        This method normalizes the response so callers can use ``tracks.total``.
        """
        fields = "id,name,items.total,public,owner.display_name,collaborative"
        resp = self._api_request("GET", f"playlists/{playlist_id}?fields={fields}")
        data = resp.json()
        # Normalize: Spotify uses "items" now, but callers expect "tracks"
        if "items" in data and "tracks" not in data:
            data["tracks"] = data["items"]
        return data

    def list_playlists(self, limit: int = 20) -> List[Dict[str, Any]]:
        sp = self._with_client()
        playlists: List[Dict[str, Any]] = []
        offset = 0
        remaining = limit
        while remaining > 0:
            batch = sp.current_user_playlists(limit=min(50, remaining), offset=offset)
            items = batch.get("items", [])
            if not items:
                break
            playlists.extend(items)
            fetched = len(items)
            if fetched < min(50, remaining):
                break
            remaining -= fetched
            offset += fetched
        return playlists

    def _fetch_items_endpoint(self, playlist_id: str, limit: int | None = None) -> list[dict[str, Any]]:
        """Fetch tracks via GET /playlists/{id}/items (primary endpoint)."""
        tracks: list[dict[str, Any]] = []
        offset = 0
        batch_size = 100
        while True:
            if limit is not None:
                batch_size = min(100, limit - len(tracks))
                if batch_size <= 0:
                    break
            resp = self._api_request(
                "GET",
                f"playlists/{playlist_id}/items",
                params={
                    "limit": batch_size,
                    "offset": offset,
                    "additional_types": "track",
                },
            )
            result = resp.json()
            items = result.get("items") or []
            for item in items:
                track = item.get("track") or item.get("item")
                if not track or not track.get("id"):
                    continue
                tracks.append(self._extract_track(track))
            if not result.get("next") or not items:
                break
            offset += len(items)
        return tracks[:limit] if limit is not None else tracks

    def _fetch_tracks_via_playlist_object(self, playlist_id: str, limit: int | None = None) -> list[dict[str, Any]]:
        """Fallback: fetch tracks embedded in GET /playlists/{id} response.

        Uses a different endpoint than /items, which may work when /items
        returns 403 or empty results due to known Spotify API regressions.
        """
        sp = self._with_client()
        data = sp.playlist(playlist_id, additional_types=("track",))
        page = data.get("tracks") or data.get("items") or {}
        tracks: list[dict[str, Any]] = []
        while True:
            for item in page.get("items") or []:
                track = item.get("track") or item.get("item")
                if not track or not track.get("id"):
                    continue
                tracks.append(self._extract_track(track))
                if limit is not None and len(tracks) >= limit:
                    return tracks[:limit]
            if not page.get("next"):
                break
            try:
                page = sp.next(page)
            except Exception:
                break
        return tracks

    def list_playlist_tracks(self, playlist_id: str, limit: int | None = None) -> list[dict[str, Any]]:
        """Fetch tracks with fallback for known Spotify API issues.

        Tries GET /playlists/{id}/items first. On 403 or empty results,
        falls back to GET /playlists/{id} which embeds tracks in the response.
        """
        items_error = None
        tracks: list[dict[str, Any]] = []

        try:
            tracks = self._fetch_items_endpoint(playlist_id, limit)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 403:
                items_error = e
            else:
                raise

        if items_error or not tracks:
            try:
                fallback = self._fetch_tracks_via_playlist_object(playlist_id, limit)
                if fallback:
                    return fallback
            except Exception:
                pass
            if items_error:
                raise items_error

        return tracks

    def search_track(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        sp = self._with_client()
        # Spotify search API caps limit at 10 as of March 2026
        result = sp.search(q=query, type="track", limit=min(limit, 10))
        return [
            self._extract_track(item)
            for item in (result.get("tracks", {}).get("items") or [])
        ]

    def find_best_track(self, artist: str, title: str) -> dict[str, Any] | None:
        results = self.search_track(f"artist:{artist} track:{title}", limit=5)
        if not results:
            return None
        a_lower = artist.lower()
        t_lower = title.lower()
        for result in results:
            artists_lower = " ".join(result["artists"]).lower()
            if a_lower in artists_lower and t_lower in result["name"].lower():
                return result
        return results[0]

    @staticmethod
    def validate_track_uris(track_uris: list[str]) -> tuple[list[str], list[str]]:
        """Sanitize and validate a list of track URIs.

        Returns (valid_uris, skipped_inputs).
        """
        valid: list[str] = []
        skipped: list[str] = []
        for raw in track_uris:
            uri = raw.strip()
            if not uri:
                continue
            if _SPOTIFY_URI_RE.match(uri):
                valid.append(uri)
            else:
                skipped.append(raw)
        return valid, skipped

    def add_tracks_to_playlist(self, playlist_id: str, track_uris: list[str]) -> None:
        clean, skipped = self.validate_track_uris(track_uris)
        if skipped:
            raise ValueError(
                f"Invalid track URI(s): {', '.join(repr(u) for u in skipped[:5])}\n"
                "Expected format: spotify:track:<22-char id>"
            )
        if not clean:
            raise ValueError("No valid track URIs provided.")
        for i in range(0, len(clean), 100):
            self._api_request("POST", f"playlists/{playlist_id}/items", json={"uris": clean[i:i + 100]})

    def remove_tracks_from_playlist(self, playlist_id: str, track_uris: list[str]) -> None:
        clean, skipped = self.validate_track_uris(track_uris)
        if skipped:
            raise ValueError(
                f"Invalid track URI(s): {', '.join(repr(u) for u in skipped[:5])}\n"
                "Expected format: spotify:track:<22-char id>"
            )
        if not clean:
            raise ValueError("No valid track URIs provided.")
        for i in range(0, len(clean), 100):
            batch = [{"uri": uri} for uri in clean[i:i + 100]]
            self._api_request("DELETE", f"playlists/{playlist_id}/items", json={"items": batch})

    def create_playlist(self, name: str, public: bool = False, description: str = "") -> dict[str, Any]:
        resp = self._api_request("POST", "me/playlists", json={"name": name, "public": public, "description": description})
        data = resp.json()
        return {"name": data["name"], "id": data["id"], "uri": data["uri"]}

    def update_playlist(self, playlist_id: str, name: str | None = None, description: str | None = None, public: bool | None = None) -> None:
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if public is not None:
            body["public"] = public
        if body:
            self._api_request("PUT", f"playlists/{playlist_id}", json=body)

    def get_top_tracks(self, time_range: str = "medium_term", limit: int = 10) -> list[dict[str, Any]]:
        resp = self._api_request("GET", "me/top/tracks", params={"time_range": time_range, "limit": limit})
        return [self._extract_track(t) for t in resp.json().get("items", [])]

    def get_top_artists(self, time_range: str = "medium_term", limit: int = 10) -> list[dict[str, Any]]:
        resp = self._api_request("GET", "me/top/artists", params={"time_range": time_range, "limit": limit})
        return [
            {
                "name": a.get("name", ""),
                "id": a.get("id", ""),
                "uri": a.get("uri", ""),
                "genres": a.get("genres", []),
            }
            for a in resp.json().get("items", [])
        ]

    def get_recently_played(self, limit: int = 10) -> list[dict[str, Any]]:
        resp = self._api_request("GET", "me/player/recently-played", params={"limit": limit})
        items = resp.json().get("items", [])
        results = []
        for item in items:
            if not item.get("track"):
                continue
            track = self._extract_track(item["track"])
            track["played_at"] = item.get("played_at", "")
            results.append(track)
        return results

    def list_devices(self) -> list[dict[str, Any]]:
        return self._with_client().devices().get("devices", [])

    def queue_track(self, track_uri: str) -> None:
        self._api_request("POST", f"me/player/queue?uri={track_uri}")

    def analyze_playlist(self, playlist_id: str, max_tracks: int | None = 200) -> dict[str, Any]:
        """Analyze a playlist's musical DNA: genres, artists, popularity, etc.

        Args:
            max_tracks: Max tracks to fetch for analysis. None = no limit.
                        Large playlists are sampled to stay within time budgets.
        """
        # Fetch metadata first to know the declared total
        declared_total: int | None = None
        playlist_name = ""
        try:
            info = self.get_playlist_info(playlist_id)
            declared_total = info.get("tracks", {}).get("total", 0)
            playlist_name = info.get("name", "")
        except Exception:
            pass

        fetch_limit = max_tracks
        try:
            tracks = self.list_playlist_tracks(playlist_id, limit=fetch_limit)
        except requests.exceptions.HTTPError as http_err:
            status = http_err.response.status_code if http_err.response is not None else None
            result: dict[str, Any] = {"track_count": 0, "tracks": []}
            if declared_total is not None:
                result["declared_total"] = declared_total
            if status == 403:
                result["error"] = (
                    "Spotify returned 403 for this playlist's tracks. "
                    "This is a known Spotify API issue affecting some user-owned "
                    "playlists (even with correct scopes). Try re-authenticating, "
                    "or check the Spotify developer forums for status updates."
                )
            else:
                result["error"] = f"Spotify API error ({status}): {http_err}"
            return result

        if not tracks:
            result = {"track_count": 0, "tracks": []}
            if declared_total is not None:
                result["declared_total"] = declared_total
            if declared_total and declared_total > 0:
                result["warning"] = (
                    f"Spotify reports {declared_total} item(s) in "
                    f"'{playlist_name}' but returned 0 usable tracks. "
                    "Possible causes: all tracks are local files, tracks were "
                    "removed from Spotify's catalog, or the API is not exposing "
                    "this playlist's contents (known /items endpoint quirk)."
                )
            return result

        # Collect artist IDs and batch-fetch info (cap at 100 unique to avoid
        # hundreds of individual API calls when batch endpoint returns 403)
        all_artist_ids: list[str] = []
        for t in tracks:
            all_artist_ids.extend(t.get("artist_ids", []))
        unique_artist_ids = list(dict.fromkeys(all_artist_ids))[:100]
        artist_info = self._get_artists_info(unique_artist_ids) if unique_artist_ids else {}

        # Compute distributions
        from collections import Counter
        artist_counter: Counter[str] = Counter()
        genre_counter: Counter[str] = Counter()
        popularities: list[int] = []
        total_duration = 0
        explicit_count = 0

        for t in tracks:
            for name in t.get("artists", []):
                artist_counter[name] += 1
            if t.get("popularity") is not None:
                popularities.append(t["popularity"])
            if t.get("duration_ms"):
                total_duration += t["duration_ms"]
            if t.get("explicit"):
                explicit_count += 1
            for aid in t.get("artist_ids", []):
                info = artist_info.get(aid)
                if info:
                    for genre in info.get("genres", []):
                        genre_counter[genre] += 1

        top_artists = [name for name, _ in artist_counter.most_common(10)]
        top_genres = [genre for genre, _ in genre_counter.most_common(10)]

        # Pick representative seed tracks: one from each top artist
        # (popularity is stripped from Spotify API, so use artist distribution instead)
        seeds: list[str] = []
        seen_seed_artists: set[str] = set()
        for t in tracks:
            primary = t["artists"][0] if t["artists"] else ""
            if primary not in seen_seed_artists:
                seen_seed_artists.add(primary)
                seeds.append(t["uri"])
                if len(seeds) >= 5:
                    break

        sampled = declared_total is not None and len(tracks) < declared_total
        result = {
            "track_count": len(tracks),
            "total_duration_ms": total_duration,
            "avg_popularity": round(sum(popularities) / len(popularities), 1) if popularities else 0,
            "popularity_range": [min(popularities), max(popularities)] if popularities else [0, 0],
            "artist_distribution": dict(artist_counter.most_common()),
            "top_artists": top_artists,
            "genre_clusters": dict(genre_counter.most_common()),
            "top_genres": top_genres,
            "explicit_ratio": round(explicit_count / len(tracks), 2) if tracks else 0,
            "representative_seed_uris": seeds,
            "tracks": tracks,
        }
        if sampled:
            result["declared_total"] = declared_total
            result["sampled"] = True
            result["warning"] = (
                f"Playlist has {declared_total} tracks; analyzed first {len(tracks)} "
                f"for performance. Use --max-tracks to adjust."
            )

        # Enrich with audio features from ReccoBeats (optional)
        try:
            from reccobeats_client import ReccoBeatsClient
            sample_ids = [t["id"] for t in tracks if t.get("id")][:30]
            if sample_ids:
                rb = ReccoBeatsClient()
                af = rb.get_audio_features(sample_ids)
                if af:
                    feature_keys = [
                        "energy", "danceability", "valence", "acousticness",
                        "instrumentalness", "speechiness", "liveness", "tempo", "loudness",
                    ]
                    agg: dict[str, list[float]] = {k: [] for k in feature_keys}
                    for feat in af.values():
                        for k in feature_keys:
                            v = feat.get(k)
                            if v is not None:
                                agg[k].append(v)
                    summary: dict[str, dict[str, float]] = {}
                    for k, vals in agg.items():
                        if vals:
                            summary[k] = {
                                "avg": round(sum(vals) / len(vals), 3),
                                "min": round(min(vals), 3),
                                "max": round(max(vals), 3),
                            }
                    result["audio_features"] = summary
                    result["audio_features_sample_size"] = len(af)
        except Exception:
            pass

        return result

    def recommend(
        self,
        seed_track_uris: list[str] | None = None,
        seed_playlist_id: str | None = None,
        seed_genres: list[str] | None = None,
        seed_artist_names: list[str] | None = None,
        exclude_artist_names: list[str] | None = None,
        exclude_track_uris: list[str] | None = None,
        boost_artist_names: list[str] | None = None,
        max_per_artist: int = 3,
        popularity_target: int | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Generate scored track recommendations from seeds.

        Uses ReccoBeats as the primary recommendation engine, with Spotify
        as a fallback when ReccoBeats is unavailable.
        """
        exclude_track_ids: set[str] = set()
        exclude_artist_set: set[str] = set(
            _normalize_name(n) for n in (exclude_artist_names or [])
        )
        boost_artist_set: set[str] = set(
            _normalize_name(n) for n in (boost_artist_names or [])
        )
        seed_popularities: list[int] = []
        playlist_track_ids: set[str] = set()
        seed_track_ids: list[str] = []  # Concrete Spotify track IDs for ReccoBeats
        seed_artist_ids: list[str] = []
        seed_genre_set: set[str] = set()
        playlist_audio_features: dict = {}

        # --- Phase 1: Seed resolution ---

        # From playlist
        if seed_playlist_id:
            analysis = self.analyze_playlist(seed_playlist_id)
            playlist_audio_features = analysis.get("audio_features", {})
            for t in analysis.get("tracks", []):
                playlist_track_ids.add(t["id"])
                for aid in t.get("artist_ids", []):
                    if aid not in seed_artist_ids:
                        seed_artist_ids.append(aid)
                if t.get("popularity") is not None:
                    seed_popularities.append(t["popularity"])
            seed_genre_set.update(analysis.get("top_genres", []))
            # Collect representative seed track IDs
            for uri in analysis.get("representative_seed_uris", []):
                tid = uri.split(":")[-1]
                if tid not in seed_track_ids:
                    seed_track_ids.append(tid)
            # Limit seed artists to the top contributors
            artist_dist = analysis.get("artist_distribution", {})
            top_artist_names = list(artist_dist.keys())[:10]
            name_to_id: dict[str, str] = {}
            for t in analysis.get("tracks", []):
                for name, aid in zip(t.get("artists", []), t.get("artist_ids", [])):
                    if name not in name_to_id:
                        name_to_id[name] = aid
            seed_artist_ids = [
                name_to_id[n] for n in top_artist_names if n in name_to_id
            ]

        # From seed track URIs
        if seed_track_uris:
            for uri in seed_track_uris:
                track_id = uri.split(":")[-1]
                exclude_track_ids.add(track_id)
                if track_id not in seed_track_ids:
                    seed_track_ids.append(track_id)
                try:
                    track_data = self._api_request(
                        "GET", f"tracks/{track_id}", params={"market": "US"}
                    ).json()
                except Exception:
                    continue
                if track_data.get("popularity") is not None:
                    seed_popularities.append(track_data["popularity"])
                for artist in track_data.get("artists", []):
                    aid = artist.get("id")
                    if aid and aid not in seed_artist_ids:
                        seed_artist_ids.append(aid)

        # From seed artist names — resolve artist ID + find seed tracks
        if seed_artist_names:
            for name in seed_artist_names:
                results = self._with_client().search(q=f'artist:"{name}"', type="artist", limit=1)
                items = results.get("artists", {}).get("items", [])
                if items:
                    aid = items[0]["id"]
                    if aid not in seed_artist_ids:
                        seed_artist_ids.append(aid)
                    # Get seed tracks: try top tracks first, fall back to search
                    top = self._get_artist_top_tracks(aid)
                    if top and top[0].get("id"):
                        if top[0]["id"] not in seed_track_ids:
                            seed_track_ids.append(top[0]["id"])
                    else:
                        # top-tracks often returns empty; search as fallback
                        search_results = self.search_track(f'artist:"{name}"', limit=3)
                        for sr in search_results:
                            if sr.get("id") and sr["id"] not in seed_track_ids:
                                seed_track_ids.append(sr["id"])
                                break

        # From seed genres — convert to seed tracks via Spotify search
        if seed_genres:
            seed_genre_set.update(g.lower() for g in seed_genres)
            for genre in list(seed_genres)[:6]:
                genre_tracks = self.search_track(f'genre:"{genre}"', limit=2)
                for gt in genre_tracks:
                    if gt.get("id") and gt["id"] not in seed_track_ids:
                        seed_track_ids.append(gt["id"])
                        if len(seed_track_ids) >= 12:
                            break

        # Fetch artist info to populate genre set from seed artists
        if seed_artist_ids:
            artist_info = self._get_artists_info(seed_artist_ids)
            for info in artist_info.values():
                seed_genre_set.update(info.get("genres", []))
        else:
            artist_info = {}

        # Exclude URIs
        if exclude_track_uris:
            for uri in exclude_track_uris:
                exclude_track_ids.add(uri.split(":")[-1])
        exclude_track_ids.update(playlist_track_ids)

        # Popularity target
        if popularity_target is not None:
            pop_center = popularity_target
        elif seed_popularities:
            pop_center = round(sum(seed_popularities) / len(seed_popularities))
        else:
            pop_center = 50

        # Cap seed track IDs to ReccoBeats limit (5 seeds max).
        # Priority: explicit URIs > playlist seeds > artist > genre
        seed_track_ids = seed_track_ids[:5]

        # --- 3-tier fallback chain ---

        # Safety net: final exclude-artists filter applied to all tiers
        def _final_exclude_filter(tracks: list[dict[str, Any]]) -> list[dict[str, Any]]:
            if not exclude_artist_set:
                return tracks
            return [
                t for t in tracks
                if not any(_normalize_name(a) in exclude_artist_set for a in t.get("artists", []))
            ]

        # Tier 1: ReccoBeats recommendations
        reccobeats_available = True
        try:
            result = self._recommend_via_reccobeats(
                seed_track_ids, exclude_track_ids, exclude_artist_set,
                boost_artist_set, pop_center, max_per_artist, limit,
                seed_artist_ids=seed_artist_ids,
                seed_artist_names=seed_artist_names,
            )
            if result:
                return _final_exclude_filter(result)
        except Exception as e:
            reccobeats_available = False
            print(f"Warning: ReccoBeats unavailable ({e})", file=sys.stderr)

        # Tier 2: Audio-feature fallback (playlist-seeded only)
        if playlist_audio_features:
            try:
                print("Using audio-feature fallback for recommendations...", file=sys.stderr)
                result = self._recommend_audio_fallback(
                    playlist_audio_features, seed_artist_ids,
                    seed_artist_names, artist_info,
                    exclude_track_ids, exclude_artist_set, boost_artist_set,
                    pop_center, max_per_artist, limit,
                )
                if result:
                    return _final_exclude_filter(result)
            except Exception as e:
                print(f"Warning: audio-feature fallback failed ({e})", file=sys.stderr)

        # Tier 3: Spotify-only fallback (genre overlap, no audio data)
        print("Using Spotify-only fallback for recommendations...", file=sys.stderr)
        return _final_exclude_filter(self._recommend_spotify_fallback(
            seed_artist_ids, seed_genre_set, artist_info,
            exclude_track_ids, exclude_artist_set, boost_artist_set,
            pop_center, max_per_artist, limit,
        ))

    def _recommend_via_reccobeats(
        self,
        seed_track_ids: list[str],
        exclude_track_ids: set[str],
        exclude_artist_set: set[str],
        boost_artist_set: set[str],
        pop_center: int,
        max_per_artist: int,
        limit: int,
        seed_artist_ids: list[str] | None = None,
        seed_artist_names: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Generate recommendations via ReccoBeats."""
        from collections import Counter
        from reccobeats_client import ReccoBeatsClient

        if not seed_track_ids:
            return []

        rb = ReccoBeatsClient()

        # Resolve Spotify IDs → ReccoBeats UUIDs
        id_map = rb.resolve_track_ids(seed_track_ids)
        if not id_map:
            return []

        seed_uuids = list(id_map.values())

        # Get recommendations
        request_size = min(limit * 2, 100)
        raw_recs = rb.get_recommendations(seed_uuids, size=request_size)
        if not raw_recs:
            return []

        # Convert to standard format and filter
        candidates: list[dict[str, Any]] = []
        for rb_track in raw_recs:
            track = rb.reccobeats_track_to_extract_format(rb_track)
            tid = track.get("id")
            if not tid or tid in exclude_track_ids:
                continue
            if any(_normalize_name(a) in exclude_artist_set for a in track.get("artists", [])):
                continue
            candidates.append(track)

        # --- Supplement candidate pool with seed artist + collaborator tracks ---
        _seed_artist_names = seed_artist_names or []
        _seed_artist_ids = seed_artist_ids or []
        seed_artist_id_set = set(_seed_artist_ids)
        has_artist_context = bool(_seed_artist_ids)
        reccobeats_count = len(candidates)  # track boundary for position scoring
        seen_ids = {t["id"] for t in candidates}
        collaborator_ids: set[str] = set()

        if _seed_artist_names:
            # Phase A: tracks by seed artists + discover collaborators
            for name in _seed_artist_names:
                artist_tracks = self.search_track(f'artist:"{name}"', limit=10)
                for t in artist_tracks:
                    tid = t.get("id")
                    if not tid or tid in exclude_track_ids or tid in seen_ids:
                        continue
                    if any(_normalize_name(a) in exclude_artist_set for a in t.get("artists", [])):
                        continue
                    seen_ids.add(tid)
                    candidates.append(t)
                    # Discover collaborators from co-artist IDs
                    for aid in t.get("artist_ids", []):
                        if aid not in seed_artist_id_set:
                            collaborator_ids.add(aid)

            # Phase B: tracks by collaborators (the scene network)
            # Resolve collaborator names from tracks we already have
            collab_name_map: dict[str, str] = {}
            for t in candidates:
                for aname, aid in zip(t.get("artists", []), t.get("artist_ids", [])):
                    if aid in collaborator_ids and aid not in collab_name_map:
                        collab_name_map[aid] = aname
            for aid, cname in list(collab_name_map.items())[:6]:
                collab_tracks = self.search_track(f'artist:"{cname}"', limit=5)
                for t in collab_tracks:
                    tid = t.get("id")
                    if not tid or tid in exclude_track_ids or tid in seen_ids:
                        continue
                    if any(_normalize_name(a) in exclude_artist_set for a in t.get("artists", [])):
                        continue
                    seen_ids.add(tid)
                    candidates.append(t)

        if not candidates:
            return []

        # --- Scoring ---
        # Fetch audio features for seeds and candidates
        all_ids_for_features = list(seed_track_ids) + [t["id"] for t in candidates]
        audio_features = rb.get_audio_features(all_ids_for_features)

        # Compute seed audio profile (average of seed features)
        seed_profile: dict[str, float] = {}
        audio_keys = ["energy", "danceability", "valence"]
        seed_feature_values: dict[str, list[float]] = {k: [] for k in audio_keys}
        for sid in seed_track_ids:
            feat = audio_features.get(sid)
            if feat:
                for k in audio_keys:
                    v = feat.get(k)
                    if v is not None:
                        seed_feature_values[k].append(v)
        for k in audio_keys:
            vals = seed_feature_values[k]
            if vals:
                seed_profile[k] = sum(vals) / len(vals)

        has_audio = bool(seed_profile)

        scored: list[dict[str, Any]] = []
        for position, track in enumerate(candidates):
            reasons: list[str] = []

            # Position score — only meaningful for ReccoBeats-sourced candidates
            if position < reccobeats_count and reccobeats_count > 1:
                pos_score = 1.0 - (position / reccobeats_count)
                reasons.append(f"recommended (rank {position + 1})")
            else:
                pos_score = 0.0

            # Audio feature alignment
            audio_score = 0.0
            if has_audio:
                feat = audio_features.get(track["id"])
                if feat:
                    diffs: list[float] = []
                    feature_vals: list[str] = []
                    for k in audio_keys:
                        target = seed_profile.get(k)
                        v = feat.get(k)
                        if target is not None and v is not None:
                            diffs.append(abs(v - target))
                            feature_vals.append(f"{k}={v:.2f}")
                    if diffs:
                        avg_diff = sum(diffs) / len(diffs)
                        audio_score = max(0, 1.0 - avg_diff)
                        if feature_vals:
                            reasons.append(f"audio match: {', '.join(feature_vals)}")

            # Popularity match
            pop = track.get("popularity") or 50
            pop_diff = abs(pop - pop_center)
            if pop_diff <= 20:
                pop_score = 1.0
            else:
                pop_score = max(0, 1.0 - (pop_diff - 20) / 60)
            if pop_score >= 0.8:
                reasons.append("popularity match")

            # Artist proximity (seed artist > collaborator > unknown)
            artist_prox = 0.0
            if has_artist_context:
                for aid in track.get("artist_ids", []):
                    if aid in seed_artist_id_set:
                        artist_prox = 1.0
                        reasons.append("seed artist")
                        break
                    if aid in collaborator_ids:
                        artist_prox = max(artist_prox, 0.7)
                if artist_prox == 0.7:
                    reasons.append("collaborator")

            # Weights: artist context shifts weight toward scene proximity
            if has_artist_context:
                score = (
                    pos_score * 0.15
                    + audio_score * 0.20
                    + artist_prox * 0.40
                    + pop_score * 0.10
                )
            elif has_audio and audio_score > 0:
                score = pos_score * 0.40 + audio_score * 0.25 + pop_score * 0.20
            else:
                score = pos_score * 0.55 + pop_score * 0.30

            # Boost
            if any(_normalize_name(a) in boost_artist_set for a in track.get("artists", [])):
                score += 0.15
                reasons.append("boosted artist")

            track_out = dict(track)
            track_out["score"] = round(score, 3)
            track_out["reasons"] = reasons
            track_out["_artist_prox"] = artist_prox
            scored.append(track_out)

        # --- Phase 4: Filtering ---
        scored.sort(key=lambda t: t["score"], reverse=True)
        artist_counts: Counter[str] = Counter()
        affiliated: list[dict[str, Any]] = []
        unaffiliated: list[dict[str, Any]] = []
        for t in scored:
            primary = t["artists"][0] if t["artists"] else ""
            if artist_counts[primary] >= max_per_artist:
                continue
            artist_counts[primary] += 1
            # Separate affiliated (seed/collaborator) from unaffiliated
            if has_artist_context and t.get("_artist_prox", 0) > 0:
                affiliated.append(t)
            else:
                unaffiliated.append(t)

        # When we have artist context, prefer affiliated tracks and only
        # pad with unaffiliated if we need more to fill the limit
        if has_artist_context:
            result = affiliated[:limit]
            if len(result) < limit:
                result.extend(unaffiliated[:limit - len(result)])
        else:
            result = (affiliated + unaffiliated)[:limit]

        # Clean internal keys from output
        for t in result:
            t.pop("_artist_prox", None)

        # If scene-affiliated tracks didn't fill the limit, add a hint
        # pointing the agent to the concentric discovery pattern (Pattern F)
        if has_artist_context and len(affiliated) < limit and affiliated:
            top = affiliated[0]
            collab_names = [
                t["artists"][0] for t in affiliated
                if "collaborator" in t.get("reasons", [])
                and _normalize_name(t["artists"][0]) not in {_normalize_name(n) for n in _seed_artist_names}
            ]
            unique_collabs = list(dict.fromkeys(collab_names))[:4]
            result.append({
                "_hint": (
                    f"Only {len(affiliated)} scene-affiliated tracks found. "
                    f"Use concentric discovery (Pattern F) to expand: "
                    f"run audio-features on {top['uri']} to get the audio DNA, "
                    f"then discover with top tracks as seeds for the next ring. "
                    + (f"Collaborators to explore further: {', '.join(unique_collabs)}. "
                       if unique_collabs else "")
                    + f"Verify outer-ring candidates with audio-features to "
                    f"confirm they still match the original vibe."
                ),
            })

        return result

    def _recommend_spotify_fallback(
        self,
        seed_artist_ids: list[str],
        seed_genre_set: set[str],
        artist_info: dict[str, dict[str, Any]],
        exclude_track_ids: set[str],
        exclude_artist_set: set[str],
        boost_artist_set: set[str],
        pop_center: int,
        max_per_artist: int,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Spotify-only recommendation fallback (original Phase 2+3+4)."""
        from collections import Counter

        candidates: dict[str, dict[str, Any]] = {}

        def add_candidates(tracks: list[dict[str, Any]]) -> None:
            for t in tracks:
                tid = t.get("id")
                if not tid or tid in exclude_track_ids or tid in candidates:
                    continue
                if any(_normalize_name(a) in exclude_artist_set for a in t.get("artists", [])):
                    continue
                candidates[tid] = t

        # Artist top tracks (up to 8 seed artists)
        for aid in seed_artist_ids[:8]:
            add_candidates(self._get_artist_top_tracks(aid))

        # Genre search (up to 6 genres)
        genre_list = list(seed_genre_set)
        for genre in genre_list[:6]:
            add_candidates(self.search_track(f'genre:"{genre}"', limit=10))

        # Artist name search (up to 4 seed artists by name)
        seed_artist_names_resolved: list[str] = []
        for aid in seed_artist_ids[:4]:
            info = artist_info.get(aid)
            if info:
                seed_artist_names_resolved.append(info["name"])
        for name in seed_artist_names_resolved:
            add_candidates(self.search_track(f'artist:"{name}"', limit=10))

        # Cross-genre discovery
        discovery_artist_ids: set[str] = set()
        for t in list(candidates.values())[:50]:
            for aid in t.get("artist_ids", []):
                if aid not in seed_artist_ids and aid not in discovery_artist_ids:
                    discovery_artist_ids.add(aid)
        cross_genre_artists = list(discovery_artist_ids)[:4]
        for aid in cross_genre_artists:
            add_candidates(self._get_artist_top_tracks(aid))

        if not candidates:
            return []

        # Scoring
        all_candidate_artist_ids: list[str] = []
        for t in candidates.values():
            all_candidate_artist_ids.extend(t.get("artist_ids", []))
        candidate_artist_info = self._get_artists_info(all_candidate_artist_ids)

        seed_artist_id_set = set(seed_artist_ids)
        seed_artist_genre_sets: dict[str, set[str]] = {}
        for aid in seed_artist_ids:
            info = artist_info.get(aid) or candidate_artist_info.get(aid)
            if info:
                seed_artist_genre_sets[aid] = set(info.get("genres", []))

        scored: list[dict[str, Any]] = []
        for tid, track in candidates.items():
            reasons: list[str] = []

            cand_genres: set[str] = set()
            for aid in track.get("artist_ids", []):
                info = candidate_artist_info.get(aid)
                if info:
                    cand_genres.update(info.get("genres", []))

            if seed_genre_set and cand_genres:
                intersection = seed_genre_set & cand_genres
                union = seed_genre_set | cand_genres
                genre_score = len(intersection) / len(union) if union else 0
                if intersection:
                    reasons.append(f"genres: {', '.join(list(intersection)[:3])}")
            else:
                genre_score = 0

            artist_prox = 0.0
            for aid in track.get("artist_ids", []):
                if aid in seed_artist_id_set:
                    artist_prox = 1.0
                    reasons.append("same artist as seed")
                    break
                cand_info = candidate_artist_info.get(aid)
                if cand_info:
                    cand_g = set(cand_info.get("genres", []))
                    for said, sg in seed_artist_genre_sets.items():
                        shared = cand_g & sg
                        if len(shared) >= 2:
                            artist_prox = max(artist_prox, 0.7)
                        elif len(shared) >= 1:
                            artist_prox = max(artist_prox, 0.3)
            if artist_prox == 0.7:
                reasons.append("shares multiple genres with seed artists")
            elif artist_prox == 0.3:
                reasons.append("shares a genre with seed artists")

            pop = track.get("popularity") or 50
            pop_diff = abs(pop - pop_center)
            if pop_diff <= 20:
                pop_score = 1.0
            else:
                pop_score = max(0, 1.0 - (pop_diff - 20) / 60)

            release = track.get("release_date", "")
            try:
                year = int(release[:4]) if release else 0
            except (ValueError, IndexError):
                year = 0
            if year >= 2021:
                freshness = 1.0
            elif year >= 2010:
                freshness = 0.75
            elif year > 0:
                freshness = 0.5
            else:
                freshness = 0.5

            score = (
                genre_score * 0.35
                + artist_prox * 0.30
                + pop_score * 0.20
                + freshness * 0.15
            )

            if any(_normalize_name(a) in boost_artist_set for a in track.get("artists", [])):
                score += 0.15
                reasons.append("boosted artist")

            track_out = dict(track)
            track_out["score"] = round(score, 3)
            track_out["reasons"] = reasons
            scored.append(track_out)

        scored.sort(key=lambda t: t["score"], reverse=True)
        artist_counts: Counter[str] = Counter()
        filtered: list[dict[str, Any]] = []
        for t in scored:
            primary = t["artists"][0] if t["artists"] else ""
            if artist_counts[primary] >= max_per_artist:
                continue
            artist_counts[primary] += 1
            filtered.append(t)

        return filtered[:limit]

    def _recommend_audio_fallback(
        self,
        playlist_audio_features: dict[str, dict[str, float]],
        seed_artist_ids: list[str],
        seed_artist_names: list[str] | None,
        artist_info: dict[str, dict[str, Any]],
        exclude_track_ids: set[str],
        exclude_artist_set: set[str],
        boost_artist_set: set[str],
        pop_center: int,
        max_per_artist: int,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Audio-feature-driven fallback for playlist-seeded recommendations.

        Uses the playlist's audio profile as the target, sources candidates
        from seed artist searches and collaborator discovery, then scores
        them by audio-feature distance via ``score_candidates_by_audio_features()``.
        """
        from collections import Counter

        # Build target profile from playlist audio features (avg values)
        target_profile: dict[str, float] = {}
        for k in self._BLEND_FEATURES:
            feat = playlist_audio_features.get(k)
            if feat and "avg" in feat:
                target_profile[k] = feat["avg"]
        if not target_profile:
            return []

        # Source candidates — artist name search + collaborator discovery
        candidate_tracks: dict[str, dict[str, Any]] = {}
        seen_ids: set[str] = set()
        collaborator_ids: set[str] = set()
        seed_artist_id_set = set(seed_artist_ids)

        # Resolve seed artist names from artist_info if not provided
        search_names: list[str] = list(seed_artist_names or [])
        if not search_names:
            for aid in seed_artist_ids[:8]:
                info = artist_info.get(aid)
                if info and info.get("name"):
                    search_names.append(info["name"])

        # Phase A: tracks by seed artists + discover collaborators
        for name in search_names:
            artist_tracks = self.search_track(f'artist:"{name}"', limit=10)
            for t in artist_tracks:
                tid = t.get("id")
                if not tid or tid in exclude_track_ids or tid in seen_ids:
                    continue
                if any(_normalize_name(a) in exclude_artist_set for a in t.get("artists", [])):
                    continue
                seen_ids.add(tid)
                candidate_tracks[tid] = t
                for aid in t.get("artist_ids", []):
                    if aid not in seed_artist_id_set:
                        collaborator_ids.add(aid)

        # Phase B: tracks by collaborators
        collab_name_map: dict[str, str] = {}
        for t in candidate_tracks.values():
            for aname, aid in zip(t.get("artists", []), t.get("artist_ids", [])):
                if aid in collaborator_ids and aid not in collab_name_map:
                    collab_name_map[aid] = aname
        for aid, cname in list(collab_name_map.items())[:6]:
            collab_tracks = self.search_track(f'artist:"{cname}"', limit=5)
            for t in collab_tracks:
                tid = t.get("id")
                if not tid or tid in exclude_track_ids or tid in seen_ids:
                    continue
                if any(_normalize_name(a) in exclude_artist_set for a in t.get("artists", [])):
                    continue
                seen_ids.add(tid)
                candidate_tracks[tid] = t

        if not candidate_tracks:
            return []

        # Score by audio features
        cand_ids = list(candidate_tracks.keys())
        scored_raw = self.score_candidates_by_audio_features(
            target_profile, cand_ids, candidate_tracks,
        )

        # Convert to recommend output format
        scored: list[dict[str, Any]] = []
        for entry in scored_raw:
            audio_score = max(0.0, 1.0 - entry["distance"])
            pop = entry.get("popularity") or 50
            pop_diff = abs(pop - pop_center)
            if pop_diff <= 20:
                pop_score = 1.0
            else:
                pop_score = max(0, 1.0 - (pop_diff - 20) / 60)

            score = audio_score * 0.70 + pop_score * 0.30

            # Boost
            if any(_normalize_name(a) in boost_artist_set for a in entry.get("artists", [])):
                score += 0.15

            # Build reasons with natural-scale deltas
            delta_parts: list[str] = []
            for k in ["energy", "valence", "danceability", "acousticness", "tempo", "loudness"]:
                fd = entry.get("feature_deltas", {}).get(k)
                if fd:
                    if k == "tempo":
                        delta_parts.append(f"\u0394{k}={fd['delta']:.1f} BPM")
                    elif k == "loudness":
                        delta_parts.append(f"\u0394{k}={fd['delta']:.1f} dB")
                    else:
                        delta_parts.append(f"\u0394{k}={fd['delta']:.2f}")
            reasons: list[str] = []
            if delta_parts:
                reasons.append(f"audio match: {', '.join(delta_parts)}")
            if pop_score >= 0.8:
                reasons.append("popularity match")
            if any(_normalize_name(a) in boost_artist_set for a in entry.get("artists", [])):
                reasons.append("boosted artist")

            track_out = dict(entry)
            track_out["score"] = round(score, 3)
            track_out["reasons"] = reasons
            track_out["_artist_primary"] = entry.get("artists", [""])[0]
            scored.append(track_out)

        # Filter: max-per-artist cap, sort by score desc
        scored.sort(key=lambda t: t["score"], reverse=True)
        artist_counts: Counter[str] = Counter()
        filtered: list[dict[str, Any]] = []
        for t in scored:
            primary = t.pop("_artist_primary", "")
            if artist_counts[primary] >= max_per_artist:
                continue
            artist_counts[primary] += 1
            filtered.append(t)

        return filtered[:limit]

    def discover(self, seed_track_uris: list[str], limit: int = 10) -> list[dict[str, Any]]:
        """Find similar tracks from seeds. Wrapper around recommend()."""
        results = self.recommend(seed_track_uris=seed_track_uris, limit=limit)
        return [
            {k: v for k, v in t.items() if k not in ("score", "reasons")}
            for t in results
        ]

    # ------------------------------------------------------------------
    # DNA Blending
    # ------------------------------------------------------------------

    # Features used for blending. 0-1 scaled features are used directly;
    # loudness and tempo are normalized to 0-1 for distance computation.
    _BLEND_FEATURES = [
        "energy", "valence", "danceability", "acousticness",
        "instrumentalness", "speechiness", "loudness", "tempo",
    ]
    _BLEND_WEIGHTS: dict[str, float] = {
        "energy": 0.20,
        "valence": 0.20,
        "danceability": 0.15,
        "acousticness": 0.15,
        "loudness": 0.10,
        "tempo": 0.10,
        "instrumentalness": 0.05,
        "speechiness": 0.05,
    }

    @staticmethod
    def _normalize_feature(key: str, value: float) -> float:
        """Normalize a feature value to 0-1 range."""
        if key == "loudness":
            # Typical range: -60 to 0 dB
            return max(0.0, min(1.0, (value + 60) / 60))
        if key == "tempo":
            # Typical range: 50-200 BPM
            return max(0.0, min(1.0, (value - 50) / 150))
        return max(0.0, min(1.0, value))

    @staticmethod
    def _denormalize_feature(key: str, value: float) -> float:
        """Convert a 0-1 normalized value back to its natural scale."""
        if key == "loudness":
            return value * 60 - 60
        if key == "tempo":
            return value * 150 + 50
        return value

    def score_candidates_by_audio_features(
        self,
        target_profile: dict[str, float],
        candidate_ids: list[str],
        candidate_tracks: dict[str, dict[str, Any]] | None = None,
        feature_weights: dict[str, float] | None = None,
        max_distance: float | None = None,
    ) -> list[dict[str, Any]]:
        """Score candidate tracks by audio-feature distance from a target profile.

        Args:
            target_profile: feature→value in natural scale (e.g. energy=0.46, tempo=122.5)
            candidate_ids: Spotify track IDs to score
            candidate_tracks: optional pre-fetched metadata keyed by track ID
            feature_weights: per-feature weights (defaults to _BLEND_WEIGHTS)
            max_distance: if set, exclude candidates with distance above this threshold

        Returns list of dicts sorted by ascending distance, each with
        ``distance`` and ``feature_deltas`` showing per-feature breakdown.
        """
        from reccobeats_client import ReccoBeatsClient

        rb = ReccoBeatsClient()
        audio_features = rb.get_audio_features(candidate_ids)
        weights = feature_weights or self._BLEND_WEIGHTS

        results: list[dict[str, Any]] = []
        for tid in candidate_ids:
            feat = audio_features.get(tid)
            if not feat:
                continue

            feature_deltas: dict[str, dict[str, float]] = {}
            weighted_distance = 0.0
            total_weight = 0.0

            for k in self._BLEND_FEATURES:
                target_val = target_profile.get(k)
                cand_val = feat.get(k)
                if target_val is None or cand_val is None:
                    continue

                cand_val = float(cand_val)
                target_val = float(target_val)
                norm_cand = self._normalize_feature(k, cand_val)
                norm_target = self._normalize_feature(k, target_val)
                norm_delta = abs(norm_cand - norm_target)
                raw_delta = abs(cand_val - target_val)

                w = weights.get(k, 0.1)
                weighted_distance += norm_delta * w
                total_weight += w

                feature_deltas[k] = {
                    "value": round(cand_val, 3),
                    "target": round(target_val, 3),
                    "delta": round(raw_delta, 3),
                }

            if total_weight == 0:
                continue

            distance = weighted_distance / total_weight
            if max_distance is not None and distance > max_distance:
                continue

            entry: dict[str, Any] = {}
            if candidate_tracks and tid in candidate_tracks:
                entry.update(candidate_tracks[tid])
            else:
                entry["id"] = tid
                entry["uri"] = f"spotify:track:{tid}"
            entry["distance"] = round(distance, 4)
            entry["feature_deltas"] = feature_deltas
            results.append(entry)

        results.sort(key=lambda x: x["distance"])
        return results

    @classmethod
    def _compute_profile(
        cls, features_by_id: dict[str, dict], track_ids: list[str],
    ) -> dict[str, dict[str, float]]:
        """Compute per-feature summary stats for a group of tracks.

        Returns {feature: {mean, std, min, max}} in NATURAL scale (not
        normalized), plus a ``_norm_mean`` key for internal use.
        """
        import math

        collected: dict[str, list[float]] = {k: [] for k in cls._BLEND_FEATURES}
        for tid in track_ids:
            feat = features_by_id.get(tid)
            if not feat:
                continue
            for k in cls._BLEND_FEATURES:
                v = feat.get(k)
                if v is not None:
                    collected[k].append(float(v))

        profile: dict[str, dict[str, float]] = {}
        for k, vals in collected.items():
            if not vals:
                continue
            mean = sum(vals) / len(vals)
            variance = sum((v - mean) ** 2 for v in vals) / len(vals)
            std = math.sqrt(variance)
            profile[k] = {
                "mean": round(mean, 3),
                "std": round(std, 3),
                "min": round(min(vals), 3),
                "max": round(max(vals), 3),
                "_norm_mean": cls._normalize_feature(k, mean),
                "_norm_std": cls._normalize_feature(k, std) if k not in ("loudness", "tempo") else std / (60 if k == "loudness" else 150),
            }
        return profile

    @classmethod
    def _compute_blend_target(
        cls,
        profile_a: dict[str, dict[str, float]],
        profile_b: dict[str, dict[str, float]],
        weight_a: float = 0.5,
    ) -> dict[str, dict[str, float]]:
        """Compute the blend target zone from two profiles.

        For each feature, the target center is the weighted average of the
        two group means.  The tolerance (how wide the acceptable zone is)
        is derived from the groups' spread: it's the distance from the
        tighter mean to the center, plus the larger std, floored at 0.08
        so we never get a zero-width zone.
        """
        weight_b = 1.0 - weight_a
        target: dict[str, dict[str, float]] = {}

        all_keys = set(profile_a) | set(profile_b)
        for k in cls._BLEND_FEATURES:
            if k not in all_keys:
                continue
            a = profile_a.get(k)
            b = profile_b.get(k)

            if a and b:
                norm_center = a["_norm_mean"] * weight_a + b["_norm_mean"] * weight_b
                # Tolerance: half the distance between the means + avg std, floored
                half_gap = abs(a["_norm_mean"] - b["_norm_mean"]) / 2
                avg_std = (a["_norm_std"] + b["_norm_std"]) / 2
                tolerance = max(half_gap + avg_std, 0.08)
            elif a:
                norm_center = a["_norm_mean"]
                tolerance = max(a["_norm_std"], 0.08)
            elif b:
                norm_center = b["_norm_mean"]
                tolerance = max(b["_norm_std"], 0.08)
            else:
                continue

            center_natural = cls._denormalize_feature(k, norm_center)
            low_natural = cls._denormalize_feature(k, max(0, norm_center - tolerance))
            high_natural = cls._denormalize_feature(k, min(1, norm_center + tolerance))

            target[k] = {
                "center": round(center_natural, 3),
                "low": round(low_natural, 3),
                "high": round(high_natural, 3),
                "_norm_center": norm_center,
                "_tolerance": tolerance,
            }
        return target

    def blend_dna(
        self,
        group_a_uris: list[str] | None = None,
        group_a_playlist_id: str | None = None,
        group_b_uris: list[str] | None = None,
        group_b_playlist_id: str | None = None,
        group_a_label: str = "Group A",
        group_b_label: str = "Group B",
        weight_a: float = 0.5,
        search_artists: list[str] | None = None,
        search_queries: list[str] | None = None,
        candidate_uris: list[str] | None = None,
        genres: list[str] | None = None,
        exclude_artist_names: list[str] | None = None,
        boost_artist_names: list[str] | None = None,
        max_per_artist: int = 3,
        limit: int = 20,
        max_tracks_per_group: int = 100,
    ) -> dict[str, Any]:
        """Blend the audio DNA of two track groups and find candidates
        that sit in the overlap zone.

        Args:
            max_tracks_per_group: Max tracks to load per group from playlists.
                Large playlists are sampled to stay within time budgets.

        Returns a dict with group profiles, blend target, and scored
        candidates — all designed for agent inspection.
        """
        from collections import Counter
        from reccobeats_client import ReccoBeatsClient

        rb = ReccoBeatsClient()
        exclude_artist_set = set(_normalize_name(n) for n in (exclude_artist_names or []))
        boost_artist_set = set(_normalize_name(n) for n in (boost_artist_names or []))
        genre_set = set(g.lower() for g in (genres or []))

        # --- Collect track IDs for each group ---
        group_a_ids: list[str] = []
        group_b_ids: list[str] = []
        exclude_track_ids: set[str] = set()

        if group_a_uris:
            for uri in group_a_uris:
                tid = uri.split(":")[-1]
                group_a_ids.append(tid)
                exclude_track_ids.add(tid)

        if group_a_playlist_id:
            try:
                tracks = self.list_playlist_tracks(group_a_playlist_id, limit=max_tracks_per_group)
                for t in tracks:
                    if t.get("id") and t["id"] not in group_a_ids:
                        group_a_ids.append(t["id"])
                        exclude_track_ids.add(t["id"])
            except Exception:
                pass

        if group_b_uris:
            for uri in group_b_uris:
                tid = uri.split(":")[-1]
                group_b_ids.append(tid)
                exclude_track_ids.add(tid)

        if group_b_playlist_id:
            try:
                tracks = self.list_playlist_tracks(group_b_playlist_id, limit=max_tracks_per_group)
                for t in tracks:
                    if t.get("id") and t["id"] not in group_b_ids:
                        group_b_ids.append(t["id"])
                        exclude_track_ids.add(t["id"])
            except Exception:
                pass

        if not group_a_ids and not group_b_ids:
            return {"error": "No tracks found in either group"}

        # --- Fetch audio features for both groups ---
        # Sample up to 50 tracks per group for profiling to keep API calls bounded
        sample_a = group_a_ids[:50]
        sample_b = group_b_ids[:50]
        all_group_ids = list(set(sample_a + sample_b))
        group_features = rb.get_audio_features(all_group_ids)

        if not group_features:
            return {"error": "Could not fetch audio features for seed tracks"}

        # --- Compute profiles (from sampled tracks) ---
        profile_a = self._compute_profile(group_features, sample_a)
        profile_b = self._compute_profile(group_features, sample_b)
        blend_target = self._compute_blend_target(profile_a, profile_b, weight_a)

        # --- Source candidates ---
        candidate_tracks: dict[str, dict[str, Any]] = {}

        def add_candidate(track: dict[str, Any]) -> bool:
            tid = track.get("id")
            if not tid or tid in exclude_track_ids or tid in candidate_tracks:
                return False
            if any(_normalize_name(a) in exclude_artist_set for a in track.get("artists", [])):
                return False
            candidate_tracks[tid] = track
            return True

        # Strategy 1: ReccoBeats recommendations from both groups
        # ReccoBeats caps at 5 seeds — split evenly between groups
        half = max(1, ReccoBeatsClient.MAX_SEEDS // 2)
        all_seed_ids = (group_a_ids[:half] + group_b_ids[:half])[:ReccoBeatsClient.MAX_SEEDS]
        try:
            id_map = rb.resolve_track_ids(all_seed_ids)
            if id_map:
                seed_uuids = list(id_map.values())
                raw_recs = rb.get_recommendations(seed_uuids, size=min(limit * 3, 100))
                for rb_track in raw_recs:
                    add_candidate(rb.reccobeats_track_to_extract_format(rb_track))
        except Exception:
            pass

        # Strategy 2: Search by artist names (track sourced counts for miss detection)
        search_artist_sourced: dict[str, int] = {}
        artist_sourced_ids: set[str] = set()
        for name in (search_artists or []):
            count = 0
            for track in self.search_track(f'artist:"{name}"', limit=10):
                if add_candidate(track):
                    count += 1
                    artist_sourced_ids.add(track["id"])
                elif track.get("id") in candidate_tracks:
                    artist_sourced_ids.add(track["id"])
            search_artist_sourced[name] = count

        # Strategy 3: Search by genre
        genre_sourced_ids: set[str] = set()
        for genre in list(genres or [])[:6]:
            for track in self.search_track(f'genre:"{genre}"', limit=10):
                tid = track.get("id")
                if add_candidate(track):
                    genre_sourced_ids.add(tid)
                elif tid in candidate_tracks:
                    genre_sourced_ids.add(tid)

        # Strategy 4: Search by free-text queries
        for query in (search_queries or []):
            for track in self.search_track(query, limit=10):
                add_candidate(track)

        # Strategy 5: Explicit candidate URIs
        for uri in (candidate_uris or []):
            tid = uri.split(":")[-1]
            if tid in exclude_track_ids or tid in candidate_tracks:
                continue
            try:
                track_data = self._api_request(
                    "GET", f"tracks/{tid}", params={"market": "US"}
                ).json()
                add_candidate(self._extract_track(track_data))
            except Exception:
                continue

        if not candidate_tracks:
            # Strip internal keys before returning
            def _clean_profile(p: dict) -> dict:
                return {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")} for k, v in p.items()}
            def _clean_target(t: dict) -> dict:
                return {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")} for k, v in t.items()}
            return {
                "group_a": {"label": group_a_label, "track_count": len(group_a_ids), "profile": _clean_profile(profile_a)},
                "group_b": {"label": group_b_label, "track_count": len(group_b_ids), "profile": _clean_profile(profile_b)},
                "blend_target": _clean_target(blend_target),
                "candidates": [],
                "warning": "No candidates found. Try adding --search-artists or --search-queries.",
            }

        # --- Fetch audio features for candidates ---
        cand_ids = list(candidate_tracks.keys())
        cand_features = rb.get_audio_features(cand_ids)

        # --- Score candidates ---
        scored: list[dict[str, Any]] = []
        for tid, track in candidate_tracks.items():
            feat = cand_features.get(tid)
            if not feat:
                continue

            reasons: list[str] = []
            feature_distances: dict[str, dict[str, float]] = {}
            weighted_score = 0.0
            total_weight = 0.0

            for k in self._BLEND_FEATURES:
                target = blend_target.get(k)
                v = feat.get(k)
                if target is None or v is None:
                    continue

                norm_v = self._normalize_feature(k, float(v))
                norm_center = target["_norm_center"]
                tolerance = target["_tolerance"]

                distance = abs(norm_v - norm_center)
                # Score: 1.0 at center, decays to 0 at 2x tolerance
                dim_score = max(0.0, 1.0 - distance / (tolerance * 2))

                w = self._BLEND_WEIGHTS.get(k, 0.1)
                weighted_score += dim_score * w
                total_weight += w

                feature_distances[k] = {
                    "value": round(float(v), 3),
                    "target": target["center"],
                    "in_zone": target["low"] <= float(v) <= target["high"],
                }

            if total_weight == 0:
                continue

            score = weighted_score / total_weight

            # Count how many features are in the blend zone
            in_zone_count = sum(1 for fd in feature_distances.values() if fd["in_zone"])
            total_features = len(feature_distances)
            reasons.append(f"{in_zone_count}/{total_features} features in blend zone")

            # Call out the strongest matches
            for k in ["energy", "valence", "danceability", "acousticness"]:
                fd = feature_distances.get(k)
                if fd and fd["in_zone"]:
                    reasons.append(f"{k}={fd['value']:.2f} (target {fd['target']:.2f})")

            # Boost
            if any(_normalize_name(a) in boost_artist_set for a in track.get("artists", [])):
                score = min(1.0, score + 0.10)
                reasons.append("boosted artist")

            track_out = dict(track)
            track_out["score"] = round(score, 3)
            track_out["reasons"] = reasons
            track_out["feature_distances"] = feature_distances
            scored.append(track_out)

        # --- Genre-based scoring adjustment ---
        # Primary: MusicBrainz genre lookup (Jaccard similarity).
        # Fallback: source-based signals (genre search membership).
        if genre_set and scored:
            # Collect unique primary artist names from scored candidates
            unique_artists = list(dict.fromkeys(
                t["artists"][0] for t in scored if t.get("artists")
            ))
            # Try MusicBrainz for genre data
            mb_genres: dict[str, list[str]] = {}
            try:
                from musicbrainz_client import MusicBrainzClient
                mb = MusicBrainzClient()
                mb_genres = mb.get_genres_batch(unique_artists, top_n=5)
            except Exception:
                pass  # MusicBrainz unavailable — fall back to source-based

            mb_available = any(len(g) > 0 for g in mb_genres.values())

            for t in scored:
                tid = t.get("id", "")
                primary_artist = t["artists"][0] if t.get("artists") else ""

                if mb_available and primary_artist in mb_genres:
                    artist_genres = set(mb_genres[primary_artist])
                    if artist_genres:
                        intersection = genre_set & artist_genres
                        if intersection:
                            genre_bonus = min(0.10, 0.05 * len(intersection))
                            t["score"] = round(min(1.0, t["score"] + genre_bonus), 3)
                            t["reasons"].append(f"genres: {', '.join(list(intersection)[:3])}")
                        else:
                            t["score"] = round(t["score"] * 0.3, 3)
                            t["reasons"].append(f"no genre overlap (penalized)")
                        continue  # MusicBrainz gave us a definitive answer

                # Fallback: source-based signals
                from_genre = tid in genre_sourced_ids
                from_artist = tid in artist_sourced_ids
                if from_genre:
                    t["score"] = round(min(1.0, t["score"] + 0.10), 3)
                    t["reasons"].append("genre match")
                elif not from_artist:
                    t["score"] = round(t["score"] * 0.5, 3)
                    t["reasons"].append("no genre/artist affiliation (penalized)")

        # --- Filter and rank ---
        scored.sort(key=lambda t: t["score"], reverse=True)
        artist_counts: Counter[str] = Counter()
        filtered: list[dict[str, Any]] = []
        for t in scored:
            primary = t["artists"][0] if t["artists"] else ""
            if artist_counts[primary] >= max_per_artist:
                continue
            artist_counts[primary] += 1
            filtered.append(t)

        # --- Detect search artist misses (Fix 2) ---
        search_artist_misses: list[str] = []
        if search_artists:
            final_artist_names = set()
            for t in filtered[:limit]:
                final_artist_names.update(_normalize_name(a) for a in t.get("artists", []))
            search_artist_misses = [
                name for name in search_artists
                if _normalize_name(name) not in final_artist_names
            ]

        # --- Build output ---
        def _clean_profile(p: dict) -> dict:
            return {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")} for k, v in p.items()}
        def _clean_target(t: dict) -> dict:
            return {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")} for k, v in t.items()}

        out = {
            "group_a": {
                "label": group_a_label,
                "track_count": len(group_a_ids),
                "features_sampled": len(sample_a),
                "features_found": sum(1 for tid in sample_a if tid in group_features),
                "profile": _clean_profile(profile_a),
            },
            "group_b": {
                "label": group_b_label,
                "track_count": len(group_b_ids),
                "features_sampled": len(sample_b),
                "features_found": sum(1 for tid in sample_b if tid in group_features),
                "profile": _clean_profile(profile_b),
            },
            "blend_target": _clean_target(blend_target),
            "candidates_sourced": len(candidate_tracks),
            "candidates_scored": len(scored),
            "candidates": filtered[:limit],
        }
        if search_artist_misses:
            out["search_artist_misses"] = search_artist_misses
        if len(group_a_ids) > len(sample_a) or len(group_b_ids) > len(sample_b):
            out["sampling_note"] = (
                f"Large groups sampled for profiling "
                f"(A: {len(sample_a)}/{len(group_a_ids)}, "
                f"B: {len(sample_b)}/{len(group_b_ids)})"
            )
        return out
