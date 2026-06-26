## Description: <br>
Drafts tutorial-style WeChat Official Account articles in an author's style, saves Markdown, and publishes drafts through wenyan-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niko-yang-arch](https://clawhub.ai/user/niko-yang-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and developers use this skill to collect tutorial steps and images, draft a Markdown article in a selected author style, convert it to WeChat-compatible formatting, and publish it to a WeChat Official Account draft box. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat publishing credentials may be stored or reused in unsafe locations. <br>
Mitigation: Use temporary environment variables or a real secret manager, and do not store AppSecret values in the skill assets directory. <br>
Risk: Personal profile text, QR codes, and images may remain in local skill assets after use. <br>
Mitigation: Delete stored profile, QR, and image files when publishing is complete. <br>
Risk: Draft articles and uploaded images may contain incorrect or unintended public-facing content. <br>
Mitigation: Review all generated Markdown and images before publishing or moving a draft toward release. <br>
Risk: The local collection server broadens the skill's runtime exposure while active. <br>
Mitigation: Run the local server only when collecting article inputs and stop it when finished. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/niko-yang-arch/wechat-tutorial-editor-publisher) <br>
- [wenyan-cli GitHub](https://github.com/caol64/wenyan-cli) <br>
- [wenyan Documentation](https://wenyan.yuzhi.tech) <br>
- [wenyan Upload and IP Whitelist Guide](https://yuzhi.tech/docs/wenyan/upload) <br>
- [WeChat Official Account API Documentation](https://developers.weixin.qq.com/doc/offiaccount/) <br>
- [Themes Reference](references/themes.md) <br>
- [Troubleshooting Reference](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article drafts, JSON step files, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local profile, image, and article files and may use wenyan-cli to upload images and publish WeChat drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
