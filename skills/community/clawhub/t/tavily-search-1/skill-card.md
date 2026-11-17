## Description:

AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petterhuang92-design](https://clawhub.ai/user/petterhuang92-design)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Tavily web searches, perform deeper or news-focused searches, and extract page content from URLs through a configured Tavily API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided search queries and URLs are sent to Tavily.

Mitigation: Use the skill only when sending those queries or URLs to Tavily is acceptable under the applicable account and data policy.

Risk: The skill requires access to a Tavily API key.

Mitigation: Provide TAVILY_API_KEY through an approved environment or secret-management path and avoid placing credentials in prompts, URLs, or skill files.

Risk: Private, sensitive, or credential-bearing URLs may be exposed if submitted for extraction.

Mitigation: Avoid submitting sensitive URLs unless that use is approved for the Tavily account and data policy.

## Reference(s):

- [Tavily](https://tavily.com)
- [ClawHub Skill Page](https://clawhub.ai/petterhuang92-design/skills/tavily-search-1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with answers, source listings, extracted URL content, and failed URL notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; search result count is clamped to 1-20.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
