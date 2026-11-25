# ZOOOP Public REST API (v1)

## Quick start

```bash
# 1. Create a Personal Access Token at https://zooop.ai/user?tab=apiKeys
export ZOOOP_API_KEY=zpk_live_...

# (Quote every URL: zsh treats `?` as a glob and `&` as a job separator.)

# 2. Discover models for the kind of task you want
curl -fsS -H "Authorization: Bearer $ZOOOP_API_KEY" \
  "https://api.zooop.ai/v1/models?type=image&subtype=default"

# 3. Submit a task with one of the model ids + a version id
curl -fsS -X POST -H "Authorization: Bearer $ZOOOP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"interfaceId":"<uuid>","versionId":"standard","params":{"prompt":"a red panda"}}' \
  "https://api.zooop.ai/v1/tasks"

# 4. Poll for the result
curl -fsS -H "Authorization: Bearer $ZOOOP_API_KEY" \
  "https://api.zooop.ai/v1/tasks/<taskId>"
```

## Authentication

All endpoints require `Authorization: Bearer <PAT>`. Tokens look like
`zpk_live_<32 chars>` and are created at <https://zooop.ai/user?tab=apiKeys>. The
plaintext is shown ONCE at creation; afterwards only the leading prefix is
visible in the settings UI. To rotate, create a new token and revoke the old
one (revocation is immediate).

A token is either **personal** (created by running `npx zooop login` — the
ZOOOP CLI's browser sign-in, which creates the same kind of token — or at the
URL above) or **team** (issued by a team owner/admin in the team admin →
API Keys tab). Credits are debited
from that token's wallet — the user's personal balance for a personal token,
or the team's shared credit pool for a team token. The endpoints are
identical; `GET /v1/me` reports which wallet funds the token.

**Project binding**: every PAT is bound to one project at creation time and
cannot be re-bound. Tasks submitted via the PAT land under that project;
uploaded files do too. If the bound project is later deleted, every call
returns 403 `token_project_unbound` — the user must revoke + recreate. See
`GET /v1/me` for the bound project info.

## Error envelope

All errors follow an OpenAI-style envelope so SDKs that parse that shape work
out of the box:

```json
{
  "error": {
    "message": "Missing required parameters: aspect_ratio, resolution",
    "type": "invalid_request_error",
    "code": "missing_required_params",
    "params": [
      {
        "id": "aspect_ratio", "type": "aspect_ratio", "required": true,
        "default": "1:1",
        "options": [{"value": "1:1", "label": "1:1"}, {"value": "16:9", "label": "16:9"}]
      },
      {
        "id": "resolution", "type": "resolution", "required": true,
        "default": "1024",
        "options": [{"value": "1024", "label": "1024 × 1024"}, ...]
      }
    ]
  }
}
```

- `type` — broad family: `invalid_request_error`, `authentication_error`,
  `permission_error`, `rate_limit_error`, `api_error`.
- `code` — stable machine-readable reason. Branch on this in client code.
- `param` — set when the failure points at a single body / query field.
- Free-form extras (`validCategories`, `spent`, `cap`, `params`, `labels`, …)
  live under `error` too and are stable for any documented `code`.
- For `missing_required_params`, the `params` array carries structured hints
  per missing field (`id` / `type` / `required` / `default` / `options` /
  `constraints`) — agents can self-correct in one round-trip without
  re-fetching the model.

Per-endpoint error tables below.

## Endpoints

### `GET /v1/me`

PAT self-introspection. Returns everything the calling agent needs to plan
its requests without trial-and-error 429s / 402s — bound project, daily
credit headroom, account balance, current rate-limit numbers.

```bash
curl -fsS -H "Authorization: Bearer $ZOOOP_API_KEY" \
  "https://api.zooop.ai/v1/me"
```

Response:

```json
{
  "key": {
    "id": "uuid",
    "prefix": "zpk_live_aBcD…",
    "label": "claude-code-mac",
    "createdAt": "2026-05-15T10:00:00.000Z",
    "expiresAt": null,
    "dailyCreditCap": 1000,
    "creditsSpentToday": 42,
    "creditsRemainingToday": 958
  },
  "project": { "id": "uuid", "name": "My Project" },
  "user":    { "creditBalance": 84495 },
  "limits":  {
    "tasksPerMin": 60,
    "uploadsPerMin": 30,
    "uploadPollPerMin": 120
  }
}
```

