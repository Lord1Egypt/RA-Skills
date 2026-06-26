## Description: <br>
Publishes Markdown articles as WeChat Official Account drafts through wenyan-cli with theme and code highlighting support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hidebug](https://clawhub.ai/user/hidebug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and developers use this skill to prepare and publish Markdown posts into the WeChat Official Account draft workflow, including title and cover frontmatter, local image handling, themes, and code highlighting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use may install a global npm package for wenyan-cli and change the local machine environment. <br>
Mitigation: Install and review a pinned wenyan-cli version yourself before use, or run the skill in a controlled environment where global npm changes are acceptable. <br>
Risk: The skill uses WeChat account credentials and can create drafts in the connected Official Account. <br>
Mitigation: Keep WECHAT_APP_SECRET out of Git and shared dotfiles, inject credentials through a trusted environment, and verify the exact Markdown file, images, and resulting draft before publishing. <br>
Risk: Publishing can fail or produce incomplete drafts when required frontmatter or local image paths are missing. <br>
Mitigation: Check that the Markdown starts with title and cover frontmatter, and use local paths for cover and article images before running the publish command. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hidebug/xqx-wechat-publisher) <br>
- [Theme reference](references/themes.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [wenyan-cli](https://github.com/caol64/wenyan-cli) <br>
- [wenyan documentation](https://wenyan.yuzhi.tech) <br>
- [WeChat Official Account documentation](https://developers.weixin.qq.com/doc/offiaccount/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and publish status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WECHAT_APP_ID and WECHAT_APP_SECRET; article Markdown must include title and a local cover image path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
