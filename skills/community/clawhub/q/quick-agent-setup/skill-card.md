## Description:

Configures additional Feishu bot accounts for OpenClaw, binds messages to a selected Agent at the account or group-chat level, backs up configuration, and restarts the gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vimself](https://clawhub.ai/user/vimself)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw developers and workspace operators use this skill to add Feishu bot credentials, choose account-level or group-chat routing, and update local gateway configuration for an Agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu App Secrets are stored in plaintext OpenClaw configuration and backup files.

Mitigation: Protect ~/.openclaw/openclaw.json and backup files, avoid entering real secrets where shell history can capture them, and rotate secrets if exposure is suspected.

Risk: Bot access is broad by default because the skill can use an open DM policy and wildcard allowFrom setting.

Mitigation: Use restrictive DM policies such as pairing or allowlist where possible, and limit enabled accounts or groups to the intended users.

Risk: The skill changes OpenClaw configuration and may restart the gateway automatically.

Mitigation: Run it during an acceptable maintenance window, review the generated binding choices, and use the automatic backup to restore configuration if the change is wrong.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vimself/skills/quick-agent-setup)
- [Publisher profile](https://clawhub.ai/user/vimself)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local OpenClaw configuration, create backups, set session routing scope, and restart the gateway when executed.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
