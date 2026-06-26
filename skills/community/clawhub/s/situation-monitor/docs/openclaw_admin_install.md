# Situation Monitor: OpenClaw Admin Install

This guide is for the person who has access to the hosted OpenClaw / Donely
instance.

## What you are installing

`Situation Monitor` is an OpenClaw skill with two lanes:

- `KubeWatch`: live Kubernetes incident triage from Apify + cluster status
- Discord situation summaries: optional, only if Discord bot credentials are set

The fastest live demo path is `KubeWatch`.

## One-time install path

1. Install or publish the skill from the repo root:

```bash
cd /Users/sarahhatcher/Documents/monitoring-the-situation-openclaw
clawhub publish . --slug situation-monitor --name "Situation Monitor" --version 0.1.2 --tags latest
```

2. In the OpenClaw / Donely instance, install `situation-monitor`.

3. Make sure the hosted gateway has these environment variables:

- `REDIS_URL`
- `FRIENDLI_TOKEN`
- `APIFY_TOKEN`
- `APIFY_ACTOR_ID`
- `CONTEXTUAL_API_KEY`
- `CONTEXTUAL_AGENT_ID`
- `KUBECONFIG`
- `KUBE_NAMESPACE=production`

Optional Discord lane:

- `DISCORD_BOT_TOKEN`
- `DISCORD_GUILD_ID`
- `DISCORD_CHANNEL_IDS`

4. Prepare and upload the Contextual runbooks:

```bash
cd /Users/sarahhatcher/Documents/monitoring-the-situation-openclaw
python3 scripts/prepare_contextual_upload.py
```

Then upload every markdown file from `dist/contextual-upload/runbooks/` into the
single Contextual agent or KB used by `CONTEXTUAL_AGENT_ID`.

5. Start a new OpenClaw session so the skill is reloaded.

## Why this install is now safer

The skill no longer depends on a manual Python setup step. It includes a helper
wrapper at `scripts/mts` that:

- creates `.venv` on first run
- installs the Python package automatically
- runs the CLI entrypoint consistently

That means the OpenClaw runtime can execute the skill from the skill directory
without a separate bootstrap session.

## First prompts to run in OpenClaw

Use these first:

```text
Use Situation Monitor to run the KubeWatch cluster scan for the production namespace and summarize anything urgent.
```

```text
Use Situation Monitor to run KubeWatch from Apify and tell me the highest-priority incident plus the next actions.
```

## Expected first result

- If the cluster is healthy, the cluster scan should report no incidents.
- The Apify path should return live public incidents from the actor.
- If Discord is not configured yet, the KubeWatch lane still demos cleanly.

## Contextual verification

Use the verification queries in `dist/contextual-upload/README.md` after upload.
The important thing is that these classes of incident retrieve the right
documents:

- OOM / CrashLoop memory issues
- bad image deploys
- cluster networking degradation
- GKE control-plane degradation
- ingress `502` failures

## If the skill installs but does not run

Check these first:

- `python3` exists on the gateway host
- the gateway can read the required env vars
- `KUBECONFIG` points to a real file on the gateway host
- `APIFY_ACTOR_ID` matches the live actor
- start a fresh session after install or update
