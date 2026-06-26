## Description: <br>
Tencent Weixin Channels publishing skill that uses browser automation to help publish video posts with uploads, titles, descriptions, topic tags, location, visibility, and originality declaration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnyxu820](https://clawhub.ai/user/Johnnyxu820) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and content operators use this skill to guide an agent through publishing prepared MP4 videos to a logged-in Weixin Channels account. It covers upload requirements, title and description entry, topic tags, optional location, visibility, originality declaration, and post-publish verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may publish real content to a Weixin Channels account. <br>
Mitigation: Before the final publish action, verify the logged-in account, video file, title, description, tags, location, visibility setting, and publish readiness. <br>
Risk: An incorrect originality declaration could misrepresent content ownership. <br>
Mitigation: Confirm that the video is original and that any originality declaration is true before selecting or confirming that option. <br>


## Reference(s): <br>
- [Weixin Channels Assistant](https://channels.weixin.qq.com) <br>
- [Weixin Channels Create Post](https://channels.weixin.qq.com/platform/post/create) <br>
- [Weixin Channels Content Management](https://channels.weixin.qq.com/platform/post/list) <br>
- [ClawHub Skill Page](https://clawhub.ai/Johnnyxu820/weixin-video-publish) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with browser navigation steps and example command text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no API key or MCP tool references detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
