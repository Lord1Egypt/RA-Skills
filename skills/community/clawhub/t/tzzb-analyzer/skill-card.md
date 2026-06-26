## Description: <br>
Analyzes Tonghuashun Investment Ledger portfolio, watchlist, and trade data to generate portfolio reports, sector breakdowns, risk monitoring, and threshold alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qcrcherry](https://clawhub.ai/user/qcrcherry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to read a logged-in Tonghuashun/TZZB portfolio session, summarize holdings and trades, generate scheduled market reports, and monitor configurable risk thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses a logged-in Tonghuashun/TZZB browser session. <br>
Mitigation: Use an isolated Chrome profile, keep CHROME_DEBUG_URL bound to a local address, and avoid running it on shared machines. <br>
Risk: Portfolio and trading details are saved locally by default. <br>
Mitigation: Periodically clean the data/ and memory/ directories and avoid storing artifacts in shared or backed-up locations unless that is intended. <br>
Risk: Generated investment recommendations may be incorrect or incomplete. <br>
Mitigation: Review the underlying holdings, market data, and personal risk constraints before taking any trading action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qcrcherry/tzzb-analyzer) <br>
- [Tonghuashun Investment Ledger](https://tzzb.10jqka.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON portfolio data, risk alerts, and command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CHROME_DEBUG_URL to access a browser session and may cache portfolio details under data/ and memory/.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
