## Description:

Audit and harden OpenClaw configurations by checking common security weaknesses, backing up configuration, applying stricter gateway and tool settings, and offering a restore path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sf-dev-systems](https://clawhub.ai/user/sf-dev-systems)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to audit local or LAN-exposed OpenClaw setups, apply stricter configuration defaults, and restore from backups when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes OpenClaw security settings and its restore path can overwrite active configuration from an unvalidated backup.

Mitigation: Use it only in a controlled local environment, make an independent backup first, and inspect the selected backup before running restore.

Risk: The inspected release overstates signed or hash lockfile protections.

Mitigation: Do not rely on the lockfile as tamper-proof protection until the implementation is fixed and independently reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sf-dev-systems/skills/stiff-sec)
- [Publisher profile](https://clawhub.ai/user/sf-dev-systems)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce audit findings, backup and restore instructions, and configuration-hardening guidance for OpenClaw.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
