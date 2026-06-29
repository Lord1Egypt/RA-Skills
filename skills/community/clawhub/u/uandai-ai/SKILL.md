---

name: uandai-ai

description: Uandai platform — configure API access, package OpenClaw workspace zip, upload agents, delete trainer-owned agents, list subscriptions, invoke runs.

metadata: {"openclaw":{"requires":{"env":["UANDAI_API_KEY","UANDAI_API_ORIGIN","APP_SITE_URL"]},"primaryEnv":"UANDAI_API_KEY","homepage":"https://api.uandai.ai/docs/programmatic-api"}}

---

# Uandai (packaging + programmatic API)

**Bundled docs version:** 2026.06.25

Use this skill for **all** Uandai automation: first-time setup, workspace packaging, upload, subscriptions, and invocation.

## First-time setup (chat → persist)

When the user sends a **configure Uandai** message with settings, or env vars are missing:

1. Parse from the user message (setup-only; do not repeat key in later work prompts):

   - `UANDAI_API_ORIGIN` — API host without `/api` (e.g. `https://api.uandai.ai` or `http://127.0.0.1:8000`)

   - `APP_SITE_URL` — uandai.ai web app origin (no trailing slash; e.g. `https://app.uandai.ai` or `http://127.0.0.1:8080`)

   - `UANDAI_API_KEY` — full `uand_live_…` from uandai.ai app → Settings → API Keys

   **API base URL (derived — do not store separately):** `{UANDAI_API_ORIGIN}/api` (e.g. `https://api.uandai.ai/api`). Use this prefix for all programmatic paths (`/v1/…`).

2. Install the **full skill folder** (`SKILL.md` + `references/`) under `~/.openclaw/skills/uandai-ai/` (preferred) or `<workspace>/skills/uandai-ai/` for local dev.

3. Merge into `~/.openclaw/openclaw.json` under `skills.entries.uandai-ai`:

```json5
{
  skills: {
    entries: {
      "uandai-ai": {
        enabled: true,
        apiKey: "uand_live_…",
        env: {
          UANDAI_API_KEY: "uand_live_…",
          UANDAI_API_ORIGIN: "https://api.uandai.ai",
          APP_SITE_URL: "https://app.uandai.ai",
        },
      },
    },
  },
}
```

4. Do **not** echo the full API key back. Tell the user to run `/new` or restart the gateway.

5. Optional smoke test: exchange → `GET /v1/auth/me`.

**Security:** Prefer a private OpenClaw session for setup messages that contain the key. After setup, operational prompts need no key and no doc URLs.

## Before any Uandai action

**Read bundled reference files in this skill directory first.** Do not rely on `web_fetch` unless the user explicitly pastes a Uandai doc URL in the current message.

| Task | Read |
|------|------|
| Package workspace zip | `references/agent-packaging.md` |
| Exchange, upload, delete, invoke | `references/programmatic-api.md` |
| Gallery screenshots + video (REST) | `references/programmatic-api.md` § Gallery media (proxy `POST /media`; direct upload when `direct_upload_enabled`) |
| Subscriber OpenClaw gateway (`/openclaw`) | `references/openclaw-integration.md` |

Optional live refresh: if the user pastes `{UANDAI_API_ORIGIN}/docs/agent-packaging`, `/docs/programmatic-api`, or `/docs/openclaw-integration` in chat, you may `web_fetch` that URL and prefer it for that session.

Default prod origins: API `https://api.uandai.ai` (base `{ORIGIN}/api`); app `https://app.uandai.ai`

## Required inputs before API calls

Do **not** call Uandai business endpoints until all required inputs for that endpoint are known.

| Source | Examples |
|--------|----------|
| Env / config (setup once) | `UANDAI_API_ORIGIN`, `APP_SITE_URL`, `UANDAI_API_KEY`, exchanged `access_token`; API base = `{UANDAI_API_ORIGIN}/api` |
| User message (minimal ZIP upload) | **`agent_name`**, **`description`**, packaged zip |
| User message (full ZIP upload) | `agent_name`, `description`, `subscription_price`, `default_model_identifier`, provider URL test value (when required), custom/skill test rows — **not** `{PROVIDER}_KEY` |
| User message (invoke) | `configs`, confirm `agent_id` / `revision_no` |
| Prior API response | `agent.id`, `revision_no` from upload `201` body (`{ "agent": { "id", "revision_no", … } }`); activations list for invoke |

If any **user-sourced** field is missing or ambiguous:

1. Ask the user in one concise message listing only missing fields.
2. **Do not** call the endpoint with placeholders, defaults, or guesses.
3. Confirm values briefly (never echo secrets).

Per-endpoint prerequisite tables and checklists: `references/programmatic-api.md`.

## Packaging (OpenClaw workspace → zip)

Stable rules (full steps in `references/agent-packaging.md`):

