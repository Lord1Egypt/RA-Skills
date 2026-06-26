## Description: <br>
Helps an agent guide user-authorized publishing of prepared video content to social platforms such as Douyin, Kuaishou, Bilibili, Xiaohongshu, and WeChat Channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and marketing teams use this skill to prepare, validate, and guide publication of videos across multiple logged-in social platform accounts. The agent confirms the platform, local video file, caption, and final publish action before browser automation or manual commands proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help operate logged-in social media accounts in a browser session. <br>
Mitigation: Confirm the target platform, account, video file, caption, and final publish step with the user before allowing automation. <br>
Risk: The helper can generate curl or wget commands for manually downloading media from a supplied URL. <br>
Mitigation: Review the generated command and URL before running it, prefer official or browser-based download paths, and scan downloaded files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hitjcl/social-publish) <br>
- [Publisher profile](https://clawhub.ai/user/hitjcl) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON validation results and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform-specific publishing steps, local file validation results, browser-operation guidance, and user-reviewed curl or wget download commands.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
