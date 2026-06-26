## Description: <br>
Stock Analyst analyzes A-share stocks with value-investing, technical, and capital-flow frameworks, then supports scheduled watchlist notifications for pre-market, close, and next-day review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading workflow operators use this skill to request structured A-share stock analysis, compare candidates, and receive scheduled watchlist or holdings summaries. It is intended to produce concise decision-oriented reports and notification text, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes root-level scheduled execution that can send automatic stock notifications. <br>
Mitigation: Audit the cron and logrotate configuration before installation; remove or disable scheduled jobs if persistent automatic notifications are not desired. <br>
Risk: The notification scripts include hard-coded WeChat recipient and holdings or watchlist defaults. <br>
Mitigation: Replace every USER_ID and holdings or watchlist value before running the scripts, and verify the message target with a controlled test. <br>
Risk: The installer can fetch a remote skill package from a placeholder GitHub URL. <br>
Mitigation: Verify the remote package source before use or avoid the downloader and install only from a reviewed local artifact. <br>
Risk: The skill provides trading recommendations that may be incorrect, incomplete, or unsuitable for a user's circumstances. <br>
Mitigation: Treat outputs as informational analysis, verify market data and assumptions independently, and apply human review before any trading decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perrykono-debug/stock-watcher-v2) <br>
- [Duan Yongping investment framework](references/duan-yongping-framework.md) <br>
- [Technical indicators guide](references/technical-indicators.md) <br>
- [Serenity bottleneck framework](references/serenity-framework.md) <br>
- [Push field verification](references/push/field-verification.md) <br>
- [Push troubleshooting](references/push/troubleshooting.md) <br>
- [Push history](references/push/history.md) <br>
- [Eastmoney quote API](https://push2.eastmoney.com/api/qt/stock/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and notification text with occasional shell commands or configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include stock codes, prices, stop-loss levels, target prices, risk notes, watchlist summaries, and scheduled notification content.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
