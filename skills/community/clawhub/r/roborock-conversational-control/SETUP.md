# Setup

This is the shortest reliable setup for a real user.

The goal is not just "control the vacuum." The goal is to give the vacuum its own conversational control layer.

## 1. Install the skill

Put this skill at:

```bash
~/.openclaw/skills/jojo-bot
```

## 2. Install the Roborock CLI

Recommended:

```bash
pipx install python-roborock
```

If the CLI has missing runtime deps in your environment, inject them:

```bash
pipx inject python-roborock PyYAML pyshark
```

## 3. Login

```bash
roborock login --email "your@email.com"
```

Current `python-roborock` versions usually use an email code flow by default.

## 4. Find the device id

```bash
roborock list-devices
```

## 5. Create local config

Create `~/.openclaw/skills/jojo-bot/jojo.env` with:

```bash
JOJO_DEVICE_ID="your-device-id"
JOJO_DEVICE_NAME="jojo"
```

Optional room aliases:

```bash
# ROOM_KITCHEN="17"
# ROOM_MASTER_BEDROOM="19"
# ROOM_LIVING_AREA="21"
```

## 6. Bootstrap room aliases

Run:

```bash
bash ~/.openclaw/skills/jojo-bot/scripts/refresh_room_aliases.sh
```

That prints suggested `ROOM_*` lines based on the live Roborock room map.

Copy the ones you want into `jojo.env`.

## 7. Restart OpenClaw

```bash
openclaw daemon restart
```

## 8. Smoke test

```bash
bash ~/.openclaw/skills/jojo-bot/scripts/jojo.sh status
bash ~/.openclaw/skills/jojo-bot/scripts/jojo.sh rooms
bash ~/.openclaw/skills/jojo-bot/scripts/jojo.sh start
bash ~/.openclaw/skills/jojo-bot/scripts/jojo.sh home
```

## 9. Optional: dedicated Telegram bot

This skill works best with a separate Telegram bot bound to a dedicated OpenClaw agent if you want Jojo to feel like a standalone character.

Typical flow:

```bash
openclaw channels add --channel telegram --account jojo --name Jojo --token <telegram-bot-token>
openclaw agents add jojo --workspace ~/.openclaw/workspace-jojo --bind telegram:jojo --non-interactive
openclaw daemon restart
```

Then give that agent a Jojo-only workspace and prompt.

This is optional. The skill also works inside a shared main bot if you reserve clear phrases like `jojo clean the kitchen` or `jojo go home`.

## Common failures

`You must login first`
- run `roborock login --email ...`

`The method called is not recognized by the device`
- use the verified command verbs from this skill (`app_start`, `app_pause`, `app_stop`, `app_charge`)

`room not found`
- the alias is missing from `jojo.env`
- or the live room name from Roborock does not match what the user said

`command requires approval`
- allowlist the wrapper path in OpenClaw exec approvals

## Publish guidance

Publish this as:
- a conversational Roborock companion
- a Telegram-friendly vacuum agent for OpenClaw
- a higher-level layer above raw Roborock control

Do not publish it as:
- an official Roborock integration
- a camera or microphone bridge
- a replacement for every low-level Roborock skill
