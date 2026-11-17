## Description:

Installs and manages Scope-Based Memory and Automated REM Sleep (memory consolidation) for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[john-20-ux](https://clawhub.ai/user/john-20-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reorganize bloated OpenClaw memory into scoped topic files and configure periodic memory consolidation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recurring background memory-consolidation job can rewrite long-term memory without clear approval safeguards.

Mitigation: Run the consolidation on demand or as a dry run that produces a diff before applying changes.

Risk: Memory pruning and topic migration can delete or distort useful long-term rules.

Mitigation: Keep backups of MEMORY.md and memory/topics, then review deletions and new long-term rules before accepting them.

Risk: A scheduled cron entry may continue operating after the user no longer wants automated memory edits.

Mitigation: Document how to list and remove the cron entry before enabling the scheduled job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/john-20-ux/skills/scoped-memory-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/john-20-ux)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create memory topic files, update MEMORY.md, and schedule a recurring cron job.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
