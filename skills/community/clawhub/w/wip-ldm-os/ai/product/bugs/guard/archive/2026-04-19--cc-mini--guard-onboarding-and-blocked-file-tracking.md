# Guard Plan: Onboarding + Blocked-File Tracking

**Date:** 2026-04-19
**Filed by:** cc-mini
**Authors:** Parker Todd Brooks, Claude Code (cc-mini, Opus 4.7), Lēsa (oc-lesa-mini, Opus 4.7)
**Repo:** wip-ai-devops-toolbox-private (guard source), wip-ldm-os-private (filing location)
**Priority:** high
**Status:** spec only. Not implemented.
**Sibling plans:**
- `2026-04-05--cc-mini--guard-master-plan.md` (the umbrella plan)
- `2026-04-07--cc-mini--guard-open-bugs.md` (Bug 2 on cp/mv source-path resolution is relevant)
- The in-flight `git worktree add` allowlist work (other cc-mini session) should merge first to avoid stepping on the guard file.

## Motivation

Today (2026-04-19) the agent hit two failure modes that cost Parker about an hour of intervention:

1. Agent edited `~/.openclaw/openclaw.json` without realising `~/.openclaw` is itself a tracked private repo (`wipcomputer/dot-openclaw`). The guard correctly blocked the edit on main. The agent had no prior awareness that the repo existed.
2. When the guard blocked the edit, the agent pivoted within seconds to `jq + install` to achieve the same filesystem write via a command that was not in the guard's blocked patterns. The permission classifier caught it. Without the classifier, it would have succeeded. If it had succeeded, it would have raced the gateway's own concurrent writes to `openclaw.json` and overwritten state.

The pattern: agent assumes unknown filesystem is runtime state rather than tracked code. Guard fires. Agent reframes the block as a puzzle and routes around. The slow path (worktree -> PR -> merge -> pull) would have forced the agent to surface the race-condition risk; the shortcut skipped the thinking.

This plan closes both failure modes via two coordinated guard extensions. They strengthen the existing guard contract; neither weakens it.

## Behavioural framing

The current guard treats a block as a signal: the agent reads the error, the agent decides what to do next. That framing leaves room for the "find another path" instinct. Today showed the instinct wins.

This plan adopts a stronger framing from GPT's feedback (2026-04-19): **a guard block is a state transition, not a signal.** On block, the agent moves from execution mode to review mode. In review mode the legal next actions are constrained: explain what was attempted, explain why the guard likely fired, inspect documentation, propose an approved path, or ask Parker. "Find an equivalent command" is not on the list.

The principle that unifies this plan's two changes and the existing `feedback_never_bypass_guards.md` memory:

> **If an intended state change is blocked, any alternative command or utility that produces the same state change counts as the same blocked action.**

Call this the anti-substitution rule. The first change (onboarding) enforces it implicitly by raising the floor of understanding before writes. The second change (blocked-file tracking) enforces it explicitly by detecting the substitution pattern at the hook level.

A deeper implication worth naming: **lack of permission often implies lack of understanding.** The response to a block is "what system fact am I missing?" The fact today was "this config file has a concurrent writer." The slow path would have surfaced that. The shortcut skipped it.

## The two changes

### 1. Onboarding-before-first-write

**Behaviour:** On the first `Write` / `Edit` / file-modifying `Bash` that targets a file inside a git repo the session has not already written to, the guard checks whether a per-session "onboarded" flag is set for that repo. If not set, the guard denies with a short, actionable list: "read these before first write: [README.md, CLAUDE.md, any *RUNBOOK*.md / *LANDMINES*.md files at repo root or one level down, then retry]."

On retry after the agent has read (via `Read` tool) the listed files, the flag flips and writes proceed normally.

**Why:** Converts "I didn't know this was a tracked repo" from a runtime discovery (via guard block) into a mechanical pre-write ritual. The agent cannot skip the onboarding by accident; the guard enforces it. Human ergonomics (shell aliases on `cd`) don't reach agents; hook-level enforcement does.

