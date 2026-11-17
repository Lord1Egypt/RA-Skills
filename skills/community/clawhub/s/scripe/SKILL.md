---
name: scripe
description: "Plan, write, schedule and measure LinkedIn posts for a team in Scripe (scripe.io) through its hosted MCP server. Use when the user wants to plan a content calendar for one or several LinkedIn profiles or company pages, draft a post in someone's own voice, turn a transcript, article or idea into posts, schedule or publish a post, read LinkedIn analytics, find outlier posts in their niche, or work with their Scripe ideas, knowledge base, labels or campaigns."
version: 1.0.0
author: Scripe GmbH
license: MIT
homepage: https://scripe.io/integrations/mcp-api
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [LinkedIn, Social Media, Content Calendar, Scheduling, Analytics, B2B Marketing, MCP]
    category: social-media
    homepage: https://scripe.io/developers/api/v1/mcp
  openclaw:
    emoji: "📅"
    homepage: https://scripe.io/integrations/mcp-api
---

# Scripe

Scripe is a social media management platform for B2B teams and agencies,
built LinkedIn-first: the posts of company pages and colleagues' profiles are
planned, written, approved, scheduled and measured in one place. This skill
drives Scripe through its hosted MCP server, `https://mcp.scripe.io/mcp`.

Scripe publishes to LinkedIn only. Do not offer other networks.

## When to Use

- "Plan our LinkedIn posts for the next two weeks", "fill the gaps in
  Eva's calendar", "what should the company page post this month".
- "Write a LinkedIn post in my voice about …", "turn this transcript /
  article / meeting into posts", "make this draft shorter".
- "Schedule this for Tuesday 9:00", "publish it now".
- "How did my posts do last month?", "which formats work for us?",
  "find outlier posts in my niche".
- Anything about Scripe ideas, the "For you" suggestions, the knowledge
  base, labels, campaigns or the review workflow.

Not for: liking, commenting on or reposting other people's LinkedIn posts.
Scripe does not do that from any agent surface, by design; tell the user it
is a click in the Scripe dashboard.

## Prerequisites

1. A Scripe account (scripe.io). Every plan, Free included, can connect.
   Scheduling and publishing need a paid plan or a running trial; AI writing
   counts against the plan's limits.
2. The Scripe MCP server connected to this agent, with OAuth. No API key:
   the MCP endpoint accepts OAuth tokens only. The first call opens a browser
   to Scripe's consent screen, where the user picks read-only or full access
   and the workspace to start in.

If no `scripe` tools are available, set the server up first. Setup per host
(Hermes Agent, Claude Code, Claude, ChatGPT, Codex, Cursor, Gemini CLI,
OpenClaw and any other MCP client) is in
[references/connect.md](references/connect.md). For Hermes Agent:

```bash
hermes mcp install scripe      # once Scripe is in the Hermes MCP catalog
```

or add it to `~/.hermes/config.yaml` and sign in:

```yaml
mcp_servers:
  scripe:
    url: "https://mcp.scripe.io/mcp"
    auth: oauth
```

```bash
hermes mcp login scripe
```

Then start a new session (or run `/reload-mcp`) so the tools load.

## How the tools are shaped

Scripe serves its ~130 operations in one of two shapes, chosen by the host.
Both call the same operations with the same arguments.

- **Grouped (most hosts):** 13 planning tools by name (`get_planning_overview`,
  `preview_plan`, `commit_plan`, `draft_planned_posts`, …) plus one tool per
  domain and effect: `workspace_read`, `posts_write`, `ideas_read`,
  `calendar_read`, `knowledge_write`, `analytics_read`, `brand_read`,
  `organize_write`, `media_write`, … Call an operation as its `action`, with
  its arguments in `arguments`:

  ```json
  { "name": "posts_write",
    "arguments": { "action": "generate_post",
                   "arguments": { "source": { "type": "topic", "text": "Why we stopped weekly status meetings" } } } }
  ```

  `describe_actions` returns the full schema of any operation.
- **Flat (Claude Code):** every operation is its own tool, named like the
  action (`generate_post`, `schedule_post`, `get_analytics_overview`).

Below, operations are written by name. Which domain tool carries each one is
in [references/operations.md](references/operations.md).

## Procedure

### 1. Know where you are

Call `get_workspace_context` first. It returns the active workspace, its plan,
whether reviews are required, and its profiles (personal profiles and company
pages) with their ids and whether LinkedIn is connected.

- Tell the user which workspace is active, by name. To work in another one,
  `list_workspaces`, match the user's words to a `name`, then
  `switch_workspace`.
