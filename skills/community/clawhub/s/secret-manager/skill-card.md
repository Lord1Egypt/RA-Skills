## Description:

Manage API keys securely via GNOME Keyring and inject them into OpenClaw config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jswortz](https://clawhub.ai/user/jswortz)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to store supported API keys in GNOME Keyring, update OpenClaw authentication configuration, and refresh the gateway service after secret changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secrets can be supplied as command arguments, which may expose them through shell history or process listings.

Mitigation: Prefer the interactive prompt or stdin entry paths for secret values.

Risk: A configurable SECRETS_ENV_FILE can be sourced during execution.

Mitigation: Use SECRETS_ENV_FILE only when the file is controlled, audited, and protected by appropriate filesystem permissions.

Risk: The script modifies OpenClaw configuration and restarts or force-stops gateway processes.

Mitigation: Review the target OpenClaw paths and service names before installing or running it, and run it in an environment where gateway restarts are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jswortz/skills/secret-manager)
- [Skill homepage](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands and CLI usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires secret-tool, systemctl, and python3; installs or runs secret-manager.sh for OpenClaw secret management.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
