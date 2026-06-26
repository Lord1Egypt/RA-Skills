## Description: <br>
Use Social Flow as an agentic control plane for Meta operations via the installed `social` CLI and Gateway API, translating natural language intents into explicit, risk-gated command flows for auth, insights, portfolio, Instagram, WhatsApp, Marketing API, Gateway, and Studio workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalgojha](https://clawhub.ai/user/vishalgojha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and marketing teams use this skill to turn Meta operations requests into scoped Social Flow CLI plans and commands. It is intended for profile-aware workflows across authentication, insights, posting, Instagram, WhatsApp, ads, approvals, and local Gateway or Studio control-plane tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can affect Meta assets, including live ad spend, customer messaging, public content, and production approvals. <br>
Mitigation: Start with read-only checks, verify the active profile, workspace, page, ad account, WhatsApp account, recipients, and budgets, and require explicit confirmation before write or high-risk commands. <br>
Risk: Diagnostics or examples could expose credentials if tokens are copied directly into commands or logs. <br>
Mitigation: Mask secrets, avoid printing full tokens, and prefer secure prompts or Social Flow setup flows for credential entry. <br>
Risk: Gateway or Studio workflows may expose a local control plane if bound broadly or left without access controls. <br>
Mitigation: Keep Gateway or Studio bound to localhost and enable API-key protection when available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vishalgojha/socialclaw-cli) <br>
- [Social Flow Homepage](https://github.com/vishalgojha/social-flow) <br>
- [Social Flow npm Package](https://www.npmjs.com/package/@vishalgojha/social-flow) <br>
- [Command Map](references/command-map.md) <br>
- [Safety and Risk Model](references/safety-and-risk.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Core Workflows](references/workflows-core.md) <br>
- [Marketing and WhatsApp Workflows](references/workflows-marketing-whatsapp.md) <br>
- [Ops, Agent, and Gateway Workflows](references/workflows-ops-agent-gateway.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify assumptions, classify command risk, and request explicit confirmation before write or high-risk execution.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
