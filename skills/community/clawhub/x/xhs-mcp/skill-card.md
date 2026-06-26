## Description: <br>
小红书 helps agents research Xiaohongshu/RedNote content and, with explicit safeguards, publish image-text notes through a user-run local MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to search Xiaohongshu/RedNote notes, inspect note details and comments, browse recommendation feeds, and publish image-text notes after per-post approval. It is intended for use with a separately installed local third-party MCP service that the user reviews, pins, starts, and controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates platform access to a separately installed third-party MCP service and its active Xiaohongshu account session. <br>
Mitigation: Review and pin the third-party component before use, run it only on localhost, use a dedicated account, stop the service after the task, and revoke the login device when finished. <br>
Risk: Publishing can create public content that may be difficult to undo after submission. <br>
Mitigation: Require a structured preview and explicit per-post authorization; the client also requires a dedicated-account declaration and interactive confirmation or --yes after approval. <br>
Risk: Remote endpoint configuration could expose account actions beyond the user's local machine. <br>
Mitigation: Keep the MCP service bound to loopback; the bundled client refuses non-loopback endpoints unless the user explicitly overrides that guard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wscats/xhs-mcp) <br>
- [Setup instructions](SETUP.md) <br>
- [Third-party Xiaohongshu MCP component](https://github.com/xpzouying/xiaohongshu-mcp) <br>
- [Third-party Xiaohongshu MCP releases](https://github.com/xpzouying/xiaohongshu-mcp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call a local loopback MCP endpoint and can emit raw JSON with --json.] <br>

## Skill Version(s): <br>
1.0.10 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
