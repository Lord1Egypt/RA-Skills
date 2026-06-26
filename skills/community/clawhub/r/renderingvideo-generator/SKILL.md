---
name: renderingvideo-generator
description: RenderingVideo preview assistant that uses the public preview flow at POST /api/preview without an API key. Use this when Codex needs to draft or edit RenderingVideo schema JSON, validate it with a temporary 7-day preview link, and return the preview URL and temp identifier.
---

# RenderingVideo Preview Assistant

Use this skill when the task only needs the public temporary preview flow.

## Read This First

- Read `https://renderingvideo.com/docs/api-and-usage.md` before calling the public preview endpoints.
- Read `https://renderingvideo.com/docs/json-spec.md` before drafting or changing schema JSON.
- Read `https://renderingvideo.com/docs/clips.md`, `https://renderingvideo.com/docs/elements.md`, and `https://renderingvideo.com/docs/elements/base-clip.md` when choosing clip types or fields.
- Read `https://renderingvideo.com/docs/animation-and-timing.md` when the task changes timing, transitions, or animations.

## Enforce These Rules

- Use `POST /api/preview` for preview creation.
- Send the schema itself as the request body. Do not wrap it in `{ "config": ... }`.
- Do not require or send an API key for this skill.
- Treat the returned preview link as temporary and expiring in 7 days.
- Do not guess fields or routes from memory when `api-and-usage.md` covers them.

## Run The Script

Use the bundled script:

```bash
node ./scripts/gen-preview.cjs [path_to_json_file]
```

## Endpoint Mapping

- `gen-preview.cjs`: `POST https://video.renderingvideo.com/api/preview`
- Playback URLs: `/t/:id` or `/preview/:id`
- Readback endpoint: `GET /api/temp/:id`

## Follow This Workflow

1. Read `json-spec.md`, `clips.md`, and the relevant element page.
2. Draft or update the schema JSON.
3. Run `scripts/gen-preview.cjs` to create a temporary preview.
4. Return the preview URL and temp identifier to the user.
5. If the preview is wrong, revise the schema and generate a new preview.

## Keep These API Rules

- The preview body is the full schema JSON.
- Missing top-level `meta` or `tracks` should be treated as invalid input.
- The returned preview page is shareable but temporary.
- Prefer `viewerUrl` when present. Fall back to `url` if needed.
- Reuse returned `tempId`, `viewerUrl`, `url`, and `expiresIn` instead of guessing routes.

## Return These Fields

- Return `tempId`, `viewerUrl`, `url`, and `expiresIn` when present.
- Return the full absolute preview URL, not only the relative path.
- If the script or API returns validation failure details, preserve them.

## Handle Failures Explicitly

- If the API returns a non-2xx response, surface the HTTP status and response body.
- If JSON parsing fails locally, report that the input file is invalid JSON.
- If the preview expires or becomes invalid later, tell the user to generate a new preview.
