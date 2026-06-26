## Description: <br>
OpenClaw skill for designing Telegram Bot API workflows and command-driven conversations using direct HTTPS requests (no SDKs). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design Telegram Bot API command workflows, update routing, and operational checklists for bots built with direct HTTPS requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTTPS requests could affect a production Telegram bot if run without review. <br>
Mitigation: Review each request, payload, and target bot before executing it against production. <br>
Risk: Bot tokens can be exposed through logs, shared chats, or copied request examples. <br>
Mitigation: Keep tokens out of logs and shared transcripts, and substitute secrets only in a secure local environment. <br>
Risk: Webhook changes and message deletion are live bot operations. <br>
Mitigation: Confirm webhook targets, secret token usage, and destructive message operations before applying them. <br>


## Reference(s): <br>
- [Telegram Bot API Field Notes](references/telegram-bot-api.md) <br>
- [Telegram Command Playbook](references/telegram-commands-playbook.md) <br>
- [Telegram Request Templates](references/telegram-request-templates.md) <br>
- [Telegram Update Routing](references/telegram-update-routing.md) <br>
- [Telegram Bot API](https://core.telegram.org/bots/api) <br>
- [Telegram Bot FAQ](https://core.telegram.org/bots/faq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON request examples and HTTPS workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plans, templates, and checklists for human review; no automatic execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
