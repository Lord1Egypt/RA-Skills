## Description:

A local deterministic checker that recomputes Chinese government subsidy ledger amounts, acceptance-document checklist completeness, duplicate project entries, budget mismatches, missing fields, and negative or unparsable amounts, with source line references for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, tax, and project filing staff use this skill during subsidy acceptance, project closeout, and annual fiscal self-checks to compare subsidy ledgers against acceptance-document checklists. It reports arithmetic and checklist issues without deciding subsidy eligibility, policy applicability, audit compliance, or legal conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes business and financial ledger contents that may be sensitive.

Mitigation: Run it locally as packaged and avoid sharing input ledgers outside the intended review workflow; server security evidence reports no network use, persistence, hidden code execution, or data exfiltration.

Risk: The findings are limited to arithmetic checks and checklist completeness, and may be mistaken for legal, audit, eligibility, or policy decisions.

Mitigation: Treat outputs as review aids only and route eligibility, policy applicability, audit compliance, and legal questions to qualified reviewers.

Risk: Incomplete or unrecognized inputs can prevent checks from running or omit conclusions.

Mitigation: Provide a table with recognizable headers and review the returned missing-input list, checks_not_run, and checks_out_of_scope fields before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/subsidy-acceptance-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill manifest and usage guide](artifact/SKILL.md)
- [Local runner](artifact/scripts/run.mjs)
- [Deterministic checking engine](artifact/scripts/engine/subsidy-acceptance-check.js)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, guidance]

**Output Format:** [Human-readable text or JSON containing status, findings, summary totals, executed checks, checks not run, and out-of-scope checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers and use P0/P1/P2 severity levels; insufficient input returns missing requirements instead of conclusions.]

## Skill Version(s):

1.0.5 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
