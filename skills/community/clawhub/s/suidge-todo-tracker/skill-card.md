## Description: <br>
Manage follow-up items and remind users during heartbeat checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suidge](https://clawhub.ai/user/suidge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to let an AI agent maintain local todo reminders, check pending follow-ups during heartbeat runs, and clean completed or cancelled items after 24 hours. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo descriptions and context can store sensitive personal or project details in the local reminder file. <br>
Mitigation: Avoid recording secrets, credentials, or sensitive details in todo descriptions or context. <br>
Risk: Casual reminder-related language may cause the agent to create or modify todo entries unexpectedly. <br>
Mitigation: Adjust routing keywords or require confirmation before adding, changing, completing, or cancelling reminders. <br>
Risk: Reminder state persists between sessions until completion, cancellation, or cleanup. <br>
Mitigation: Install only when persistent local reminder tracking is desired and review the todo JSON file during routine maintenance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/suidge/suidge-todo-tracker) <br>
- [README](artifact/README.md) <br>
- [Data Structure](artifact/data-structure.md) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Usage Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON file updates and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists reminder state in a local JSON file when installed.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
