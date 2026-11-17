## Description:

Unofficial Bitwarden CLI written in Rust. Manage passwords, TOTP codes, and secure notes from the terminal with a background agent for stateful sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxhoio](https://clawhub.ai/user/sxhoio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and terminal-focused users use this skill to operate rbw for Bitwarden vault access, including passwords, TOTP codes, secure notes, profiles, sync, clipboard use, and SSH agent setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill helps operate rbw against a Bitwarden vault, so generated commands can expose secrets or change vault state.

Mitigation: Review commands before execution, especially get, --raw, --clipboard, add, edit, remove, sync, SSH agent setup, and purge.

Risk: Password and 2FA prompts may fail or block in non-interactive agent sessions.

Mitigation: Use an unlocked rbw agent for non-interactive work or run prompt-requiring commands in a PTY-capable session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxhoio/skills/rbw-bitwarden)
- [rbw homepage](https://github.com/doy/rbw)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers sensitive password-manager workflows and should be reviewed before commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
