## Description:

Recognize Intent classifies rewritten natural-language business-intelligence questions and extracts the requested intent, metrics, and dimensions for downstream query handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovenervermore](https://clawhub.ai/user/lovenervermore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business-intelligence workflow builders use this skill to route rewritten user questions into data-query, metadata-query, attribution-analysis, or other intents and to prepare metric and dimension structures for later pipeline steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and query exposure through hard-coded tokens, broad environment loading, or caller-supplied LLM endpoints.

Mitigation: Remove hard-coded tokens, load only an explicit skill-owned configuration file, require HTTPS allowlisted LLM endpoints, and prevent caller-supplied URLs from receiving environment credentials.

Risk: Workflow JSON files can contain user queries, extracted metadata, and SQL-bearing fields.

Mitigation: Treat workflow JSON files as sensitive data, restrict file access, and apply retention and review controls before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovenervermore/skills/recognize-intent)
- [ClawHub publisher profile](https://clawhub.ai/user/lovenervermore)

## Skill Output:

**Output Type(s):** [JSON, text]

**Output Format:** [JSON object containing intent, indicator_metric, metric_info, mode, success, message, and related candidate fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request clarification when confidence is below threshold; standalone mode reads and writes workflow JSON files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
