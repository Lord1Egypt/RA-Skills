## Description:

邮件智能处理。使用 AgentMail API 收发邮件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fhbillwer](https://clawhub.ai/user/fhbillwer)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to send and receive email through AgentMail, manage mailboxes, handle attachments, and work with email conversation threads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle private or business email and persist mailbox activity under /workspace/data/emails/.

Mitigation: Before installation, confirm whose AgentMail account and API key it uses, when it may read inbox contents or attachments, whether it asks before sending mail, and how saved email data can be reviewed or deleted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fhbillwer/skills/ws-agent-mail)

## Skill Output:

**Output Type(s):** [guidance, API Calls, Files]

**Output Format:** [Markdown or text responses with email actions and mailbox results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read, send, receive, and persist email data under /workspace/data/emails/ when configured with AgentMail access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
