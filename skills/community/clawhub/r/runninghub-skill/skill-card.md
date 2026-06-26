## Description: <br>
RunningHub AI 智能调用。Use when user wants to generate images, videos, or audio content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airix315](https://clawhub.ai/user/airix315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to guide OpenClaw agents in selecting and calling RunningHub AI workflows for image, video, and audio generation, including parameter defaults, async polling, storage decisions, and fallback handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, media, and generation requests to the external RunningHub service. <br>
Mitigation: Use it only when RunningHub processing is intended, and avoid submitting private prompts or media unless the user accepts that external-service handling. <br>
Risk: RunningHub access depends on the RUNNINGHUB_API_KEY credential. <br>
Mitigation: Store the API key in the environment or approved secret storage, avoid logging it, and rotate it if exposure is suspected. <br>
Risk: The setup flow asks users to install and build the external RHMCP project before use. <br>
Mitigation: Review the external project and dependency installation path before running npm install or build commands. <br>


## Reference(s): <br>
- [RHMCP project](https://github.com/AIRix315/RHMCP) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [RunningHub](https://www.runninghub.cn) <br>
- [recommended-apps.json](references/recommended-apps.json) <br>
- [templates.json](references/templates.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Code] <br>
**Output Format:** [Markdown guidance with JavaScript, shell command, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to return RunningHub task results and media URLs while using the configured RHMCP tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
