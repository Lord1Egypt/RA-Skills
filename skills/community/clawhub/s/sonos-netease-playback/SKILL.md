---
name: sonos-netease-playback
description: Portable Sonos + Netease playback skill for OpenClaw environments. Use when an agent needs a standard reusable workflow to search and play a specific song to a Sonos room, preserve Sonos App metadata display, bootstrap the Python SoCo dependency, or restore the environment after migration. Suitable for packaging or sharing because it avoids machine-specific hardcoded paths and uses environment variables for workspace, wrapper, script, and venv resolution.
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
              "label": "Run the skill bootstrap script to create the Sonos Python venv and install soco",
            },
          ],
      },
  }
---

# Sonos Netease Playback

> Deprecated: this skill has been superseded by `sonos-music-playback`, which covers both 网易云音乐 and QQ音乐.
> Prefer the newer skill for fresh installs and future updates.

## Overview

Use this skill as the portable, shareable version of the Sonos 网易云点播 workflow.

This skill assumes:
- Sonos devices are reachable on the local network
- the `sonos` CLI is installed and available in `PATH`
- Sonos App has a working linked Netease music service authorization
- service availability may vary by region and by the user's linked Sonos music services

This skill should be designed toward simple installation:
- prefer one bootstrap command over many manual steps
- keep path assumptions configurable through environment variables
- minimize the number of places an agent must remember

This skill avoids machine-specific hardcoded paths by resolving from:
- `OPENCLAW_WORKSPACE_DIR`
- `OPENCLAW_SONOS_VENV`
- `OPENCLAW_SONOS_WRAPPER`
- `OPENCLAW_SONOS_SCRIPT`

Default behavior should remain simple:
- workspace defaults to the current OpenClaw workspace inferred from the skill location
- venv defaults to `$HOME/.openclaw/venvs/soco-sonos`
- wrapper defaults to `./scripts/sonos_netease_play.sh` under the workspace
- playback script defaults to `./scripts/sonos_netease_play.py` under the workspace

## Quick Start

Preferred simple install:

```bash
./skills/sonos-netease-playback-market/scripts/install.sh
```

Manual flow if needed:

```bash
./skills/sonos-netease-playback-market/scripts/check_env.sh
```

If the check fails, run bootstrap:

```bash
./skills/sonos-netease-playback-market/scripts/bootstrap_env.sh
```

Then use the standard playback entrypoint, for example:

```bash
./scripts/sonos_netease_play.sh --room 'Living Room' '至少还有你'
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
- the wrapper is missing or not executable

Bootstrap will:
- create the Sonos Python venv if missing
- install `soco` if missing
- create a default playback wrapper if the wrapper file is absent

Bootstrap does not install the `sonos` CLI. If `sonos` is missing, install or restore it separately.

### 4. Play through the standard wrapper

Do not call the Python playback file with system `python3`.

Prefer the wrapper because it pins the correct Python venv and avoids interpreter drift.

## Important implementation contract

### Preserve metadata by playing from queue

When implementing or patching the playback logic, do not replace queue playback with a direct `play_uri(...)` rewrite.

Correct pattern:
- convert the music service result into a Sonos-accepted object
- `add_to_queue(...)`
- `play_from_queue(...)`

This preserves Sonos App metadata such as:
- title
- artist
- album
- album art

### Do not trust search titles alone

Netease search results through Sonos may contain:
- same-title tracks by different artists
- live / piano / cover / female / child / sentimental variants
- results whose final queue metadata differs from the plain search title

Prefer a two-stage selection strategy:
1. title-based initial filtering
2. queue-metadata-based rescoring using actual Sonos metadata

## Troubleshooting

### Can search but cannot play

First suspect linked service authorization state in Sonos App.

A reliable recovery path is usually:
- re-add or re-authorize the Netease service in Sonos App

### Plays but metadata is blank

First inspect whether the playback path regressed to `play_uri(...)`.

### Still chooses the wrong version

Inspect the actual queue metadata returned by Sonos. If the search source itself does not return the desired original version, this is a source-quality limitation, not necessarily a scoring bug.

## Release Checklist

Before publishing or distributing this skill, verify:
- `scripts/check_env.sh` returns `ready=yes` in a representative environment
- `scripts/bootstrap_env.sh` can create the venv and install `soco` when missing
- a real playback command reaches `PLAYING`
- `nowPlaying.title` is non-empty after playback starts
- the documented prerequisites match reality for the target environment

## Resources

### scripts/

- `scripts/install.sh`
  - one-command installer that runs bootstrap and validation, then prints the standard playback example
- `scripts/check_env.sh`
  - portable environment checker using environment-variable-based path resolution
- `scripts/bootstrap_env.sh`
  - portable bootstrap script for the Sonos Python venv and `soco`, and can generate a default playback wrapper when absent
