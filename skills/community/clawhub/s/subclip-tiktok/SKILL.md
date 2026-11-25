---
name: subclip-tiktok
description: Post, schedule and review TikTok videos for a connected TikTok account through Subclip MCP (beta). Use for TikTok drafts and direct posts, scheduling, and TikTok analytics. The user chooses privacy, interactions and disclosures.
---

# TikTok (beta)

TikTok is in beta: only enabled accounts see it. If `list_social_accounts` has no `tiktokAccounts`, say TikTok is not available for this account yet and stop. Do not try other routes.

## The review limit

Until Subclip's TikTok app passes TikTok's audit, TikTok only accepts a direct post to a private TikTok account with privacy "Only me". Two safe paths, offer both:
1. **Draft**: `postMode: "draft"` sends the video to the user's TikTok inbox. They finish and post it in the TikTok app. Works for everyone, any privacy.
2. **Direct, Only me**: `postMode: "direct"` with `privacyLevel: "SELF_ONLY"`, after the user set their TikTok account to private.
A direct post with any other privacy fails with a clear error (`unaudited_client_can_only_post_to_private_accounts`). `tiktok_get_creator_info` tells you whether the app is audited.

## What the user decides (never pick silently)

Ask, in one message with options: draft or direct; who can view (use the options from `tiktok_get_creator_info`, shown with their labels: Everyone, Friends, Followers, Only me); the caption (show the exact text); comments / duet / stitch on or off; whether the video promotes the user's own business or a paid partnership (branded content cannot be private); whether it is AI-generated; now or a scheduled time with timezone. If a choice is missing, the publish tools answer `needs-user-choice` with the options and upload nothing: ask the user, then call again.

## Flow

1. `list_social_accounts`, use the exact `tiktokAccounts[].id`. If several accounts exist and the user did not say which, ask.
2. `tiktok_get_creator_info` with that id: privacy options, interactions the account turned off (they stay off), the longest video allowed, audit state.
3. Confirm with the user: account, caption, mode, privacy, interactions, disclosures, timing.
4. Publish with `publish_video_to_social` / `publish_video_segment_to_social` (timeline) or `publish_video_file_to_social` (an exported file), `platform: "tiktok"`, `confirmed: true`, the options in the `tiktok` object. Scheduling is app-side (TikTok has no native schedule): `postNow: false` with a future `scheduledFor`.
5. Check with `get_social_publication_status` (platform `tiktok`). A draft is finished when it reaches the TikTok inbox: tell the user to open TikTok to post it. A failed post carries a readable reason; fix the setting and use `retry_social_publication` with `tiktokFix` (for example `postMode: "draft"`) instead of re-uploading.
6. Reschedule or cancel a pending post with `reschedule_social_publication` / `cancel_social_publication`.

## Analytics

`get_social_insights` (TikTok block: followers, likes, video count, and the videos created in the range with views, likes, comments, shares) and `tiktok_list_videos`. TikTok gives no audience demographics or watch time for normal accounts: do not invent them. `reconnectRequired` means the user must reconnect the account.

## Edit and delete

Editing or deleting a published TikTok video is not available through TikTok's public API, so there is no tool for it. Tell the user to do it in the TikTok app.

## Log

Write what was posted into the project log (`write_session_summary`): the account, mode, privacy, caption, time and the publication id, so the next agent and the user can see it.
