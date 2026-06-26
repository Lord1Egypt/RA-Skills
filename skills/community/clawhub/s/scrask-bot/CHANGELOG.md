# Changelog

All notable changes to Scrask are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.3.0] - 2026-05-25

### Added

- **Hybrid invocation model.** Scrask is now invoked implicitly by
  default (the OpenClaw agent reads `## Invocation` in `SKILL.md` and
  routes screenshots automatically) AND can be explicitly invoked by
  the user with any of the new aliases:
  - `scrask`
  - `scrask this`
  - `screenshot`
  - `screenshot to calendar`

  Aliases work with or without `@` / `/` prefixes. The platform must
  check explicit aliases first; if none matches, fall back to the
  implicit trigger conditions.
- **New `invocation` block in the manifest** (`metadata.openclaw`):
  declares `mode: hybrid` and the alias list. This is the declarative
  contract the platform consumes to know which strings should
  force-dispatch to Scrask.

### Changed

- **`SKILL.md` "Trigger Conditions" section renamed and rewritten** as
  `## Invocation`. Documents both modes side by side with explicit
  examples and a brief rationale for when each path fires.

### Compatibility

- **Fully backward compatible.** The implicit trigger conditions are
  preserved verbatim under the `Implicit (default…)` subheading. Any
  agent that has been reading the old prose continues to behave
  exactly the same. The aliases simply add a second, more direct path.

## [4.2.0] - 2026-05-25

### Added

- **OpenClaw as a first-class provider.** New `--provider openclaw`
  mode uses whichever vision LLM the platform has configured. Scrask
  reads three env vars OpenClaw injects into skill subprocesses:
  `OPENCLAW_VISION_PROVIDER` (`"anthropic"` or `"google"`),
  `OPENCLAW_VISION_KEY`, and optional `OPENCLAW_VISION_MODEL`.
- **`parse_with_openclaw()`** helper in `scripts/scrask_bot.py`. Routes
  to the existing `parse_with_claude` or `parse_with_gemini` based on
  what the platform reports.
- **Optional `model` parameter** on `parse_with_claude` and
  `parse_with_gemini`, so the platform can override the default model
  name without mutating module globals.

### Changed

- **`auto` mode is now credential-aware** rather than Gemini-only:
  - `GEMINI_API_KEY` set → Gemini-first with Claude fallback (existing
    v4.1 behaviour, preserved for users who opt in).
  - Only `ANTHROPIC_API_KEY` set → Claude directly.
  - Neither set → defer to OpenClaw's configured vision LLM.

  Result: the skill works out of the box for any OpenClaw user with a
  vision-capable platform LLM. No skill-level API key is required.
- **`GEMINI_API_KEY` is no longer required.** Removed from
  `metadata.openclaw.requires.env` in `SKILL.md`; both keys are now
  listed under `optional_env`. `primaryEnv` removed.
- **Env-var validation** in `main()` updated. Auto mode no longer
  errors out when `GEMINI_API_KEY` is missing; it only errors when
  none of (Gemini key, Claude key, OpenClaw injection) is available.
- **`_parse_with_auto_fallback` renamed** to
  `_parse_with_gemini_claude_fallback` for clarity. A new
  `_parse_with_auto` wraps the credential-aware routing logic.
- **Docs:** `SKILL.md`, `README.md`, `docs/decision-flow.md`,
  `docs/decision-flow.html` updated with the new provider model. The
  parser-side flowchart now shows the auto-routing decision tree.

### Compatibility

- **Fully backward compatible.** Existing users with `GEMINI_API_KEY`
  set continue to get exactly the same Gemini-first behaviour they
  had in v4.1. Users with both keys still get Gemini → Claude
  fallback. Only the failure mode changed: instead of refusing to
  run, Scrask now uses the platform LLM when no skill-level key is
  set.

## [4.1.0] - 2026-05-25

### Added

