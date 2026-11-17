---
name: skill-md-optimizer
slug: skill-md-optimizer
displayName: "SKILL.md 渐进式披露优化器"
version: 1.0.0
summary: >-
  Refactor or optimize any SKILL.md for progressive disclosure: precise-trigger
  frontmatter, layered body, a single-turn closed flow, permission/context
  declarations, and a length budget. Emits a full optimized file plus a changelog.
  Read-only mode diagnoses without touching the original.
description: >-
  Refactor/optimize any SKILL.md for progressive disclosure: precise-trigger
  frontmatter, layered body (hard constraints vs single-run flow), a flow of five
  steps or fewer, permission/context declarations, and a token budget.
  Triggers: "optimize / refactor / slim down this SKILL.md", "make the skill
  trigger more precisely", "the body is too long / hard constraints get lost when
  the context compacts", "split this SKILL.md into a lean body plus references".
  Three modes: refactor (default, emits the optimized file + a changelog), audit
  (read-only diagnostic), and readme (polish the companion README.md - structure,
  badges, install, usage examples, license).
  NOT for: auditing the code a skill calls (skill-clean-audit), a publish-time
  security/compliance gate (skill-publish-gate), or from-scratch creation
  (skill-creator). No external network and no required secrets; the linter runs
  offline.
when_to_use: >-
  (1) The user names "optimize / refactor / slim down SKILL.md" and gives a target
  skill; (2) wording like "this skill mis-triggers", "the body is too long", "the
  hard constraints vanish after context compaction", "I want to split references";
  (3) a request to fit a long SKILL.md under an 8000-token budget with the core rules
  placed up front; (4) the user asks to "optimise / polish this README.md" or "my
  README is too long / missing install steps / no usage examples". Does not fire for:
  code-quality audits (skill-clean-audit), publish gates (skill-publish-gate),
  from-scratch creation (skill-creator), or a pure YAML syntax error (fix the syntax
  directly).
trigger_keywords:
  - SKILL.md 优化
  - 渐进式披露
  - frontmatter 精修
  - 触发词精化
  - skill 瘦身
tags:
  - skill
  - skill-md
  - frontmatter
  - progressive-disclosure
  - refactor
  - audit
  - readme
  - skill-optimization
network: none
disclaimer: >-
  本 skill 仅做 SKILL.md 文本与结构优化，不执行外部网络请求，不读取环境变量或
  凭据；linter（scripts/check_skillmd.py）为纯离线运行，零网络、零必需密钥。
  结论是本地预检，不构成任何平台上架保证；最终能否发布由各平台审核决定。
reference: https://github.com/your-org/skill-md-optimizer
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
      config: []
    homepage: https://github.com/your-org/skill-md-optimizer
---

# SKILL.md Progressive-Disclosure Optimizer

> **Hybrid skill: methodology + deterministic linter.** `scripts/check_skillmd.py`
> gives reproducible red/amber/green calls on the *mechanical* checks; this file
> gives the criteria and a five-step flow for the *judgment* layer. The read-only
> mode (audit) never modifies the original.
>
> Natural-language note: every instruction below is plain guidance for the agent.
> No command, tool, or external call is required to follow them.

---

## Hard constraints (obey every turn; re-applied after any context compaction)

If the context has been compacted, this section must be preserved and re-applied.
Violating any item is an execution failure — "the user did not emphasize it" is not
an excuse.

| # | Constraint | Rationale |
|---|---|---|
| **H1** | **Never silently drop rules.** Refactoring only moves content (down into `references/`) and adds a pointer; it does not delete any substantive rule. Deletion requires the user's explicit confirmation. | Same contract as a read-only audit |
| **H2** | **Never overwrite.** Back up the original before writing back (a `<name>.bak` or git commit); if the target name already exists, choose a different one. | Reversibility |
| **H3** | **Every change is traceable.** Record each change in the changelog table: old -> new + reason + "assumed?" + "P0?". Any change that assumes a default must be explicitly marked "assumed". | Trust |
| **H4** | **No network, no secrets.** Do not make requests, read keys, or call external APIs. | Compliance red line |
| **H5** | **Never guess the target.** If no SKILL.md is named, ask first; if it cannot be read, give a three-step self-check (spelling / relative path / list the directory) and do **not** fall back to auditing a different file. | Reliability |
| **H6** | **Mechanical checks go to the script.** Frontmatter syntax, name rules, character/line budgets, and dangling references are decided by `scripts/check_skillmd.py`, never by impression. | Cross-agent reproducibility |
| **H7** | **Stay in lane.** Optimize SKILL.md text and structure only; do not audit the code the skill calls (skill-clean-audit) or run a publish gate (skill-publish-gate). | Division of labor |
| **H8** | **Declarations must match behavior.** If anything new reads env / calls a binary / uses the network, declare it; default is zero-network. | Consistency |
| **H9** | **Do not guess the output language.** Follow explicit `zh`/`en` > inferred interaction language > ask; do not switch mid-run. | Consistency |

