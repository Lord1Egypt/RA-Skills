## Description:

Manage Slack workspaces via the Slack API, including messages, channels, files, reminders, search, and team communication workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external teams use this skill to automate Slack workspace communication and administration from an agent chat after connecting a Slack workspace through ClawLink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and trust an external plugin and hosted OAuth intermediary with broad Slack read, write, file, and admin capabilities.

Mitigation: Review the ClawLink plugin publisher, requested Slack OAuth scopes, and revocation process before installing; use the least-privileged Slack connection suitable for the workspace.

Risk: Slack write and destructive actions can post messages, change channels, upload or delete files, or alter workspace objects.

Mitigation: Require explicit user confirmation for write actions, preview intended changes before execution, and confirm target channels, users, files, and message content.

Risk: Connecting highly sensitive workspaces may expose workspace metadata, users, conversations, files, or audit information through the connected integration.

Mitigation: Avoid connecting highly sensitive workspaces unless the user trusts ClawLink as a credential intermediary and has confirmed how to remove the plugin and revoke Slack access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/slack-workspace)
- [Slack API Documentation](https://api.slack.com/)
- [Slack Web API Reference](https://api.slack.com/methods)
- [Slack Rate Limits](https://api.slack.com/docs/rate-limits)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Slack tool-call instructions, connection checks, previews for write actions, and troubleshooting guidance.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
