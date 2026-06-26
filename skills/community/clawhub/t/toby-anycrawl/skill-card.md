## Description: <br>
Perform web scraping, crawling, and Google search with multi-engine support and structured data extraction via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to scrape URLs, search Google, start and monitor site crawls, and retrieve structured web content through SkillBoss API Hub. It is useful for web research and content extraction workflows where sending queries and crawled content to external providers is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, crawl targets, and retrieved page content may be sent to external API providers. <br>
Mitigation: Do not use the skill with secrets, private internal URLs, regulated data, or confidential documents unless third-party sharing has been approved. <br>
Risk: The skill requires a SkillBoss API key for external service access. <br>
Mitigation: Store SKILLBOSS_API_KEY in an approved secret store or environment configuration and rotate it if exposure is suspected. <br>
Risk: Scraped web content and search results can be incomplete, outdated, or misleading. <br>
Mitigation: Review and validate retrieved content before relying on it for downstream decisions or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-anycrawl) <br>
- [Publisher profile](https://clawhub.ai/user/tobeyrebecca) <br>
- [SkillBoss](https://skillboss.co) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Images] <br>
**Output Format:** [Structured API results containing search results, crawl job status, and scraped content in requested formats such as markdown, HTML, text, JSON, or screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends requests to SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
