---
name: reelsfarm-social-scheduler
description: Schedule or publish approved ReelsFarm slideshows and videos to your own connected TikTok, Instagram, YouTube and Facebook accounts, with caption checks, per-platform settings from preflight, and best posting times. Needs a ReelsFarm account.
metadata:
  openclaw:
    emoji: "🗓️"
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

# ReelsFarm social scheduler

Schedule or publish finished ReelsFarm content to the user's own connected TikTok, Instagram, YouTube, and Facebook accounts. Every post needs the user's explicit approval of the account, content, caption, and time.

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

## 1. Pick the account and content

```bash
reelsfarm social connected --agent
reelsfarm slideshows list --agent
reelsfarm videos list --agent
```

Accounts are connected in the ReelsFarm dashboard; the CLI can't add new ones. Use the `connectionId` of the account the user chose. Content types are `slideshow`, `ugc-video`, and `avatar`. Publish formats are `video`, `photo`, and `carousel`.

## 2. Check before posting

```bash
reelsfarm validate caption "Cold brew in 3 steps #coffee" --platforms tiktok,instagram --agent
reelsfarm posts preflight --content-type slideshow --content-id <id> --publish-format carousel --connection-ids <connectionId> --agent
```

Preflight returns each target's `settingsSchema`, `rules`, and `limits`. Fill every required setting from that schema for the chosen account; settings differ between accounts and platforms. Run preflight again if the content, format, or account changes.

## 3. Schedule or publish

```bash
reelsfarm posts optimal-times --platform tiktok --agent
reelsfarm posts schedule --content-type slideshow --content-id <id> --when 2026-11-05T17:00:00Z --publish-format carousel --platforms tiktok:<connectionId> --caption "Cold brew in 3 steps" --agent
reelsfarm posts publish-now --content-type ugc-video --content-id <id> --platforms-json '[{"platform":"TIKTOK","connectionId":"<connectionId>","tiktokPublishMode":"DIRECT","tiktokPrivacyLevel":"PUBLIC_TO_EVERYONE"}]' --caption "New drop" --agent
```

Use `--platforms-json` when a target needs settings from preflight, such as `tiktokPrivacyLevel` or `instagramShareToFeed`. Show the user the exact post before you run it with `--yes`. Publishing in Review mode needs a confirmation. Creator mode can't publish, and only the account owner can change the mode.

## 4. Follow up

```bash
reelsfarm posts list --agent
reelsfarm posts status --id <postId> --agent
reelsfarm posts cancel --id <postId> --agent
```

## Rules

- Post only to accounts the user owns and connected themselves, and only content the user approved.
- One approval covers one post. Don't turn a single approval into a series of posts.
- No spam, repeated duplicate posts, fake engagement, or posting to get around a platform ban or limit.
