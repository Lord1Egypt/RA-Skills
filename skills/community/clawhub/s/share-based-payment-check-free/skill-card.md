## Description:

This skill locally checks Chinese share-based payment detail tables for row recalculation, total tie-outs, duplicate rows, blanks, and balance roll-forward consistency, with each finding tied back to the source text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance teams at companies with equity incentive plans use this skill before monthly or quarterly share-based payment expense close, audit workpaper handoff, or broker review to check deterministic relationships in exported table text. It helps identify arithmetic mismatches, missing required columns, blank placeholders, duplicate plan-period rows, and free-tier checks that were not run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic table checks as accounting, audit, tax, or valuation judgment.

Mitigation: Use the output as a deterministic tie-out aid only, and have qualified finance, audit, tax, or valuation reviewers decide policy and judgment questions.

Risk: The free tier intentionally omits several checks, including straight-line variance, over-amortization, and vesting-period completion checks.

Mitigation: Review the reported withheld checks before relying on results, and run additional procedures where those omitted checks matter.

Risk: Insufficient or malformed source table text can prevent meaningful conclusions.

Mitigation: Provide exported table text with recognizable headers and data rows; treat insufficient-input output as a request for more material, not as a clean result.

Risk: The skill runs a local Node.js script on exported share-based payment table text.

Mitigation: Install and run it only in environments where local Node.js execution on that data is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/share-based-payment-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Terminal text or JSON result object with findings, summary, executed checks, withheld checks, and local execution status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a JSON input file or copied table text; insufficient input returns missing-field guidance instead of a pass or fail conclusion.]

## Skill Version(s):

1.0.20 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
