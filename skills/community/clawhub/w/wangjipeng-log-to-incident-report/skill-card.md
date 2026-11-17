## Description:

Converts user-provided error logs into structured incident reports with root cause, impact, timeline, mitigation steps, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and incident responders use this skill to turn pasted logs, stack traces, or system output into a structured incident report for triage and follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logs pasted into the agent context may contain tokens, API keys, personal data, internal hostnames, or customer identifiers.

Mitigation: Redact sensitive values before use and avoid sharing logs that exceed the intended incident-analysis scope.

Risk: Incomplete logs can lead to uncertain root-cause or impact conclusions.

Mitigation: Review the generated incident report against monitoring data and source systems before using it for operational decisions.

Risk: Artifact documentation includes boilerplate read/write mode and API_KEY sections that may not reflect actual runtime needs.

Mitigation: Treat those sections as unverified until the publisher clarifies configuration and workflow requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/wangjipeng-log-to-incident-report)
- [Skill reference index](artifact/references/index.md)
- [MiniMax-AI skills source](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown incident report with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence level, assumptions, and uncertainty statements when logs are incomplete.]

## Skill Version(s):

1.0.0 (source: release evidence; artifact frontmatter and changelog use 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
