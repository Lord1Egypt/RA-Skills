## Description: <br>
AI-optimized web search with structured summarization, combining Tavily Search API + proven summarization methodology from summarize. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxiaolong1988](https://clawhub.ai/user/liuxiaolong1988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run Tavily-backed web searches or URL extraction, then present concise Markdown summaries with source-oriented context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and submitted URLs are sent to Tavily for processing. <br>
Mitigation: Use a dedicated Tavily API key and avoid confidential search terms, private documents, internal URLs, or secret-bearing links unless that sharing is approved. <br>
Risk: Web search summaries can reflect stale, incomplete, or third-party source content. <br>
Mitigation: Review cited sources and use the summary as research assistance rather than as sole authority for high-impact decisions. <br>


## Reference(s): <br>
- [ClawHub Tavily Summary](https://clawhub.ai/liuxiaolong1988/tavily-summary) <br>
- [Tavily](https://tavily.com) <br>
- [Summarize methodology reference](https://github.com/steipete/summarize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text from Node.js command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search accepts result count, depth, topic, and news recency options; URL extraction prints extracted page content and failed URL details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence and metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
