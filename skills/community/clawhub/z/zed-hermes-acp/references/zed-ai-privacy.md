# Zed AI Privacy & the Hermes Boundary

Lean distillation of Zed's `ai/privacy-and-security` and `ai/ai-improvement` docs,
for the `zed-hermes-acp` skill. Linux-only. Source: zed.dev/docs/ai/*.

## Core boundary (read this first)
- Hermes runs in Zed as an **External Agent** (ACP process you own).
- Per Zed's request-path table, External Agents route model requests to
  "the External Agent and its configured providers" — handled "under its own terms."
- Consequence: Hermes threads sit **outside Zed's AI feedback/training collection**.
  Zed's rating, feedback, and Edit Prediction opt-ins govern **Zed-hosted**
  features only — not Hermes threads.
- Data boundary ownership for Hermes:
  - Model/provider config, auth, API keys, subscriptions -> owned by **Hermes**
  - Tool/MCP behavior -> depends on agent + ACP config
  - Training data, ratings, improvement telemetry -> **Hermes's** terms, not Zed's
- Zed "does not retain your prompts or code context by default" and "only
  retains AI data when you explicitly share feedback or opt in."

## AI request paths (distilled)
Each path has a different data owner; the table below is the privacy-relevant split.
- **Zed-hosted models** -> Zed routes to hosted providers (zero-retention, no-training; see below)
- **Provider API keys** -> configured provider, under its terms; keys in system keychain, not settings.json
- **Existing subscriptions** -> subscription provider, under its terms
- **Gateways** -> gateway + upstream providers, under their terms
- **Local models** -> local/self-hosted server, under your config
- **External Agents (Hermes)** -> the agent + its providers, under their terms
- **Terminal Threads** -> CLI/TUI owns auth, routing, tools, MCP, data handling
- **Edit Prediction** -> selected provider; per-keystroke local context sent
- **Agent tools / MCP / integrations** -> Zed, MCP servers, external systems (scope by profile/permissions)
- **Project trust + instructions** -> trusted worktree; External Agents may read own instruction files

## Zed-hosted model commitments (NOT Hermes)
- Provider agreements: prohibit training on prompts/code context; require
  **zero data retention** for inference, *except* provider-designated safety retention.
- Providers with documented no-training + zero-retention: Anthropic, Google, OpenAI.
- **Safety-retention exception**: some providers retain limited data for
  designated "Covered Models" (e.g. Anthropic Claude Fable 5) >= 30 days, for
  trust & safety. Applies on every platform; Zed cannot opt out; no-training
  still holds (used for safety review, not training). Switching to your own API
  key/subscription does **not** avoid it for covered models.
- These commitments bind **Zed-hosted** inference. Hermes uses its own providers
  under Hermes's terms — verify retention with the provider Hermes calls.

## What Zed retains — opt-in only (Zed-hosted scope)
Zed keeps AI data solely when you explicitly share or opt in:
- **Response ratings / feedback**: sharing sends the conversation thread to Zed
  (your messages, AI responses, thread metadata, install metadata). Opt-in per
  share; stored in Snowflake; anonymized; reviewed to refine prompts/tools.
  - This applies to **Zed-hosted** response UIs. Hermes threads are owned by
    Hermes; rating behavior there follows Hermes, not this Zed flow.
- **Edit Prediction training data**: collected only if ALL hold: (1) opt-in via
  Training Data Collection toggle, (2) project is open source (license file
  present), (3) file not in `edit_predictions.disabled_globs`. Collects code
  around cursor, recent diffs, prediction, repo URL/revision, buffer outline +
  diagnostics. Stored in Snowflake; public dataset at zed-industries/zeta.
  - Edit Prediction is a **Zed-native** feature; irrelevant to Hermes threads.
- If you neither rate/feedback nor opt in, Zed stores no Customer Data from AI
  usage for improvement. (Telemetry is separate — see Controls.)

## Controls & related docs
- Telemetry: collected separately (AI feature used, response time, edit accept/reject); control via Telemetry settings.
- Privacy for Business: data sharing off by default; admins block feedback/training opt-in.
- Turn AI off: AI Quick Start -> "turn AI off."
- Further: Zed Privacy Policy, Subprocessors, Terms of Service.

## Linux specifics
- Settings path: `~/.config/zed/settings.json` (custom `XDG_CONFIG_HOME` overrides). Not macOS/Windows paths.
- Hermes ACP registers under `agent_servers` -> `hermes-agent` (custom, command `hermes`, args `[acp]`).
- `dev: open acp logs` (Ctrl+Shift+P) shows Zed<->agent traffic for boundary/debug questions.

## Section refs (zed.dev/docs)
- AI Privacy: `ai/privacy-and-security` (#ai-request-paths, #data-retention-and-training, #provider-safety-retention, #ai-data-retained-by-zed)
- Feedback & Training: `ai/ai-improvement` (#ai-feedback-with-ratings, #edit-predictions, #business-controls)
- External Agents: `ai/external-agents`  (request-path owner for Hermes)
- Skill depth: `references/zed-external-agents.md`, `hermes-agent` skill
