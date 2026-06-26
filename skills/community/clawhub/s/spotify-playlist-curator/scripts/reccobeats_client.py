#!/usr/bin/env python3
"""ReccoBeats API client — recommendation and audio features backend."""
from __future__ import annotations

import re
import sys
from typing import Any

import requests

_SPOTIFY_HREF_RE = re.compile(r"https://open\.spotify\.com/track/([A-Za-z0-9]+)")
_SPOTIFY_ARTIST_HREF_RE = re.compile(r"https://open\.spotify\.com/artist/([A-Za-z0-9]+)")


class ReccoBeatsClient:
    RECCOBEATS_API = "https://api.reccobeats.com/v1"

    def __init__(self, timeout: int = 10):
        self._timeout = timeout

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{self.RECCOBEATS_API}/{path.lstrip('/')}"
        resp = requests.get(url, params=params, timeout=self._timeout)
        resp.raise_for_status()
        return resp.json()

    def resolve_track_ids(self, spotify_ids: list[str]) -> dict[str, str]:
        """Resolve Spotify track IDs to ReccoBeats UUIDs.

        Returns {spotify_id: reccobeats_uuid} for tracks found.
        """
        result: dict[str, str] = {}
        for i in range(0, len(spotify_ids), 20):
            batch = spotify_ids[i:i + 20]
            try:
                data = self._get("track", params={"ids": ",".join(batch)})
                tracks = data if isinstance(data, list) else data.get("content", data.get("tracks", []))
                if isinstance(tracks, dict):
                    # Single track response
                    tracks = [tracks]
                for track in tracks:
                    spotify_id = self.extract_spotify_id_from_href(track.get("href", ""))
                    rb_id = track.get("id")
                    if spotify_id and rb_id:
                        result[spotify_id] = rb_id
            except requests.exceptions.RequestException as e:
                print(f"Warning: ReccoBeats track resolve failed: {e}", file=sys.stderr)
        return result

    # ReccoBeats /track/recommendation accepts at most 5 seeds.
    MAX_SEEDS = 5

    def get_recommendations(
        self, seed_uuids: list[str], size: int = 40, offset: int = 0
    ) -> list[dict]:
        """Get track recommendations from ReccoBeats UUIDs.

        Returns raw ReccoBeats track dicts in relevance order.
        The API accepts at most 5 seeds; extras are silently trimmed.
        """
        if not seed_uuids:
            return []
        capped = seed_uuids[:self.MAX_SEEDS]
        try:
            data = self._get(
                "track/recommendation",
                params={
                    "seeds": ",".join(capped),
                    "size": size,
                    "offset": offset,
                },
            )
            if isinstance(data, list):
                return data
            return data.get("content", data.get("tracks", []))
        except requests.exceptions.RequestException as e:
            print(f"Warning: ReccoBeats recommendations failed: {e}", file=sys.stderr)
            return []

    def get_audio_features(self, spotify_ids: list[str]) -> dict[str, dict]:
        """Get audio features for Spotify track IDs.

        Returns {spotify_id: {danceability, energy, valence, ...}}.
        """
        result: dict[str, dict] = {}
        for i in range(0, len(spotify_ids), 20):
            batch = spotify_ids[i:i + 20]
            try:
                data = self._get("audio-features", params={"ids": ",".join(batch)})
                features_list = data if isinstance(data, list) else data.get("content", [])
                if isinstance(features_list, dict):
                    features_list = [features_list]
                for item in features_list:
                    # Response keys by ReccoBeats UUID; extract Spotify ID from href
                    sid = ReccoBeatsClient.extract_spotify_id_from_href(
                        item.get("href", "")
                    )
                    if not sid:
                        sid = item.get("trackId") or item.get("spotify_id")
                    if sid and isinstance(item, dict):
                        result[sid] = item
            except requests.exceptions.RequestException as e:
                print(f"Warning: ReccoBeats audio features failed: {e}", file=sys.stderr)
        return result

    def search_artist(self, name: str) -> list[dict]:
        """Search for artists by name."""
        try:
            data = self._get("artist/search", params={"searchText": name})
            if isinstance(data, list):
                return data
            return data.get("content", [])
        except requests.exceptions.RequestException as e:
            print(f"Warning: ReccoBeats artist search failed: {e}", file=sys.stderr)
            return []

    @staticmethod
    def extract_spotify_id_from_href(href: str) -> str | None:
        """Extract Spotify track ID from an open.spotify.com URL."""
        m = _SPOTIFY_HREF_RE.search(href or "")
        return m.group(1) if m else None

    @staticmethod
    def extract_spotify_artist_id_from_href(href: str) -> str | None:
        """Extract Spotify artist ID from an open.spotify.com URL."""
        m = _SPOTIFY_ARTIST_HREF_RE.search(href or "")
        return m.group(1) if m else None

    @staticmethod
    def reccobeats_track_to_extract_format(rb_track: dict) -> dict:
        """Convert a ReccoBeats track dict to the _extract_track() shape."""
        spotify_id = ReccoBeatsClient.extract_spotify_id_from_href(
            rb_track.get("href", "")
        )
        artists = rb_track.get("artists", [])
        artist_names = [a.get("name", "") for a in artists]
        artist_ids = []
        for a in artists:
            aid = ReccoBeatsClient.extract_spotify_artist_id_from_href(
                a.get("href", "")
            )
            if aid:
                artist_ids.append(aid)

        return {
            "name": rb_track.get("trackTitle", ""),
            "artists": artist_names,
            "artist_ids": artist_ids,
            "uri": f"spotify:track:{spotify_id}" if spotify_id else "",
            "id": spotify_id or "",
            "popularity": rb_track.get("popularity"),
            "duration_ms": rb_track.get("durationMs"),
            "explicit": None,
            "release_date": "",
            "album": "",
        }
