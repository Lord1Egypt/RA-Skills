## Description:

Generates Chinese vendor-risk briefs for external SaaS or API integrations, focusing on integration impact, permissions, data flows, risks, mitigations, alternatives, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Security, procurement, and integration reviewers use this skill to turn supplied vendor capability, permission, and data-type information into a structured review draft. It is intended as a review aid and checklist source, not as a formal legal or security approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated brief could be mistaken for a completed legal, procurement, or security approval.

Mitigation: Treat the output as a review draft and require formal approval by the appropriate legal, security, or procurement owner before relying on it.

Risk: Sensitive vendor or customer information may be included in the input materials.

Mitigation: Run the skill only on files intentionally provided for review, prefer stdout or dry-run for sensitive material, and redact personal or confidential data before processing when possible.

Risk: The skill does not independently verify vendor facts or fetch current external evidence.

Mitigation: Use the generated待确认项 and next steps to identify missing facts, then verify those facts against authoritative vendor and internal sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/vendor-risk-brief)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Output template](artifact/resources/template.md)
- [Structured spec](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Structured Markdown by default, with optional JSON output from the bundled local script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include vendor summary, permissions and data flow, main risks, mitigations, alternatives, recommendation, items to confirm, and next steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
