## Description:

Use the Ultrahuman MCP to answer questions about sleep, recovery, readiness, daily metrics, morning brief, ring data, glucose, and metabolic health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzafizzl](https://clawhub.ai/user/duzafizzl)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for concise summaries and comparisons of their Ultrahuman sleep, recovery, readiness, activity, ring, and CGM metrics. The skill guides the agent to fetch only relevant daily metrics and present descriptive wellness context without medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad wellness triggers could access sensitive Ultrahuman health data when a user asks an ambiguous sleep or recovery question.

Mitigation: Confirm the intended Ultrahuman account and requested date range for ambiguous requests, then retrieve only the metrics needed to answer the specific question.

Risk: Health metric explanations could be mistaken for medical advice.

Mitigation: Keep interpretations descriptive, use the bundled glossary and interpretation reference for context, and avoid diagnosis, treatment advice, or prescriptive medical targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duzafizzl/skills/ultrahuman-biodata-assistant)
- [Interpreting Ultrahuman metrics](references/interpretation.md)
- [Ultrahuman metrics glossary](references/metrics_glossary.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries, compact metric lists, and short comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Ultrahuman MCP data for requested account/date scopes; avoids raw JSON unless the user asks for export.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
