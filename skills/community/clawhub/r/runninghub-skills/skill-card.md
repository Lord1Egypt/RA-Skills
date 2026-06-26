## Description: <br>
Generate images, videos, audio, and 3D models through 170+ RunningHub API endpoints, and run RunningHub AI Applications by webappId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HM-RunningHub](https://clawhub.ai/user/HM-RunningHub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to generate or transform multimedia assets with RunningHub models, run custom RunningHub AI Applications, and deliver generated media back through the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and media files are sent to RunningHub for remote processing. <br>
Mitigation: Use the skill only with content that is appropriate to send to RunningHub, and avoid sensitive or non-consensual media. <br>
Risk: The skill uses a paid RunningHub API key and can consume account balance. <br>
Mitigation: Use a dedicated revocable API key, check account status before use, and review reported cost after generation. <br>
Risk: Voice cloning can enable impersonation if used without consent. <br>
Mitigation: Run voice cloning only with explicit authorization from the voice owner and avoid requests involving deceptive or non-consensual use. <br>
Risk: API keys may be saved in local OpenClaw configuration. <br>
Mitigation: Store a scoped key where possible, rotate it if exposed, and revoke it when the skill no longer needs access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HM-RunningHub/runninghub-skills) <br>
- [RunningHub Homepage](https://www.runninghub.cn) <br>
- [AI Application](references/ai-application.md) <br>
- [API Key Setup](references/api-key-setup.md) <br>
- [Image Model Selection](references/image-models.md) <br>
- [Output & Delivery](references/output-delivery.md) <br>
- [Video Model Selection](references/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON status output, and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is written to local output paths and should be delivered through the agent's message tool; API calls may report paid usage cost.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