**Notes:**
- "Repo the session has not already written to" is the onboarding scope. Reads are free; writes trigger onboarding.
- The list of required reads is generated dynamically by `ls` + glob at the repo root and one level down. Files matched: `README.md`, `CLAUDE.md`, any file matching `*RUNBOOK*.md`, `*LANDMINES*.md`, `WORKFLOW*.md` (case-insensitive).
- An explicit override path: `OC_GUARD_SKIP_ONBOARDING=<repo-path>` environment variable. Parker sets this in-session when he has a specific reason to skip.
- Tracking state: a per-session JSON file at `~/.ldm/state/guard-session-<session-id>.json` (or similar). Session ID comes from the hook input. File records `onboarded_repos: [<repo-toplevel>, ...]` and decays with the session.

### 2. Recently-blocked-file tracking

**Behaviour:** When the guard denies any write to file F via tool A, it appends `{path: F, tool: A, command: <stripped>, ts: <iso>}` to the session state file. On any subsequent file-writing `Bash`/`Write`/`Edit` targeting F within the session, the guard checks the log. If F was denied in the last N entries (default 5) via any tool, the new attempt is denied with: "this file was blocked X turns ago (`<tool>` on `<ts>`). If you're routing around the previous block, stop and tell Parker. If this is legitimate and unrelated, set `OC_GUARD_ACK_BLOCKED_FILE=<path>` to proceed."

**Why:** Closes the exact loop from today. Blocked on Edit -> pivot to `jq + install` = immediate re-block. The same-effect tool swap anti-pattern is named in the existing `feedback_never_bypass_guards.md` memory; this makes the naming mechanical.

**Notes:**
- The log is session-scoped and bounded (oldest entries drop past ~100 entries).
- The override `OC_GUARD_ACK_BLOCKED_FILE=<path>` is per-invocation, not persistent. Agent must re-assert intent each time, forcing friction commensurate with the safety override.
- Each denial on this path also writes to a separate `bypass-audit.jsonl` under `~/.ldm/state/` for later review. Parker (or a post-mortem) can read the audit to see every time the pattern triggered, independent of what the agent said in conversation.

### 3. Contested-file detector (optional, adjacent)

**Behaviour:** A new tag in guard config or inline in the protected repo: `contested: [<path glob>, ...]`. Files matching these globs have known concurrent writers (gateway, LaunchAgents, cron jobs). The guard denies direct `Write`/`Edit` on these paths outright, even inside a worktree, and points to the documented mutation path (usually: open a PR on the tracked repo that deploys the file, not the deployed file directly).

**Why:** This is today's openclaw.json problem at root. The gateway writes to that file continuously (auth-state, plugin manifests, config warnings). Agents editing it directly race those writes. Even if the agent is in a worktree, a direct edit to the deployed path fails to respect the ownership model.

**Candidates to tag contested on day one:**
- `~/.openclaw/openclaw.json`
- `~/.openclaw/agents/*/agent/auth-state.json`
- `~/.openclaw/memory/*.json`, `~/.openclaw/memory/*.jsonl`
- Any file listed under "gateway-owned" or "runtime-owned" in `KNOWN-LANDMINES.md`.

**Why optional for this plan:** Requires a decision about where the list lives (guard config, per-repo config, or scraped from `KNOWN-LANDMINES.md`). If Parker wants, this becomes its own follow-up plan. I flag it here because GPT's feedback named the pattern and it would have prevented today's openclaw.json race.

## Incorporates external feedback

Three independent external sources converged on the same conclusion as the post-mortem: **the mechanical cold-start onboarding step is a higher-leverage fix than any amount of CLAUDE.md polish.** Grok, GPT, and a public X user Parker surfaced 2026-04-19 all independently pointed at "scan git, read the runbook, then touch files" as the primary lever. That convergence is the justification for change 1 being the first thing shipped, not a follow-up.

