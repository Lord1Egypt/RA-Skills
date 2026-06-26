## Description: <br>
Scans a user-provided cross-market stock watchlist with TradingView data, evaluates technical signals, and writes Markdown reports with optional Excel output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sarahwang94712](https://clawhub.ai/user/sarahwang94712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run scheduled or on-demand technical scans over A-share, Hong Kong, US, and Japan stock watchlists stored in an Obsidian vault. It helps generate daily technical-analysis summaries, signal tables, scores, and report files for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a watchlist CSV and writes report and cache files in user-selected Obsidian vault paths. <br>
Mitigation: Confirm the CSV path and output directory before running, and keep sensitive portfolio amounts out of the watchlist. <br>
Risk: The skill queries TradingView for ticker data and may be run automatically through a user-created cron job. <br>
Mitigation: Use scheduled execution only when intentional, and tune concurrency or delays if data-provider limits or failures appear. <br>
Risk: The setup instructions install Python dependencies for local execution. <br>
Mitigation: Use an isolated virtual environment rather than installing packages into the system Python environment. <br>
Risk: Generated technical-analysis reports may be mistaken for investment advice. <br>
Mitigation: Treat reports as technical-analysis reference material and review results independently before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sarahwang94712/tradingviewscanner) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Sample scan report](artifact/sample_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, optional Excel workbooks, terminal summaries, and setup or run commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a CSV watchlist, queries TradingView through tvDatafeed, writes report and cache files to the configured output directory, and can run in offline demo mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
