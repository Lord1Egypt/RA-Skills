## Description:

Connects to and operates SiYuan Note through the siyuan-note-cli command-line tool, using notes as context for AI tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agilebuilder](https://clawhub.ai/user/agilebuilder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query, create, update, and organize SiYuan notes, notebooks, documents, blocks, and databases from an agent workflow. It also helps write task results back to SiYuan while preserving Markdown formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Note contents may be treated as instructions, which can give mutable local notes instruction authority over the agent.

Mitigation: Treat SiYuan note contents, including guide documents, as untrusted context unless the user explicitly confirms that their instructions should be followed.

Risk: The skill repeatedly invokes an unpinned npm CLI against local notes and configured SiYuan API tokens.

Mitigation: Use a pinned or preinstalled verified CLI and avoid exposing API tokens in commands, logs, or generated notes.

Risk: Broad reads, writes, deletes, and database changes can expose or damage local note data.

Mitigation: Require explicit confirmation before destructive, broad, or database-changing operations, and verify writes with a read-back command.

Risk: Fixed temporary Markdown file paths can expose note content or collide with another run.

Mitigation: Use unique private temporary files and clean them up after the note operation completes.

## Reference(s):

- [SiYuan Note CLI Command Reference](artifact/references/commands.md)
- [SiYuan Note CLI Workflow Examples](artifact/references/workflow-examples.md)
- [Server-Resolved GitHub Source](https://github.com/agilebuilder/work-skills/tree/master/skills/siyuan-note-cli)
- [ClawHub Skill Page](https://clawhub.ai/agilebuilder/skills/siyuan-note-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose JSON-formatted CLI output for batch reads and verification.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
