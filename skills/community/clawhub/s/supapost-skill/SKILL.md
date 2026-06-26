---
name: supapost
version: 1.0.1
description: Generate AI images and video, build TikTok slideshows, manage AI influencers, and schedule posts to TikTok / Instagram / YouTube / X through the Supapost MCP. Use whenever the user asks to create social content, run image-to-video, lock a character identity, or queue posts across connected accounts.
license: MIT-0
homepage: https://supapost.so/developers/openclaw
repository: https://github.com/supapost-dev/skills
documentation: https://supapost.so/developers/mcp
keywords:
  - supapost
  - mcp
  - tiktok
  - ai-influencer
  - content-generation
  - scheduler
metadata:
  openclaw:
    requires:
      env:
        - SUPAPOST_API_KEY
      bins: []
    primaryEnv: SUPAPOST_API_KEY
    mcp:
      transport: streamable-http
      url: https://mcp.supapost.so
      auth: oauth
---

# Supapost

Supapost is an end-to-end studio for AI-native content creators. This skill teaches your agent how to drive Supapost via its MCP server.

## Installing this skill

Use the [vercel-labs/skills](https://github.com/vercel-labs/skills) CLI to drop the `SKILL.md` into your coding agent's skills folder (Claude Code, Cursor, OpenCode, OpenClaw, etc.):

```bash
npx skills add supapost-dev/skills
```

Or download the raw file from **https://supapost.so/skill.md**.

## Connecting the MCP

Installing the skill only teaches the agent *how* to use Supapost. To actually call tools, connect the Supapost MCP. Create an API key at **https://supapost.so/settings/developer** (keys start with `sp_`), then pick the install for your client.

**Claude Code (CLI):**

```bash
claude mcp add --transport http supapost \
  https://mcp.supapost.so \
  --header "Authorization: Bearer sp_..."
```

**Cursor / Windsurf / VS Code / any MCP client** — add to `~/.cursor/mcp.json` (or `.mcp.json` in the project root):

```json
{
  "mcpServers": {
    "supapost": {
      "url": "https://mcp.supapost.so",
      "headers": { "Authorization": "Bearer sp_..." }
    }
  }
}
```

**Verify the connection.** After registering, call `list_models` once. A valid key returns a JSON list. A `401 Invalid API key` means the key is wrong, expired, or missing the `sp_` prefix — regenerate it at https://supapost.so/settings/developer.

**Local stdio (MCP developers only):** if you need to run the server locally against a custom `SUPAPOST_API_URL`, use the stdio package: `claude mcp add supapost --env SUPAPOST_API_KEY=sp_... -- npx -y @supapost/mcp`.

## Tools at a glance

Reads: `list_models`, `list_influencers`, `list_products`, `list_projects`, `get_project`, `list_scheduled_posts`, `list_assets`, `list_social_accounts`, `list_stores`.

Writes: `generate_image`, `generate_video`, `generate_slides`, `create_influencer`, `update_influencer`, `delete_influencer`, `upsert_project`, `delete_project`, `schedule_post`, `update_scheduled_post`, `delete_scheduled_post`, `publish_tiktok`, `delete_asset`.

## Core concepts

- **Influencer = identity anchor.** An influencer has a first-generation image that locks the face. Pass `influencer_id` to `generate_image` / `generate_video` to keep the character consistent across scenes.
- **Projects** are containers — a slide deck, an influencer workspace, or a video. Use `upsert_project` to create or update; `generate_slides` creates a slides project in one call.
- **Assets** are generated or uploaded media. Generation tools are async — results appear as assets when the job completes.
- **Scheduled posts** are queued with `scheduled_at` as an ISO 8601 future datetime. Delivery is handled by Cloudflare Queues.

## Canonical workflows

### 1. Build a TikTok deck from a prompt

1. `generate_slides` with `{ prompt: "<topic + angle + tone>" }`.
2. The response contains a project with slides. Review with the user.
3. Optional: `upsert_project` to tweak metadata (name, status) only.

> **Don't use `upsert_project` to author slide content from scratch.** The
> editor stores slides as positioned `layers` with full typography and
> positioning metadata. `generate_slides` produces that shape correctly.
> Hand-rolling JSON through `upsert_project` will save but the editor may
> render blank slides.

### 2. Create a consistent AI influencer

1. `generate_image` with the character description. Pick the best output.
2. `create_influencer` with that image URL in `images[]`. The first image becomes the identity anchor.
3. For every new scene, call `generate_image` with `influencer_id` set. Do **not** restate the character in the prompt — describe scene, pose, outfit, lighting only.

### 3. Animate a still into video

1. Find or generate a source image URL (from `list_assets` or `generate_image`).
2. `generate_video` with `{ prompt, reference_images: [url], model: "kling-2.5-turbo-pro", duration: 5 }`.
3. Keep prompts under ~40 words: camera move → subject action → environment.

### 4. Schedule a TikTok slideshow for next Tuesday 9am

1. `list_social_accounts` → find the TikTok account id.
2. `schedule_post` with `platform: "tiktok"`, `social_account_id`, `scheduled_at` (ISO 8601, future), and either a `project_id` (existing slide deck) or `image_urls[]`.

### 5. Publish to TikTok drafts right now

`publish_tiktok` with `{ account_id, image_urls, title }`. This creates a TikTok draft the user reviews in the TikTok app before going live.

## Rules

- **Never** paste the user's `SUPAPOST_API_KEY` into logs, files, prompts, or tool args. It lives only in the MCP env.
- **Always** list before writing when the user references something by name ("my Emma influencer", "the summer sale project") — call `list_influencers` / `list_projects` / `list_stores` to resolve the id first.
- **Always** confirm destructive actions (`delete_*`) with the user before calling.
- **Scheduled posts:** verify `scheduled_at` is in the future and in ISO 8601 with timezone (e.g. `2026-05-01T09:00:00Z`).
- **Images must be URLs**, not base64. If the user pastes a local file, upload it first through the web app and use the resulting URL.
- **Generation is async.** `generate_image` / `generate_video` return a job id. Surface that to the user rather than pretending the asset is ready.
- **Models:** prefer the team default (leave `model` unset) unless the user asks for a specific one. Use `list_models` to show options.

## Errors

The API returns `{ message: "..." }` on failure with an HTTP status. Common cases:

- `401 Invalid API key` — key is wrong, expired, or missing the `sp_` prefix.
- `403 No team found` — key isn't linked to a team; user needs to recreate it.
- `404 Not found` — bad id, or the resource belongs to a different team.
- `400` — validation error; surface the message verbatim.

## Docs

- Product: https://supapost.so
- Developer portal: https://developers.supapost.so
- API keys: https://supapost.so/settings/developer
