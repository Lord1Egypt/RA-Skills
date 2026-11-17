## Description:

A memory-system skill that helps AI assistants manage layered persistent memories, tags, cross-session retrieval, periodic organization, and optional IMA knowledge-base synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taobaoaz](https://clawhub.ai/user/taobaoaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give assistants a persistent, searchable memory structure for cross-session recall, durable notes, and optional IMA synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived memories may be stored on disk and synchronized to IMA.

Mitigation: Use the skill only for memory content suitable for local persistence and possible IMA transmission; keep secrets, credentials, private keys, and confidential project files out of memory content.

Risk: The security guidance says enabled=false should not be relied on as a sync block in the current script.

Mitigation: Treat IMA synchronization as potentially active when configured, and review sync settings and credentials before using synchronization commands.

Risk: The synchronization helper can accept a file path for upload.

Mitigation: Avoid using --file with sensitive paths and review the selected file before syncing it to an external knowledge base.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taobaoaz/skills/yaoyaoya-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, configuration snippets, and memory-file conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory-management guidance and helper-script usage; persistent memory files and IMA synchronization depend on local configuration and user action.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-04-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
