## Description:

A free local checker for tuition refund tables that recalculates consumed tuition, refundable tuition, actual refunds, differences, totals, duplicate students, and blank placeholders with source line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External education and training operators use this skill to check tuition refund spreadsheets before disputes or reconciliation reviews. It helps agents run deterministic arithmetic checks and report missing inputs without making legal, contract, or business-policy judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read the local input file path supplied by the user.

Mitigation: Run it only on intended tuition refund table files and avoid pointing it at unrelated sensitive documents.

Risk: The checks are deterministic arithmetic checks and do not decide whether refund terms, contract clauses, or business policies are legal or appropriate.

Mitigation: Use the findings as reconciliation support and have a qualified reviewer assess legal, contractual, and policy questions.

Risk: Missing headers, blank rows, or unsupported source formats can prevent the checker from reaching a conclusion.

Mitigation: Provide table text with the required refund columns and treat insufficient-input output as a request for more material, not as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/tuition-refund-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text or JSON findings with source line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided tuition refund table text and reports insufficient input instead of inventing conclusions.]

## Skill Version(s):

1.0.49 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
