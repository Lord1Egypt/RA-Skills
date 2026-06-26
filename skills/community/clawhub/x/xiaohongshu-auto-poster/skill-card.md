## Description: <br>
Xiaohongshu Auto Poster helps an agent generate Xiaohongshu post copy and publish, pin, or inspect account content through a locally configured MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmin1113](https://clawhub.ai/user/jmin1113) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, merchants, and technically capable operators can use this skill to draft Xiaohongshu posts, check login status, publish image or video notes, pin posts, and review basic post metrics after configuring the required local service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or pin live Xiaohongshu account content with weak confirmation safeguards. <br>
Mitigation: Use a test or low-risk account first, generate drafts for review, and require explicit confirmation before any post or pin action. <br>
Risk: The workflow depends on running a local MCP binary and may be configured for background or autostart execution. <br>
Mitigation: Verify the MCP binary source before running it and disable background or autostart behavior when the service is not actively needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jmin1113/xiaohongshu-auto-poster) <br>
- [Setup Guide](references/setup.md) <br>
- [Content Templates](references/content-templates.md) <br>
- [Xiaohongshu Operations Notes](references/运营知识.md) <br>
- [Xiaohongshu MCP Releases](https://github.com/xpzouying/xiaohongshu-mcp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown instructions with generated social post copy and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger live Xiaohongshu account actions through a locally running MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
