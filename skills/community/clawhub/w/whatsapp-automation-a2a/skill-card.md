## Description: <br>
Automate WhatsApp at scale with AI lead discovery, channel broadcasts, bulk messaging, scheduled campaigns, AI replies, review collection, delivery tracking, REST endpoints, MCP tools, and a Python SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-tradequo](https://clawhub.ai/user/alex-tradequo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External business users, agencies, campaign managers, and developers use this skill to plan and operate WhatsApp outreach, lead capture, CRM pipeline updates, AI-assisted replies, review collection, and agent integrations through the MoltFlow API. It is suited for agents that draft or execute user-approved API calls and setup guidance for WhatsApp automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable live WhatsApp messaging, contact extraction, monitoring, exports, scheduled actions, and admin operations against business data. <br>
Mitigation: Use a dedicated least-privilege API key, enable approval mode and phone whitelisting, and review recipients, message text, exports, schedules, webhooks, A2A endpoints, API keys, AI profiles, document indexes, and review collectors before use. <br>
Risk: Bulk or scheduled outreach can send messages to many recipients or run later without immediate operator attention. <br>
Mitigation: Preview campaign audiences and content before starting jobs, keep rate and recipient safeguards enabled, and audit active schedules regularly. <br>
Risk: Group member imports, exports, and review collection may involve personal or customer data. <br>
Mitigation: Import or export group members only with appropriate consent, use scoped credentials, and keep data handling aligned with the organization's privacy requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alex-tradequo/whatsapp-automation-a2a) <br>
- [MoltFlow homepage](https://molt.waiflow.app) <br>
- [AI Agent Integrations](integrations.md) <br>
- [MoltFlow A2A discovery](https://apiv2.waiflow.app/.well-known/agent.json) <br>
- [MoltFlow ERC-8004 agent card](https://molt.waiflow.app/.well-known/erc8004-agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline curl commands, JSON request bodies, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MoltFlow API key or OAuth setup; user review is expected before live WhatsApp messaging, exports, schedules, or admin actions.] <br>

## Skill Version(s): <br>
2.16.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
