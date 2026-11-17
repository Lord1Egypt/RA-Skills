# Authentication

## Getting an API key

The user generates keys at **ViralNote dashboard → Settings → API keys**. They pick the scopes the key should be allowed to use.

Keys look like `vnd_xxxxxxxx...` and are shown **once** at creation time — the user must copy and store it immediately. They cannot be re-displayed.

## Scopes

Each key has a fixed set of scopes. Common ones:

| Scope | Grants |
|---|---|
| `posts:read` | List, read, search posts. Read analytics and publish history. |
| `posts:write` | Create, update, delete, publish posts. Upload and import media. |
| `webhooks:read` | List webhook subscriptions. |
| `webhooks:write` | Create, update, delete webhook subscriptions. |

Request only the scopes the workflow needs. If the user is setting up an analytics-only integration, `posts:read` is sufficient.

## Sending the key

Both forms accepted:

```bash
# Preferred
-H "x-api-key: $VIRALNOTE_API_KEY"

# Equivalent
-H "Authorization: Bearer $VIRALNOTE_API_KEY"
```

## Storing the key

In agent contexts, the key should live in an environment variable named `VIRALNOTE_API_KEY` — never in a tracked file, never in chat logs.

If the agent doesn't have `VIRALNOTE_API_KEY` set, prompt the user to set it before continuing. Example prompt:

> "I don't see VIRALNOTE_API_KEY in your environment. Generate one at https://viralnote.app/developers/auth and export it:
> ```
> export VIRALNOTE_API_KEY=vnd_...
> ```
> Then I'll continue."

## Rotation

If a key is leaked or rotated, the old key starts returning `401` immediately. Ask the user to:

1. Revoke the leaked key in dashboard → Settings → API keys
2. Generate a new key
3. Update their environment

Then retry the failed action with the new key.
