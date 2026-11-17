---
name: reelsfarm-ai-avatars
description: Generate AI images of fictional people for marketing creatives with ReelsFarm (GPT Image, Nano Banana, Seedream, FLUX 3), start from reference templates, and edit results in follow-up turns. Needs a ReelsFarm account.
metadata:
  openclaw:
    emoji: "🧑‍🎤"
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

# ReelsFarm AI avatars

Generate AI images of people for marketing creatives with ReelsFarm, such as a creator-style selfie for a slideshow or a starting frame for a video. Edit a result in follow-up turns until it is right.

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

## Generate

```bash
reelsfarm avatars generate --prompt "Woman in her 20s taking a mirror selfie in a sunny kitchen, phone camera look" --model gpt-image-2.5-sunburst --aspect-ratio 9:16 --quality high --agent
```

- Models: `gpt-image-2.5-sunburst`, `gpt-image-2`, `nano-banana-2-1`, `nano-banana-2-pro`, `nano-banana-pro`, `seedream-5-pro`, and `flux-3`.
- `--quality`: `low`, `medium`, or `high` for GPT Image. Leave it out for Nano Banana. FLUX 3 takes `basic`, `high`, `ultra` (2K), or `max` (4K); bigger sizes cost more credits.
- `--aspect-ratio`: `9:16`, `4:5`, `3:4`, `1:1`, or `16:9`.
- `--style-mode`: `default`, `pinterest`, or `linkedin`.
- `--reference-url` starts from an existing ReelsFarm image.

Prices differ by model and quality, so check `reelsfarm account pricing --agent` and tell the user the cost before you run it.

## Start from a template

```bash
reelsfarm avatars templates --agent
```

Templates are reference photos of people and settings. Pass one as `--reference-url` and describe the person, outfit, and setting you want in the prompt. Follow `nextCursor` to see more.

## Edit a result

Keep the same person and change one thing at a time by continuing the conversation:

```bash
reelsfarm avatars generate --prompt "Same person, tighter crop, holding a coffee cup" --model gpt-image-2.5-sunburst --quality high --reference-url <previous image URL> --conversation-id <conversationId> --parent-generation-id <generationId> --agent
reelsfarm image-generations conversation --conversation-id <conversationId> --agent
```

Saved avatars are listed by `reelsfarm avatars list --agent`. To animate one, pass its `avatar.imageUrl` to the `reelsfarm-ai-videos` skill.

## Responsible use

- Make fictional people only. Don't recreate a real, identifiable person or a public figure, and don't edit a photo of someone who hasn't agreed to it.
- Don't present an AI person as a real customer, and don't write fake testimonials or reviews.
- Follow each platform's rules for labeling AI-generated content.
