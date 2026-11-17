## Description:

Tmp Soul Evolver analyzes agent memory files with MiniMax and proposes or applies incremental updates to workspace identity and guidance files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relunctance](https://clawhub.ai/user/relunctance)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review accumulated memory, learnings, and preferences, then maintain files such as SOUL.md, USER.md, IDENTITY.md, MEMORY.md, AGENTS.md, and TOOLS.md. It is suited for scheduled or manual memory review workflows where identity-file changes are inspected before adoption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private memory, learning, or conversation content may be sent to an external MiniMax API during analysis.

Mitigation: Use dry-run only, restrict the workspace and API environment, and do not run it on memory files that may contain secrets or confidential conversations until redaction and endpoint validation are added.

Risk: The scheduled hook can persist model-generated changes into identity or control files without enough approval controls.

Mitigation: Avoid enabling the scheduled hook and require explicit approval for each proposed update before writing to SOUL.md, AGENTS.md, or similar files.

Risk: Generated identity-file updates may introduce incorrect, stale, or unsafe behavioral guidance.

Mitigation: Review proposed diffs before adoption, keep target-file allowlists narrow, and rely on backups for recovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/relunctance/skills/soul-evolver)
- [SoulForge Architecture](references/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text output, Markdown update blocks, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append generated update blocks to workspace identity files; dry-run mode previews changes without writing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
