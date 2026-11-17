## Description:

Web search via Tavily API (alternative to Brave). Use when the user asks to search the web / look up sources / find links and Brave web_search is unavailable or undesired. Returns a small set of relevant results (title, url, snippet) and can optionally include short answer summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pazzilivo](https://clawhub.ai/user/pazzilivo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily web searches when web search is requested, especially when Brave search is unavailable or undesired. It returns concise titles, URLs, snippets, and optional short answer summaries for follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the configured Tavily API key are sent to Tavily.

Mitigation: Use only queries and text approved to leave the environment; avoid secrets, private internal URLs, and proprietary content unless sharing with Tavily is allowed.

Risk: The skill can read a Tavily API key from environment variables or a local ~/.openclaw/.env file.

Mitigation: Store keys in approved secret-management or restricted local configuration, limit file access, and rotate credentials if exposure is suspected.

Risk: Returned snippets and optional summaries may be incomplete for decisions that require source-level accuracy.

Mitigation: Use returned URLs for source review before relying on results in sensitive, external, legal, medical, or financial contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pazzilivo/skills/tavily-search-with-multi-key)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON search results, Brave-like JSON, or compact Markdown list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to concise search results and caps requested results between 1 and 10.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