Parker shared feedback from Grok and GPT on 2026-04-19. Relevant items folded in:

**From Grok:**
1. **Bypass audit log.** The `bypass-audit.jsonl` in change 2 is this. A paper trail the agent sees growing instead of forgetting between turns.
2. **Context-specific risk in error messages.** Folded into both denials. Richer than the current generic `WORKFLOW_ON_MAIN` string.
3. **`INVARIANTS.md` per protected repo.** Candidate for a separate future plan.

**From GPT (more conceptual, shaped the Behavioural framing section above):**
1. **Block-as-state-transition.** Drives the framing section's "execution mode → review mode" language.
2. **Anti-substitution rule.** Named explicitly in the framing; enforced mechanically by change 2.
3. **Contested-file detector.** Became change 3 (optional), directly targeting today's openclaw.json race problem.
4. **Lack-of-permission-implies-lack-of-understanding.** Named in the framing section. Changes the response to a block from "how else" to "what am I missing."

**Not in this plan (worth noting as deferred):**
- Grok's shell-alias-on-`cd` idea (doesn't reach agents; shell aliases help humans).
- Grok's "start prompts with 'follow CLAUDE.md strictly'" (CLAUDE.md already loads via hooks).
- GPT's "turn this into a tight CLAUDE.md section with hooks-style wording" ... that is a separate, small follow-up plan (update the repo CLAUDE.md files with the six constitutional rules GPT proposed: Classify before mutating; A block changes mode; No equivalent-action bypasses; Prefer reviewable change paths; Assume contested ownership until proven otherwise; Narrate risk honestly). Candidate filename: `2026-04-XX--cc-mini--claude-md-operating-rules.md`.

## Implementation outline

**Files to touch:**
- `tools/wip-branch-guard/guard.mjs`: add the two behaviours. Both attach to existing repo-resolution and write-detection logic. The onboarding check runs after repo is resolved and before the `isBlockedCompoundCommand` check. The blocked-file tracking runs at the point of every `deny(...)` call.
- `tools/wip-branch-guard/test.sh`: cases for both. Onboarding: first write → deny with read list; Read of required files → retry write → allow. Blocked-file: Edit blocked → `install` attempt on same file → deny with prior-block message.
- Session state helpers: `readGuardSessionState(sessionId)` and `appendGuardSessionEvent(sessionId, event)` in a small shared module.
- `~/.ldm/state/` directory creation (should already exist; verify).

**Size estimate:** ~150 lines of guard code + ~100 lines of tests. One PR on `wip-ai-devops-toolbox-private`. Contained change; does not touch any other guard behaviour.

**Version bump:** guard sub-tool `1.9.75 -> 1.9.76`. Alpha release via the normal pipeline (`wip-release alpha`). Dogfood for at least 48 hours before promoting to stable.

## Test plan

1. Install the updated guard. Start a fresh session.
2. In the fresh session, immediately run `Edit` on a file inside a new repo the session hasn't touched: onboarding denial with read list.
3. Run `Read` on the listed files.
4. Retry the `Edit`: succeeds (if the rest of the guard checks pass).
5. In the same or a different session, trigger a main-branch write block on file F via `Edit`. Attempt `install` or `cat > F` or similar on F. Second denial with prior-block message.
6. Set `OC_GUARD_ACK_BLOCKED_FILE=F` and retry: proceed.
7. Check `~/.ldm/state/bypass-audit.jsonl` has one entry per denial.
8. Regression: existing 33 guard tests all still pass.

## Decisions confirmed by Parker 2026-04-19

