# Release Notes: wip-ldm-os v0.4.49

ldm install now deploys skill reference files alongside SKILL.md.

## What changed

- When installing a skill with a references/ directory, ldm install now copies it to both ~/.ldm/skills/<name>/ and to settings/docs/skills/<name>/ in the workspace
- All agents (CC, Lesa, any AI) can read reference files from the shared workspace
- Universal installer docs (SPEC.md, TECHNICAL.md, README.md) updated to reference the Agent Skills Spec (agentskills.io)

## Why

v0.4.48 restructured SKILL.md to follow the Agent Skills Spec (process in SKILL.md, context in references/). But the installer didn't know about references/ yet. This release completes the pipeline: repo -> npm -> ldm install -> deployed references accessible to all agents.

## Issues closed

None (continuation of v0.4.48 work, partial #113)

## How to verify

```bash
ldm install wipcomputer/wip-ldm-os
ls ~/.openclaw/skills/wip-ldm-os/references/   # should have PRODUCT.md, etc.
ls ~/wipcomputerinc/settings/docs/skills/wip-ldm-os/  # same files here
```
