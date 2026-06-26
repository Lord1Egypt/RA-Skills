# Situation Monitor

`Situation Monitor` is an OpenClaw skill and demo app for two closely
related workflows:

- turning noisy Discord activity into a ranked situation report
- turning Kubernetes incident feeds into grounded remediation actions

The repo is hackathon-shaped. Both lanes work with fixture data immediately,
and each lane upgrades to live sponsor integrations when you add keys.

Important: this same repo now serves two purposes:

- the Python/OpenClaw skill and local CLI
- the repo-root Apify actor that feeds live KubeWatch incidents

## Project pitch

We built `Situation Monitor` for teams drowning in noisy operational
signals so they can catch up instantly and act safely. The Discord lane uses
Redis, FriendliAI, and Civic. The `KubeWatch` lane uses Apify for live incident
collection, Contextual for runbook grounding, Redis for state, and FriendliAI
for fast summaries and drafts.

## Public description

`Situation Monitor` is for the moment when Discord is exploding, the cluster is
misbehaving, and nobody has time to read everything. It pulls signal out of the
noise, ranks what matters, and turns operational chaos into a brief with
concrete next actions.

## What is working now

- Fixture mode with realistic sample Discord traffic
- Fixture mode with realistic Kubernetes incident traffic
- Ranked digest generation with deterministic heuristics
- Optional FriendliAI refinement for executive summaries and reply drafts
- Redis-backed checkpoint and latest-report storage
- Live Discord snapshot mode for bot-visible channels only
- KubeWatch fixture triage with runbook grounding from local docs
- KubeWatch live intake via Apify actor results when `APIFY_TOKEN` is present
- Outbound actions blocked by default until Civic is configured

## Repo layout

- `SKILL.md`: OpenClaw skill entrypoint
- `src/monitoring_the_situation/`: app code
- `examples/demo_messages.json`: synthetic Discord fixture
- `examples/kubewatch_incidents.json`: synthetic K8s incident fixture
- `docs/context/`: local runbooks for KubeWatch grounding
- `02-incidents.sh`: cluster incident trigger/fix script pulled from the team
- `docs/hackathon_pitch.md`: demo positioning and sponsor story
- `tests/`: lightweight regression coverage

## Quick start

```bash
cd /Users/sarahhatcher/Documents/monitoring-the-situation-openclaw
cp .env.example .env
bash scripts/mts --help
```

If you want to run the Apify actor locally too:

```bash
npm install
```

Run the offline demo:

```bash
bash scripts/mts fixture --input examples/demo_messages.json --save-path .local/demo_report.md
bash scripts/mts kubewatch-fixture --input examples/kubewatch_incidents.json --save-path .local/kubewatch_report.md
```

Run tests:

```bash
source .venv/bin/activate
pytest
```

## Live Discord mode

Add a fresh hackathon-only Discord bot token to `.env`, then set:

- `DISCORD_BOT_TOKEN`
- `DISCORD_GUILD_ID`
- `DISCORD_CHANNEL_IDS`

The bot must have access to the target channels, and Discord must allow message
content for the bot if you want the actual text payloads summarized.

Fetch a one-shot live snapshot:

```bash
bash scripts/mts discord-fetch --hours 24 --limit-per-channel 75 --save-path .local/live_report.md
```

## KubeWatch mode

`KubeWatch` is the SRE lane in this same skill bundle. It ingests incident feed
items, deduplicates them, grounds remediation on runbooks, and emits a
demo-friendly triage report.

Run the fixture path:

```bash
bash scripts/mts kubewatch-fixture --input examples/kubewatch_incidents.json --save-path .local/kubewatch_report.md
```

Run the live Apify path once sponsor keys are available:

```bash
bash scripts/mts kubewatch-apify --actor-id "$APIFY_ACTOR_ID" --save-path .local/kubewatch_live_report.md
```

If you want to send explicit actor input:

```bash
bash scripts/mts kubewatch-apify \
  --actor-id "$APIFY_ACTOR_ID" \
  --actor-input examples/apify_actor_input.json \
  --save-path .local/kubewatch_live_report.md
```

Inspect recent incident history:

```bash
bash scripts/mts kubewatch-history --limit 5
```

Scan the real cluster from `KUBECONFIG` or `.local/kubeconfig`:

```bash
bash scripts/mts kubewatch-cluster --namespace production --save-path .local/kubewatch_cluster_report.md
```

## Hosted OpenClaw / Donely setup

The skill is now packaged so the gateway can bootstrap it from the skill
directory itself. The wrapper at `scripts/mts` creates `.venv` on first run and
installs the Python package automatically.

If you are handing this off to the person who has access to OpenClaw, send them
[docs/openclaw_admin_install.md](/Users/sarahhatcher/Documents/monitoring-the-situation-openclaw/docs/openclaw_admin_install.md).

## Contextual upload bundle

Prepare the exact runbook bundle for Contextual with:

```bash
cd /Users/sarahhatcher/Documents/monitoring-the-situation-openclaw
python3 scripts/prepare_contextual_upload.py
```

That generates:

