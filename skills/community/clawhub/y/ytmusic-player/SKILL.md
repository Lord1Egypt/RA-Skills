---
name: ytmusic
description: Operate YouTube Music via natural language. Search songs, artists, albums, playlists, lyrics, charts, recommendations, and control playback. Browse personal library, manage playlists, rate tracks, and inspect account info. Use this skill whenever the user asks about YouTube Music, wants to play music, manage playlists, search by song or artist name, inspect lyrics, or control playback.
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - uv
      config:
        - .ytmusic/auth.json
    skillKey: ytmusic
    homepage: https://github.com/kadaliao/ytmusic-skill
---

# YouTube Music Skill

Run bundled scripts from the skill root:

- `scripts/helper.py`: search, library, playlists, lyrics, ratings, account
- `scripts/player.py`: playback client and daemon management
- `scripts/player_daemon.py`: persistent Playwright browser daemon
- Runtime state is local to `./.ytmusic/`
- Playback uses a dedicated Playwright-managed browser profile in `./.ytmusic/playwright-profile`

## Workflow

1. If the user gives names instead of IDs, search first.
2. For auth-required actions, run `auth check` first.
3. If auth is missing, switch into auth-guidance mode and do not continue yet.
4. Only after auth succeeds, execute the original command.
5. Format JSON into short tables or lists.

## ID Resolution

Use search to resolve `videoId`, `browseId`, or `playlistId`:

```bash
uv run --with ytmusicapi python scripts/helper.py search "<query>" --type songs --limit 5
uv run --with ytmusicapi python scripts/helper.py search "<query>" --type artists --limit 3
uv run --with ytmusicapi python scripts/helper.py search "<query>" --type albums --limit 3
```

If results are ambiguous, ask the user which one they want.

## Auth

Check auth before `library`, `playlist`, `rate`, `subscribe`, `home`, `history`, `taste`, `upload`, or `auth account`:

```bash
uv run --with ytmusicapi python scripts/helper.py auth check
```

If auth is missing, do not continue with the requested action yet.

You must explicitly guide the user to provide one of these:
- a Cookie string copied from a logged-in `music.youtube.com` request
- a cookies JSON export file path

This is a hard rule:
- Do not just say "auth missing"
- Do not stop after showing a shell error
- Do not ask a vague question like "please log in first"
- Do ask for the exact artifact you need next: Cookie string or cookies JSON file path
- Mirror the user's language when possible; if the user's language is unclear, default to concise English
- Treat the English templates below as defaults and translate or adapt them to match the user's language

Use this flow:
1. Tell the user authentication is required before you can access their library, playlists, account, uploads, or full playback.
2. Ask them to open `music.youtube.com` in a logged-in browser.
3. Offer two options:
   - Cookie string: open DevTools, Network, filter `/browse`, reload, open any matching request, copy the `Cookie` header value, send it back
   - Cookies JSON: export cookies for `music.youtube.com` with a cookie extension and send the file path back
4. When the user replies with either the cookie string or a JSON file path, run `auth setup`.
5. Retry the original command after `auth setup` succeeds.

Preferred default user-facing wording:

```text
You need to sign in to YouTube Music before I can access your library, playlists, account, uploads, or full playback.

Please send me one of these:
1. A Cookie string
2. A cookies JSON file path
```

Cookie string instructions:

```text
Open a logged-in music.youtube.com page
Open DevTools -> Network
Filter /browse and reload the page
Open any matching request
Copy the Cookie request header value
Send the full Cookie string back to me
```

Cookies JSON instructions:

```text
Use a cookie export extension such as Cookie-Editor on music.youtube.com
Export cookies as JSON
Save the exported file locally
Send me the file path
```

Setup commands:

```bash
uv run --with ytmusicapi python scripts/helper.py auth setup --cookie '<cookie string>'
uv run --with ytmusicapi python scripts/helper.py auth setup --cookies-file /path/to/cookies.json
```

## Common Commands

```bash
uv run --with ytmusicapi python scripts/helper.py search "<query>" [--type songs|artists|albums|playlists|videos]
uv run --with ytmusicapi python scripts/helper.py library playlists
uv run --with ytmusicapi python scripts/helper.py playlist get <playlistId>
uv run --with ytmusicapi python scripts/helper.py playlist create --title "<name>"
uv run --with ytmusicapi python scripts/helper.py playlist add <playlistId> <videoId...>
uv run --with ytmusicapi python scripts/helper.py lyrics <videoId>
uv run --with ytmusicapi python scripts/helper.py related <videoId>
uv run --with ytmusicapi python scripts/helper.py rate <videoId> LIKE|DISLIKE|INDIFFERENT
uv run --with ytmusicapi python scripts/helper.py charts [--country CN|US|KR|JP|ZZ]
```

Full command reference: `references/commands.md`

## Playback

Playback runs through a persistent Playwright browser daemon. The first playback command auto-starts a dedicated browser window and reuses it for later `open`, `play`, `pause`, `next`, `prev`, `seek`, `volume`, and `status` commands.

```bash
uv run --with playwright python scripts/player.py daemon-start
uv run --with playwright python scripts/player.py open <videoId>
uv run --with playwright python scripts/player.py play
uv run --with playwright python scripts/player.py pause
uv run --with playwright python scripts/player.py next
uv run --with playwright python scripts/player.py prev
uv run --with playwright python scripts/player.py status
uv run --with playwright python scripts/player.py volume <0-100>
uv run --with playwright python scripts/player.py seek <seconds>
uv run --with playwright python scripts/player.py daemon-status
uv run --with playwright python scripts/player.py daemon-stop
```

Important behavior:
- The daemon launches a dedicated persistent browser profile in `./.ytmusic/playwright-profile`
- On first launch, the user may need to sign in to `music.youtube.com` in that browser window
- The user does not need to start Chrome or open a debugging port manually
- If `open <videoId>` loads the page but playback is still paused, autoplay was likely blocked and the user may need to click play once in the daemon-managed window
- `daemon-status` checks whether the background browser is alive without starting a new one

If playback commands fail, first verify:
- The daemon-managed browser window is still open
- The user is signed in at `music.youtube.com` in that browser window if the requested track requires it
- The requested song page can actually play in that browser session
- `./.ytmusic/player-daemon.log` does not show a launch or Playwright error

## Output

- Search results: numbered table with title, artist, album, duration
- Playlist tracks: numbered list with title, artist, album
- Lyrics: print plain text
- Playback: `▶ {title} — {artist} ({position} / {duration})`
- Errors: state cause and next action

After success, suggest one natural next step such as play, add to playlist, show lyrics, or fetch related tracks.
