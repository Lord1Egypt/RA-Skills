## Description: <br>
TCED Cloud Drive helps agents manage Tencent Cloud Enterprise Drive files, spaces, and account authentication through MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuijiawei123](https://clawhub.ai/user/cuijiawei123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and enterprise users use this skill to browse, search, upload, download, and manage files across Tencent Cloud Enterprise Drive personal and team spaces after OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and using the skill grants OAuth-based access to enterprise cloud files. <br>
Mitigation: Install only when TCED access is intended, authorize only needed spaces, and confirm upload or download paths before file transfer. <br>
Risk: OAuth tokens and endpoint configuration are stored in ~/.tced-mcp/auth.json. <br>
Mitigation: Protect the local auth file, keep permissions restricted, and avoid exposing the file contents. <br>
Risk: Changing TCED endpoints can send OAuth tokens and API requests to unintended services. <br>
Mitigation: Use only the official Tencent endpoints pan.tencent.com and api.tencentsmh.cn as directed by the security guidance. <br>
Risk: Using an unpinned MCP package version can introduce unexpected package changes. <br>
Mitigation: Keep the MCP package pinned to the reviewed version and review changelogs before upgrading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cuijiawei123/tced-skill) <br>
- [TCED MCP Server API Reference](references/api_reference.md) <br>
- [Tencent Cloud Enterprise Drive authorization endpoint](https://pan.tencent.com) <br>
- [Tencent SMH API endpoint](https://api.tencentsmh.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to call MCP tools for OAuth login, account and space selection, file listing, search, upload, and download.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
