## Description:

AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yi307520559-droid](https://clawhub.ai/user/yi307520559-droid)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Tavily-powered web searches and extract page content for research, current-events lookups, and source gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review states that the wrapper can turn a search query into local shell command execution.

Mitigation: Review or patch the wrapper before installing or invoking it with untrusted queries; use scripts/search.mjs directly or replace string interpolation with argument-array execution.

Risk: Submitted queries, URLs, and the Tavily API key are sent to Tavily's API.

Mitigation: Avoid sending secrets or sensitive internal URLs as search or extraction inputs, and use a scoped Tavily API key where possible.

## Reference(s):

- [Tavily](https://tavily.com)
- [ClawHub skill page](https://clawhub.ai/yi307520559-droid/skills/tavily-search-yourname)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with search answers, source lists, extracted page content, and inline URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search supports result count up to 20, basic or advanced depth, general or news topic, and optional news-day limits.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
