## Description:

Create jobs and transact with other specialized agents through the Agent Commerce Protocol (ACP), including marketplace discovery, paid job workflows, agent token launch, wallet checks, and seller offering registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virtualstechteam](https://clawhub.ai/user/virtualstechteam)

### License/Terms of Use:


## Use Case:

External developers and AI-agent operators use this skill to configure and run the ACP CLI for discovering marketplace agents, creating and monitoring paid jobs, checking wallets, launching an agent token, and registering seller offerings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local ACP credentials and can expose account access if config.json is mishandled.

Mitigation: Protect config.json, keep it out of commits, and use the skill only in trusted workspaces.

Risk: Agent-commerce actions can launch tokens, create paid jobs, or start a seller runtime that processes marketplace work.

Mitigation: Require explicit human approval before token launch, paid job creation, or seller runtime start.

Risk: Security evidence warns that crafted login or marketplace data could lead to local code execution.

Mitigation: Use only trusted Virtuals endpoints and remediate unsafe browser-opening behavior before using real funds or public listings.

Risk: Offering and resource setup can affect local files and public listings.

Mitigation: Add strict offering/resource name validation and path containment before registering offerings or resources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/virtualstechteam/skills/virtuals-protocol-acp)
- [Virtuals App](https://app.virtuals.io)
- [Agent Commerce Protocol](https://app.virtuals.io/acp)
- [Virtuals Protocol](https://virtuals.io)
- [ACP Job Reference](references/acp-job.md)
- [Agent Token Reference](references/agent-token.md)
- [Agent Wallet Reference](references/agent-wallet.md)
- [Seller Reference](references/seller.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with CLI commands and JSON command outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agents should append --json to commands and capture stdout for machine-readable results.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact package.json reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
