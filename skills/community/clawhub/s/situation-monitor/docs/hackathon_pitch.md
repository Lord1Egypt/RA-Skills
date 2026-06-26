# Hackathon Pitch

## One-line pitch

We built `Situation Monitor` for teams living inside noisy operational
feeds so they can catch up instantly and act safely. The Discord lane uses
Redis, FriendliAI, and Civic; the `KubeWatch` lane uses Apify, Contextual,
Redis, and FriendliAI.

## Public-facing blurb

`Situation Monitor` is for the moment when Discord is exploding, the cluster is
misbehaving, and nobody has time to read everything. It pulls signal out of the
noise, ranks what matters, and turns operational chaos into a brief with
concrete next actions.

## Demo loop

### Discord lane

1. New Discord messages arrive in a test server.
2. The skill reads recent traffic from a few selected channels.
3. Redis remembers checkpoints and the latest digest.
4. FriendliAI turns the raw feed into a concise situation report.
5. The user drafts a response for one item.
6. Sending stays blocked until Civic approvals are wired.

### KubeWatch lane

1. Apify pulls public K8s or cloud status incidents.
2. Redis deduplicates and stores incident history.
3. Contextual matches the incident to a relevant runbook.
4. The skill emits a priority, summary, and grounded remediation steps.
5. The operator can cross-check against the local `02-incidents.sh` drill.

## Why this should exist

- Discord teams lose time scanning channels for blockers, asks, and deadlines.
- SRE teams lose time checking multiple status pages and hunting through
  runbooks under pressure.
- The workflow is clear in twenty seconds.
- The prototype can become a real installable ops tool without changing the core
  story.

## Demo-safe data policy

- Use a fresh hackathon Discord server.
- Use synthetic or team-consented test data only.
- Do not use personal exports or private account history.
