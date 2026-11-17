---
name: shapeless
description: Drive the user's ShapelessAI account - draft and publish social posts, run durable content jobs, manage standing agents and Brand Memory. Use when the user asks to create, review, schedule, or publish social content, or to check on their ShapelessAI jobs, posts, agents, or brand.
---

# Driving ShapelessAI

ShapelessAI runs the user's social presence. You reach it through the `shapeless` MCP tools this
plugin ships (or the `shapeless` CLI, same surface). Everything is one account, gated by a
credential - the OAuth sign-in or an API key - with scopes: `read`, `write`, `publish`. Only
`publish` puts content into the world.

## The documentation

Do not guess this API. It is published, and it answers Markdown:

- **https://shapelessai.com/docs** - one page per subject. Append `.md` to any path
  (`https://shapelessai.com/docs/posts.md`) or send `Accept: text/markdown` to get the source
  instead of the page.
- **https://shapelessai.com/llms-full.txt** - every page in one fetch. Read this when you need the
  whole surface; read a single `.md` page when you need one answer.
- **https://shapelessai.com/api/openapi.json** - OpenAPI 3.1 for every route.

Straight to the page you need: [posts](https://shapelessai.com/docs/posts.md) ·
[platforms](https://shapelessai.com/docs/platforms.md) · [api](https://shapelessai.com/docs/api.md) ·
[jobs](https://shapelessai.com/docs/jobs.md) · [mcp tools](https://shapelessai.com/docs/mcp.md) ·
[brand memory](https://shapelessai.com/docs/brand-memory.md) ·
[auth](https://shapelessai.com/docs/auth.md).

## First contact

Call `me` to confirm the credential works and see the plan and credit balance. If it fails, the user
signs in over OAuth: run `/mcp`, pick shapeless, choose Authenticate, and allow in the browser tab.
The stdio fallback (`npx shapelessai mcp`) needs a key instead: minted at
https://shapelessai.com/studio/api-keys, then `shapeless login` or `export SHAPELESS_API_KEY=slk_...`.

**No `me` tool at all?** Then this skill arrived without its server (a ClawHub or skills.sh
install carries only this file). The server is hosted at `https://shapelessai.com/mcp`
(Streamable HTTP, OAuth, nothing to run locally). Add it once, then sign in; the browser tab
that opens also creates the account when the user has none, and the Free plan is enough to post:

```bash
# OpenClaw
openclaw mcp set shapeless '{"url":"https://shapelessai.com/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login shapeless

# Claude Code
claude mcp add --transport http --scope user shapeless https://shapelessai.com/mcp   # then /mcp, Authenticate

# Codex
codex mcp add shapeless --url https://shapelessai.com/mcp && codex mcp login shapeless
```

Every other host (Hermes, Cursor, Gemini CLI, ChatGPT, Claude, Grok, Perplexity) has its steps at
https://shapelessai.com/connect. Tell the user which command you ran and that one sign-in is
theirs to do; the tools appear once the host reloads its servers (the next turn or session).

## The shape of the work

- **Jobs** are durable server-side runs: `jobs_create` with a goal ("draft three posts about the
  beta launch") returns an id and keeps going whether or not you stay attached. `jobs_list` lists
  them, `jobs_get` shows the transcript and outputs, `jobs_brief` is the compact version for
  continuing, `jobs_tail` watches a run live, `jobs_run` presses Run on a proposed plan,
  `jobs_continue` resumes a stuck or finished run with new instructions, and `jobs_stop` stops
  one. Prefer a job for anything generative - posts, carousels, images, narrated video - the
  server holds the account's Brand Memory, connected platforms, and media pipeline.
- **Media rides the message** as `mediaKeys`: anything already in the account (`assets_list`).
  Up to 6 per message. The agent reads them for real - an image's pixels, not just its filename.
  The hosted server has no disk, so a local file goes in first with the CLI
  (`shapeless assets upload ./file`) or `PUT /api/brain/assets/{filename}`, which returns the key.
- **Posts** are the queue: proposed -> scheduled -> published. `posts_list` / `posts_get` to
  review, `posts_approve` to accept a proposal into the schedule, `posts_dismiss` to reject,
  `posts_publish` to put one out now.
- **`posts_create` puts a post you wrote on a real account.** Call `platforms_list` first - it
  carries each platform's text limit, media rules, whether a title is required, first-comment
  support, and the JSON Schema for its `settings`. Then:

  ```jsonc
  {
    "connectionId": "<from connections_list>",
    "text": "The post.",
    "scheduledAt": "2026-09-21T09:00:00+03:00",  // omit for now
    "queue": true,                    // instead of scheduledAt: the next free slot
    "mediaKeys": ["..."],             // media already in the account
    "title": "The video title",       // YouTube requires one
    "settings": { },                  // per platform; platforms_list has the schema
    "firstComment": "Link: https://..."   // LinkedIn, X, Bluesky only
  }
  ```

  `scheduledAt` and `queue` are exclusive. A platform rule refuses at creation with a `422` that
  names the rule, never at publish time. The CLI equivalent is
  `shapeless posts create --to <id> --text "..." [--at <ISO> | --queue] [--media k1,k2]
  [--title "..."] [--settings '{json}'] [--first-comment "..."]`.
- **The Free plan posts ten a day on the rail**, counted on the UTC day each post goes out on -
  so a week planned ahead is ten a day, not ten in total, and approving a proposal counts the
  same as creating one. The eleventh answers
  `402 {code: "free_daily_cap", limit, day, resetsAt}` naming the day that is full: move the post
  to a day with room, or tell the user their account is on Free. Paid plans have no cap.
  Composing, scheduling and publishing never spend credits; Free also carries $5 of credits a
  month for the generative work.
- **Studio tools** are the studio agent's own tools, each its own MCP tool under the same name,
  for one direct step when a whole job is more than you need: `generate_image`,
  `generate_footage`, `edit_footage`, `render_carousel`, `render_thumbnail`, `speak`,
  `caption_file`, `web_search`, `read_page`, `screenshot_page`, `x_pulse`, `news_search` and
  more (`tools_list` reads the catalog live, with prices). Each takes the `write` scope and
  answers `{tool, output, media: [{key, url}], chargedUsd}`; put a `media` key in
  `posts_create`'s `mediaKeys` to publish it. One with a price spends credit, so confirm first.
  The full table is at [docs/mcp](https://shapelessai.com/docs/mcp.md).
- **Capabilities** (`capabilities_list`) say what ShapelessAI can do, live or planned;
  `capabilities_want` records that the user wants a planned one.
- **Agents** are standing schedules (`agents_list`, `agents_save`, `agents_wake`) - recurring
  content work the server runs on its own.
- **Brand Memory** (`brain_tree`, `brain_read`, `brain_write`) is the account's durable
  knowledge: voice, positioning, product facts. Edit it when the user corrects how their brand
  should sound - that fixes every future post, not just one.
- **Actors** (`characters_list`, `characters_voice`) are the faces and voices videos use.
  `characters_voice` designs a voice from a description or clones one from a sample the user
  holds the rights to - it spends credit, so confirm first.

## Ground rules

- Tools whose descriptions say they publish or put content out are **live**: approving, publishing,
  waking an agent. Confirm with the user before calling them unless they explicitly asked for that
  exact action.
- Review before approving: read the post's actual text and media via `posts_get`, don't approve
  blind.
- Generative quality issues (wrong tone, wrong facts) are Brand Memory issues - offer to fix the
  source, not just the symptom.
- Putting a file in the brand library is for reuse; passing its media key on a message is what
  makes this turn's agent look at it. They are different asks - do the one you were asked for.
- The API is rate-limited at 600 requests/hour per key; poll jobs with restraint.

- Read `posts_create`'s rules before writing the post, not after a `422`: the character limit and
  the media rules are in `platforms_list`, and a draft written past the limit is a rewrite.

The full contract - routes, scopes, refusal codes - is at https://shapelessai.com/docs/api
(Markdown at https://shapelessai.com/docs/api.md).
