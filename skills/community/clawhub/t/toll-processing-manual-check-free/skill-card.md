## Description:

A local Chinese-language checker that reviews processing-trade manual and bonded-material reconciliation tables for arithmetic consistency, duplicate rows, blanks, placeholders, and negative quantity or amount values, with source-cited findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Customs, documentation, finance, and operations users can run this skill before monthly customs close or manual cancellation to check a pasted processing-trade reconciliation table. It helps identify table-level inconsistencies and missing evidence, but does not provide customs, tax, or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the checker output as customs, tax, or legal advice even though it only checks table-level consistency.

Mitigation: Present findings as reconciliation checks and require review by qualified customs, finance, or legal personnel before acting on them.

Risk: The free edition omits several checks that a complete reconciliation may require.

Mitigation: Show the executed and withheld check lists with each run, and do not interpret a clean free-edition run as a complete compliance review.

Risk: The local Node.js checker processes user-provided files passed with --input.

Mitigation: Install only when comfortable running the local checker, review inputs before execution, and avoid providing unnecessary sensitive data.

Risk: Insufficient or malformed input can otherwise lead to misleading reassurance.

Mitigation: When required table evidence is missing, return an insufficient-input status rather than a pass/fail conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/toll-processing-manual-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON findings with line references, plus command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Node.js checks on user-provided input; free edition reports only the checks it executes and lists withheld checks.]

## Skill Version(s):

1.0.43 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
