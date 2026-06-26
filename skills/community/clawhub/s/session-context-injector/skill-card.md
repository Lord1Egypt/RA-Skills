## Description: <br>
Reorient a Telegram chat after a session reset by reading a project's STATUS.md and sending a project-specific context injection message through the Telegram Bot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project operators use this skill to restore context in Telegram project rooms, direct messages, and newly created collaborator rooms after a reset or onboarding event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Context may be sent to the wrong Telegram chat if chat_id or room mappings are incorrect. <br>
Mitigation: Confirm each chat_id and project-room mapping before sending context injection messages. <br>
Risk: Project status text may contain sensitive details that would be posted to Telegram or written to local logs. <br>
Mitigation: Keep secrets out of STATUS.md and review resume points and blockers before injection. <br>
Risk: The Telegram bot token can grant unintended sending access if it is over-privileged or exposed. <br>
Mitigation: Use a least-privileged bot token, store it securely, and avoid logging or hardcoding the token. <br>


## Reference(s): <br>
- [Session Context Injector on ClawHub](https://clawhub.ai/nissan/session-context-injector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [HTML-formatted Telegram message text, Markdown log entries, and implementation guidance with Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Messages must fit Telegram's 4096-character limit and use HTML parse mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
