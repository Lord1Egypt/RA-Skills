## Description: <br>
Fetches webpage content through the XiaoBenYang service and converts HTML into Markdown for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill when an agent needs to fetch a public URL and return extracted page content as Markdown or raw HTML. It is best suited for public webpage retrieval where routing the URL through the XiaoBenYang service is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a XiaoBenYang API key and saves it in a local .env file. <br>
Mitigation: Use a dedicated key, keep the .env file out of source control, rotate the key after testing, and remove it when the skill is no longer needed. <br>
Risk: Requested URLs are handled by a third-party MCP service. <br>
Mitigation: Use the skill for public URLs unless the provider and data handling behavior have been reviewed for private, internal, authenticated, or regulated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-fetch) <br>
- [XiaoBenYang API key site](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP service endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or raw HTML returned from a JSON-like tool result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The fetch tool accepts url, max_length, start_index, and raw parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
