---
name: suno-music
description: "Generate AI music and songs via Suno. Use when: (1) user asks to create, make, or generate a song or music, (2) user wants lyrics written, (3) user wants a song for an occasion (birthday, celebration, joke, roast, lullaby, etc). Requires gcui-art/suno-api self-hosted server. Supports custom lyrics, style/genre tags, instrumental tracks, and Suno v5."
---

# Suno Music Generation

Generate songs via a local [gcui-art/suno-api](https://github.com/gcui-art/suno-api) server.

## Setup

1. Clone and install: `git clone https://github.com/gcui-art/suno-api && cd suno-api && npm install && npm run build`
2. Create `.env` with your Suno cookie and optional 2Captcha key (see repo README)
3. Start server: `PORT=3100 npm start` (or create a LaunchAgent/systemd service)
4. Verify: `curl http://localhost:3100/api/get_limit`

Set `SUNO_API_URL` env var if not running on `http://localhost:3100`.

## Quick Generate (simple mode)

For casual requests ("make a song about X") — Suno writes the lyrics:

```bash
scripts/suno.sh generate --prompt "DESCRIPTION" --wait
```

## Custom Generate (full control)

For specific lyrics and style:

```bash
scripts/suno.sh custom --prompt "LYRICS" --style "GENRE TAGS" --title "TITLE" --wait
```

Add `--instrumental` for no vocals. Add `--negative-tags "TAGS"` to exclude styles.

## Generate Lyrics First

When user provides a theme but not lyrics — generate, review, then create:

```bash
scripts/suno.sh lyrics --prompt "THEME"
```

## Check Status / Credits

```bash
scripts/suno.sh status --ids "ID1,ID2"
scripts/suno.sh credits
```

## Download Audio

```bash
scripts/suno.sh download --url "AUDIO_URL" --out "/path/to/file.mp3"
```

## Workflow

1. **Vague idea** → `generate` (Suno writes lyrics from description)
2. **Specific vision** → write lyrics, then `custom` with style tags and title
3. **Review first** → `lyrics` to generate, show user, edit, then `custom`
4. Always use `--wait` — blocks until audio URLs are ready (~60-120s)
5. Each generation creates **2 song variations**
6. Download audio and send via message tool (as attachment)
7. Songs appear in the user's Suno library/playlists

## Style Tags Examples

- `pop, upbeat, happy, female vocals`
- `country, acoustic guitar, male vocals, storytelling`
- `hip hop, trap beats, autotuned vocals`
- `classical, orchestral, cinematic`
- `rock, electric guitar, energetic, anthem`
- `thrash metal, aggressive riffs, double bass drums, distorted guitar`
- `jazz, smooth, saxophone, lounge`
- `lullaby, soft, gentle, music box`
- `folk, banjo, americana, warm`
- `edm, electronic, dance, synth`
- `r&b, soulful, smooth, groovy`

## Cookie Refresh

If auth errors occur, refresh the Suno cookie:
1. Open suno.com/create in browser → DevTools (F12) → Network tab
2. Refresh page → find request with `?__clerk_api_version`
3. Copy the Cookie header value → update `.env` → restart server

## Notes

- Default model: Suno v5 (`chirp-crow`); override via `--model` flag
- Each generation uses credits (~10 per song pair)
- Audio files are MP3, typically 2-4 min
- 2Captcha key optional but recommended for long-term stability
