## Description:

Web search, extraction, crawling, mapping, and deep research via Tavily API. Five tools for finding information, extracting content, exploring websites, and generating research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[popxool868-abcd](https://clawhub.ai/user/popxool868-abcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search the web, extract URL content, crawl or map websites, and produce research reports through Tavily. It is suited for current-information lookup, fact-checking, reference gathering, and structured web research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, target URLs, crawl instructions, and research prompts are sent to Tavily using the configured API key.

Mitigation: Avoid sending secrets, internal-only URLs, regulated data, or proprietary prompts unless Tavily is approved as a third-party processor for the intended use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/popxool868-abcd/skills/tavily-searchpb)
- [Tavily API Documentation](https://docs.tavily.com)
- [Tavily](https://tavily.com)
- [openclaw-tavily npm Package](https://www.npmjs.com/package/openclaw-tavily)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, and JSON-like configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY; search results are capped by script options, and crawl output truncates page content in script fallback mode.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
