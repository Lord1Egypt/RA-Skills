## Description: <br>
Provides guidance and helper tools for starting and using a Sefaria API MCP server to retrieve, search, and explore Jewish texts through MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davad00](https://clawhub.ai/user/davad00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to configure a local Sefaria MCP server and get example calls for text retrieval, search, reference parsing, metadata lookup, related content, and calendar tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing dependencies or starting the referenced MCP server runs local project code. <br>
Mitigation: Review the referenced repository and dependencies before running npm install, building, or connecting. <br>
Risk: The MCP server opens a local service on the configured port. <br>
Mitigation: Choose an appropriate local port, limit exposure to the intended environment, and stop the server when finished. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davad00/sefaria-api-skill) <br>
- [Sefaria API Documentation](https://developers.sefaria.org/) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [Referenced Sefaria API MCP Repository](https://github.com/davad00/sefaria-api-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a helper command to start a local MCP server with an optional port parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
