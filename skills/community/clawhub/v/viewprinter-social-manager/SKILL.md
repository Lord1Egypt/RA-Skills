---
name: viewprinter-social-manager
description: >-
  Use ONLY for work that goes through a connected ViewPrinter account: scheduling or
  publishing a post to TikTok, Instagram, Facebook, YouTube or X; uploading, describing,
  listing or PERMANENTLY DELETING media held in ViewPrinter; amending or cancelling a post
  that has not gone out; managing named groups of accounts; and reading follower and post
  performance. Two capabilities are destructive and irreversible: publishing to a real
  public account, and media_delete, which erases a stored file and its bytes. Listing media
  or posts reads everything in the user's ViewPrinter workspaces, not just one item.
  Requires ViewPrinter to be connected — do NOT use it to draft copy the user has no
  intention of posting, to schedule anything anywhere else, or for a platform ViewPrinter
  does not support. A bare "post this" with no ViewPrinter account in play is not this
  skill.
metadata:
  version: "1.3.1"
license: MIT
allowed-tools: ViewPrinter MCP (platforms, accounts, groups, media, posts)
---

# ViewPrinter

ViewPrinter is a hosted MCP server that publishes to social platforms on the
user's behalf. You drive it by calling its tools; the user drives you by asking
for what they want posted.

The platform names above are in the description so this skill can be *found*.
They are not a list to reason from — `platforms_list` is the only source of
truth for what can publish and what each one accepts. See
`references/rules/platforms-first.md`.

## If the tools are not there yet

The nine rules below all assume `platforms_list`, `media_upload` and the rest are
callable. Installed as a plugin they are — the manifest brings the server. But a
skill can be installed on its own, and then none of them exist.

**Check before working.** If the ViewPrinter tools are not available, the server
is not connected, and nothing below applies. Say so and hand it back:

- It is a remote MCP server at `https://viewprinter.tech/api/mcp` — streamable
  HTTP, OAuth only. There is no API key to paste anywhere, and any instruction
  to obtain one is wrong.
- The authorization server advertises Client ID Metadata Documents. A client
  that only attempts Dynamic Client Registration may fail with *"Incompatible
  auth server: does not support dynamic client registration"* — use the client's
  CIMD flow instead.
- Let the user complete the browser sign-in. Do not ask for credentials in chat.

## When to use this

- Posting, scheduling, drafting, rescheduling or cancelling anything
- Connecting a social account, or fixing one that needs reconnecting
- Grouping accounts so a post can name the set instead of listing ids
- Uploading an image or video to attach to a post
- Asking how a post did, or how an account is growing

## The shape of the work

1. **See what exists** — `accounts_list`, `groups_list`, `media_list`
2. **Learn the rules** — `platforms_list`, before composing anything
3. **Get the media in** — `media_upload`, then PUT the bytes; that is all
4. **Confirm label choices, then queue it** — ask about promotional-content and
   AI labels before `posts_save` creates a post or releases a draft; see
   `references/rules/scheduling.md`
5. **Read what happened** — `posts_list` (filters, one post, numbers per
   destination) and `accounts_list` with `metrics: true`

Nothing publishes until `posts_save` returns. Do not tell anyone a post is
scheduled before it does.

## Rules

Read the one that covers what you are about to do. Do not read all of them.

| Rule | Priority | Covers |
|---|---|---|
| `platforms-first` | CRITICAL | Live platform rules and connection-specific schema mismatches |
| `media-upload` | CRITICAL | Uploading is two steps, and the second is yours |
| `destinations` | CRITICAL | Workspaces, and why a group is a snapshot |
| `scheduling` | CRITICAL | Approval, opt-in labels, trial audiences, absolute times, and safe retries |
| `drafts` | HIGH | The word means two unrelated things |
| `refusals` | HIGH | A refused post was never saved, and is not a sales opening |
| `amend-and-cancel` | HIGH | What can still be changed, and what cannot be recalled |
| `connecting` | MEDIUM | Only the user can finish it |
| `reading-results` | MEDIUM | Measured when it was measured, and missing is not zero |

## Honesty constraints that hold everywhere

- **Report what the tool returned**, not what you expected it to return.
- **A refusal is a fact to relay, not a problem to route around.** You are
  running inside somebody else's client.
- **Numbers carry the time they were measured.** Quote it.
