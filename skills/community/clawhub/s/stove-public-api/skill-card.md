## Description: <br>
Uses the Stove Protocol Public API to query read-only public market data, including platform statistics, orderbooks, ticker statistics, and ticker heatmaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zschen211](https://clawhub.ai/user/zschen211) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve Stove Protocol public market data through a standard-library Python helper and summarize the returned JSON for platform, ticker, orderbook, and heatmap queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A custom base URL can direct the helper to an arbitrary or untrusted host. <br>
Mitigation: Use the default production endpoint or documented QA endpoint unless intentionally testing a trusted endpoint. <br>


## Reference(s): <br>
- [Stove Public API Skill Page](https://clawhub.ai/zschen211/stove-public-api) <br>
- [Public API](references/Public API.md) <br>
- [Query Platform Statistics](references/Query Platform Statistics.md) <br>
- [Query Ticker Information and Statistics](references/Query Ticker Information and Statistics.md) <br>
- [Query Ticker Orderbook](references/Query Ticker Orderbook.md) <br>
- [Query Ticker Heatmap](references/Query Ticker Heatmap.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON API results and command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public API helper; no credential environment variables detected.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
