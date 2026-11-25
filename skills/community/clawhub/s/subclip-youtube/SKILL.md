---
name: subclip-youtube
description: Upload exported files or timeline segments to YouTube, manage connected channels, videos, native schedules, comments, playlists, captions, thumbnails and Analytics reports through Subclip MCP. Use for YouTube actions and clip batches, without creating upload projects.
---

# YouTube

Discover `youtube` tools with `mcp_editor__list_tools` and `includeSchemas=true`. Read tools use `mcp_editor__call_read_tool`; mutations use `mcp_editor__call_tool`. Start with `list_social_accounts` and `get_social_status`. Use the exact connected channel database ID, not a public channel ID or guessed account. Match a unique user-named channel; ask if ambiguous. Status reports permissions, pagination, publication configuration and API limitations, without tokens.

## Files and segments

- Existing exported video: `youtube_upload_file`. Pass the exact authorized absolute `filePath`, the conversation/project context if needed, and a stable unique `operationId` per clip and account. Do not import the file into a timeline.
- Saved timeline segment: `youtube_publish_segment` with inclusive `startTime`, exclusive `endTime`, and a meaningful `outputFileName`. The renderer preserves the original timeline and renders all visible layers, captions and audible audio in that range. Use `publish_video_segment_to_social` for another chosen platform. A full project can still use `publish_video_to_social`.
- Multiple generated shorts: use the clipping brief's OUTPUT timeline ranges, not original-source timecodes. Keep the candidate reel intact. Export each approved range with `export_video` and a distinct filename, sequentially. Save completed output paths in the brief; then upload each with `youtube_upload_file`. Alternatively publish those ranges directly. Never clone one project per clip, delete the other clips, or cycle imports/removals merely to satisfy publishing.
- Do not silently export a whole reel when the user requests individual clips. Do not repeat a render when its usable exported file already exists. Preserve enhanced audio, muted original tracks and caption layers by rendering the candidate range rather than uploading the unedited source.

## Confirmation and timing

Before any upload, post, reply, moderation, metadata/privacy/schedule edit, thumbnail/caption or playlist change, or deletion, prepare an exact reviewable summary and obtain user confirmation. Read-only status, analytics and inbox queries need no confirmation. Publishing approval identifies files/ranges, channel, rendered caption summary, exact titles/descriptions/tags/privacy and schedule/timezone. One approval may cover an explicitly listed batch; never extend it to unlisted clips/accounts or changed metadata. Pass `confirmed=true` only for the approved action. Export approval alone does not authorize publishing.

If the user says “schedule” without specifying the mechanism, ask which one:
- **Subclip (`scheduleMode=app`, default for legacy callers):** retain the source and upload at the future time; supports public, unlisted or private upload destinations.
- **YouTube (`scheduleMode=youtube`):** upload immediately, private with `publishAt`, then YouTube makes it public at the chosen time. Requires a future public publication. UI/status calls this **Scheduled (YT)**. It is not publicly published while private.

Clarify the date/time/timezone if vague. Use ISO timestamps with a timezone. For already-uploaded private, never-published videos, `youtube_schedule_video` sets native publication time; `youtube_cancel_schedule` removes the time and leaves the video private. Use Subclip publication tools for managed Subclip records so the app and platform remain coordinated. YouTube rejects scheduling previously published videos; privacy=private alone cannot prove never-published eligibility.

## Completion and retries

- Renderer export/segment publish: store requestId, end the internal assistant turn and await automatic resume. External clients use `get_export_status`.
- File upload: store operationId, end the internal assistant turn and await automatic resume. External clients use `get_social_file_publish_status`. The ledger persists across app restarts. Reusing the SAME operationId for identical input returns the existing result. A changed submission needs new approval and a new ID.
- Queued/accepted means submitted, not uploaded or publicly published. Inspect `get_social_publication_status`; require the returned platform video ID/URL and verified proof for immediate/native uploads. Native “uploaded” means scheduled on YouTube, not public yet. A Subclip future schedule is a confirmed scheduling action, with upload pending.
- Record each clip's file/range, operationId, publicationId, external video ID, metadata and result in the director brief. Resume only unfinished clips. If interrupted or a submission response is uncertain, reconcile the stored objectKey with `get_social_status` and existing publication records; never blindly generate a new operationId or duplicate upload. Retry the existing publication when appropriate.
- Paid-plan denial stops the batch; show the supplied pricing link. Source cleanup frees Subclip storage but never deletes the YouTube video. Deleting a YouTube video requires its own explicit confirmation.

