# LDM OS v0.4.1

Consolidate Universal Installer into LDM OS. Closes wipcomputer/wip-ai-devops-toolbox#182.

## What changed

The `wip-install` command now ships with LDM OS. The 700-line standalone `install.js` from the DevOps Toolbox is replaced by a thin bootstrap (`lib/bootstrap.mjs`) that delegates to `ldm install`.

Three steps:
1. Check if `ldm` is on PATH
2. If not, `npm install -g @wipcomputer/wip-ldm-os`
3. Delegate to `ldm install`

No standalone fallback code. All install logic lives in `lib/deploy.mjs`.

## Also

- SPEC.md (Universal Interface Spec) moved from toolbox to `docs/universal-installer/SPEC.md`
- `wip-install` added to package.json bin entries

## Issues closed

- Closes wipcomputer/wip-ai-devops-toolbox#182
