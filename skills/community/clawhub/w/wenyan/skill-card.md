## Description: <br>
文颜 guides agents through using wenyan-cli to publish frontmatter-based Markdown articles to a WeChat Official Account, including theme, syntax highlighting, image, and credential setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caol64](https://clawhub.ai/user/caol64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, and developers use this skill as a command guide for preparing Markdown with required frontmatter, publishing it to a WeChat Official Account through wenyan-cli, and managing publishing themes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on an external npm CLI used to publish content. <br>
Mitigation: Verify the npm package before installation and consider pinning a known version. <br>
Risk: Incorrect Markdown frontmatter, cover images, embedded image paths, or account targets can publish unintended content. <br>
Mitigation: Review the Markdown file, metadata, image paths, and target WeChat account before publishing. <br>
Risk: WeChat app credentials and server API keys are sensitive secrets. <br>
Mitigation: Keep WECHAT_APP_ID, WECHAT_APP_SECRET, and any server API key out of source control, logs, screenshots, and shared shells. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caol64/wenyan) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and option tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential-handling guidance for WeChat publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
