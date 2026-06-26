# API Dogfood Caveats

Use this note when a task involves copying edits between projects, correcting captions, workspace settings, media asset lookup, or endpoint discovery.

## Fact-checked issues from agent dogfooding

| Issue | Status | Diagnosis | Agent workaround |
|---|---|---|---|
| OpenAPI unavailable | Historical possible fallback | `src/trpc/api/openapi.ts` can return an empty spec if generation fails. Live OpenAPI is currently healthy. | Use OpenAPI as source of truth. If it is empty with a generation error, fall back to `llms-full.txt`, local skills, and route source. |
| Caption-block CRUD now project-scoped | Fixed in API | Caption list/get/patch routes are project-scoped: `GET /projects/{id}/captions`, `GET /projects/{id}/captions/{captionId}`, and `PATCH /projects/{id}/captions/{captionId}`. There is still no global `/captions/{captionId}` route. | Use `captionId` from full context, or list project captions before patching. |
| Caption themes public | Confirmed live | `/caption-themes` routes are registered in OpenAPI. | Use the caption-themes skill; still preflight on non-prod/older deployments. |
| Project metadata update public | Confirmed live | `PATCH /projects/{id}` accepts `name` and `description`. | Use it for metadata only; not editor/render settings. |
| Background audio insert exists but scoped | Confirmed live | `POST /projects/{id}/timeline/audio` is registered, but expects an existing workspace audio asset. `/timeline/media` and `/broll` are visual media insertion paths. | Use `/timeline/audio` for existing audio assets. Do not guess `/audio` or `/music`. |
| Asset detail path hard to discover | Confirmed | Correct path is `/workspace/media/assets/{assetId}`. | Use workspace media routes for asset lookup and signed file URLs. |
| `GET /captions/words` style schema drift | Historical risk | Public output now normalizes per-word `style` before response validation. Older deployments could 500 if stored word style shape drifted. | On older deployments, fall back to project full context or transcript correction endpoint, then preview/verify. |
| Token-count-changing transcript replacement rejected | Confirmed | The transcript correction endpoint supports single-token `replacements` and same-token-count `phrase_replacements`, but not deletion/fusion/splitting. | Use phrase replacements for same-count edits. For `"de Expo" -> "d'Expo"`, use caption block patching or `POST /captions/words/merge`. |
| `safe_words` + `protected_words` PATCH rejected | Confirmed | GET returns both aliases; PATCH explicitly rejects sending both. | Send only `protected_words` or only `safe_words`, and patch only changed fields. |
| Workspace media `limit > 100` rejected | Confirmed | `limit` schema is `.max(100)`. | Page through with `limit=100&offset=N`. |
| Caption correction can merge chunks | Plausible side effect | Transcript/caption writes can preserve word text while changing how caption chunks render. | After correction, compare context/preview frames. Use `/timeline/split` only when a user asks to repair chunking. |
| Workspace description changed during settings patch | Not reproduced in public PATCH code | The public PATCH route only writes `description` when input includes `description`. A side effect likely came from the caller sending a normalized sibling field or another internal tool. | Patch only the changed fields. Read back settings after write and flag unexpected sibling changes. |

## Endpoint discovery rule

Do this before calling an unfamiliar endpoint:

1. Search OpenAPI. If it is empty with a generation error, continue.
2. Search `llms-full.txt`.
3. Search this skill and sibling references.
4. If still absent, do not guess by analogy. Tell the user the public API does not expose it, or inspect local source if available.

## Copy fixes from previous video

Preferred sequence:

1. Read previous project context: `GET /projects/{previousProjectId}/context?mode=full`.
2. Read target project context: `GET /projects/{targetProjectId}/context?mode=full`.
3. Copy caption style: `GET /projects/{previousProjectId}/captions/style`, then `PATCH /projects/{targetProjectId}/captions/style`.
4. Apply transcript corrections with single-token `replacements` or same-token-count `phrase_replacements`. For token-count-changing caption edits, patch caption blocks or use word delete/merge/split endpoints.
5. Copy editable overlays through `/projects/{id}/content-items`, then copy placement using registered timeline item update routes.
6. Verify with `preview-frames`, `visual-debug`, or `context?mode=full`.

Do not try guessed global caption-block, timeline pack, timeline silence-detection, alternate overlay, generated graphics, or background music paths unless OpenAPI lists them.
