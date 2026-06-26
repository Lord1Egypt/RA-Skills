## Description: <br>
全平台视频发布汇总。对比四大国内视频平台（小红书、抖音、B站、视频号）的发布规则和步骤，提供最佳发布策略。自动选择最适合的平台组合。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnyxu820](https://clawhub.ai/user/Johnnyxu820) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and social media operators use this skill to prepare publishing guidance for videos across Xiaohongshu, Douyin, Bilibili, and WeChat Channels. It helps compare platform constraints, choose a publishing sequence, and confirm title and video requirements before posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may prepare or initiate public video posts to external social platforms. <br>
Mitigation: Require explicit confirmation of the account, target platforms, video file, title, description, tags, and final publish action before anything is posted. <br>
Risk: A stale or incorrect published-record path may cause duplicate-posting checks to be unreliable. <br>
Mitigation: Confirm the local published.json path and inspect the existing record before relying on duplicate-publish guidance. <br>
Risk: Platform-specific title, file-size, or format limits may block publication if not checked. <br>
Mitigation: Validate the video and title against each selected platform's requirements before upload. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Johnnyxu820/video-publish-all) <br>
- [Xiaohongshu video publishing portal](https://creator.xiaohongshu.com/publish/publish?source=official&target=video) <br>
- [Douyin video publishing portal](https://creator.douyin.com/creator-micro/content/post/video) <br>
- [Bilibili video upload portal](https://member.bilibili.com/platform/upload/video/frame) <br>
- [WeChat Channels post creation portal](https://channels.weixin.qq.com/platform/post/create) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with tables, examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local video and published-record paths supplied by the user or skill evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: _meta.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
