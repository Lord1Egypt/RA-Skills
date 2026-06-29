## Description: <br>
Sogni Creative Agent Skill lets agents generate and edit images, videos, and music through the Sogni AI CLI, including personas, memories, style transfer, hosted workflows, and creative media references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krunkosaurus](https://clawhub.ai/user/krunkosaurus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to route natural-language creative requests into Sogni image, video, music, persona, memory, and hosted workflow operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Sogni API key for authenticated generation. <br>
Mitigation: Store the key only in the documented credentials file or environment variable, keep it out of repositories and chats, and restrict file permissions on local credentials. <br>
Risk: Hosted modes can upload referenced media to Sogni for remote processing. <br>
Mitigation: Use direct CLI mode for private media that should remain local, and confirm before uploading sensitive reference images, audio, or video. <br>
Risk: Generation uses Sogni credits and may spend account balance. <br>
Mitigation: Check balance and cost controls before large or repeated generations, and confirm user intent before actions that consume credits. <br>
Risk: Personas, voice clips, memories, and preferences may be stored under ~/.config/sogni. <br>
Mitigation: Avoid saving unnecessary sensitive identity assets, review stored persona and memory data periodically, and purge or back up the directory during uninstall according to user preference. <br>
Risk: Automatic update notices may disclose version state or interrupt agent workflows. <br>
Mitigation: Disable or snooze update checks when automatic version notices are not wanted, and keep JSON stdout separate from advisory stderr. <br>


## Reference(s): <br>
- [Sogni Homepage](https://sogni.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/krunkosaurus/sogni-creative-agent-skill) <br>
- [Hosted API Guide](references/hosted-api.md) <br>
- [Model Guide](references/models.md) <br>
- [OpenClaw Configuration Guide](references/openclaw-config.md) <br>
- [Personas and Memory Guide](references/personas-memory.md) <br>
- [Video Editing Guide](references/video-editing.md) <br>
- [Video Prompting Guide](references/video-prompting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with CLI commands, configuration steps, JSON command output, and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media should be saved to the user's current working directory unless another location is explicitly requested.] <br>

## Skill Version(s): <br>
3.6.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
