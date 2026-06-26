## Description: <br>
Automatically detects multimodal, coding, reasoning, Office, and general tasks and recommends or switches the current main session to an appropriate model while leaving subagent sessions on their preset models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route main-session requests to task-appropriate models for images, video, audio, code, reasoning, Office documents, writing, and general chat. It is intended for automatic model selection guidance and optional session-level switching, with subagent sessions excluded from automatic switching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic model changes can route prompts or sensitive media to a different provider than the user expected. <br>
Mitigation: Review the documented routing rules before installation and avoid sensitive images, audio, video, or prompts unless provider routing and consent behavior are clear. <br>
Risk: The documented authority is broader and less clearly controlled than users may expect, including cross-session sessionKey usage. <br>
Mitigation: Disable or remove any ability to target other sessions and keep automatic switching limited to the current main session. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidme6/smart-model-switcher-v5) <br>
- [Publisher Profile](https://clawhub.ai/user/davidme6) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, command examples, JavaScript CLI output, and model routing recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend or perform local session model changes through OpenClaw-compatible session controls.] <br>

## Skill Version(s): <br>
5.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
