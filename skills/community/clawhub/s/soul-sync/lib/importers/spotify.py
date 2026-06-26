#!/usr/bin/env python3
"""
Spotify Importer — Analyzes Spotify listening history for taste and personality insights.
Uses Spotify Web API. Requires OAuth token or uses public playlist data.

Setup: Create app at https://developer.spotify.com/dashboard
Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET env vars.
"""
import os
import sys
import json
import urllib.request
import urllib.parse
import base64
from datetime import datetime, timezone
from collections import Counter

IMPORT_DIR = "/tmp/soulsync"

def get_spotify_token():
    """Get Spotify access token via client credentials flow."""
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        return None
    
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=data,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            return result.get("access_token")
    except Exception:
        return None

def spotify_api(endpoint, token):
    """Make Spotify API request."""
    req = urllib.request.Request(
        f"https://api.spotify.com/v1/{endpoint}",
        headers={"Authorization": f"Bearer {token}"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except Exception:
        return None

def analyze_user_playlists(user_id, token):
    """Analyze a user's public playlists for taste signals."""
    playlists = spotify_api(f"users/{user_id}/playlists?limit=50", token)
    if not playlists or "items" not in playlists:
        return None
    
    genres = Counter()
    artists = Counter()
    playlist_names = []
    total_tracks = 0
    
    for playlist in playlists.get("items", [])[:20]:
        if not playlist:
            continue
        
        playlist_names.append(playlist.get("name", ""))
        track_count = playlist.get("tracks", {}).get("total", 0)
        total_tracks += track_count
        
        # Get first 50 tracks from each playlist
        playlist_id = playlist.get("id")
        if playlist_id:
            tracks = spotify_api(
                f"playlists/{playlist_id}/tracks?limit=50&fields=items(track(artists(name,id)))",
                token
            )
            if tracks and "items" in tracks:
                for item in tracks["items"]:
                    track = item.get("track")
                    if track and track.get("artists"):
                        for artist in track["artists"]:
                            name = artist.get("name")
                            if name:
                                artists[name] += 1
                                
                                # Get artist genres
                                artist_id = artist.get("id")
                                if artist_id:
                                    artist_data = spotify_api(f"artists/{artist_id}", token)
                                    if artist_data and "genres" in artist_data:
                                        for genre in artist_data["genres"]:
                                            genres[genre] += 1
    
    return {
        "playlists": playlist_names,
        "top_artists": [a for a, _ in artists.most_common(20)],
        "top_genres": [g for g, _ in genres.most_common(15)],
        "total_tracks": total_tracks,
        "playlist_count": len(playlists.get("items", [])),
    }

def infer_personality_from_music(analysis):
    """Map music taste to personality traits."""
    if not analysis:
        return {}
    
    traits = []
    genres = [g.lower() for g in analysis.get("top_genres", [])]
    
    # Genre-personality correlations (simplified)
    genre_traits = {
        "hip hop": "culturally engaged, values authenticity",
        "rap": "values self-expression, competitive spirit",
        "rock": "independent, values tradition and rebellion",
        "indie": "creative, values uniqueness, open to new experiences",
        "electronic": "forward-thinking, tech-inclined, likes complexity",
        "jazz": "sophisticated, analytical, values improvisation",
        "classical": "structured thinker, values discipline and beauty",
        "country": "values storytelling, community, and authenticity",
        "r&b": "emotionally expressive, values connection",
        "pop": "social, optimistic, mainstream-aware",
        "metal": "intense, detail-oriented, values technical skill",
        "punk": "anti-establishment, values DIY and directness",
        "folk": "thoughtful, values simplicity and storytelling",
        "latin": "social, values rhythm and celebration",
        "ambient": "introspective, values calm and focus",
        "lo-fi": "creative worker, values focus and atmosphere",
    }
    
    for genre in genres[:8]:
        for key, trait in genre_traits.items():
            if key in genre:
                traits.append(trait)
                break
    
    # Playlist naming patterns
    playlist_names = " ".join(analysis.get("playlists", [])).lower()
    if any(w in playlist_names for w in ["work", "focus", "study", "coding", "productive"]):
        traits.append("uses music for focus/productivity")
    if any(w in playlist_names for w in ["workout", "gym", "run", "energy"]):
        traits.append("fitness-oriented")
    if any(w in playlist_names for w in ["chill", "relax", "sleep", "calm"]):
        traits.append("values downtime and recovery")
    if any(w in playlist_names for w in ["party", "hype", "pregame"]):
        traits.append("social/extroverted side")
    
    # Deduplicate
    return list(dict.fromkeys(traits))[:8]

def import_spotify(user_id):
    """Main import function."""
    token = get_spotify_token()
    
    if not token:
        return {
            "source": "spotify",
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "error": "No Spotify credentials. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.",
            "setup_help": "Create an app at https://developer.spotify.com/dashboard",
        }
    
    analysis = analyze_user_playlists(user_id, token)
    
    if not analysis:
        return {
            "source": "spotify",
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "error": f"Could not fetch playlists for user '{user_id}'. Profile may be private.",
        }
    
    personality_traits = infer_personality_from_music(analysis)
    
    return {
        "source": "spotify",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "insights": {
            "interests": analysis["top_genres"][:10],
            "personality_traits": personality_traits,
            "top_artists": analysis["top_artists"][:10],
            "top_genres": analysis["top_genres"][:10],
            "music_engagement": f"{analysis['playlist_count']} playlists, {analysis['total_tracks']} total tracks",
            "communication_style": "",  # Music doesn't tell us this directly
            "tone": "",
        },
        "confidence": min(analysis["total_tracks"] / 200, 1.0),
        "items_processed": analysis["total_tracks"],
    }

if __name__ == "__main__":
    os.makedirs(IMPORT_DIR, exist_ok=True)
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: spotify.py <spotify_user_id>"}))
        sys.exit(1)
    
    user_id = sys.argv[1]
    result = import_spotify(user_id)
    
    output_path = os.path.join(IMPORT_DIR, "spotify.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(json.dumps(result, indent=2))
