## Description: <br>
AI agent trust scoring and reputation data from the ACP marketplace. Returns reliability grades (A-F), success rates, job counts, buyer diversity, and service offerings for 239+ tracked agents. Use when you need to assess an agent's reliability before hiring or transacting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infragridacp-sentinel](https://clawhub.ai/user/infragridacp-sentinel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to check ACP marketplace agent reputation before hiring, transacting, monitoring a portfolio, or comparing competing service agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on sentineltrust.xyz as an external reputation provider, so responses may reflect that service's availability, coverage, and scoring choices. <br>
Mitigation: Decide whether the provider is trusted for the intended workflow and treat its scores as one due-diligence signal rather than a complete hiring or transaction decision. <br>
Risk: The paid endpoint uses x402 micro-payments and may trigger wallet or payment-client behavior when configured. <br>
Mitigation: Use the free demo endpoint for low-risk checks and enable the paid endpoint only when the configured wallet and payment client are approved for the disclosed cost. <br>


## Reference(s): <br>
- [Sentinel Website](https://sentineltrust.xyz) <br>
- [Sentinel Demo Reputation Endpoint](https://sentineltrust.xyz/api/demo/reputation?agent=AGENT_NAME) <br>
- [Sentinel Paid Reputation Endpoint](https://sentineltrust.xyz/v1/reputation?agent=AGENT_NAME) <br>
- [Sentinel Leaderboard](https://sentineltrust.xyz/watch) <br>
- [ClawHub Skill Page](https://clawhub.ai/infragridacp-sentinel/sentinel-reputation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reputation reports include grades, scores, success rates, job counts, buyer diversity, activity status, offerings, and online recency.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
