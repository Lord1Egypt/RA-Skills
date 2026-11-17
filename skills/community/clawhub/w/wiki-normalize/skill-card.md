## Description:

Standardizes Chinese commercial research terms by applying an L1-L5 business taxonomy to assign a hierarchy level, normalized name, sizing metric baseline, and concise reasoning in JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leadleo](https://clawhub.ai/user/leadleo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commercial research data teams use this skill to normalize raw Chinese business terms for taxonomy-backed database ingestion and size-model metric selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is narrowly scoped to Chinese commercial term normalization, so multilingual adaptations may drift from the required JSON fields.

Mitigation: Validate that every response preserves the expected JSON object and field names before using it in downstream systems.

Risk: Incorrect taxonomy level or sizing metric assignments could affect research databases or size-model inputs.

Mitigation: Review normalized results against the L1-L5 taxonomy rules before database ingestion or commercial analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leadleo/skills/wiki-normalize)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns original_name, assigned_level, standardized_name, sizing_metric_baseline, and reasoning.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
