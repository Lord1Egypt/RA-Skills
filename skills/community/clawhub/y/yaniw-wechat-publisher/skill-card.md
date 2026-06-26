## Description: <br>
Helps an agent manage multiple WeChat public accounts, generate article content and cover images, and create WeChat draft posts with user confirmations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgedu-new](https://clawhub.ai/user/zgedu-new) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and manage WeChat public-account posts across multiple accounts, including account selection, article drafting, cover generation, and draft publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use real WeChat account credentials and create WeChat public-account drafts. <br>
Mitigation: Use environment variables for credentials, keep AppSecret values out of shared folders and version control, verify the active account before each run, and require an explicit final command before uploading covers or creating drafts. <br>
Risk: Broad prompts may produce incorrect, unintended, or unsuitable content for a public-account draft. <br>
Mitigation: Review generated article text and cover choices before proceeding, and preserve the skill's confirmation steps before any upload or draft creation. <br>
Risk: Publishing can fail or expose operational details when WeChat credentials or IP whitelist settings are incorrect. <br>
Mitigation: Configure credentials and IP allowlisting before use, test account connectivity, and rely on redacted error handling instead of sharing raw credential values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zgedu-new/yaniw-wechat-publisher) <br>
- [README](README.md) <br>
- [User Guide](USER_GUIDE.md) <br>
- [Configuration Guide](CONFIGURATION.md) <br>
- [Workflow Guide](references/workflow_guide.md) <br>
- [Article Format](references/article_format.md) <br>
- [Cover Styles](references/cover_styles.md) <br>
- [Configuration Template](references/config.template.json) <br>
- [WeChat Public Platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON configuration examples, shell commands, generated article Markdown, cover assets, and publish logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local article files, cover HTML/PNG files, publish logs, and WeChat draft entries when configured with valid account credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and changelog, released 2026-03-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
