## Description:

A local checker for treasury and bill worksheets that runs 14 built-in consistency checks per object directory and reports conclusion lines with source file and line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance teams, treasury staff, accountants, and bookkeeping providers use this skill during month-end close, cash counts, bill maturity checks, and bank reconciliation to review exported treasury and bill worksheets. It helps identify arithmetic, reconciliation, duplicate-entry, missing-material, and not-run check conditions without replacing audit, approval, legal, or authenticity review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes exported financial worksheets locally, which may contain sensitive treasury and bill data.

Mitigation: Run it only in an approved local environment and handle input and output files according to the organization's financial data policy.

Risk: Consistency-check output could be mistaken for audit, legal, approval, authenticity, or business-judgment conclusions.

Mitigation: Use the output as review support only, and require qualified finance, audit, legal, or approval review for final decisions.

Risk: The free release lists withheld and not-run checks, so missing coverage may be easy to overlook.

Mitigation: Review the reported withheld, not-run, and insufficient-input sections before relying on any conclusion line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/treasury-bill-pack-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Command-line text or JSON results with source file and line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally over user-provided worksheet exports; reports withheld and not-run checks separately from executed checks.]

## Skill Version(s):

1.0.27 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
