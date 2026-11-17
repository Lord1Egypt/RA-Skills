## Description:

Fetches quantitative market, financial, fund-flow, stock-code, and opinion data for Chinese stocks and funds, supporting both single-symbol queries and batch pulls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharkpicker](https://clawhub.ai/user/sharkpicker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative finance practitioners use this skill to retrieve A-share market, financial, fund-flow, stock-code, and sentiment-style datasets for analysis workflows and local data pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch modes can write to caller-chosen local paths.

Mitigation: Use the skill only in an isolated project or account and keep the default status_file and data_path values unless the target paths have been reviewed.

Risk: The public_opinion mode may return unlabeled mock data.

Mitigation: Treat public_opinion results as unreliable until the publisher clearly labels or replaces the mock implementation.

Risk: The skill makes outbound requests to AkShare-backed data sources.

Mitigation: Run it only where outbound finance-data requests are expected and acceptable for the workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sharkpicker/skills/quant-trading-skills)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON response objects; batch modes may also write Apache Parquet files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses use success, data, and message fields; batch outputs include summary counts and local partitioned data files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and package.json; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
