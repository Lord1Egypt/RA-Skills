## Description:

Sync Obsidian helps Claude Code users save session plans and implementation reports to an Obsidian vault as Markdown notes and Canvas maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chatrichai](https://clawhub.ai/user/chatrichai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code can use this skill to archive project plans and completed implementation work in Obsidian. It is intended for workflows that need durable Markdown notes plus visual Canvas summaries organized by detected project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session plans, implementation summaries, file paths, and technical details may be written into the configured Obsidian vault.

Mitigation: Review generated notes for secrets or confidential content and configure the vault path only for storage locations approved for that information.

Risk: Optional automatic sync rules can persist session content from broad completion cues without a clear per-write confirmation step.

Mitigation: Keep automatic CLAUDE.md sync setup disabled unless the user wants this behavior, or require manual review before each sync.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chatrichai/skills/sync-obsidian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes and Obsidian Canvas JSON files, with setup and path guidance in agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces paired plan or report outputs and writes them under a configured Obsidian vault path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
