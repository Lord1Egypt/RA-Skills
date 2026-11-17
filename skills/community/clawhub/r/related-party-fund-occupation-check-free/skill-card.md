## Description:

A free local checker for related-party ledger tables that recalculates row balances and totals, detects duplicates and blanks, and cites source evidence for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, securities affairs, and internal audit teams use this skill to check copied related-party ledger tables before monthly cleanup, annual audit work, and disclosure preparation. It performs deterministic arithmetic and data-quality checks, but it does not decide legal, audit, tax, or securities-compliance conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic and data-quality findings as legal, audit, tax, or securities-compliance advice.

Mitigation: Use the output as a preliminary ledger check and have qualified professionals review disclosure, audit, tax, and regulatory conclusions.

Risk: The free release intentionally omits several checks listed as outside the free scope and does not verify bank, ERP, contract, or board-resolution records.

Mitigation: Confirm the executed-check list before relying on results and perform separate audit or reconciliation procedures for source-document truth and omitted checks.

Risk: Results depend on user-supplied Chinese ledger text with recognizable headers, so malformed or incomplete tables can produce insufficient-input outcomes.

Mitigation: Provide the required table headers and source rows, then review the cited evidence for each finding before acting on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/related-party-fund-occupation-check-free)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output can be human-readable text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; execution is local and the runner rejects input files above 4 MB.]

## Skill Version(s):

1.0.17 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
