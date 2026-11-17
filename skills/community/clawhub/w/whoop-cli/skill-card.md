## Description:

Use when operating the installed `whoop` CLI for agent-friendly WHOOP access, cross-platform secret storage checks, daily briefs, summaries, health flags, activity trends, exports, or installing the bundled WHOOP agent skill into `~/.agents`, Codex, OpenClaw, or another agent skill directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreasnlarsen](https://clawhub.ai/user/andreasnlarsen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate the installed WHOOP CLI for account status checks, daily health summaries, activity trend review, data export, and local installation of the bundled agent skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party npm CLI that can access WHOOP account data and sensitive health information.

Mitigation: Install only when comfortable trusting @andreasnlarsen/whoop-cli@0.5.2 with WHOOP access, and prefer read-only operational commands such as summary, day-brief, health, trend, and sync pull.

Risk: Credential handling mistakes could expose long-lived secrets or tokens.

Mitigation: Use local login flows, never paste long-lived secrets into chat, and prefer macOS Keychain or 1Password secret storage.

Risk: The local-vps storage mode is a lower-security fallback.

Mitigation: Use local-vps only with explicit acceptance of its risk and avoid it when Keychain or 1Password storage is available.

Risk: Using --force can write into agent skill directories.

Mitigation: Review the target path and intended overwrite before running forceful skill installation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andreasnlarsen/skills/whoop-cli)
- [whoop-cli homepage](https://github.com/andreasnlarsen/whoop-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes read-only WHOOP commands, local authentication, and secure secret storage.]

## Skill Version(s):

0.5.2 (source: server release metadata and npm install metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
