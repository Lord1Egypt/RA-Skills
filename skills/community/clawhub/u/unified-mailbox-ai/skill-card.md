## Description: <br>
Unified mailbox AI for both Outlook and Gmail checks unread emails, summarizes new mail with AI, detects meeting invitations, checks calendar conflicts on Outlook and Google Calendar, and sends Telegram notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l1tangdingzhen](https://clawhub.ai/user/l1tangdingzhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who monitor Outlook, Gmail, or both use this skill to detect new unread mail, summarize messages, check meeting-related calendar conflicts, and deliver notifications to Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read configured Outlook and Gmail mailboxes and calendars through OAuth-backed integrations. <br>
Mitigation: Review OAuth scopes before installation, avoid broad write or send permissions where possible, and use only on accounts approved for this monitoring workflow. <br>
Risk: Email summaries and meeting details may be processed by an AI agent and delivered to Telegram. <br>
Mitigation: Use only where external AI processing and Telegram delivery are acceptable for the mailbox and calendar contents. <br>
Risk: Automatic cron execution and shell environment changes can keep mailbox monitoring active beyond a one-time check. <br>
Mitigation: Review cron entries and shell configuration after installation, keep credentials scoped, and disable scheduled monitoring when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/l1tangdingzhen/unified-mailbox-ai) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [outlook-graph ClawHub Skill](https://clawhub.ai/byungkyu/outlook-graph) <br>
- [gog CLI](https://gogcli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [JSON for mailbox checks and concise Markdown/text notification summaries with inline shell commands for setup and operation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sender, subject, brief summary, meeting indication, calendar conflict status, and provider-specific mailbox source.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
