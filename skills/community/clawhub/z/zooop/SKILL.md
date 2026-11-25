---
name: zooop
description: |
  Generate or edit images / videos / audio via the ZOOOP AI platform — t2i,
  i2i, t2v, i2v, lipsync, upscale, remove-background, TTS, voice-clone,
  sound-effect, music, plus ZOOOP's published one-click templates (superhero
  poster, future baby, action figure, …) run by slug. Use whenever the user
  asks to generate, create, make, edit, or transform any of those media
  types, or names a ZOOOP template / pastes a zooop.ai/templates link.
---

# ZOOOP AI generation

Public REST API host: `https://api.zooop.ai` (override via `$ZOOOP_API_HOST`).
Auth: `Authorization: Bearer $ZOOOP_API_KEY` on every request.

`scripts/{upload,quote,submit,poll,download,ai-tools,templates,describe}.sh` ship with
this skill. Inline `curl` recipes below work the same way if the bundle isn't
cloned. Full request / response / error reference:
[`references/api-docs.md`](./references/api-docs.md) — read it whenever this
guide doesn't cover a field.

## API key — setup

**The token must NEVER appear in the agent conversation.** Token in chat
risks leaking into training corpora, telemetry, or shared transcripts —
once leaked it spends the user's credits until revoked. Always have the
**user** set the env var themselves, in their own terminal.

Agent: check `$ZOOOP_API_KEY` (or OS-equivalent). If empty, give the user
these instructions **verbatim** — do not ask them to paste the token back:

