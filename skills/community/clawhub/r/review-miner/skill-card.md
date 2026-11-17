## Description:

Extracts key selling points, pain points, objections, and phrases to avoid from reviews, ratings, and customer feedback for voice-of-customer and marketing analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, product, customer support, and research teams use this skill to turn local review CSVs, text lists, or ticket summaries into reviewable Markdown reports covering high-frequency selling points, pain points, objections, unsafe claims, testable information, and sample gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input review data may contain personal or sensitive customer information.

Mitigation: Redact or anonymize inputs before use and provide only files intended for analysis.

Risk: Generated summaries may overstate themes or produce unsupported marketing claims.

Mitigation: Review outputs against the source reviews before using them in marketing or operational decisions.

Risk: The skill can be misused to fabricate reviews or expose user identities.

Mitigation: Use only for analysis of genuine source material and keep outputs free of invented reviews or identifiable customer details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/review-miner)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)
- [Artifact README](artifact/README.md)
- [Output Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown report, with an optional JSON wrapper when the local script is invoked in JSON mode.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewable summaries and checklists from local user-supplied content; outputs should be checked before use in marketing or operational decisions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