- A "profile" is a Scripe project. Most operations take an optional
  `projectId` and fall back to the profile pinned when the user connected.
  When the user names a person ("Eva's posts"), pass that profile's id.
- A profile without a LinkedIn connection can still be planned and written
  for. Publishing and analytics need the connection, which the user makes in
  the Scripe dashboard.

### 2. Plan a period (one or many profiles)

"Our", "we" and "everyone" mean every profile you can reach unless the user
names people.

1. `get_planning_overview`: every profile in one call, with goal gaps, open
   calendar slots and idea stock.
2. In the same turn, `get_profile_planning_context` (who each profile is,
   their voice and positioning) and `get_planning_signals` (what works in
   their niche now, new source items, knowledge, their own performance, the
   "For you" suggestions with reasons). Never loop per-profile reads for this.
3. Write the ideas yourself from that evidence: one angle and hook per open
   slot, spread across the profile's lanes (Reach, Trust, Convert).
4. `preview_plan` and read its warnings (repeated angles, bare titles).
5. Show the plan to the user and wait for their yes.
6. `commit_plan`: one write; each idea reserves its slot.
7. `draft_planned_posts`: Scripe writes the posts in each profile's voice, in
   the background. Poll `get_draft_run` and report what landed.

The MCP prompt `plan_content` runs this whole loop.

### 3. Write one post

- From a topic, idea, note or text: `generate_post` with a `source`. Scripe
  writes it in the profile's voice (tone of voice, past posts, knowledge
  base) and saves a draft. Show the text and the link it returns.
- When the user wrote the text themselves: `create_post_draft` with their
  words as `content`, unchanged.
- To change a draft: `get_post`, then `update_post`.
- For material to draw on: `search_knowledge` (by meaning) or
  `read_knowledge_document`; to add material, `add_to_knowledge_base`
  (text, file, URL or YouTube).

### 4. Schedule or publish

- `schedule_post` schedules on the first call and the post then goes live on
  LinkedIn by itself at that time. Say so to the user, using the `notice` it
  returns. Undo with `update_post` and `scheduledFor: null`.
- `publish_post` posts to LinkedIn immediately. It is two-phase: the first
  call returns a proposal and a `confirmationToken`. Show the proposal, get
  the user's explicit yes, then call again with the token. Publishing right
  away through an agent is limited to 5 posts per user in 24 hours.
- In a workspace that requires review, a post needs an approved review first.
  `request_review` sends posts to a reviewer (two-phase); approving or
  rejecting happens only in the Scripe dashboard.

### 5. Measure

- `get_analytics_overview` for a profile's headline figures over a range.
- `list_post_analytics` for per-post figures (pass `postId` for one post).
- `get_analytics_report` for a daily series; `get_posting_times` for when
  this profile's posts perform best.
- `search_viral_posts` for outlier posts in the user's niche, judged against
  each author's own usual post.
- Report only figures Scripe returned. Never estimate a missing number.

### 6. Ideas

- `list_for_you_ideas` / `get_for_you_idea`: Scripe's suggested ideas with
  the sources they were built on. `save_for_you_idea` puts one on the board.
- `list_ideas`, `create_idea`, `update_idea`, `schedule_idea` for the idea
  board. `generate_post_ideas` turns material into ideas.
- Idea operations echo the `project` they wrote to. Tell the user which
  profile an idea landed on.

## Pitfalls

- **Two-phase actions are not consent by themselves.** `publish_post`,
  every delete, `request_review`, `send_content_questions`, `add_post_media`
  and several settings writes return a proposal first. Always show it and get
  the user's yes before the confirming call. A changed request needs a new
  proposal.
- **401 / "No Authorization header"**: the connection is not signed in or
  lapsed. Re-run the host's MCP login (`hermes mcp login scripe` on Hermes).
  An API key does not work on MCP.
- **`plan_not_eligible`**: the workspace's plan does not include that action
  (scheduling on Free, for example). Say what it needs; do not retry.
- **`conflict` on scheduling**: the workspace requires an approved review.
- **402 on an AI verb**: the plan's AI limit for the period is spent. The
  error says when it resets.
- **Wrong workspace**: every read and write is scoped to the active
  workspace. Confirm it by name before writing.
- Scripe never likes, comments or reposts on other people's posts and has no
  tool for it. Do not try to work around that.

## Verification

- After a write, read it back (`get_post`, `get_idea`, `list_calendar`) and
  give the user the link Scripe returned.
- After `schedule_post`, confirm the time in the profile's time zone.
- After `draft_planned_posts`, report each item from `get_draft_run`
  (done, failed with reason, or still writing).
