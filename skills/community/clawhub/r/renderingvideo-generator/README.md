# renderingvideo-generator

Public RenderingVideo preview skill for AI agents.

Use this skill when an agent needs to draft RenderingVideo schema JSON and turn it into a temporary preview link through the public preview endpoint:

- `POST https://video.renderingvideo.com/api/preview`
- No API key required
- Preview links expire after 7 days

## What It Does

- reads the live RenderingVideo docs
- drafts or edits valid schema JSON
- sends the schema to the public preview API
- returns a shareable preview URL and temp ID

## Files

```text
renderingvideo-generator/
+-- README.md
+-- SKILL.md
+-- example.json
+-- .gitignore
`-- scripts/
    `-- gen-preview.cjs
```

## Included Resources

- `SKILL.md`: AI-facing execution instructions
- `example.json`: minimal previewable schema
- `scripts/gen-preview.cjs`: helper script for `POST /api/preview`

## Documentation Sources

Use these live docs as the source of truth:

- `https://renderingvideo.com/docs/api-and-usage.md`
- `https://renderingvideo.com/docs/json-spec.md`
- `https://renderingvideo.com/docs/clips.md`
- `https://renderingvideo.com/docs/elements.md`
- `https://renderingvideo.com/docs/elements/base-clip.md`
- `https://renderingvideo.com/docs/animation-and-timing.md`

## Requirements

- Node.js 18+
- network access to `https://video.renderingvideo.com`
- a valid RenderingVideo schema JSON file

## Usage

Run the example:

```bash
node ./scripts/gen-preview.cjs ./example.json
```

Run with your own schema:

```bash
node ./scripts/gen-preview.cjs ./my-video.json
```

## Output

On success, the script prints:

- `tempId`
- absolute preview URL
- absolute viewer URL when present
- absolute player URL when present
- `expiresIn`

## API Behavior

- request body is the schema itself
- do not wrap the schema in `{ "config": ... }`
- the preview link is temporary and shareable
- prefer `viewerUrl` when present

## GitHub Usage

If you publish this skill in a GitHub repository:

- keep `README.md` human-facing
- keep `SKILL.md` AI-facing
- keep the script behavior aligned with the live API docs
- keep examples minimal and valid

