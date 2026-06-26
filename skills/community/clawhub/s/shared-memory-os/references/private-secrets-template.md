# Private Secrets Template

Use `memory/private-secrets.md` only when the workspace owner explicitly wants the system to remember actual secret material.

## Suggested entry shape

```md
## OPENROUTER_API_KEY
- value: <actual secret>
- purpose: api-failover secondary provider
- used_by: api-failover.service
- last_verified: 2026-04-02
- notes: only use in private trusted sessions
```

```md
## TELEGRAM_BOT_TOKEN
- value: <actual secret>
- purpose: OpenClaw Telegram channel
- used_by: openclaw gateway runtime
- last_verified: 2026-04-02
- notes: never copy into public docs or skill bundles
```

## Rules

- Keep this file out of skill bundles and public artifacts
- Do not duplicate these values in daily/project/release notes
- Read only on explicit need
- Prefer adding purpose and verification metadata so secrets remain usable rather than mysterious
