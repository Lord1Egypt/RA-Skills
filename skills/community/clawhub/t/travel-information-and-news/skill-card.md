## Description:

Search and aggregate travel news, destination information, and reviews from multiple sources for travel planning workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhzallen](https://clawhub.ai/user/nhzallen)

### License/Terms of Use:

MIT-0

## Use Case:

Travel planning professionals, travel agents, tour operators, and travel content creators use this skill to gather current destination information, tourism news, reviews, travel tips, and visa or policy updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional browser scraping uses Chromium, Xvfb, and Puppeteer and may interact with third-party travel, social, or review sites.

Mitigation: Run browser scraping only in an isolated environment with no unrelated secrets or active personal sessions.

Risk: Search queries and review lookups may disclose sensitive travel plans or account-related details to external services.

Mitigation: Avoid submitting sensitive travel, identity, or account information in queries and use the minimum query detail needed.

Risk: Optional dependencies and desktop automation guidance increase the installation and execution surface.

Mitigation: Pin dependencies, review packages before installation, and install desktop-control only when the workflow requires simulated interaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nhzallen/skills/travel-information-and-news)
- [Tavily](https://tavily.com)
- [Brave Search API](https://brave.com/search/api)
- [Desktop Control skill](https://clawhub.com/skills/desktop-control)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown guidance, JSON search data, DOCX, or PDF depending on selected options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include source URLs, detected language metadata, review summaries, and generated report files.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
