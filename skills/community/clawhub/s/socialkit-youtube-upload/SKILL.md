---
name: socialkit-youtube-upload
description: Uploads an approved video to YouTube with the official Data API v3 - private by default, optional scheduled publish time, AI or synthetic content disclosure, and custom thumbnail - after the user approves the exact file and settings. Use when the user wants to upload, publish or schedule a YouTube video, or to connect their YouTube channel.
license: MIT
compatibility: Requires Node.js 22.12+, network access, and the user's own Google Cloud OAuth client.
metadata:
  author: Ahmad Hussain
  platform: youtube
  requires: socialkit-social-core socialkit-youtube-pipeline
---

# YouTube upload

Uses the user's own Google Cloud project. First-time setup: [setup](references/setup.md).

## Steps

1. **Authorise once.** If there is no token, ask the user to run in their own terminal:
   `node scripts/auth.mjs`
   It needs a browser sign-in; do not run it on their behalf in the background.
2. **Plan.** Ask the user:
   - privacy: `private` (default), `unlisted` or `public`
   - schedule: an ISO date with time zone, or none (scheduled videos must be private)
   - does the video contain realistic AI-generated or altered content?
   - notify subscribers?

   Then run:
   `node scripts/upload.mjs --dir <project-folder> --plan [--privacy private] [--schedule 2026-11-01T15:00:00Z] [--synthetic-media] [--notify-subscribers]`
3. **Approval.** Stop. Ask the user to watch the video and run the socialkit-youtube-pipeline
   approve command for the `upload` checkpoint in their own terminal. Do not continue
   until the upload checkpoint verifies.
4. **Upload.** `node scripts/upload.mjs --dir <project-folder>`
5. Report the result and every warning.

## Output contract

JSON with `videoId`, `url`, `studioUrl`, `requestedPrivacy`, `actualPrivacy`,
`publishAt`, `containsSyntheticMedia`, `thumbnail` and `warnings`.

## Failure handling

| Code | What to tell the user |
| - | - |
| `APPROVAL_REQUIRED` | Which file changed or which approval is missing; request approval again |
| `YT_NOT_AUTHORISED`, `YT_TOKEN_EXPIRED` | Run the auth script again (testing-mode tokens expire after 7 days) |
| `YT_QUOTA_EXCEEDED` | Daily quota used; resets at midnight Pacific Time; extension needs an audit |
| `YT_UPLOAD_LIMIT` | Channel upload limit reached; try later |
| `YT_ALREADY_UPLOADED` | This file was uploaded before; only re-upload if the user asks |
| `YT_CLIENT_TYPE` | The OAuth client must be a "Desktop app" client |
| Privacy warning | YouTube set a different privacy than requested; check YouTube Studio |
| Thumbnail warning | Custom thumbnails need a verified channel; set it in Studio |

Never retry an upload automatically after an error that may have created the video;
check YouTube Studio first.