- **Per-field confidence scoring.** Each extracted field (`title`, `date`,
  `time`, `location`, `participants`, `description`, `priority`, etc.) now
  carries its own 0.0-1.0 confidence score in a new `confidences{}` map per
  item. Replaces the single-confidence-per-item model.
- **Two top-level decision confidences.** `actionable_confidence` (is this
  screenshot about an event or task at all?) at the result level, and
  `type_confidence` (calendar event or task list?) per item.
- **`clarifications[]` array on each item.** Pre-formatted, targeted
  clarification questions the bot asks the user when a field is missing or
  low-confidence. Example: `"What time is dinner with Priya?"` instead of a
  generic `"is this right?"` prompt.
- **`needs_actionable_confirmation` flag** at the result level. When the
  parser is unsure the screenshot is actionable at all, the bot asks before
  dispatching.
- **`participants[]` field.** Names extracted when visible. Never invented.
- **Three new threshold constants** (`ACTIONABLE_THRESHOLD`,
  `TYPE_THRESHOLD`, `FIELD_THRESHOLD`, all 0.70) with matching CLI flags
  (`--actionable-threshold`, `--type-threshold`, `--field-threshold`).
- **New documentation:**
  - `docs/ARCHITECTURE_OVERVIEW.md` — how Scrask is built, written for both
    technical and non-technical readers.
  - `docs/decision-flow.md` — Mermaid flowcharts of the parser and bot
    decision flow, plus the threshold reference table.
  - `docs/decision-flow.html` — interactive version of the same with
    clickable nodes (detail popups for every decision and threshold).
  - `docs/example-walkthrough.md` — a concrete USER ↔ BOT ↔ PARSER
    transcript.

### Changed

- **`shape_intent` rewritten** to build the clarifications list by walking
  mandatory fields per item type. `needs_confirmation` is now derived from
  the presence of outstanding clarifications, not a single threshold
  comparison.
- **Gemini → Claude auto-fallback** triggers on the worst per-field score
  across all items, not a synthetic per-item number. Finer-grained signal,
  catches cases where the model is broadly confident but missed a single
  critical field.
- **`format_summary`** renders clarifications as a bullet list with
  targeted questions, leads with the actionable-gate prompt when relevant.
- **Docs sweep:** `README.md`, `SKILL.md`, and
  `.github/copilot-instructions.md` rewritten to reflect the new schema and
  flow. Removed lingering Scrask v3 references (direct Google Calendar
  writes, `--dry-run`, `GOOGLE_CREDENTIALS`, and several functions that no
  longer exist).

### Compatibility

- **Backward compatible.** Items in the legacy single-confidence schema (no
  `confidences{}` block) still route correctly via the legacy
  `DEFAULT_CONFIDENCE_THRESHOLD` (0.75) gate. Anything reading
  `item["confidence"]` still works — synthesized as
  `min(confidences.values())` when not directly provided by the model.

## [4.0.0]

### Changed

- **Refactored from direct Google Calendar / Tasks writes into a
  parse-and-delegate skill.** Scrask now emits structured intent JSON and
  the OpenClaw agent delegates writes to whichever destination skill the
  user has installed (`calctl`, `accli`, `apple-calendar`,
  `brainz-calendar`, `gcal-pro`, `apple-reminders`, `things-mac`, `notion`,
  etc.).
- **Removed direct Google API dependencies.** No `GOOGLE_CREDENTIALS`, no
  service-account JSON, no Calendar / Tasks client construction inside
  Scrask.

### Added

- **Provider routing:** `auto` (Gemini first, Claude fallback when needed),
  `gemini` (Gemini only), `claude` (Claude only).
- **`screenshot_summary`, `end_date`, `source_type`** surfaced in the parse
  output for downstream destination skills.

## [3.x] - prior

Direct integration with Google Calendar and Google Tasks via service-account
credentials. Superseded by the v4 parse-and-delegate architecture.
