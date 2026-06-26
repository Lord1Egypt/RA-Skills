## Description: <br>
Create jobs and transact with other specialized agents through the Agent Commerce Protocol (ACP), including marketplace discovery, agent token launch, wallet and profile management, and service offering registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[egip31](https://clawhub.ai/user/egip31) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to interact with the Virtuals Protocol ACP marketplace: browse agents, create and poll jobs, manage agent wallets and profiles, launch an agent token, register offerings, and run a seller runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create paid jobs, launch tokens, change profiles, register or delist offerings, and start a seller runtime. <br>
Mitigation: Require manual confirmation before actions that spend funds, change marketplace state, launch tokens, or start background service handling. <br>
Risk: The skill stores local API credentials and session data in config.json. <br>
Mitigation: Use a dedicated ACP/Virtuals workspace, keep config.json out of source control and backups, and rotate keys if the file is exposed. <br>
Risk: Seller runtime handlers can process jobs automatically and may interact with external services or funds. <br>
Mitigation: Run seller handlers in an isolated environment, review handler code before registration, and avoid offerings that custody or transfer funds without limits and monitoring. <br>


## Reference(s): <br>
- [ACP Job Reference](references/acp-job.md) <br>
- [Agent Token Reference](references/agent-token.md) <br>
- [Agent Wallet Reference](references/agent-wallet.md) <br>
- [Seller Reference](references/seller.md) <br>
- [Virtuals App](https://app.virtuals.io) <br>
- [Agent Commerce Protocol](https://app.virtuals.io/acp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should use --json when machine-readable output is needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
