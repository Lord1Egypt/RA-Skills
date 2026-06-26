## Description: <br>
Personal memo and todo management system. Use when user expresses intent related to remembering, tracking, or managing tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yfsong0709](https://clawhub.ai/user/yfsong0709) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to manage personal todos, reminders, task completion, and accomplishment review through natural conversation. The skill guides an agent to run local shell helpers that update pending and completed Markdown memo files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write to local pending and completed memo files automatically when user intent is interpreted as task management. <br>
Mitigation: Use explicit wording for actions that should be saved, and review the memo files after automated updates. <br>
Risk: Todo entries may contain sensitive information if a user asks the assistant to remember secrets or private data. <br>
Mitigation: Do not store secrets, credentials, tokens, or other sensitive data in memo items. <br>
Risk: The bundled cross-platform test script can delete real pending and completed memo files in an active workspace. <br>
Mitigation: Run the test script only in a disposable workspace or after backing up the memo files. <br>
Risk: Optional cron or shell-profile setup can create persistent daily-summary behavior. <br>
Mitigation: Enable cron or shell-profile configuration only when persistent summaries are deliberately wanted. <br>


## Reference(s): <br>
- [ClawHub yf-memo release page](https://clawhub.ai/yfsong0709/yf-memo) <br>
- [OpenClaw project homepage](https://github.com/openclaw/openclaw) <br>
- [User Guide](references/user-guide.md) <br>
- [Implementation Guide](references/implementation.md) <br>
- [Path Resolution Guide](references/path-resolution.md) <br>
- [Cross-platform Test Script](references/test-cross-platform.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Conversational text with shell commands and Markdown memo-file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local pending, completed, and summary files under the OpenClaw workspace when helper scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
