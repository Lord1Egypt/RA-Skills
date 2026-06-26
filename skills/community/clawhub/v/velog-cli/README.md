# velog-cli

Velog public RSS/GraphQL CLI — fetch latest posts for any Velog user without API keys.

- No auth required (uses public RSS: `https://v2.velog.io/rss/<username>`)
- Output as Markdown (default) or JSON
- Filter by count

## Quickstart

```bash
pipx install .  # or: uv tool install .
velog-cli user-posts --username velopert --limit 5 --format md
```

Example output (md):

```
- [Understanding React Hooks](https://velog.io/@velopert/react-hooks) — 2026-04-01
- [TypeScript Utility Types](https://velog.io/@velopert/ts-utility) — 2026-03-27
```

## CLI

```
velog-cli user-posts --username <name> [--limit 10] [--format md|json]
```

## Why

ClawHub currently lacks a Velog integration while Korean developer communities rely heavily on Velog. This tool fills a common need: quickly pulling a user's latest posts for newsletters, digests, or agent context.

## Configuration

No environment variables are required.

## References
- Official site: https://velog.io
- Public RSS: https://v2.velog.io/rss/<username>
```
