# Setup

## Purpose

This skill uses the Spotify Web API through local Python scripts.

## Quick start

From the skill root, run:

```bash
bash scripts/setup.sh
```

That script:

- creates a local `.venv` if needed
- installs Python dependencies from `requirements.txt`
- prints the next auth step

Then authenticate directly with the venv Python:

```bash
.venv/bin/python scripts/spotify_auth.py
```

This avoids relying on shell activation state and is usually safer to copy and paste.

The auth helper opens a browser for Spotify OAuth consent and writes a token file containing the refresh token and access token metadata.

## Required environment

Provide credentials using either standard Spotipy names or explicit Spotify names:

- `SPOTIPY_CLIENT_ID` or `SPOTIFY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET` or `SPOTIFY_CLIENT_SECRET`

Optional path overrides:

- `SPOTIFY_TOKENS_PATH` - path to the token JSON file
- `SPOTIFY_ENV_PATH` - path to a dotenv-style file containing client credentials
- `SPOTIFY_REDIRECT_URI` - override the OAuth redirect URI
- `VENV_DIR` - override the virtual environment location for `scripts/setup.sh`
- `PYTHON_BIN` - override which Python executable `scripts/setup.sh` uses

## Dependencies

Current Python dependencies are listed in `requirements.txt`:

- `spotipy`
- `requests`

## Notes

### Required Spotify OAuth scopes

The skill requests these scopes when you run `scripts/spotify_auth.py` (via `spotify_client.SCOPES`):

- `user-read-playback-state`
- `user-modify-playback-state`
- `user-read-currently-playing`
- `playlist-read-private`  
  (required to read playlists like **the witches are angry**)
- `playlist-read-collaborative`
- `playlist-modify-public`
- `playlist-modify-private`
- `user-top-read`
- `user-read-recently-played`

If you hit `403 Forbidden` when analyzing or reading a playlist, re-run auth to ensure these scopes were granted:

```bash
cd skills/spotify-playlist-curator
.venv/bin/python scripts/spotify_auth.py
```

### Other behavior notes

- Queueing requires an active Spotify device.
- Playlist creation and editing do not require active playback.
- Do not print raw credentials or token values.
