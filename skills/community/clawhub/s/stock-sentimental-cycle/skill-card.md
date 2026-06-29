## Description: <br>
Analyzes A-share market sentiment with seven indicators to score the current cycle stage, detect turning points, and produce a structured review report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuqp](https://clawhub.ai/user/qiuqp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market analysts use this skill to collect or enter A-share market breadth, limit-up/down, turnover, and premium data, then receive a sentiment-stage score, turning-point assessment, and trading-reference report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce market-stage, entry/exit, or position-size suggestions that users could mistake for personalized financial advice. <br>
Mitigation: Use it as research support only, verify data independently, and do not treat outputs as personalized investment advice. <br>
Risk: Reports depend on third-party or manually supplied market data that may be stale, incomplete, or unavailable. <br>
Mitigation: Check data freshness and source reliability, fall back to manual input when APIs fail, and clearly mark missing dimensions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/qiuqp/stock-sentimental-cycle) <br>
- [Eastmoney financial data query endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/query) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Structured Markdown report with scoring tables and trading-reference guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market-stage scores, turning-point signals, position-size suggestions, and caveats based on supplied or third-party market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
