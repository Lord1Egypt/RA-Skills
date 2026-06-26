## Description: <br>
Financial brain for x402 payments: budget enforcement, cost policies, spend analytics, anomaly detection, and audit trail for autonomous agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Upn-130guthub](https://clawhub.ai/user/Upn-130guthub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and autonomous-agent operators use this skill to route x402 paid API requests through budget checks, payment policy enforcement, spend analytics, anomaly alerts, and an audit ledger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can install or use an unpinned payment package. <br>
Mitigation: Pin and review the x402-cfo npm package version before enabling the skill. <br>
Risk: An agent can automatically spend wallet funds within broad default budget limits. <br>
Mitigation: Use a dedicated low-balance wallet, lower the default hourly, daily, session, and per-request budgets, and configure allowed networks and blocklists. <br>
Risk: The generated ledger can contain payment history and operational details. <br>
Mitigation: Keep the x402-cfo ledger out of source control and review audit records before sharing logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Upn-130guthub/x402-cfo) <br>
- [Publisher profile](https://clawhub.ai/user/Upn-130guthub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to initialize x402-cfo, route paid requests through cfo.fetch(), inspect spend summaries, and react to budget events.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
