## Description: <br>
微信操作手册 helps an agent open and browse WeChat Moments, scroll through posts, view friend updates, and like or comment on posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[islandlxl](https://clawhub.ai/user/islandlxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal automation operators use this skill to guide an agent through Windows WeChat UI actions for opening Moments, browsing posts, and optionally interacting with contacts. Because it can affect a live WeChat account, likes, comments, messages, and calls should require manual confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate live WeChat messages, likes or comments, and voice calls from the user's account. <br>
Mitigation: Install only when this account control is intentional, and require manual confirmation before any like, comment, message, or call is sent. <br>
Risk: Fixed screen coordinates can click unintended UI elements on different resolutions or window layouts. <br>
Mitigation: Verify and adapt coordinates in a controlled session before allowing execution on a live account. <br>
Risk: Users who only need Moments browsing may receive broader contact search, message sending, and voice call behavior than expected. <br>
Mitigation: Remove or ignore the contact search, message sending, and voice call sections when only browsing WeChat Moments is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/islandlxl/wechat-moment) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes coordinate-based Windows UI automation steps for WeChat; coordinates may require local adjustment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