---

## Language picker (Natural-Language Policy: offer a choice) — keep in first ~3000 tokens

This skill serves multilingual users; artifact language is decided by three states,
fixed for the whole run (no mid-run switch):

- **auto (default):** follow the language you use with the agent — English in → English
  out; Chinese in → Chinese out; mixed → your dominant language; pure code/paths with
  no natural language → ask "Chinese or English report?"
- **zh:** force Chinese; every artifact Chinese, ignoring the exchange language.
- **en:** force English; every artifact English, ignoring the exchange language.

Priority: your explicit `zh`/`en` > inferred `auto` > ask as a fallback. No locale is
hard-set, so this is not a single-language lock; if you must pin a locale, state the
reason and an exit here. Full policy detail and the layering rules live in
`references/i18n_policy.md`.

---

## Criteria core (read first; keep within the first ~3000 tokens)

**Root premise:** SKILL.md is shared context with the host agent. Every line must
earn its token cost.
**Key reversal:** stuffing variant details, platform matrices, and changelog
templates into the body *raises* per-run cost. Sink what is not used every turn into
`references/`; keep only per-turn essentials plus navigation pointers in the body.

Four criteria:

- **T. Trigger precision** — frontmatter (name / description / when-to-use) matches
  how users actually ask, including trigger words, boundaries, and explicit
  "not-for" cases.
- **L. Layering** — persistent hard constraints are separated from the single-run
  flow; hard constraints are explicitly marked "every turn" so they survive
  compaction.
- **C. Convergence** — the single-run flow is five steps or fewer; each step states
  its input / output / failure fallback; it closes within one turn with no later re-read.
- **B. Budget** — the whole file fits a 3500-token budget (the official 500-line
  body cap), the core rules sit in the first ~1500–2000, and the remaining slack
  is reserved as compaction headroom.

---

## Five-step flow (single-turn closed loop; no cross-turn re-read)

Each step states input / action / output / fallback.

### Step 1 - Resolve target and mode
- **Input:** the user query (may include a SKILL.md path, a directory, a target platform).
- **Action:** If no target is named, ask first (H5). Pick the mode: `refactor`
  (default, optimizes a SKILL.md), `audit` (read-only diagnostic), or `readme`
  (polish the companion README.md — see `references/readme_quality.md`). Pick the
  platform profile (ClawHub / SkillHub / Claude-WorkBuddy; default to the host
  profile).
- **Output:** a confirmed target file + mode + platform profile.
- **Fallback:** file missing / unreadable -> three-step self-check, do not fall back
  to a different file.

### Step 2 - Read the original and run the linter
- **Input:** the target from Step 1.
- **Action:** Read the full SKILL.md (frontmatter and body). Run
  `scripts/check_skillmd.py <file> [--platform p] [--token-budget 3500]` to get the
  red/amber/green calls and the budget read.
