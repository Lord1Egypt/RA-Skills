## Description: <br>
企微瓣 (Qiweiban) AI 平台 CLI 工具 that helps agents use the qwb CLI for speech synthesis, voice cloning, digital-human video generation, AI chat, image generation, and account balance workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louiseliu](https://clawhub.ai/user/louiseliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to have an agent produce qwb CLI commands and guidance for Qiweiban media-generation, AI chat, user profile, and petals balance workflows. It is most relevant when the user already intends to use the Qiweiban/qwb service and can authorize uploads or account spending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide account login and stores qwb tokens in ~/.qwb/credentials.json. <br>
Mitigation: Use it only in a trusted environment, avoid sharing passwords or SMS codes with the agent when possible, and protect or remove the credentials file when the session ends. <br>
Risk: Voice, face, image, video, and audio uploads may include biometric or personal media. <br>
Mitigation: Require explicit user confirmation and rights review before uploading personal media or creating cloned voices and digital humans. <br>
Risk: Some commands can spend account credits or consume petals. <br>
Mitigation: Confirm billable actions before execution and review qwb petals balance and history for unexpected usage. <br>
Risk: The security verdict is suspicious and recommends publisher and package review. <br>
Mitigation: Verify the npm package, qwb binary source, and publisher profile before installing or running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/louiseliu/qwb-cli) <br>
- [Publisher profile](https://clawhub.ai/user/louiseliu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text] <br>
**Output Format:** [Markdown with inline qwb CLI commands and expected JSON, table, or quiet CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying qwb CLI defaults to JSON output and may write generated media to URLs or local files when commanded.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
