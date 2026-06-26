# Skill: spotify-download

Use this skill when the user wants to download MP3 files from a Spotify playlist.

## When to Use

- User asks to download music from Spotify playlist
- User wants to convert Spotify playlist to MP3
- User provides a Spotify playlist URL and wants audio files

## Setup

### Requirements

1. **Python 3.10+** - Required
2. **ffmpeg** - Required for audio conversion
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - Windows: `choco install ffmpeg` or download from https://ffmpeg.org

### Installation Options

**Option 1: uvx (no install needed)**
```bash
uvx spotify-download "https://open.spotify.com/playlist/..."
```

**Option 2: pip install**
```bash
pip install spotify-download
spotify-download "https://open.spotify.com/playlist/..."
```

**Option 3: pipx**
```bash
pipx install spotify-download
spotify-download "https://open.spotify.com/playlist/..."
```

**Option 4: Local development**
```bash
git clone https://github.com/zesong/spotify-download.git
cd spotify-download
pip install -e .
spotify-download "https://open.spotify.com/playlist/..."
```

### Spotify Credentials (Optional)

**Public playlists**: No credentials needed - the tool uses Spotify's embed page to fetch metadata.

**Private playlists** or **more accurate metadata**: Get credentials:
1. Go to https://developer.spotify.com/dashboard
2. Create an app
3. Copy Client ID and Client Secret

Then use either:
```bash
spotify-download "https://..." --client-id "XXX" --client-secret "YYY"
```

Or set environment variables:
```bash
export SPOTIFY_CLIENT_ID="your-client-id"
export SPOTIFY_CLIENT_SECRET="your-client-secret"
spotify-download "https://..."
```

## Usage

### Basic Command

```bash
uvx spotify-download "https://open.spotify.com/playlist/5TFrk1Wdap4jufziW7SyIh"
```

### Common Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output directory | `downloads` |
| `-w, --workers` | Concurrent downloads | `4` |
| `-d, --delay` | Search delay (seconds) | `1.0` |
| `--json-output` | Save playlist JSON path | `<output>/playlist.json` |
| `--skip-export` | Skip export, use existing JSON | - |

### Examples

```bash
# Download to custom directory
uvx spotify-download "https://open.spotify.com/playlist/..." -o ~/Music/my-playlist

# Faster downloads
uvx spotify-download "https://open.spotify.com/playlist/..." -w 8

# Save playlist JSON for later
uvx spotify-download "https://open.spotify.com/playlist/..." --json-output my-playlist.json

# Re-download from saved JSON (skip export)
uvx spotify-download --skip-export --json-output my-playlist.json -o ~/Music

# With credentials for private playlist
uvx spotify-download "https://open.spotify.com/playlist/..." --client-id XXX --client-secret YYY
```

## Output

Files saved to `<output>/music/` as `{Artist} - {Track Name}.mp3`:

```
downloads/
├── playlist.json          # Playlist metadata
└── music/
    ├── Eason Chan - 任我行.mp3
    ├── Mayday - 突然好想你.mp3
    └── ...
```

## Troubleshooting

### "ffmpeg not found"
Install ffmpeg:
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### "Could not find embedded playlist metadata"
Spotify's embed page structure may have changed. Use API credentials:
```bash
spotify-download "https://..." --client-id "your-id" --client-secret "your-secret"
```

### Some tracks fail to download
YouTube search may not find the right match. Re-run the command - it skips already-downloaded tracks.

## Implementation

The tool:
1. **Fetches** playlist metadata from Spotify (embed page for public, API for private)
2. **Searches** YouTube for each track ("{artist} {track name}")
3. **Downloads** best audio match as MP3 (320kbps)
4. **Validates** - skips already-downloaded valid MP3s

## Notes

- Requires ffmpeg for audio conversion to MP3
- Uses yt-dlp for YouTube search/download
- Public playlists work without any Spotify credentials
- Concurrent downloads are supported (default: 4 workers)