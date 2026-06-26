# Flow Runner

Use `run` when a short repeatable browser flow fits the built-in action set.

## Supported actions

The current `run` command supports only these step actions:

- `openbrowser`
- `openUrl`
- `wait-for`
- `click`
- `query`

Do not assume `run` supports `type`, `eval-js`, `wait-for-gone`, or proxy commands unless the toolkit is extended first.

## Flow shape

```json
{
  "name": "example-flow",
  "settings": {
    "port": 9222,
    "timeoutMs": 10000,
    "pollMs": 200,
    "retries": 0,
    "retryDelayMs": 300
  },
  "steps": [
    { "id": "browser", "action": "openbrowser" },
    { "id": "open", "action": "openUrl", "url": "https://example.com" },
    { "id": "ready", "action": "wait-for", "selector": "body" },
    { "id": "links", "action": "query", "selector": "a[href]", "fields": "text,href", "limit": 10 }
  ]
}
```

## Step fields

- Shared optional fields: `id`, `port`, `targetId`, `urlMatch`, `timeoutMs`, `pollMs`, `retries`, `retryDelayMs`
- `openUrl`: requires `url`
- `wait-for`: requires `selector`
- `click`: requires `selector`
- `query`: requires `selector`, optional `fields` and `limit`

## Artifacts

`run` writes per-step JSON, a summary, a log, and usually a final DOM snapshot into an artifacts directory. Pass `--artifacts-dir` when you need a deterministic output location.
