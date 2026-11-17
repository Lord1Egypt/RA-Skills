## Description:

Provides web scraping, website crawling, Google search, and search-plus-scrape helpers through the SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to retrieve web page content, run Google searches, crawl sites asynchronously, and extract structured data for downstream agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs, search queries, extraction prompts or schemas, crawl targets, and optional proxy settings are sent to SkillBoss and may involve downstream scraping providers.

Mitigation: Avoid submitting secrets, internal-only URLs, regulated data, or credential-bearing proxy URLs unless approved for the deployment environment.

Risk: Persisting SKILLBOSS_API_KEY in shell profile files can leave credentials broadly available on the local system.

Mitigation: Use OpenClaw configuration or a secret manager when API keys should not be stored in shell startup files.

## Reference(s):

- [SkillBoss API Docs](https://skillboss.co/docs)
- [SkillBoss Website](https://skillboss.co)
- [ClawHub Skill Page](https://clawhub.ai/tobeyrebecca/skills/toby-anycrawl)
- [Publisher Profile](https://clawhub.ai/user/tobeyrebecca)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, screenshots, search results, crawl job data]

**Output Format:** [Structured JavaScript objects returned from SkillBoss API responses, including scraped content, search result arrays, crawl job metadata, or paginated crawl results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends requested URLs, search queries, extraction options, crawl settings, and optional proxy settings to SkillBoss.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
