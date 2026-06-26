## Description: <br>
Telnyx API integration for Clawdbot. Send SMS/email/WhatsApp messages, manage phone numbers, query call logs, debug webhooks, and access your Telnyx account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamtelnyx](https://clawhub.ai/user/teamtelnyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run Telnyx CLI workflows for messaging, phone number management, call log review, webhook debugging, and account checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Telnyx account in ways that may spend money, send messages, manage phone numbers, retry webhooks, or expose account data. <br>
Mitigation: Require explicit user approval before sending messages, buying or releasing numbers, retrying webhooks, creating or refreshing API keys, or starting upgrade flows. <br>
Risk: Telnyx API keys and exported account data may be exposed through local files, command output, or logs. <br>
Mitigation: Protect the Telnyx API key file, avoid logging account details or secrets, and use secure storage for exported data. <br>
Risk: Messaging workflows can contact unintended or non-consented recipients. <br>
Mitigation: Confirm recipient consent and destination details before bulk or individual message sends. <br>


## Reference(s): <br>
- [Telnyx Docs](https://developers.telnyx.com) <br>
- [Telnyx API Portal](https://portal.telnyx.com/#/app/api-keys) <br>
- [Telnyx CLI](https://github.com/team-telnyx/telnyx-api-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Telnyx CLI table, JSON, and CSV command output formats.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact/CHANGELOG.md, released 2026-02-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
