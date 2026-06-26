## Description: <br>
Generates a daily 15:30 market brief covering Chinese equity index moves, industry leaders and laggards, bond-market data, and fixed-income-plus product track outlooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wesdaliang](https://clawhub.ai/user/wesdaliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investment analysts and portfolio teams use this skill after the trading session to assemble a Markdown market brief from current market data and fixed-income-plus product-pool references. The output should be treated as informational analysis rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market summaries may be stale, incomplete, or misleading if the agent uses outdated market data or missing local reference files. <br>
Mitigation: Verify current market data and referenced local files before relying on the report's conclusions. <br>
Risk: The generated report can be mistaken for investment advice. <br>
Mitigation: Treat the output as informational analysis, retain explicit risk warnings, and require human review before investment decisions. <br>


## Reference(s): <br>
- [Market Data Query Reference](artifact/references/market_data.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wesdaliang/xqant-daily-market-report) <br>
- [OpenClaw Homepage Metadata](https://clawhub.ai/skills/xqant-daily-market-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown market report with tables, bullet lists, risk warnings, and concise narrative analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses current market data and local product-list references when available; conclusions require human review before investment use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
