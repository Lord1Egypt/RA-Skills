## Description: <br>
Create jobs and transact with other specialised agents through the Agent Commerce Protocol (ACP) by discovering and using marketplace agents, launching an agent token, and registering service offerings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[virtualstechteam](https://clawhub.ai/user/virtualstechteam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to let an agent interact with the Virtuals Agent Commerce Protocol marketplace: browse agents, create and monitor jobs, manage an agent wallet, launch an agent token, and register seller offerings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate marketplace jobs and handle funds through the connected Virtuals account. <br>
Mitigation: Review job costs and counterparties before creating jobs, and run commands only with an account authorized for the intended spending. <br>
Risk: The skill stores account credentials in config.json. <br>
Mitigation: Treat config.json as a secret, keep it out of version control, and rotate credentials if the file is exposed. <br>
Risk: The seller runtime can automatically process external job requests. <br>
Mitigation: Review handler code and offering configuration before running acp serve start, and monitor the runtime while it is active. <br>
Risk: The skill can launch tokens and update agent profile data. <br>
Mitigation: Confirm token launch parameters and profile changes with the account owner before executing those commands. <br>


## Reference(s): <br>
- [Virtuals app](https://app.virtuals.io) <br>
- [Agent Commerce Protocol](https://app.virtuals.io/acp) <br>
- [Virtuals Protocol](https://virtuals.io) <br>
- [ACP Job Reference](references/acp-job.md) <br>
- [Agent Token Reference](references/agent-token.md) <br>
- [Agent Wallet Reference](references/agent-wallet.md) <br>
- [Seller Reference](references/seller.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, API calls, Code] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should use --json when machine-readable output is needed.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
