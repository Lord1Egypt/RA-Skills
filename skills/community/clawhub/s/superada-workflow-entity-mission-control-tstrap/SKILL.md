---
name: superada-workflow-entity-mission-control-bootstrap
description: Installs from a real external skill bundle that bootstraps the Entity Mission Control helper runtime for a crew of agents with shared scripts, structured task intake, per-agent manifests, and supervised rollout steps.
---

# Entity Mission Control Bootstrap

Workflow bundle exported from SuperAda.ai for ClawHub discovery.

## Source
- SuperAda page: https://superada.ai/workflows/entity-mission-control-bootstrap/
- Source URL: https://github.com/h-mascot/enterprise-crew-skills/tree/main/entity-mc
- Category: Operations
- Difficulty: Advanced
- Status: Live

## Install

```bash
git clone https://github.com/h-mascot/enterprise-crew-skills.git /tmp/enterprise-crew-skills && mkdir -p skills && cp -R /tmp/enterprise-crew-skills/entity-mc skills/entity-mc && bash skills/entity-mc/install-auto.sh
```

## What It Does

Installs from a real external skill bundle that bootstraps the Entity Mission Control helper runtime for a crew of agents with shared scripts, structured task intake, per-agent manifests, and supervised rollout steps.

## Verification
- OpenClaw runtime with skill install access
- Mission Control connectivity
- Operator review of host mappings
- Source bundle review
- Bundle install present
- Manifest applied

## Safety Notes
- cron-safe rollout
- Canonical source bundle
- This listing describes an externally hosted skill bundle. It does not imply those runtime files are checked into this website repo.
- Review the linked GitHub bundle before install so the runtime, manifests, and helper scripts are understood.
- "If `openclaw skills install --help` only accepts a ClawHub slug, do not use the `github:` source spec. Clone the source repo, copy `entity-mc` into the local `skills/entity-mc` workspace path, and run `bash skills/entity-mc/install-auto.sh`."
- "`install-auto.sh` creates an auto manifest for the current workspace, installs wrappers, installs portable MC/intake setup context, writes the auto-pull and stall-check cron entries, then runs verification."
