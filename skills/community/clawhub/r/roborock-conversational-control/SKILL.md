---
name: jojo-bot
description: "Turn a Roborock into a conversational OpenClaw companion. Use when the user wants natural-language vacuum control like clean the kitchen, go home, pause, status, or room-specific cleaning, especially in Telegram. This is a higher-level companion layer, not just raw Roborock control. Execute the local shell wrapper in scripts/jojo.sh via exec; do not use ACP or sessions_spawn for routine control actions."
version: 1.0.1
user-invocable: true
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins:
        - bash
        - roborock
        - python3
---

# Jojo Bot

> **Execution rule**: use the `exec` tool to run the shell wrapper in `scripts/jojo.sh`. Do not use `sessions_spawn` or ACP for routine Jojo commands.

This skill turns a Roborock vacuum into a conversational device companion.

It is designed for:
- OpenClaw chat
- Telegram bots
- room-aware vacuum control
- a lightweight Jojo-style persona on top of real device actions

It is not a replacement for low-level Roborock tooling. It is the higher-level layer that makes a vacuum feel like its own agent.

Use it for:
- `clean the kitchen`
- `clean the living area`
- `clean the house`
- `pause`
- `go home`
- `status`
- `which rooms do you know`

## Required local config

Create `jojo.env` in this skill folder from `jojo.env.example`.

Minimum required value:
- `JOJO_DEVICE_ID`

Optional:
- `JOJO_DEVICE_NAME`
- `ROOM_<ALIAS>` mappings such as `ROOM_KITCHEN="17"`

## Wrapper

Resolve the skill directory, then call:

```bash
bash <skill_dir>/scripts/jojo.sh status
bash <skill_dir>/scripts/jojo.sh start
bash <skill_dir>/scripts/jojo.sh pause
bash <skill_dir>/scripts/jojo.sh stop
bash <skill_dir>/scripts/jojo.sh home
bash <skill_dir>/scripts/jojo.sh rooms
bash <skill_dir>/scripts/jojo.sh room kitchen
bash <skill_dir>/scripts/jojo.sh room "master bedroom"
```

## Intent mapping

- `status`, `what are you doing`, `battery`, `where are you` -> `status`
- `clean the house`, `start cleaning`, `go clean` -> `start`
- `pause`, `wait`, `hold on` -> `pause`
- `stop cleaning` -> `stop`
- `go home`, `dock`, `charge`, `return to dock` -> `home`
- `which rooms`, `what rooms`, `rooms` -> `rooms`
- `clean the <room>` -> `room "<room>"`

If room intent is ambiguous, ask one short follow-up.

## Room aliases

The wrapper supports user-defined aliases through env vars:

```bash
ROOM_KITCHEN="17"
ROOM_MASTER_BEDROOM="19"
ROOM_LIVING_AREA="21"
```

To bootstrap aliases from the live Roborock map:

```bash
bash <skill_dir>/scripts/refresh_room_aliases.sh
```

## Positioning

- Use `robo-rock` or the raw `roborock` CLI when you only want direct device control.
- Use `jojo-bot` when you want a conversational robot companion with room aliases, short replies, and a dedicated device identity.

## Notes

- Current `python-roborock` builds use `roborock login --email ...`
- Verified command verbs are `app_start`, `app_pause`, `app_stop`, `app_charge`, and `app_segment_clean`
- Keep this skill device-scoped. If the user wants a dedicated Telegram bot, bind a dedicated OpenClaw agent to a separate Telegram account.