## Supported Studio actions

Discover each schema rather than guessing parameters:
- Channel details and upload playlist/video listing, including private videos, pagination, metadata, privacy, processing and statistics.
- Video title/description/tags/category/language, made-for-kids and synthetic-media disclosures, embedding/license/statistics visibility, privacy, native schedule and deletion. Partial updates preserve omitted writable fields.
- Comments and replies, owner reply status via `list_social_comments`, reply/edit/delete own comments, held/published/rejected moderation and optional author ban. Use `reply_social_comment` when replying from the shared inbox so app activity records the reply. No YouTube DMs exist.
- Playlist create/list/update/delete and add/remove/list items. Removing a playlist item does not delete its video.
- Timed SRT/WebVTT caption upload/list/delete and thumbnail replacement. Caption `isDraft` is a CAPTION track setting, not a Studio video draft.
- `youtube_get_analytics` queries activity-date reports with startDate/endDate, metrics, dimensions, filters, sorting and 1-based startIndex pagination. It requires the channel to have granted `yt-analytics.readonly`. Use `get_social_status` to inspect analyticsAuthorized / analyticsReconnectRequired. Adding the scope in Cloud Console does not grant it to existing tokens: if missing, ask the user to reconnect the selected channel. Do not initiate account changes without permission.
- Convenient read-only tools: `youtube_get_daily_analytics` for daily views/watch time/average view duration/subscribers gained and lost; `youtube_get_video_retention` for one owned video's retention; `youtube_get_traffic_sources` for discovery sources. No publication confirmation is needed for reading reports.
- `get_social_insights` continues to return lifetime statistics for CONTENT PUBLISHED in a chosen range. Analytics instead measures ACTIVITY DURING that range, including older videos. Keep those meanings distinct. Do not substitute lifetime totals for period performance.
- Google controls compatible metric/dimension combinations, data lag and privacy suppression. Use the returned columnHeaders to interpret rows; empty or omitted rows do not prove zero activity. Follow maxResults/startIndex pagination when needed. Never invent data or claim the complete date range is available just because it was requested.
- Query examples for `youtube_get_analytics`: daily `dimensions=day` with `metrics=views,estimatedMinutesWatched,averageViewDuration`; per-video ranking `dimensions=video`, `sort=-views`, same metrics; country/device views with `dimensions=country` or `deviceType`; demographics with `dimensions=ageGroup,gender`, `metrics=viewerPercentage`; search terms with `dimensions=insightTrafficSourceDetail`, `filters=insightTrafficSourceType==YT_SEARCH`, `metrics=views`, `sort=-views`, `maxResults=25`. Retention uses `dimensions=elapsedVideoTimeRatio`, `filters=video==ONE_VIDEO_ID`, `metrics=audienceWatchRatio,relativeRetentionPerformance`. Use `youtube_get_video` to resolve/check the video before querying it.
- Revenue and ad-performance metrics remain unavailable in this integration: monetary Analytics permission is separate and is not requested. Do not promise every report shown in Studio is exposed through the API.

## API boundaries

A private upload is the review-before-publication alternative; there is no exposed YouTube Studio video-draft upload. Shorts Related video is not an exposed Data API field; direct the user to Studio after upload. Eligibility and channel features remain YouTube-controlled. Literal `| @handle` text may be used in title/description, but do not promise a clickable mention. Shorts description URLs are not clickable; channel profile links and the Studio related-video link are alternatives. Do not download, export, publish or mutate merely while answering a capability question.

Sources: [video updates](https://developers.google.com/youtube/v3/docs/videos/update), [Analytics](https://developers.google.com/youtube/analytics/reference/reports/query), [Shorts related videos](https://support.google.com/youtube/answer/14075157), [clickable links](https://support.google.com/youtube/answer/13748639).
