# Design

ShowMeAI Skill 2.1 separates Agent reasoning from a platform-neutral Python runtime.

## Goals and boundaries

The Skill covers creative workflow routing, one-time credential setup, model/default configuration, ShowMeAI calls, durable polling, and local result download. It does not provide a ShowMeAI account, bypass token-group permissions, run a background daemon after the host is killed, or guarantee that every cataloged task model is enabled for every Key.

`SKILL.md` is the concise Agent behavior and routing contract. `DESIGN.md` records architecture, alternatives, limitations, and decisions; operational detail belongs in `references/`. This SKILL–DESIGN division keeps routine Agent context small while preserving rationale for maintainers.

## Alternatives and trade-offs

| Alternative | Benefit | Trade-off | Decision |
|---|---|---|---|
| Store config under each Agent brand | Familiar on one host | Repeats setup and creates divergent state | Rejected |
| Require environment variables only | Simple implementation | Agents repeatedly ask for the Key | Kept as an override, not the sole store |
| Return task IDs immediately | Short command runtime | User often never receives the media | Rejected |
| Maintain one static model list | Easy documentation | Quickly becomes stale and ignores token groups | Rejected |
| Intersect live models with a local capability catalog | Group-aware and parameter-aware | Task APIs sometimes need verify-on-use | Selected |

## Architecture overview

```text
User intent
    │
    ▼
SKILL.md routing ──► references/<workflow>.md
    │
    ▼
scripts/showmeai.py
    ├── config + credentials ──► OS-native app directory
    ├── live models ∩ catalog ──► model/default guidance
    ├── HTTP + retries ─────────► ShowMeAI API
    ├── task journal + polling ─► terminal state
    └── output manager ─────────► local media file
```

The Agent owns ambiguous creative interpretation and explains choices. The scripts own deterministic validation, secret handling, request construction, state machines, retries, and file writes.

First-use readiness is also runtime-owned. Key validation and category-default confirmation are separate states: `needs_key`, `needs_defaults`, and `complete`. Generation commands enforce category readiness, so an Agent cannot bypass onboarding by starting creative intake early. Categories are progressive and independent; completing image setup does not falsely mark video or audio defaults as reviewed.

## Security model

Secrets resolve in this order: `SHOWMEAI_API_KEY`, legacy `Showmeai_API_KEY`, then the OS-native credentials file. The Key is never stored in `config.json`. Setup accepts secrets through hidden input or standard input and returns only a four-character fingerprint. Files are written atomically and the credential mode is `0600` where supported.

## Long-running state

Every asynchronous submission creates a `TaskRecord` before polling. Each response is atomically journaled. Polling has a capped interval but no default wall-clock timeout. Terminal success requires downloadable result URLs; terminal failure becomes a structured error. Retryable transport failures have a configured ceiling, and pending records can be resumed by a later process.

## Known limitations

- `/v1/models` can only prove visibility in the current token group; task-only capabilities may require live verification.
- A killed host cannot continue executing Python, so recovery is journal-based rather than a permanent background service.
- The local catalog must be updated when ShowMeAI introduces new parameter schemas.
- Voice names, task payloads, and supported media settings can differ by model and group.
- Fulfilling an image count can require multiple concurrently billed API requests when a model lacks native batching or returns an incomplete batch.

## Decision records

### D-001 · Platform-neutral paths

Use OS-native application config/state directories with environment overrides. Never bind runtime state to OpenClaw, Codex, Hermes, WorkBuddy, or another Agent brand.

### D-002 · Standard-input Agent setup

Allow a trusted Agent to receive a user-provided Key and pass it over process standard input. Never accept the secret as a command argument. Persist it after live validation so future Agents do not ask again.

### D-003 · Gemini 3.1 Flash Image preference

Use `gemini-3.1-flash-image` as the fresh-install image preference. Preserve the setup user's visible-model selection and model-specific parameter defaults.

### D-004 · Terminal-state polling

Do not treat submission as completion. Persist, poll with capped backoff, emit heartbeats, download every result, and allow explicit recovery through `tasks resume`.

### D-005 · Multi-image count fulfillment

Treat the requested image quantity as a runtime output contract independently of model-specific count support. Use a native count parameter when cataloged; otherwise, or when a successful upstream response is incomplete, submit bounded parallel one-image completion requests until the count is satisfied. Aggregate usage, report the physical request count, and return a structured error instead of silently returning an incomplete result.

### D-006 · Runtime-enforced progressive onboarding

Do not treat a validated Key as completed setup. Require an explicit model and supported-parameter decision once per requested media category, persist that state in schema version 3, and reject new generation with `ONBOARDING_REQUIRED` until it is complete. Agent-assisted standard-input setup returns choices but never silently confirms them.

### D-007 · Host configuration isolation

Expose resolved paths through `paths --json` and explicitly forbid Agents from storing ShowMeAI state in a host application's config or `.env` file. Editing defaults through the low-level `config set` command invalidates that category's onboarding confirmation until it is revalidated with `onboarding apply`.

## File structure

```text
references/
├── audio.md
├── configuration.md
├── image-tools.md
├── image.md
├── polling.md
├── three-d.md
└── video.md
```

The remaining runtime structure is documented in `README.md` to avoid maintaining two full file trees.
`SKILL.md` delegates the distribution inventory to the annotated tree in `README.md`.
