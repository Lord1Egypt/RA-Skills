## Description:

Checks Chinese safety hazard rectification ledgers for deadline arithmetic, closure consistency, duplicate hazards, total-row reconciliation, and missing or invalid fields, with source line citations for findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Safety, environmental health, and operations teams use this skill to self-check copied text from monthly hazard investigation and rectification ledgers before reporting, audits, or inspections. It identifies document-level consistency issues and missing fields without making legal, regulatory, or on-site safety determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat document checks as legal, regulatory, or on-site safety determinations.

Mitigation: Use the output as a ledger consistency aid only; qualified personnel should verify site conditions, remediation effectiveness, and compliance decisions.

Risk: Incomplete or malformed ledger input can prevent checks from running or leave unsupported conclusions unavailable.

Mitigation: Provide the ledger text with headers and required columns, review any missing-input guidance, and rerun with complete material before relying on results.

Risk: Ledger materials may contain sensitive operational safety details.

Mitigation: Provide only the text or input file intended for analysis and follow the organization's data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/safety-hazard-rectification-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Shell commands]

**Output Format:** [Plain text or JSON containing line-referenced findings, executed-check summaries, omitted-check notes, and missing-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on supplied ledger text or input files; security evidence reports no network use, persistence, credential access, or hidden destructive behavior.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
