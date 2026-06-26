---
name: skill-hub-gateway
description: Unified gateway skill for async execute/poll, portal user closure, and telemetry feedback workflows.
version: 2.4.2
metadata:
  openclaw:
    skillKey: skill-hub-gateway
    emoji: "🧩"
    homepage: https://gateway.binaryworks.app
    requires:
      bins:
        - node
---

# Skill Hub Gateway

Default API base URL: `https://gateway-api.binaryworks.app`

Default site base URL (for upload route): `https://gateway.binaryworks.app`

Chinese documentation: `SKILL.zh-CN.md`

## Version Check Protocol (Agent)

- Official latest version source: `GET /skills/manifest.json` -> `data.version`.
- Local current version source: this installed `SKILL.md` frontmatter `version`.
- Compare versions using semantic version order (`major.minor.patch`).
- Check timing: once at session start, then at most once every 24 hours within the same session.
- If version check fails (network/timeout/parse error), do not block runtime execution. Continue current workflow and retry at the next allowed check window.

## Agent Decision Flow

- If `latest_version > current_version`, read the matching section under `Release Notes` in this document to build `update_summary`.
- Agent should show the user:
  - `current_version`
  - `latest_version`
  - `update_summary`
- User decision options:
  - `Update now`
  - `Remind me later in this session`
- If user chooses `Remind me later in this session`, suppress repeated prompts for the same target version until a new session starts.

## First-Time Onboarding (install_code)

Scripts auto-complete onboarding by default:

1. `POST /agent/install-code/issue` with `{"channel":"local"}` or `{"channel":"clawhub"}`.
2. Read `data.install_code`.
3. `POST /agent/bootstrap` with `{"agent_uid":"<agent_uid>","install_code":"<install_code>"}`.
4. Read `data.api_key`, then call runtime APIs with `X-API-Key` or `Authorization: Bearer <api_key>`.

Manual override:

- You can still provide `api_key` explicitly.
- If `agent_uid` and `owner_uid_hint` are omitted, scripts derive stable local defaults from the current workspace path.

## Legacy Runtime Contract (Compatibility)

- Execute: `POST /skill/execute`
- Poll: `GET /skill/runs/:run_id`

## Portal Actions (User Closure)

Action catalog (single default path per action):

- `portal.me` -> `GET /user/me`
- `portal.balance` -> `GET /user/points/balance`
- `portal.ledger.query` -> `GET /user/points/ledger`
- `portal.usage.query` -> `GET /user/usage`
- `portal.skill.execute` -> `POST /user/skills/execute`
- `portal.skill.poll` -> `GET /user/skills/runs/:runId`
- `portal.skill.presentation` -> `GET /user/skills/runs/:runId/presentation`
- `portal.voucher.redeem` -> `POST /user/vouchers/redeem` (write)
- `portal.recharge.create` -> `POST /user/recharge/orders` (write)
- `portal.recharge.get` -> `GET /user/recharge/orders/:orderId`

Write safety gate:

- `portal.voucher.redeem` and `portal.recharge.create` require `payload.confirm === true`.
- If `confirm` is missing or not `true`, action runner rejects the call locally and does not send write traffic.

## Payload Contract

Default payload conventions:

- `payload.input` is the primary input object for `portal.skill.execute`.
- `payload.request_id` is optional and passed through as-is.
- Query actions use `payload` fields directly as query params (`date_from`, `date_to`, `service_id`, `channel`).

Media normalization conventions:

- Prefer explicit URL fields already present in input: `image_url`, `audio_url`, `file_url`.
- If `attachment.url` exists, map it to the capability target URL field.
- If `file_path` exists, auto-upload through `{site_base}/api/blob/upload`, with fallback to `{site_base}/api/blob/upload-file` when `@vercel/blob/client` is unavailable, then backfill URL into input before execution.
- For agent runtimes that do not include `@vercel/blob/client`, you can also pre-upload media via your backend (for example Vercel Blob) and pass `attachment.url` or explicit URL fields.
- `site_base_url` is a guarded field: runtime only accepts the trusted configured site base URL (default `https://gateway.binaryworks.app` or env `SKILL_SITE_BASE_URL`).
- Users should not need to manually paste media URLs in normal product flows.

Presentation files:

- `portal.skill.presentation` accepts optional `include_files=true` to return `visual.files.assets` with rendered file URLs.
- `portal-action.mjs` defaults `include_files=true` for `portal.skill.presentation` unless explicitly disabled.
- Image runs return `overlay` (boxed image), plus `mask` / `cutout` assets when available.
- Audio runs normalize data URLs to `output.media_files.assets` with uploaded file URLs when blob storage is configured.

## Runtime Auth Bridge

User-scoped actions use a fixed auth bridge:

1. Resolve runtime API key context (`api_key`, `agent_uid`, `owner_uid_hint`, `base_url`).
2. `GET /agent/me` with `X-API-Key` + `x-agent-uid` to resolve `user_id`.
3. `POST /user/api-key-login` with `user_id + api_key` to obtain `userToken`.
4. Execute Portal Action with `Authorization: Bearer <userToken>`.

## Insufficient Points Recovery

For `POINTS_INSUFFICIENT` responses:

- Keep `error.code` and `error.message` unchanged.
- Preserve and surface `error.details.recharge_url` when available.
- Diagnostic logs should recommend `portal.recharge.create` or direct open of `recharge_url`.

## Bundled Files

