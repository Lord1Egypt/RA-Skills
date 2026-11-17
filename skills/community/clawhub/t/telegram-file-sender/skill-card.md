## Description:

Sends local files or notes up to 50 MB to a Telegram user through a configured bot, with path handling and automatic zipping when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daowuu](https://clawhub.ai/user/daowuu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent prepare and send a specified local file, note, or document to a Telegram chat through a configured bot account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload arbitrary local files to Telegram, so using a broad or incorrect path could disclose sensitive content.

Mitigation: Confirm the exact file path, recipient chat ID, and bot account before sending, and use it only with non-sensitive files intentionally selected for upload.

Risk: Temporary-file cleanup and output parsing are part of the workflow and may leave avoidable exposure if not completed or reviewed.

Mitigation: Review script output before the send action and verify cleanup after successful delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daowuu/skills/telegram-file-sender)
- [Skill homepage](https://clawhub.ai/skills/telegram-file-sender)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown instructions with bash commands, key-value script output, and JSON tool payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prepares a temporary file path for Telegram document sending; files over 50 MB are zipped when compression brings them within the limit.]

## Skill Version(s):

1.0.3 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
