## Description:

Structured Vector Memory (SVM) helps an OpenClaw agent maintain layered long-term memory using LanceDB Pro retrieval, scheduled memory summaries, deduplication, scope separation, and archive workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylin19860916](https://clawhub.ai/user/kylin19860916)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users use this skill to set up and operate an OpenClaw memory system that captures decisions, summarizes recent sessions, distills long-term memory, and separates memory by scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled jobs repeatedly inspect conversation history and maintain long-term memory without enough user control.

Mitigation: Run the scripts manually before enabling cron, keep autoCapture and autoRecall disabled until needed, and define retention and deletion procedures.

Risk: The weekly maintenance workflow can update persistent agent memory and control files, including SYSTEM_GUIDE.md.

Mitigation: Require explicit review before allowing updates to control files and keep backups before memory distillation or archive changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kylin19860916/skills/structured-vector-memory)
- [AGENTS.md memory rules template](references/agents-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cron task templates that append memory-maintenance instructions to persistent workspace files.]

## Skill Version(s):

3.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
