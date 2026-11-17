## Description:

Maintain separate memory contexts per WhatsApp group and direct message so an agent can recall prior context, decisions, participants, notes, and follow-ups without mixing conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep WhatsApp group and DM memory separated, inject recent context before responding, and log decisions, participants, tasks, preferences, and weekly activity summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores WhatsApp conversation memory on disk, which can include sensitive personal or organizational information.

Mitigation: Avoid logging secrets or unnecessary personal information, define retention and deletion rules, and review stored memory before sharing or backing it up.

Risk: Conversation IDs and memory filenames can affect file paths beyond the intended memory scope.

Mitigation: Allowlist memory filenames and strictly validate or encode conversation IDs before creating, reading, or appending files.

Risk: Recalled memory can influence future agent responses even when it contains stale, incorrect, or hostile content.

Mitigation: Treat recalled memory as untrusted context and verify important facts before using them in responses or decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell functions and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-based memory conventions under an agent workspace and a weekly digest command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
