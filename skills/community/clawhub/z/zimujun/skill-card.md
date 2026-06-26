## Description: <br>
字幕菌（zimujun）：从主流视频平台链接提取视频文案/字幕文本。适用于 YouTube、TikTok/抖音、小红书、Bilibili 等平台。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyriswu](https://clawhub.ai/user/kyriswu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to extract transcript or subtitle text from supported video platform links, including YouTube, TikTok/Douyin, Xiaohongshu, and Bilibili. The skill can either run the zimujun npm command or direct users to the hosted transcript page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive API key and the artifact includes language suggesting that users may paste the key into chat. <br>
Mitigation: Set `ZMJ_API_KEY` only in a local environment or approved secret manager, do not paste it into chat, and rotate the key if it has been shared. <br>
Risk: Video links and transcript requests may be processed by the zimujun/devtool service and npm code is fetched at runtime. <br>
Mitigation: Use the skill only for content appropriate for that third-party service, review the service before submitting sensitive links, and approve runtime npm execution in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kyriswu/zimujun) <br>
- [Web transcript entry](https://devtool.uk/video-transcript) <br>
- [API key information](https://devtool.uk/plugin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command guidance and transcript or error fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a video URL or share text; npm command usage requires a ZMJ_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.18 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
