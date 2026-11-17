## Description:

Track your AI agent's token usage, API spend, and set soft budget thresholds with in-session warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openauthority](https://clawhub.ai/user/openauthority)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to monitor estimated token usage, API spend, burn rate, and soft daily budget thresholds during OpenClaw sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary questions about spend or token usage may invoke the skill and reveal local usage estimates in the session.

Mitigation: Use the skill in sessions where token and spend estimates are acceptable to display, and avoid invoking it in shared or sensitive contexts.

Risk: Token counts and spend are estimates rather than exact billing records.

Mitigation: Use the skill for operational awareness and confirm final costs in the API provider's billing dashboard.

Risk: Soft thresholds warn the agent but cannot hard-stop execution after a budget is exceeded.

Mitigation: Use external policy or budget enforcement when hard spending limits are required.

Risk: The skill uses a local budget-state file for thresholds and history, and the exact read/write timing should be clarified by the publisher.

Mitigation: Review local state file behavior and permissions before deployment in environments with strict data-handling requirements.

## Reference(s):

- [Token Budget ClawHub listing](https://clawhub.ai/openauthority/skills/token-budget)
- [OpenAuthority publisher profile](https://clawhub.ai/user/openauthority)
- [OpenAuthority plugin for hard budget enforcement](https://github.com/Firma-AI/openauthority)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown text summaries, budget history tables, configuration confirmations, and in-session warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides estimated token and cost reporting with soft threshold warnings; exact billing should be confirmed in the API provider dashboard.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
