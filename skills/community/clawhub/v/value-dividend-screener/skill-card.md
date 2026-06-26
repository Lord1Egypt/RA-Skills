## Description: <br>
Screen US equities for value and dividend quality using multi-factor scoring across P/E, P/B, dividend yield, and payout sustainability via the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-focused agents use this skill to screen US stock universes or watchlists for undervalued dividend-paying equities, rank candidates by value, income, and financial health factors, and surface dividend sustainability risks. Outputs should be treated as screening information rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key and may use paid-plan or rate-limited API access. <br>
Mitigation: Keep FINSKILLS_API_KEY private, monitor API limits and billing, and avoid exposing credentials in prompts, logs, or shared outputs. <br>
Risk: The skill produces investment screening information that could be mistaken for financial advice. <br>
Mitigation: Review results independently before making investment decisions and present outputs as screening analysis, not recommendations to buy or sell securities. <br>
Risk: Large-universe screening can require many API calls and may return stale or incomplete financial data. <br>
Mitigation: Apply pre-filters, verify key metrics against current sources, and note when data coverage or recency affects confidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/value-dividend-screener) <br>
- [Publisher profile](https://clawhub.ai/user/finskills) <br>
- [Project homepage](https://github.com/finskills/value-dividend-screener) <br>
- [Finskills API](https://finskills.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, analysis, guidance] <br>
**Output Format:** [Markdown with ranked tables, score breakdowns, rationale, and risk flags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY; full S&P 500 screening can involve many API calls and paid-plan API usage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
