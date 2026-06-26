---
name: assemble-panel
description: "Use when another skill or agent needs a review panel assembled, retained, or converged — invoked by /review, /plan-review, and code-reviewer, not directly by users."
---

# Assemble Panel

Centralizes reviewer selection and loop governance. Returns a panel + policy to the caller; the caller dispatches. This skill produces data — it never dispatches agents or modifies files.

## Integration Contract

Callers provide:
- `scope`: a plan file path OR a git diff (the artifact under review)
- `overrides` (optional): `{ include: [], exclude: [] }`

Returns (structured text the caller parses):
- `panel`: ordered list of reviewer agent names
- `policy`: gate, cap, and the algebra below

Fallback when unavailable: `[technical-editor, code-reviewer]`, gate=P2, cap=3.

**Cross-tool note:** Codex/Cursor cannot invoke skills via the Skill tool. Read this file directly and apply the policy algebra inline.

## Policy Algebra (frozen — do not modify, version: 1)

```
DEFAULTS:
  gate    = P2                       # fix P0-P2, record P3+
  cap     = 3                        # max rounds before escalate
  always  = [technical-editor]       # expandable, never reducible

ASSEMBLE(scope: plan_file | diff):
  panel = always
        + select_by_scope(file_types(scope))
        + select_by_keywords(body(scope))
        + overrides.include
        - overrides.exclude            # cannot remove `always` members

RETAIN(reviewer, round_findings):
  keep(reviewer) while round_findings.any_above(gate)

EXPAND(panel, prior_scope, current_scope):
  new_coverage = file_types(current_scope) - file_types(prior_scope)
  panel += select_by_scope(new_coverage) when new_coverage

CONVERGE(round, panel, cap):
  APPROVE   when all(reviewer.done for reviewer in panel)
  ESCALATE  when round >= cap
  EXIT      when any(reviewer.verdict == DROP)
  continue  otherwise

ESCALATE_RECURRING(finding, rounds_present):
  finding.severity += 1 when rounds_present >= 2
```

## Scope-to-Reviewer Map

Used by `select_by_scope(file_types)`:

| File pattern | Reviewer |
|---|---|
| `.ts`, `.js`, `src/`, `tests/` | code-reviewer |
| `.yml`, `.github/workflows/` | code-reviewer, security-auditor |
| `.sh`, `scripts/`, `hooks/` | code-reviewer, security-auditor |
| `.md` (plans, ADRs, docs) | architect-reviewer |
| `*.css`, `*.tsx`, UI components | design-reviewer, accessibility-tester |
| `sync.sh`, `AGENTS.md`, `config.toml`, skills | codex-specialist |
| `*.pem`, `*.key`, secrets patterns | security-auditor |

When multiple patterns match, union all reviewers. Duplicates collapsed.

## Keyword-to-Reviewer Map

Used by `select_by_keywords(body)`:

| Keyword / phrase | Reviewer |
|---|---|
| "architecture", "ADR", "system design", "plan" | architect-reviewer |
| "security", "auth", "token", "PAT", "OIDC" | security-auditor |
| "WCAG", "accessibility", "a11y", "aria" | accessibility-tester |
| "UI", "component", "layout", "design system" | design-reviewer |
| "docs", "research", "ecosystem", "reference", "educational" | fact-checker |
| "Codex", "cross-tool", "sync.sh" | codex-specialist |

Keywords are case-insensitive substring matches against the scope body.

## Override Rules

- `overrides.include` appends reviewers unconditionally.
- `overrides.exclude` removes reviewers EXCEPT those in `always`. Attempting to exclude an `always` member is silently ignored.
- Invalid reviewer names are rejected with an error listing valid names.

## Failure Modes

- **Scope empty or unreadable**: return `always` panel only, warn caller.
- **No file types detected**: fall back to keyword matching only. If neither matches, return `always` panel.
- **Caller requests cap > 5**: clamp to 5. Non-negotiable ceiling.
- **Panel exceeds 5 members**: warn caller — likely a sign the change is too broad.
- **Reviewer unavailable at dispatch time**: caller skips that reviewer and notes the gap.

## Orchestrator Authority

The panel recommends; the orchestrator (the agent dispatching the panel) decides. The gate and cap above are inputs to that decision, not overrides of it.

**MAY:**
- **Descope** a P1/P2 finding if addressing it balloons scope past a single concern — file a follow-up issue.
- **Split** into phased PRs when panel findings grow scope past a reasonable single landing. Core ships first; hardening and docs follow. **Pre-dispatch:** before handing off to an implementer, check the plan's scope — if Files-to-Modify > 5 OR total planned test count > 8, split into sequential phases upfront. The reactive trigger above fires after panel feedback; this fires before implementation starts, preventing single-agent context overflow (e.g., PR #241: 3 new scripts + aggregator changes + ADR + 11 tests → 78 tool uses → overflow).
- **Push back** on false positives with explicit rationale. If the same finding recurs across reviewers or rounds, examine why — either the reviewers are right, or there's a structural reason the code looks like the pattern they're flagging. When pushing back, name the finding (reviewer + severity + quoted text), give the rationale, and cite evidence (code paths, existing patterns, prior ADRs).
- **Accept with documented deviation** — address some P1s, defer others with justification in the plan's Risks section.

**MUST NOT:**
- Silently drop P0 findings. P0 must be addressed, escalated, or the plan rejected.
- Override `security-auditor` findings without escalating to a human.

**Escalate to human when:**
- A P0 is disputed and the rationale for pushback isn't clear.
- Multiple reviewers converge on a concern the orchestrator disagrees with.
- A security finding's mitigation trade-off affects the trust model.

**Example pushback:**
> Security-auditor P1: "Include severity inside HMAC payload."
> Orchestrator: Pushing back. Severity is computed by a separate classifier (classify-findings.sh), not emitted by the CLI wrapper, so it's not available at sign-time. Binding it into HMAC would require restructuring the entire review pipeline. Alternative: include `tier` in fingerprint — this closes the cross-tier collision vector without HMAC restructure. Will address P0-2 with tier-in-fingerprint; defer severity-in-HMAC as a separate ADR if needed.

## Output Format

```
PANEL: technical-editor, code-reviewer, security-auditor
GATE: P2
CAP: 3
ALWAYS: technical-editor
NOTE: codex-specialist included — scope touches sync.sh
```

One `NOTE` line per non-obvious selection decision. Callers surface these in review summaries.
