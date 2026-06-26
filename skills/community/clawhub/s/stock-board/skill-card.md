## Description: <br>
Screens A-share limit-up and strong stocks, including ChiNext and STAR Market views, using public market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrBlackerX](https://clawhub.ai/user/MrBlackerX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents can use this skill to run the board command and quickly inspect A-share limit-up, strong-gainer, ChiNext, and STAR Market lists for market screening. Treat results as informational market data, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to eastmoney.com for public stock data, so results depend on third-party availability and response quality. <br>
Mitigation: Allow only the expected public market-data endpoint, handle request failures, and avoid treating unavailable data as a market signal. <br>
Risk: Market output can be incomplete, delayed, or misleading if used as financial advice. <br>
Mitigation: Use the output for informational screening only and verify results with authoritative market data before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MrBlackerX/stock-board) <br>
- [Eastmoney Public Stock Data Endpoint](https://push2.eastmoney.com/api/qt/clist/get) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are limited to the command's supported screening modes and the public data returned at runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
