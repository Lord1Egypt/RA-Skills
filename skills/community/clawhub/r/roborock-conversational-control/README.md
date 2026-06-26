# Jojo Bot

Jojo Bot turns a Roborock vacuum into a conversational device companion for OpenClaw and Telegram.

It supports:
- status
- start / pause / stop / dock
- room cleaning by alias
- room alias bootstrap from the live Roborock map
- a dedicated Jojo persona layer on top of Roborock control

## What this skill is

This is not just a raw Roborock control wrapper.

It is a higher-level companion skill built on top of the `roborock` CLI so the bot can:
- talk as the vacuum
- understand room-oriented intent
- stay scoped to Jojo-only tasks

If you only want direct device commands, use a lower-level Roborock skill.
If you want a vacuum with its own voice, room aliases, and Telegram-friendly behavior, use this skill.

## What the user needs

- `python-roborock` installed
- a logged-in Roborock account
- a device id from `roborock list-devices`
- a local `jojo.env` created using the config block in `SETUP.md`

Optional:
- a dedicated Telegram bot and OpenClaw agent binding

## Install summary

1. Install `python-roborock`
2. Run `roborock login --email "..."`
3. Run `roborock list-devices`
4. Create `jojo.env`
5. Set `JOJO_DEVICE_ID`
6. Run `bash ./scripts/refresh_room_aliases.sh`
7. Restart OpenClaw

For the full process, read [SETUP.md](./SETUP.md).

## Good test prompts

- `status`
- `clean the house`
- `pause`
- `go home`
- `which rooms do you know`
- `clean the kitchen`

## What to say on ClawHub

Position this as:
- a conversational Roborock companion
- a Jojo-style agent layer for OpenClaw
- useful for Telegram or direct OpenClaw chat

Do not position it as:
- a drop-in replacement for every Roborock skill
- low-level device protocol tooling
- microphone or camera integration

## For agents

Agent-specific operating rules live in [AGENTS.md](./AGENTS.md).