- `scripts/execute.mjs` (CLI args: `[api_key] [capability] [input_payload] [base_url] [agent_uid] [owner_uid_hint]`)
- `scripts/poll.mjs` (CLI args: `[api_key] <run_id> [base_url] [agent_uid] [owner_uid_hint]`)
- `scripts/feedback.mjs` (CLI args: `[api_key] [payload_json] [base_url] [agent_uid] [owner_uid_hint]`)
- `scripts/telemetry.mjs` (shared best-effort telemetry helper)
- `scripts/runtime-auth.mjs` (shared auto-bootstrap helper)
- `scripts/portal-auth.mjs` (api-key -> user session bridge)
- `scripts/portal-action.mjs` (CLI args: `[api_key] <action> <payload_json> [base_url] [agent_uid] [owner_uid_hint]`)
- `scripts/attachment-normalize.mjs` (attachment URL/path normalization + upload)
- `references/capabilities.json`
- `references/openapi.json`
- `SKILL.zh-CN.md`

## Telemetry and Feedback

- Bundled scripts now support best-effort telemetry emit for auth/execute/poll/feedback flows.
- Telemetry is non-blocking and does not change runtime exit semantics if telemetry delivery fails.
- Optional environment variables:
  - `SKILL_TELEMETRY_ENABLED` (`true` by default)
  - `SKILL_TELEMETRY_BASE_URL` (defaults to runtime `base_url`)
  - `SKILL_TELEMETRY_TIMEOUT_MS` (`2000` by default)
- Feedback script posts to `POST /feedback/submit` with runtime auth (`X-API-Key`) and attaches `agent_uid` + `owner_uid_hint` in metadata.

## Capability IDs

- `human_detect`
- `image_tagging`
- `tts_report`
- `embeddings`
- `reranker`
- `asr`
- `tts_low_cost`
- `markdown_convert`
- `face-detect`
- `person-detect`
- `hand-detect`
- `body-keypoints-2d`
- `body-contour-63pt`
- `face-keypoints-106pt`
- `head-pose`
- `face-feature-classification`
- `face-action-classification`
- `face-image-quality`
- `face-emotion-recognition`
- `face-physical-attributes`
- `face-social-attributes`
- `political-figure-recognition`
- `designated-person-recognition`
- `exhibit-image-recognition`
- `person-instance-segmentation`
- `person-semantic-segmentation`
- `concert-cutout`
- `full-body-matting`
- `head-matting`
- `product-cutout`
## Release Notes

When publishing a new version, add a new section here. Agent update summaries must be generated from this block.

### 2.4.2 (2026-03-12)

**What's New**

- Added `/api/blob/upload-file` direct-upload fallback for `file_path` flows when `@vercel/blob/client` is unavailable.
- Added `portal.skill.presentation` file rendering (`visual.files.assets`) for overlay/mask/cutout URLs.
- Added audio output normalization to return `output.media_files.assets` with uploaded file URLs when blob storage is configured.

**Breaking/Behavior Changes**

- None.

**Migration Notes**

- For agent runtimes without `@vercel/blob/client`, send `file_path` as before; the runtime now falls back to direct upload.
- To receive rendered files, call `portal.skill.presentation` with `include_files=true` or rely on the portal default.

### 2.4.1 (2026-03-12)

**What's New**

- Added server-side `portal.skill.execute` input normalization for `attachment.url` (both `input.attachment.url` and top-level `attachment.url`).
- Added explicit media URL precedence guard (`image_url`/`audio_url`/`file_url` take priority over `attachment.url` when both are present).
- Added end-to-end tests for upload-first execution payload compatibility and precedence behavior.
- Clarified fallback guidance for runtimes missing `@vercel/blob/client` to use backend pre-upload URLs.

**Breaking/Behavior Changes**

- None.

**Migration Notes**

- Existing `portal-action.mjs` workflows remain compatible.
- For local file workflows in constrained agent runtimes, prefer backend pre-upload then pass `attachment.url` or explicit media URL.

### 2.4.0 (2026-03-12)

**What's New**

- Added Portal Actions contract for single-skill user closure flows (`portal.me`, balance/ledger/usage, execute/poll/presentation, voucher and recharge actions).
- Added local double-confirm write gate: `portal.voucher.redeem` and `portal.recharge.create` require `confirm=true`.
- Added runtime auth bridge script (`portal-auth.mjs`) for `api_key -> user session`.
- Added action runner (`portal-action.mjs`) and attachment normalization script (`attachment-normalize.mjs`) with `attachment.url` and `file_path` support.
- Standardized insufficient-points diagnostics to preserve `recharge_url` in passthrough envelopes.

**Breaking/Behavior Changes**

- Write actions now fail fast locally when `confirm=true` is absent.

**Migration Notes**

- Existing `execute.mjs` and `poll.mjs` workflows remain available.
- Portal users should call `portal-action.mjs` for user closure actions.

### 2.3.4 (2026-03-11)

**What's New**

- Added best-effort telemetry emit in runtime scripts for auth/execute/poll flows.
- Added `scripts/feedback.mjs` to submit structured feedback via runtime auth (`X-API-Key`).
- Added shared telemetry helper with optional env controls (`SKILL_TELEMETRY_*`).

**Breaking/Behavior Changes**

- None.

**Migration Notes**

- Existing execute/poll calls remain unchanged.
- If you run scripts in constrained environments, allow optional telemetry calls to `/agent/telemetry/ingest` and `/telemetry/ingest`.

### 2.3.3 (2026-03-11)

**What's New**

- Standardized user-facing guidance around upload-based flows: do not expose manual URL/JSON fields for media/document inputs.
- Updated capability reference examples and wording to match upload-first product UX.
- Renamed CLI argument label from `input_json` to `input_payload` for consistency with structured payload semantics.

**Breaking/Behavior Changes**

- None.

**Migration Notes**

- Existing runtime API calls remain unchanged.
- If your integration shows custom input forms, prefer file/attachment inputs instead of manual URL/JSON text fields.
