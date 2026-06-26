## Description: <br>
A股个股十书全景分析法 v2.0，基于十本经典投资书籍的多维度分析框架，自动分类（A/B/C/D型）后选择对应分析路径。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w5208111111](https://clawhub.ai/user/w5208111111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to analyze A-share stocks by supplying a stock name and code, with optional cutoff dates for timeline-constrained backtesting. The skill produces company classification, market and financial data review, book-framework analysis, ratings, and concrete operation suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock names, stock codes, cutoff dates, and related search terms may be sent to third-party finance sites or search providers. <br>
Mitigation: Review queries before use and avoid submitting confidential portfolio, account, or personal information. <br>
Risk: Buy, hold, avoid, price-range, and position-size outputs may be incorrect, stale, or misleading. <br>
Mitigation: Treat outputs as informational analysis only and independently verify market data and financial conclusions before making investment decisions. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/w5208111111/stock-tenbook-analysis) <br>
- [Standard Output Template](references/output-template.md) <br>
- [Ten Book Analysis Notes](references/tenbook-analysis.md) <br>
- [Type-C Framework](references/type-c-framework.md) <br>
- [Tencent market quote endpoint](https://qt.gtimg.cn/q=sz002602) <br>
- [Tencent 52-week K-line endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=CODE,day,START,END,300,,) <br>
- [Sina financial indicators page](https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/CODE/ctrl/YEAR/displaytype/4.phtml) <br>
- [Zhiliaocaibao PE percentile page](https://www.zhiliaocaibao.com/gz_pe/CODE_名称_9/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown with tables, ratings, and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes stock classification, data tables, risk flags, price ranges, position sizing, and a financial-risk disclaimer.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
