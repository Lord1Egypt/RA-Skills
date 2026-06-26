---
name: sonos-music-playback
description: 面向中文用户的 Sonos 音乐点播技能。支持通过 Sonos 侧搜索加队列起播的方式播放已绑定音乐服务，当前已验证兼容 网易云音乐 和 QQ音乐。通过 SoCo 将搜索结果转成 Sonos 队列项，再从队列起播，以保留 Sonos App 中的标题、歌手、专辑和封面等 metadata。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["sonos"] },
        "install":
          [
            {
              "id": "soco-python-venv",
              "kind": "message",
              "label": "Run the skill bootstrap script to create the Sonos Python venv and install soco"
            }
          ]
      }
  }
---

# Sonos 音乐点播

## Overview

这个 skill 面向中文用户，用来沉淀可复用的 Sonos 点播工作流。

当前已验证兼容的音乐服务：
- 网易云音乐
- QQ音乐

This skill assumes:
- Sonos devices are reachable on the local network
- the `sonos` CLI is installed and available in `PATH`
- Sonos App has a working linked music-service authorization for the target service
- service availability may vary by region and by the user's linked Sonos music services

This skill avoids machine-specific hardcoded paths by resolving from:
- `OPENCLAW_WORKSPACE_DIR`
- `OPENCLAW_SONOS_VENV`
- `OPENCLAW_SONOS_NETEASE_WRAPPER`
- `OPENCLAW_SONOS_QQ_WRAPPER`
- `OPENCLAW_SONOS_NETEASE_SCRIPT`
- `OPENCLAW_SONOS_QQ_SCRIPT`

Default behavior should remain simple:
- workspace defaults to the current OpenClaw workspace inferred from the skill location
- venv defaults to `$HOME/.openclaw/venvs/soco-sonos`
- wrappers default to `./scripts/sonos_netease_play.sh` and `./scripts/sonos_qq_play.sh` under the workspace
- playback scripts default to `./scripts/sonos_netease_play.py` and `./scripts/sonos_qq_play.py` under the workspace

## Quick Start

Preferred simple install:

```bash
./skills/sonos-music-playback-market/scripts/install.sh
```

Manual flow if needed:

```bash
./skills/sonos-music-playback-market/scripts/check_env.sh
```

If the check fails, run bootstrap:

```bash
./skills/sonos-music-playback-market/scripts/bootstrap_env.sh
```

Then use the standard playback entrypoints, for example:

```bash
./scripts/sonos_netease_play.sh --room 'Living Room' '至少还有你'
./scripts/sonos_qq_play.sh --room 'Living Room' '稻香'
```

## Workflow

### 1. Prefer one-command install

Prefer `scripts/install.sh` when:
- using the skill for the first time
- after migration or system reinstall
- handing the skill to another environment

### 2. Check environment

Run `scripts/check_env.sh` when:
- debugging a broken environment
- validating an installation result

### 3. Bootstrap if needed

Run `scripts/bootstrap_env.sh` when:
- `soco` is missing
- the Sonos Python venv does not exist
- either playback wrapper is missing or not executable

Bootstrap will:
- create the Sonos Python venv if missing
- install `soco` if missing
- verify both playback wrappers and scripts exist

Bootstrap does not install the `sonos` CLI. If `sonos` is missing, install or restore it separately.

### 4. Play through the standard wrappers

Do not call the Python playback files with system `python3`.

Prefer the wrappers because they pin the correct Python venv and avoid interpreter drift.

## Important implementation contract

### Preserve metadata by playing from queue

When implementing or patching the playback logic, do not replace queue playback with a direct `play_uri(...)` rewrite.

Correct pattern:
- search via `sonos smapi search`
- convert the selected result into a Sonos-accepted object with `SoCo MusicService(...)`
- `add_to_queue(...)`
- `play_from_queue(...)`

This preserves Sonos App metadata such as:
- title
- artist
- album
- album art

### Do not trust search titles alone

Search results through Sonos may contain:
- same-title tracks by different artists
- live / piano / cover / female / child / sentimental variants
- results whose final queue metadata differs from the plain search title

Prefer a two-stage selection strategy:
1. title-based initial filtering
2. queue-metadata-based rescoring using actual Sonos metadata

### QQ音乐-specific note

`sonoscli` currently supports searching QQ音乐 via `sonos smapi search --service 'QQ音乐'`, but its `--open` flow still behaves like a Spotify-only path and does not directly play QQ search results.

For QQ音乐, use the validated queue-based SoCo path instead of `sonos smapi search --open`.

## Troubleshooting

### Can search but cannot play

First suspect linked service authorization state in Sonos App.

A reliable recovery path is usually:
- re-add or re-authorize the music service in Sonos App

### QQ音乐 auth page opens but does not complete in CLI

This is likely an incompatibility in the current CLI auth/open flow rather than a proof that QQ音乐 itself is unavailable in Sonos.

If Sonos App already has a working QQ音乐 binding and `sonos smapi search --service 'QQ音乐'` returns results, prefer the SoCo queue-based playback path.

### Plays but metadata is blank

First inspect whether the playback path regressed to `play_uri(...)`.

### Still chooses the wrong version

Inspect the actual queue metadata returned by Sonos. If the search source itself does not return the desired original version, this is a source-quality limitation, not necessarily a scoring bug.

## Release Checklist

Before publishing or distributing this skill, verify:
- `scripts/check_env.sh` returns `ready=yes` in a representative environment
- `scripts/bootstrap_env.sh` can create the venv and install `soco` when missing
- a real 网易云 playback command reaches `PLAYING`
- a real QQ音乐 playback command reaches `PLAYING`
- `nowPlaying.title` is non-empty after playback starts
- the documented prerequisites match reality for the target environment

## Resources

### scripts/

- `scripts/install.sh`
  - one-command installer that runs bootstrap and validation, then prints example playback commands
- `scripts/check_env.sh`
  - portable environment checker using environment-variable-based path resolution
- `scripts/bootstrap_env.sh`
  - portable bootstrap script for the Sonos Python venv and `soco`, and verifies both playback entrypoints exist
