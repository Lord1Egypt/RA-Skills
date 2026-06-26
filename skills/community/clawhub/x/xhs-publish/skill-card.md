## Description: <br>
Generates Xiaohongshu post titles, body copy, covers, knowledge cards, or videos, then helps publish the reviewed note through a Xiaohongshu MCP workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianduoduo1422608857](https://clawhub.ai/user/qianduoduo1422608857) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and social media operators use this skill to draft Xiaohongshu notes, generate associated visual or video assets, review the prepared content, and publish it to a target account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Xiaohongshu account sessions, secrets, background services, and public posting. <br>
Mitigation: Use a dedicated Xiaohongshu account, keep API keys and browser cookies out of chat, rotate any exposed credentials, and avoid running the MCP service or downloaded binaries outside a sandbox. <br>
Risk: Prepared content may be published publicly to the wrong account or before the user catches title, body, media, or destination mistakes. <br>
Mitigation: Manually review the exact title, body, media, and destination account before approving any publish action. <br>
Risk: The artifact describes platform automation and login flows that may be sensitive under Xiaohongshu platform rules. <br>
Mitigation: Confirm the current platform policy and the account owner's authorization before using automated publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qianduoduo1422608857/xhs-publish) <br>
- [Publisher profile](https://clawhub.ai/user/qianduoduo1422608857) <br>
- [Content guide](references/content-guide.md) <br>
- [Cover guide](references/cover-guide.md) <br>
- [Title guide](references/title-guide.md) <br>
- [XHS content vetter](references/xhs_content_vetter.md) <br>
- [MD2Card service](https://md2card.cn/zh/login) <br>
- [Volcengine content generation API](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, shell commands, and generated media publishing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare titles, body text, cover images, knowledge-card images, video notes, login guidance, and final publish commands for user review.] <br>

## Skill Version(s): <br>
1.4.5 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
