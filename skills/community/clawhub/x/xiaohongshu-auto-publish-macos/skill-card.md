## Description: <br>
小红书自动发布技能 - 支持图片搜索下载、自动上传发布一键完成 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardx0319](https://clawhub.ai/user/richardx0319) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill on macOS to prepare Xiaohongshu posts, including image preparation, title and body entry, hashtags, and browser-based publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Xiaohongshu publishing session and may proceed to public posting without a clear final approval checkpoint. <br>
Mitigation: Require the agent to pause before the final publish click and show the target account, image source, title, body, hashtags, and final page state for explicit user approval. <br>
Risk: Automatically downloaded or prepared images may not match the intended post topic or rights expectations. <br>
Mitigation: Review the selected image source and final upload preview before authorizing publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/richardx0319/xiaohongshu-auto-publish-macos) <br>
- [Xiaohongshu creator publish page](https://creator.xiaohongshu.com/publish/publish) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown instructions and terminal output with file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare image files on disk when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
