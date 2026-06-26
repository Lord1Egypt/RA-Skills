## Description: <br>
Aggregates configured RSS and web news sources, filters them by keyword categories, generates a daily Markdown digest, and can post the digest to Feishu. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and developers use this skill to monitor configured news sources, group matching items by topic keywords, and prepare a concise daily briefing for review or Feishu delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured source URLs may include private or sensitive sources, and generated digests can be sent to the configured Feishu conversation. <br>
Mitigation: Keep private or intranet sources out of the source list unless sharing their headlines is intentional, and use a dedicated Feishu bot token with minimal chat access. <br>
Risk: The scheduler can run recurring fetch, digest, and push operations automatically. <br>
Mitigation: Enable the scheduler only when recurring delivery is intended, and review the configured cron expression and destination chat before running it. <br>
Risk: The skill fetches external RSS feeds and web pages from every URL listed in config.json. <br>
Mitigation: Use source lists that comply with each site's terms and crawling rules, and keep fetch intervals conservative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/quannwang-news-aggregator) <br>
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown daily digest, JSON news data files, and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can post the digest to a configured Feishu conversation; local history is stored to avoid repeat daily pushes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json, and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
