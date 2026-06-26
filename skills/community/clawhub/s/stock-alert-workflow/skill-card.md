## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, crypto analysis, periodic performance reports, and earnings surprise alerts with WhatsApp-ready output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to analyze stock and cryptocurrency tickers, manage local portfolio records, generate period returns, and prepare earnings surprise alerts for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores portfolio quantities and cost basis locally. <br>
Mitigation: Install only when local portfolio storage is acceptable, and use update, remove, and delete commands carefully because they change saved records. <br>
Risk: Ticker lookups and alerts rely on external market and news data providers. <br>
Mitigation: Treat results as informational, review data freshness and caveats, and do not use outputs as financial advice. <br>
Risk: Generated WhatsApp-ready alert text may be forwarded outside the local environment. <br>
Mitigation: Review alert content before sending or forwarding it through WhatsApp or another messaging channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/stock-alert-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [CNN Fear & Greed](https://money.cnn.com/data/fear-and-greed/) <br>
- [SEC EDGAR](https://www.sec.gov/edgar) <br>
- [Google News RSS](https://news.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON analysis results, plus WhatsApp-ready alert text and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include buy, hold, or sell signals, portfolio summaries, caveats, analyst rating summaries, and informational disclaimers.] <br>

## Skill Version(s): <br>
5.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
