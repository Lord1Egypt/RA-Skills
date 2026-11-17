## Description:

Send Live-Activities & Ongoing-Notifications to iOS and Android phones using Signalgrid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[signalgridco](https://clawhub.ai/user/signalgridco)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and developers use this skill to start, update, and end Signalgrid live activities or ongoing phone notifications while jobs such as deployments, backups, imports, or CI runs are in progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Signalgrid credentials and sends notification content and channel metadata to Signalgrid.

Mitigation: Avoid secrets or sensitive incident details in notification titles and bodies, and use revocable scoped credentials when available.

Risk: The skill documentation asks users to enable OpenClaw's unrestricted full tool profile for a narrow notification-sending task.

Mitigation: Prefer a constrained OpenClaw profile or an isolated environment when installing and running the skill.

## Reference(s):

- [Signalgrid website](https://web.signalgrid.co)
- [ClawHub skill page](https://clawhub.ai/signalgridco/skills/signalgrid-activity)
- [ClawHub publisher profile](https://clawhub.ai/user/signalgridco)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, JSON]

**Output Format:** [Markdown with inline bash examples and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and SIGNALGRID_CLIENT_KEY and SIGNALGRID_CHANNEL environment variables; sends activity title, body, severity, progress, and channel metadata to Signalgrid.]

## Skill Version(s):

1.0.16 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
