## Description:

Automatically loads Slack channel context files (e.g., bebops.md, C0AK8SDFS4W.md) into session context for Slack channels and threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hirebrianm](https://clawhub.ai/user/hirebrianm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Slack-based agent users use this skill to automatically load channel-specific Markdown context for Slack channels and threads, including project notes, rules, and recent activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Channel identifiers or names could resolve Markdown files outside the intended Slack context folder.

Mitigation: Install only after strict channel identifier validation and resolved-path containment checks are in place; avoid untrusted channel_id or channel_name values until fixed.

Risk: Automatically injected channel context can expose secrets or sensitive private data to an agent session.

Mitigation: Keep context files free of secrets and sensitive private data, and enable the skill only in Slack channels where automatic context injection is intended.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill before installing and follow the server security guidance for deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hirebrianm/skills/slack-channel-context)
- [Channel context template](references/context-template.md)
- [Example channel context](examples/EXAMPLE_CHANNEL_CONTEXT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown context text with success status and channel metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns empty context when no channel-specific file exists; loaded context may be cached according to configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
