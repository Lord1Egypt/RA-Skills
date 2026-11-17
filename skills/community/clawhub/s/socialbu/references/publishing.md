# Publishing

## Read posts

- `list_posts` reads scheduled, draft, published, or awaiting-approval posts and supports account filtering and pagination. Use `get_post` for the current state and details of an individual post.
- `get_post_options` returns the options supported by the selected account types. Use it before supplying network-specific options.

## Schedule a post or batch

1. Resolve the destination account IDs with `list_accounts` or `search_accounts`. A post targets one account; prepare a separate post for each destination.
2. Resolve the user's timezone with `get_current_user`, unless they specified another timezone. Make relative dates concrete. Ask only when the destination, content, or time is ambiguous enough to affect what gets scheduled.
3. Read `list_posts` for the selected accounts, following pagination, to check the relevant schedule for duplicates and occupied slots. Do not move existing posts to make room unless authorized.
4. Call `get_post_options` for the selected accounts. Tailor copy, format, media, and options to each destination using the returned capabilities.
5. Show the proposed content, destination accounts, media, and local dates/times when the user needs to choose or approve them. A clear request to schedule already-specified posts is sufficient authorization; do not ask again.
6. Convert each approved local date/time using its timezone's offset on that date, including daylight saving changes, to UTC `Y-m-d H:i:s`. Pass an explicit future `scheduled_at` and `post_type: scheduled` to `create_post`; omitting the time can request immediate publication. For a user-selected existing draft, use `update_post` with its ID, `post_type: scheduled`, and `scheduled_at` rather than creating a duplicate.
7. Record each returned post ID and check its state and schedule using `get_post` when the create/update response is incomplete. Return actual results in the user's timezone. Scheduled, awaiting approval, queued, and published are different states.

If a batch partially fails, report the successful IDs and the failed entries separately. After an ambiguous timeout, read the affected account's posts and match content and time before retrying: `create_post` is not idempotent. Stop and ask if the outcome remains uncertain.

## Save drafts and request team approval

Pass `post_type: draft` when the user wants a saved draft, or `post_type: awaiting_approval` when they request team approval. Use a UTC `scheduled_at` when a publishing time is specified. Return the created post ID and actual state from SocialBu's response.

A request to write content in chat does not authorize saving, scheduling, or publishing it in SocialBu.

## Media

- `create_post` and `add_post_to_queue` can accept accessible HTTP(S) media URLs or supported base64 data URLs.
- For a file held by the agent, call `create_media_upload`, upload the raw bytes to the returned signed URL using the stated content type, then pass the returned temporary media URL to the post tool.
- Treat signed upload URLs as short-lived secrets. Do not repeat them after the upload completes.

## Change post state

- `update_post` changes a scheduled or draft post. Supplying the same values is intended to have no additional effect.
- `publish_post_now` requests immediate publication asynchronously and may require approval. Use it only when the user explicitly requests immediate publication. Check `get_post` for the final state, errors, and permalink before claiming the post is live.
- `approve_post` and `reject_post` change an awaiting-approval post and require team approval permission.
- `delete_post` removes a post. Confirm the ID belongs to the intended post before deletion.

If SocialBu returns a provider, permission, plan, validation, or processing error, report it directly and do not claim the post was published.
