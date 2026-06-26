## Description: <br>
TickHub helps agents retrieve real-time quote data for A-share, Hong Kong, and U.S. stocks, including current price, percentage change, and volume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oct16](https://clawhub.ai/user/oct16) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up public real-time stock quote information from a ticker symbol or company name. It is intended for quick price and market movement checks, not historical analysis, technical indicators, or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols, company names, or market lookup queries may be sent to the endpoint used by the skill. <br>
Mitigation: Use the skill only for public market-data lookups and avoid sending brokerage credentials, private portfolio details, trading instructions, or other sensitive financial information. <br>
Risk: Real-time quote responses can be incomplete, delayed, unavailable, or unsuitable as a basis for trading decisions. <br>
Mitigation: Treat returned prices as informational market data and verify important financial decisions with authoritative market-data sources or qualified advisors. <br>


## Reference(s): <br>
- [TickHub ClawHub listing](https://clawhub.ai/oct16/tickhub) <br>
- [TickHub stock quote endpoint example](https://tickhub.net/stock/600519) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with stock quote values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns public market quote fields such as current price, percentage change, and volume.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
