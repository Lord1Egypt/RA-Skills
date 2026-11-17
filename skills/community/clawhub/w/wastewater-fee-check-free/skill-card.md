## Description:

A local wastewater settlement checker that recalculates water volume, service fees, quality-band pricing, excess-discharge deductions, duplicate settlements, and missing or unparseable table fields from user-provided tabular data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External water utility, wastewater plant, park operations, and finance teams use this skill during monthly settlement review to find arithmetic mismatches and missing data in wastewater fee and water-quality tables. It supports local prepayment and invoicing checks, but does not decide legal compliance, water-quality truth, monitoring equipment validity, or contract reasonableness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic reconciliation results as proof of legal compliance, water-quality status, or monitoring-equipment validity.

Mitigation: Use the skill only for table arithmetic and consistency checks; route compliance, monitoring, and contract judgments to qualified reviewers and authoritative records.

Risk: Incomplete or unrecognized input tables can prevent a reliable conclusion.

Mitigation: Provide the full table with headers and required columns; when the skill reports insufficient input, treat that as no conclusion rather than a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/wastewater-fee-check-free)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Human-readable console text or JSON containing findings, summaries, executed checks, withheld checks, and scope notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers and original table values when issues are detected; insufficient input returns missing-field guidance rather than a conclusion.]

## Skill Version(s):

1.0.7 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
