## Description:

Track and find unanswered messages using a local file-based inbox. No DB required. Use when asked to find unanswered messages, missed messages, people waiting for a response, or to log a new incoming message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain a lightweight inbox of messages that still need replies, find recent unanswered messages, mark them answered, and clean up old answered records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inbox stores sender details, phone numbers, chat IDs, and message previews in a local plaintext JSON file.

Mitigation: Use restrictive file permissions, keep the file in a controlled workspace, and avoid storing unnecessary message body content.

Risk: Heartbeat or reminder jobs may expose private message previews in logs or alerts.

Mitigation: Avoid logging full message bodies from automated checks and limit previews to the minimum needed for follow-up.

Risk: Concurrent updates to the JSON inbox can overwrite or corrupt message state.

Mitigation: Use file locking or move to a small database if multiple processes may write to the inbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/unanswered-messages)
- [Publisher profile](https://clawhub.ai/user/netanel-abergel)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON structure examples and inline Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file operations and concise message summaries; no external service calls are required by the artifact.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
