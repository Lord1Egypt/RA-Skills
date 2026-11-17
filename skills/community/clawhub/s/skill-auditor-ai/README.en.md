# Skill Auditor

> Independent audit skill for comprehensive 8-dimension inspection of existing Skills.

## Features

- **8-dimension deep audit**: Structure(S) / Security(T) / Trigger(A) / Effectiveness(E) / Competition(C) / Platform(P) / Documentation(D) / Code Quality(Q)
- **3-level maturity grading**: L1 Prototype / L2 Iteration / L3 Release — determines audit scope and strictness
- **4 user confirmation points**: Maturity / Report / Post-remediation / Publish
- **Remediation mode**: Fixes P0/P1/P2 issues after user authorization, minimal changes
- **Regression audit**: Post-remediation re-audit + before/after diff (fixed/unfixed/new)
- **4 entry modes**: Full audit / Single-dimension / Batch / Regression
- **Standardized reports**: Severity grading (Critical/Important/Minor/FYI) + fix suggestions + priority

## Positioning

This skill focuses on **independent deep audit + regression verification**, not responsible for skill creation or publishing:

```
Skill Creation  → Create new skills from scratch (not this skill's responsibility)
Skill Publishing → Push to external platforms (not this skill's responsibility; this skill only provides publishing suggestions, executed manually by the user)
Skill Audit     → Independent deep audit + maturity grading + remediation + regression (this skill)
```

This skill **defaults to read-only audit, remediation requires user authorization, never executes publishing operations**.

> **User Notice**: The remediation mode (Phase 4.5) and originality cleanup submode (A2) modify the audited Skill's files.
> - Defaults to read-only audit; modifications only occur after the user explicitly selects "Enter remediation mode" at confirmation point 2
> - Originality cleanup (Phase O-4) requires explicit user authorization at confirmation point O before executing Edit; **no trigger phrase can bypass confirmation point O**
> - To skip remediation, select "Report only"
> - Publishing: this skill **does not execute publishing**; it only provides publishing suggestions after explicit user authorization at confirmation point 4, with the user manually publishing to the three platforms

## Trigger Words

- 「技能审计」(Skill Audit)
- 「审计技能」(Audit Skill)
- 「技能体检」(Skill Health Check)

## Audit Dimensions

| Code | Dimension | Core Checks |
|------|-----------|-------------|
| S | Structure | frontmatter / 4 modules / ≤200 lines / progressive disclosure |
| T | Security | credentials/paths/dangerous commands/YARA/SSD3/MCP |
| A | Trigger | positive/negative examples/conflict/keyword frontloading |
| E | Effectiveness | declaration consistency/output format/incremental value |
| C | Competition | SkillHub API + Tencent 9-dim + differentiation |
| P | Platform | TRACE 5-dim + SkillSpector 9 items + file limits |
| D | Documentation | reference consistency/version sync/EN-CN sync |
| Q | Code Quality | error handling/resource mgmt/naming/complexity |

## Scoring

- Each dimension scored 0-10
- Weighted average (T×2.0, P×1.5, S/A/E×1.0, C/D/Q×0.5)
- Critical in T dimension → overall status = ❌ FAIL (veto)

## Output

- Audit report output to both conversation and `<skill-dir>/.audit-report.md`
- Regression audit additionally generates `.audit-report-prev.md` (previous report backup)

## License

MIT
