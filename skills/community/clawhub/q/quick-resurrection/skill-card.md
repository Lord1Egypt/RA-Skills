## Description:

Quick Resurrection packages and restores an OpenClaw Agent workspace, including identity files, team workspaces, skills, configuration, and scheduled tasks, with review and dry-run controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao-zwl](https://clawhub.ai/user/zhao-zwl)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to migrate or rebuild an agent team after moving machines or reinstalling a system. It helps package local agent identity, memory, tool configuration, skills, and scheduled tasks, then restore them into a new environment with review prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration packages can contain private memory, tool configuration, API keys, account details, server addresses, and internal workflow information.

Mitigation: Use dry-run first, inspect the package contents manually, keep the archive private, and encrypt it during transfer.

Risk: Restoring a package can make persistent local changes, including OpenClaw configuration updates, workspace file copies, cron task creation, and gateway restarts.

Mitigation: Review the displayed diff and cron payloads before confirming, prefer --no-cron and --no-restart for an initial run, and confirm that automatic backups were created.

Risk: Packages from other users or untrusted agents may import unwanted configuration, scheduled tasks, or sensitive identity material.

Mitigation: Avoid importing untrusted packages; if trust is uncertain, review the scripts and package contents in an isolated environment before migration.

## Reference(s):

- [Quick Resurrection on ClawHub](https://clawhub.ai/zhao-zwl/skills/quick-resurrection)
- [Publisher profile](https://clawhub.ai/user/zhao-zwl)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Material packing guide](artifact/MATERIAL_PACKING.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated migration package files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and restores local OpenClaw workspace files, agent configuration, and optional scheduled task definitions.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
