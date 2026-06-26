## Description: <br>
多平台内容自动分发工具，在小红书发布后将内容同步到抖音、视频号、快手，并支持图片尺寸处理、标题标签填写和验证码处理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hwl1413520](https://clawhub.ai/user/hwl1413520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and developers use this skill to synchronize owned social-media content from Xiaohongshu to Douyin, WeChat Channels, and Kuaishou with platform-specific formatting and scheduling controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use account sessions and cookie files to publish publicly on social platforms. <br>
Mitigation: Use only accounts you control, protect cookie files as credentials, and require manual review before public posting. <br>
Risk: CAPTCHA and risk-control automation can create platform-rule and data-sharing risks, especially with third-party solving services. <br>
Mitigation: Keep third-party CAPTCHA solving disabled unless those risks are explicitly accepted, and prefer manual handling for sensitive account workflows. <br>
Risk: Batch and scheduled posting can publish content repeatedly or at scale without clear approval safeguards. <br>
Mitigation: Test behavior interactively first, keep scheduled mode disabled until reviewed, and set conservative rate limits and posting windows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hwl1413520/skill-distribute) <br>
- [Publisher profile](https://clawhub.ai/user/hwl1413520) <br>
- [Platform adaptation guide](references/PLATFORM_GUIDE.md) <br>
- [Selector configuration](references/SELECTORS.md) <br>
- [API documentation](references/API.md) <br>
- [Changelog](references/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operating guidance for browser automation, content adaptation, batch distribution, and scheduled posting workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
