## Description: <br>
Automatically generates a daily World of Warcraft report with news, NGA forum highlights, daily images, and Feishu and WeChat notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lorexxar](https://clawhub.ai/user/lorexxar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Community operators and content maintainers use this skill to compile daily World of Warcraft news, NGA forum discussions, and image content into a Feishu document, then notify Feishu and WeChat recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated document links may be sent to fixed Feishu and WeChat recipients. <br>
Mitigation: Replace the hard-coded recipients with accounts you control before running the skill. <br>
Risk: The workflow can start or depend on local helper software, including a Xiaohongshu MCP service. <br>
Mitigation: Verify the helper scripts and binary, confirm they can be stopped and audited, and run them only in a trusted environment. <br>
Risk: Broad trigger phrases can cause the report workflow to run unintentionally. <br>
Mitigation: Narrow the trigger phrase or require explicit confirmation before creating and sending the report. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lorexxar/wow-daily-news) <br>
- [EXWIND World of Warcraft News](https://exwind.net/) <br>
- [World of Warcraft China News](https://wow.blizzard.cn/news/) <br>
- [NGA Forum](https://nga.178.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, files] <br>
**Output Format:** [Lark-flavored Markdown, generated Feishu document links, notification messages, and local Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include image media insertions and local files under the configured OpenClaw workspace image directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
