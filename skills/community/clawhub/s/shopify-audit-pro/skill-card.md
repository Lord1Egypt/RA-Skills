## Description:

Provides read-only Shopify store audits, reporting, and operational briefs through the Admin GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artificialintelligently](https://clawhub.ai/user/artificialintelligently)

### License/Terms of Use:

MIT

## Use Case:

Shopify merchants and their agents use this skill to review store launch readiness, catalog health, orders, inventory, and sales operations without changing store data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Read access can expose sensitive customer, order, and store data.

Mitigation: Grant only needed read_* scopes, use --redact-pii by default, and exclude customer details from reports.

Risk: Exposed Shopify credentials could allow unauthorized store access.

Mitigation: Use the masked secret store or a mode-600 file; never paste secrets into chat, commands, or logs.

Risk: Bulk exports and audit logs can leave sensitive data on disk.

Mitigation: Protect local files, limit access, and delete exports when no longer needed.

Risk: API-only audits cannot confirm payment, tax, checkout, or other screen-only settings.

Mitigation: Label unchecked items explicitly and verify them in Shopify admin before treating a store as launch-ready.

## Reference(s):

- [Shopify Audit Pro on ClawHub](https://clawhub.ai/artificialintelligently/skills/shopify-audit-pro)
- [GraphQL cookbook](references/graphql-cookbook.md)
- [Audit report template](references/report-template.md)
- [Safety and scopes](references/safety-and-scopes.md)
- [Audit workflows](references/workflows.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown audit reports and briefs; optional JSON or JSONL query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-tagged findings and optional PII redaction; bulk exports are saved locally.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
