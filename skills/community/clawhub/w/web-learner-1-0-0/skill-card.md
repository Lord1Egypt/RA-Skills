## Description:

Enables an AI assistant to search, fetch, browse, and summarize current web information when users ask for news, recent facts, links, or topic-specific research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[332054781](https://clawhub.ai/user/332054781)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide an assistant through web search, page fetching, browser fallback, and concise Chinese summaries with cited sources. It is intended for up-to-date research tasks such as news, weather, events, public links, and topics not covered by model training data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web queries may disclose sensitive private information to search engines or websites.

Mitigation: Avoid including sensitive private information in web queries unless the user is comfortable sending those terms to external web services.

Risk: Fetched web content can be incomplete, unavailable, anti-scraping protected, or misleading.

Mitigation: Use alternate sources or browser fallback when appropriate, disclose access limits, and summarize with clear source notes.

## Reference(s):

- [Web Learner reference resources](references/resources.md)
- [ClawHub skill page](https://clawhub.ai/332054781/skills/web-learner-1-0-0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown with concise Chinese summaries and source notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose web search, web fetch, or browser-tool usage depending on tool availability.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
