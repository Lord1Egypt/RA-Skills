## Description:

Bidirectionally syncs session names between Claude Code CLI/VSCode and cc-connect so Claude Code JSONL titles and cc-connect session names stay consistent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code with cc-connect use this skill to set, compare, synchronize, bind, or register session names across local Claude Code sessions and cc-connect session records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may edit Claude Code and cc-connect session files.

Mitigation: Back up session state files before use and review proposed file changes before allowing writes.

Risk: The skill may restart cc-connect and affect Feishu message handling.

Mitigation: Ask explicitly before any daemon restart and avoid running the restart flow during active Feishu use.

Risk: Unsafe local command execution patterns could mishandle arbitrary or untrusted session names.

Mitigation: Pass session names as data, validate or quote inputs carefully, and avoid running commands with untrusted names.

Risk: Broad daemon and state changes could target the wrong process or stale state.

Mitigation: Verify daemon PIDs and target paths before stopping processes or changing cc-connect state.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhangyanbo2007/skills/session-name-sync)
- [ClawHub publisher profile](https://clawhub.ai/user/zhangyanbo2007)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file edits, state synchronization steps, and daemon restart guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
