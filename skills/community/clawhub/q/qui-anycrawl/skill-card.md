## Description: <br>
Provides web scraping, crawling, and Google search through the SkillBoss API for structured data extraction and automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, scrape individual pages, and crawl websites into structured results for research, content extraction, and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs, search terms, crawl targets, and extracted page content are sent to SkillBoss/HeyBossAI and its backend providers. <br>
Mitigation: Use only with targets and content approved for external processing; avoid internal-only sites, secrets, personal data, or regulated content unless that sharing is authorized. <br>
Risk: The skill requires an API key that could be exposed if committed, logged, or synced in shell configuration. <br>
Mitigation: Store the key in approved secret storage or local configuration, prefer scoped or revocable keys when available, and do not commit files containing the key. <br>
Risk: Large searches or crawls can consume external API quota or paid service capacity. <br>
Mitigation: Set conservative crawl depth and page limits, monitor usage, and cancel long-running crawl jobs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Anycrawl page](https://clawhub.ai/quincygunter/qui-anycrawl) <br>
- [HeyBossAI API key and service](https://heybossai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, configuration] <br>
**Output Format:** [JSON objects containing search results, crawl job data, or scraped page content in the requested formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may return asynchronous crawl job identifiers for later status and result retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
