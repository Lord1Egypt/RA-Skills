## Description: <br>
Analyze and clean up OpenClaw session storage files. Use when the user wants to manage session files, clean up old sessions, delete cron/heartbeat, or organize session storage. Triggers on phrases like "clean up sessions", "delete old sessions", "manage session storage", "remove cron sessions", "session cleanup". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[denq04](https://clawhub.ai/user/denq04) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to inspect, categorize, and clean local session storage while protecting the current active session and preserving important chat records unless explicitly confirmed for deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remove local conversation history when cleanup actions are confirmed. <br>
Mitigation: Review the listed files and categories before confirming deletion, avoid broad cleanup unless intended, and back up sessions that may contain important records. <br>
Risk: The current active session or most recent chat session could be selected unintentionally during cleanup. <br>
Mitigation: Keep the current session excluded from bulk deletion and require separate explicit confirmation before deleting it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/denq04/session-storage-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with session summaries and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deletion steps require explicit user confirmation before file removal.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
