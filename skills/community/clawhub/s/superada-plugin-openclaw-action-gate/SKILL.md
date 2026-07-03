---
name: openclaw-action-gate
description: The OpenClaw-side runtime plugin for the Action Gate project. Hooks before_incoming_action, before_outbound_message, and after_outbound_message, applies the per-scope action-gate.json policy, and writes a per-decision audit record. This is the package you actually install; the Action Gate page on SuperAda documents the contract and use cases, this page documents the package.
---

# OpenClaw Action Gate

Plugin bundle exported from SuperAda.ai for ClawHub discovery.

## Source
- SuperAda page: https://superada.ai/plugins/openclaw-action-gate/
- Source URL: https://github.com/h-mascot/agent-action-gate/tree/main/plugins/openclaw-action-gate
- Category: Security
- Status: Live

## Install

```bash
git clone --depth=1 https://github.com/h-mascot/agent-action-gate.git /tmp/agent-action-gate && mkdir -p plugins && cp -R /tmp/agent-action-gate/plugins/openclaw-action-gate plugins/openclaw-action-gate && (cd plugins/openclaw-action-gate && pnpm install --prod && pnpm run build) && openclaw plugins enable openclaw-action-gate
```

## What It Does

The OpenClaw-side runtime plugin for the Action Gate project. Hooks before_incoming_action, before_outbound_message, and after_outbound_message, applies the per-scope action-gate.json policy, and writes a per-decision audit record. This is the package you actually install; the Action Gate page on SuperAda documents the contract and use cases, this page documents the package.

## Verification
```bash
bash plugins/openclaw-action-gate/scripts/verify.sh --scope shared-room --non-owner ada
```
