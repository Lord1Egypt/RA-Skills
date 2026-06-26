#!/usr/bin/env python3
"""Spotify API client for OpenClaw skill."""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from auth import get_valid_token

BASE = "https://api.spotify.com/v1"


def api(method, path, data=None, params=None):
    token = get_valid_token()
    if not token:
        return {"error": "Not authenticated. Run: python3 scripts/auth.py auth"}

    url = f"{BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    body = json.dumps(data).encode() if data else None
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().strip()
            if not raw:
                return {"ok": True}
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"ok": True, "status": resp.status}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {"error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"error": str(e)}


# ── Playback ──

def now_playing():
    r = api("GET", "/me/player/currently-playing")
    if "error" in r and "item" not in r:
        return r
    if not r or not r.get("item"):
        return {"status": "Nothing playing"}
    item = r["item"]
    artists = ", ".join(a["name"] for a in item.get("artists", []))
    return {
        "track": item["name"],
        "artists": artists,
        "album": item.get("album", {}).get("name", ""),
        "duration_ms": item.get("duration_ms", 0),
        "progress_ms": r.get("progress_ms", 0),
        "is_playing": r.get("is_playing", False),
        "device": r.get("device", {}).get("name", ""),
    }


def play(uri=None, context_uri=None, device_id=None):
    data = {}
    if uri:
        data["uris"] = [uri] if uri.startswith("spotify:track:") else [uri]
    if context_uri:
        data["context_uri"] = context_uri
    params = {"device_id": device_id} if device_id else None
    return api("PUT", "/me/player/play", data or None, params)


def pause(device_id=None):
    params = {"device_id": device_id} if device_id else None
    return api("PUT", "/me/player/pause", params=params)


def skip_next(device_id=None):
    params = {"device_id": device_id} if device_id else None
    return api("POST", "/me/player/next", params=params)


def skip_prev(device_id=None):
    params = {"device_id": device_id} if device_id else None
    return api("POST", "/me/player/previous", params=params)


def seek(position_ms):
    return api("PUT", "/me/player/seek", params={"position_ms": position_ms})


def volume(percent, device_id=None):
    params = {"volume_percent": max(0, min(100, percent))}
    if device_id:
        params["device_id"] = device_id
    return api("PUT", "/me/player/volume", params=params)


def shuffle(state=True):
    return api("PUT", "/me/player/shuffle", params={"state": str(state).lower()})


def repeat(state="off"):
    # off, track, context
    return api("PUT", "/me/player/repeat", params={"state": state})


def queue_add(uri):
    return api("POST", "/me/player/queue", params={"uri": uri})


def queue_get():
    return api("GET", "/me/player/queue")


def devices():
    return api("GET", "/me/player/devices")


def transfer(device_id, play=True):
    return api("PUT", "/me/player", data={"device_ids": [device_id], "play": play})


# ── Search ──

def search(query, types="track,artist,album,playlist", limit=5):
    return api("GET", "/search", params={"q": query, "type": types, "limit": limit})


# ── Library ──

def saved_tracks(limit=20, offset=0):
    return api("GET", "/me/tracks", params={"limit": limit, "offset": offset})


def save_tracks(ids):
    return api("PUT", "/me/tracks", data={"ids": ids})


def remove_saved_tracks(ids):
    return api("DELETE", "/me/tracks", data={"ids": ids})


def saved_albums(limit=20, offset=0):
    return api("GET", "/me/albums", params={"limit": limit, "offset": offset})


# ── Playlists ──

def my_playlists(limit=20):
    return api("GET", "/me/playlists", params={"limit": limit})


def playlist_tracks(playlist_id, limit=50):
    return api("GET", f"/playlists/{playlist_id}/items", params={"limit": limit})


def create_playlist(name, public=False, description=""):
    return api("POST", "/me/playlists", data={
        "name": name, "public": public, "description": description
    })


def add_to_playlist(playlist_id, uris):
    return api("POST", f"/playlists/{playlist_id}/items", data={"uris": uris})


def remove_from_playlist(playlist_id, uris):
    return api("DELETE", f"/playlists/{playlist_id}/items", data={"tracks": [{"uri": u} for u in uris]})


def edit_playlist(playlist_id, name=None, description=None, public=None):
    """Edit playlist details."""
    data = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if public is not None:
        data["public"] = public
    return api("PUT", f"/playlists/{playlist_id}", data=data)


def play_playlist(playlist_id, device_id=None):
    """Start playback of a playlist from the beginning."""
    context_uri = f"spotify:playlist:{playlist_id}"
    params = {"device_id": device_id} if device_id else None
    return api("PUT", "/me/player/play", data={"context_uri": context_uri, "offset": {"position": 0}}, params=params)


def smart_playlist(name, source="top", limit=30, time_range="medium_term", seed_genres=None, audio_features=None):
    """Create a playlist from top tracks, saved tracks, or recommendations based on them.

    Args:
        name: Playlist name
        source: 'top' (top tracks), 'saved' (liked songs), 'top-recs' (recommendations from top tracks)
        limit: Number of tracks (max 100)
        time_range: For top tracks - short_term, medium_term, long_term
        seed_genres: Optional genre seeds for recommendations
        audio_features: Optional dict of target audio features e.g. {"target_energy": 0.8}
    """
    # me() call no longer needed since create_playlist uses /me/playlists

    uris = []

    if source == "top":
        result = top_items("tracks", time_range, min(limit, 50))
        if "items" in result:
            uris = [t["uri"] for t in result["items"] if t]

    elif source == "saved":
        result = saved_tracks(min(limit, 50))
        if "items" in result:
            uris = [t.get("track", t.get("item", {}))["uri"] for t in result["items"] if t.get("track") or t.get("item")]

    elif source == "top-recs":
        # Get top 2 tracks as seeds, then get recommendations
        top_result = top_items("tracks", time_range, 2)
        if "items" not in top_result or len(top_result["items"]) < 1:
            return {"error": "Not enough top tracks to seed recommendations"}
        seed_ids = ",".join(t["id"] for t in top_result["items"][:2])
        rec_params = {"seed_tracks": seed_ids, "limit": min(limit, 100)}
        if seed_genres:
            rec_params["seed_genres"] = seed_genres
        if audio_features:
            rec_params.update(audio_features)
        result = recommendations(**rec_params)
        if "tracks" in result:
            uris = [f"spotify:track:{t['id']}" for t in result["tracks"]]

    else:
        return {"error": f"Unknown source: {source}. Use 'top', 'saved', or 'top-recs'"}

    if not uris:
        return {"error": "No tracks found"}

    # Create playlist
    pl = create_playlist(name, public=False, description=f"Auto-generated from {source}")
    if "id" not in pl:
        return {"error": "Failed to create playlist", "details": pl}

    # Add tracks (Spotify limits 100 per request)
    added = 0
    for i in range(0, len(uris), 100):
        batch = uris[i:i+100]
        add_to_playlist(pl["id"], batch)
        added += len(batch)

    return {
        "playlist": pl["name"],
        "id": pl["id"],
        "url": pl.get("external_urls", {}).get("spotify", ""),
        "tracks_added": added,
        "source": source,
    }


def claw_list(name="Claw-List", seeds=5, per_seed=5, public=False):
    """Create a discovery playlist: diverse seeds from top/saved + mood-matched tracks.
    
    For each seed: 2 same-artist tracks + (per_seed-2) mood-matched discoveries.
    """
    import random as _random
    
    pool = []
    top = top_items("tracks", limit=50)
    for item in top.get("items", []):
        pool.append({"id": item["id"], "uri": item["uri"], "name": item["name"],
                     "artist": ", ".join(a["name"] for a in item.get("artists", []))})
    
    saved = saved_tracks(limit=50)
    for item in saved.get("items", []):
        t = item.get("track") or item.get("item") or {}
        if t.get("id") not in {p["id"] for p in pool}:
            pool.append({"id": t["id"], "uri": t["uri"], "name": t.get("name", "?"),
                         "artist": ", ".join(a["name"] for a in t.get("artists", []))})
    
    # Dedupe by primary artist for diversity
    _random.shuffle(pool)
    seen_artists = set()
    selected = []
    for p in pool:
        primary = p["artist"].split(",")[0].strip().lower()
        if primary not in seen_artists:
            seen_artists.add(primary)
            selected.append(p)
        if len(selected) >= seeds:
            break
    
    def _mood(f):
        terms = []
        if f.get("energy", 0) > 0.7: terms.append("energetic")
        elif f.get("energy", 0) < 0.4: terms.append("chill")
        if f.get("valence", 0) > 0.7: terms.append("upbeat")
        elif f.get("valence", 0) < 0.3: terms.append("dark")
        if f.get("danceability", 0) > 0.7: terms.append("dance")
        if f.get("instrumentalness", 0) > 0.5: terms.append("instrumental")
        if f.get("acousticness", 0) > 0.5: terms.append("acoustic")
        return terms
    
    uris = []
    used_ids = set(s["id"] for s in selected)
    details = []
    
    for s in selected:
        uris.append(s["uri"])
        entry = {"seed": f"{s['name']} — {s['artist']}", "related": []}
        
        feats = audio_features(s["id"])
        mood = _mood(feats)
        artist_name = s["artist"].split(",")[0].strip()
        added = 0
        
        # Same-artist tracks
        results = search(artist_name, types="track", limit=10)
        for track in results.get("tracks", {}).get("items", []):
            if track["id"] not in used_ids and track["id"] != s["id"] and added < 2:
                uris.append(track["uri"])
                used_ids.add(track["id"])
                entry["related"].append(f"{track['name']} — {', '.join(a['name'] for a in track['artists'])}")
                added += 1
        
        # Mood-matched discovery
        if mood and added < per_seed:
            query = f"{' '.join(mood[:2])} similar to {artist_name}"
            results = search(query, types="track", limit=10)
            for track in results.get("tracks", {}).get("items", []):
                if track["id"] not in used_ids and added < per_seed:
                    uris.append(track["uri"])
                    used_ids.add(track["id"])
                    entry["related"].append(f"~ {track['name']} — {', '.join(a['name'] for a in track['artists'])}")
                    added += 1
        
        details.append(entry)
    
    pl = create_playlist(name, public=public,
        description=f"Diverse seeds + mood-matched discoveries ({seeds}×{per_seed}), by Claw")
    add_to_playlist(pl["id"], uris)
    
    return {"playlist": name, "id": pl["id"], "url": pl["external_urls"]["spotify"],
            "seeds": seeds, "per_seed": per_seed, "total_tracks": len(uris), "details": details}


# ── User Data ──

def me():
    return api("GET", "/me")


def top_items(type_="tracks", time_range="medium_term", limit=10):
    return api("GET", f"/me/top/{type_}", params={"time_range": time_range, "limit": limit})


def recently_played(limit=10):
    return api("GET", "/me/player/recently-played", params={"limit": limit})


# ── Audio Features ──

def audio_features(track_id):
    return api("GET", f"/audio-features/{track_id}")


def audio_features_batch(track_ids):
    return api("GET", "/audio-features", params={"ids": ",".join(track_ids)})


# ── Recommendations ──

def recommendations(seed_tracks=None, seed_artists=None, seed_genres=None, limit=10, **tuneable):
    params = {"limit": limit}
    if seed_tracks:
        params["seed_tracks"] = seed_tracks
    if seed_artists:
        params["seed_artists"] = seed_artists
    if seed_genres:
        params["seed_genres"] = seed_genres
    params.update(tuneable)
    return api("GET", "/recommendations", params=params)


# ── Artists ──

def artist(artist_id):
    return api("GET", f"/artists/{artist_id}")


def artist_top_tracks(artist_id):
    return api("GET", f"/artists/{artist_id}/top-tracks", params={"market": "US"})


def follow_artist(ids, unfollow=False):
    method = "DELETE" if unfollow else "PUT"
    return api(method, "/me/following/type/artist", params={"ids": ids})


# ── New Releases ──

def new_releases(limit=10):
    return api("GET", "/browse/new-releases", params={"limit": limit})


# ── CLI ──

COMMANDS = {
    "now-playing": lambda args: now_playing(),
    "play": lambda args: play(uri=args[0] if args else None),
    "play-playlist": lambda args: play_playlist(args[0]),
    "pause": lambda args: pause(),
    "next": lambda args: skip_next(),
    "prev": lambda args: skip_prev(),
    "seek": lambda args: seek(int(args[0])),
    "volume": lambda args: volume(int(args[0])),
    "shuffle": lambda args: shuffle(args[0].lower() == "on" if args else True),
    "repeat": lambda args: repeat(args[0] if args else "off"),
    "queue-add": lambda args: queue_add(args[0]),
    "queue": lambda args: queue_get(),
    "devices": lambda args: devices(),
    "transfer": lambda args: transfer(args[0]),
    "search": lambda args: search(" ".join(args)),
    "saved-tracks": lambda args: saved_tracks(int(args[0]) if args else 20),
    "save": lambda args: save_tracks(args),
    "playlists": lambda args: my_playlists(int(args[0]) if args else 20),
    "playlist-tracks": lambda args: playlist_tracks(args[0]),
    "create-playlist": lambda args: create_playlist(args[0], description=" ".join(args[1:]) if len(args) > 1 else "New Playlist"),
    "edit-playlist": lambda args: edit_playlist(args[0], name=args[1] if len(args) > 1 else None),
    "add-to-playlist": lambda args: add_to_playlist(args[0], args[1:]),
    "remove-from-playlist": lambda args: remove_from_playlist(args[0], args[1:]),
    "claw-list": lambda args: claw_list(
        args[0] if args else "Claw-List",
        seeds=int(args[1]) if len(args) > 1 else 5,
        per_seed=int(args[2]) if len(args) > 2 else 5,
    ),
    "smart-playlist": lambda args: smart_playlist(
        args[0],
        source=args[1] if len(args) > 1 else "top",
        limit=int(args[2]) if len(args) > 2 else 30,
        time_range=args[3] if len(args) > 3 else "medium_term",
    ),
    "top-tracks": lambda args: top_items("tracks", args[0] if args else "medium_term"),
    "top-artists": lambda args: top_items("artists", args[0] if args else "medium_term"),
    "recent": lambda args: recently_played(int(args[0]) if args else 10),
    "audio-features": lambda args: audio_features(args[0]),
    "recommendations": lambda args: recommendations(seed_tracks=args[0] if args else None),
    "new-releases": lambda args: new_releases(int(args[0]) if args else 10),
    "me": lambda args: me(),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"Usage: spotify.py <command> [args]")
        print(f"Commands: {', '.join(sorted(COMMANDS.keys()))}")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]
    result = COMMANDS[cmd](args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
