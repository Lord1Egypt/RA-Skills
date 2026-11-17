## Description:

Checks copied R&D super-deduction worksheet text locally for arithmetic consistency, other-expense cap issues, duplicate projects, blank fields, and line-cited findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External finance and tax teams at companies with R&D spending use this skill to check copied R&D expense collection tables before quarterly prepayments or annual settlement. It highlights table arithmetic issues, other-expense cap problems, duplicate projects, blanks, and missing input instead of giving unsupported conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks tax-adjacent R&D expense tables but does not provide tax advice, determine R&D eligibility, choose the applicable super-deduction ratio, or check industry exclusions.

Mitigation: Use the output as an arithmetic and table-consistency aid, and have tax-qualified reviewers confirm eligibility, ratios, and policy applicability before filing decisions.

Risk: The free edition intentionally omits several checks, including entrusted R&D inclusion, super-deduction amount calculation, negative expense detection, and single-item other-expense ratio prompts.

Mitigation: Confirm whether omitted checks are required for the workflow before relying on the free-edition output.

Risk: Malformed, incomplete, or headerless input can prevent execution or produce a missing-input result rather than a conclusion.

Mitigation: Provide the complete worksheet text with recognizable headers and treat missing-input responses as non-results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/rd-expense-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance plus optional JSON check results from the local Node runner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input returns missing fields instead of conclusions.]

## Skill Version(s):

1.0.35 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
