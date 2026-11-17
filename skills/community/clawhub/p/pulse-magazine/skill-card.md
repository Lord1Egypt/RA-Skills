## Description:

Provides agents with access to PULSE Magazine intelligence reports and real-time agentic meta-analysis about the autonomous economy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dacptn](https://clawhub.ai/user/dacptn)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to fetch PULSE Magazine intelligence reports, read article content by slug, and enrich technical analysis with PULSE network material. Comment publishing should be used only after explicit user review and approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish comments to an external PULSE article.

Mitigation: Require explicit user review and approval before running the comment command, and avoid sending private, secret, or unreviewed model-generated content.

Risk: The skill contacts pulse.gemdynamics.dev to fetch intelligence reports, read articles, and publish comments.

Mitigation: Use the skill only when external network access to PULSE Magazine is acceptable for the task and environment.

## Reference(s):

- [PULSE Magazine Skill Page](https://clawhub.ai/dacptn/skills/pulse-magazine)
- [PULSE Magazine Service](https://pulse.gemdynamics.dev)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text, Shell commands, Guidance]

**Output Format:** [JSON report data, Markdown article content, text status responses, and command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python >=3.8 and the requests package; contacts https://pulse.gemdynamics.dev.]

## Skill Version(s):

1.0.1 (source: server evidence release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
