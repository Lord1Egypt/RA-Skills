## Description: <br>
Agent-facing QQ Mail inbox management over IMAP/SMTP for OpenClaw, Hermes, and other autonomous agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echovic](https://clawhub.ai/user/echovic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to inspect, search, classify, organize, archive, mark, send, and reply to QQ Mail messages while producing dry-run plans before mailbox-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to a QQ Mail mailbox and expose private email metadata or content during mailbox inspection. <br>
Mitigation: Install only when mailbox access is intended, use a dedicated QQ Mail authorization code, and report concise sender, subject, date, count, and category summaries unless the user requests a specific message body. <br>
Risk: Archive, mark, send, reply, and permanent delete operations can mutate mailbox state or send externally visible messages. <br>
Mitigation: Review dry-run JSON or command previews first and require exact user approval before any send, reply, archive, mark, or permanent delete action. <br>
Risk: Broad selectors or personalized cleanup rules can affect more messages than intended. <br>
Mitigation: Validate rule files, prefer narrow selectors, inspect matched counts and proposed actions, and avoid broad delete or archive selectors before applying rules. <br>


## Reference(s): <br>
- [QQMail Organizer ClawHub page](https://clawhub.ai/echovic/qqmail-organizer) <br>
- [QQMail Organizer rules schema](https://github.com/echoVic/qqmail-organizer/rules.schema.json) <br>
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes read-only plans, dry-run previews, mailbox action summaries, and generated rule configuration guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
