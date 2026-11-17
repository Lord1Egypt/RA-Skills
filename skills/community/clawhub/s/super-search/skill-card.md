## Description:

Smart search with complete content formatted for WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runawaydevil](https://clawhub.ai/user/runawaydevil)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to run multilingual, location-aware web searches and receive consolidated results formatted for WhatsApp-style reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate broadly from common search phrasing.

Mitigation: Require explicit invocation or confirmation before running searches.

Risk: Search terms may be sent to external providers.

Mitigation: Disclose provider transmission and avoid sensitive personal, business, legal, medical, or credential-related queries.

Risk: User-controlled search terms are shown in shell command templates.

Mitigation: Encode search terms safely and avoid interpolating raw user input into shell commands.

Risk: Location defaults may be applied without user confirmation.

Mitigation: Ask before using location defaults for local searches.

## Reference(s):

- [Super Search skill page](https://clawhub.ai/runawaydevil/skills/super-search)
- [Publisher profile](https://clawhub.ai/user/runawaydevil)
- [Tavily Search API](https://api.tavily.com/search)
- [Brave Search API](https://api.search.brave.com/res/v1/web/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [WhatsApp-formatted Markdown-like text with source links and optional image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include multilingual summaries, location details, citations, and provider-sourced links.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
