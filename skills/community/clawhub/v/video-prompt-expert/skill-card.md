## Description: <br>
帮助用户编写专业级 AI 视频提示词，支持多场景创作、常见问题诊断，并可调用 RedFox API 生成 MP4 视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, content operators, and creative professionals use this skill to turn natural-language video ideas into structured, executable AI video prompts, diagnose common generation issues, and optionally submit prompts for MP4 generation through RedFox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes hidden usage-recording behavior that transmits the user's RedFox API key to a record endpoint. <br>
Mitigation: Review the skill before installation and require clear user notice and consent before any usage-recording call sends credentials or usage data. <br>
Risk: The skill may guide users to store REDFOX_API_KEY in permanent shell or user environment configuration. <br>
Mitigation: Use a limited, revocable API key and prefer session-only environment variables or a trusted secret store instead of permanent profile-file changes. <br>
Risk: Prompts and generation requests are sent to RedFox service endpoints. <br>
Mitigation: Avoid submitting sensitive, confidential, or regulated content unless RedFox handling, retention, and access controls are acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/video-prompt-expert) <br>
- [Core Workflow](references/core_workflow.md) <br>
- [Prompt Templates](assets/templates/prompt_templates.json) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?souce=github) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown and plain text prompts with optional shell commands, configuration guidance, and generated MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY for RedFox API calls; generated videos are submitted to and retrieved from RedFox endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
