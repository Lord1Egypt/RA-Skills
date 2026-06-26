# wip-branch-guard v1.9.84

## Proactive onboarding advisory + bypass audit escalation

Closes #255.

Closes out the last two follow-ups from the v1.9.82 ticket (`2026-04-21--parker-cc-mini--bugfix.md`): Gap A and Gap C. Together with v1.9.82 (cross-session state fix + Layer 3 temp-dir filter + env-var hatch removal) and v1.9.83 (shell-redirect bypass block + state sanity check), the v1.9.82 ticket is fully closed.

## Gap A: proactive SessionStart onboarding advisory

### The bug

The onboarding gate is reactive. It fires on the first Write/Edit/Bash-write attempt in a session-new repo, not on session start or first `cd`. When an agent hasn't done the onboarding Reads before its first write, it hits the deny, which then triggers the retry-after-block pattern on subsequent attempts. That pattern is what Claude Code's auto-mode decider false-positives on (tracked upstream as anthropics/claude-code#51676).

Prevention is the only fix that doesn't require Anthropic to ship a remediation-aware decider: surface the required onboarding reads at SessionStart so the agent does them up-front in a single parallel-Read turn, before any write.

### The fix

New `checkProactiveOnboardingAdvisory(cwd)` helper, called from `handleSessionStart`. If cwd is a git repo and the repo root has `README.md`, `CLAUDE.md`, or any `*RUNBOOK*.md` / `*LANDMINES*.md` / `WORKFLOW*.md`, the guard emits a boot-context advisory listing each required Read path. Non-blocking; purely informational.

Example output (injected into boot context):

```
📖 ONBOARDING ADVISORY: /path/to/repo has onboarding docs. Before your first Write/Edit/Bash-write in this session, Read these in parallel (one turn):

  Read /path/to/repo/README.md
  Read /path/to/repo/CLAUDE.md

The guard enforces onboarding on first write; reading up-front avoids retry-after-block cycles that Claude Code's auto-mode decider false-positives on.
```

## Gap C: bypass audit escalation at SessionStart

### The bug

`~/.ldm/state/bypass-audit.jsonl` records every guard denial and every env-var override. Pre-v1.9.82, `LDM_GUARD_SKIP_ONBOARDING` and `LDM_GUARD_ACK_BLOCKED_FILE` writes appeared here frequently. The log existed; nothing parsed it. Repeat bypasses accumulated silently.

### The fix

New `checkBypassAuditEscalation()` helper, called from `handleSessionStart`. Reads the last 500 lines of the audit log, filters to the last 24 hours, and emits a boot-context warning if:

- Any path was denied 3+ times in the window (`🚨 BYPASS AUDIT`), OR
- Any env-var override fired at all (`⚠️ ENV-VAR OVERRIDES`). Post-v1.9.82, only `LDM_GUARD_UPSTREAM_PR_APPROVED` is legitimate; any other override appearing here means the deployed guard is stale (pre-v1.9.82) and `ldm install` is needed.

The warning is non-blocking; it surfaces the pattern so Parker can triage without reading the audit log manually.

## What's in the diff

- `tools/wip-branch-guard/guard.mjs`
  - New: `checkProactiveOnboardingAdvisory(cwd)` helper (Gap A)
  - New: `checkBypassAuditEscalation()` helper (Gap C)
  - Changed: `handleSessionStart` now collects warnings from four sources (state sanity, bypass audit, onboarding advisory, on-main warning) and emits them joined into a single `additionalContext` response
- `tools/wip-branch-guard/package.json`
  - Version bump 1.9.83 → 1.9.84

## Tradeoff accepted

The onboarding advisory fires on EVERY SessionStart in a git repo with onboarding docs. That's slightly noisy for experienced sessions in familiar repos. The alternative (gate on "not yet onboarded" via state lookup) requires state to exist at SessionStart, which it typically doesn't (per-session state file is created on first PreToolUse). Preferred noisy-but-useful over silent-but-inert.

## The v1.9.82 ticket is now closed

| Item | Shipped in |
|---|---|
| Cross-session state collision fix | v1.9.82 |
| Env-var escape hatches removed | v1.9.82 |
| Layer 3 temp-dir false-positive filter | v1.9.82 |
| Gap B: shell-redirect bypass block | v1.9.83 |
| SessionStart state sanity check | v1.9.83 |
| Gap A: proactive SessionStart onboarding advisory | v1.9.84 |
| Gap C: bypass audit escalation | v1.9.84 |

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).
