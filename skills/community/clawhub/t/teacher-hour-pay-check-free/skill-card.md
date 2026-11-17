## Description:

Teaching Hour Pay Check (Free) locally checks teaching-hour consumption and teacher hourly-pay sheets by recomputing pay, validating lesson-type rules, tying student consumption to system ledger rows, reviewing totals, and flagging missing or duplicate records with source line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Education operations and finance staff use this skill to check monthly teacher-hour pay sheets against student hour-consumption records. It performs local arithmetic and table-consistency checks, reports missing input instead of guessing, and cites source line numbers for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be used on copied teacher hour and pay table data that can contain sensitive payroll or student-related operational information.

Mitigation: Run it only in an approved local environment and avoid sharing input tables or outputs beyond authorized reviewers.

Risk: The findings are limited to arithmetic and table-consistency checks and do not validate attendance, payroll policy, employment terms, legal compliance, or contract interpretation.

Mitigation: Use the cited line-level findings as review aids, then confirm payroll, attendance, contract, and policy decisions with the appropriate source records and responsible staff.

Risk: The free version withholds several broader reconciliation checks such as cross-teacher or cross-campus summaries and difference attribution.

Mitigation: Review the checks_not_run or checks_withheld output before relying on the result for month-end reconciliation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/teacher-hour-pay-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON or human-readable terminal text with finding summaries and source line citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; sample execution reported no network use and returns insufficient_input when required table columns are missing.]

## Skill Version(s):

1.0.5 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
