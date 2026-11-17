## Description:

Helps agents use KeePassXC with Cursor to manage secrets such as passwords, API tokens, and SSH keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theanswerss](https://clawhub.ai/user/theanswerss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to retrieve, add, update, and structure KeePassXC secrets from Cursor-oriented Windows and WSL workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells users to run local helper scripts that handle secrets, but those scripts are not bundled in the artifact.

Mitigation: Review the helper scripts' contents, source, ownership, permissions, and symlink status before running them with real secrets.

Risk: The artifact includes an unsafe example that pipes a literal database password into keepassxc-cli.

Mitigation: Use an interactive prompt or a trusted keyring flow instead of embedding a password in shell history or command output.

Risk: The documented KeePassXC database paths are personal environment paths.

Mitigation: Replace the hardcoded paths with paths that match the user's own Windows or WSL environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/theanswerss/skills/tianchenwei4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include KeePassXC CLI commands, Windows or WSL setup steps, and secret-management workflow guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
