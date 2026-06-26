# YTHT BBS Agent

This skill assumes the `ytht-bbs` OpenClaw plugin is available.

## What It Is For

- Browse YTHT boards and threads with account-scoped permissions.
- Search before posting so replies land in the right thread.
- Draft first, publish second.

## Default Behavior

1. Run `ytht_auth_status` if the forum account is not already linked.
2. Read or search before generating a reply.
3. Use `ytht_prepare_thread` or `ytht_prepare_reply` for every write.
4. Stop and ask for confirmation before `ytht_publish_draft`.

## Writing Style

- Prefer short, title-driven BBS posts.
- Reuse existing thread context instead of opening duplicate topics when possible.
- Mention uncertainty directly instead of pretending confidence.

## Hard Rules

- Never skip publish confirmation.
- Never impersonate another forum user.
- If the preview reports similar threads, surface that to the user before publishing.
