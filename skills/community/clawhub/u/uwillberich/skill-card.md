## Description: <br>
Build next-session A-share game plans from market structure, overnight macro shocks, policy timing, and watchlist leadership. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangrichao2020](https://clawhub.ai/user/huangrichao2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-focused agents use this skill to turn A-share market structure, policy timing, overnight macro signals, watchlists, and live data checks into a next-session discretionary plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an Eastmoney API key locally and uses it for live finance workflows. <br>
Mitigation: Install only when the user intentionally wants Eastmoney-backed market analysis, keep the key in ~/.uwillberich/runtime.env, and remove it when the workflow is no longer needed. <br>
Risk: The skill queries external finance and news services, so live outputs can be affected by source availability, throttling, or stale data. <br>
Mitigation: Benchmark and verify sources before using a report, and cross-check time-sensitive market or policy facts with primary sources. <br>
Risk: The skill can write reports, alerts, watchlists, JSONL logs, and SQLite-backed state under ~/.uwillberich. <br>
Mitigation: Review generated files periodically and delete the state directory if stored alerts, watchlists, or local reports are no longer wanted. <br>
Risk: The optional news iterator can run as a launchd or nohup background poller. <br>
Mitigation: Enable recurring polling only deliberately, and disable the launchd job or background process when continuous monitoring is not desired. <br>
Risk: The generated A-share game plans may be incomplete or misleading if used as trading advice without review. <br>
Mitigation: Treat outputs as decision-support notes, confirm live market conditions, and apply human review before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huangrichao2020/uwillberich) <br>
- [Project Homepage](https://github.com/huangrichao2020/uwillberich) <br>
- [Methodology](artifact/references/methodology.md) <br>
- [Data Sources](artifact/references/data-sources.md) <br>
- [Opening Window Template](artifact/references/opening-window-template.md) <br>
- [Message Iterator](artifact/references/message-iterator.md) <br>
- [Cross-Cycle Watchlist](artifact/references/cross-cycle-watchlist.md) <br>
- [Event Regime Watchlists](artifact/references/event-regime-watchlists.md) <br>
- [Eastmoney MX Claw Key Application](https://ai.eastmoney.com/mxClaw) <br>
- [Eastmoney AI Official Site](https://ai.eastmoney.com/nlink/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate markdown, JSONL, SQLite-backed state, watchlist overlays, and reports under ~/.uwillberich when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
