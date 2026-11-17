## Description:

Upgrade Guard provides a safe OpenClaw upgrade workflow with pre-flight config checks, automatic backups, post-upgrade migration, and rollback across cautious, openclaw-update, and manual modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w-sss](https://clawhub.ai/user/w-sss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan OpenClaw upgrades, back up configuration, run pre-flight checks, verify health, and recover with rollback steps when an upgrade breaks Gateway startup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Upgrade and restart guidance can affect production OpenClaw configuration and Gateway availability.

Mitigation: Review before installing on machines with production OpenClaw config or credentials, back up configuration first, and verify health before and after restart.

Risk: Using a latest global package install can pull an unexpected OpenClaw version.

Mitigation: Pin an exact OpenClaw version and confirm package provenance before running upgrade commands.

Risk: Backup pruning guidance includes an rm -rf cleanup pipeline.

Mitigation: Use owner-only backup permissions and replace cleanup with path-validated pruning before production use.

## Reference(s):

- [Upgrade Guard on ClawHub](https://clawhub.ai/w-sss/skills/upgrade-guard)
- [Upgrade Guard Chinese Reference](references/zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
