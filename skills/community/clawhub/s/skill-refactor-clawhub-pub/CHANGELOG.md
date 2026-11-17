# Changelog

All notable changes to **skill-md-optimizer** are recorded here.
Format follows `Keep a Changelog`; versions follow SemVer.
(Conventions: the changelog lives here, **not** in `README.md`.)

## [1.0.0] - 2026-10-11

First published version of the cross-agent SKILL.md progressive-disclosure
optimizer. Ships the skill body, five references, two assets, and the
deterministic offline linter.

### Added
- `SKILL.md` — host-neutral (ClawHub-native `metadata.openclaw`), three modes
  (`refactor` / `audit` / `readme`), 9 hard constraints (H1–H9), four criteria
  (T/L/C/B), a five-step single-turn closed flow, a language three-state picker
  (NL-Policy compliant), and a progressive-disclosure routing table.
- `references/platform-frontmatter.md` — 14-agent field matrix; verified
  conclusion that OpenClaw-native metadata is the common format and Claude's
  fields are an extension layer, not a competing standard.
- `references/token_budget.md` — official budget anchors (body <500 lines,
  description ≤1024, name ≤64; compaction 5000/skill + 25000 combined;
  500 lines ≈ 3500 tokens) plus the ÷4 estimation rule.
- `references/i18n_policy.md` — ClawHub Natural-Language Policy two shapes
  (with scanner hit samples) and the auto/zh/en three-state picker.
- `references/readme_quality.md` + `assets/readme_template.md` — the readme
  mode (five questions + fixed order + exclusions).
- `references/trigger_boundary_changelog.md` — wording + changelog template.
- `references/skillmd_audit_sample.md` — audit-mode output contract sample
  (verdict / T-L-C-B / H checks / NL-Policy / change log / next steps).
- `scripts/check_skillmd.py` — offline, stdlib-only linter; 0/2/1 exit-code
  contract; per-finding `hint` for human fallback; `--json` with
  `schema_version 1.0`.
- `assets/checklist.html` — 33-item checkable audit list (localStorage + export).
- `README.md` — repository overview (install / usage / platform copies / rules).

### Lint rule set (P0 + P1)
- `PL-CL-2` recognizes `metadata.openclaw.requires` (nested), not only top-level
  `requires` — removes the OpenClaw-native false positive.
- T1.4: reference check strips code fences, so code examples are not flagged as
  dangling references.
- T1.2: `NL-001` / `NL-002` Natural-Language Policy mechanical probes
  (non-blocking advisory).
- T1.6: `--json` schema frozen at `schema_version 1.0`
  (`verdict`, `exit_code`, `counts`, `issues[{rule_id,severity,msg,hint}]`).
- Default `--token-budget` set to **3500** to match the official 500-line body
  cap.
