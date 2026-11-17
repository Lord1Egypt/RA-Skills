## Description:

Helps agents access Sentry issues, events, projects, teams, and releases through a managed connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect Sentry errors and events and, with approval, manage projects, issues, teams, releases, and related automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sentry access is routed through Maton, with authentication stored in the operating system's credential store.

Mitigation: Confirm this access path before installation and do not expose stored credentials.

Risk: Broad Sentry permissions or unintended changes may affect connected resources.

Mitigation: Use the narrowest available scopes, prefer read-only actions, and explicitly approve each write or delete.

Risk: Hosted functions, triggers, and destinations can run actions or forward data automatically.

Mitigation: Separately approve each automation or forwarding rule and review its target and effect.

## Reference(s):

- [Sentry skill release](https://clawhub.ai/byungkyu/skills/sentry-api)
- [Maton homepage](https://maton.ai)
- [Sentry API documentation](https://docs.sentry.io/api/)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only access by default; changes and automation require user approval.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
