# Session Storage

The skill now uses two durable layers:

1. per-origin manifests for live runtime verification
2. a site session registry for default per-site identity reuse

## 1. Session Manifest

`session-manifest.sh` stores exact runtime records under `~/.agent-browser/` by default.

Current scoped layout:

- runtime: `run/<origin-key>/<session-key>/`
- assisted overlay: `assist/<origin-key>/<session-key>/`
- profile: `profiles/<origin-key>/<session-key>/`
- logs: `logs/<origin-key>/<session-key>/`
- manifests: `sessions/<origin-key>/<session-key>.json`

Typical manifest commands:

```bash
scripts/session-manifest.sh list
scripts/session-manifest.sh show --origin 'https://github.com' --session-key default
scripts/session-manifest.sh write --origin 'https://github.com' --session-key default --state ready --browser-pid 123
scripts/session-manifest.sh mark-stale --origin 'https://github.com' --session-key default --reason 'browser exited'
```

Operational notes:

- manifests track exact captured runtime details
- they are still used for verification and compatibility fallback
- they are not the primary product abstraction for default reuse anymore

## 2. Site Session Registry

`site-session-registry.sh` stores the default durable identity by canonical site:

- `github.com`
- `google.com`
- exact host for other sites unless an alias is intentionally added

Storage file:

- `index/site-sessions.json`

Typical commands:

```bash
scripts/site-session-registry.sh show --site github.com
scripts/site-session-registry.sh resolve --site github.com --session-key default
scripts/site-session-registry.sh write --site github.com --session-key default --profile-dir ~/.agent-browser/profiles/https___github_com/default --source-origin 'https://github.com'
```

Operational notes:

- default reuse should prefer `site + session-key`
- non-default identities are allowed, but only when the user explicitly chooses a different `session-key`
- corrupt registry JSON is treated as empty and rewritten on the next successful capture

## Resolution Model

Current preferred resolution order:

1. explicit CLI `--profile-dir`
2. site session registry
3. exact manifest `profile_dir`
4. compatibility fallback for legacy/scoped profile reuse
5. fresh derived path only as the last fallback
