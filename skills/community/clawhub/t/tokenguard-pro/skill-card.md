## Description:

Token cost optimizer for OpenClaw agents that scans usage patterns, identifies waste such as excessive context, repeated queries, and inefficient tool use, and provides actionable recommendations to reduce AI costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sammy-the-bot](https://clawhub.ai/user/sammy-the-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and teams running OpenClaw agents use this skill to analyze historical token usage, identify cost waste, and generate optimization guidance for high-volume API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed release artifact does not include the advertised tokenguard-analyze implementation, so the behavior of the installable command could not be verified from the provided files.

Mitigation: Install only from a verified, pinned ClawHub release and review the executable implementation before running it.

Risk: The skill is intended to analyze OpenClaw logs, which may contain secrets, prompts, private data, or commercially sensitive usage details.

Mitigation: Run it only on sanitized logs or in a controlled local environment until clear data-handling guarantees are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sammy-the-bot/skills/tokenguard-pro)
- [Publisher profile](https://clawhub.ai/user/sammy-the-bot)
- [Project homepage](https://github.com/appincubator/tokenguard-pro)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Plain text, Markdown-style reports, or JSON report exports with token-usage findings and optimization recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Historical analysis only; recommendations are advisory and do not automatically modify code or enforce budgets.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
