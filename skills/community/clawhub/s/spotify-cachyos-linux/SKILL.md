---
name: spotify-linux
description: "Control Spotify on Linux via MPRIS DBus. Use when: launching Spotify from command line, playing/pausing/skipping tracks, searching songs and switching playback to a specific track, any Spotify playback control task on Linux."
allowed-tools:
  - Bash
  - WebSearch
---

# Spotify Linux Control

Control Spotify desktop client on Linux through MPRIS DBus — no browser automation, no simulated clicks.

## ⚠️ Scope and Warnings

This skill controls the **real Spotify client on the local desktop**. Every command takes effect immediately:

- `OpenUri` starts the track playing right away, at the current volume, and replaces the current playback context. Confirm the track/album/playlist URI matches what the user asked for before calling it.
- Playback state and volume changes are live — they alter what the user is currently hearing.
- Launching starts Spotify as a desktop background process managed by a systemd `--user` unit named `spotify-skill-launch`; §9 shows how to inspect and stop it.
- The launcher only ever uses the invoking user's own graphical-session credentials, and refuses to run with elevated privileges.

Use this skill only on your own desktop session.

## Prerequisites

- Spotify desktop client installed. The launcher auto-detects any of these install methods:
  - native package providing a `spotify` executable (Arch/AUR, Debian/Ubuntu .deb)
  - `spotify-launcher` (the community launcher, common on Fedora)
  - Flatpak: `flatpak install com.spotify.Client`
  - Snap: `snap install spotify`
- An active X11 session (or Wayland with XWayland) for the invoking user
- `dbus-send` (bundled with DBus, always present); `python3` and a Chromium-based browser are needed only for the fallback search (§2a)
- `systemd --user` manager (present in every desktop session on systemd-based distributions)

## Declared Scope

Everything this skill does stays inside the invoking user's own desktop session. This list is the complete declared footprint — if a task appears to need more, stop and tell the user instead of improvising.

- **Tools declared:** `Bash` and `WebSearch` (frontmatter `allowed-tools`). Nothing else is required.
- **Commands used:** `dbus-send` (MPRIS control and property reads), `systemctl --user` / `systemd-run --user` (start, inspect and stop the `spotify-skill-launch` unit), `pgrep` (process check), `curl` inside the launcher (reachability probe only, `-o /dev/null`), and — only for the §2a fallback search — a Chromium-based browser in headless mode plus `python3` to parse the dumped DOM.
- **Privileges:** the whole skill runs as the invoking desktop user. The launcher aborts if the effective user is not the session owner; no step requests elevation.
- **Commands never used:** no package installation, no configuration-file edits, no remote payload download or execution, no reads of other users' data.
- **Sensitive data:** none. The §2a fallback renders Spotify's **public** search page from a throwaway browser profile it creates itself — no cookies, saved logins, or browser session data are read or copied, and the throwaway profile is deleted on exit.
- **Files written:** only the §2a throwaway profile and DOM dump (both inside one `mktemp -d` directory, removed by a `trap`), plus the launcher's own systemd `--user` unit state. Playback control itself only sends messages on the session bus.

## Quick Start

```bash
# Pause/Play toggle
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause

# Next/Previous
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous
```

## 1. Launch Spotify (Managed Background Process)

Use the bundled launcher — it resolves the session credentials and proxy settings safely and hands Spotify to the user's systemd manager, so the process is tracked and can be stopped cleanly. Its complete source ships at `scripts/launch_spotify.sh` in this package.

**Always call it by absolute path.** The launcher ships at `scripts/launch_spotify.sh` relative to the skill directory — the directory that holds this `SKILL.md`. An agent's working directory is usually not the skill directory, so a relative `scripts/launch_spotify.sh` fails with "No such file or directory". Resolve the skill directory once and reuse it:

```bash
# <skill-dir> is the absolute path of the directory holding this SKILL.md;
# the runtime that loaded the skill knows it (DSH reports the loaded skill's path).
SKILL_DIR="<skill-dir>"

"$SKILL_DIR/scripts/launch_spotify.sh"             # start (or confirm it is already running)
"$SKILL_DIR/scripts/launch_spotify.sh" --check     # diagnose without launching anything
"$SKILL_DIR/scripts/launch_spotify.sh" --stop      # stop the managed instance
```

If the runtime does not report a path for the loaded skill, ask the user for the skill directory. Do not search the filesystem for the launcher: a search can silently pick a stale copy of the package, and installing skills in several locations is common.

What the launcher does:

