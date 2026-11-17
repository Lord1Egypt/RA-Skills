## Description:

Checks local travel-standard and toll-expense worksheets for each department and prints findings with source file and line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance reviewers use this skill before monthly or quarterly reimbursement review to check department travel and toll materials for arithmetic, consistency, missing data, and unsupported conclusions. It is a local aid for expense review, not an approval, audit, tax, or policy decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes reimbursement worksheets selected by the user.

Mitigation: Run it only on intended local folders and review the selected inputs before execution.

Risk: The output can identify arithmetic or consistency issues but is not an audit, tax, approval, or policy decision.

Mitigation: Treat findings as review aids and have the responsible finance or policy owner make final determinations.

Risk: The free release intentionally omits some checks and reports them as not run.

Mitigation: Review the runtime not-run check lists, including scope.checks_not_run and scope.sub_checks_not_run, before relying on coverage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/travel-toll-pack-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Console text or JSON results with per-department conclusions and source file line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes user-provided local files and prints results without network use, file writes, or persistence according to the supplied security evidence.]

## Skill Version(s):

1.0.22 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
