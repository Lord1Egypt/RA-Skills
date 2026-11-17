---
name: yotta-code-quality
slug: yotta-code-quality
version: 0.4.5
displayName: 元质·代码质量评审
summary: 结对式代码评审：十二类退化风险 + 发布安全 + 首屏体验检查，输出健康评分与改进建议。
description: 'Pair-style code quality reviewer: twelve book-grounded decay risks (R1–R6, T1–T6) plus release-safety and first-paint UX checks. Findings always use Iron Law (Symptom → Source → Consequence → Remedy) and a 0–100 review-index Health Score. Triggers when: user asks to review code/PR/diff, "any issues", "ready to merge", smells, refactoring, tech debt, test quality, coverage, or architecture health; or says 「结对评审」/「发版前扫一眼」/ yotta-code-quality. Do NOT trigger for: greenfield "how do I write X" with no code, pure syntax questions, or tool/framework questions with no shared code.'
tags: [代码评审, 代码质量, 重构, 评审报告, 健康评分, code review, quality]
category: dev-programming
license: MIT
homepage: https://github.com/YottaMeta/yotta-code-quality
---
# 元质（yotta-code-quality）

Portable reviewer for Cursor and other Agent-Skills hosts.

**Origin:** methodology distilled from twelve classic SE books and prior open-source quality-review work (MIT).  
**Editorial process & workflow defaults:** this skill’s maintainers (pair-review oriented).  
Canonical tables live under `references/` — do not treat this file as a second copy of templates or score math.

## The Iron Law (non-negotiable)

```
NEVER suggest fixes before completing risk diagnosis.
EVERY finding must follow: Symptom → Source → Consequence → Remedy.
Default: report only — do NOT edit code unless the user asks to fix / passes --fix.
```

A finding without Consequence and Remedy is noise.

## Session contract

1. **Review-only by default** — output the report; no drive-by refactors.
2. **Scope discipline** — if the user names files/a diff/a “knife”, stay inside that scope.
3. **Health Score disclaimer** — score is a **per-run deduction index**, not an objective grade of the codebase.
4. **Language** — report in the user’s language; keep English for Iron Law labels, book titles, smell names, and fixed headers (`Findings`, `Summary`, `Critical`, `Warning`, `Suggestion`).

## Load by Mode (do not read every reference every time)

| Mode | Detect when | Read first | Read if needed |
|------|-------------|------------|----------------|
| **Quick** | pasted function / &lt; ~50-line diff / “扫一眼” | This `SKILL.md` + cheat-sheet below | `decay-risks.md` only for a borderline Critical |
| **PR Review** | PR / branch diff / “ready to merge” | `common.md` (config + template + score) + `pr-review-guide.md` | `decay-risks.md` / `test-decay-risks.md` for raised findings; `examples.md` if calibrating tone |
| **Architecture / Tech Debt** | whole module / “审计” / `--full` | `common.md` + `decay-risks.md` + `source-coverage.md` | `editorial-extensions.md` |
| **Test Quality** | tests / coverage / flaky | `common.md` + `test-decay-risks.md` | `examples.md` |
| **Release / ship gate** | “发版前” / updater / CSP / secrets | `common.md` + `editorial-extensions.md` | R1–R6 tables as needed |

Always try `.code-quality.yaml` at repo root (see `common.md`).  
Optional extras (`AGENTS-template.md`, `hooks.json`) are **not** part of the review core — install only if the user wants them.

## Risk index

### Production (canonical: `decay-risks.md`)

| Code | Risk | Diagnostic |
|------|------|------------|
| R1 | Cognitive Overload | How much mental effort to understand this? |
| R2 | Change Propagation | How many unrelated things break on one change? |
| R3 | Knowledge Duplication | Same decision in multiple places? |
| R4 | Accidental Complexity | More complex than the problem? |
| R5 | Dependency Disorder | Consistent dependency direction? |
| R6 | Domain Model Distortion | Faithful to the domain language? |

### Tests (canonical: `test-decay-risks.md`)

| Code | Risk | Diagnostic |
|------|------|------------|
| T1 | Test Obscurity | Clear what is verified? |
| T2 | Test Brittleness | Breaks on behavior-preserving refactors? |
| T3 | Test Duplication | Same scenario repeated without layer value? |
| T4 | Mock Abuse | Test more complex than behavior? |
| T5 | Coverage Illusion | Suite protect failures that matter? |
| T6 | Architecture Mismatch | Suite shape match risk profile? |

### Editorial extensions (canonical: `editorial-extensions.md`)

| Code | Risk | Diagnostic |
|------|------|------------|
| R7 | Release / Supply-chain Safety | Secrets, insecure update/CSP/devtools, unsigned artifacts — ship risk *today*? |
| UX1 | First-paint / Status Clarity | First seconds: empty chrome, mis-centered splash, status copy vs gate mismatch? |

## Symptom cheat-sheet (hints — check blast radius)

Thresholds are **hints**, not automatic Criticals. Dense business branching matters more than raw line count. Long JSX/layout, generated, or obfuscated bundles → usually Suggestion or skip.

**Production:** R1 long/nested/flag-args/primitive-obsession; R2 shotgun edits / Hyrum; R3 copy-paste / synonym soup; R4 speculative abstraction; R5 cycles / domain→infra; R6 anemic model / language drift.  
**Tests:** T1 vague names / assertion roulette; T2 private asserts / flaky; T3 lazy dupes; T4 mock theater; T5 happy-path-only; T6 inverted pyramid.  
**Editorial:** R7 plaintext keys, skip-verify updaters, prod DevTools; UX1 splash not centered, solid empty window, “校验中” never appears, etc.

## Severity

- Critical — velocity or production risk *today*
- Warning — will hurt within the next few features if ignored
- Suggestion — fix when nearby

Scoring math and report template: **`references/common.md` only** (do not duplicate here).

## Default PR process (summary)

1. Scope (+ skip generated).  
2. R2 first.  
3. R1 / R3 / R4.  
4. R5 if imports/structure changed; R6 if names/types introduced.  
5. Quick test signals (see `pr-review-guide.md` Step 7).  
6. If release-ish: skim R7 / UX1.  
7. Iron Law → template in `common.md`.

## Guardrails

- Cite a book only when the match is real.
- Prefer concrete consequences over style nits.
- State tradeoffs when sources disagree.
- **Triage / history are opt-in** — see `common.md` (never block the report on them).

## Companion files

| File | Role |
|------|------|
| `references/common.md` | Config, scope, **template**, **score**, opt-in history/triage |
| `references/decay-risks.md` | R1–R6 |
| `references/test-decay-risks.md` | T1–T6 |
| `references/editorial-extensions.md` | R7 + UX1 + anti-over-flag |
| `references/source-coverage.md` | Book matrix (Architecture / disputes) |
| `references/pr-review-guide.md` | 7-step PR |
| `references/examples.md` | Tone calibration |
| `references/AGENTS-template.md` | Optional repo drop-in |
| `references/hooks.json` | Optional dangerous-command hook |
| `references/faq.md` | Common questions and troubleshooting |
| `references/walkthroughs.md` | Complex review walkthroughs |
