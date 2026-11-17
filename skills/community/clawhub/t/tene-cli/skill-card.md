## Description:

Local-first encrypted secret management with the tene CLI for agents handling secrets, API keys, credentials, tokens, .env files, environment variables, or commands that need secrets injected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomo-kay](https://clawhub.ai/user/tomo-kay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide an agent through safe local secret management with tene, including initializing vaults, storing secrets without exposing values, migrating from .env files, and running development or deployment commands through `tene run --`.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified remote installation can execute installer code for a tool that manages credentials.

Mitigation: Review before installing and prefer a pinned, verified release or package-manager install instead of `curl | sh`.

Risk: Running installation steps in secret-bearing CI jobs can expose deployment credentials if the installer path is compromised.

Mitigation: Do not run installation steps in CI jobs that already have TENE_MASTER_PASSWORD or deployment secrets; install a pinned, verified binary before secrets are available.

Risk: Self-update commands can replace the credential-handling binary without enough review.

Mitigation: Require explicit user approval before running `tene update`, and prefer `tene update --check` for discovery.

Risk: Plaintext secret inspection commands can leak credentials into chat, logs, or process history.

Mitigation: Use `tene list` for introspection, use encrypted exports for backups, avoid `tene get` in agent sessions, and never pass secret values as CLI arguments.

## Reference(s):

- [Tene homepage](https://tene.sh)
- [Tene installer](https://tene.sh/install.sh)
- [ClawHub skill page](https://clawhub.ai/tomo-kay/skills/tene-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes not printing plaintext secrets, not reading .tene/ contents, and using `tene run --` for secret injection.]

## Skill Version(s):

1.0.3 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
