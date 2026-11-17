## Description:

A free local checker for accounts-receivable collection plan and payment tables that recomputes row arithmetic, totals, duplicates, blanks, and negative amounts while citing source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users can use this skill during monthly closing, reconciliation, or inventory checks to validate accounts-receivable collection plan tables. It focuses on deterministic table checks and does not assess customer creditworthiness, aging policy, legal deadlines, or ERP exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accounts-receivable tables may contain sensitive financial or customer information.

Mitigation: Run the skill only in an environment approved for that data and review inputs before use; the reviewed artifact processes data locally and does not show network transmission.

Risk: The free release omits several checks that are listed as unavailable, so results may not cover all business controls.

Mitigation: Treat findings as deterministic checks for the included scope and separately review omitted areas such as overdue-balance limits, collection-rate thresholds, and aging-day policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/receivable-collection-plan-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON check results, with cited row-level findings and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with bundled Node.js code; accepts JSON or pasted table text and reports insufficient input without making a finding.]

## Skill Version(s):

1.0.47 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
