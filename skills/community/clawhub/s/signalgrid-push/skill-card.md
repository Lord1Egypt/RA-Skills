## Description:

Send push notifications to your iOS, Android, and web browser devices using Signalgrid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[signalgridco](https://clawhub.ai/user/signalgridco)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an OpenClaw agent send status, alert, success, warning, or critical push notifications through Signalgrid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires the full OpenClaw tool profile to reach the Signalgrid API.

Mitigation: Install and run it only in environments where enabling the full tool profile is acceptable.

Risk: Notification titles and bodies may contain sensitive personal or business data.

Mitigation: Avoid sending secrets or sensitive data in notification content.

Risk: The script logs raw and parsed command arguments, which can expose notification content.

Mitigation: Remove or disable debug logging before production use.

## Reference(s):

- [Signalgrid Homepage](https://web.signalgrid.co)
- [ClawHub Skill Page](https://clawhub.ai/signalgridco/skills/signalgrid-push)
- [ClawHub Publisher Profile](https://clawhub.ai/user/signalgridco)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples; runtime command returns JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the SIGNALGRID_CLIENT_KEY and SIGNALGRID_CHANNEL environment variables.]

## Skill Version(s):

1.0.35 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
