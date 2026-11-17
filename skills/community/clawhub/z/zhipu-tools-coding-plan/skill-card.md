## Description:

Provides agents with Z.AI/Zhipu tools for web search, web page reading, GitHub repository documentation lookup, file parsing, vision understanding, and quota checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wnzzer](https://clawhub.ai/user/wnzzer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve web results, read pages, search repository documentation, parse local documents, analyze images or videos, and check Zhipu quota while coding or researching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, URLs, repository identifiers, and selected local files or media may be sent to Z.AI/Zhipu services.

Mitigation: Avoid sensitive inputs and confirm user intent before processing private documents, screenshots, videos, or repository data.

Risk: Some paths can involve billing or quota behavior that differs between MCP and Legacy modes.

Mitigation: Prefer the Python zhipu_tool.py path, keep Legacy mode explicit, and check quota or balance before higher-volume use.

Risk: The optional Vision MCP command runs an unpinned npm package.

Mitigation: Pin and review the package version before running that optional command, or avoid it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wnzzer/skills/zhipu-tools-coding-plan)
- [Z.AI Open Platform](https://open.bigmodel.cn/)
- [Z.AI MCP web reader endpoint](https://api.z.ai/api/mcp/web_reader/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with command, code, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-derived search results, web page content, repository file excerpts, parsed document text, vision analysis, or quota summaries.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
