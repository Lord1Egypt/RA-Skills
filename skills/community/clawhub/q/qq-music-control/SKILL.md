---
name: qq-music-control
version: 1.3.0
description: "Community-maintained browser automation for QQ Music's web player (y.qq.com). Supports play/pause/next/prev, search songs/artists/albums, play liked songs, random play, like/unlike, playlist management (list/create/add-to), and browser-target discovery across platforms."
metadata:
  openclaw:
    emoji: "🎵"
---

# QQ Music Browser Control

Use this community-maintained skill to control QQ Music's web player (y.qq.com) through a browser DevTools/CDP endpoint.

## Security model

This skill uses the Chrome DevTools Protocol (CDP) to automate QQ Music's web UI. It is **not affiliated with Tencent or QQ Music**. CDP is a powerful protocol — the following safeguards are in place to minimize its blast radius:

### Domain whitelist

The script **only operates on `y.qq.com` tabs**. Two layers of domain validation are enforced:

1. **Target selection**: When choosing which tab to connect to, the script checks the tab URL against an allow-list (`y.qq.com`). Non-matching tabs are rejected.
2. **Pre-evaluate re-check**: Immediately before every `Runtime.evaluate` call, the script queries `location.hostname` of the connected page and verifies it is still `y.qq.com`. If the page has navigated to a different domain since connection, the call is rejected with an error.

This prevents the script from reading or manipulating content on other websites (email, banking, etc.), even if the page navigates away after the initial connection.

### Isolated browser profile (recommended)

We **strongly recommend** launching the browser with `--user-data-dir` pointing to a dedicated directory:

```bash
chrome --remote-debugging-port=9222 --user-data-dir=/path/to/qq-music-profile
```

This ensures:
- The CDP-enabled browser instance has **no access** to your main browser's cookies, passwords, or sessions
- Only QQ Music login state exists in this profile
- Closing this browser leaves your main browser unaffected

### Single-port binding

The script probes **only one port** by default — read from `.cdp-port` cache file, or falling back to `9222`. It does not scan port ranges. This minimizes the chance of accidentally connecting to unrelated DevTools endpoints.

### No SSRF policy changes required

This skill does **not** use OpenClaw's built-in `browser` tool. It connects to CDP directly via WebSocket from a local Node.js script. No SSRF policy relaxation is needed in OpenClaw's configuration.

### What CDP can and cannot do

| Capability | In scope? | Notes |
|---|---|---|
| Execute JS in y.qq.com tabs | ✅ | Core functionality — clicks buttons, reads DOM. Domain re-checked before every call. |
| Execute JS in non-y.qq.com tabs | ❌ | Blocked by domain whitelist |
| Read cookies from y.qq.com | ⚠️ | Technically possible via CDP, but the script never does this |
| Access other browser tabs | ⚠️ | CDP can list all tabs, but the script only interacts with y.qq.com tabs |
| Access filesystem | ❌ | CDP `Runtime.evaluate` runs in page sandbox |
| Install extensions | ❌ | The script does not use `Target.createBrowserContext` or extension APIs |

### Honest limitations

- CDP inherently has access to **all tabs** in the connected browser. The domain whitelist is an application-level guard, not a browser-level sandbox. Using `--user-data-dir` for isolation is the strongest mitigation.
- The script runs `Runtime.evaluate` with arbitrary JavaScript on QQ Music pages. This is equivalent to using the browser's DevTools console on that page.
- This is a community automation tool for a music player, not a security-critical application. Use common sense: don't run it on a machine you don't trust.

## What it supports

- Cross-platform: Windows, macOS, Linux
- Cross-browser: Chrome, Chromium, Edge, Brave, Arc, or any browser exposing a DevTools/CDP endpoint
- Transport: play, pause, toggle, next, previous
- Search & play: songs, artists, albums
- Liked songs: play all, play random, like/unlike current track
- Playlists: list created playlists, create new playlists, add current song to a playlist, play a playlist by ID
- Mode control: list loop, single loop, shuffle, sequential
- Status: current track, artist, time, play state
- Screenshot capture

