## Description:

Smarter Task Planner helps an agent create timestamped task folders, plan steps, save checkpoints, recover interrupted work, and track progress for structured analysis, research, information extraction, and document generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hou0515](https://clawhub.ai/user/hou0515)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to organize multi-step work into traceable task directories with persistent progress records and recovery checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent workspace memory and task files, which may retain sensitive task details after use.

Mitigation: Review MEMORY.md, memory, and output files after use, and avoid recording secrets or sensitive content in task summaries.

Risk: Automatic task recovery checks can write or read workspace state from configured script paths.

Mitigation: Enable the heartbeat template only after verifying the script path and confirming the behavior is appropriate for the workspace.

Risk: Untrusted task IDs or step names may lead to unintended file organization or confusing recovery records.

Mitigation: Use trusted, simple task IDs and step names, and inspect generated task directories before continuing long-running work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hou0515/skills/smarter-task-planner)
- [Task Memory Guide](artifact/references/task-memory-guide.md)
- [Workflow Analysis Guide](artifact/references/workflow-analysis.md)
- [Workspace Structure Examples](artifact/references/examples.md)
- [Heartbeat Guide](artifact/templates/HEARTBEAT-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and workspace file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent task memory, task metadata, and output files in the OpenClaw workspace.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
