# skill-deep-audit

> Generic, multi-dimension quality audit for agent skills — with explicit
> ERR / WARN severity, 115-point scoring, and an opt-in `--fix` workflow.

`skill-deep-audit` is a **read-only**, deterministic skill auditor. Point
it at any skill folder and it will run 7 dimensions of static (or static +
read-only dryRun) checks, then produce a scorecard MD with citations,
ERR / WARN findings, and a fix plan split into "auto-fixable" vs "needs
human confirmation".

## What you get

| Mode | What runs | Max | Time |
|------|-----------|-----|------|
| **L1 static** | File read, structural check, keyword scan, syntax check (D1–D7 minus items that need external systems) | **112** | ~2 min |
| **L2 dryRun** ⭐ | L1 + Hub existence check + dependency existence check + read-only branch reachability simulation | **115** | ~5 min |

Both depths share the same pass line: **≥ 90 points AND zero ERR**.

## The 7 dimensions

| Dim | Name | Core question |
|-----|------|---------------|
| **D1** | Process closure & idempotency | Will the run produce the right result, and is the second run safe? |
| **D2** | Tool & command conventions | Are command calls safe and auditable? |
| **D3** | Portability & defense | Can it run on someone else's machine? |
| **D4** | Skill usability conventions | Can a new user actually pick it up and use it? |
| **D5** | Security & op risk | Is it safe after the run? Are high-risk ops protected? |
| **D6** | Code & doc quality | Is the code correct? Does the doc match the code? |
| **D7** | Dependency & footprint health | Is the overall architecture healthy and maintainable? |

## Quick start

The skill is invoked by an LLM agent (Claude Code, Cursor, OpenClaw, etc.).
Once installed, just ask:

```
"audit my-skill"
"check skill quality of ./skills/my-skill"
"is this skill ready to ship?"
"lint this skill"
"do a skill-deep-audit on my-skill"
```

The agent will:

1. Ask which depth you want (L1 / L2 dryRun) and wait for your reply.
2. Locate the skill directory and read everything in scope.
3. Run the per-dimension static scan defined in
   [`references/check-rules.md`](references/check-rules.md).
4. (L2 only) Run Hub existence + dependency existence + branch reachability
   simulation — all read-only.
5. Produce a scorecard at `{skill-path}/AUDIT-{YYYY-MM-DD}.md`.
6. Print a summary with the highest-priority ERR and the estimated
   post-fix score.
7. Offer to fix — but **never auto-fixes** without your explicit "fix"
   reply, and always backs up the skill folder first.

## Severity rules

| Tag | Meaning |
|-----|---------|
| ❌ **ERR** | Functional impact / security risk / silent data error / a hard red line. **Must fix.** |
| ⚠️ **WARN** | Maintainability, conformance, defensive gap. **Should fix.** |
| ℹ️ **INFO** | Style preference, minor optimization (used sparingly). **Optional.** |

**Escalation rule that matters most**: any single ERR makes the final
result **FAIL**, no matter how high the total score is. The dual-judgement
is built into the pass criterion: `total ≥ 90 AND zero ERR`.

## Scoring

```
Total          : 115 pts
  D1 Process closure & idempotency   :  13
  D2 Tool & command conventions      :  10
  D3 Portability & defense           :  15
  D4 Skill usability conventions     :  21
  D5 Security & op risk              :  21
  D6 Code & doc quality              :  31
  D7 Dependency & footprint health   :   4

Pass line      : ≥ 90  AND  zero ERR   (both must hold)
L1 max         : 112  (skips Hub + dryRun-only items)
L2 max         : 115
```

ERR is uniformly 3 points (the value is symbolic — a single ERR means
FAIL). WARN uses 3 priority tiers (3 / 2 / 1) to guide fix order.

## Red lines

- **Read-only by default.** The audit never executes a write operation of
  the audited skill and never modifies its files.
- **`--fix` is the only exception.** It requires explicit user
  authorization, always backs up the skill folder first, and never touches
  business-logic items (5.2) without per-item confirmation.
- **Determinism.** Each rule's hit/miss decision uses the grep pattern,
  keyword list, and numeric thresholds defined for it — not the agent's
  subjective judgement. Edge cases without explicit coverage are marked
  "manual verification needed", not hard-judged.

## Why this, not a free-form review

| Without skill-deep-audit | With skill-deep-audit |
|---------------------------|-------------------------|
| Agent reviews one thing at a time, may miss a dimension | Agent runs 7 dimensions deterministically |
| Findings often vague ("looks off here") | Every finding must cite `file:line` and follow the 4-element ERR/WARN structure (problem / example / fix / blast radius) |
| No severity discipline | Explicit ERR / WARN + the "any ERR = FAIL" red line |
| Hard to repeat reliably across agents | grep patterns + thresholds + False-Positive General Rules keep results stable across re-runs |
| Risk of fix-breaks-more | `--fix` separates auto-safe (5.1) from business-logic (5.2), and always backs up first |

## Part of build-better-skills

This skill is part of the
[build-better-skills](https://github.com/Songhonglei/build-better-skills)
suite — open-source skills that help you build better skills, end-to-end:

| Stage | Skill | Status |
|-------|-------|--------|
| Creation | `skill-creator` | 🚧 Not yet released |
| **Audit** | **`glic-check`** | ✅ **v1.0.x** |
| **Audit** | **`skill-deep-audit`** | ✅ **v1.0.0** |
| Testing | `skill-regression` | 🚧 Not yet released |
| Sediment | `skill-sediment` | 🚧 Not yet released |

Two complementary tools share the **Audit** stage:

- **`glic-check`** — lightweight & qualitative; run right after any edit for a
  fast multi-dimension sanity review (no score).
- **`skill-deep-audit`** (this tool) — heavyweight & quantitative; a full
  dryRun-level exam that grades the skill on a 115-point scale. Best as the
  pre-ship final check.

Only `glic-check` and `skill-deep-audit` are installable today. The other
entries are roadmap placeholders — they will appear in the suite repo as
they are open-sourced.

## Files

```
skill-deep-audit/
├── SKILL.md                       ← agent entry point + workflow (Steps 0–8)
├── README.md                      ← this file
├── LICENSE                        ← MIT
├── .gitignore
└── references/
    ├── check-rules.md             ← full rule decisions + grep patterns + thresholds
    ├── output-template.md         ← scorecard MD template (4-element ERR/WARN structure)
    └── controlled-domains.md      ← optional D2-E1 controlled-domain config (default empty)
```

## Changelog

### v1.0.0 (2026-06-21)

- Initial open-source release.
- 7-dimension framework (D1–D7), 115-point scoring, pass line 90 + zero ERR.
- L1 static (~2 min) + L2 dryRun (~5 min) depth modes.
- Explicit ERR / WARN severity with deterministic grep patterns and
  thresholds; "False-Positive General Rules" to stabilize edge cases.
- Opt-in `--fix` workflow split into auto-fixable (5.1) and human-confirm
  (5.2) tiers, always backs up the skill folder first, never auto-re-audits.
- Scorecard template with the 4-element ERR/WARN structure (problem /
  example / fix / blast radius), full checklist table, and dependency
  section.

## License

MIT — see [LICENSE](./LICENSE).

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
