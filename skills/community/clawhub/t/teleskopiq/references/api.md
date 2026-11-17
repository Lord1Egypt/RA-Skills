# API inputs and additional operations

The source of truth is `server/graphql/modules/` in Teleskopiq. Do not assume every operation declared by the schema
is authorized for API keys. Browser/Firebase-user operations such as style editing, channel memory administration,
channel setup, billing, and key management are outside this skill's key-authenticated workflows.

## JSON files

- `update-script --input-file`: an `UpdateScriptInput` object; the CLI supplies `id`. Supported fields include `title`,
  `content`, `status`, `scheduledFor`, `publishedAt`, `metadata`, and `thumbnails`. Omit fields to preserve them;
  use `scheduledFor: null` to unschedule. The accompanying server fix merges metadata/thumbnails maps; arrays still
  replace their values. Older servers replace whole maps, so deploy that fix before partial thumbnail edits.
  `metadata` supports titles, description, tags, checkedVisuals, and suggestedPacing.
- Status enum values: `Draft`, `InProgress`, `ReadyToShoot`, `Recorded`, `Editing`, `Ready`, `Published`, `OnIce`.
  Returned display names can contain spaces; send enum values on writes.
- Pacing file: `{"targetMinutes": 10, "targetWPM": 150, "targetWords": 1500}`.
- Selection file: `{"selection": "selected text", "before": "preceding context", "after": "following context"}`.
- Files: `[{"uri": "uploaded Gemini URI", "mimeType": "application/pdf", "name": "reference.pdf"}]`.
  Upload through `uploadToGemini(data: String!, mimeType: String!, displayName: String!)` if needed; `data` is base64.
  Uploads are remote actions, not a local path reference; do not submit unrelated files.
- Comments are an array of `ScriptCommentInput` objects. Required: `id`, `type` (`range` or `general`), `text`, and
  `status` (`open`, `resolved`, `stale`). Range anchors use `selectedText`, `contextBefore`, `contextAfter`.
- Thumbnail updates use `thumbnails.ideas: [{description, text_overlay, generatedUrl}]`,
  `thumbnails.custom: {prompt, fullPrompt, url, assets: [{url, mimeType}]}`, or `thumbnails.selectedUrl`.
  GraphQL reads expose idea fields as `visual` and `text`, and generated results as `thumbnails {url idea ideaIndex}`.

## Direct GraphQL

`graphql --query-file operation.graphql --variables-file variables.json` supports queries/mutations using variables.
Use this for authorized operations without a named command. It has the same auth, error handling, redirect protection,
and no-retry behavior as other commands. It does not implement generic subscriptions; use the named streaming commands.

The client uses `metadataJob` SSE and `generateScriptThumbnail` to observe actual completion.
`startMetadataJob` / `startThumbnailJob` only acknowledge background launch, with no job ID or durable status query.
Polling for any nonempty `metadata` or `thumbnails` can return old results and is not a reliable completion check.

`chatJob` supports `toolResponse {callId, answer}`, comments, selection/context, files, pacingTarget, and requestKind.
It does not take `aiMode`. `AIEvent.type` includes `reply`, `script`, `thought`, `title`, `question`, `error`, and `complete`.
Final script content and patches are persisted server-side before chat's terminal event. Questions are resumable,
not successful completion. Keep returned script IDs when something fails; there are no idempotency keys for creation.
