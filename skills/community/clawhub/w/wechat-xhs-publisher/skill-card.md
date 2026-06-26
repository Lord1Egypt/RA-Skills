## Description: <br>
Rewrites trending news into WeChat Official Account articles, generates article images, checks publishing IP, and guides publishing to WeChat and Xiaohongshu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[achievejia](https://clawhub.ai/user/achievejia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operators and content creators use this skill to turn trending news material into article drafts with images and publish them to WeChat Official Accounts and Xiaohongshu after account, IP, and originality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can publish content to public WeChat and Xiaohongshu accounts. <br>
Mitigation: Require a preview and explicit user confirmation before any upload or post, and verify the active publishing accounts. <br>
Risk: Rewritten news may be marked as original without enough copyright or authorship confirmation. <br>
Mitigation: Confirm source rights, authorship, and platform originality requirements before setting originality flags. <br>
Risk: Publishing from an unapproved public IP can interrupt or misroute the WeChat publishing flow. <br>
Mitigation: Run the documented IP check before WeChat publishing and stop for user review if the IP differs from the configured allowlist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/achievejia/wechat-xhs-publisher) <br>
- [IP38 public IP lookup](https://www.ip38.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles with frontmatter, image-generation prompts, publishing commands, configuration checks, and completion reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local article and image files and may invoke external publishing tools when the user authorizes them.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
