## Description: <br>
面向 talking-head / presenter 场景的 Sparki skill 变体，沿用最新版官方 Sparki 安装、API key、上传和命令说明，同时保留口播场景定位。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to route talking-head, interview, tutorial, presenter, and explainer videos through Sparki cloud editing workflows for tighter edits, cleaner presentation, captions, resizing, and downloadable video results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos are uploaded to Sparki cloud services for editing. <br>
Mitigation: Use only videos that are appropriate for cloud processing, and do not use the skill for sensitive videos that must remain local. <br>
Risk: The setup flow can save a Sparki API key under the user's OpenClaw configuration directory. <br>
Mitigation: Prefer providing SPARKI_API_KEY through the environment when the key should not be saved to disk. <br>
Risk: A custom API base URL changes where videos and credentials are sent. <br>
Mitigation: Use the default Sparki endpoint unless the alternate base URL is fully trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fischerlam/talking-head-editor-zh) <br>
- [Publisher profile](https://clawhub.ai/user/fischerlam) <br>
- [Sparki homepage](https://sparki.io) <br>
- [Sparki API domain](https://agent-api.sparki.io) <br>
- [Telegram upload link](https://t.me/Sparki_AI_bot/upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses from Sparki commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Sparki setup, upload, edit, status, download, and run command guidance; completed edits download video files through the Sparki service.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