1. Get a token. **Personal** (spends your own credits): visit
  [https://zooop.ai/user?tab=apiKeys](https://zooop.ai/user?tab=apiKeys) → **Create token** → pick project
   (immutable) → **set a daily credit cap** → copy token (shown ONCE).
   **Team** (spends the team's shared credits): a team owner/admin creates
   it in the team admin → API Keys tab. Everything below works identically.
2. In their **own terminal** (NOT this chat), set the env var:
  - macOS / Linux / WSL / Git Bash —
   `echo 'export ZOOOP_API_KEY=zpk_live_…' >> ~/.zshrc && source ~/.zshrc`
  - Windows PowerShell —
  `[Environment]::SetEnvironmentVariable('ZOOOP_API_KEY','zpk_live_…','User')`
  - Windows cmd — `setx ZOOOP_API_KEY "zpk_live_…"`
3. **Restart the agent** so the new env var is inherited.

Tasks and uploads land under the token's bound project. `GET /v1/me` shows
the active wallet and balance (`user.creditBalance` personal, `team.creditBalance` team).

## Three paths: raw model, AI tool, template

**Default to raw models.** The other two are narrow, deliberate surfaces:

- **AI tools** cover capabilities raw text-to-image / text-to-video models
  CAN'T replicate — chiefly precise background removal and image / video
  upscaling. For everything else (style transfer, edits, age changes,
  character animations, etc.) a raw model is more flexible AND cheaper.
- **Templates** are the site's one-click looks (superhero poster, future
  baby, action figure, …). Reach for one when the user names that specific
  look, or asks for "that viral effect" — the prompt behind it is tuned and
  hard to reproduce blind. Don't route generic requests through a template:
  its prompt is fixed and you cannot steer it.


| Path                                        | When                                                                                                                                                           | How                                                                                    |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Raw model** (`interfaceId` + `versionId`) | Default. Text-driven generation, prompt-driven edits, anything where you'd write a prompt                                                                      | `GET /v1/models?type=…&subtype=…` → submit with `interfaceId` + `versionId` + `params` |
| **AI tool** (`aiTool` slug)                 | Specialized non-prompt-driven capabilities only — currently background removal + image/video upscale. Browse `GET /v1/ai-tools` to see what's actually exposed | `GET /v1/ai-tools` → submit with `aiTool: <slug>` + the tool's `params[]`              |
| **Template** (`template` slug)              | The user wants a specific published look ("超英海报", "future baby", "手办"), or hands you a `zooop.ai/templates/…` link. Browse `GET /v1/templates`             | `GET /v1/templates` → submit with `template: <slug>` + the template's `params[]`        |


`/v1/ai-tools` is a short curated list. If your task isn't on it, don't force
it through — use a raw model with a tailored prompt.

```bash
bash scripts/ai-tools.sh [image|video]   # browse catalog, optionally filtered
bash scripts/ai-tools.sh -s <slug>       # one tool's full param schema

bash scripts/templates.sh [image|video]  # browse every published template
bash scripts/templates.sh -s <slug>      # one template's full param schema
```

Then reuse the raw-path `submit.sh` / `quote.sh`, swapping `<interfaceId> <versionId>` for `--ai-tool <slug>` or `--template <slug>`:

```bash
bash scripts/submit.sh --ai-tool background-removal '{"image_url":"https://storage.zooop.ai/…"}'
bash scripts/submit.sh --template superhero-movie-poster \
  '{"image_urls":["https://storage.zooop.ai/…"],"hero_name":"DAFU"}'
```

### Working with templates

- **The slug is the URL.** `https://zooop.ai/templates/image/superhero-movie-poster`
  → `template: "superhero-movie-poster"`. If the user pastes a template link,
  take the slug straight from it and skip the catalog browse.
- **Only send what the template exposes.** `GET /v1/templates/{slug}` lists
  exactly those params. Anything the template fixes (`prompt`, `quality`, …)
  is absent from that list, and sending it back is a 400
  (`Param "prompt" is fixed by template`). A template you can't steer is
  working as designed — if the user wants a different look, use a raw model.
- **Template-specific inputs are ordinary params.** e.g. `hero_name` on the
  superhero poster: pass it in `params` like any other id and it gets woven
  into the fixed prompt server-side. Omit it and its `default` applies.
- Both official and community templates are callable, and cost is quoted the
  same way (`quote.sh --template <slug> …`).

## How model selection works (raw path)

Pick a (type, subType) pair by **what the user wants to do**, not by what
inputs they happen to provide. Slug names like `motion-control` / `text-ref`
aren't self-explanatory — read the descriptions, don't guess from the name.


| type  | subType          | What it's for                                                                                                                                                                                                                                                                                                |
| ----- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| image | default          | Generate a new image, **or edit an existing one from a plain text description** (text-to-image, img-to-img, style transfer, prompt-driven edits — GPT Image 2 / Nanobanana handle "把背景换成…" / "去掉左边的人" without any mask)                                                                                      |
| image | edit-image       | Targeted region edit driven by a **black-and-white mask or hand-drawn annotation** the user supplies. Only pick this when the user actually provides (or asks to draw) a mask/region — never for plain text-described edits                                                                                  |
| image | image-svg        | Generate **scalable vector graphics** (`.svg`) — logos, icons, flat illustrations, infographics — from a text prompt, or vectorize a raster image. Recraft Text/Image-to-Vector models; output is editable vector paths, NOT a raster PNG. Pick this only when the user explicitly wants vector / SVG output |
| video | text-ref         | Generate a video from a prompt. Some models also accept reference images **for style** (referenced as `@Image1` / `@Image2` in the prompt) — these guide look, NOT motion                                                                                                                                    |
| video | first-last-frame | **Animate a still image** — provide one image as the start frame and the model generates motion outward. Optional end frame interpolates between two keyframes                                                                                                                                               |
| video | motion-control   | Make an image move using motion **copied from a reference video** (e.g. the character in the image performs the action / dance in the reference clip)                                                                                                                                                        |
| video | audio-lipsync    | Make a character image lip-sync to a given audio track                                                                                                                                                                                                                                                       |
| video | extend-video     | Continue an existing video — append more frames after its last one                                                                                                                                                                                                                                           |
| video | video-edit       | Restyle or re-edit an existing video clip                                                                                                                                                                                                                                                                    |
| audio | text-to-speech   | TTS in a named voice                                                                                                                                                                                                                                                                                         |
| audio | voice-clone      | Speak text using a voice cloned from a reference audio sample                                                                                                                                                                                                                                                |
| audio | sound-effect     | One-shot sound effect from a text description                                                                                                                                                                                                                                                                |
| audio | music            | Music track from a text description                                                                                                                                                                                                                                                                          |


For the per-model required fields (which image / video / audio params, and
which are optional), read `params[].required` on the model returned by
`/v1/models`. Don't infer from the subType — different models in the same
subType can have different param requirements.

### Disambiguation — pick subType by intent

The hard cases are video subTypes (and image edits), where the user's
**goal** decides, not which media they happen to hand you:


| User says…                                                                                           | Pick                       | Why                                                                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "把这张图的背景换成海边" / "remove the person on the left" / "edit this photo to…" (image + text only, no mask) | **image/default**          | Plain-text edits go through `default` with GPT Image 2 or Nanobanana — they take a reference image + edit prompt natively. `edit-image` is the wrong pick because it requires a mask the user didn't provide.              |
| "我画了个 mask / 涂了一块区域，只改这里"                                                                            | **image/edit-image**       | The user actually has a mask or hand-drawn region. That's the only time `edit-image` is right.                                                                                                                             |
| "做个矢量图 / SVG" / "我要可缩放可编辑的 logo 矢量文件" / "as an SVG / vector"                                         | **image/image-svg**        | The deciding signal is **vector / SVG**, not the word "logo" or "icon" — those alone usually mean a normal raster image (use `default`). Only route here when the user wants an editable, infinitely scalable vector file. |
| "让这张图动起来" / "animate this poster"                                                                    | **video/first-last-frame** | Goal: bring a still image to life. The image is a *start frame*.                                                                                                                                                           |
| "用这张图当风格参考生成视频" / "use this image as a style reference"                                              | **video/text-ref**         | Goal: generate a new scene; image only shapes look. Reference image goes into the model's `image_urls` / `reference_image_urls` param and is cited as `@Image1` in the prompt.                                             |
| "让这个角色跳这段舞" / "make this character do this dance"                                                    | **video/motion-control**   | Goal: transplant motion from a reference video onto an image.                                                                                                                                                              |
| "让这个人对口型说这段话" / "lip-sync this audio to my photo"                                                    | **video/audio-lipsync**    | Goal: drive an image's mouth from audio.                                                                                                                                                                                   |
| "续写这段视频" / "extend this clip"                                                                        | **video/extend-video**     | Goal: more frames after the last one.                                                                                                                                                                                      |
| "把这段视频换风格" / "restyle this video"                                                                    | **video/video-edit**       | Goal: change look/feel of existing video.                                                                                                                                                                                  |
| Pure prompt → video, no input image                                                                  | **video/text-ref**         | Goal: generate from text alone.                                                                                                                                                                                            |


Each model has one or more `versions` (e.g. `standard` / `pro` / `fast`)
with a coarse `typicalPrice` summary like
`{ typicalCredits: 8, unit: "second", note: "~40 credits for 5s @ 720p" }`.
That's enough to explain ballpark cost to the user. For an **exact** quote,
call `POST /v1/quote` (see "Quote before submit"). Final cost is enforced
server-side at submit time and echoed in `creditsCharged`.

## Standard workflow

1. **(Optional, first call only)** `GET /v1/me` — remaining daily budget,
  wallet balance (personal or team), bound project name, rate-limit numbers.
2. **Discover models** for the matching subtype:
  ```bash
   curl -fsS "$ZOOOP_API_HOST/v1/models?type=video&subtype=motion-control" \
        -H "Authorization: Bearer $ZOOOP_API_KEY"
  ```
   Match the user's hint (e.g. "用 seedance2") against `name` / `brand.name`.
   No hint → follow "Default model selection" below. If the user named a
   published look instead of a model, browse `GET /v1/templates` and submit
   `template: <slug>`.
3. **(Optional) Upload local files.** If the user gave a path on disk:
  ```bash
   bash scripts/upload.sh /path/to/file.png
   # → prints the storage URL to feed into params.
  ```
   Wraps `POST /v1/uploads`. Image / audio return sync; video is processed
   asynchronously — the script polls until ready (5–30s typical). Rejected
   content → exits non-zero.
4. **Quote the task** — exact credits + ETA, no side effects:
  ```bash
   bash scripts/quote.sh <interfaceId> <versionId> '<params-json>'
   # → { "credits": 8, "estimatedSeconds": 18, "breakdown": {...} }
  ```
   Safe to repeat. See "Quote before submit" for the confirmation policy.
5. **Submit the task**:
  ```bash
   bash scripts/submit.sh <interfaceId> <versionId> '<params-json>'
   # → { "taskId": "...", "status": "queued", "modelId": "...", "versionId": "..." }
  ```
   `submit.sh` attaches an `Idempotency-Key` (default `sha256(body)`), so a
   submit that times out is safe to recover by **re-running the identical
   command** — see "Idempotency". Never tweak the params on a timeout retry to
   "avoid a duplicate"; that changes the key and creates a real duplicate.
6. **Poll until terminal** (`succeeded` / `failed` / `cancelled`). If the user
   changes their mind while the task is still `queued`,
   `POST /v1/tasks/{id}/cancel` stops it and refunds the credits:
  ```bash
   bash scripts/poll.sh <taskId>
   # → { "status": "succeeded", "outputs": [{"url": "..."}], "creditsCharged": 4 }
  ```
7. **Show the URL, then offer download.** Proactively ask *"Want me to
  download it to a local file?"* (unless the user already said they only
   want the URL) — on yes, run:

