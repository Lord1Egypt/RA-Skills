## Description: <br>
WaitingForMacGuffin provides Oscar prediction-market intelligence, including live odds, whale activity, price movements, precursor awards, order book depth, and frontrunner changes across 19 Oscar categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonderspot](https://clawhub.ai/user/sonderspot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research Oscar prediction markets, summarize market activity, inspect nominee or category odds, and produce slippage-aware betting simulations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Betting recommendations or portfolio simulations could be mistaken for financial or gambling advice. <br>
Mitigation: Treat outputs as informational research, verify current odds and local gambling rules independently, and do not rely on the skill as financial or gambling advice. <br>
Risk: Prediction-market data can change quickly, making stale odds or whale-activity summaries misleading. <br>
Mitigation: Refresh the public endpoints before making decisions and include the relevant time window or query context when summarizing results. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/sonderspot/waitingformacguffin) <br>
- [WaitingForMacGuffin public data source](https://waitingformacguffin.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with optional curl command examples and summarized API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public read-only HTTP endpoints and requires curl when the agent makes API calls.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
