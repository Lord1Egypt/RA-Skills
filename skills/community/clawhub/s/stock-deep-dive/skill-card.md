## Description: <br>
Stock Deep Dive gathers ticker-level stock research signals, valuation summaries, conviction scoring, and concise report output for investor research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cplog](https://clawhub.ai/user/cplog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run ticker-level deep dives that combine stock analysis, fundamentals, dividends, valuation, investor-panel scoring, and report-style summaries. Outputs are intended for informational investment research, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X social scanning may require reused browser session tokens and can expose broad environment secrets to an external CLI. <br>
Mitigation: Avoid enabling Twitter/X scanning on a primary account; if used, protect .env like a password, never commit it, prefer a dedicated low-risk account, and review the external CLI before granting credentials or Full Disk Access. <br>
Risk: The skill depends on external finance and news sources and may store portfolio data locally. <br>
Mitigation: Install only if comfortable with those sources and local portfolio storage, and review generated research before using it in a decision workflow. <br>
Risk: Investment research output can be incomplete, delayed, or misleading if treated as financial advice. <br>
Mitigation: Use the output for informational research only and consult a licensed financial advisor before making investment decisions. <br>


## Reference(s): <br>
- [Stock Deep Dive ClawHub Page](https://clawhub.ai/cplog/stock-deep-dive) <br>
- [Publisher Profile](https://clawhub.ai/user/cplog) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Credits](artifact/references/CREDITS.md) <br>
- [Stock Analysis Usage](artifact/stock-analysis/docs/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style research summary with supporting JSON and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ticker analysis, conviction scoring, DCF/comparable valuation notes, risk notes, saved report metadata, and links when deployment steps are available.] <br>

## Skill Version(s): <br>
1.3.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
