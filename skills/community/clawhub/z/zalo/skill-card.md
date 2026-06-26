## Description: <br>
OpenClaw skill for Zalo Bot API workflows (bot token) plus optional guidance on unofficial personal automation tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to plan Zalo Bot API workflows, token setup, webhook or polling routing, message handling, and operational guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bot tokens, webhook secrets, cookies, or session state could be exposed if logged, committed, exported, or stored in untrusted locations. <br>
Mitigation: Keep credentials in a trusted secret store, avoid logging them, rotate compromised tokens, and treat state files and cookies as secrets. <br>
Risk: Unofficial personal-account automation can expose cookie/session material and may create account-policy risks. <br>
Mitigation: Prefer the official Zalo Bot API path; use unofficial personal automation only for low-risk workflows with explicit consent and accepted account risk. <br>


## Reference(s): <br>
- [Bot Messaging Capabilities](references/zalo-bot-messaging-capabilities.md) <br>
- [Zalo Bot Platform Overview](references/zalo-bot-overview.md) <br>
- [Bot Token and Setup](references/zalo-bot-token-and-setup.md) <br>
- [Bot UX Playbook](references/zalo-bot-ux-playbook.md) <br>
- [Webhook and Polling Routing](references/zalo-bot-webhook-routing.md) <br>
- [n8n Automation Notes](references/zalo-n8n-automation.md) <br>
- [Personal Zalo Automation (Unofficial)](references/zalo-personal-zca-js.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with checklists and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow plans, method checklists, and operational guardrails; does not execute API calls directly.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
