## Description:

A methodology-first workspace governance skill for AI agents focused on principles, decision framework, and safe execution patterns instead of fixed directory templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars2003](https://clawhub.ai/user/mars2003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to audit, organize, archive, or initialize workspaces with clear boundaries, dry-run planning, user confirmation, and rollback-oriented execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Platform profiles may allow extension or skill installation and updates beyond the workspace-cleanup purpose.

Mitigation: Review the OpenClaw and Hermes adaptation profiles before installation and require explicit confirmation for extension or skill install/update actions.

Risk: External directory management can expand the operational boundary of workspace cleanup.

Mitigation: Disable external directory management unless the user specifically needs it, and define workspace_root before scanning or changing files.

Risk: Workspace organization can move, archive, or delete user files if applied too broadly.

Mitigation: Use the documented dry-run plan, protected file patterns, immutable directories, explicit confirmation gates, and checkpoint logs before destructive or bulk actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mars2003/skills/workspace-governance)
- [Governance Manual](references/Governance-Manual.md)
- [Chinese Governance Manual](references/治理手册.zh-CN.md)
- [Minimal Governance Run Example](examples/minimal-governance-run.md)
- [Interoperability Capability Matrix](tools/interop-capabilities.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown plans, tables, blocked-status summaries, shell commands, configuration snippets, and JSON-style log records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run plans, pending decisions, checkpoints, rollback references, and governance logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