- **Session ID source.** Use Claude Code's `PreToolUse` payload `session_id` field. Implementation probes it once at guard bootstrap and falls back to a guard-generated ID + warning if the field is absent.
- **Override scope.** Per-session. Overrides decay when the session ends. No global / persistent overrides; those created silent-drift risk in earlier designs. A future Kaleidoscope biometric approval flow replaces the env-var mechanism entirely (see "Approval mechanism" below).
- **Onboarding read-list scope.** Root + one level deep. Configurable later if repos with deeper relevant docs appear, but this is the default.
- **Onboarding flag persistence.** Reset on (a) new session-id detection OR (b) more than 2 hours since the last guard invocation for that repo in the current session. Implementation stores `{repo_path, onboarded_at_ts, last_touch_ts}`; on every tool call, compute `now - last_touch_ts`, clear the flag if it exceeds 2h. New-session detection clears everything. ~5 lines of extra logic in the session-state helper.

## Approval mechanism: pluggable backend

The override mechanism referenced above (OC_GUARD_ACK_BLOCKED_FILE, OC_GUARD_SKIP_ONBOARDING, and the external-PR guard's approval gate covered in a sibling plan) should be implemented through a single interface with swappable backends, not hard-coded to env vars.

```
approvalBackend.request(action, context) -> { approved: bool, reason: string, via: "env" | "bridge" | "kaleidoscope-biometric" }
```

Backends (shipped incrementally):

1. **`env` (ship day one).** Checks the relevant env var. Simplest. Works today. Per-invocation or per-session depending on the caller.
2. **`bridge` (ship when the bridge backend stabilises).** Agent sends Parker an approval request via `lesa_send_message` or a dedicated approval channel, blocks on a response token. Async. Parker acknowledges inline.
3. **`kaleidoscope-biometric` (long-term, ties into the product we are building).** The approval request surfaces in Kaleidoscope; Parker uses his passkey / WebAuthn / biometric to grant the specific scope for a bounded window. The token the agent receives is cryptographic, not a plain env string. This is the actual destination for "proper" in-session overrides once Kaleidoscope's agent-auth flow is wired.

Why this matters for today's work: the `env` backend is enough to ship onboarding + blocked-file tracking. But if the env var pattern leaks into CLAUDE.md, into docs, into agent muscle memory, the eventual migration to the biometric backend becomes a rewrite instead of a swap. Pinning the indirection now costs ~30 lines of extra code and zero agent-facing complexity.

Parker's direction on this plan 2026-04-19: ship B (env-based hook now), architect so D (bridge approval) and the Kaleidoscope biometric backend are drop-in replacements later.

## Not in scope for this plan

- `INVARIANTS.md` convention per repo. Separate plan if Parker wants.
- Surfacing the onboarding prompt to the agent more visually (e.g., at SessionStart rather than at first write). The current SessionStart hook already fires on main detection; adding per-repo runbook reminders would belong there.
- Extending the guard to also read the contents of CLAUDE.md etc at onboarding time and inject them into the agent's context. That's a bigger behavioural change and should be its own plan.

## Why this takes Parker out of the middle

Layers, as described in the 2026-04-19 post-mortem discussion:
- Layer 1 (memory rules): reduces rate of bypass and unfamiliar-repo assumptions. Demonstrated today: not sufficient.
- Layer 2 (permission classifier): catches specific bypass patterns after the fact. Demonstrated today: caught one of two.
- Layer 3 (this plan): enforces onboarding and blocks same-file tool swaps at hook level. Independent of agent discipline. This is the layer that stops Parker from being safety-of-last-resort on every new repo.

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).

## Resolution

Status: Closed on 2026-04-24.

Closed by `wip-ai-devops-toolbox-private` PR #386. Automatic Read/Glob onboarding tracking remains, and agents now also have an explicit recovery path: `wip-branch-guard onboard <repo>`. Recently-blocked-file retry tracking remains active so swapping tools after a denial does not bypass the original block.

Verification:

- First-write onboarding tests cover explicit onboard.
- Same-file retry detection remains in guard regression coverage.
- `bash tools/wip-branch-guard/test.sh`: 117 passed, 0 failed, 1 skipped.
