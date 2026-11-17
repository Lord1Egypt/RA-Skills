## Description:

Guides migration of local OpenClaw sub-agents to a VPS, including file transfer, Discord bot configuration, bindings updates, gateway restarts, and disabling the local account to avoid conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sparkingskin-tech](https://clawhub.ai/user/sparkingskin-tech)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill when moving configured OpenClaw agents such as creative, dev, qa, strategist, or pojun from a local machine to a remote VPS while preserving Discord routing behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration procedure uses password-based root SSH and disables SSH host key checking, which can expose credentials or allow host impersonation.

Mitigation: Use a verified SSH key with a limited account and keep host key verification enabled before transferring files or changing remote configuration.

Risk: Discord bot tokens and VPS secrets may be printed, embedded, or exposed through shell history and process listings.

Mitigation: Handle tokens through a secret manager or protected environment variables, avoid echoing them in commands, and rotate any token that may have been exposed.

Risk: Remote configuration changes and gateway restarts can break agent routing or leave both local and VPS accounts in an inconsistent state.

Mitigation: Back up openclaw.json, perform a dry run with an allowlisted transfer set, verify bindings, and prepare rollback steps before restarting gateways or disabling the local account.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, Python, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes placeholders for VPS credentials, Discord IDs, tokens, agent names, and OpenClaw bindings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
