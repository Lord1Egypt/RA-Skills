## Description: <br>
小红书（XHS/RED）自动化助手，提供登录、搜索、浏览、互动、用户主页读取以及图文和视频发布的 MCP 服务端工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weznai](https://clawhub.ai/user/weznai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate Xiaohongshu workflows through an MCP service, including login, feed discovery, search, note detail retrieval, engagement actions, profile lookup, and content publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes account cookies and may expose an authenticated Xiaohongshu session. <br>
Mitigation: Remove bundled cookies before installation, rotate any exposed session, and reauthenticate locally. <br>
Risk: The MCP service exposes publishing, commenting, replying, liking, favoriting, and local media upload actions. <br>
Mitigation: Bind the service to localhost or require authentication, and require explicit user approval before state-changing or upload operations. <br>


## Reference(s): <br>
- [API Documentation](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/weznai/skill-xiaohongshu) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON tool responses and Markdown instructions with inline shell and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Xiaohongshu login session; media publishing tools may upload local image or video files.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
