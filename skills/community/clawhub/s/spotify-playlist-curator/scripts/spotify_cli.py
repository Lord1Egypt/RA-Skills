#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import requests

from reccobeats_client import ReccoBeatsClient
from spotify_client import SpotifyClient, _SPOTIFY_URI_RE, resolve_client_credentials, resolve_tokens_path


def trim_to_duration(tracks: list[dict[str, Any]], target_ms: int) -> list[dict[str, Any]]:
    """Trim a scored track list to fit within target duration (with 10% tolerance)."""
    result = []
    cumulative = 0
    ceiling = int(target_ms * 1.1)
    for t in tracks:
        dur = t.get("duration_ms") or 240000  # fallback ~4 min
        if cumulative + dur > ceiling and result:
            break
        result.append(t)
        cumulative += dur
    return result


def check_status() -> dict[str, Any]:
    """Check auth and connection status non-destructively."""
    status: dict[str, Any] = {
        "authenticated": False,
        "credentials_found": False,
        "token_exists": False,
        "token_valid": False,
    }

    try:
        resolve_client_credentials()
        status["credentials_found"] = True
    except Exception as e:
        status["credentials_error"] = str(e)
        status["fix"] = (
            "If this is a first run, set up the skill first with 'bash scripts/setup.sh'. "
            "Then fill in .env with SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET."
        )
        return status

    tokens_path = resolve_tokens_path()
    status["token_exists"] = tokens_path.exists()
    if not status["token_exists"]:
        status["fix"] = "Run: .venv/bin/python scripts/spotify_auth.py"
        return status

    try:
        client = SpotifyClient.from_env()
        client._ensure_fresh_token()
        status["token_valid"] = True
        status["authenticated"] = True
        me = client._api_request("GET", "me").json()
        status["user"] = me.get("display_name") or me.get("id")
    except Exception as e:
        status["token_error"] = str(e)
        status["fix"] = "Re-run: .venv/bin/python scripts/spotify_auth.py"

    return status


