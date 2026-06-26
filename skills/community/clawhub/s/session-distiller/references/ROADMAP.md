# ROADMAP — session-distiller

## Known Issues

### context-gate.py: Live Session Token Counts Null (Permanent Workaround — 2026.3.11+)
- Gateway API returns `null` for `totalTokens`, `remainingTokens`, `percentUsed` on all live sessions
- Only completed cron sessions report `inputTokens`
- Root cause: regression introduced in OpenClaw 2026.3.11 — token counts not populated for active sessions via `gateway call status`
- **Upstream issue status (2026-03-14):** Upstream maintainers addressed the symptom only at the display layer (openclaw/openclaw #43987, PR #44045) — `session_status` now renders `?/...` instead of a misleading `0/...`. The underlying API fields (`totalTokens`, `remainingTokens`, `percentUsed`) remain null as of 2026.3.13. See openclaw/openclaw #45268 for the deeper tracking issue; maintainers consider the display-layer fix sufficient.
- **Workaround implemented:** JSONL fallback — reads session file on disk, counts chars, estimates tokens at chars÷4. Token source tagged in log output (`[api]`, `[api:inputTokens]`, or `[jsonl-estimate]`). Gate auto-switches back to API source if upstream restores the fields.
- **Assessment:** JSONL fallback should be treated as the permanent workaround. Upstream is unlikely to restore raw API field population. Tracked in <your-repo>/session-distiller as a known upstream dependency issue.
- **Tracked:** <your-repo>/session-distiller issue #5 (upstream bug reference)

### Batch Cron Timeout (Resolved — v0.2.0)
- ~~The 03:00 cron had a 600-second timeout causing consistent failures with ~44 sessions × LLM calls~~
- **Resolved:** Cron timeout increased to 1800s in v0.2.0. 5 consecutive failures observed before fix.
- Additional mitigation: `--min-age-hours 48` reduces batch size on large backlogs

### Hardcoded openclaw Binary Path
- `context-gate.py` calls `/opt/homebrew/bin/openclaw` directly
- Non-Homebrew installations will need to adjust this path
- Should be discoverable via `which openclaw` or env var

### macOS-Only
- `trash` CLI is macOS-specific
- Session paths assume `~/.openclaw/agents/main/sessions/`
- Cross-platform support is a Phase 4 goal

---

## Future Ideas

### Phase 4 — Community Release
Package session-distiller as a publishable skill on ClawHub that any operator can install, configure, and run.

**Changes needed:**
- Replace `LIVE_ALLOWLIST_KEYS` hardcoded dict with external config file (`distiller.yaml`)
- Accept `--model` flag instead of hardcoded model name
- Auto-discover session paths from OpenClaw config or CLI args
- ~~Strip all deployment-specific defaults~~ **Resolved v0.5.0** — configurable paths via env vars; docs de-identified
- Cross-platform path handling (macOS/Linux/Windows)
- Fallback for `trash` on Linux (`gio trash`, `trash-put`)
- `--init` / `--setup` wizard to generate cron entries
- Example configs for single-user, group chat, and multi-agent setups

**Estimated effort:** ~2 days (1 day cleanup/generalization, 1 day testing + ClawHub packaging)

### Incremental Distillation
- Rather than one LLM call per session, stream chunks as they accumulate
- Reduces per-call latency and overall timeout risk
- Requires rethinking the dedup model

### Multi-Model Support
- Allow non-Anthropic models for distillation (GPT-4, Gemini, local LLMs)
- Accept `--model` flag or config file entry
- Validate distillation quality across models before defaulting

### Prompt Iteration
- A/B test prompt variations for extraction quality
- Track NO_DISTILL rates by prompt version
- Consider session-type-specific prompts (group chat vs. direct)

### Re-Anchor (Planned)
- After context compaction or a long gap between runs, re-establish baseline state by re-reading current daily log and offset positions
- Prevents stale offsets from causing re-distillation of already-processed content after file rotation or manual edits
- Would integrate with `--live` mode: detect drift between saved offsets and actual file state before processing

### Metrics / Observability
- Track sessions processed, distillation latency, NO_DISTILL rate, error counts
- Expose via a simple dashboard or daily summary
- Alert on sustained error rates (beyond individual cron timeout alerts)
