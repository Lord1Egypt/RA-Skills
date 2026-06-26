## Description: <br>
Analyzes Taiwan-listed stock monthly revenue data, calculates year-over-year and month-over-month growth, and emits BEAT, MISS, or NEUTRAL signals for a configurable watchlist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyy7263](https://clawhub.ai/user/andyy7263) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and investment workflow operators use this skill after monthly Taiwan stock revenue publication to fetch watchlist revenue data, calculate YoY and MoM changes, and update monitoring or decision pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill description names MOPS, while the script calls the FinMind public API for Taiwan stock monthly revenue data. <br>
Mitigation: Confirm the data source and validate revenue figures against official sources before using generated BEAT/MISS signals in investment or automation workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyy7263/tw-monthly-revenue) <br>
- [MOPS](https://mops.twse.com.tw) <br>
- [FinMind TaiwanStockMonthRevenue API](https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockMonthRevenue) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON revenue analysis with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes period, per-stock revenue metrics, YoY and MoM percentages, cumulative YoY, and BEAT/MISS/NEUTRAL summary signals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
