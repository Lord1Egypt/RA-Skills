## Description: <br>
Query real-time stablecoin supply APY from Barker's yield index across 500+ protocols and 20+ CEX, returning ranked APY, TVL, protocol, chain, and asset details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyeweb3](https://clawhub.ai/user/zuoyeweb3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up and compare stablecoin yield opportunities from Barker's public index, including APY, TVL, protocol, chain, and asset details. Results are for informational comparison rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on live public API requests for yield data, so results may change or the endpoint may be unavailable. <br>
Mitigation: State that data is live, handle API failures without inventing yields, and encourage direct verification of any opportunity. <br>
Risk: Users could treat ranked APY results as financial advice. <br>
Mitigation: Present results as informational only and remind users to verify terms, risks, and current rates before moving funds. <br>


## Reference(s): <br>
- [Barker](https://barker.money) <br>
- [Barker Public Stablecoin Yields API](https://api.barker.money/api/public/v1/stablecoin-yields) <br>
- [ClawHub release page](https://clawhub.ai/zuoyeweb3/stablecoin-yield-radar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown table with concise explanatory text and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks yield opportunities and includes Barker attribution; no credentials required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
