## Description: <br>
Manage a Xiaohongshu (RED) account through a local MCP service for account status checks, content search, note publishing, comments, likes, favorites, and related social media operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and developers use this skill to operate a Xiaohongshu account from an agent workflow, including browsing, publishing image or video notes, and performing engagement actions through a local MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a real Xiaohongshu account and perform public actions such as publishing, commenting, liking, favoriting, deleting cookies, or batch interactions. <br>
Mitigation: Require explicit user confirmation before any public, destructive, or batch account action. <br>
Risk: The local cookies.json file grants account access if exposed. <br>
Mitigation: Protect cookies.json like a password, keep it out of shared or synced folders, and reset the login session if exposure is suspected. <br>
Risk: Deployment depends on a third-party binary downloaded outside the skill artifact. <br>
Mitigation: Verify the binary source and release before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-xiaohongshu-mcp-skill-1-0-0) <br>
- [Deployment guide](artifact/references/deploy.md) <br>
- [Usage guide](artifact/references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets, MCP configuration, and tool usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local MCP service at http://localhost:18060/mcp and an authenticated cookies.json session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
