## Description: <br>
Use when working with Sportfolio through its public authenticated MCP endpoint or the repo-local CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelhmiv](https://clawhub.ai/user/michaelhmiv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Sportfolio through MCP or the repo-local CLI, authenticate with a user API token, read account and portfolio data, inspect public docs and resources, and stage confirmation-gated gameplay actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User API tokens can expose account-scoped access if logged, reused broadly, or sent to an unintended endpoint. <br>
Mitigation: Use a dedicated user API token where possible, avoid exposing it in logs or shell history, and verify the Sportfolio endpoint before connecting. <br>
Risk: Gameplay changes such as trades or liquidity actions can affect the user's Sportfolio account if confirmed without review. <br>
Mitigation: Start with read-only checks and review each staged trade or account-change summary before giving explicit confirmation. <br>


## Reference(s): <br>
- [Sportfolio.Market ClawHub listing](https://clawhub.ai/michaelhmiv/sportfolio-market) <br>
- [Sportfolio MCP endpoint](https://www.sportfolio.market/mcp) <br>
- [Sportfolio website](https://www.sportfolio.market) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented CLI examples for machine-readable agent workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
