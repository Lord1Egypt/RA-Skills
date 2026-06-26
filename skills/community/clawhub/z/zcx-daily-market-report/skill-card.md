## Description: <br>
Generate automated daily market reports for Chinese futures markets, including sector performance, top movers, volume and open-interest changes, and formatted end-of-day summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to assemble daily Chinese futures market summaries after the trading day, including market breadth, sector performance, top gainers and losers, abnormal moves, and distribution-ready Markdown or PDF output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches market data through curl from an external finance endpoint, so reports can reflect delayed, unavailable, or malformed quote data. <br>
Mitigation: Review fetched values and report calculations before distribution, especially top movers, open-interest changes, and turnover estimates. <br>
Risk: PDF export depends on optional local tools and may fail or produce formatting differences across environments. <br>
Mitigation: Keep Markdown as the default output and verify generated PDFs when pandoc, wkhtmltopdf, or weasyprint are used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/zcx-daily-market-report) <br>
- [Publisher profile](https://clawhub.ai/user/zhaocaixia888) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [Sina Finance futures quote endpoint](https://hq.sinajs.cn/list=IF0,IC0,IH0,IM0,CU0,AL0,AU0,AG0,I0,RB0,HC0,SC0,LU0,MA0,TA0,SA0,EG0,C0,M0,Y0,P0,SR0,CF0,EC0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with optional shell commands and optional PDF export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses current market quote data when available; PDF export depends on local pandoc, wkhtmltopdf, or weasyprint availability.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