Field notes:
- `key.dailyCreditCap` is `null` when no cap is set; `creditsRemainingToday`
  is also `null` in that case.
- `key.expiresAt` is `null` when the token never expires. Warn the user to
  renew before this date.
- `project.id` / `project.name` are both `null` (with `project.bound: false`)
  when the bound project was deleted — submits will fail with
  `token_project_unbound` until the token is rotated.
- **Wallet** — exactly one key is present: `user: { creditBalance }` for a
  **personal** token, or `team: { id, creditBalance }` for a **team** token
  (the team's shared pool; a team token never exposes its creator's personal
  balance). This is the wallet that funds tasks — even with
  `creditsRemainingToday > 0`, an empty wallet still blocks expensive submits.
- `limits.*` reflect the current per-PAT rate-limit numbers. Honor them.

All PATs grant full access to every `/v1/*` endpoint.

Privacy: deliberately omits `user.id / email / name` (PAT bearer doesn't
need user identity — the token itself is the identity) and never enumerates
other PATs of the same user.

### `GET /v1/models?type=<type>&subtype=<subType>`

Lists the enabled model interfaces that match one `(type, subType)` pair.
Both query params are **required** — calling without them returns 400 plus
the full set of valid `(type, subType)` pairs so the caller can self-correct.

Exposure rule: a `(type, subType)` pair is exposed via the public API iff
the corresponding generator tool is currently in the homepage sidebar. The
single source of truth is `src/lib/seo/tool-pages-seo.ts` (`inSidebar: true`).

Response shape:

```json
{
  "models": [
    {
      "id": "uuid",
      "name": "Flux Pro",
      "type": "image",
      "subType": "default",
      "description": "Photorealistic text-to-image model …",
      "brand": { "id": "flux", "name": "Black Forest Labs", "logo": "https://..." },
      "promptRequired": true,
      "promptMaxLength": 2000,
      "params": [
        { "id": "prompt", "type": "long_text", "required": true, "maxLength": 2000 },
        { "id": "aspect_ratio", "type": "aspect_ratio", "required": false, "enumValues": ["1:1","16:9","9:16"] }
      ],
      "versions": [
        { "id": "standard", "name": "Standard",
          "typicalPrice": { "typicalCredits": 4, "unit": "image", "note": "1024×1024, 1:1" } },
        { "id": "pro",      "name": "Pro",
          "typicalPrice": { "typicalCredits": 8, "unit": "image", "note": "1024×1024, 1:1" } }
      ],
      "tags": ["HOT"]
    }
  ]
}
```

### Public categories

| type   | subType            | Tool                            |
| ------ | ------------------ | ------------------------------- |
| image  | default            | Image generator                 |
| image  | edit-image         | Image editor                    |
| image  | image-svg          | SVG generator (text/image-to-vector) |
| video  | text-ref           | Video generator                 |
| video  | motion-control     | Motion control (image-to-video) |
| video  | first-last-frame   | First / last frame video        |
| video  | audio-lipsync      | Lip sync                        |
| video  | extend-video       | Extend video                    |
| video  | video-edit         | Video editor                    |
| audio  | text-to-speech     | Text-to-speech                  |
| audio  | voice-clone        | Voice clone                     |
| audio  | sound-effect       | Sound effect                    |
| audio  | music              | Music generation                |

`typicalPrice.unit` values:

- `image` — credits per generated image (total at default dimensions)
- `second` — credits per second (output for duration-defaulted models, OR
  per second of input for extend / lipsync-style models)
- `frame` — credits per frame of input video
- `1k_chars` — credits per 1000 characters (TTS; all per-character pricing
  is normalized to this unit so the number is always a relatable integer
  / one-decimal value rather than a fractional per-char rate)
- `call` — credits per call (flat, no dimension scaling)

For flat units (`image`, `call`) `typicalCredits` is an integer and the
`minPrice` floor is already applied. For rate units (`second`, `frame`,
`1k_chars`) it may be fractional (e.g. `50.5`) to preserve fidelity for
sub-credit rates. `typicalPrice` is a coarse ballpark only — call
`POST /v1/quote` (below) with the exact payload you'd submit to get the
authoritative number.

