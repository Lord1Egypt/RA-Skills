## Description:

Provides a starter pricing-tier report and US SaaS pricing guidance for founders, pricing managers, and sales engineers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US SaaS founders, pricing managers, and sales engineers can use it to draft a tiered pricing report and consult US-focused pricing guidance. Independently calculate and approve prices before use because the generated figures do not reflect supplied cost inputs or margin checks.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Generated prices are placeholders because the tool ignores supplied costs and does not perform the promised margin checks.

Mitigation: Independently calculate and approve prices before using the report.

Risk: Writing to an output folder that already contains price-tiers.md may replace that file.

Mitigation: Choose an output folder where replacing price-tiers.md is acceptable.

Risk: The optional Windows app is separate from this workflow and was not reviewed; a matching publisher-provided hash does not establish its safety.

Mitigation: The app is unnecessary for this workflow; avoid it unless you separately assess it before execution.

## Reference(s):

- [US SaaS pricing mechanics](artifact/references/saas-pricing.md)
- [SaaS Pricing Tiers on ClawHub](https://clawhub.ai/rapidworker1/skills/saas-pricing-tiers)

## Skill Output:

**Output Type(s):** [Markdown, Pricing guidance]

**Output Format:** [Markdown price-tier report with tier names, prices, and guardrails]

**Output Parameters:** [Reads an input file and an optional output directory; the bundled report currently uses preset cost and markup values.]

**Other Properties Related to Output:** [Writes price-tiers.md in the selected output folder. Treat generated prices as placeholders: the tool ignores supplied costs and does not check margins. Review and approve all pricing before use.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
