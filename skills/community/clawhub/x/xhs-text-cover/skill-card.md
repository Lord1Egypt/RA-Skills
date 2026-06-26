## Description: <br>
Xhs helps agents draft Xiaohongshu titles and post copy, generate simple cover images, and assist with publishing, search, and engagement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckychay](https://clawhub.ai/user/luckychay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and account operators use this skill to create Xiaohongshu-ready content, generate cover images, and manage posting or engagement actions through an agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a real Xiaohongshu account for posts, comments, likes, favorites, and product-related actions. <br>
Mitigation: Require a preview and explicit user confirmation before any account-changing action. <br>
Risk: The workflow may use browser cookies or QR login state for account access. <br>
Mitigation: Prefer QR login, avoid pasting browser cookies when possible, and delete stored cookies after use. <br>
Risk: The workflow depends on a persistent local MCP service and a downloaded Xiaohongshu MCP release. <br>
Mitigation: Verify the downloaded release before use and confirm operators know how to stop the service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luckychay/xhs-text-cover) <br>
- [Publisher profile](https://clawhub.ai/user/luckychay) <br>
- [Title guide](references/title-guide.md) <br>
- [Content guide](references/content-guide.md) <br>
- [Cover guide](references/cover-guide.md) <br>
- [Xiaohongshu MCP releases](https://github.com/xpzouying/xiaohongshu-mcp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local cover image files and structured MCP tool arguments for user-confirmed platform actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
