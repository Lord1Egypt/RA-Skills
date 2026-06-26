# Multi-account routing

## Goal

Map separate QQ bot accounts to separate OpenClaw agents without cross-routing.

Example:

- `K1 -> main`
- `K2 -> agent2`

## Minimal binding pattern

```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "qqbot",
        "accountId": "K1"
      }
    },
    {
      "agentId": "agent2",
      "match": {
        "channel": "qqbot",
        "accountId": "K2"
      }
    }
  ]
}
```

## Root cause of duplicate sessions

If the same inbound message reaches two agents, the most important check is runtime isolation by `appId`.

The following state should be account-scoped, not global:

- access token cache
- token fetch singleflight state
- background refresh controller

## Typical symptom

- one QQ DM
- two bot accounts process it
- two agents create sessions
