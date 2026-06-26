## Description: <br>
Analyze stock market setups with thesis checks, catalyst mapping, risk controls, and explicit trade or no-trade decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill for stock market analysis, watchlist planning, market briefings, and risk-managed trade decision support. It helps convert a ticker thesis into a trade candidate, watchlist candidate, or explicit no-trade decision with triggers, invalidation, and risk controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local planning files may contain sensitive watchlists, risk limits, or financial notes. <br>
Mitigation: Create or modify files under ~/stock-market/ only after user confirmation, and review or delete that directory when those notes should not persist. <br>
Risk: Stock analysis can be mistaken for automatic trade execution or personalized financial advice. <br>
Mitigation: Keep outputs decision-support oriented, require explicit triggers and invalidation levels, preserve no-trade outcomes, and do not connect to brokers or place orders. <br>
Risk: Stale catalysts or watchlist entries can lead to outdated trade plans. <br>
Mitigation: Re-rank watchlists after major market events, log post-action reviews, and remove setups after their catalyst window passes without a valid trigger. <br>


## Reference(s): <br>
- [Stock Market ClawHub page](https://clawhub.ai/ivangdavila/stock-market) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Stock Market homepage](https://clawic.com/skills/stock-market) <br>
- [Analysis Framework](artifact/analysis-framework.md) <br>
- [Risk Playbook](artifact/risk-playbook.md) <br>
- [Setup](artifact/setup.md) <br>
- [Watchlist Template](artifact/watchlist-template.md) <br>
- [Briefing Template](artifact/briefing-template.md) <br>
- [Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and structured planning templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local planning files under ~/stock-market/ after user confirmation; does not place broker orders or execute trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
