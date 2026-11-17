## Description:

Checks VAT surtax worksheets by recalculating listed surtax lines, totals, duplicate periods, and missing fields, with each finding tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External finance, tax, and accounting users can run this local checker against copied VAT surtax worksheet text to identify arithmetic mismatches, total-row issues, duplicate periods, and blank or placeholder fields. The free version reports only the checks it executes and should not be treated as tax advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the checker output for complete tax advice.

Mitigation: Treat findings as worksheet arithmetic and completeness checks only, and have qualified tax staff review rate, policy, and filing conclusions.

Risk: The free version omits several validations, including some rate and policy checks.

Mitigation: Review the listed checks not run before relying on a clean result, especially for negative VAT bases, abnormal rates, and applicable surtax policy.

Risk: Insufficient or malformed worksheet text can prevent the skill from reaching a conclusion.

Mitigation: Provide worksheet text with recognizable headers and line items, and treat insufficient-input output as no conclusion rather than a pass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/surtax-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON findings with source line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard libraries; the free version lists checks that were executed and checks that were not included.]

## Skill Version(s):

1.0.31 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
