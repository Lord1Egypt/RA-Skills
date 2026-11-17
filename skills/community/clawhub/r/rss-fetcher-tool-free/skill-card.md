## Description: <br>
RSS采集器免费版 helps an agent guide personal users through lightweight RSS feed collection, URL-based deduplication, tag extraction, local SQLite storage, and terminal-based article browsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External personal users and developers use this skill to configure RSS sources, fetch articles over the network, store them in a local SQLite archive, and browse or query collected articles by time, category, tag, or SQL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches RSS feeds over the network and stores article data in a local SQLite archive. <br>
Mitigation: Use trusted RSS sources and keep the agent limited to the intended local RSS archive. <br>
Risk: Source management commands can disable or remove configured RSS sources. <br>
Mitigation: Review proposed source-management commands before execution. <br>
Risk: The local archive can be lost or corrupted if the database is deleted, interrupted during writes, or accessed by multiple writers. <br>
Mitigation: Back up data/rss_fetcher.db when the archive matters and avoid simultaneous fetch processes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/rss-fetcher-tool-free) <br>
- [Python](https://python.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown with bash, JSON, SQL, and text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve network RSS fetching and local SQLite storage when executed by the agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
