# Install and deploy

## Docker priority path

Deploy the skill to:

- `/home/node/shared/skills/youtube-digest`

This makes the skill visible to all Docker agents if `shared/skills` is already included in skill loading.

## Minimum dependencies

### Debian / Ubuntu

```bash
apt-get update
apt-get install -y yt-dlp ffmpeg
```

If `yt-dlp` is unavailable from apt or too old, use pipx / pip / direct binary install.

### Direct binary install

```bash
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
  -o /usr/local/bin/yt-dlp
chmod +x /usr/local/bin/yt-dlp
```

## Verification

```bash
yt-dlp --version
python3 scripts/fetch_youtube.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --out /tmp/youtube-digest-test
cat /tmp/youtube-digest-test/summary.json
```

## Optional ASR upgrade

Only add this after subtitle-first workflow is stable:

- install Whisper or faster-whisper
- optionally add audio download fallback to the script
- keep the subtitle path as the default because it is cheaper and faster
