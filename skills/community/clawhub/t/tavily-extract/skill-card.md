## Description: <br>
Extract content from specific URLs using Tavily's extraction API and return clean markdown or text from web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanYDL](https://clawhub.ai/user/evanYDL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract readable content from known web URLs without writing custom Tavily API code. It supports single-page and batch extraction, focused extraction by query, and advanced extraction for dynamic pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided URLs, query text, and extraction options to Tavily under the user's account. <br>
Mitigation: Use it only with URLs and extraction inputs approved for sharing with Tavily; avoid private, internal, authenticated, regulated, or confidential URLs unless that sharing is approved. <br>
Risk: The OAuth flow and MCP token cache may retain Tavily credentials on shared machines. <br>
Mitigation: Review local OAuth/token cache behavior before use on shared systems, or configure an approved Tavily API key through the agent environment. <br>


## Reference(s): <br>
- [ClawHub Tavily Extract Release](https://clawhub.ai/evanYDL/tavily-extract) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Extract API Endpoint](https://api.tavily.com/extract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON response containing extracted markdown or text content, failed URLs, and response timing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes up to 20 URLs per request and supports query-focused chunking, extraction depth, output format, image inclusion, and timeout options.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