### `GET /v1/ai-tools[?type=image|video]`

List active AI tools — admin-curated recipes that pre-bind a model + version
+ tuned params for a specific outcome (background removal, age modification,
style transfer, video upscale, etc.). Agents submit by stable `slug` and
supply only the recipe's visible inputs instead of configuring the raw
underlying interface.

Optional `?type=image|video` filters by media type. Other values return 400
`invalid_type`. There is **no** `subtype` query — the recipe's `subType`
field is admin free-form ("特效", "动作模仿") and not a filter axis.

Exposure rule: a tool appears iff (a) `recipe.isActive = true`, (b) the
recipe carries the `api` tag (admin opt-in — fail-closed by default), and
(c) its underlying interface is still enabled. This is a deliberately
narrow surface: most /tools/* recipes are prompt-wrappers around generic
text-to-image models that an agent could replicate cheaper by calling the
raw model directly. Only the tools that genuinely add capability beyond
`/v1/models` (background removal, upscalers, etc.) are tagged.

Response:

```json
{
  "aiTools": [
    {
      "slug": "background-removal",
      "name": "Background Removal",
      "mediaType": "image",
      "subType": "",
      "summary": "Remove the background and keep only the subject.",
      "coverUrl": "https://storage.zooop.ai/...",
      "tags": ["NEW"],
      "params": [
        { "id": "image_url", "type": "image_url", "required": true, "displayName": "" }
      ],
      "typicalPrice": { "typicalCredits": 2, "unit": "image" }
    },
    {
      "slug": "style-transfer",
      "name": "Style Transfer",
      "mediaType": "image",
      "params": [
        { "id": "image_url", "type": "image_url", "required": true },
        { "id": "target_style", "type": "enum", "required": true,
          "options": [
            { "value": "impressionism", "label": "Impressionism" },
            { "value": "cubism", "label": "Cubism" }
          ]
        },
        { "id": "aspect_ratio.ratio", "type": "aspect_ratio", "required": true,
          "options": ["1:1","16:9","9:16","4:3","3:4"] }
      ],
      "typicalPrice": { "typicalCredits": 6, "unit": "image" }
    }
  ]
}
```

The `params[]` shape mirrors `/v1/models` exactly — same `id` / `type` /
`required` / `options` / `default` / `constraints` semantics. Voice-type
params on TTS-style tools expand options to `{value, label, previewUrl?}`
identical to `/v1/models`. Fields the agent doesn't need (mapping internals,
preset overrides, hidden / fixed params) are stripped.

### `GET /v1/ai-tools/{slug}`

Fetch one AI tool by stable slug. Same shape as a single entry from the
list endpoint. Returns 404 `unknown_ai_tool` for unknown / inactive slugs
and for slugs whose interface is no longer enabled.

```bash
curl -fsS -H "Authorization: Bearer $ZOOOP_API_KEY" \
  "https://api.zooop.ai/v1/ai-tools/background-removal"
```

### `GET /v1/templates[?type=image|video]`

List the gallery templates published at `/templates/{slug}` — a tuned prompt
plus a bound model + version, run by stable `slug`. Where an AI tool adds a
capability the raw models lack, a template packages a *look*: superhero
poster, future baby, action figure, and so on. You supply only the inputs it
leaves open (usually a photo and a word or two); the prompt itself is baked
in and cannot be overridden.

Optional `?type=image|video` filters by media type. Other values return 400
`invalid_type`. No `subtype` query — same reason as `/v1/ai-tools`.

Exposure rule: every template with `status = approved` + `isActive` + an
enabled interface, **official and community alike** — the same set the public
gallery runs. Unlike `/v1/ai-tools` there is no per-row opt-in tag, because a
template IS the user-facing product rather than an internal wrapper. Running
a community template attributes its creator exactly as the website does.

Response:

```json
{
  "templates": [
    {
      "slug": "superhero-movie-poster",
      "name": "Superhero Movie Poster",
      "mediaType": "image",
      "subType": "",
      "summary": "One photo becomes a blockbuster teaser poster.",
      "coverUrl": "https://storage.zooop.ai/global/website/templates/superhero-movie-poster-cover.webp",
      "tags": ["poster", "movie"],
      "params": [
        { "id": "aspect_ratio", "type": "aspect_ratio", "default": "2:3",
          "options": ["1:1", "2:3", "3:2", "9:16"], "required": true },
        { "id": "image_urls", "type": "image_urls", "displayName": "Your photo",
          "constraints": { "maxCount": 1 } },
        { "id": "hero_name", "type": "text", "displayName": "Poster title",
          "default": "NIGHTFALL", "constraints": { "maxLength": 28 } }
      ],
      "official": true,
      "typicalPrice": { "typicalCredits": 5, "unit": "image" }
    }
  ]
}
```

A template priced per resolution reports `typicalPrice` as the per-run price
at its default resolution with every resolution's price in `note`
(`{"typicalCredits": 180, "unit": "call", "note": "480p: 180 / 720p: 257 credits per run"}`);
`POST /v1/quote` returns the exact charge plus `breakdown.templatePrice`.

`params[]` has the same shape as `/v1/models` and `/v1/ai-tools`. Two things
to notice on templates specifically:

- Params the template fixes (`prompt`, `quality`, …) are **absent** — sending
  one back returns 400 `invalid_payload` (`Param "prompt" is fixed by
  template`). Don't try to steer a template by prompt; pick a different
  template or call the raw model.
- Template-specific inputs (e.g. `hero_name`) are ordinary ids you submit
  like any other param. Their values get interpolated into the fixed prompt
  server-side; leaving one out falls back to its `default`.

### `GET /v1/templates/{slug}`

Fetch one template by stable slug — the same slug as the website URL
`https://zooop.ai/templates/image/{slug}`. Same shape as a single list entry.
Returns 404 `unknown_template` for unknown / draft / pending / rejected /
inactive slugs and for slugs whose interface is no longer enabled.

```bash
curl -fsS -H "Authorization: Bearer $ZOOOP_API_KEY" \
  "https://api.zooop.ai/v1/templates/superhero-movie-poster"
```

### `POST /v1/quote`

Price a hypothetical task without submitting. Same request body as
`POST /v1/tasks` (so an agent can reuse one payload for both calls).
No credits are charged, no DB row is created, no capacity is reserved —
safe to repeat freely.

Body — pick one shape:

```json
// (a) Raw model
{
  "interfaceId": "<uuid from /models>",
  "versionId": "standard",
  "params": { "prompt": "…", "duration": 5 }
}

// (b) AI tool (curated recipe)
{
  "aiTool": "<slug from /ai-tools>",
  "params": { "image_url": "https://storage.zooop.ai/…" }
}

// (c) Template (gallery preset)
{
  "template": "<slug from /templates>",
  "params": { "image_urls": ["https://storage.zooop.ai/…"], "hero_name": "DAFU" }
}
```

Body — **one of three shapes**, mutually exclusive. Sending more than one of
`interfaceId` / `aiTool` / `template` returns 400 `invalid_payload`.

Response:

```json
{
  "credits": 8,
  "estimatedSeconds": 18,
  "modelId": "uuid",
  "versionId": "standard",
  "modelName": "Kling V3",
  "breakdown": {
    "pricingKey": "720p",
    "base": 8,
    "multiplier": 1,
    "surcharges": 0,
    "basePrice": 0,
    "minPriceApplied": false
  }
}
```

- `credits` — authoritative cost for this exact payload. The `POST /v1/tasks`
  call WILL charge this number, provided input media durations don't change
  between quote and submit (media duration is part of the pricing basis).
- `estimatedSeconds` — P50 of the last 10 successful generations on this
  model. `null` when the model has no completion history yet.
- `breakdown` — itemised cost so the agent can explain "why" to the user:
  `final = max(minPrice, ceil(base × multiplier + surcharges + basePrice))`.

Errors mirror `POST /v1/tasks` for the same payload-validation paths
(`invalid_payload`, `missing_required_params`, `unknown_model`,
`model_not_public`). Quote also has its own `rate_limited` 429 (default
120 / min per token).

### `POST /v1/tasks`

Submit one generation task. Three body shapes are accepted — mutually
exclusive.

Body — **raw model path**:

```json
{
  "interfaceId": "<uuid from /v1/models>",
  "versionId": "standard",
  "params": { "prompt": "…", "image_url": "…", "duration": 5 }
}
```

Body — **AI tool path** (curated recipe):

```json
{
  "aiTool": "<slug from /v1/ai-tools>",
  "params": { "image_url": "https://storage.zooop.ai/…" }
}
```

Body — **template path** (gallery preset):

```json
{
  "template": "<slug from /v1/templates>",
  "params": {
    "image_urls": ["https://storage.zooop.ai/…"],
    "hero_name": "DAFU"
  }
}
```

On the AI-tool path the server resolves slug → recipe → underlying
interfaceId + versionId, merges your `params` with the recipe's
fixedParams / defaultParams / customParams, validates the merged shape,
and applies the recipe's pricing override. The keys allowed in `params`
come from the tool's `params[]` spec returned by `/v1/ai-tools/{slug}`.

The template path works the same way — slug → template → interfaceId +
versionId, your `params` merged over the template's fixed / default / custom
params, priced off the bound interface version plus the template's credit
markup. Allowed keys come from `/v1/templates/{slug}`. The resulting task
carries the template attribution, so a community creator is credited exactly
as they would be from the website.

On the raw path, the keys come from the model's `params[]` spec returned
by `/v1/models`. Param values are validated server-side via the same path
the web `/api/ai/execute` route uses.

**Header** `Idempotency-Key: <1–256 chars>` — repeat submissions with the
same `(token, key)` within 24 hours return the original `taskId` plus
`"idempotent": true` instead of creating a duplicate. Stripe semantics.

Strongly recommended on every submit: a slow-but-successful request (task
created + credits charged) can still time out before the response arrives,
and a blind retry would double-charge. `scripts/submit.sh` sets the header
automatically (default `sha256(body)`); if you call this endpoint directly,
send your own stable key and reuse it verbatim on retry. The header is
optional only in the sense that omitting it is allowed — but then duplicate
protection is off.

Response:

```json
{ "taskId": "uuid", "status": "queued", "modelId": "...", "versionId": "..." }
```

Errors:

| HTTP | code                       | Cause                                       |
| ---- | -------------------------- | ------------------------------------------- |
| 400  | `invalid_payload`          | Missing required input, bad shape, an attempt to set a param the tool / template fixes, OR more than one of `interfaceId` / `aiTool` / `template` set |
| 400  | `missing_required_params`  | Model `required: true` params absent; `error.params` lists each with type / options / default |
| 400  | `invalid_idempotency_key`  | `Idempotency-Key` header present but empty or > 256 chars |
| 401  | `missing_token` / `invalid_token` | Missing or revoked / expired PAT     |
| 402  | `arrears`                  | Account in arrears                          |
| 402  | `token_daily_cap_exceeded` | This task's cost would breach the token's daily cap (post-pricing precise check) |
| 403  | `model_not_public`         | Raw-path model exists but isn't on the public API surface (does not apply to AI-tool / template paths) |
| 403  | `account_banned`           | Token's owner is banned                     |
| 404  | `unknown_model`            | Bogus `interfaceId` or disabled model       |
| 404  | `unknown_ai_tool`          | Bogus `aiTool` slug, inactive recipe, or underlying interface disabled |
| 404  | `unknown_template`         | Bogus `template` slug, template not approved / inactive, or underlying interface disabled |
| 422  | `moderation_blocked`       | Text or image violates content policy       |
| 422  | `token_project_unbound`    | PAT's bound project was deleted — revoke + recreate |
| 429  | `rate_limited`             | Per-token rate-limit ceiling (default 60 req/min) |
| 429  | `token_daily_cap_reached`  | Token's `dailyCreditCap` already met before this call (coarse pre-check) |
| 503  | various                    | No enabled provider — pick a different model |

### `GET /v1/tasks/{id}`

Returns the current state of a task. Path-id is the `taskId` from submit.

```json
{
  "taskId": "uuid",
  "status": "succeeded",
  "type": "image",
  "kind": "t2i",
  "modelId": "interface-uuid",
  "outputs": [{ "url": "https://storage.zooop.ai/cdn-cgi/image/format=png,quality=95/.../uuid.webp",
                "thumbnailUrl": "https://storage.zooop.ai/cdn-cgi/image/format=png,quality=95/.../uuid-thumb.webp" }],
  "error": null,
  "creditsCharged": 4,
  "createdAt": "2026-05-14T01:23:45.000Z",
  "completedAt": "2026-05-14T01:24:12.000Z"
}
```

Public `status` values: `queued | running | succeeded | failed | cancelled`.
`type` is the media produced (`image` / `video` / `audio`), `kind` the
specific generation (`t2i`, `i2v`, `first-last-frame`, `text-to-speech`, …).
`outputs[]` lists every result (some models return several); `error` is set
for `failed` and `cancelled`, and `creditsCharged` drops to 0 once a task is
refunded. A token reads its owner's tasks in its own
scope — team tasks for a team token, personal ones for a personal token —
including ones made in the web app; anything else is 404 `unknown_task`.
Internal granular states (`pending`, `processing`, `uploading`, `moderating`)
are collapsed into `running` since they're not actionable for agents.

**Image output URLs** are served via Cloudflare Image Transformations
(`cdn-cgi/image/format=png,quality=95`). The `format=png` is a soft hint
that Cloudflare honours selectively:

- Source has **alpha** (background-removal, transparent stickers) →
  response is **`image/png`** with transparency preserved.
- Source is fully **opaque** (typical t2i / i2i output) → Cloudflare
  downgrades to **`image/jpeg`** to keep delivery size small. This is
  Cloudflare's standard behaviour and there is no URL switch to override.

Either way the response `content-type` reflects the actual format. Trust
the header, not the URL pathname (which still ends in `.webp` — that's
the source-object key, not the delivered format). When saving locally,
pick the extension from `content-type`:

```bash
URL="https://storage.zooop.ai/cdn-cgi/image/format=png,quality=95/.../uuid.webp"
CT=$(curl -sI "$URL" | awk 'tolower($1)=="content-type:" {print $2}' | tr -d '\r')
EXT=$(case "$CT" in image/png) echo png;; image/jpeg) echo jpg;; *) echo bin;; esac)
curl -fL -o "out.$EXT" "$URL"
```

Video / audio URLs pass through unchanged.

### `GET /v1/tasks[?status=&page=&pageSize=]`

The token owner's tasks in the token's bound project (team tasks for a team
token), newest first, each in the `GET /v1/tasks/{id}` shape. `status` filters
by public status; `page` starts at 1 (max 500); `pageSize` 1–100 (default 20).

```json
{ "tasks": [ { "taskId": "uuid", "status": "succeeded", "...": "..." } ],
  "page": 1, "pageSize": 20, "hasMore": false }
```

### `POST /v1/tasks/{id}/cancel`

Cancels a task that is still `queued` and refunds it to the wallet that paid.
Once the provider has it (`running`) it can't be stopped. Repeating the call
on a cancelled task is a `200` with `refundedCredits: 0`.

```json
{ "taskId": "uuid", "status": "cancelled", "refundedCredits": 70 }
```

Errors: 404 `unknown_task`, 409 `cancel_too_late` (running), 409
`task_already_finished` (succeeded / failed) — both 409s carry
`error.taskStatus`.

### `POST /v1/uploads`

Upload a local file in a single request. The file content is the raw HTTP
body (NOT multipart). `Content-Type` selects the media type. Returns a
public URL ready to feed into a subsequent `/tasks` submission.

```bash
curl -X POST \
  -H "Authorization: Bearer $ZOOOP_API_KEY" \
  -H "Content-Type: image/png" \
  --data-binary @cat.png \
  https://api.zooop.ai/v1/uploads
```

The upload lands under the PAT's bound project (same path as Web UI uploads),
so it shows up in the "Uploads" tab of the in-app history picker and counts
toward your storage quota.

**Image / audio — synchronous response** (typically < 1s):

```json
{
  "status": "ready",
  "url": "https://storage.zooop.ai/<userId>/<projectId>/<uuid>.png",
  "size": 123456,
  "contentType": "image/png"
}
```

**Video — asynchronous**. Returns `202` with an upload id:

```json
{
  "status": "processing",
  "uploadId": "<uuid>",
  "pollUrl": "/v1/uploads/<uuid>"
}
```

Poll `GET /v1/uploads/{uploadId}` until you get a terminal status.
Recommended cadence: 5s first poll, then 10–20s. Most clips resolve in
under a minute; the workflow has a 30-minute deadline.

**Image rejected by content policy**:

```json
{
  "error": {
    "message": "Uploaded content violates content policy",
    "type": "invalid_request_error",
    "code": "moderation_blocked",
    "labels": "porn"
  }
}
```
HTTP 451.

**Allowed Content-Type values**: `image/png`, `image/jpeg`, `image/webp`,
`image/gif`, `audio/mpeg`, `audio/wav`, `audio/webm`, `audio/ogg`,
`video/mp4`, `video/webm`, `video/quicktime`. Off-list values return 400
with the allowlist in the response.

**Size cap**: 100 MB (Cloudflare request-body limit). If you need to upload
something larger, use the Web UI then pass that URL to `/tasks`.

### `GET /v1/uploads/{uploadId}`

Poll the status of an async (video) upload returned by `POST /v1/uploads`.

```bash
curl -H "Authorization: Bearer $ZOOOP_API_KEY" \
  https://api.zooop.ai/v1/uploads/<uuid>
```

Response shapes:

```json
{ "status": "processing" }                                    # 202, still moderating
{ "status": "ready",   "url": "...", "contentType": "..." }   # 200, ready to use
{ "status": "blocked", "labels": "porn", "error": "..." }     # 200, rejected
{ "status": "errored", "reason": "..." }                       # 200, workflow gave up
```

Ownership: the upload id can only be polled by the PAT that created it.
Other tokens (even from the same user account) get 404 `unknown_upload`.

### `POST /v1/describe-image`

Analyse a reference image and return a structured prompt suitable for feeding
back into a generator (`subject` / `composition` / `style` / `lighting` /
`palette` / `mood` / `camera`, plus a single flowing `overallDescription`
paragraph).

Body:

```json
{
  "imageUrl": "https://storage.zooop.ai/<userId>/<projectId>/<uuid>.png",
  "language": "zh"
}
```

- `imageUrl` is **required** and MUST be a ZOOOP CDN URL (i.e. one returned
  by `POST /v1/uploads`). Foreign URLs are rejected — this avoids SSRF and
  guarantees the input has already been validated.
- `language` is **optional** — a locale code (`zh`, `zh-TW`, `ja`, `fr`,
  `es`, `de`, `pt`, `ru`, … ) that sets the output language. Every field,
  including `overallDescription`, is written in it; pass the locale the user
  is working in so the result is readable to them. Unknown / omitted →
  English.

Response:

```json
{
  "credits": 1,
  "subject": "A young woman with light skin in her 20s",
  "composition": "Centered portrait, eye-level framing",
  "style": "Soft photographic realism with film grain",
  "lighting": "Warm window light from the left, gentle shadows",
  "palette": "Muted earth tones with desaturated greens",
  "mood": "Contemplative and serene",
  "camera": "Shot at 50mm with shallow depth of field",
  "overallDescription": "A young woman with light skin in her 20s, ..."
}
```

- `overallDescription` is the canonical "ready-to-use" field — drop it
  straight into a generator's `prompt` param. The other dimension fields
  are best-effort and may be empty strings depending on the active vision
  model. Treat `overallDescription` as the only field with strong stability.
- `credits: 1` is charged on success (failures are refunded — see the error
  table below).
- `camera` may be `null` for compositionally minimal images.

Errors:

| HTTP | code                    | Cause                                                    |
| ---- | ----------------------- | -------------------------------------------------------- |
| 400  | `invalid_payload`       | `imageUrl` missing or not on a ZOOOP CDN host            |
| 402  | `insufficient_credits`  | Balance below 1 credit (no refund issued — nothing was charged) |
| 422  | `policy_violation`      | Vision model refused the image on content policy (refund issued) |
| 429  | `rate_limited`          | Default 10 / min per PAT                                 |
| 429  | `upstream_rate_limited` | Upstream LLM rate-limited us (refund issued — retry with backoff) |
| 503  | `vision_unavailable`    | Vision service unreachable (refund issued)               |

## Limits

- **Rate limit** (per PAT, 60-second sliding window):
  - `POST /v1/tasks` — 60 req/min
  - `POST /v1/quote` — 120 req/min
  - `POST /v1/uploads` — 30 req/min
  - `GET /v1/uploads/{id}` — 120 req/min
  - `GET /v1/me` — 120 req/min
  - `GET /v1/ai-tools` and `GET /v1/ai-tools/{slug}` — 120 req/min
  - `GET /v1/templates` and `GET /v1/templates/{slug}` — 120 req/min (own bucket)
  - `POST /v1/describe-image` — 10 req/min
  - `GET /v1/tasks` — 120 req/min
  - `POST /v1/tasks/{id}/cancel` — 60 req/min
  - `GET /v1/models`, `GET /v1/tasks/{id}` — unbounded
  - 429 responses carry `Retry-After` (seconds).
- **Tokens per user**: max 10 active. Revoke an old one to create a new one.
- **Daily credit cap (optional)**: per token; UTC-midnight rollover. Two
  enforcement points — coarse pre-check (`token_daily_cap_reached`, 429)
  and precise post-pricing check (`token_daily_cap_exceeded`, 402,
  prevents over-cap submission even when current spend < cap).
- **Concurrency**: `maxConcurrency` (personal token → the user's, default 3;
  team token → the team's shared pool) caps how many tasks run in parallel —
  excess queues in FIFO order and drains as earlier tasks complete.
  Rate-limit and concurrency are orthogonal: you can submit 60/min but only a
  few run at once.
- **Content policy**: prompts are checked before any credits are charged;
  uploaded images are checked synchronously on `POST /v1/uploads`, uploaded
  videos asynchronously via the poll route. Rejections surface as
  `moderation_blocked`.
- **Upload size**: 100 MB hard ceiling per file (Cloudflare request-body
  limit). Larger files: use the Web UI and pass the URL.

## Out of scope

- **Workspace management**: a token's scope (personal vs team) and bound
  project are fixed at creation in the web UI — the API can't switch them. A
  team token is issued by a team owner/admin and spends the team's shared
  credits; otherwise the endpoints are identical to a personal token.
- **Project management**: tokens are bound to one project at creation. To
  switch projects, revoke and create a new token.
- **Canvases / story timeline**: the API exposes single-shot generation only.
- **Streaming progress**: poll instead.
- **Listing uploads**: there is no upload list — keep the URLs
  `POST /v1/uploads` returns. (Tasks: `GET /v1/tasks`.)

## Transient errors — what to retry, how to diagnose

A single failed request often has nothing to do with the API. Retry the
transient class with exponential backoff before declaring an outage.

**Retry (transient, usually self-heals):**
- TCP / TLS errors with no HTTP status — `ECONNRESET`, `EAI_AGAIN`, curl
  exit codes `6` (DNS), `7` (connect), `35` / `52` / `56` (TLS / recv).
- HTTP `502` / `503` / `504`.
- HTTP `429` — honor `Retry-After`.
- Cloudflare `520`–`526`.

**Do NOT retry:**
- Other `4xx` (auth / validation — retry won't help).
- `451 moderation_blocked` — same bytes will be rejected again.
- `422 token_project_unbound` — bound project deleted; user must rotate
  the token.

**Pattern:** up to 3 attempts, exponential backoff 1s → 3s → 9s, honor
`Retry-After`. If all 3 fail, surface the error.

**Special case — `POST /v1/tasks` that times out with no response body**
(curl exit `28`, or an outer command-timeout hard-kill with no exit code):
the submit path runs cold-start + media probing + workflow dispatch
synchronously, so the task is often already created and charged by the time
the connection stalls — most visible on the *first* submit of a session.
Always submit with an `Idempotency-Key` (the bundled `submit.sh` does this by
default). Then a timeout is safe to retry **with the same key + same body** —
the server returns the original `taskId` (`"idempotent": true`) rather than
duplicating. If you have a candidate id, `GET /v1/tasks/{id}` to reconcile.
Do not re-submit a modified request after a timeout.

**Diagnostic before declaring outage:**

```bash
curl -fsS -o /dev/null -w "%{http_code}\n" https://zooop.ai
curl -fsS -o /dev/null -w "%{http_code}\n" https://api.zooop.ai/llms.txt
```

If `zooop.ai` is up but `api.zooop.ai` keeps failing, only THEN report an
outage — otherwise it's almost always local network or transient.
