---
name: youtube-openclaw-creator
description: Review YouTube upload metadata and publish-readiness notes before a human handles the final upload.
---

# YouTube Publish Readiness Reviewer

Use this skill to prepare YouTube upload metadata and a final human review
packet. Keep the work to planning, metadata QA, and final upload-readiness
notes.

## Inputs

Collect:

- video title,
- description draft,
- thumbnail path or description,
- target audience,
- privacy preference,
- tags and playlists,
- publish or schedule preference,
- source asset checklist.

Avoid collecting account credentials, channel recovery information, cookies, or
private analytics exports.

## Review Workflow

1. Check title, description, and thumbnail promise for consistency.
2. Verify that claims are backed by the video content or user-provided sources.
3. Check policy-sensitive areas:
   - made-for-kids audience choice,
   - medical, financial, legal, or education claims,
   - copyrighted media,
   - private personal information.
4. Produce a publish-readiness packet for the human uploader.

## Output

Return:

- cleaned title,
- cleaned description,
- tag and playlist recommendations,
- thumbnail notes,
- final human-upload checklist,
- risks or missing assets.

## Guardrails

- Do not perform uploads, scheduling, or publishing.
- Do not automate login, captcha, 2FA, or browser actions.
- Do not claim a video is live without a user-provided public or unlisted URL.
- Keep viewer-facing copy limited to text the audience should see.
