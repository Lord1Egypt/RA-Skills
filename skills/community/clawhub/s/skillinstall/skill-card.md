## Description:

Install OpenClaw skills from clawhub.ai ZIP files with automatic detection, validation, duplicate checking, and Gateway updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otho2966-ai](https://clawhub.ai/user/otho2966-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to install downloaded ClawHub skill ZIP files, list installed skills, and update the local Gateway after installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer writes ZIP contents into persistent OpenClaw skill directories with weak validation and unsafe filesystem handling.

Mitigation: Use only trusted skill archives and fix the installer to validate package metadata, constrain install paths to the skills directory, use a private temporary directory, and reject symlinks and traversal.

Risk: Automatic Gateway restart can apply newly installed skill behavior immediately.

Mitigation: Make Gateway restart an explicit opt-in step and review installed files before activating the skill.

Risk: Running the installer with elevated privileges increases the impact of unsafe archive handling or destructive commands.

Mitigation: Do not run the installer with elevated privileges, and avoid wildcarded rm -rf reinstall commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/otho2966-ai/skills/skillinstall)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown instructions with inline shell commands and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and write access to the local OpenClaw skills directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