1. Uses `$DISPLAY` and `$XAUTHORITY` from the environment when present, after validating them.
2. Otherwise looks for credentials in the invoking user's own session only: `~/.Xauthority`, then Xauthority files under `$XDG_RUNTIME_DIR`, then the user's own Xwayland/Xorg processes. Every candidate must be a regular file owned by the invoking user with no group/other access, or it is rejected.
3. Resolves proxy settings from the calling environment, falling back to KDE's `~/.config/kioslaverc`, and forwards them into the unit. A `systemd --user` unit inherits the systemd user manager's environment, which has no proxy variables — so without this step Spotify would take the direct route instead of the session's configured one.
4. Launches Spotify as a transient `systemd-run --user` unit named `spotify-skill-launch` — independent of the agent process tree, visible in `systemctl --user`, stoppable on demand.
5. Waits for DBus registration (~5-8 seconds), then reports what the client actually holds, e.g.:

```
Spotify ready (took 3s, proxy: kioslaverc)
  state: Playing, track: 克卜勒
```

Read that report. `state: Stopped, no track loaded` means the client registered but has nothing to play — it is signed out or still initializing, and **every MPRIS command will answer successfully while changing nothing**. Confirm sign-in/network and re-launch before issuing control commands.

## 2. Search and Play a Track

MPRIS has no search method. The workflow: web-search → extract Spotify track ID → `OpenUri`. If web search can't find the track (new releases are rarely indexed anywhere), fall back to §2a below.

```bash
# Step 1: Search the web for the track to get its Spotify URL
# Example search: "李白 李荣浩 spotify"
# Extract the track ID from URL like: https://open.spotify.com/track/0aLtafjN146xAdZeqYN8Ho

# Step 2: Call OpenUri with the spotify:track:<ID> URI
TRACK_ID="0aLtafjN146xAdZeqYN8Ho"
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.mpris.MediaPlayer2.Player.OpenUri \
  string:"spotify:track:$TRACK_ID"
```

> ⚠️ **Immediate playback:** `OpenUri` makes Spotify load the track and start playing instantly, at the current volume, replacing the current playback context. Confirm the URI first — no additional `Play` call is needed.

URL types supported:
- `spotify:track:<id>` — single track
- `spotify:album:<id>` — full album
- `spotify:playlist:<id>` — playlist
- `spotify:artist:<id>` — artist page

### 2a. When Web Search Fails: Read the Public Spotify Search Page

New releases and region-locked tracks are often missing from search engines and third-party indexes (MusicBrainz, Deezer, song.link lag months). Spotify's **public** search page still returns them, and it answers **without any login** — so read it from a throwaway browser profile. Never point the browser at the user's real profile: no cookies, saved logins or session state are needed, read, or copied.

Any Chromium-based browser works (Google Chrome, Chromium, Brave).

```bash
# Run this whole block as ONE shell invocation: the throwaway profile and the
# DOM dump are removed together when the shell exits.
WORK="$(mktemp -d)"                 # random path; mktemp -d creates it 0700 already
trap 'rm -r -- "$WORK"' EXIT HUP INT TERM

# Chrome does not pick up the HTTP_PROXY/HTTPS_PROXY variables a shell exports:
# without this flag the page renders with ZERO results (measured: 165 KB, no
# /track/ links) instead of failing loudly. Forward the session proxy.
PROXY="${https_proxy:-${HTTPS_PROXY:-${http_proxy:-${HTTP_PROXY:-}}}}"
PROXY_ARG=(); [ -n "$PROXY" ] && PROXY_ARG=("--proxy-server=$PROXY")

# 1. Render the public search page. The query must be percent-encoded
#    (e.g. 王菲 主角 → %E7%8E%8B%E8%8F%B2%20%E4%B8%BB%E8%A7%92).
#    --user-data-dir is a fresh empty directory: nothing of the user's is read.
#    `timeout 60` keeps a wedged render from hanging the task.
render() {
  timeout 60 google-chrome-stable --headless=new --user-data-dir="$WORK" \
    --no-first-run --no-default-browser-check --disable-gpu "${PROXY_ARG[@]}" \
    --virtual-time-budget=8000 --dump-dom \
    "https://open.spotify.com/search/<encoded-query>" > "$WORK/dom.html" 2>/dev/null
}

render
# No /track/ links covers every failure mode at once: Chrome error page (never
# loaded), proxy/network problem (loads but fetches nothing), login wall, or a
# query with no match. Retry once before concluding anything.
if ! grep -q 'href="/track/' "$WORK/dom.html"; then
  echo "no results on first render, retrying once" >&2
  sleep 2
  render
fi
if ! grep -q 'href="/track/' "$WORK/dom.html"; then
  echo "NO RESULTS: the page returned no /track/ links. Do NOT report 'track not found' — check connectivity/proxy first, then ask the user to paste the Spotify link." >&2
fi

# 2. Pair every track link with the result card that carries it, in page order.
python3 - "$WORK/dom.html" <<'PY'
import re, sys
h = open(sys.argv[1], encoding='utf-8', errors='replace').read()
seen = set()
for t in re.finditer(r'href="/track/([A-Za-z0-9]+)"', h):
    if t.group(1) in seen:
        continue
    seen.add(t.group(1))
    before = h[max(0, t.start() - 900):t.start()]
    label = re.findall(r'aria-label="([^"]{1,120})"', before)           # song rows
    title = re.findall(r'<a[^>]*title="([^"]{1,120})"[^>]*$', before)   # top-result card
    print(t.group(1), '|', label[-1] if label else (title[-1] if title else '?'))
PY
```

