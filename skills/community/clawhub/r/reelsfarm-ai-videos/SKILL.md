---
name: reelsfarm-ai-videos
description: Generate short AI videos with ReelsFarm from a prompt, start and end frames, or reference images (Seedance, Veo, Gemini Omni), and turn an avatar image into a hook clip that opens with a reaction. Needs a ReelsFarm account.
metadata:
  openclaw:
    emoji: "🎬"
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

# ReelsFarm AI videos

Generate short AI videos with ReelsFarm: from a text prompt, from a start frame (optionally with an end frame), or from reference images. You can also turn a ReelsFarm avatar image into a hook clip that opens with a reaction.

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

One video job runs at a time per account. If you get `VIDEO_JOB_IN_PROGRESS`, wait for the job it names to finish, then run the command again. Don't start a replacement while that job is still running.

## Videos from a prompt, frames, or references

```bash
reelsfarm videos generate --prompt "Slow push-in on a latte on a sunny cafe table" --model seedance-2.5 --duration 8 --aspect-ratio 9:16 --category product --agent
reelsfarm videos status --job-id <jobId> --agent
```

- Models: `seedance-2.5` (default), `seedance-2`, `seedance-2-fast`, `veo-3.1`, `veo-3.1-fast`, and `gemini-omni-1.1-flash` (needs `--include-audio`). Each supports its own durations, aspect ratios (`9:16`, `16:9`, `1:1`), and resolutions (`720p`, `1080p`). Read them under `videoGeneration` in `reelsfarm account pricing --agent` before you choose.
- Frames: `--first-frame-url` and an optional `--last-frame-url`.
- References: `--reference-image-urls` (up to three), plus `--reference-video-url` and `--reference-audio-url` on Seedance models only. Don't combine frames with references.
- With a start frame of a person, `--motion-preset` opens with a reaction: `shocked`, `grateful`, `looks_up`, `fed_up`, `confident`, `nod_smile`, or `subtle_pan`.
- Spoken lines in quotes in the prompt get natural delivery. Pass `--no-natural-speech` to send them exactly as written.
- `--category` files the result under `people`, `product`, or `scenes`.

Use only ReelsFarm asset URLs for frames and references.

A video exists only when `videos status` reports `COMPLETED` with `assetCreated: true` and a `video` object. To publish it, use the `reelsfarm-social-scheduler` skill with content type `ugc-video` and that `video.id`.

## Hook clips from an avatar

Animate a finished ReelsFarm avatar (see the `reelsfarm-ai-avatars` skill). Wait until the avatar job is `COMPLETED`, then pass its `avatar.imageUrl`:

```bash
reelsfarm hooks generate --avatar-url <avatar.imageUrl> --preset shocked --model seedance-2.5 --duration 5 --agent
```

- Presets: `shocked`, `grateful`, `looks_up`, `fed_up`, `confident`, `nod_smile`, `subtle_pan`, and `surprised_reaction`.
- Models: `seedance-2.5`, `seedance-2`, `seedance-2-fast`, `veo-3.1`, and `veo-3.1-fast`.
- `--custom-prompt` describes the motion. `--script-text` with `--include-audio` adds a spoken line.

Saved hooks are listed by `reelsfarm hooks list --agent`.

Don't make videos that show a real, identifiable person without their consent, and don't present AI people as real customers.
