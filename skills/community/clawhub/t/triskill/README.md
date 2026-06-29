# Triskill

Three small, independently-useful agent capabilities in one package:

1. **Fact-Check** — verify a claim against a live web search before stating
   it with confidence. Read-only, refuses credential/login-looking queries.
2. **Self-Heal** — bounded diagnose-and-retry wrapper for failing commands.
   Classifies the failure cause, logs every attempt for audit, refuses
   destructive commands (`rm -rf /`, fork bombs, etc.), and never silently
   rewrites your code — it surfaces a diagnosis, the agent proposes the fix.
3. **Shared Memory** — a local, file-locked JSON key-value store so multiple
   agents/sub-agents on the same machine can coordinate (claim tasks,
   maintain counters, avoid double-work) without racing each other.
   Verified under load: 20 parallel processes × 10 increments = 200/200,
   zero lost writes.

## Why three in one?

These three problems — "is this still true?", "it failed, now what?", and
"how do two agents avoid stepping on each other?" — show up constantly in
real agent workflows and are usually solved with ad-hoc, unsafe scripts.
Triskill gives each one a small, tested, safety-limited implementation
instead.

## Install

```
clawhub install triskill
```

## Quick examples

```bash
# Verify a claim
python3 scripts/factcheck.py "current Mayor of Casablanca"

# Run a flaky command with bounded retries + diagnosis
python3 scripts/selfheal.py --max-retries 3 -- npm test

# Coordinate two agents claiming work without racing
python3 scripts/sharedmem.py cas job-42 status pending claimed_by_agentA
```

See `SKILL.md` for the full instructions an agent should follow, including
the hard safety limits for each capability.

## License

MIT
