## Description: <br>
Production-ready Volcengine/ARK video generation for prompt-to-video, image-to-video, and draft-video refinement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinhuadeng](https://clawhub.ai/user/jinhuadeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-production agents use this skill to run real Volcengine/ARK video generation tasks from text prompts, reference images, or draft clips, then poll task status, inspect returned payloads, and download completed video outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts or media may be sent to the configured remote video provider, and the scanner notes the skill can unexpectedly use OpenAI environment credentials as fallbacks. <br>
Mitigation: Use only prompts and media appropriate for the configured provider; explicitly set VOLCENGINE_API_KEY or ARK_API_KEY and endpoint, and clear OPENAI_API_KEY or OPENAI_BASE_URL unless those fallbacks are intentional. <br>
Risk: Generated files may be saved locally by default. <br>
Mitigation: Disable result downloads or set --download-dir when saving generated files to Desktop is not desired. <br>
Risk: The authoritative security verdict is suspicious and recommends review before installation. <br>
Mitigation: Review the skill and its runtime configuration before installing or executing it. <br>


## Reference(s): <br>
- [Volcengine Video Studio on ClawHub](https://clawhub.ai/jinhuadeng/volcengine-video-studio) <br>
- [Publisher profile: jinhuadeng](https://clawhub.ai/user/jinhuadeng) <br>
- [API notes](references/api-notes.md) <br>
- [Sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download generated video files to a local directory when downloads are enabled.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
