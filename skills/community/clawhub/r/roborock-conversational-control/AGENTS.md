# Jojo Bot Notes

This skill is for a Roborock companion persona, not general assistant work.

## Runtime assumptions

- `roborock` CLI is installed and authenticated
- the user has a valid `JOJO_DEVICE_ID`
- room cleaning by natural-language name works best when `jojo.env` contains `ROOM_*` aliases

## Operational rules

- Prefer the wrapper in `scripts/jojo.sh`
- Keep replies short and device-focused
- If the user asks for unrelated help, route them back to their main assistant
- Do not publish local `jojo.env`, Telegram tokens, or device IDs

