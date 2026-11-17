## Description:

Export and import OpenClaw instances as portable .claw packages for backup, sharing, and migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovelcp](https://clawhub.ai/user/lovelcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to back up, share, migrate, restore, and roll back OpenClaw setups as portable .claw packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive local OpenClaw files and generated export archives.

Mitigation: Review generated .claw packages and exported contents before sharing, and do not rely solely on automatic credential stripping.

Risk: Imported .claw archives can write workspace, configuration, and skill files.

Mitigation: Use dry-run first, import only from trusted senders, and create a separate backup before allowing writes.

Risk: Archives or URLs from untrusted sources may contain unwanted configuration or skill changes.

Mitigation: Avoid importing from arbitrary URLs or unknown senders, and inspect the preview for file changes, skill requirements, and credential placeholders.

## Reference(s):

- [Zhuaxia ClawHub skill page](https://clawhub.ai/lovelcp/skills/zhuaxia)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to inspect local OpenClaw state, create or load .claw archive files, manage backups, and report required credential placeholders.]

## Skill Version(s):

0.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