The output is `<track-id> | <card text>`, in result order. Verified output (2026-09-21):

```
0aLtafjN146xAdZeqYN8Ho   | 李白
2Foc5Q5nqNiosCNqttzHof   | 播放 Daft Punk, Pharrell Williams, Nile Rodgers 的 Get Lucky (Radio Edit) [...]
```

The card wording follows the user's UI language — Chinese `播放 <artist> 的 <title>`, English `Play <title> by <artist>` — so match on the title and artist text, not on the fixed words. Confirm the candidate matches what the user asked for, then pass `spotify:track:<id>` to `OpenUri`.

- One lookup takes ~10-25 s. `--virtual-time-budget=8000` is enough; measured here: 8 s budget ≈ 8-11 s wall clock, 25 s budget ≈ 25 s — identical results.
- **The proxy must be forwarded.** Measured on this machine with a working session proxy: without `--proxy-server` the same query returned 0 track links from a 165 KB page; with it, 4 track links from a 709 KB page. Absence of the flag looks like "no such track" and is not.
- Because a silent empty page is the main failure mode, **treat zero `/track/` links as "could not resolve", not as "not found"** — say so, and offer the paste-the-link route.
- Results follow the **request's exit IP region**, not the user's account region, so they can differ from what the user sees in the client.
- Chrome prints harmless noise on stderr (crashpad `settings.dat`, NSS, GCM registration, occasional SSL handshake retries). Judge success by the parsed output, not by stderr.
- Spotify's front end changes; if parsing breaks, re-run without the `trap` and inspect the markup around `href="/track/` in the dumped DOM.
- Nothing is authenticated here, so there is no session to leak.

## 3. Read Playback State

```bash
# Current play/pause status
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Get \
  string:org.mpris.MediaPlayer2.Player string:PlaybackStatus

# Current track metadata (title, artist, album, URL, art, etc.)
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Get \
  string:org.mpris.MediaPlayer2.Player string:Metadata
```

Key metadata fields in returned dict:
- `xesam:title` — track title
- `xesam:artist` — artist (array)
- `xesam:album` — album name
- `xesam:url` — Spotify web URL
- `mpris:trackid` — internal track ID path
- `mpris:artUrl` — album art URL

## 4. Volume Control

```bash
# Set volume (0.0 to 1.0)
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Set \
  string:org.mpris.MediaPlayer2.Player string:Volume \
  variant:double:0.5

# Read current volume
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Get \
  string:org.mpris.MediaPlayer2.Player string:Volume
```

## 5. Check If Spotify Is Running

```bash
# Quick: process check
pgrep -a spotify

# Reliable: DBus check (confirms fully initialized)
dbus-send --session --dest=org.freedesktop.DBus --type=method_call --print-reply \
  /org/freedesktop/DBus org.freedesktop.DBus.ListNames 2>/dev/null | grep spotify
```

DBus check is preferred because it confirms the client is fully initialized and ready for commands; process check alone can give false positives when Spotify is still starting up.

## 6. Play Daily Recommendation Playlists

"今日推荐" / "每日推荐" maps to Spotify's Daily Mix series — personalized playlists updated daily. Other recommendation playlists include Discover Weekly and Release Radar.

```bash
# Daily Mix 1-6 (personalized, content varies per user/region)
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.mpris.MediaPlayer2.Player.OpenUri \
  string:"spotify:playlist:37i9dQZF1E37SmkLuYDrmF"  # Daily Mix 1 (personalized — content differs per account)

# Discover Weekly (每周新发现)
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.mpris.MediaPlayer2.Player.OpenUri \
  string:"spotify:playlist:37i9dQZEVXcJZyENOWUFo7"

# Release Radar (新歌雷达)
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.mpris.MediaPlayer2.Player.OpenUri \
  string:"spotify:playlist:37i9dQZEVXbhM8yqJpzH4B"
```

