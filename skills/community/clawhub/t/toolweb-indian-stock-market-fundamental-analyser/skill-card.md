## Description: <br>
AI-powered fundamental analysis for Indian stocks (NSE/BSE) designed for long-term investors seeking data-driven investment insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail investors, financial advisors, portfolio managers, and fintech developers use this skill to request API-based fundamental analysis for NSE/BSE stocks across investment horizons such as 3, 5, or 10 years. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill returns investment analysis and recommendations that may be incorrect, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat results as informational research only, independently verify data and assumptions, and consult qualified financial advice before making investment decisions. <br>
Risk: Stock ticker, company, and investment-horizon queries are sent to an external ToolWeb API. <br>
Mitigation: Use the skill only when sharing those queries with the external API is acceptable for the user's privacy and compliance requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-indian-stock-market-fundamental-analyser) <br>
- [Kong Route](https://api.toolweb.in/tools/indian-stock-fundamental-analyzer) <br>
- [API Docs](https://api.toolweb.in:8204/docs) <br>
- [ToolWeb](https://toolweb.in) <br>
- [RapidAPI publisher profile](https://rapidapi.com/user/mkrishna477) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, text, JSON, guidance] <br>
**Output Format:** [JSON responses and explanatory text describing stock fundamentals, recommendations, risks, and valuation estimates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires stock_ticker and investment_horizon inputs for the POST /analyze endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
