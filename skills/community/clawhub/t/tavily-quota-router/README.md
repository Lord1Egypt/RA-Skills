# Tavily Quota Router

**Multi-key Tavily search router with auto-failover, 429-aware cooldown, and quota observability.**

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)

Tavily is a great web search API for AI agents, but a single API key has hard rate limits (100 RPM for dev keys, 1000/month quota) — one burst from your agent and you're 429-blocked. This router solves that by rotating across multiple keys automatically.

**For installation and configuration, see [QUICKSTART.md](./QUICKSTART.md).**

## What it does

- **Auto-rotates across keys** — when key A 429s, the next search automatically uses key B
- **Honors Tavily's `Retry-After` header** — instead of using a 10-minute blanket cooldown, the router waits exactly as long as Tavily tells it to (typically 10-60s)
- **Recovers from auth errors** — 401/403 puts a key on a 1-hour cooldown, then auto-reprobes (instead of permanently disabling it)
- **Per-key observability** — `status` shows usage, cooldown, and last error for each key
- **Hot-swappable keys** — edit `config/keys.json` while the router is running; changes take effect on the next search

## When to use this

✅ You have 2+ Tavily keys and want fault-tolerance  
✅ Your agent bursts >5 searches in quick succession  
✅ You use Tavily >500 times/month  
✅ You want to see per-key quota usage in real time

❌ You only have 1 key (direct HTTP is simpler)  
❌ You use Tavily <100 times/month (won't hit limits)  
❌ You need production-grade high concurrency (≥100 req/sec) — use the Tavily SDK with your own queue

## Install

```bash
clawhub install @fangtang0206/tavily-quota-router
```

Then follow [QUICKSTART.md](./QUICKSTART.md) — 5 commands, ~2 minutes.

## Usage

```bash
python3 ~/.hermes/skills/openclaw-imports/tavily-quota-router/scripts/tavily_multi_key.py search \
    --query "your query here" --count 5
```

Or import from your agent code:

```python
import subprocess, json
result = subprocess.run([
    'python3',
    '~/.hermes/skills/openclaw-imports/tavily-quota-router/scripts/tavily_multi_key.py',
    'search', '--query', q, '--count', '5'
], capture_output=True, text=True)
data = json.loads(result.stdout)
if data['ok']:
    for r in data['results']:
        print(r['title'], r['url'])
```

## Why these specific behaviors?

These are documented in [SKILL.md](./SKILL.md) and traced through verification transcripts in `references/`:

- [references/tavily-429-retry-after-2026-07-17.md](./references/tavily-429-retry-after-2026-07-17.md) — why we parse `Retry-After`, with a real Tavily 429 response dump
- [references/tavily-401-403-recovery-pattern.md](./references/tavily-401-403-recovery-pattern.md) — why we don't permanently disable on auth errors
- [references/state-machine-2026-07-08.md](./references/state-machine-2026-07-08.md) — `state/quota.json` field semantics
- [references/security-hardening.md](./references/security-hardening.md) — env var migration path for multi-user servers

## Contributing

Bug reports and PRs welcome. Before pushing, the `pre-commit` hook auto-checks for accidental `tvly-dev-...` leaks — `scripts/check-secrets.sh`.

## License

MIT-0 — public domain, no attribution required.