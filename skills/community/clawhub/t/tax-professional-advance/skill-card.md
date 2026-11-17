## Description:

Tax Professional Advance helps users evaluate US tax deductions, track deductible expenses, plan estimated payments, assess audit risk, and prepare year-end summaries across W-2, self-employed, S-Corp, mixed, and multi-state situations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shoumiksaha](https://clawhub.ai/user/shoumiksaha)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals, self-employed workers, and small business owners use this skill to get US tax planning guidance, track potential deductions, organize documentation, and prepare filing summaries. Users should verify tax decisions with a licensed tax professional for their specific facts.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can store sensitive financial records in workspace expense files.

Mitigation: Use it only in a private workspace and avoid storing full payment confirmation numbers, tax identifiers, or other unnecessary sensitive details.

Risk: The skill may read context from other skills when tailoring tax guidance.

Mitigation: Confirm before allowing it to read other skills' data and limit that access to information needed for the current tax task.

Risk: The skill includes persistent Telegram reminder setup commands.

Mitigation: Run reminder setup only after verifying the recipient and understanding how to review or remove the scheduled jobs.

Risk: Tax guidance may be incomplete or outdated for a user's exact situation.

Mitigation: Verify current-year rules and significant tax decisions with authoritative IRS guidance or a licensed CPA or tax attorney.

## Reference(s):

- [Common Write-Offs People Miss](references/common-writeoffs.md)
- [IRS](https://www.irs.gov)
- [ClawHub Skill Page](https://clawhub.ai/shoumiksaha/skills/tax-professional-advance)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON expense records and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workspace expense-tracking records and reminder setup commands when the user requests tracking or calendar workflows.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