1. **Never** zip the live workspace root directly
2. **Staging:** copy to `output/<agent>-workspace/` with exclusions → validate → zip **staging contents only**
3. **Output:** `output/<agent-name>-workspace.zip`
4. **Uandai zip layout:**

   - Personality files (`SOUL.md`, `IDENTITY.md`, …) at **zip root**
   - No extra parent wrapper folder in the archive
   - `SKILL.md` only at `skills/<id>/SKILL.md`, `workspace/skills/<id>/SKILL.md`, or zip root
   - Exclude `node_modules/`, `.env`, `logs/`, `memory/`, `.openclaw/`, `output/`, **`uandai-ai/`** — max **50MB**

5. **Do not include this skill in the upload zip.** Install on the trainer machine at `~/.openclaw/skills/uandai-ai/` (full folder with `references/`). A copy under `<workspace>/skills/uandai-ai/` is for local dev only — exclude it when packaging.

6. Report: `📍 Path: MEDIA:<path-to-zip>`

Common failures: personality only under `workspace/`; nested wrapper folder; misplaced `skill/SKILL.md`; **`uandai-ai/` in zip** (`openclaw_bundle_platform_skill`).

## API authentication (exchange required)

Raw API keys work **only** on exchange:

```http
POST /v1/auth/token
Authorization: Bearer $UANDAI_API_KEY
```

Alternative on exchange only: send the raw key in header `X-Uandai-Api-Key` or JSON `{ "api_key": "…" }`.

Response: `{ "access_token", "refresh_token", "user" }` — cache in session memory.

**All other calls:** `Authorization: Bearer <access_token>`

On access expiry: `POST /v1/auth/refresh`. On refresh `401`: re-exchange if key still active; else user creates a new key in Settings.

Do **not** send `$UANDAI_API_KEY` on upload, invoke, or list endpoints.

## After upload (trainer)

Upload `201` response shape: `{ "agent": { "id", "revision_no", "name", … } }`.

Always return to the user:

1. **`agent.id`** — numeric agent id from the response
2. **`revision_no`** — current revision from the same response (needed for proposal updates and invoke)
3. **Manage link** — `{APP_SITE_URL}/training-center/agents/manage/{agent.id}` where they set subscription price, invokable duration, provider LLM URL (when required), default model, and remaining marketplace fields (subscribers supply provider API keys at subscribe/invoke)

Use `APP_SITE_URL` from skill env (setup above). Do not guess the app origin.

## Workflows

**Trainer — publish end-to-end (minimal ZIP):** setup → read `references/agent-packaging.md` → package zip → collect **`agent_name`** + **`description`** from user → exchange → `POST {UANDAI_API_ORIGIN}/api/v1/agents/upload` with `bundle` → return **`agent.id`** and **`revision_no`** from the upload response → share manage link `{APP_SITE_URL}/training-center/agents/manage/{agent.id}` (pricing, duration, provider LLM, model, invocation settings) → user completes there or via `POST /agents/{id}/proposals` → `PATCH …/proposals/{id}` `status=submitted` when ready

**Trainer — full ZIP upload:** collect all ZIP prerequisites from user → optional `GET /agents/duration-pricing` when invokable → exchange → `POST /v1/agents/upload` with `bundle` + `agent_name` + `description` + `subscription_price` + `default_model_identifier` + provider `config_data_type_json` / `test_values_json` (Ollama: `OLLAMA_URL` only — **never** `OLLAMA_KEY`; prefer `agent_duration_pricing_id` over `invokable_duration_seconds` when invokable) → return **`agent.id`**, **`revision_no`**, and the same manage link

**Trainer — minimal ZIP only:** collect **`agent_name`** + **`description`** + packaged zip → exchange → `POST /v1/agents/upload` with `bundle` — do **not** block on price/model at upload time; do **not** use multipart `files` for the minimal path

**Trainer — list / delete agent:** optional `GET /agents/created` (includes `can_delete` + `delete_blockers`) or `GET /agents/{agent_id}/delete-eligibility` → confirm `agent_id` with user → `DELETE /agents/{agent_id}` → on `200` confirm `{ "agent_id", "deleted": true }`; on `409` explain the structured `code` (e.g. `agent_delete_entitled_subscribers` + `destroys_at`) — do **not** retry without resolving it

**Subscriber — discover:** exchange → `GET /v1/me/subscriptions` → `GET /v1/me/activations?invokable_only=true` (or `invokable_only=false` to include archived `agent_removed` history)

**Subscriber — invoke:** exchange → `GET /v1/me/activations?invokable_only=true` → skip rows with `agent_removed: true` or `is_invokable: false` → **collect `configs` from user** (and confirm numeric `agent_id` / `revision_no`) → `POST /v1/executions` → poll `GET /v1/executions/{run_id}` until terminal (`status` may start as `queued` or `pending_payment`)

**Subscriber — archived agent:** if `agent_removed: true`, do **not** invoke or PATCH configs (`410` on configs); run history remains via `GET /v1/executions?user_agent_id={user_agent_id}`

## Safety

- Never log or echo the full API key
- On `401`: refresh → re-exchange → key may be revoked
- On `402`: user needs credits
- API keys cannot create/revoke other keys (Settings / password JWT only)
