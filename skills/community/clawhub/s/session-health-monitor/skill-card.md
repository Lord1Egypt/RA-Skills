## Description:

Context window health monitoring for OpenClaw agents: threshold warnings via Telegram, pre-compaction snapshots, and memory rotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assistantheinrich-prog](https://clawhub.ai/user/assistantheinrich-prog)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to monitor OpenClaw session context usage, trigger Telegram threshold warnings, capture key facts before compaction, and rotate local memory snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session summaries can persist sensitive facts, credentials, personal data, or untrusted instructions into long-term memory.

Mitigation: Review snapshot contents before saving and configure operators to exclude secrets, credentials, personal data, and instructions from untrusted sources.

Risk: Temporary status files use shared local temp storage for session-health state.

Mitigation: Use a private per-user state directory or isolate the runtime environment before enabling statusline tracking on shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/assistantheinrich-prog/skills/session-health-monitor)
- [Publisher profile](https://clawhub.ai/user/assistantheinrich-prog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local memory snapshots and temporary session-health state when its scripts are run.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
