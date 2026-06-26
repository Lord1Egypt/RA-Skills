## Description: <br>
Searches and extracts Xiaohongshu notes, user profiles, comments, and content details through the xiaohongshu-mcp service. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[neargg](https://clawhub.ai/user/neargg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search Xiaohongshu content by keyword, inspect result metadata, and build reports from note details through a logged-in local MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a logged-in Xiaohongshu account and local cookies that may remain valid for a long time. <br>
Mitigation: Install and run it only in a trusted local environment, protect the cookie store, and re-authenticate deliberately when cookies expire. <br>
Risk: The underlying MCP tool exposes account-changing actions such as liking, favoriting, and publishing content. <br>
Mitigation: Require explicit user approval before any like, favorite, or publish action, and use search and read-only extraction by default. <br>
Risk: The release depends on a third-party MCP binary and was flagged suspicious by the security evidence. <br>
Mitigation: Review the third-party binary before use, avoid startup persistence unless needed, and follow the security guidance from the release evidence. <br>


## Reference(s): <br>
- [xhs-search ClawHub release](https://clawhub.ai/neargg/xhs-search) <br>
- [xiaohongshu-mcp GitHub repository](https://github.com/xpzouying/xiaohongshu-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; the search wrapper prints plain text result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled wrapper returns up to 10 search results by default; the source MCP search is documented as returning about 44 results per search.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
