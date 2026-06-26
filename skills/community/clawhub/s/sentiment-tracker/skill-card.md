## Description: <br>
Monitor brand sentiment, crypto opinions, and product perception across social media with automated tracking, alerts, and multi-entity dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to analyze public sentiment around brands, products, competitors, crypto assets, and topics, then optionally track changes over time with local reports and alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracked entities, alert thresholds, report preferences, historical sentiment data, and monitoring settings can be retained locally for future sessions. <br>
Mitigation: Review and remove data under ~/sentiment-analysis/ when monitoring needs change, and avoid tracking topics that should not be retained in local or agent memory. <br>
Risk: Scheduled monitoring can continue after setup if cron jobs or similar schedules remain active. <br>
Mitigation: Review active cron jobs and disable schedules when monitoring should pause or stop. <br>
Risk: Public web searches and URL fetches send query text or URL requests outside the local machine. <br>
Mitigation: Use non-sensitive search terms and avoid tracking topics whose query text should not be sent to public search or public content services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/sentiment-tracker) <br>
- [Skill homepage](https://clawic.com/skills/sentiment-tracker) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, local markdown tracking files, alert summaries, and optional scheduling instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public web search and fetched public URLs; stores tracking state, reports, and alerts locally under ~/sentiment-analysis/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