Note: Daily Mix URIs with `37i9dQZF1E37` prefix are personalized — the same URI shows different content for each user. Content displayed in search results may differ from what the user hears.

## 7. Verify a Command Took Effect

MPRIS methods return success even when the client ignores them, so after a
playback command, read the state back:

```bash
# Playback status + current title, one shot
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Get \
  string:org.mpris.MediaPlayer2.Player string:PlaybackStatus
dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify \
  /org/mpris/MediaPlayer2 \
  org.freedesktop.DBus.Properties.Get \
  string:org.mpris.MediaPlayer2.Player string:Metadata
```

- After `Play`/`PlayPause`, `PlaybackStatus` must change.
- After `Next`, `xesam:title` must change.
- `Previous` restarts the current track when more than ~3s have elapsed and
  only then steps back on a second call — an unchanged title there is normal
  Spotify behaviour, not a failed command.
- If nothing changes at all, the client has no track loaded — see Troubleshooting.

## 8. Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `scripts/launch_spotify.sh: No such file or directory` | A relative path was used, or the wrong copy of the package was picked. Resolve `SKILL_DIR` as §1 describes (the directory holding this `SKILL.md`) and call the launcher by absolute path; do not fall back to a filesystem search. |
| Commands return success but nothing happens | The client has no track loaded (signed out or still initializing). Run `--check`; if it reports `no track loaded`, run `--stop` then launch again and re-read the state before sending more commands. |
| Music stops when the agent session restarts | Spotify was started as a plain child of the agent, so it lives in the agent's cgroup and is killed with it. Use the launcher: its systemd `--user` unit is independent of the agent. |
| `WARNING: Spotify process running but DBus not registered after 15s` | The client failed to start. Check `systemctl --user status spotify-skill-launch` and `journalctl --user -u spotify-skill-launch`. |
| `--check` reports `cannot reach accounts.spotify.com` | No track loaded: no working network route (proxy missing or down) — fix connectivity before launching. Track loaded and playing: probe false negative (the probe is a heuristic), ignore it — `--check` says so explicitly in that case. |
| Web search finds no Spotify link for the track | New release not yet indexed by search engines or third-party sources. Read Spotify's public search page instead (§2a) — it needs no login and no browser profile; if it returns no `/track/` links, ask the user to paste the link. |

## 9. Lifecycle: What Is Left Running

Launching starts Spotify as a transient `systemd --user` unit named `spotify-skill-launch`. It deliberately outlives the agent process so playback is not cut off when the agent session ends, and it stays visible and stoppable at any time:

```bash
systemctl --user status spotify-skill-launch     # inspect the managed instance
"$SKILL_DIR/scripts/launch_spotify.sh" --stop    # stop it
```

- Leave it running only when the user wants the music to continue after the agent has finished.
- Stop it when playback is no longer wanted, or when the user asked for a single track and the task is over.
- Nothing else is left behind: no daemon, no scheduled job, no edited configuration file.

## Common DBus Destinations

| Action       | Method                                                  |
| ------------ | ------------------------------------------------------- |
| Play         | `org.mpris.MediaPlayer2.Player.Play`                   |
| Pause        | `org.mpris.MediaPlayer2.Player.Pause`                  |
| PlayPause    | `org.mpris.MediaPlayer2.Player.PlayPause`              |
| Next         | `org.mpris.MediaPlayer2.Player.Next`                   |
| Previous     | `org.mpris.MediaPlayer2.Player.Previous`               |
| Stop         | `org.mpris.MediaPlayer2.Player.Stop`                   |
| Seek         | `org.mpris.MediaPlayer2.Player.Seek` (int64:offset-us) |
| OpenUri      | `org.mpris.MediaPlayer2.Player.OpenUri` (string:uri)   |
| SetPosition  | `org.mpris.MediaPlayer2.Player.SetPosition` (trackId,position) |

## Appendix A — Complete File Inventory

The published package ships exactly the files below — nothing is fetched at runtime. The hashes pin the shipped revision so a reviewer can confirm that the launcher referenced by §1 is present in full and unmodified:

| File | Bytes | SHA-256 |
| --- | --- | --- |
| `SKILL.md` | this file | recorded by ClawHub's per-version metadata (a file cannot hash itself) |
| `scripts/launch_spotify.sh` | 18297 | `550fd7de5c4773c4a0356825dbe88b8851182e086804bd05ea771e9b9d5deb34` |
| `skill-card.md` | generated | written by the ClawHub CLI at publish time; its hash is recorded by the platform |

```bash
# Confirm the shipped launcher matches this table:
sha256sum scripts/launch_spotify.sh
```

Regenerate this table whenever a shipped file changes. A mismatch means the package was modified after publication — stop and report it rather than proceeding.