## Requirements

- **Node.js 18+** (uses built-in `fetch` and `WebSocket`)
- A Chromium-based browser with remote debugging enabled (see setup below)
- A QQ Music account logged in at `y.qq.com` (needed for liked songs, playlists, and like/unlike)

## Setup guide (for Agents)

This skill connects to a browser via CDP. The Agent needs to:
1. Discover the CDP port
2. Cache it for subsequent calls
3. Ensure QQ Music is open and logged in

### Step 1: Discover and cache the CDP port

Run the built-in `browser status` tool to get the current `cdpPort`, then write it to `.cdp-port`:

```
browser status → read cdpPort from response (e.g. 19011)
Write the port number to: <skill-directory>/.cdp-port
```

The `.cdp-port` file should contain **only** the port number, nothing else. Example content: `19011`

### Step 2: Verify the connection

```bash
node qq-music-ctl.js doctor
```

Check that `status` is `"ready"`. If `status` is `"connected_no_qq_music_tabs"`, open QQ Music first via `node qq-music-ctl.js init`. If `status` is `"no_endpoint"`, the cached port may be stale — go back to Step 1.

### Step 3: Ensure QQ Music is open and logged in

The user must have logged in to `y.qq.com` in the browser at least once. If there are no QQ Music tabs:

```bash
node qq-music-ctl.js init
```

This opens `https://y.qq.com/` in a new tab. The user may need to log in manually the first time.

> **Note:** This skill does NOT require any OpenClaw SSRF policy changes. It connects to CDP directly, not through OpenClaw's browser tool.

### Connection failure recovery

If any command fails with "No DevTools endpoint found":
1. Re-run `browser status` to get the current `cdpPort`
2. Overwrite `.cdp-port` with the new port number
3. Retry the command


## Controller script

All actions go through the bundled script:

```bash
node qq-music-ctl.js <action> [args...]
```

All output is JSON on stdout. Exit code 0 = success, 1 = error.

### CDP port discovery

The script resolves the CDP port from:

1. **`.cdp-port` file** — a single-line file in the same directory as `qq-music-ctl.js`, containing just the port number (e.g. `19011`).
2. **Fallback `9222`** — the Chrome documentation default.

All connections are restricted to `127.0.0.1`. Remote endpoints are not supported.

> **For OpenClaw Agents:** Run `browser status` (built-in tool) → read `cdpPort` from the response → write it to `.cdp-port`. The script will then use it automatically on every subsequent call. If a command fails with "No DevTools endpoint found", re-run `browser status`, update `.cdp-port`, and retry.

## Action reference

### Playback control

| Action | Description |
|---|---|
| `play` | Resume playback (idempotent) |
| `pause` | Pause playback (idempotent) |
| `toggle` | Toggle play/pause |
| `next` | Next track |
| `prev` | Previous track |
| `status` | Current track, artist, time, duration, play state |

### Search & play

| Action | Description |
|---|---|
| `search <keyword>` | Search for a song and play best match |
| `search-artist <name>` | Search for an artist and open their page |
| `play-artist-all-songs <name>` | Play all songs by an artist |
| `search-album <name>` | Search for an album and play it |

### Liked songs

| Action | Description |
|---|---|
| `play-liked` | Play all liked songs (clicks "播放全部") |
| `play-liked-random` | Randomly play one liked song from the visible page |
| `like` | Like current song (idempotent; returns `already_liked` if already liked) |
| `unlike` | Unlike current song (idempotent; returns `already_unliked` if not liked) |

### Playlists

| Action | Description |
|---|---|
| `list-playlists` | List all created playlists with name, song count, and numeric ID |
| `create-playlist <name>` | Create a new playlist (max 20 characters) |
| `add-to-playlist <name>` | Add the currently playing song to a playlist by name |
| `play-playlist <id>` | Play a playlist by its numeric ID |

### Play mode

| Action | Description |
|---|---|
| `mode` | Show current play mode |
| `mode list` | Set to list loop (列表循环) |
| `mode single` | Set to single loop (单曲循环) |
| `mode random` | Set to shuffle (随机播放) |
| `mode order` | Set to sequential (顺序循环) |

