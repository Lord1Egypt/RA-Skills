## Description: <br>
Analyzes A-share stocks using volume-price behavior, capital flow, chip structure, margin financing, catalysts, and technical signals to generate stock-picking reports and risk notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mosqu1to3zz](https://clawhub.ai/user/mosqu1to3zz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to structure A-share stock screening, compare candidate equities, and produce pre-market recommendation-style analysis with caveats about uncertainty and non-advisory use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-picking analysis can be wrong, incomplete, or mistaken for financial advice. <br>
Mitigation: Treat outputs as informational analysis only, verify market data independently, and require user or professional review before trading decisions. <br>
Risk: Automated daily runs can repeat stale assumptions or generate recommendations without fresh context. <br>
Mitigation: Review each generated report before use and confirm current market, financing, catalyst, and sentiment data from the referenced sources. <br>
Risk: Generated shell commands or scheduling suggestions may not match the user's environment. <br>
Mitigation: Review commands before execution and run them only in an intended, permissioned environment. <br>


## Reference(s): <br>
- [Datang Power Case Study](references/case-study-datang.md) <br>
- [Ganfeng Lithium Case Study](references/case-study-ganfeng.md) <br>
- [Stock Screening Reference](references/stock-screening.md) <br>
- [Tonghuashun Stock Page Data Source](https://stockpage.10jqka.com.cn/{code}/) <br>
- [Eastmoney Quote Data Source](https://quote.eastmoney.com/sh{code}.html) <br>
- [Xueqiu Stock Page Data Source](https://xueqiu.com/S/SH{code}) <br>
- [ClawHub Skill Page](https://clawhub.ai/mosqu1to3zz/trader-stock-picks) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown analysis reports with tables and optional shell command prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock candidate rankings, scenario analysis, reference operation notes, and explicit risk reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
