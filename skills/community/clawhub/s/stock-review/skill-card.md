## Description: <br>
Provides daily A-share market review with data on top traders, sector limits, fund flows, streaks, sentiment, and next-day strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnxufei-tech](https://clawhub.ai/user/cnxufei-tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Traders, analysts, and market-monitoring agents use this skill to generate an after-market A-share recap covering market movers, sector activity, capital flow, sentiment, and next-day strategy notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled report generation may run at an unwanted time or cadence. <br>
Mitigation: Confirm the daily 16:30 schedule is desired before enabling automatic execution. <br>
Risk: Optional Feishu sharing could send market recap content to an unintended channel or recipient. <br>
Mitigation: Verify the Feishu push target before enabling or distributing generated reports. <br>
Risk: Market recaps and next-day strategy notes can be incomplete or misleading if public data sources are stale or unavailable. <br>
Mitigation: Treat generated strategy notes as review material and confirm important conclusions against current market data before acting. <br>


## Reference(s): <br>
- [ClawHub Stock Review Skill Page](https://clawhub.ai/cnxufei-tech/stock-review) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May be generated manually for an optional YYYY-MM-DD date or on a daily 16:30 schedule after market close.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
