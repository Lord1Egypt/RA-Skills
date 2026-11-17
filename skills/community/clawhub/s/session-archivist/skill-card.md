## Description:

Use when session files grow too large (>1MB), context compression fails to trigger, or you need to manage long-running session lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangqb666](https://clawhub.ai/user/zhangqb666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of Hermes Agent use this skill to detect oversized session files, archive important content, and trim long-running session history while preserving structured summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite and trim Hermes session files, which may remove conversation history.

Mitigation: Run dry-run first and keep independent backups before enabling automatic trimming.

Risk: The skill can persist session summaries to a memory service when Hindsight is enabled.

Mitigation: Disable Hindsight unless storing summaries in the memory service is explicitly desired.

Risk: The setup script can install a recurring archival task.

Mitigation: Review the scheduled job before enabling it and confirm that the timing fits operational use.

## Reference(s):

- [Hindsight Integration Guide](references/hindsight-integration.md)
- [Structured Summary Template](references/summary-template.md)
- [Hermes Agent Issue 3015](https://github.com/NousResearch/hermes-agent/issues/3015)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local markdown archives, trimmed session files, backups, and optional memory-service entries when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
