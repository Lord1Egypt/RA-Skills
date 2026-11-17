## Description:

Workspace memory and persona management subroutine that manages user-owned MEMORY.md, SOUL.md, IDENTITY.md, and memory/*.md files to maintain session continuity with configurable confirmations and disabled-by-default auto-triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnjlewis](https://clawhub.ai/user/shawnjlewis)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent persistent workspace memory and persona continuity through controlled reads and writes to memory, soul, and identity files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and persona file changes can alter future agent behavior.

Mitigation: Install only when persistent memory and persona management are intended; keep backups of SOUL.md, IDENTITY.md, and MEMORY.md and review the audit log after use.

Risk: High-autonomy operation can permit automatic future behavior changes and has conflicting approval rules in the security evidence.

Mitigation: Prefer Extreme Safety or Balanced profiles with explicit confirmations, and avoid High Autonomy unless the user accepts automatic behavior changes.

Risk: Workspace file-access restrictions depend on instruction design and host sandbox enforcement.

Mitigation: Run the skill in a host sandbox and keep the allowed file list limited to memory/*.md, MEMORY.md, SOUL.md, and IDENTITY.md.

## Reference(s):

- [Westworld Reverie Configuration Reference](references/config-reference.md)
- [ClawHub release page](https://clawhub.ai/shawnjlewis/skills/westworld-reverie)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance, command responses, configuration snippets, and workspace file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update MEMORY.md, SOUL.md, IDENTITY.md, memory/*.md, and skill_audit.log when permitted by the selected security profile.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
