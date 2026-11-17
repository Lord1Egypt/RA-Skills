## Description:

Analyzes a single SKU in a specified retail store, covering sales performance, inventory status, clerk contribution, customer mix, and AIoT conversion metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operators, analysts, and store managers use this skill to evaluate one SKU's store-level sales, inventory, clerk performance, customer mix, and AIoT conversion behavior over a selected date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external local API client path that was not included in the reviewed artifact.

Mitigation: Install only in an environment where that API client path is controlled, audited, and part of the reviewed dependency chain.

Risk: The skill can expose SKU sales, clerk performance, AIoT telemetry, customer-segment analytics, and raw backend API responses.

Mitigation: Run only for authorized users and remove, redact, or gate raw_data before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwyang7/skills/retail-sku-store-analysis)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Python function result as structured JSON, with console text summarizing analysis progress and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns status, SKU identity, store identity, analysis period, goods details, core metrics, findings, recommendations, and raw backend response data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
