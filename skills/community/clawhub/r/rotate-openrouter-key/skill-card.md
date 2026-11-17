## Description:

Safely rotates OpenRouter API keys across OpenClaw config files by locating stored keys, updating .env and JSON configs, restarting the gateway, and verifying the new key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to rotate OpenRouter credentials in OpenClaw installations, avoid priority-chain mistakes across .env and JSON config files, and verify the replacement key before disabling the old one.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenRouter API keys may be exposed through command lines, chat logs, terminal output, or script output.

Mitigation: Use dry-run first, avoid pasting live keys into chat or reusable command history, and redact any reported key values.

Risk: Timestamped backups may retain plaintext copies of old keys after rotation.

Mitigation: Review and remove .bak files after rollback is no longer needed, and keep OpenClaw config paths owner-readable only.

Risk: Gateway restarts and SSH-based remote updates can affect running services or other machines.

Mitigation: Treat each restart or remote update as a separate user-approved maintenance action.

## Reference(s):

- [Changing OpenRouter API Key for an Existing OpenClaw Installation](references/key-rotation-guide.md)
- [OpenRouter Key Management](https://openrouter.ai/keys)
- [OpenRouter Key Authentication Endpoint](https://openrouter.ai/api/v1/auth/key)
- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/skills/rotate-openrouter-key)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and modify OpenClaw credential files, create timestamped backups, verify keys through the OpenRouter API, and propose gateway restart commands.]

## Skill Version(s):

1.0.0 (source: skill.yml, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