## Quote before submit

Before every `POST /v1/tasks`, call `POST /v1/quote` with the **same body**
to get exact credits + P50 ETA. No charge, no DB row, no capacity hold —
safe to call as often as you like.

```bash
curl -fsS -X POST "$ZOOOP_API_HOST/v1/quote" \
  -H "Authorization: Bearer $ZOOOP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"interfaceId":"...","versionId":"...","params":{...}}'
# → { "credits": 8, "estimatedSeconds": 18, "modelName": "Kling V3",
#     "breakdown": { "pricingKey": "720p", "base": 8, "multiplier": 1, ... } }
```

After the quote, print **one compact summary line** before submitting —
just the agent's choice + cost, so the user can sanity-check it. Don't
echo the prompt back; they just typed it and re-reading it is noise.

```
→ Kling V3 · 720p · 8 credits · ~18s
```

**Confirmation policy** (don't confirm on every task — annoying):


| Situation                                        | Behaviour                                                  |
| ------------------------------------------------ | ---------------------------------------------------------- |
| Default — single task, no opt-in/out             | Print summary line, submit. No "should I continue?".       |
| User said "不用问我" / "just go" / "make N variants" | Submit silently, no extra confirmation.                    |
| User said "ask me before spending" / "贵的让我确认"    | Confirm before submitting.                                 |
| Batch (≥ 3 tasks OR total ≥ 100 credits)         | Confirm once for the whole batch unless already opted out. |
| `estimatedSeconds == null`                       | Say "ETA unknown" — don't invent a number.                 |


If the quote returns 400 / 404, fix the payload and re-quote — never submit
a request that just failed to quote.

## Default model selection

When the user's request is vague and does NOT name a model / brand / quality
tier, pick the curated defaults below.

### Images (`type=image, subtype=default`)

- Default model: **GPT Image 2.0** with `quality: "low"`, `resolution: "2k"`,
`aspect_ratio: "1:1"`. ~80% of cases are fine at `low`; `medium` handles
~95% of needs. Also strong for prompt-driven edits.
- **Quality-sounding words inside the user's prompt are prompt-words, not
param hints.** Phrases like "highest quality", "最高质量", "4k",
"ultra-realistic", "cinematic", "电影级" appear as decorative descriptors
in almost every prompt — they do NOT mean the user is asking you to bump
the `quality` param. Keep `quality: "low"`.
- Bump to `quality: "medium"` when the request is non-trivial (detailed
composition, important visual fidelity) or when a `low` result didn't
satisfy.
- `quality: "high"` only for genuinely complex requests (intricate detail,
fine typography, multi-subject composition) OR when the user explicitly
passes `params.quality: "high"`.
- Switch to a different image model only when the user explicitly asks
(e.g. "use Flux" / "用 Seedream"). Don't switch on a quality complaint.

### Videos (`type=video, subtype=text-ref`)


| User signal                             | Pick                                                                                                    |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| "highest quality" / "best" / "电影级"      | **Seedance 2**                                                                                          |
| Balanced (default — no explicit signal) | **Kling O3** → fallback to **Kling V3** → **Happy Horse** → **Grok Imagine** (pick first one available) |
| "cheap" / "fastest" / "性价比" / "便宜"      | **Grok Imagine**                                                                                        |


Match by `name` (case-insensitive substring) or `brand.name` against `/v1/models`.

### Other categories

For every other (type, subType), use `**models[0]`** from `/v1/models` —
it's pre-sorted, so the first row is the recommended default.

## Reference image → prompt (`POST /v1/describe-image`)

Turn a user-supplied reference image into a structured, ready-to-feed prompt.

**Call this only when** you need to extract a specific dimension from the
image (subject / style / lighting / palette / …), OR the user explicitly
asks to reverse-engineer a prompt from a picture. Otherwise **skip it** —
most image / video models accept a reference image directly through their
own param (e.g. `image_urls` / `reference_image_urls`), so feed the picture
straight into the submit without a describe round-trip (saves a credit and
a step).

```bash
bash scripts/describe.sh <https://storage.zooop.ai/…> [language]
# language: optional locale code (zh / ja / fr / es / …); omitted → English
# → { "credits": 1, "overallDescription": "A vibrant ...", "subject": "...",
#     "composition": "...", "style": "...", "lighting": "...", "palette": "...",
#     "mood": "...", "camera": "..." }
```

- Input MUST be a ZOOOP CDN URL (returned by `/v1/uploads`). Foreign URLs are
rejected — pipe local files through `upload.sh` first.
- Costs 1 credit per call.
- Optional `language` sets the output language — every field (including
`overallDescription`) comes back in it. Pass the locale the user is working
in so they can read the result; unknown / omitted → English.
- `overallDescription` is the canonical one-paragraph prompt; other fields
are best-effort and may be empty when the model can't tell.

## Endpoints


| Method | Path                     | What                                                    |
| ------ | ------------------------ | ------------------------------------------------------- |
| GET    | `/v1/me`                 | Self-introspection                                      |
| GET    | `/v1/models`             | List public models by `type` × `subtype`                |
| GET    | `/v1/ai-tools`           | List curated AI tools (optional `?type=image|video`)    |
| GET    | `/v1/ai-tools/{slug}`    | Full param schema for one tool                          |
| GET    | `/v1/templates`          | List published templates (optional `?type=image|video`) |
| GET    | `/v1/templates/{slug}`   | Full param schema for one template                      |
| POST   | `/v1/quote`              | Price a task (`interfaceId` OR `aiTool` OR `template`)  |
| POST   | `/v1/tasks`              | Submit a generation (`interfaceId` OR `aiTool` OR `template`) |
| GET    | `/v1/tasks/{id}`         | Poll status / outputs                                   |
| POST   | `/v1/uploads`            | Upload a file (raw body + `Content-Type`)               |
| GET    | `/v1/uploads/{uploadId}` | Poll async (video) upload status                        |
| POST   | `/v1/describe-image`     | Reference image → structured prompt (1 credit)          |


Full request / response shapes live in `references/api-docs.md`.

## Reading a model's params schema

`/models` returns `params: InterfaceParam[]` per model. Each entry carries
`id` (the key to set in `params`), `type`, `required`, `options`,
`constraints`, `default`. Media-URL types (`image_url`, `video_url`,
`audio_url`, `first_frame`, `last_frame`, `mask_url`, `voice`, …) accept
only ZOOOP-hosted URLs — pipe foreign URLs / local paths through
`upload.sh` first. Full type list and behaviour: `references/api-docs.md`.

## Uploads — single-step raw-body

```bash
curl -X POST "$ZOOOP_API_HOST/v1/uploads" \
  -H "Authorization: Bearer $ZOOOP_API_KEY" \
  -H "Content-Type: image/png" \
  --data-binary "@$HOME/Desktop/cat.png"
```

`Content-Type` drives how the file is processed AND the resulting file
extension — pass the file's REAL mime, not a guess. Image / audio return sync
(`{ "status": "ready", "url": ..., "size": ..., "contentType": ... }`).
Video returns `{ "status": "processing", "uploadId": ..., "pollUrl": ... }`
— then poll `GET /v1/uploads/{uploadId}` until `ready` / `blocked` / `errored`.

Allowed mimes, size cap (100 MB), and full poll-status shapes: see
`references/api-docs.md` → `POST /v1/uploads`.

## Error response shape

OpenAI-style envelope:

```json
{ "error": { "message": "...", "type": "invalid_request_error",
             "code": "missing_required_params", "params": [...] } }
```

- `type` — broad family: `invalid_request_error` / `authentication_error` /
`permission_error` / `rate_limit_error` / `api_error`. Branch on `code`.
- `param` — set when one field is at fault.
- `missing_required_params` carries a structured `params` array with `id`,
`type`, `default`, `options`, `constraints` — self-correct in one
round-trip without re-fetching the model.

Most common codes (full table in `references/api-docs.md`):


| HTTP | code                       | Meaning                                          |
| ---- | -------------------------- | ------------------------------------------------ |
| 400  | `missing_required_params`  | Required model params absent — see `params` hint |
| 400  | `invalid_payload`          | Bad body shape                                   |
| 401  | `invalid_token`            | Token missing / revoked / expired                |
| 402  | `token_daily_cap_exceeded` | This task's cost would breach the daily cap      |
| 404  | `unknown_model`            | Bogus `interfaceId` or disabled model            |
| 422  | `moderation_blocked`       | Text or image violates content policy            |
| 422  | `token_project_unbound`    | Bound project deleted — revoke + recreate token  |
| 429  | `rate_limited`             | Honor `Retry-After`                              |
| 503  | various                    | No enabled provider — try another model          |


## Transient errors

Up to 3 attempts with exponential backoff (1s → 3s → 9s), honor
`Retry-After`. Retry only: connection errors with no HTTP status, `5xx`,
`429`. Don't retry other `4xx`, `451 moderation_blocked`, or
`422 token_project_unbound`. Full retry table + outage-diagnostic curls:
`references/api-docs.md` → "Transient errors".

**Submit timed out with no response (curl exit 28 / outer kill)?** The task
may already exist — `submit.sh` likely created it before the connection
stalled. Recover by **re-running the exact same `submit.sh` command** (the
`Idempotency-Key` returns the original `taskId`), or reconcile with
`GET /v1/tasks/{id}` if you captured an id. Never submit a fresh, modified
request — that double-charges.

## Idempotency (automatic on submit)

`POST /v1/tasks` is the only retryable **write**, and a slow-but-successful
submit (task created + credits charged) can still time out before the
response reaches you. So `submit.sh` always sends an `Idempotency-Key`
(default `sha256(body)`). The server caches it 24h; a repeat submit with the
same `(token, key)` returns the original `taskId` plus `"idempotent": true`
instead of creating — and charging for — a duplicate. Stripe semantics.

Rules:
- **Retry a timed-out submit by re-running the identical command.** Same key
  → same task → no double charge.
- **Don't add "uniqueness" to params to dodge duplicates** — that's backwards;
  it changes the hash and produces a genuine duplicate.
- To intentionally launch N tasks from identical params, set a distinct
  `ZOOOP_IDEMPOTENCY_KEY` per submission.
- Calling the raw endpoint yourself? Set the `Idempotency-Key` header
  manually — the dedup only works if you do.

## Rate limits

Per-PAT, 60s sliding window. Headline: `tasks 60/min`, `quote 120/min`,
`uploads 30/min`, `me / upload-poll / ai-tools / templates / task-list 120/min`, `task cancel 60/min`, `describe-image 10/min`. `/models` and `/tasks/{id}` are unbounded. `429` carries
`Retry-After`. Full table: `references/api-docs.md` → "Limits".

## What this skill does NOT do

- It does **not** manage projects, canvases, or organizations — single-shot
generation only. PAT's bound project is fixed at creation time.
- It does **not** stream progress — poll instead.
- It does **not** auto-download outputs; always **ask** first (step 7)
and pick the save extension from response `content-type`.
- It does **not** allow uploads > 100 MB via the API — direct the user to
the Web UI for those.