def main() -> int:
    parser = argparse.ArgumentParser(prog="spotify-playlist-curator")
    parser.add_argument("--json", action="store_true", default=False, help="Output results as JSON")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Check auth and connection status")

    sc = sub.add_parser("search", help="Search for tracks by free-text query")
    sc.add_argument("query")
    sc.add_argument("--limit", type=int, default=5)

    lps = sub.add_parser("list-playlists", help="List your playlists")
    lps.add_argument("--limit", type=int, default=20)

    lp = sub.add_parser("list-playlist", help="List tracks in a playlist")
    lp.add_argument("playlist_id")
    lp.add_argument("--limit", type=int, default=None)

    cp = sub.add_parser("create-playlist", help="Create a new playlist")
    cp.add_argument("name")
    cp.add_argument("--public", action="store_true", default=False)
    cp.add_argument("--description", default="")

    ap = sub.add_parser("add-to-playlist", help="Add tracks to a playlist")
    ap.add_argument("playlist_id")
    ap.add_argument("track_uris", nargs="+", metavar="track_uri")

    rp = sub.add_parser("remove-from-playlist", help="Remove tracks from a playlist")
    rp.add_argument("playlist_id")
    rp.add_argument("track_uris", nargs="+", metavar="track_uri")

    sa = sub.add_parser("search-and-add", help="Search tracks by 'Artist - Title' and add to a playlist")
    sa.add_argument("playlist_id")
    sa.add_argument("queries", nargs="+", metavar='"Artist - Track"')

    tt = sub.add_parser("top-tracks", help="Show top tracks")
    tt.add_argument("--time-range", default="medium_term", choices=["short_term", "medium_term", "long_term"])
    tt.add_argument("--limit", type=int, default=10)

    ta = sub.add_parser("top-artists", help="Show top artists")
    ta.add_argument("--time-range", default="medium_term", choices=["short_term", "medium_term", "long_term"])
    ta.add_argument("--limit", type=int, default=10)

    rc = sub.add_parser("recent", help="Show recently played tracks")
    rc.add_argument("--limit", type=int, default=10)

    up = sub.add_parser("update-playlist", help="Update playlist metadata")
    up.add_argument("playlist_id")
    up.add_argument("--name", default=None)
    up.add_argument("--description", default=None)
    vis = up.add_mutually_exclusive_group()
    vis.add_argument("--public", dest="public", action="store_true", default=None)
    vis.add_argument("--private", dest="public", action="store_false")

    ds = sub.add_parser("discover", help="Find similar tracks from seed tracks")
    ds.add_argument("seed_uris", nargs="+", metavar="seed_uri")
    ds.add_argument("--limit", type=int, default=10)
    ds.add_argument("--add", dest="add_to_playlist", default=None, metavar="playlist_id")

    anp = sub.add_parser("analyze-playlist", help="Analyze a playlist's musical DNA")
    anp.add_argument("playlist_id")
    anp.add_argument("--max-tracks", type=int, default=200, metavar="N",
                     help="Max tracks to analyze (default 200, 0=unlimited)")

    rec = sub.add_parser("recommend", help="Generate scored track recommendations")
    rec.add_argument("--seed-uris", nargs="+", default=None, metavar="URI")
    rec.add_argument("--seed-playlist", default=None, metavar="PLAYLIST_ID")
    rec.add_argument("--genres", nargs="+", default=None, metavar="GENRE")
    rec.add_argument("--artists", nargs="+", default=None, metavar="NAME")
    rec.add_argument("--exclude-artists", nargs="+", default=None, metavar="NAME")
    rec.add_argument("--exclude-uris", nargs="+", default=None, metavar="URI")
    rec.add_argument("--boost-artists", nargs="+", default=None, metavar="NAME")
    rec.add_argument("--max-per-artist", type=int, default=3)
    rec.add_argument("--popularity-target", type=int, default=None)
    rec.add_argument("--limit", type=int, default=20)
    rec.add_argument("--target-duration", type=int, default=None, metavar="MINUTES",
                     help="Target playlist duration in minutes (trims results to fit)")
    rec.add_argument("--add", default=None, metavar="PLAYLIST_ID", help="Add results to existing playlist")
    rec.add_argument("--create", default=None, metavar="NAME", help="Create new playlist with results")

    qu = sub.add_parser("queue", help="Queue a selected track on the active device")
    qu.add_argument("track_uri")

    cfr = sub.add_parser("create-from-recent", help="Create a playlist from recently played tracks")
    cfr.add_argument("name")
    cfr.add_argument("--limit", type=int, default=20)
    cfr.add_argument("--public", action="store_true", default=False)
    cfr.add_argument("--description", default="")

    cft = sub.add_parser("create-from-top", help="Create a playlist from your top tracks")
    cft.add_argument("name")
    cft.add_argument("--time-range", default="medium_term", choices=["short_term", "medium_term", "long_term"])
    cft.add_argument("--limit", type=int, default=20)
    cft.add_argument("--public", action="store_true", default=False)
    cft.add_argument("--description", default="")

    bd = sub.add_parser("blend-dna", help="Blend audio DNA of two track groups and find candidates in the overlap")
    bd.add_argument("--group-a", nargs="+", default=None, metavar="URI", help="Track URIs for group A")
    bd.add_argument("--group-a-playlist", default=None, metavar="ID", help="Playlist ID for group A")
    bd.add_argument("--group-b", nargs="+", default=None, metavar="URI", help="Track URIs for group B")
    bd.add_argument("--group-b-playlist", default=None, metavar="ID", help="Playlist ID for group B")
    bd.add_argument("--label-a", default="Group A", metavar="TEXT", help="Label for group A")
    bd.add_argument("--label-b", default="Group B", metavar="TEXT", help="Label for group B")
    bd.add_argument("--weight-a", type=float, default=0.5, metavar="W", help="Weight for group A (0.0-1.0, default 0.5)")
    bd.add_argument("--search-artists", nargs="+", default=None, metavar="NAME", help="Artists to search for candidates")
    bd.add_argument("--search-queries", nargs="+", default=None, metavar="QUERY", help="Free-text search queries for candidates")
    bd.add_argument("--candidate-uris", nargs="+", default=None, metavar="URI", help="Explicit candidate track URIs")
    bd.add_argument("--genres", nargs="+", default=None, metavar="GENRE", help="Genres to source candidates from and filter by")
    bd.add_argument("--exclude-artists", nargs="+", default=None, metavar="NAME")
    bd.add_argument("--boost-artists", nargs="+", default=None, metavar="NAME")
    bd.add_argument("--max-per-artist", type=int, default=3)
    bd.add_argument("--max-tracks-per-group", type=int, default=100, metavar="N",
                    help="Max tracks to load per group from playlists (default 100, 0=unlimited)")
    bd.add_argument("--limit", type=int, default=20)
    bd.add_argument("--target-duration", type=int, default=None, metavar="MINUTES",
                     help="Target playlist duration in minutes (trims results to fit)")
    bd.add_argument("--add", default=None, metavar="PLAYLIST_ID", help="Add results to existing playlist")
    bd.add_argument("--create", default=None, metavar="NAME", help="Create new playlist with results")

    af = sub.add_parser("audio-features", help="Get audio features for tracks via ReccoBeats")
    af.add_argument("track_ids", nargs="+", metavar="TRACK_ID")

    ar = sub.add_parser("artist-releases", help="Show an artist's most recent releases with lead tracks")
    ar.add_argument("artist_name")
    ar.add_argument("--limit", type=int, default=5)
    ar.add_argument("--include-groups", default="single,album")

    att = sub.add_parser("artist-top-tracks", help="Get an artist's top tracks")
    att.add_argument("artist_name")

    sbf = sub.add_parser("score-by-features", help="Score candidate tracks by audio-feature distance from a target profile")
    sbf.add_argument("--target-playlist", default=None, metavar="PLAYLIST_ID",
                      help="Extract target profile from playlist's avg audio features")
    sbf.add_argument("--target-energy", type=float, default=None)
    sbf.add_argument("--target-valence", type=float, default=None)
    sbf.add_argument("--target-danceability", type=float, default=None)
    sbf.add_argument("--target-acousticness", type=float, default=None)
    sbf.add_argument("--target-tempo", type=float, default=None)
    sbf.add_argument("--target-loudness", type=float, default=None)
    sbf.add_argument("--candidate-ids", nargs="+", default=None, metavar="TRACK_ID",
                      help="Explicit Spotify track IDs to score")
    sbf.add_argument("--candidate-artists", nargs="+", default=None, metavar="NAME",
                      help="Search for tracks by these artists as candidates")
    sbf.add_argument("--exclude-artists", nargs="+", default=None, metavar="NAME")
    sbf.add_argument("--limit", type=int, default=20)
    sbf.add_argument("--max-distance", type=float, default=None,
                      help="Filter out candidates with distance above this threshold")

    tp = sub.add_parser("taste", help="View or update the user's taste profile")
    tp_sub = tp.add_subparsers(dest="taste_action")
    tp_sub.add_parser("show", help="Show the current taste profile")
    tp_exclude = tp_sub.add_parser("exclude", help="Add an artist to the excluded list")
    tp_exclude.add_argument("artist_name", help="Artist to always exclude")
    tp_unexclude = tp_sub.add_parser("unexclude", help="Remove an artist from the excluded list")
    tp_unexclude.add_argument("artist_name", help="Artist to stop excluding")
    tp_fav_genre = tp_sub.add_parser("fav-genre", help="Add a favorite genre")
    tp_fav_genre.add_argument("genre", help="Genre to add")
    tp_unfav_genre = tp_sub.add_parser("unfav-genre", help="Remove a favorite genre")
    tp_unfav_genre.add_argument("genre", help="Genre to remove")
    tp_fav_artist = tp_sub.add_parser("fav-artist", help="Add a favorite artist")
    tp_fav_artist.add_argument("artist_name", help="Artist to add")
    tp_unfav_artist = tp_sub.add_parser("unfav-artist", help="Remove a favorite artist")
    tp_unfav_artist.add_argument("artist_name", help="Artist to remove")
    tp_note = tp_sub.add_parser("note", help="Add a free-text note about the user's taste")
    tp_note.add_argument("text", help="Note text")
    tp_rm_note = tp_sub.add_parser("rm-note", help="Remove a note by index (0-based)")
    tp_rm_note.add_argument("index", type=int, help="Note index to remove")

    args = parser.parse_args()

    def clean_uris(raw_uris: list[str]) -> list[str]:
        """Strip whitespace and filter out empty/invalid URIs with warnings."""
        cleaned: list[str] = []
        for raw in raw_uris:
            uri = raw.strip()
            if not uri:
                continue
            if not _SPOTIFY_URI_RE.match(uri):
                print(f"Skipped invalid URI: {repr(raw)}", file=sys.stderr)
                continue
            cleaned.append(uri)
        return cleaned

    # status command — no Spotify auth needed
    if args.command == "status":
        result = check_status()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["authenticated"]:
                print(f"Authenticated as: {result.get('user', 'unknown')}")
            else:
                print("Not authenticated.")
                if result.get("fix"):
                    print(f"  Fix: {result['fix']}")
                if result.get("credentials_error"):
                    print(f"  Credentials error: {result['credentials_error']}")
                if result.get("token_error"):
                    print(f"  Token error: {result['token_error']}")
        return 0

    # taste profile — no Spotify auth needed
    elif args.command == "taste":
        import taste_profile as tp
        profile = tp.load()
        action = args.taste_action

        if action is None or action == "show":
            if args.json:
                print(json.dumps(profile, indent=2))
            else:
                print("=== Taste Profile ===")
                if profile["excluded_artists"]:
                    print(f"Excluded artists: {', '.join(profile['excluded_artists'])}")
                else:
                    print("Excluded artists: (none)")
                if profile["favorite_genres"]:
                    print(f"Favorite genres: {', '.join(profile['favorite_genres'])}")
                else:
                    print("Favorite genres: (none)")
                if profile["favorite_artists"]:
                    print(f"Favorite artists: {', '.join(profile['favorite_artists'])}")
                else:
                    print("Favorite artists: (none)")
                if profile["notes"]:
                    print("Notes:")
                    for i, note in enumerate(profile["notes"]):
                        print(f"  [{i}] {note}")
                else:
                    print("Notes: (none)")
        elif action == "exclude":
            if tp.add_to_list(profile, "excluded_artists", args.artist_name):
                tp.save(profile)
                print(f"Added '{args.artist_name}' to excluded artists.")
            else:
                print(f"'{args.artist_name}' is already excluded.")
        elif action == "unexclude":
            if tp.remove_from_list(profile, "excluded_artists", args.artist_name):
                tp.save(profile)
                print(f"Removed '{args.artist_name}' from excluded artists.")
            else:
                print(f"'{args.artist_name}' was not in excluded artists.")
        elif action == "fav-genre":
            if tp.add_to_list(profile, "favorite_genres", args.genre):
                tp.save(profile)
                print(f"Added '{args.genre}' to favorite genres.")
            else:
                print(f"'{args.genre}' is already a favorite genre.")
        elif action == "unfav-genre":
            if tp.remove_from_list(profile, "favorite_genres", args.genre):
                tp.save(profile)
                print(f"Removed '{args.genre}' from favorite genres.")
            else:
                print(f"'{args.genre}' was not in favorite genres.")
        elif action == "fav-artist":
            if tp.add_to_list(profile, "favorite_artists", args.artist_name):
                tp.save(profile)
                print(f"Added '{args.artist_name}' to favorite artists.")
            else:
                print(f"'{args.artist_name}' is already a favorite artist.")
        elif action == "unfav-artist":
            if tp.remove_from_list(profile, "favorite_artists", args.artist_name):
                tp.save(profile)
                print(f"Removed '{args.artist_name}' from favorite artists.")
            else:
                print(f"'{args.artist_name}' was not in favorite artists.")
        elif action == "note":
            profile["notes"].append(args.text)
            tp.save(profile)
            print(f"Added note: {args.text}")
        elif action == "rm-note":
            if 0 <= args.index < len(profile["notes"]):
                removed = profile["notes"].pop(args.index)
                tp.save(profile)
                print(f"Removed note: {removed}")
            else:
                print(f"Invalid note index: {args.index}", file=sys.stderr)
                return 1
        return 0

    # audio-features uses ReccoBeats directly — no Spotify auth needed
    elif args.command == "audio-features":
        rb = ReccoBeatsClient()
        # Strip spotify:track: prefix if users pass full URIs
        clean_ids = [
            tid.split(":")[-1] if tid.startswith("spotify:track:") else tid
            for tid in args.track_ids
        ]
        try:
            features = rb.get_audio_features(clean_ids)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        if not features:
            print("No audio features found for those track IDs.", file=sys.stderr)
            return 1
        if args.json:
            not_found = [tid for tid in clean_ids if tid not in features]
            if not_found:
                output = dict(features)
                output["_not_found"] = not_found
                print(json.dumps(output, indent=2))
            else:
                print(json.dumps(features, indent=2))
        else:
            feature_keys = [
                "energy", "danceability", "valence", "acousticness",
                "instrumentalness", "speechiness", "liveness", "tempo", "loudness",
            ]
            for tid in clean_ids:
                feat = features.get(tid)
                if not feat:
                    print(f"{tid}: not found")
                    continue
                vals = "  ".join(
                    f"{k}={feat[k]}" for k in feature_keys if k in feat
                )
                print(f"{tid}: {vals}")
        return 0

    try:
        client = SpotifyClient.from_env()
        use_json = args.json

        # Load taste profile and merge excluded artists into --exclude-artists
        import taste_profile as tp
        _taste = tp.load()
        _taste_excludes = _taste.get("excluded_artists", [])
        if _taste_excludes and hasattr(args, "exclude_artists"):
            if args.exclude_artists:
                merged = list(args.exclude_artists)
                existing_lower = {a.lower() for a in merged}
                for a in _taste_excludes:
                    if a.lower() not in existing_lower:
                        merged.append(a)
                args.exclude_artists = merged
            else:
                args.exclude_artists = list(_taste_excludes)

        def output_json(data: object) -> None:
            print(json.dumps(data, indent=2))

        if args.command == "search":
            tracks = client.search_track(args.query, limit=args.limit)
            if use_json:
                output_json(tracks)
            else:
                for track in tracks:
                    print(f"{', '.join(track['artists'])} — {track['name']} | uri={track['uri']}")
        elif args.command == "list-playlists":
            playlists = client.list_playlists(limit=args.limit)
            if use_json:
                output_json(playlists)
            else:
                for playlist in playlists:
                    visibility = "public" if playlist.get("public") else "private"
                    print(f"{playlist.get('name')} | id={playlist.get('id')} | {visibility}")
        elif args.command == "list-playlist":
            try:
                tracks = client.list_playlist_tracks(args.playlist_id, limit=args.limit)
            except requests.exceptions.HTTPError as http_err:
                status = http_err.response.status_code if http_err.response is not None else "?"
                if status == 403:
                    print(
                        "Error: Spotify returned 403 for this playlist's tracks. "
                        "This is a known Spotify API issue affecting some playlists "
                        "(even with correct scopes). Try re-authenticating, or check "
                        "the Spotify developer forums for status updates.",
                        file=sys.stderr,
                    )
                else:
                    print(f"Error: {http_err}", file=sys.stderr)
                return 1
            if use_json:
                output_json(tracks)
            else:
                for track in tracks:
                    print(f"{', '.join(track['artists'])} — {track['name']}")
        elif args.command == "create-playlist":
            result = client.create_playlist(args.name, public=args.public, description=args.description)
            if use_json:
                output_json(result)
            else:
                print(f"{result['name']} | id={result['id']} | uri={result['uri']}")
        elif args.command == "add-to-playlist":
            uris = clean_uris(args.track_uris)
            if not uris:
                print("Error: no valid track URIs provided. Expected format: spotify:track:<id>", file=sys.stderr)
                return 1
            client.add_tracks_to_playlist(args.playlist_id, uris)
            print(f"Added {len(uris)} track(s) to playlist {args.playlist_id}")
        elif args.command == "remove-from-playlist":
            uris = clean_uris(args.track_uris)
            if not uris:
                print("Error: no valid track URIs provided. Expected format: spotify:track:<id>", file=sys.stderr)
                return 1
            client.remove_tracks_from_playlist(args.playlist_id, uris)
            print(f"Removed {len(uris)} track(s) from playlist {args.playlist_id}")
        elif args.command == "search-and-add":
            uris: list[str] = []
            for query in args.queries:
                parts = query.split(" - ", 1)
                if len(parts) != 2:
                    print(f"Skipped (expected 'Artist - Title'): {query}", file=sys.stderr)
                    continue
                artist, title = parts[0].strip(), parts[1].strip()
                match = client.find_best_track(artist, title)
                if match:
                    uris.append(match["uri"])
                    print(f"Added: {', '.join(match['artists'])} — {match['name']}", file=sys.stderr)
                else:
                    print(f"No match for: {query}", file=sys.stderr)
            if not uris:
                print("No tracks matched; nothing added.", file=sys.stderr)
                return 1
            client.add_tracks_to_playlist(args.playlist_id, uris)
            print(f"Added {len(uris)} track(s) to playlist {args.playlist_id}")
        elif args.command == "top-tracks":
            tracks = client.get_top_tracks(time_range=args.time_range, limit=args.limit)
            if use_json:
                output_json(tracks)
            else:
                for i, track in enumerate(tracks, 1):
                    print(f"{i}. {', '.join(track['artists'])} — {track['name']} | uri={track['uri']}")
        elif args.command == "top-artists":
            artists = client.get_top_artists(time_range=args.time_range, limit=args.limit)
            if use_json:
                output_json(artists)
            else:
                for i, artist in enumerate(artists, 1):
                    genres = ", ".join(artist["genres"][:3]) if artist["genres"] else "no genres"
                    print(f"{i}. {artist['name']} ({genres}) | uri={artist['uri']}")
        elif args.command == "recent":
            tracks = client.get_recently_played(limit=args.limit)
            if use_json:
                output_json(tracks)
            else:
                for track in tracks:
                    ts = track["played_at"][:16].replace("T", " ") if track["played_at"] else ""
                    print(f"{ts}  {', '.join(track['artists'])} — {track['name']} | uri={track['uri']}")
        elif args.command == "update-playlist":
            client.update_playlist(args.playlist_id, name=args.name, description=args.description, public=args.public)
            print(f"Updated playlist {args.playlist_id}")
        elif args.command == "analyze-playlist":
            max_t = args.max_tracks if args.max_tracks > 0 else None
            analysis = client.analyze_playlist(args.playlist_id, max_tracks=max_t)
            if analysis.get("error"):
                print(f"Error: {analysis['error']}", file=sys.stderr)
                return 1
            if use_json:
                output_json(analysis)
            else:
                if analysis.get("warning"):
                    print(f"Warning: {analysis['warning']}", file=sys.stderr)
                if analysis["track_count"] == 0:
                    declared = analysis.get("declared_total")
                    if declared:
                        print(f"Tracks: 0 (Spotify reports {declared} items — see warning above)")
                    else:
                        print("Tracks: 0")
                    return 0
                if analysis.get("sampled"):
                    print(f"Tracks: {analysis['track_count']} (of {analysis['declared_total']} total, sampled)")
                else:
                    print(f"Tracks: {analysis['track_count']}")
                dur_min = analysis['total_duration_ms'] // 60000
                print(f"Duration: {dur_min} min")
                print(f"Avg popularity: {analysis['avg_popularity']} (range {analysis['popularity_range'][0]}-{analysis['popularity_range'][1]})")
                print(f"Explicit ratio: {analysis['explicit_ratio']}")
                print(f"Top artists: {', '.join(analysis['top_artists'][:5])}")
                print(f"Top genres: {', '.join(analysis['top_genres'][:5])}")
                if analysis.get("audio_features"):
                    af = analysis["audio_features"]
                    sample = analysis.get("audio_features_sample_size", "?")
                    print(f"Audio profile ({sample} tracks sampled):")
                    for key in ["energy", "danceability", "valence", "acousticness",
                                "instrumentalness", "speechiness", "liveness", "tempo", "loudness"]:
                        feat = af.get(key)
                        if feat:
                            print(f"  {key}: avg={feat['avg']}  range=[{feat['min']}, {feat['max']}]")
        elif args.command == "recommend":
            if not any([args.seed_uris, args.seed_playlist, args.genres, args.artists]):
                print("Error: at least one seed source required (--seed-uris, --seed-playlist, --genres, or --artists)", file=sys.stderr)
                return 1
            rec_limit = args.limit
            if args.target_duration:
                rec_limit = max(rec_limit, 40)
            tracks = client.recommend(
                seed_track_uris=args.seed_uris,
                seed_playlist_id=args.seed_playlist,
                seed_genres=args.genres,
                seed_artist_names=args.artists,
                exclude_artist_names=args.exclude_artists,
                exclude_track_uris=args.exclude_uris,
                boost_artist_names=args.boost_artists,
                max_per_artist=args.max_per_artist,
                popularity_target=args.popularity_target,
                limit=rec_limit,
            )
            if not tracks:
                print("No recommendations found for those seeds.", file=sys.stderr)
                return 1
            if args.target_duration:
                tracks = trim_to_duration(tracks, args.target_duration * 60000)
                total_ms = sum(t.get("duration_ms") or 0 for t in tracks)
                if use_json:
                    # inject duration metadata — will be output below
                    pass
                else:
                    print(f"Trimmed to {len(tracks)} tracks ({total_ms // 60000} min)", file=sys.stderr)
            if use_json:
                output_json(tracks)
            else:
                for i, track in enumerate(tracks, 1):
                    if "uri" not in track:
                        continue
                    reasons = "; ".join(track.get("reasons", []))
                    print(f"{i}. {', '.join(track['artists'])} — {track['name']} (score={track['score']}) | uri={track['uri']}")
                    if reasons:
                        print(f"   {reasons}")
            if args.add:
                uris = [t["uri"] for t in tracks if "uri" in t]
                client.add_tracks_to_playlist(args.add, uris)
                print(f"Added {len(uris)} track(s) to playlist {args.add}", file=sys.stderr)
            elif args.create:
                playlist = client.create_playlist(args.create)
                uris = [t["uri"] for t in tracks if "uri" in t]
                client.add_tracks_to_playlist(playlist["id"], uris)
                print(f"Created '{playlist['name']}' with {len(uris)} track(s) | id={playlist['id']}", file=sys.stderr)
        elif args.command == "blend-dna":
            if not any([args.group_a, args.group_a_playlist, args.group_b, args.group_b_playlist]):
                print("Error: at least one group required (--group-a, --group-a-playlist, --group-b, --group-b-playlist)", file=sys.stderr)
                return 1
            max_tpg = args.max_tracks_per_group if args.max_tracks_per_group > 0 else None
            bd_limit = args.limit
            if args.target_duration:
                bd_limit = max(bd_limit, 40)
            result = client.blend_dna(
                group_a_uris=args.group_a,
                group_a_playlist_id=args.group_a_playlist,
                group_b_uris=args.group_b,
                group_b_playlist_id=args.group_b_playlist,
                group_a_label=args.label_a,
                group_b_label=args.label_b,
                weight_a=args.weight_a,
                search_artists=args.search_artists,
                search_queries=args.search_queries,
                candidate_uris=args.candidate_uris,
                genres=args.genres,
                exclude_artist_names=args.exclude_artists,
                boost_artist_names=args.boost_artists,
                max_per_artist=args.max_per_artist,
                limit=bd_limit,
                max_tracks_per_group=max_tpg or 100,
            )
            if result.get("error"):
                print(f"Error: {result['error']}", file=sys.stderr)
                return 1
            candidates = result.get("candidates", [])
            if args.target_duration:
                candidates = trim_to_duration(candidates, args.target_duration * 60000)
                result["candidates"] = candidates
                result["total_duration_ms"] = sum(t.get("duration_ms") or 0 for t in candidates)
            if use_json:
                output_json(result)
            else:
                ga = result["group_a"]
                gb = result["group_b"]
                print(f"=== {ga['label']} ({ga['track_count']} tracks, {ga.get('features_found', '?')} with audio) ===")
                for k, v in ga.get("profile", {}).items():
                    print(f"  {k}: mean={v['mean']}  std={v['std']}  range=[{v['min']}, {v['max']}]")
                print(f"\n=== {gb['label']} ({gb['track_count']} tracks, {gb.get('features_found', '?')} with audio) ===")
                for k, v in gb.get("profile", {}).items():
                    print(f"  {k}: mean={v['mean']}  std={v['std']}  range=[{v['min']}, {v['max']}]")
                print(f"\n=== Blend target ===")
                for k, v in result.get("blend_target", {}).items():
                    print(f"  {k}: center={v['center']}  zone=[{v['low']}, {v['high']}]")
                print(f"\nSourced {result.get('candidates_sourced', 0)} candidates, scored {result.get('candidates_scored', 0)}")
                if candidates:
                    print(f"\nTop {len(candidates)} candidates:")
                    for i, t in enumerate(candidates, 1):
                        reasons = "; ".join(t.get("reasons", []))
                        print(f"{i}. {', '.join(t['artists'])} — {t['name']} (score={t['score']}) | uri={t['uri']}")
                        if reasons:
                            print(f"   {reasons}")
                else:
                    print("\nNo candidates matched the blend zone.")
                    if result.get("warning"):
                        print(f"  {result['warning']}")
            if candidates and args.add:
                uris = [t["uri"] for t in candidates]
                client.add_tracks_to_playlist(args.add, uris)
                print(f"Added {len(uris)} track(s) to playlist {args.add}", file=sys.stderr)
            elif candidates and args.create:
                playlist = client.create_playlist(args.create)
                uris = [t["uri"] for t in candidates]
                client.add_tracks_to_playlist(playlist["id"], uris)
                print(f"Created '{playlist['name']}' with {len(uris)} track(s) | id={playlist['id']}", file=sys.stderr)
        elif args.command == "discover":
            tracks = client.discover(args.seed_uris, limit=args.limit)
            if not tracks:
                print("No discoveries found for those seeds.", file=sys.stderr)
                return 1
            if use_json:
                output_json(tracks)
            else:
                for track in tracks:
                    print(f"{', '.join(track['artists'])} — {track['name']} | uri={track['uri']}")
            if args.add_to_playlist:
                client.add_tracks_to_playlist(args.add_to_playlist, [track["uri"] for track in tracks])
                print(f"Added {len(tracks)} discovered track(s) to playlist {args.add_to_playlist}", file=sys.stderr)
        elif args.command == "queue":
            if not any(device.get("is_active") for device in client.list_devices()):
                print("No active Spotify device is available for queueing.", file=sys.stderr)
                return 1
            client.queue_track(args.track_uri)
            print(f"Queued: {args.track_uri}")
        elif args.command == "create-from-recent":
            tracks = client.get_recently_played(limit=args.limit)
            if not tracks:
                print("No recent listening history found.", file=sys.stderr)
                return 1
            track_uris = [t["uri"] for t in tracks if t.get("uri")]
            # Deduplicate while preserving order (recent can have repeats)
            seen: set[str] = set()
            unique_uris: list[str] = []
            for uri in track_uris:
                if uri not in seen:
                    seen.add(uri)
                    unique_uris.append(uri)
            playlist = client.create_playlist(args.name, public=args.public, description=args.description)
            client.add_tracks_to_playlist(playlist["id"], unique_uris)
            if use_json:
                output_json({"playlist": playlist, "tracks_added": len(unique_uris), "tracks": tracks})
            else:
                print(f"Created '{playlist['name']}' with {len(unique_uris)} track(s) | id={playlist['id']}")
        elif args.command == "create-from-top":
            tracks = client.get_top_tracks(time_range=args.time_range, limit=args.limit)
            if not tracks:
                print("No top tracks found for that time range.", file=sys.stderr)
                return 1
            track_uris = [t["uri"] for t in tracks if t.get("uri")]
            playlist = client.create_playlist(args.name, public=args.public, description=args.description)
            client.add_tracks_to_playlist(playlist["id"], track_uris)
            if use_json:
                output_json({"playlist": playlist, "tracks_added": len(track_uris), "tracks": tracks})
            else:
                print(f"Created '{playlist['name']}' with {len(track_uris)} track(s) | id={playlist['id']}")
        elif args.command == "artist-releases":
            releases = client.get_artist_releases(
                args.artist_name,
                limit=args.limit,
                include_groups=args.include_groups,
            )
            if not releases:
                print(f"No releases found for '{args.artist_name}'.", file=sys.stderr)
                return 1
            if use_json:
                output_json(releases)
            else:
                for i, track in enumerate(releases, 1):
                    album_type = track.get("album_type", "")
                    release_date = track.get("release_date", "")
                    print(
                        f"{i}. [{album_type}] {release_date} — "
                        f"{', '.join(track['artists'])} — {track['name']} "
                        f"(from {track['album']}) | uri={track['uri']}"
                    )
        elif args.command == "artist-top-tracks":
            tracks = client.get_artist_top_tracks(args.artist_name)
            if not tracks:
                print(f"No top tracks found for '{args.artist_name}'.", file=sys.stderr)
                return 1
            if use_json:
                output_json(tracks)
            else:
                for i, track in enumerate(tracks, 1):
                    print(
                        f"{i}. {', '.join(track['artists'])} \u2014 {track['name']} "
                        f"| uri={track['uri']}"
                    )
        elif args.command == "score-by-features":
            # Build target profile
            target_profile: dict[str, float] = {}
            if args.target_playlist:
                analysis = client.analyze_playlist(args.target_playlist)
                af = analysis.get("audio_features", {})
                for k in ["energy", "valence", "danceability", "acousticness",
                           "instrumentalness", "speechiness", "loudness", "tempo"]:
                    feat = af.get(k)
                    if feat and "avg" in feat:
                        target_profile[k] = feat["avg"]
            # Explicit target values override playlist values
            explicit_targets = {
                "energy": args.target_energy,
                "valence": args.target_valence,
                "danceability": args.target_danceability,
                "acousticness": args.target_acousticness,
                "tempo": args.target_tempo,
                "loudness": args.target_loudness,
            }
            for k, v in explicit_targets.items():
                if v is not None:
                    target_profile[k] = v
            if not target_profile:
                print("Error: no target profile specified. Use --target-playlist and/or --target-<feature> flags.", file=sys.stderr)
                return 1
            if not args.candidate_ids and not args.candidate_artists:
                print("Error: no candidates specified. Use --candidate-ids and/or --candidate-artists.", file=sys.stderr)
                return 1

            # Build candidate pool
            candidate_tracks: dict[str, dict[str, Any]] = {}
            exclude_artist_set = set(n.lower() for n in (args.exclude_artists or []))
            if args.candidate_artists:
                for name in args.candidate_artists:
                    tracks = client.search_track(f'artist:"{name}"', limit=10)
                    for t in tracks:
                        tid = t.get("id")
                        if not tid or tid in candidate_tracks:
                            continue
                        if any(a.lower() in exclude_artist_set for a in t.get("artists", [])):
                            continue
                        candidate_tracks[tid] = t
            if args.candidate_ids:
                for raw_id in args.candidate_ids:
                    tid = raw_id.split(":")[-1] if raw_id.startswith("spotify:track:") else raw_id
                    if tid not in candidate_tracks:
                        candidate_tracks[tid] = {"id": tid, "uri": f"spotify:track:{tid}"}
            if not candidate_tracks:
                print("No candidates found after filtering.", file=sys.stderr)
                return 1

            # Score
            cand_ids = list(candidate_tracks.keys())
            results = client.score_candidates_by_audio_features(
                target_profile, cand_ids, candidate_tracks,
                max_distance=args.max_distance,
            )
            # Apply exclude-artists filter on results
            results = [
                r for r in results
                if not any(a.lower() in exclude_artist_set for a in r.get("artists", []))
            ]
            results = results[:args.limit]

            if not results:
                print("No candidates matched the target profile.", file=sys.stderr)
                return 1
            if use_json:
                output_json(results)
            else:
                for i, entry in enumerate(results, 1):
                    artists = ", ".join(entry.get("artists", ["?"]))
                    name = entry.get("name", entry.get("id", "?"))
                    uri = entry.get("uri", "")
                    dist = entry.get("distance", 0)
                    print(f"{i}. {artists} \u2014 {name} (distance={dist}) | uri={uri}")
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
                    if delta_parts:
                        print(f"   {', '.join(delta_parts)}")
        else:
            parser.print_help()
            return 1
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
