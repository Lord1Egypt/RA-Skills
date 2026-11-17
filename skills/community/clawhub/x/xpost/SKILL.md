---
name: xpost
description: Post to social media through xpost — draft, schedule, edit and check delivery across X, Instagram, LinkedIn, Facebook, TikTok, YouTube, Threads, Bluesky and Pinterest, with their brand rules enforced server-side and their approval where the project asks for it. Use whenever asked to post, schedule, cross-post or take down social content, or to check whether a post went out and how it did.
---

# Posting through xpost

xpost is the posting layer between you and the user's social audience. It
holds their connected accounts, their brand rules and, where they have asked
for one, their approval queue. **Creating a post sends it**: it publishes at
the time given, or straight away when none is — there is no second step that
sends it. A project in copilot mode holds an agent's posts for approval
instead (`get_project` says which), and the approval route refuses an agent
key in every mode, so a held post moves when a person moves it.

A post made by hand in a browser is invisible to all three, and cannot be
tracked, retried or taken down from here. These tools are the route that
leaves a record.

## Connection

**Preferred: the `xpost` MCP server.** If it is connected you have the
tools below and nothing else is needed. If it is not connected, here is how —
no key required:

- Claude Code: `claude mcp add --transport http xpost https://xpost.to/api/mcp`, then `/mcp` → xpost → sign in.
- Cursor / Windsurf / Gemini CLI / VS Code: add `https://xpost.to/api/mcp` as an HTTP MCP server; the client opens the sign-in page.
- ChatGPT: xpost is in the plugin directory — find it, add it, sign in.
- Claude.ai / Claude Desktop: Settings → Connectors → Add custom connector, paste `https://xpost.to/api/mcp`, sign in.

**Fallback: the `xpost` CLI** (`npx xpost`, zero install), when there is no
MCP client — a shell, a script, a headless box. Every command is one route of
the public API and answers with the API's own JSON; a refusal prints the
body and exits 1, so `error_code` is the machine-readable half. Sign in once
with `npx xpost login` (a browser opens), or set `XPOST_API_KEY` where no
browser can. The tool names below map one to one:

```bash
npx xpost project                      # get_project
npx xpost accounts                     # list_accounts
npx xpost rules <accountId>            # get_posting_rules
npx xpost upload ./pic.jpg --alt "…"   # upload_media → media id
npx xpost posts create -c "…" -a <account> [-a …] [--media <id>] [--at 2026-10-01T09:00:00+02:00] [--draft] [--config '{"x":{"first_comment":"…"}}']
npx xpost posts list --status pending_approval,rejected
npx xpost posts edit <postId> -c "…"   # update_post — answers with a NEW id
npx xpost posts delete <postId>
npx xpost receipt <postId>             # get_delivery_receipt
```

Raw HTTP works too: `XPOST_URL` (default `https://xpost.to`) +
`Authorization: Bearer $XPOST_API_KEY`, spec at `$XPOST_URL/api/v1/openapi.json`.

## The tools

| Do this | Tool |
|---|---|
| Learn the project: timezone, approval mode, signature, guardrails, allowance | `get_project` |
| See destinations and what each can carry | `list_accounts` |
| The exact options an account takes (placements, first comment, boards…) | `get_posting_rules` |
| Attach a file the user gave you (path, URL, or a chat attachment) | `upload_media` — or `create_post` with `files` / `media_pending` |
| Create one post | `create_post` |
| Create many | `bulk_post` |
| Find posts, see verdicts and rejection reasons | `list_posts` |
| Change words, media, time or options | `update_post` |
| Remove your own unpublished post | `delete_post` |
| Where it landed, per account | `get_delivery_receipt` |
| A destination failed — try it again | `retry_delivery` |
| Pull a live post down (only when asked) | `take_down_post` |
| Which accounts need reconnecting | `list_connection_issues` |
| Test a caption against the rules before writing more | `check_guardrails` |
| Learn what works | `get_post_metrics`, `get_insights`, `get_top_posts`, `get_best_times` |

## Workflow

1. **`get_project`, then `list_accounts`.** You need account ids, and each
   account says what it can carry (`limits`, `can`). An **empty** list comes
   with `connect_message` and `connect_url`: nothing can be posted until the
   person connects an account. Both are written for them to read as they
   stand — the message is the sentence, the url is where it happens.
2. **`get_posting_rules`** for the accounts you will use, whenever you set
   anything beyond a caption. It is the option catalog per ACCOUNT — a key
   that is absent cannot be used on that account, whatever the platform
   allows elsewhere. Pinterest answers live `boards` with `eligible`; a board
   that is not eligible is refused.
