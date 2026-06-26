## Description: <br>
自动生成微信公众号文章、插入配图、执行格式、敏感词和重复检查，并将通过检查的内容发布到微信公众号草稿箱。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taoj2025](https://clawhub.ai/user/taoj2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and developers can use this skill to assemble WeChat public-account drafts from a topic, generate or attach images, run pre-publication checks, and submit passing drafts for review or publishing. The workflow is best used with manual review before enabling scheduled or credentialed publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires content-generation and WeChat or Tencent publishing credentials. <br>
Mitigation: Use least-privilege credentials, keep secrets outside source files, and confirm exactly which account permissions are needed before running publish steps. <br>
Risk: The security evidence says publishing authority and safety checks are not clearly controlled enough for a public-account workflow. <br>
Mitigation: Require manual review before publishing, verify the external WeChat publisher dependency, and replace placeholder sensitive-word and duplication checks with real policy checks. <br>
Risk: Scheduled execution can generate and publish drafts automatically. <br>
Mitigation: Do not enable cron or unattended publishing until review gates, logging, and rollback procedures are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taoj2025/wechat-content-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/taoj2025) <br>
- [Configuration reference](artifact/references/config.md) <br>
- [MiniMax image generation endpoint](https://api.minimaxi.com/v1/image_generation) <br>
- [Picsum image source](https://picsum.photos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles with image references, command-line output, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create article directories, image files, draft content, and publishing notifications when configured with credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
