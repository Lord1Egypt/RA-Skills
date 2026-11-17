## Description:

Analyze Claude Code session history to generate self-observation journals, detect goal drift, and surface hidden behavioral patterns. Outputs to Obsidian Vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuiooo1102-droid](https://clawhub.ai/user/yuiooo1102-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to sync local session history into an Obsidian vault and generate short reflection, goal-drift, hidden-pattern, and monthly portrait reports. It is intended for personal analysis of recent conversation history and user-authored notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local Claude session history and recent Obsidian notes, which may contain sensitive personal or work information.

Mitigation: Use a dedicated vault or limited folder when possible, and run the skill only when that local data scope is acceptable.

Risk: Session digests and reflection reports are copied into long-lived vault files where sensitive content may persist.

Mitigation: Review generated Markdown files for secrets or private details, and avoid broad backfills until the stored output scope is understood.

Risk: Installed slash commands can continue syncing and analyzing local history after the initial setup.

Mitigation: Remove the ~/.claude/commands/reflect commands if this behavior is no longer wanted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuiooo1102-droid/skills/session-reflect)
- [Obsidian + Claude Code Codebook](https://www.youtube.com/watch?v=6MBq1paspVU)
- [session-retro](https://github.com/pwarnock/session-retro)
- [continuity](https://clawskills.sh/skills/riley-coyote-continuity)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files in an Obsidian vault, with supporting shell commands and concise guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes session digests and reflection reports; session messages are sanitized, code blocks are replaced, and long messages are capped at 2000 characters.]

## Skill Version(s):

0.2.1 (source: server release metadata; artifact frontmatter lists 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
