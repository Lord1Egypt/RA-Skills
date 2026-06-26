## Description: <br>
Enhanced Tavily search with multi-API key rotation, AI-powered intent recognition, sub-question decomposition, intelligent summarization, and offline document export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fundou1081](https://clawhub.ai/user/fundou1081) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Tavily Plus to run Tavily-backed web searches with query classification, sub-question decomposition, key rotation, summaries, and optional local Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and result processing are sent to Tavily or the configured base URL. <br>
Mitigation: Avoid searching for secrets or highly sensitive internal data, and configure the base URL only for trusted Tavily-compatible endpoints. <br>
Risk: Optional report export can store query content, source snippets, and summaries locally. <br>
Mitigation: Enable report export only for content that is acceptable to save under the OpenClaw workspace. <br>


## Reference(s): <br>
- [ClawHub Tavily Plus release page](https://clawhub.ai/fundou1081/tavily-plus) <br>
- [Configured Tavily API base URL](https://api.tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Structured JSON response with optional Markdown report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tavily API key configuration; optional export writes local reports under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