### Utility

| Action | Description |
|---|---|
| `screenshot [path]` | Capture a screenshot of the QQ Music tab |
| `tabs` | List all detectable browser tabs |
| `init` | Open QQ Music if no tab exists |
| `doctor` | Full environment diagnostic: port config, endpoint status, QQ Music tabs |

## How it works

1. **Endpoint discovery**: The script reads the CDP port from `.cdp-port` (or falls back to `9222`), then probes `127.0.0.1:<port>` for a DevTools HTTP endpoint (`/json/version` + `/json/list`).
2. **Tab selection**: Player-tab (`/player` URL) is preferred for transport controls (play/pause/next/prev/status). A separate browse-tab is used for search, navigation, and playlist operations.
3. **DOM automation**: All interactions use `Runtime.evaluate` over CDP to run JavaScript in the page context. No Puppeteer or Playwright dependency.
4. **No external dependencies**: The script is a single file using only Node.js built-ins (`fs`, `path`, `WebSocket`, `fetch`). No `npm install` needed.
5. **Domain re-check**: Before every `Runtime.evaluate` call, the script verifies the page's `location.hostname` is still on `y.qq.com`. If the page has navigated away, the call is rejected with an error.

## Selection rules

- Prefer the player tab for transport controls.
- Prefer the browse tab for search and playlist discovery.
- If there is no QQ Music tab, `init` opens a blank tab and navigates to `https://y.qq.com/`.
- For song search, the first exact or containing title match wins; otherwise the first visible result is played.
- For liked songs, random play picks from the currently visible page (~10 songs; the web version does not expose all liked songs without scrolling).
- For `add-to-playlist`, if a newly created playlist is not yet visible in the player's menu, the player page is automatically reloaded to refresh the cache and retry.
- `like` and `unlike` are idempotent and report the current state.
- `create-playlist` accepts names up to 20 characters (QQ Music web limit).

## Limitations

- The QQ Music web version shows at most ~10 liked songs per page. `play-liked` uses the "播放全部" button which queues all liked songs in the player, but `play-liked-random` can only pick from the visible ~10.
- System audio volume control is out of scope (OS-level, not browser-controlled).
- Some features (like VIP-only songs) depend on the user's QQ Music subscription.
- The skill does not handle QQ Music login; the user must log in manually first.

## Troubleshooting

- **"No DevTools endpoint found"**: The cached port in `.cdp-port` may be stale, or no browser is running with remote debugging. Re-run `browser status`, update `.cdp-port`, and retry. Run `node qq-music-ctl.js doctor` for detailed diagnostics.
- **Port changed after browser restart**: Delete `.cdp-port`, re-query via `browser status`, and write the new port.
- **"Player not found"**: Play a song first (via `search` or `play-liked`) to make the player tab appear.
- **Timeouts**: Increase `QQ_MUSIC_PAGE_WAIT_MS` for slow connections, or `QQ_MUSIC_PROBE_TIMEOUT_MS` for slow endpoint discovery.
- **"CDP connection closed"**: The page may have navigated or crashed. Retry the command.

## Notes

- The skill does not assume a specific browser brand or OS.
- The skill does not hardcode any personal paths, usernames, tokens, or port numbers.
- The `.cdp-port` file is a local cache and should be added to `.gitignore`. It is not part of the published skill.
- If the browser exposes multiple DevTools endpoints, the controller probes the configured port and prefers the one with QQ Music tabs.

## Disclaimer

This is a **community-maintained** tool for personal learning and research. It automates the QQ Music web UI through a user's own browser — equivalent to manual DevTools console usage. It is not an official QQ Music/Tencent plugin.

It does not reverse-engineer server APIs, extract music files, or bypass payment restrictions.

Users are responsible for complying with [QQ Music's Terms of Service](https://y.qq.com/). If you receive a takedown notice from the rights holder, stop using this skill immediately.

Open-source, non-commercial, and provided as-is with no warranty.
