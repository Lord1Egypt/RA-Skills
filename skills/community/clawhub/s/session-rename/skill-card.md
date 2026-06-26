## Description: <br>
Helps agents rename OpenClaw chat sessions by using the built-in rename path or, when necessary, a scoped update to the session history store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw instances use this skill to rename chat sessions while limiting changes to the intended session record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A direct history.db update could rename the wrong session if the agent selects the wrong OpenClaw instance or sessionId. <br>
Mitigation: Confirm the target instance and session before writing, prefer the built-in sessions.rename path when available, and read the updated row back after the change. <br>
Risk: Editing the session history database directly could affect local state if the update is malformed. <br>
Mitigation: Back up history.db before direct edits and update only displayName and updatedAt for the selected sessionId. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maverick-software/session-rename) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with inline shell and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include targeted SQLite update examples and verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
