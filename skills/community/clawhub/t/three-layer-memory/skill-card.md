## Description:

Three Layer Memory + LanceDB Pro manages hot, warm, and cold OpenClaw memory with LanceDB auto-capture and auto-recall, scheduled synchronization, daily summaries, weekly compaction, scope isolation, deduplication, and archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylin19860916](https://clawhub.ai/user/kylin19860916)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to install a local memory-management routine that captures decisions, generates daily structured summaries, compacts long-term memory, and separates memory by agent scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring local automation can review conversation history and persist or modify long-term agent memory without enough user review controls.

Mitigation: Enable cron, autoCapture, and autoRecall only after adding review or approval before memory updates and guidance-file changes.

Risk: Captured summaries may retain secrets, sensitive personal data, or stale information in local memory files or LanceDB storage.

Mitigation: Define retention and deletion rules, avoid storing secrets or sensitive personal data, and restrict file permissions on the OpenClaw workspace.

Risk: The workflow depends on a separate memory plugin and API-backed retrieval behavior that may affect what gets captured or recalled.

Mitigation: Pin and verify the memory-lancedb-pro plugin before enabling the scheduled scripts.

## Reference(s):

- [AGENTS.md memory rules template](references/agents-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides cron-driven shell scripts that write memory-review tasks and structured summary prompts into the local OpenClaw workspace.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
