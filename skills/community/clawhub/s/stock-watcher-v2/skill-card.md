## Description: <br>
A-share stock analysis and watchlist notification skill that combines value-investing, technical, and capital-flow checks to produce explicit stock recommendations and scheduled market updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze A-share stocks, compare candidates, generate Markdown reports with buy, sell, hold, target price, stop-loss, and risk notes, and configure scheduled watchlist notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence says the release includes privileged scheduled installation behavior. <br>
Mitigation: Review install.py before running it, avoid root-level cron installation unless intentionally needed, and prefer a user-scoped scheduler where possible. <br>
Risk: Security evidence says the scripts include a hard-coded WeChat recipient that could send portfolio or watchlist data to the wrong account. <br>
Mitigation: Replace the hard-coded USER_ID and verify the destination with a test message before enabling scheduled notifications. <br>
Risk: The skill can generate direct buy, sell, target-price, and stop-loss language for stocks. <br>
Mitigation: Treat outputs as informational analysis, not personalized financial advice, and review all recommendations against current data and the user's risk profile. <br>
Risk: Preset holdings or watchlists may not match the user's portfolio. <br>
Mitigation: Edit or remove preset holdings and watchlists before use, and confirm WATCHLIST.md contents before enabling push tasks. <br>


## Reference(s): <br>
- [Duan Yongping Investment Framework](references/duan-yongping-framework.md) <br>
- [Technical Indicators Guide](references/technical-indicators.md) <br>
- [Eastmoney Field Verification](references/push/field-verification.md) <br>
- [Push Troubleshooting](references/push/troubleshooting.md) <br>
- [Stock Analyst ClawHub Page](https://clawhub.ai/perrykono-debug/stock-watcher-v2) <br>
- [Publisher Profile](https://clawhub.ai/user/perrykono-debug) <br>
- [Eastmoney Quote API](https://push2.eastmoney.com/api/qt/stock/get) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown reports and notification text with optional shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write analysis reports and send scheduled watchlist notifications when configured.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