3. **Media.** Instagram, TikTok, YouTube and Pinterest require it; stories
   and reels do too. `upload_media` takes a local `path` (stdio server only),
   a public `url`, or base64 `data`. A picture, video or PDF the user
   attached to the chat goes ON THE POST, two ways:
   - Your host hands attachments over as file objects (ChatGPT does): pass
     them as `files` on `create_post` or `update_post`, in post order.
   - Otherwise create the post with `media_pending: true`. It is held, and
     the reply carries `upload_url` and `upload_curl`: if the file is in
     your environment, that command (YOUR_FILE replaced) lands the picture
     on the post — nothing passes through a tool argument, so no host
     asks anyone to allow an opaque payload. Where it cannot be run, the
     approval card that came back carries a drop zone: the person adds the
     picture there, straight onto the post, and approves in the same card.
     Either way nothing comes back to you; the post simply has its picture.
     `list_posts` shows `mediaIds`. Base64 `data` on
     `upload_media` is for something you generated, not the user's file.
   "I've added another photo" therefore needs nothing further — it is
   already on the post. To add one from the chat, `update_post` with `files`
   or `add_media_ids`; `media_ids` replaces the set.
   A PDF is a LinkedIn document post: one PDF, alone, LinkedIn only.
4. **`create_post`.** `scheduled_at` is ISO 8601 with an offset, in the
   project's timezone (from `get_project`); omit it and the post goes out
   now (or, in copilot mode, as soon as they approve it). **`"next_slot"`** hands the time to the project's own posting
   schedule — it fits "queue it", and any ask with no time behind it where
   `get_project` shows `queue.configured: true` (its `next_slots` are what
   they will get). Refused as `no_queue_slots` where there is no schedule,
   and a time then has to come from the person. `is_draft: true` files a scratchpad draft — no queue, no
   approval link; the person sends it from its page. Per-account words and
   options go in `platform_configurations`, keyed by platform:
   `{"x": {"caption": "shorter", "first_comment": "…", "thread": ["…"]}}`,
   `{"instagram": {"placement": "stories"}}`. Every text field — caption,
   overrides, first comment, thread — runs through the guardrails.
5. **What the answer means.**
   - `scheduled` — the normal outcome: nothing is holding it. `publishes` is
     when it goes out, on the project's clock, and the **See post preview**
     link the result carries is the door to it — the post as every
     destination will draw it, still changeable, still cancellable, and after
     it lands, still removable.
   - `pending_approval` — this project holds agent posts. It is waiting on a
     person, it has not published, and the call has already landed; the same
     preview link is where they see it.
   - `ok: false` with `error_code` — a refusal, as data. Guardrail violations
     name the rule in `violations[].detail`, and the same rules run again on
     the next attempt, so a caption that meets them is what clears it. A
     missing plan (`publishing_needs_plan`) or a missing account comes with a
     `message` written for the person.
6. **`list_posts` is the current state of the queue.** Its `from` /
   `to` bound the scheduled time, so "what goes out next week" is one call,
   soonest first. The person can
   reject through a link you never see; a `rejected` row carries
   `rejectionReason`, which is what to fix. To change anything, `update_post`
   — it answers with a **new id**, and an edit to an approved post goes back
   into the queue because the approval was for the old words.
7. **After publish time, `get_delivery_receipt`.** One row per destination,
   each with its live link or the reason it failed. `retry_delivery`
   takes a failed row; `take_down_post` is for when the user asks for it,
   because there is no undo.

## Bulk

For a calendar or a CSV, `bulk_post` (≤100 rows) instead of a loop. Rows are
independent, and the answer is per row: which were created (every row
`scheduled`, or `pending_approval` on a project that holds agent posts, is
normal) and which failed, with the reason. Only the failed rows need sending
again. An `idempotency_key` per row makes a
resend after a timeout answer `repeated: true` instead of making a second copy.

## Learning what works

Before drafting, when there is history: `get_top_posts` shows what actually
performed — what carries over is angle, length and format, since the captions
belong to those posts — and
`get_best_times` ranks slots from this workspace's own results. `signal` is
what that ranking is worth: `none` or `thin` means there is too little
history behind it for an hour to mean anything. After a post has been live a while,
`get_post_metrics`; `null` means the platform does not report that metric,
not zero, and stories are not reported on by anyone. `get_insights` for
"how are we doing".

## Worth knowing

- Each `create_post` is one post. Variations are separate posts, and each of
  them is sent.
- The time that will happen is `publishes` in the answer, on the project's
  clock — a request's `scheduled_at` is what was asked for, not what came back.
- A guardrail refusal is about the words; a held post is about a person. One
  is fixed by rewriting, the other by waiting.
- A receipt can be partial — delivered on X, failed on Instagram with its own
  reason — because each destination is independent.
- Upload plumbing (sandboxes, hosts, slots) is nothing the person can act on;
  the card asks them for the file itself. What is open to them is the post: a
  missing caption, the time, the destinations.