- `dist/contextual-upload/runbooks/`: the markdown files to upload
- `dist/contextual-upload/manifest.json`: machine-readable file list
- `dist/contextual-upload/README.md`: verification queries and expected matches

Upload only the runbooks in that bundle to the Contextual agent backing
`CONTEXTUAL_AGENT_ID`. Do not mix in unrelated repo docs.

Shortest path:

1. Publish or install the skill into the Donely/OpenClaw instance.
2. Put the required env vars on the gateway host or in the OpenClaw skill
   config:
   - `REDIS_URL`
   - `FRIENDLI_TOKEN`
   - `APIFY_TOKEN`
   - `APIFY_ACTOR_ID`
   - `CONTEXTUAL_API_KEY`
   - `CONTEXTUAL_AGENT_ID`
   - `KUBECONFIG`
   - `KUBE_NAMESPACE=production`
3. Start a new OpenClaw session so the new skill is loaded.
4. Ask OpenClaw to use `Situation Monitor` for one concrete task.

Recommended first prompt in Donely:

```text
Use Situation Monitor to run the KubeWatch cluster scan for the production namespace and summarize anything urgent.
```

Recommended second prompt:

```text
Use Situation Monitor to run KubeWatch from Apify and tell me the highest-priority incident plus the next actions.
```

## Apify actor instructions

The Apify actor is defined at the repo root:

- `main.js`: actor entrypoint
- `INPUT_SCHEMA.json`: Apify input form
- `package.json`: actor runtime dependencies

The actor fetches:

- recent GCP status incidents relevant to K8s, GKE, networking, and ingress
- unresolved GitHub status incidents
- open `kubernetes/kubernetes` issues labeled `kind/bug` and `priority/critical-urgent`

If the live sources return nothing, the actor falls back to
`examples/kubewatch_incidents.json` so the demo still shows a stable loop.

### Build or rebuild the actor in Apify

1. Keep the Apify actor pointed at the repo root with no subfolder override.
2. Pull the latest `origin/main` in GitHub.
3. In Apify, trigger a new build for `hatchingsunrise/monitoring-the-situation-openclaw`.
4. Run the actor with the default input or `examples/apify_actor_input.json`.
5. Confirm the run writes dataset items before calling `mts kubewatch-apify`.

### Run the actor locally before pushing

```bash
cd /Users/sarahhatcher/Documents/monitoring-the-situation-openclaw
npm install
node main.js
```

That creates a local Apify dataset under `storage/` so you can confirm the
actor is returning normalized incident records.

### Minimum actor input

`examples/apify_actor_input.json` is the default demo-safe input:

```json
{
  "includeGcpStatus": true,
  "includeGithubStatus": true,
  "includeKubernetesGithubIssues": true,
  "gcpLookbackDays": 365,
  "maxGcpIncidents": 6,
  "githubIssuesLimit": 6,
  "useFixtureWhenEmpty": true,
  "fixturePath": "examples/kubewatch_incidents.json"
}
```

## Incident drill script

The pulled [02-incidents.sh](/Users/sarahhatcher/Documents/monitoring-the-situation-openclaw/02-incidents.sh)
script is now part of the demo story. It injects the same failure classes that
the KubeWatch lane knows how to classify:

- `trigger1`: OOM / CrashLoop on `payment-processor`
- `trigger2`: bad image tag / `ImagePullBackOff` on `user-service`
- `trigger3`: repeat OOM pattern on `analytics-worker`

Use it with a hackathon-only GKE cluster if you want the extra live angle. The
fixture path remains the safe fallback.

## Sponsor usage

- `Redis`: report state, checkpoints, incident dedup, and history
- `FriendliAI`: concise summaries and reply drafts
- `Civic`: fail-closed approval gate for outbound actions
- `Apify`: public cloud/K8s incident intake for KubeWatch
- `Contextual`: runbook-grounded remediation guidance for KubeWatch

## Redis and FriendliAI

If `REDIS_URL` is set, the app stores the latest report and channel checkpoints
in Redis. If `FRIENDLI_TOKEN` is set, the app uses Friendli's OpenAI-compatible
endpoint to rewrite the executive summary and draft replies with lower latency
than the fallback heuristic layer.

If either variable is missing, the app falls back safely:

- no Redis: local JSON state in `.local/`
- no Friendli token: deterministic local digesting and templated drafts

For KubeWatch specifically:

- no Apify token: use `examples/kubewatch_incidents.json`
- no Contextual key: ground against local markdown runbooks in `docs/context/`
- no `KUBECONFIG`: the live cluster scan will fail with a clear local-only error

## Civic stance

This repo treats outbound posting as sensitive. Draft generation is supported,
but actual send actions stay blocked until you wire a real Civic-backed approval
flow. That keeps the demo honest and avoids fake claims about trust or auth.

## Publish as a skill

OpenClaw skills are directory bundles rooted at `SKILL.md`. This repo is ready
to publish directly to ClawHub from the repo root when you want:

```bash
clawhub publish . \
  --slug situation-monitor \
  --name "Situation Monitor" \
  --version 0.1.0 \
  --tags latest
```
