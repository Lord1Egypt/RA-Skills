## Description:

Tavily Search Pro lets agents use Tavily for web, news, and finance search; URL content extraction; website crawling; sitemap discovery; and deep research with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaharsha](https://clawhub.ai/user/shaharsha)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Tavily-backed searches, extract URL content, crawl or map websites, and generate research reports with citations from a command-line interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries and URLs are sent to Tavily's external service.

Mitigation: Use the skill only with non-sensitive queries and URLs unless external processing has been approved.

Risk: The installer uses an unpinned tavily-python dependency in the shared Python environment.

Mitigation: Install the dependency in an isolated virtual environment and pin tavily-python before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/shaharsha/skills/tavily-search-pro)
- [Tavily application](https://app.tavily.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Plain text, Markdown, or structured JSON from Tavily-backed command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY and supports search, news, finance, extract, crawl, map, and research modes.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
