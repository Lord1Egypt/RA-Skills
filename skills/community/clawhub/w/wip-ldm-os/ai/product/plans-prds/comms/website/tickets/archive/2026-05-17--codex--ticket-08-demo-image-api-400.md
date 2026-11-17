# Ticket 08: Fix the Kaleidoscope demo image API 400

**Date:** 2026-05-17
**Filed by:** Codex, with Parker
**Status:** archived 2026-05-18. Implemented by `wip-ldm-os-private` PR #991 plus production xAI env correction; Parker confirmed image generation worked.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** Ticket 02 login/demo entry and PR #987 image model update
**Surface:** `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs` and `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/index.html`

## Summary

The Kaleidoscope demo now reaches the scripted image generation step, but `/demo/api/imagine` is failing against xAI with a `400 Bad Request`.

This is not currently shaped like a login token failure. The observed live flow authenticated, entered the demo, ran the photo/vision step, then the image generation request reached xAI and was rejected upstream.

Fix the image generation request so the scripted Demo 1 image works. Keep the current xAI integration. Do not replace it with OpenAI, do not refactor auth, and do not build Demo 2.

## Observed behavior

Parker tested `https://wip.computer/login?next=/demo` after Ticket 02 and PR #987 were deployed.

The demo entered the chat and reached:

```text
Creating your kaleidoscope...
```

The server logs showed the image call reaching xAI and failing upstream:

```text
Demo imagine upstream error: {"status":400,"model":"grok-imagine-image-quality","aspectRatio":"1:1","message":"Bad Request"}
```

Current code sends the image request from `server.mjs` using:

```js
model: "grok-imagine-image-quality"
prompt: prompt
n: 1
aspect_ratio: "1:1"
```

Current demo prompts in `demo/index.html` include named album/style references:

```text
Boards of Canada album cover
Geogaddi album cover
```

Those references are not required for the product demo. Parker's direction: "The prompt shouldn't be that. It should be 'take an image.'"

## Desired behavior

- User logs in through `https://wip.computer/login?next=/demo`.
- Demo enters the scripted chat.
- User provides or uses the captured photo path.
- `/demo/api/imagine` successfully returns an image URL.
- The generated kaleidoscope image renders in the demo.
- Wallet deduction remains `$0.04`.
- If xAI rejects the request, the server logs enough non-secret detail to diagnose the rejection.

## Implementation direction

Keep this as a small launch fix.

1. Treat the current auth/token path as working unless proven otherwise by code or logs.
2. Make the xAI image request use the simplest valid request body for `grok-imagine-image-quality`.
3. Remove risky named album, artist, or brand/style references from the prompt text.
4. Keep the prompt aligned with the user action: take the user's image or image analysis and make a kaleidoscope-style image from it.
5. If `aspect_ratio` or `n` is causing the 400, remove or correct those fields according to the current xAI image-generation docs.
6. Keep error logging sanitized. Log status, model, and upstream error fields, but never log API keys, Authorization headers, raw secrets, or full request headers.

Suggested prompt shape:

```text
Create an abstract kaleidoscope image from the colors, light, and shapes in the user's photo. Use mirrored radial symmetry, analog film grain, warm color bleed, soft exposure, and no text.
```

For the no-photo fallback:

```text
Create an abstract kaleidoscope image with mirrored radial symmetry, analog film grain, warm color bleed, soft exposure, and no text.
```

These are examples, not mandatory copy. The required outcome is a working request and a prompt that does not depend on named album/artist references.

## Constraints

1. No login, passkey, WebAuthn, `next` allowlist, or token-handoff changes.
2. No Remote Control, pair/relink, relay, daemon sync, or E2EE changes.
3. No homepage changes.
4. No API key changes and no key handling changes.
5. Do not paste, print, or expose the xAI key.
6. Do not run live image generation or spend credits unless Parker explicitly asks. Parker owns product-flow testing.
7. Do not deploy. Stop at PR.

## Acceptance criteria

- `src/hosted-mcp/server.mjs` uses `grok-imagine-image-quality` or env override as intended.
- The `/demo/api/imagine` payload is compatible with the current xAI image-generation API.
- The demo prompt no longer contains `Boards of Canada`, `Geogaddi`, or other named album/artist/style references.
- Error logging remains sanitized and useful.
- Wallet cost remains `$0.04`.
- `node --check src/hosted-mcp/server.mjs` passes.
- `git diff --check` passes.
- No auth, Remote Control, relay, pair/relink, homepage, or deploy files are touched.

## Reviewer notes

The likely failing boundary is the upstream xAI image request, not the login token:

- The demo reached the chat.
- The photo/vision step ran.
- xAI returned `400 Bad Request` for the image call.

Review should focus on whether the request body and prompt are safe and current-doc compatible. Do not expand the PR into broader demo architecture work.

## Out of scope

- Replacing xAI with another provider.
- Moving the demo to the future Kaleidoscope app architecture.
- Adding a live Lēsa backend.
- Redesigning the scripted demo.
- Hardening the full homepage.
- Running the live image-generation test.
