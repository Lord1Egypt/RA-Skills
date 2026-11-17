## Description:

Reports estimated current-session token usage, remaining context, usage percentage, and threshold-based suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to monitor long conversations, estimate remaining context capacity, and decide when to start or compact a session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads current conversation history to estimate aggregate token usage.

Mitigation: Deploy it only where local session-history access is acceptable and aligned with the host platform's permission model.

Risk: Broad command and natural-language triggers may activate when users ask about context or token usage.

Mitigation: Review and narrow trigger phrases if the skill is used in workflows where accidental activation would be disruptive.

Risk: Token counts are estimates and may differ from platform accounting.

Mitigation: Use the output as operational guidance, and rely on platform-reported token usage for billing or hard limit decisions.

Risk: Development dependency versions should be reviewed before using the package in build or CI pipelines.

Mitigation: Refresh and audit the lockfile as part of the normal release or deployment process.

## Reference(s):

- [Spark Context Monitor on ClawHub](https://clawhub.ai/rfdiosuao/skills/spark-context-monitor)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status report with token counts, percentage, progress bar, and suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token counts are estimated from the current session history and model context window.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
