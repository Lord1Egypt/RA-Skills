## Description:

Drafts Chinese-language stakeholder updates for bosses, clients, execution teams, and risk-transparent reviews from the same project facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and communication teams use this skill to turn project progress, risks, and next steps into audience-specific Markdown status updates for management, customers, execution teams, and risk reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stakeholder drafts may misstate facts, over-polish risk, or hide uncertainty if sent without review.

Mitigation: Review drafts against the source facts, keep missing information visible, and preserve risk-transparent language before sending.

Risk: Inputs may contain personal, confidential, or compliance-sensitive project information.

Mitigation: Redact or limit sensitive data unless authorized, and do not send generated drafts directly to external systems without approval.

Risk: The packaged script contains unused local-audit functions that are not active under the bundled configuration.

Mitigation: Keep the bundled spec unchanged unless those audit functions have been reviewed and intentionally enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/stakeholder-update-drafter)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [Skill README](artifact/README.md)
- [Structured output specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown drafts with audience-specific sections and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce JSON when the bundled script is run with the JSON format option.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
