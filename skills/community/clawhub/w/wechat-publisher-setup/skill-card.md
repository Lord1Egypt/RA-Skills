## Description: <br>
Installs an OpenClaw WeChat publishing team with visual design, article formatting, API publishing, and publishing analytics support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[little-ke](https://clawhub.ai/user/little-ke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and developers use this skill to deploy a two-agent WeChat Official Account publishing workflow, including cover design, article formatting, draft creation, publication, and post-publication metrics review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles WeChat AppID, AppSecret, and access-token material that may be stored in local workspace files. <br>
Mitigation: Use a secret manager or runtime environment variables where possible, restrict file permissions, remove stored secrets after use, and rotate the WeChat AppSecret if exposure is suspected. <br>
Risk: Persistent workspace memory may retain account details, publishing context, or other sensitive operating information. <br>
Mitigation: Allow memory retention only when intentional, review stored memory files periodically, and delete sensitive prior-session data that is not required. <br>
Risk: The included publishing flow can submit WeChat drafts for publication through the WeChat API. <br>
Mitigation: Require explicit operator confirmation before publishing and validate credentials, IP allowlisting, draft content, cover assets, and publication status before treating a release as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/little-ke/wechat-publisher-setup) <br>
- [WeChat Official Accounts API base endpoint](https://api.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an existing OpenClaw content-creation team.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
