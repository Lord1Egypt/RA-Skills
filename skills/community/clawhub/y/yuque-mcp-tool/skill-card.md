## Description: <br>
Read Yuque documents in AI clients via MCP, including rendered content, Markdown conversion, and knowledge-base document listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy8663](https://clawhub.ai/user/andy8663) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-client users use this skill to connect Claude Desktop, Cursor, WorkBuddy, or another MCP client to Yuque so an agent can read, convert, and list knowledge-base documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Yuque session cookie, which can grant access to documents reachable by that account. <br>
Mitigation: Store the session carefully, avoid sharing MCP configuration files, use the least-privileged Yuque account practical, and rotate or remove the session if the configuration may have been exposed. <br>
Risk: Connected AI agents can read Yuque documents available to the configured session. <br>
Mitigation: Install only for trusted MCP clients and use an account whose document access is appropriate for the intended workflow. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/andy8663/yuque-mcp-tool) <br>
- [ClawHub skill page](https://clawhub.ai/andy8663/yuque-mcp-tool) <br>
- [Publisher profile](https://clawhub.ai/user/andy8663) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, text, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Yuque document content reachable by the configured session.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
