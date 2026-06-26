## Description: <br>
Tavily AI 搜索工具，专为AI Agent设计的联网搜索能力，支持实时搜索、深度研究、图片搜索、引用生成，返回结构化搜索结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-powered web searches, deeper research queries, and image searches, returning structured results with source URLs for Chinese or English workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes a prefilled Tavily API key and stores keys in plaintext config.json. <br>
Mitigation: Remove or replace the bundled key before use, use your own Tavily key, and store it outside the package or restrict config.json permissions. <br>
Risk: Search queries are sent to Tavily for processing. <br>
Mitigation: Use the skill only for queries appropriate to send to Tavily, and avoid submitting sensitive or restricted information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/tavily-search-cn) <br>
- [Tavily website](https://tavily.com/) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text or JSON search results with source URLs and optional image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tavily API key; search queries are sent to Tavily.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
