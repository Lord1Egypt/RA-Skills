---
name: wahlu
description: Social media automation for AI agents. Create posts, schedule content, upload media, manage queues, track publications, organise ideas, and publish across Instagram, TikTok, LinkedIn, Facebook, and YouTube. AI-powered social media manager with full API access.
homepage: https://wahlu.com/openclaw
metadata: {"openclaw":{"emoji":"🦐","requires":{"env":["WAHLU_API_KEY"]},"primaryEnv":"WAHLU_API_KEY","install":[{"id":"npm","kind":"node","pkg":"@wahlu/cli","bins":["wahlu"],"label":"Install Wahlu CLI"}]}}
---

# Wahlu — Social Media Manager for AI Agents

Wahlu lets your agent create, schedule, and publish social media posts across **Instagram, TikTok, LinkedIn, Facebook, and YouTube** — all from the command line.

- **Website:** [wahlu.com](https://wahlu.com)
- **CLI on npm:** [@wahlu/cli](https://www.npmjs.com/package/@wahlu/cli)
- **API docs:** [wahlu.com/docs](https://wahlu.com/docs)
- **OpenClaw integration page:** [wahlu.com/openclaw](https://wahlu.com/openclaw)

---

## Setup

```bash
# Set your API key (get one at wahlu.com under Settings > API Keys)
export WAHLU_API_KEY=wahlu_live_...
```

No global install needed — use `npx @wahlu/cli` to run any command.

---

## Core Workflow

1. **List brands** — `npx @wahlu/cli brand list`
2. **Switch to a brand** — `npx @wahlu/cli brand switch <brand-id>`
3. **List integrations** — `npx @wahlu/cli integration list` (get integration IDs for scheduling)
4. **Create a post** — `npx @wahlu/cli post create --name "Title" --instagram '{"description":"Caption","post_type":"grid_post"}'`
5. **Schedule it** — `npx @wahlu/cli schedule create <content-item-id> --at 2026-03-15T14:00:00Z --integrations <id>`
6. **Upload media** — `npx @wahlu/cli media upload ./photo.jpg` (returns a media ID)
7. **Check publications** — `npx @wahlu/cli publication list`

Use `npx @wahlu/cli --help` and `npx @wahlu/cli <command> --help` to discover all commands and options. Always use `--json` when you need to parse output.

---

## What You Can Do

| Capability | Commands |
|---|---|
| **Post to 5 platforms** | `post create` with `--instagram`, `--tiktok`, `--facebook`, `--youtube`, `--linkedin` |
| **Schedule posts** | `schedule create` with `--at` (ISO 8601) and `--integrations` |
| **Upload images & video** | `media upload <file>` — supports PNG, JPG, GIF, WebP, MP4, MOV, WebM |
| **Manage posting queues** | `queue list`, `queue add <queue-id> <content-item-id>` |
| **Save content ideas** | `idea create "Name" --description "Details"` |
| **Organise with labels** | `label create "Campaign" --color "#ff5500"` |
| **View publish history** | `publication list` — see status, platform, failure reasons |
| **List connected accounts** | `integration list` — find integration IDs for scheduling |

---

## Platform-Specific Settings

Each platform has its own settings passed as JSON:

- **Instagram** — `--instagram '{"description":"...","post_type":"grid_post|reel|story","media_ids":["mid-123"]}'`
- **TikTok** — `--tiktok '{"description":"...","post_type":"video|image|carousel","media_ids":["mid-123"]}'`
- **Facebook** — `--facebook '{"description":"...","post_type":"fb_post|fb_story|fb_reel|fb_text","media_ids":["mid-123"]}'`
- **YouTube** — `--youtube '{"title":"...","description":"...","post_type":"yt_short|yt_video","media_ids":["mid-123"]}'`
- **LinkedIn** — `--linkedin '{"description":"...","post_type":"li_text|li_image|li_video","media_ids":["mid-123"]}'`

---

## Quick Examples

```bash
# Upload an image and create a cross-platform post
npx @wahlu/cli media upload ./photo.jpg
# → media ID: mid-abc123

npx @wahlu/cli post create --name "New product launch" \
  --instagram '{"description":"Just launched!","post_type":"grid_post","media_ids":["mid-abc123"]}' \
  --tiktok '{"description":"Just launched!","post_type":"image","media_ids":["mid-abc123"]}' \
  --linkedin '{"description":"Just launched!","post_type":"li_image","media_ids":["mid-abc123"]}'

# Schedule for tomorrow at 9am
npx @wahlu/cli schedule create <content-item-id> \
  --at 2026-03-15T09:00:00Z \
  --integrations int-123 int-456 int-789
```

---

## Rules

- Always confirm with the user before publishing or scheduling
- Use `npx @wahlu/cli integration list` to find integration IDs — never guess them
- Use ISO 8601 format for all dates
- Use `--json` flag when you need to parse command output programmatically
