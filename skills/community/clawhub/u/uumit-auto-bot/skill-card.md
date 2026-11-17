## Description:

Automatically scans UUMit tasks, matches them to the user's configured skills, submits applications, monitors status, and sends approval notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cx75227-ops](https://clawhub.ai/user/cx75227-ops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation operators use this skill to configure a UUMit API key and matching rules so an agent can scan task listings, apply to matches, monitor status, and notify on approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic matching and application submission can apply to unintended tasks.

Mitigation: Review matching rules and available approval controls before enabling automated operation, and monitor status notifications.

Risk: Configured UUMit API key and billing settings can incur charges under monthly or per-request plans.

Mitigation: Confirm UUMit permissions, billing terms, renewal behavior, and any available limits before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cx75227-ops/skills/uumit-auto-bot)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls, Text]

**Output Format:** [Markdown or text with configuration guidance and status notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a UUMit API key and may trigger paid automated matching and application activity.]

## Skill Version(s):

2.0.0 (source: evidence.release.version and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
