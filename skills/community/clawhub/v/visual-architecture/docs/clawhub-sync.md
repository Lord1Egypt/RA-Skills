# ClawHub Sync Checklist

Publish to ClawHub only after the public repo state is green and the installable package is clean.

## Required Checks

```bash
make validate
grep -RInE "private-path|private-host|token-placeholder|client-name-placeholder" README.md SKILL.md CHANGELOG.md docs examples scripts schemas
```

Install smoke after publish must confirm:

- `SKILL.md` reports the expected version
- examples are present
- `python3 scripts/render_architecture.py validate examples/service-map.json --json` exits 0
- no generated docs expose private local paths, private hosts, credentials, or internal runtime state

## Current State

GitHub `v1.0.0` is the target public release for the full product ladder. ClawHub sync is allowed only if the publish bundle passes the checks above and the registry accepts the package cleanly.
