## Description: <br>
Extracts text from supported Chinese video and social platforms, analyzes why the source content performs well, and rewrites it into copy drafts for Xiaohongshu, Toutiao, and Douyin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roseryztzhoutong](https://clawhub.ai/user/roseryztzhoutong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, media operators, and marketing teams use this skill to turn supported video links or copied scripts into viral-content analysis and platform-specific rewritten drafts for publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may fetch third-party platform content and use downloader or browser-automation tooling. <br>
Mitigation: Use it only for public or authorized content, and check the applicable platform terms before collecting or republishing source material. <br>
Risk: Some collection paths ask for platform session cookies. <br>
Mitigation: Avoid providing cookies unless necessary, keep them out of shared prompts and logs, and revoke or rotate them after use. <br>
Risk: Rewritten drafts can still create copyright, attribution, or platform-policy issues. <br>
Mitigation: Review all generated copy before publishing, verify claims and attribution, and adjust outputs for brand, legal, and platform compliance. <br>
Risk: The skill depends on local browser, transcription, and downloader packages that may change or fail independently. <br>
Mitigation: Install dependencies in an isolated environment and review generated files and commands before relying on them in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roseryztzhoutong/yijian-ba-baokuan) <br>
- [Douyin video page pattern](https://www.douyin.com/video/{video_id}) <br>
- [Bilibili video metadata API](https://api.bilibili.com/x/web-interface/view?bvid={bvid}) <br>
- [Bilibili player subtitle API](https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with setup commands and plain-text rewritten copy drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save rewritten drafts under an output directory; some platform paths may require local Python dependencies, browser automation, ASR downloads, or user-provided cookies.] <br>

## Skill Version(s): <br>
0.6.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
