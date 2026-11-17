## Description:

Monitors ClawHub for skills gaining traction by tracking download and star growth, alerts on surges based on configurable thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabriel-kaufman](https://clawhub.ai/user/gabriel-kaufman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor public ClawHub skill metrics, detect download or star surges, and prioritize relevant skill changes for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled use periodically contacts ClawHub and writes state, configuration, profile data, and optional logs to local paths.

Mitigation: Run it only in approved environments, configure storage paths deliberately, and review scheduled logs according to your retention needs.

Risk: Profile descriptions and keywords may contain sensitive agent or organizational details if supplied by the user.

Mitigation: Keep secrets and sensitive internal agent details out of profile text and keywords.

## Reference(s):

- [Hot Skills on ClawHub](https://clawhub.ai/gabriel-kaufman/skills/trending-skill-identifier)
- [ClawHub Skills Directory](https://clawhub.ai/skills)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text CLI output with markdown-compatible examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces surge alerts, top-mover summaries, relevance scores, and status or configuration summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
