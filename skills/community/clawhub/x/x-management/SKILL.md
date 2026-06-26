---
name: x_management
description: Draft-first X/Twitter account management workflow for OpenClaw. Use when the user wants to read their X account context, draft tweets, replies, quote tweets, or threads, and keep every write action gated behind explicit approval. Use with the OpenClaw X plugin when managing a personal X account safely.
---

# X Management

Use the X plugin as a **draft-first system**, not an autonomous posting engine.

## Core operating rule
Never treat a generated tweet/reply/quote as ready to publish by default.
Always:
1. gather context first when relevant
2. create a draft
3. show the draft clearly
4. require explicit user approval
5. only publish if approval has been captured through the plugin flow

## Current real plugin capabilities
Working now:
- `x_account_connect`
- `x_account_auth_url`
- `x_account_complete`
- `x_account_me`
- `x_followers_list`
- `x_posts_search`
- `x_user_posts_search`
- `x_timeline_me`
- `x_timeline_mentions`
- `x_post_get`
- `x_post_context`
- `x_post_create`
- `x_post_reply`
- `x_post_quote`
- `x_post_thread`
- `x_post_approve`
- `x_post_publish` for approved single posts, replies, quotes, and thread drafts
- `x_media_upload`
- `x_util_resolve_url`

Multi-account:
- Account-sensitive tools accept an optional `accountId`; omitted means `default`.
- Use explicit `accountId` whenever more than one X account is configured or when an automation is account-specific.
- Treat account ids as exact local slot ids. Similar-looking ids such as `dontdieeveryday` and `dont-die-everyday` can point to different persisted OAuth sessions.
- Verify the selected account with `x_account_me` before approving or publishing from a non-default account.
- Drafts are account-bound. A draft created for one `accountId` must be approved and published with the same `accountId`.
- Plugin config can optionally define per-account overrides under `accounts: { [accountId]: { ... } }`.

Still partial:
- engagement actions
- deeper thread expansion beyond immediate referenced context
- packaged-runtime validation should still be treated as an active release-quality concern when new plugin versions ship

## Use the plugin surface this way

### Reading context
Prefer read actions before drafting whenever the content depends on an external post or thread.
Use:
- `x_followers_list` when follower tracking, audience-change checks, or graph-aware monitoring is needed
- `x_posts_search` for recent X search through the authenticated account; it is not a full archive search and may return zero for older posts
- `x_user_posts_search` when looking for older posts from the connected account or a known user id
- `x_util_resolve_url` to normalize a target post URL
- `x_post_get` for a single post with normalized output
- `x_post_context` for a post plus immediate referenced context
- `x_timeline_mentions` when deciding whether/how to reply
- `x_timeline_me` when recent account voice/context matters

When searching Prince's own older posts, prefer `x_user_posts_search` over `x_posts_search` or manually paging `x_timeline_me`. Use `maxPages` and `nextPaginationToken` when one shallow page is not enough.

Follower reads require the connected X OAuth session to include `follows.read`.
If `x_followers_list` fails with a missing-scope/auth error after upgrading the plugin, reconnect the account through `x_account_auth_url` and `x_account_complete` so the new scope set is granted.

### Follower tracking
For an unfollower/follower-tracker workflow:
- call `x_followers_list` with `allPages: true` to gather the current follower snapshot
- if the result is `partial: true`, continue with `nextPaginationToken` until complete
- compare the returned `usernames` against the prior stored snapshot
- only conclude "no change" after the snapshot is complete

### Drafting
Use:
- `x_post_create` for a normal tweet
- `x_post_reply` for a reply
- `x_post_quote` for a quote tweet
- `x_post_thread` for multi-post threads

Treat returned `draftId` as the durable handle for follow-up approval/publish steps.
For threads, keep each post concise and make sure the full sequence is approved before publishing.
When using a non-default account, keep passing the same `accountId` through draft creation, approval, and publish.

### Approval and publish
Use `x_post_approve` only after the user has explicitly approved the exact draft.
Then use `x_post_publish` only for the approved draft id.
`x_post_publish` can now publish approved single posts, replies, quotes, and thread drafts.
Do not mutate draft text between approval and publish.

## Drafting heuristics

### For replies
Before drafting a reply:
- inspect the target post
- inspect immediate referenced context when available
- inspect your recent voice if tone consistency matters
- avoid replying to a hallucinated interpretation of the post
- keep factual claims anchored to what is actually visible

### For quote tweets
A quote tweet should add something:
- analysis
- framing
- disagreement
- emphasis
- synthesis

Do not produce empty applause unless the user wants that tone.

### For tweets
When the user does not specify tone, prefer concise, high-signal writing over bloated threadbait.
Offer 2-3 options when tone uncertainty is real.

## Safety boundaries
- do not publish automatically
- do not assume approval from conversational enthusiasm
- do not like/repost/bookmark autonomously unless the user explicitly asks
- do not DM from this workflow
- if publish or read capabilities fail, explain the actual failure clearly

## Current architectural split
- plugin = auth, reads, drafts, approval state, publish primitive
- agent/skill = judgment, research, tone, decision-making, proposing options

That is the intended shape for Prince’s eventual dedicated X-managing agent.
