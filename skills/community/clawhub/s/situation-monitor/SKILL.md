---
name: situation_monitor
description: Triages Discord activity and Kubernetes incidents into ranked situation reports with fixture-first demos, live Discord and Apify intake, Contextual-grounded runbooks, Redis-backed memory, Friendli-powered drafting, and approval-gated outbound actions.
metadata:
  openclaw:
    requires:
      bins: ["bash", "python3"]
---

# Situation Monitor

Use this skill when the user wants to catch up on Discord traffic, monitor a
few noisy channels, triage Kubernetes incidents, produce a digest, or draft a
safe follow-up.

Use the helper wrapper at `scripts/mts` for all commands. It bootstraps `.venv`
and installs the package on first run, which makes hosted OpenClaw installs far
more reliable than calling `python3 -m monitoring_the_situation.cli` directly.

## Guardrails

- Never use a user token or self-bot. Live mode requires a Discord bot token.
- Prefer fixture mode when a live Discord bot is not configured yet.
- Do not ingest personal or private account history for demos.
- Prefer public status pages, public incident feeds, and synthetic cluster
  incidents for KubeWatch unless the user explicitly provides other sources.
- Treat outbound posting as sensitive. Drafts are allowed; sending stays blocked
  until Civic approval is configured.

## Working modes

1. Discord fixture mode for a safe demo:

```bash
bash scripts/mts fixture \
  --input examples/demo_messages.json \
  --save-path .local/demo_report.md
```

2. Live Discord snapshot mode after bot setup:

```bash
bash scripts/mts discord-fetch \
  --hours 24 \
  --limit-per-channel 75 \
  --save-path .local/live_report.md
```

3. Draft a reply for a specific report item:

```bash
bash scripts/mts draft-reply \
  --bucket urgent \
  --channel api-alerts
```

4. KubeWatch fixture mode for the SRE lane:

```bash
bash scripts/mts kubewatch-fixture \
  --input examples/kubewatch_incidents.json \
  --save-path .local/kubewatch_report.md
```

5. KubeWatch live intake from Apify after sponsor setup:

```bash
bash scripts/mts kubewatch-apify \
  --actor-id "$APIFY_ACTOR_ID" \
  --actor-input examples/apify_actor_input.json \
  --save-path .local/kubewatch_live_report.md
```

6. KubeWatch live cluster scan against the demo namespace:

```bash
bash scripts/mts kubewatch-cluster \
  --namespace production \
  --save-path .local/kubewatch_cluster_report.md
```

7. Rebuild and sanity-check the Apify actor when the repo changes:

```bash
cd /Users/sarahhatcher/Documents/monitoring-the-situation-openclaw
npm install
node main.js
```

The actor lives at the repo root, so Apify should stay pointed at the root with
no folder override.

## Expected output

Produce a report with:

- An executive summary
- Urgent threads
- Direct asks
- Decisions and deadlines
- FYI items
- Source citations by channel/message
- Incident priorities and grounded remediation steps for KubeWatch

If the user asks to send a message instead of drafting one, explain that the
repo is intentionally fail-closed until Civic-backed approvals are wired.
