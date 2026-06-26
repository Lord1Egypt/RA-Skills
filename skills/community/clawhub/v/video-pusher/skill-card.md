## Description: <br>
Routes account management and browser-assisted publishing workflows for Douyin, Xiaohongshu, WeChat Channels, Threads, and Instagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SamCheng0717](https://clawhub.ai/user/SamCheng0717) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and social-media teams use this skill to manage reusable platform login sessions and prepare content for publication across multiple social platforms. The skill uploads media, fills captions or metadata, and leaves the final publish or share action for user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable browser sessions can retain access to social-media accounts. <br>
Mitigation: Use dedicated accounts where possible, review account groups before publishing, and remove profile/session directories when an account is retired. <br>
Risk: Browser automation may conflict with platform account policies because the scripts try to hide automation indicators. <br>
Mitigation: Install only when this automation posture is acceptable for the target accounts and platforms, and verify each platform action before proceeding. <br>
Risk: Automatic removal of Chromium lock files can create profile-corruption risk. <br>
Mitigation: Avoid concurrent browser sessions for the same profile and back up or recreate profiles if browser state becomes inconsistent. <br>
Risk: Incorrect files, captions, platforms, or account groups could be prepared for publication. <br>
Mitigation: Confirm the exact file path, caption, target platform, and account group before the final publish or share click. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SamCheng0717/video-pusher) <br>
- [Douyin Creator upload](https://creator.douyin.com/creator-micro/content/upload) <br>
- [Xiaohongshu Creator publish](https://creator.xiaohongshu.com/publish/publish) <br>
- [WeChat Channels post creation](https://channels.weixin.qq.com/platform/post/create) <br>
- [Threads](https://www.threads.net/) <br>
- [Instagram](https://www.instagram.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and brief status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reuse local Chromium profile/session directories and opens a browser for user-controlled final publishing.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence; artifact frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
