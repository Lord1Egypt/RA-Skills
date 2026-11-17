## Description:

Monitors ClawHub for skills gaining traction by tracking downloads and stars, alerting when growth or popularity thresholds are exceeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabriel-kaufman](https://clawhub.ai/user/gabriel-kaufman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor ClawHub skill traction, review top movers, and surface surge alerts for skills that may be relevant to their agent profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public ClawHub data over the network.

Mitigation: Install only where outbound requests to ClawHub are acceptable.

Risk: The profile feature stores agent descriptions and keywords in local files.

Mitigation: Do not put secrets, sensitive project details, or private user data in the profile description or keywords.

Risk: The suggested cron entry creates persistent scheduled execution.

Mitigation: Review the cron entry before adding it and remove it when automatic checks are no longer wanted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gabriel-kaufman/skills/skill-traction-notifier)
- [Publisher profile](https://clawhub.ai/user/gabriel-kaufman)
- [ClawHub skills directory](https://clawhub.ai/skills)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON state, configuration, and profile files under ~/.skill-surge-notifier when commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
