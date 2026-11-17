# Render artifacts and cloud handoff

Use a local/session record when delivering, uploading, continuing, or revising media. It is not an API request or proof of a saved editable platform project. Simple delivery need not expose every field.

Record what is relevant and known:
- Local `artifact_id`, revision, `kind` (full_video/clip/overlay), and related shot/creative IDs.
- Actual tool/version, inputs, execution parameters, and media references. For animation projects, include project path, template version, and lockfile; FFmpeg needs no invented project fields.
- Real process/session, logs, and observed state. Never manufacture a server task ID for local rendering.
- Actual local path, byte size, hash, and probed duration/dimensions/frame rate/audio/alpha. Omit unchecked fields or mark them unknown.
- The reviewed file/version, actual viewing/listening coverage, probe results, issues, and unchecked areas.
- Intended delivery or cloud subtitle/packaging step, placement, audio handling, and subtitle time basis.
- Real uploaded URL, actual library material ID only if registration succeeded, and relevant expiry.
- Real cloud task ID, redacted journal, state, and final result.

Local artifact IDs, material-library IDs, and server task IDs are distinct. Do not save temporary upload credentials. Handle credential-bearing URLs according to the service's privacy requirements.

Distinguish prepared project, inspected preview, active local render, verified export, successful upload, library registration, submitted cloud composition, and completed final media. These are handoff descriptions, not invented server status codes. Obtaining upload credentials is not an upload; uploading is not library registration. A usable URL can go directly to composition without forced library registration.

If the local video is complete but requested cloud packaging is pending, report that exact state. A verified local-only deliverable requires no upload.

When using [receipts](production-plan.md), let the receipt own file/input identity and link review/cloud handoff to its version. A caption review does not certify unrelated speech or visuals. Preserve prior template versions, inputs, and media on revision.

Record source intervals and target placement separately with explicit units. Recheck alignment after duration or frame-rate changes. Generated material retains its generated role; source/reference media retain their original roles. See [media inputs](../runtime/media-inputs.md) and [hybrid production](../workflows/hybrid-video.md).
