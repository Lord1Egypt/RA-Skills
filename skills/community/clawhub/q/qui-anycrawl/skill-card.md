## Description:

Anycrawl provides web scraping, crawling, and Google search with multi-engine support through the SkillBoss API Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search the web, scrape individual pages, start and manage site crawls, and retrieve structured page content for research, data extraction, and automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs, search terms, crawl parameters, extraction prompts, and page content may be sent to SkillBoss/HeyBossAI and downstream scraping providers.

Mitigation: Use the skill only for approved public or non-sensitive content, and avoid private networks, credentials, personal data, or regulated content unless that use is authorized.

Risk: The skill requires SKILLBOSS_API_KEY for remote API access.

Mitigation: Prefer a session-scoped or managed secret instead of storing the key permanently in shell startup files.

## Reference(s):

- [Anycrawl ClawHub skill page](https://clawhub.ai/quincygunter/skills/qui-anycrawl)
- [HeyBossAI API key portal](https://heybossai.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML]

**Output Format:** [Structured API responses containing search results, scraped page content, crawl job metadata, and optional page formats such as markdown, HTML, text, JSON, or screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends requested URLs, search terms, crawl parameters, extraction prompts, and page content to SkillBoss/HeyBossAI and downstream scraping providers.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
