## Description: <br>
StockEarning provides an OpenClaw skill suite for querying stock market data, reviewing portfolio performance, and recording stock trades through the StockEarning.cn API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hareluya](https://clawhub.ai/user/hareluya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an AI assistant to StockEarning.cn for stock price lookup, portfolio summaries, position review, and user-confirmed trade or position updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit trade and position updates to the remote StockEarning.cn system. <br>
Mitigation: Review the confirmation checklist and approve write actions only when the symbol, market, quantity, price, fees, and trade date are correct. <br>
Risk: Portfolio and trade details are sent to mystockearning.cn. <br>
Mitigation: Install only when StockEarning.cn is the intended portfolio system of record and use a dedicated API key. <br>
Risk: The local API key grants access to portfolio operations. <br>
Mitigation: Store the API key in the generated local env file with private permissions and avoid sharing it in prompts, logs, or shell history. <br>


## Reference(s): <br>
- [StockEarning Skill Page](https://clawhub.ai/hareluya/secn) <br>
- [StockEarning.cn](https://www.mystockearning.cn) <br>
- [Source Repository](https://github.com/hareluya/stock-earning-cn-skills) <br>
- [Release Notes](https://github.com/hareluya/stock-earning-cn-skills/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown responses with shell command execution and JSON API results summarized for the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STOCK_API_KEY and sends portfolio, market, and trade data to mystockearning.cn.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
