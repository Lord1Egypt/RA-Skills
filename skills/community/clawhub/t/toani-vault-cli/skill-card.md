## Description:

Install, configure, and securely operate the Toani Vault CLI for login, health checks, credential metadata reads, and sandbox browser sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toani](https://clawhub.ai/user/toani)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to install and operate the Toani Vault CLI, validate authentication and configuration, inspect credential metadata, and manage remote sandbox browser sessions without exposing plaintext secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a mutable global npm CLI and handles authentication tokens.

Mitigation: Install it only for intended Toani Vault use, trust or review the @toani/vault-cli package, prefer a pinned version when possible, avoid elevated npm installs, and use least-privilege tokens.

Risk: Sandbox workflows can use credential-backed browser actions where accidental disclosure or long-lived sessions would increase exposure.

Mitigation: Inspect page state before secret-backed fill steps, avoid passing secrets to script bindings, prefer safe readback operations after fills, and terminate sandbox sessions when finished.

Risk: CLI command availability may drift across installed versions.

Mitigation: Verify the installed command surface with toani --help and toani --version before relying on command groups or flags.

## Reference(s):

- [Toani Vault CLI source](https://github.com/credbridge/credbridge/tree/main/cli)
- [ClawHub skill page](https://clawhub.ai/toani/skills/toani-vault-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands, environment variable names, JSON-output flags, and safety cautions for credential and sandbox workflows.]

## Skill Version(s):

0.0.21 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
