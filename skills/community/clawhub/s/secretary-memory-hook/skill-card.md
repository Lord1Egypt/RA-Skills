## Description:

Automatically runs Secretary Memory scripts around OpenClaw session compaction to create conversation summaries, persist lightweight reply logs, maintain the memory index, and recall prior context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgj24](https://clawhub.ai/user/wgj24)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this hook to automate memory workflows during long-running sessions, including compact-time summarization, context recall, and local memory index maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hook automatically persists parts of assistant replies and may capture sensitive conversation content.

Mitigation: Document logging and retention clearly, obtain user approval before enabling the hook, and provide controls to disable or prune incremental logs.

Risk: The hook runs shell commands using session and filename-derived data.

Mitigation: Replace shell-based execution with argument-safe process APIs and validate or hash session keys before using them in commands or paths.

Risk: The hook automatically moves markdown files and rebuilds local indexes during compaction.

Mitigation: Require explicit user control for file migration and indexing, and limit the operation to the intended memory directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wgj24/skills/secretary-memory-hook)
- [Publisher Profile](https://clawhub.ai/user/wgj24)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, text logs, local command execution, and recalled context for OpenClaw sessions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Automatically appends up to 200 characters of reply content to a daily memory log and invokes local Python memory scripts during session compaction.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
