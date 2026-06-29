## Description: <br>
Deploy and monetize an agent-built app with SettleMesh OAuth login, a managed database, usage-based billing, and end-user payments in one command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kallee-si](https://clawhub.ai/user/kallee-si) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy an app, add SettleMesh login and a managed database, configure usage-based billing, and support end-user payments. It also guides use of the SettleMesh capability catalog and MCP server for paid service calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide deploy, publish, database, authentication, and billing-related actions that may change an account, project, or paid resources. <br>
Mitigation: Require explicit confirmation before paid, deploy, publish, or destructive actions, and verify the account, project, payer, and affected resources before proceeding. <br>
Risk: Headless use of SETTLE_API_KEY may grant access to SettleMesh account capabilities. <br>
Mitigation: Store SETTLE_API_KEY only in trusted secret storage, avoid exposing it in logs or prompts, and use browser login for local interactive setup when practical. <br>


## Reference(s): <br>
- [SettleMesh Agent Contract](https://settlemesh.io/agent.md) <br>
- [SettleMesh on ClawHub](https://clawhub.ai/kallee-si/settlemesh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and HTTP/API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented command examples for deployment, capability search, tool calls, billing quotes, and account balance checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
