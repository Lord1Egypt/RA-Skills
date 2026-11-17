## Description:

Things plus helps an agent capture, review, schedule, update, delete, and summarize personal tasks in Things 3 through the local things CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sars666](https://clawhub.ai/user/sars666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees can use this skill to let an agent manage their Things 3 task system, including capturing personal commitments, scheduling reminders, organizing projects and tags, producing daily summaries, and cleaning up tasks after verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent Things 3 tasks from broad conversational planning cues without explicit confirmation.

Mitigation: Require confirmation before inferred captures, especially when the user did not explicitly ask to add a Things task.

Risk: The skill reads and modifies the user's local Things 3 database.

Mitigation: Install only for users who accept local task database access, and verify writes with read-back before reporting success.

Risk: The setup flow relies on an unpinned third-party things3-cli Homebrew install.

Mitigation: Pin or review the CLI source and version before broad use.

Risk: Full Disk Access may expose more local data than the skill needs for ordinary task operations.

Mitigation: Avoid granting Full Disk Access unless a specific Things database read fails and the access is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sars666/skills/things-plus)
- [Things Plus Delete-Focused Test Report](artifact/references/report.md)
- [Things Plus Integrated Test Prompt](artifact/references/test_prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON-derived task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform local Things 3 reads and writes; write success should be verified by read-back.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
