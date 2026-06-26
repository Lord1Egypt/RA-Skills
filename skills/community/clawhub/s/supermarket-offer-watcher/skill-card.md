## Description: <br>
Save a personal grocery product watchlist and check nearby supermarket deals automatically by radius. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukasosterheider](https://clawhub.ai/user/lukasosterheider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain a grocery product watchlist, configure a home location and radius, and receive daily or weekly summaries of validated nearby supermarket offers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an approximate home location and grocery preferences in the workspace. <br>
Mitigation: Use a coarse location when possible, avoid sensitive notes, and review or delete /data/workspace/data/supermarkt-watchlist.json when it is no longer needed. <br>
Risk: Daily or weekly cron checks may run scheduled web searches if enabled. <br>
Mitigation: Enable cron alerts only intentionally and review the configured schedule, timezone, products, and radius before activation. <br>
Risk: Offer search results can be stale, incomplete, or misleading. <br>
Mitigation: Report only deals that satisfy the documented validation checks for product or alias, store, valid date window, and visible price or discount. <br>


## Reference(s): <br>
- [Offer Check Template](references/check-template.md) <br>
- [ClawHub Release Page](https://clawhub.ai/lukasosterheider/supermarket-offer-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and compact alert summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local JSON watchlist at /data/workspace/data/supermarkt-watchlist.json and may guide daily or weekly cron scheduling.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
