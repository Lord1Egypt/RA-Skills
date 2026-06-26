## Description: <br>
Fetch comprehensive stock data from Simplywall.st for stock prices, valuation, financials, dividend, and investment analysis across supported global exchanges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raufimusaddiq](https://clawhub.ai/user/raufimusaddiq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch SimplyWall.st stock data for supported global exchanges when analyzing prices, valuation, financials, dividends, forecasts, and insider activity. Users should verify returned financial data independently before making investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker and exchange lookups are sent to SimplyWall.st. <br>
Mitigation: Use the skill only when sharing the requested ticker and exchange with SimplyWall.st is acceptable. <br>
Risk: Returned stock and financial data comes from a third-party source and may be incomplete, stale, or unsuitable as investment advice. <br>
Mitigation: Verify results against independent financial sources before making investment decisions. <br>
Risk: The skill requires aiohttp at runtime. <br>
Mitigation: Install aiohttp from a trusted package source when the runtime does not already provide it. <br>
Risk: Unsupported or omitted exchange input falls back to the IDX URL pattern. <br>
Mitigation: Provide an explicit supported exchange such as IDX, NASDAQ, NYSE, ASX, LSE, TSX, SGX, TSE, HKSE, or KRX. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raufimusaddiq/stock-data-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/raufimusaddiq) <br>
- [SimplyWall.st](https://simplywall.st) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON stock data returned by the Python skill, with markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ticker input and accepts an optional exchange; no API key is required.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
