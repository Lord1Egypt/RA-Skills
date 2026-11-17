## Description:

Generate daily or range-based lead summaries from read-only lead data, including broker inventory counts, locality trends, and priority bucket breakdowns for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalgojha](https://clawhub.ai/user/vishalgojha)

### License/Terms of Use:


## Use Case:

Brokerage and operations teams use this skill to summarize read-only lead records across date ranges, locations, record types, urgency levels, and priority buckets. It supports human review and downstream action planning without ingesting new messages or modifying storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could expose or summarize unintended lead records if granted broad data access.

Mitigation: Grant only read-only access to the intended lead data source and constrain requests by date range and permitted record types.

Risk: Users may treat summary output as an executed workflow or outbound report.

Mitigation: Keep the skill limited to validated summary objects; route follow-up actions and external communications to separate reviewed tools.

Risk: Missing read permissions or invalid request shapes could produce incomplete summaries.

Mitigation: Validate requests and outputs against the bundled schemas, return explicit failure reasons, and fail closed when read permissions are absent.

## Reference(s):

- [Summary input schema](references/summary-input.schema.json)
- [Summary output schema](references/summary-output.schema.json)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Validated JSON summary object with concise human-facing error text when validation or permissions fail]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lead summaries include counts, trends, record type breakdowns, priority breakdowns, urgency breakdowns, top localities, and dataset mode when available.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
