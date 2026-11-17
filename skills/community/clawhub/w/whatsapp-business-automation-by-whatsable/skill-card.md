## Description:

A three-phase Notifyer by WhatsAble agent skill suite for setting up a WhatsApp Business workspace, managing templates, bots, broadcasts, analytics, webhooks, and operating live chat workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsable](https://clawhub.ai/user/whatsable)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to let agents configure and operate Notifyer WhatsApp Business workflows through scripted account setup, automation, broadcasts, analytics, webhooks, and chat actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real WhatsApp messages, schedule broadcasts, and perform destructive delete actions.

Mitigation: Require human review of recipients, schedules, broadcast IDs, template IDs, bot IDs, and webhook IDs before running commands that send or delete data.

Risk: The skill uses account passwords, JWTs, and Developer API keys.

Mitigation: Run commands in a private environment, keep credentials out of shell history, CI logs, and agent transcripts, and treat the Developer API key as a long-lived secret.

Risk: Security evidence flags weak destination validation and high-impact backend deletion risks.

Mitigation: Use only the official Notifyer API base URL, review the skill before installation, and avoid invoking raw backend endpoints outside the provided script safeguards.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whatsable/skills/whatsapp-business-automation-by-whatsable)
- [WhatsAble publisher profile](https://clawhub.ai/user/whatsable)
- [Artifact repository link](https://github.com/Whatsable/whatsapp-business-agent-skills)
- [Notifyer by WhatsAble](https://notifyer-systems.com)
- [Account and authentication reference](artifact/skills/setup-notifyer/references/account-reference.md)
- [Broadcasts API reference](artifact/skills/automate-notifyer/references/broadcasts-reference.md)
- [Messaging reference](artifact/skills/chat-notifyer/references/messaging-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Node.js shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run local Node.js scripts that call Notifyer APIs using user-provided credentials.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
