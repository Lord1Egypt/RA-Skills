## Description: <br>
Xhs Mcp Service provides a local MCP server that lets agents search Xiaohongshu content, inspect login status, manage session cookies, interact with posts, and publish image or video notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackydai-bc](https://clawhub.ai/user/jackydai-bc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to connect an MCP client to a local Xiaohongshu automation service for content discovery, account interaction, and publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes live Xiaohongshu account actions such as posting, commenting, liking, favoriting, deleting cookies, and running examples or tests. <br>
Mitigation: Add an explicit confirmation step before any account-changing action or example/test script execution. <br>
Risk: The service can be bound broadly and expose account automation outside the local machine. <br>
Mitigation: Run it only on a machine and network you control, and bind the service to localhost rather than 0.0.0.0. <br>
Risk: The saved cookies file can provide account access if disclosed. <br>
Mitigation: Protect data/cookies.json like a password and remove or rotate it when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jackydai-bc/xhs-mcp-service) <br>
- [Publisher Profile](https://clawhub.ai/user/jackydai-bc) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [Puppeteer Documentation](https://pptr.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger live Xiaohongshu account actions through a separately running local MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
