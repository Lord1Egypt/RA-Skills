# Token and control notes

## Token source

Prefer one of these:

1. A user-provided Yandex Music auth token they already extracted.
2. A token exported into `YM_TOKEN` for one command/session.
3. A token saved with `scripts/ymctl.py auth-set ...` into the workspace-local config file.

Do not paste tokens back into chat unless the user explicitly asks.

## Quick token workflow

### Safest path for day-to-day use

- put a fresh token into `YM_TOKEN` for one-off checks
- if it works, persist it with `auth-set`
- verify with `auth-check`
- inspect source/preview with `auth-where`

### If the saved token stops working

- run `auth-check`
- if you get `Unauthorized`, the token is stale/invalid
- replace it with a fresh one via `auth-set`
- if needed, `auth-clear` first

### Practical extraction hint

The exact extraction dance changes over time, so do not hardcode brittle browser automation into the skill.
Use a manual browser/devtools flow when needed: sign into Yandex Music in the browser, inspect authenticated requests, copy the OAuth token, then save it locally.
If the user asks for extraction help, guide them interactively instead of promising a forever-stable scraping method.

## Storage

Default config file:

`/root/.openclaw/workspace/.openclaw/yandex-music-control/config.json`

The helper script writes it with mode `0600`.

Useful commands:

- `scripts/ymctl.py auth-where`
- `scripts/ymctl.py auth-check`
- `scripts/ymctl.py auth-clear`

## Playback reality check

This helper is intentionally limited to the operations that were shown to work reliably.

Reliable commands from the helper:

- search
- now-playing (Ynison probe for modern clients)
- likes / playlists
- like / unlike

Not supported by this helper:

- next / prev / jump
- pause / resume
- guaranteed cross-device transport controls
- blind playback start on arbitrary devices

Why the limitation:

- Ynison can expose current-track state reliably.
- In testing, transport-like mutations could change server-visible mirrored state without switching the real client playback.
- So transport controls were removed instead of leaving misleading pseudo-success in place.

## Device metadata

`now-playing` intentionally includes Ynison device/session metadata when available. This is useful for debugging, but it should not be interpreted as proof that live remote control is available.

## Suggested command mapping for natural-language requests

- "что сейчас играет" → `now-playing`
- "найди трек/альбом/артиста" → `search`
- "лайкни это" → `like <track-id or query>`
- "покажи лайкнутые" → `likes`
- "какие у меня плейлисты" → `playlists`
- "где у тебя сейчас токен/какой источник" → `auth-where`
