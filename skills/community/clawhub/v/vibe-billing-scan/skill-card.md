## Description:

Scans OpenClaw API logs to identify costly runs, sessions, retry storms, large context windows, and repeated tool calls that may be driving higher API spend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinertx](https://clawhub.ai/user/shinertx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect local API usage data, find high-cost sessions or retry loops, and understand where API spend is concentrated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned remote commands against sensitive billing and log data.

Mitigation: Use a pinned, reviewed version of the billing package and run it in a restricted local environment before sharing or acting on results.

Risk: The optional setup command may install or configure a monitoring proxy whose changes are underdocumented in the artifact.

Mitigation: Do not enable proxy setup unless the publisher documents what it changes, what data it observes, and how to disable or uninstall it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shinertx/skills/vibe-billing-scan)
- [Vibe Billing landing page](https://api.jockeyvc.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and scan interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional setup guidance for ongoing monitoring; scan results depend on local OpenClaw logs and API proxy data.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