- **Output:** line-numbered original + linter verdict (mechanical items already called).
- **Fallback:** items the linter cannot call (for example, "should this be split into
  references") are marked "needs human review", not asserted. A missing PyYAML is
  auto-installed; if it cannot, it is reported as a blocker, never passed silently.

### Step 3 - Check the criteria and plan the changes
- **Input:** the original + the linter output + the four criteria T/L/C/B.
- **Action:** For each criterion, record the hits. Plan a change list (frontmatter
  fields, body layering, flow convergence, permission declarations, context
  isolation, length). Tag each change with its reason, whether it assumes a default,
  and its P0 status.
- **Output:** the change plan (the rows that will become the changelog).
- **Fallback:** a missing permission/context field -> infer a sensible default and
  mark it "assumed" (H3). Dangerous operations or external calls -> infer
  `disable-model-invocation: true` or narrow the tool list, and mark it "assumed".

### Step 4 - Emit the artifact
- **Input:** the change plan.
- **Action:**
  - **refactor:** write the optimized full SKILL.md (backing up the original, H2),
    including a changelog section (old -> new + reason + assumed? + P0?).
  - **audit:** write a diagnostic report `skillmd_audit_<name>.md` only; do **not**
    touch the original (H1).
  - Show the result to the user.
- **Output:** the optimized file / the audit report.
- **Fallback:** if a same-named report exists, choose a new name; never overwrite.

### Step 5 - Close with a conclusion
- **Input:** the Step 4 artifact.
- **Action:** Give the "what changed + the assumed list + the P0 items + next steps
  (split into references? run the publish gate?)". State the boundary plainly: this
  skill does not fix the called code and does not run a publish-compliance gate.
- **Acceptance gate (全通过):** re-run the linter on the emitted file; the refactor
  is "done" only when `BLOCKER=0 AND MEDIUM=0` (LOW/reminder items may remain and be
  reported, never silently dropped - H1). If any BLOCKER or MEDIUM remains, return to
  Step 3 with the linter's "diagnosis + suggested fix" hints (human fallback).
- **Output:** the closing paragraph + the final linter verdict.
- **Fallback:** if a same-named report exists, choose a new name; never overwrite.

---

## Progressive-disclosure routing

**Input:** any `SKILL.md` (frontmatter and body). Refuses binaries / pure data /
non-skill files.

| When | Read |
|---|---|
| A routine optimization or audit | this file's five-step flow |
| Per-platform frontmatter fields (Claude / ClawHub / SkillHub) | `references/platform-frontmatter.md` |
| Trigger/boundary wording and the changelog template | `references/trigger_boundary_changelog.md` |
| Token budget and compaction headroom | `references/token_budget.md` |
| i18n / Natural-Language Policy + non-Chinese-user checklist | `references/i18n_policy.md` |
| Polishing the companion README.md (structure, badges, install, examples, license) | `references/readme_quality.md` (skeleton: `assets/readme_template.md`) |
| The audit-mode output contract (read-only diagnostic report shape) | `references/skillmd_audit_sample.md` |
| A quick mechanical screen | `scripts/check_skillmd.py <file> [--platform p]` |

## Trigger examples

Typical trigger: "This skill's SKILL.md is too long and the hard constraints get
lost when the context compacts; refactor it for progressive disclosure and give me
the full file plus a changelog." -> recognize as Step 1, `refactor` mode, host
platform, run the five steps.

Explicit non-trigger: "Help me audit whether `scripts/gate.py` inside this skill is
well written." -> that is a code-quality audit; route to **skill-clean-audit**. This
skill optimizes SKILL.md text and structure only; it does not review the called
scripts.

Easy-to-confuse boundary: "Run every check before I publish." -> that is a
publish-time security/compliance gate; route to **skill-publish-gate**. This skill
only optimizes SKILL.md structure and triggering; it does not run a publish
preflight.

Readme-mode trigger: "This skill's README is too long and missing install steps —
polish it." -> recognize as Step 1, `readme` mode, host platform, read
`references/readme_quality.md`, run its five steps.

---

## Maintenance notes

- **Main-file budget:** target 150 lines or fewer, hard cap 200; sink details into
  `references/`. Core rules stay within the first ~3000 tokens.
- **Frontmatter contract:** the published skill uses the ClawHub-native
  `metadata.openclaw.requires` and `license: MIT-0`. Host-side fields such as
  `allowed-tools`, `context: fork`, and `disable-model-invocation` are per-host and
  documented in `references/platform-frontmatter.md`, not invented into the published
  schema.
- **Cross-agent:** the body never hard-codes one host; platform differences live in
  `references/platform-frontmatter.md`.
- **Division of labor:** skill-clean-audit (code quality) / skill-publish-gate
  (publish gate) / skill-creator (new skill); this skill only optimizes an existing
  SKILL.md's structure and triggering.
- **i18n / readme modes:** the language picker and README capability live in
  `references/i18n_policy.md` and `references/readme_quality.md`; both reuse the
  three-state language choice, so they never duplicate language handling. The
  `readme` mode only polishes the companion README.md — it does not fix called
  code or run a publish gate.
