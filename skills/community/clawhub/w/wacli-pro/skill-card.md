## Description: <br>
Professional WhatsApp messaging via the wacli CLI. Use when the user wants the agent to message another person from their personal WhatsApp account, search chat history before replying, draft more human-sounding messages, manage follow-ups, or send files with concise professional tone instead of robotic AI phrasing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prantikmedhi](https://clawhub.ai/user/prantikmedhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agents use this skill to draft, review, and send WhatsApp messages or files through the user's personal WhatsApp account with context-aware tone and recipient confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read relevant WhatsApp chat history and send messages or files through the user's account. <br>
Mitigation: Keep recipient lookup and history review scoped to the task, minimize personal data exposure, and require the user to verify the exact recipient, message text, and attachment before approving sends. <br>
Risk: The skill depends on a separate wacli CLI authenticated to the user's WhatsApp identity. <br>
Mitigation: Install only a trusted wacli setup, run wacli doctor when troubleshooting, and avoid using wacli for the user's direct chat with OpenClaw. <br>


## Reference(s): <br>
- [Message patterns](references/message-patterns.md) <br>
- [History workflow](references/history-workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/prantikmedhi/wacli-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and drafted message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation for recipient, final message text, and attachment before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
