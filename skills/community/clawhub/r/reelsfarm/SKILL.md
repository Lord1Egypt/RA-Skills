---
name: reelsfarm
description: Use the ReelsFarm CLI to make short-form marketing content with AI (TikTok and Instagram slideshows, AI avatar images, product photos, AI videos) and schedule approved posts to your own TikTok, Instagram, YouTube and Facebook accounts. Covers setup, discovery and safe confirmation. Needs a ReelsFarm account.
metadata:
  openclaw:
    emoji: "🌾"
    homepage: https://reelsfarm.com/docs/mcp
    primaryEnv: REELSFARM_API_KEY
    requires:
      bins:
        - reelsfarm
      env:
        - REELSFARM_API_KEY
    envVars:
      - name: REELSFARM_API_KEY
        required: true
        description: ReelsFarm MCP API key (starts with rfmcp_), created in the MCP tab of the ReelsFarm account.
    install:
      - kind: node
        package: "@reelsfarm/mcp-client"
        bins:
          - reelsfarm
---

# ReelsFarm

ReelsFarm (https://reelsfarm.com) makes short-form marketing content with AI and publishes it to the user's own social accounts. This skill covers setup, discovery, and the rules every ReelsFarm command follows. Separate skills cover each workflow: `reelsfarm-tiktok-slideshows`, `reelsfarm-ai-avatars`, `reelsfarm-product-photos`, `reelsfarm-ai-videos`, and `reelsfarm-social-scheduler`.

## Setup

1. Install the CLI: `npm install -g @reelsfarm/mcp-client`. It provides the `reelsfarm` command.
2. Create an MCP API key in the MCP tab of the ReelsFarm account and set it as `REELSFARM_API_KEY`. The key is shown only once.
3. Check the connection: `reelsfarm agent status` and `reelsfarm account status --agent`.

ReelsFarm is a paid service (https://reelsfarm.com). Creating media spends credits from the user's plan or trial. Without one, commands that create or publish return a link to choose a plan. Credential, connection-mode, and permanent-delete settings stay in the ReelsFarm dashboard and are not in the CLI.

## Running actions

- Always add `--agent`. It prints one JSON object with `ok`, `data` or `error`, and a `nextStep` hint.
- Preview first with `--dry-run`. Nothing runs on the server. Tell the user what will be made and what it costs; `reelsfarm account pricing --agent` lists credit prices.
- After the user approves, run the same command with `--yes --wait`. `--yes` confirms only the action the server prepared. It never changes the account's connection mode. `--wait` waits for the job to finish.
- If a response has `requiresConfirmation: true`, ask the user, then run its `nextStep` (`reelsfarm confirm <id> --tool <tool> --agent`). If that returns an operation id, follow it with `reelsfarm operations wait --id <operationId> --agent`.
- Give each action one `--idempotency-key` and reuse it only to retry that same action after a timeout. Never start a second copy while the first may still be running.

## Results

Say an image, video, or slideshow exists only when the response shows `executionState: "COMPLETED"`, `assetCreated: true`, and a ReelsFarm asset id and URL. `PREPARED` or `NOT_STARTED` means nothing ran. `ENQUEUED` or `PROCESSING` means it is not finished. When the user asked for ReelsFarm, don't swap in another image or video generator.

## Discover before acting

```bash
reelsfarm agent status
reelsfarm agent commands
reelsfarm account status --agent
reelsfarm social connected --agent
reelsfarm media-collections gallery --kinds COLLECTION,AVATAR --agent
reelsfarm slideshows list --agent
reelsfarm videos list --agent
reelsfarm posts list --agent
```

`agent commands` lists every command with its arguments. When a list takes `--limit` or `--cursor`, follow `nextCursor` until `hasMore` is false.

## Connection modes

The account owner picks the mode in the ReelsFarm dashboard. The CLI cannot change it.

- Review: every create or publish action is prepared first and needs confirmation.
- Creator: content is created right away, but publishing and automations are blocked.
- Autopilot: publishing and automations also run right away, within credits and plan limits.

Even in Creator or Autopilot, ask the user before anything that spends credits or posts publicly.

## Common errors

- `AUTHENTICATION_REQUIRED`: `REELSFARM_API_KEY` is missing, revoked, or mistyped.
- `VIDEO_JOB_IN_PROGRESS`: one video job runs at a time per account. Wait for the job the message names, then run the command again.
- An unclear response after a create command: check `reelsfarm operations get --id <operationId> --agent` before you try again.
