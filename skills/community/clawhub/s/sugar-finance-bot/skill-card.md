## Description:

Calculates landed cost and unit economics for food import/export shipments from structured shipment cost data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patttyyywu](https://clawhub.ai/user/patttyyywu)

### License/Terms of Use:

MIT-0

## Use Case:

Supply chain finance, import/export operations, and cost analysis teams use this skill to estimate total landed cost, cost per kilogram, and cost per unit for food shipments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed, missing, non-numeric, zero, or negative shipment quantities and costs can produce misleading calculations or runtime errors.

Mitigation: Validate shipment objects before calculation, including required numeric cost fields and positive net weight and quantity values.

Risk: The landed-cost result is only as reliable as the caller-provided shipment data.

Mitigation: Review source shipment records and customs, freight, insurance, duty, and fee inputs before using results for pricing or margin decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patttyyywu/skills/sugar-finance-bot)
- [Publisher profile](https://clawhub.ai/user/patttyyywu)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Structured calculation results and concise Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on caller-provided shipment quantities and cost fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
