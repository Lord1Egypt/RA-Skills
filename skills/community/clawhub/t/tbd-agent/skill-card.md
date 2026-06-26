## Description: <br>
Prediction market for crypto, sports, politics, and culture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coreyjoshuamiller](https://clawhub.ai/user/coreyjoshuamiller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure agents that browse TBD prediction-market campaigns, check USDC balances, and place bets through the TBD CLI or HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help automate real-money USDC prediction-market betting without clear per-bet approval. <br>
Mitigation: Require explicit user approval and hard spending limits before enabling autonomous betting loops. <br>
Risk: API keys may be exposed through logs, shell history, or unsafe automation. <br>
Mitigation: Keep the API key out of logs and shell history, and use a dedicated low-balance account. <br>
Risk: A strategy file can influence betting behavior in ways the user may not expect. <br>
Mitigation: Review the strategy file before running the agent and after any strategy changes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/coreyjoshuamiller/tbd-agent) <br>
- [TBD website](https://tbd.vote) <br>
- [TBD API base URL](https://production-tbd-bets-api.tbd.vote) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, CLI examples, and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes JSON-oriented CLI usage guidance for parseable agent workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
