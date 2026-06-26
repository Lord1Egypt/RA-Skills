# Publish Spec

This file defines the standalone publish contract for the `welight-wechat-layout-publish` skill.

The skill may publish only when the runtime already provides the required credentials and publish-side capabilities.

## Required Prerequisites

The runtime must already have access to:

- WeChat Official Accounts `appId`
- WeChat Official Accounts `appSecret`
- a way to request `access_token`
- a way to upload cover images
- a way to upload article body images
- a way to create draft articles

For formal publish, the runtime must also provide:

- the account capability to submit free publish
- a way to poll the publish status

Optional but often necessary:

- a reverse proxy or allowed egress path for WeChat API access
- an outbound IP already whitelisted in WeChat MP if required by the account setup

## Publish Sequence

Use this exact order:

1. Validate `appId` and `appSecret`.
2. Request `access_token`.
3. Check account capability if the runtime exposes that step.
4. Determine the cover image.
   - Use a user-provided cover if available.
   - Otherwise reuse the first suitable content image when allowed.
5. Upload the cover image and obtain `thumb_media_id`.
6. Convert themed article output into WeChat-compatible HTML.
7. Upload article body images to WeChat and replace external image URLs when required.
8. Build the article payload:
   - title
   - author
   - digest
   - content
   - content source URL if available
   - comment settings if supported
   - `thumb_media_id`
9. Create a draft.
10. If the mode is formal publish, submit free publish and poll until final status.

## Failure Handling

Report failures at the exact failing step.

Important failure cases:

- `40164`: the current outbound IP is not in the WeChat MP whitelist
- `48001`: the account lacks the required publish capability; fall back to draft mode if possible
- missing `thumb_media_id`: cover upload did not complete successfully
- broken content images: image upload or URL replacement did not complete correctly

## Expected Behavior

- If draft creation succeeds, report draft success clearly.
- If formal publish is unavailable, fall back to draft when possible and say so explicitly.
- If the runtime lacks publish tools entirely, stop before publish and state that the skill completed formatting/theme selection but could not execute the publish step.
