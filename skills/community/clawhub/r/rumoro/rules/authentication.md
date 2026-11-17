# Authentication

Every request sends `Authorization: Bearer $RUMORO_API_KEY`. A key belongs to one workspace, so every call acts on that workspace and nothing else.

## The key

- Keys start with `ref_`. The full key is shown once, when it's created, and Rumoro stores only its hash.
- Each key has a `scope`. A `write` key runs the whole skill. A `read` key covers searching, analytics and people but changes nothing, and a write with it returns `403 read_only_key`.
- A key can carry `expiresAt`, after which it stops working. That's useful for a contractor or a one-off script.
- `GET /v1/whoami` names the workspace and says whether the credential can write. Call it once when in doubt.

## Where keys come from

- Most users create keys on the API keys page of the Rumoro dashboard at https://app.rumoro.dev. Send the user there.
- `POST /v1/api-keys` with `name`, `scope` and an optional `expiresAt` creates a key from an existing write key. Only create keys when the user asks, and hand a new key over once without storing it.
- `DELETE /v1/api-keys/{id}` revokes a key. The API refuses it right away, and cached checks catch up within a few minutes.

## The same key elsewhere

The CLI and both SDKs read the same key from `RUMORO_API_KEY`. The CLI can also store one with `rumoro auth:login`, which signs in through the browser and saves the key in `~/.rumoro/config.json` (see rules/cli.md). MCP clients can sign in with OAuth instead of a key, while this skill uses the key.

## Care

Never repeat the key back, write it into a file the user didn't ask for, or send it anywhere but `api.rumoro.dev`. If a request returns `401`, stop and tell the user to check `RUMORO_API_KEY` (see Setup in SKILL.md) instead of retrying.
