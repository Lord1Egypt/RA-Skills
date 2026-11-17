---
title: "WIP Codex fork upstream hygiene"
status: open
priority: P0
owner: Cody
repo: openai-codex-private
created: 2026-05-05
---

# WIP Codex Fork Upstream Hygiene

## Decision

WIP will carry a private Codex fork for Remote Control v1 co-presence work.

Private fork:

```text
wipcomputer/openai-codex-private
```

Local checkout:

```text
/Users/lesa/wipcomputerinc/repos/third-party-repos/openai-codex-private
```

Remote shape:

- `upstream`: `https://github.com/openai/codex.git`
- `origin`: private WIP fork

The private fork exists so WIP can build, test, and dogfood the generic Codex co-presence patch without waiting for upstream release timing.

## Upstream Boundary

The upstreamable patch is generic Codex infrastructure:

- App Server supports multiple subscribers to the same thread.
- Multiple clients observe the same semantic turn stream.
- One client disconnecting does not cancel or unload the others.
- `turn/interrupt`, status, approval, and turn lifecycle events broadcast to all subscribers.
- Tests exercise generic App Server behavior with no WIP services.

The upstreamable patch must not depend on:

- WIP hosted relay.
- WIP passkey auth.
- Phone-as-key assumptions.
- Kaleidoscope UI.
- `codex-daemon`.
- LDM install behavior.
- WIP URLs.
- WIP product names in code.
- Dogfood transcripts or screenshots.
- `ai/**`.

## Private Fork Contents

The private fork may contain WIP-only planning and coordination files:

- `ai/**`
- internal notes
- dogfood runbooks
- private product decisions
- WIP release/install notes

Those files are allowed only in `wipcomputer/openai-codex-private`. They must never appear in an upstream PR to `openai/codex`.

## Required Repo Init

During private fork initialization, add:

- root `AGENTS.md` or `CLAUDE.md` with the upstream hygiene rule
- `ai/README.md` explaining that `ai/**` is private WIP planning only
- `scripts/check-upstream-pr-clean.sh`

The guard script should fail if an upstream PR branch includes private files:

```bash
#!/usr/bin/env bash
set -euo pipefail

base="${1:-upstream/main}"

bad="$(git diff --name-only "$base"...HEAD | grep -E '^(ai/|.*private.*\\.md)' || true)"

if [ -n "$bad" ]; then
  echo "Blocked: private WIP files would be included in upstream PR:"
  echo "$bad"
  exit 1
fi
```

The final upstream PR checklist must include:

```text
Before opening upstream PR:
- Run scripts/check-upstream-pr-clean.sh upstream/main
- Confirm no ai/** files are in the upstream diff
- Confirm no WIP hosted relay, passkey, Kaleidoscope, daemon, or install dependency is in the patch
```

## Acceptance

- `wipcomputer/openai-codex-private` exists and is private.
- Local checkout exists under `repos/third-party-repos/openai-codex-private`.
- `upstream` points to `openai/codex`.
- `origin` points to the private WIP fork.
- WIP `ai/` structure exists in the private fork.
- Root repo instructions state that `ai/**` never goes upstream.
- `ai/README.md` states that `ai/**` is private WIP planning only.
- `scripts/check-upstream-pr-clean.sh` exists and blocks `ai/**` in upstream diffs.
- The Remote Control co-presence patch branch can be dogfooded from the private fork.
- The upstream PR branch can be cut cleanly without WIP-private files.
