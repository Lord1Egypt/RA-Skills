## Description:

Audits e-commerce sites for AI shopping-agent discoverability and readiness by scoring product data, catalog APIs, shopping feeds, checkout compatibility, and description quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, e-commerce operators, and agency teams use this skill to audit Shopify, WooCommerce, or custom storefronts before launches, during traffic investigations, or as recurring storefront health checks. It produces a scored readiness report and prioritized fixes for improving product visibility to AI shopping agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auditing storefronts without authorization may create unwanted traffic or policy concerns.

Mitigation: Use the skill only on sites you control or have permission to test.

Risk: Cart API availability checks could be confused with live purchasing behavior.

Mitigation: Treat cart checks as non-purchasing availability tests and do not submit live transactions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-b2a-audit)
- [Publisher profile](https://clawhub.ai/user/zero2ai-hub)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with score tables and prioritized findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends the audit report to a notes file when the host agent supports file notes.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
