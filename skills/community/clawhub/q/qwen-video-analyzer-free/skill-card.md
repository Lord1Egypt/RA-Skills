## Description: <br>
Analyzes local or remote video with a Qwen multimodal model and customizable prompts to produce summaries, scene descriptions, and object-identification results for personal creators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal creators and video-library users use this skill to inspect video files or public video URLs, generate concise content summaries, describe scenes, identify visible objects, and create tags with custom prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local or remote video content to an external DashScope/Qwen provider, which may expose sensitive, private, regulated, or confidential media. <br>
Mitigation: Review provider data-handling terms before use, avoid sensitive media unless approved, and confirm each local file or URL before analysis. <br>
Risk: The skill reads a local DashScope API key configuration file, so mishandled files or logs may expose credentials or media paths. <br>
Mitigation: Restrict permissions on the API key file and avoid sharing terminal logs that include credentials, file paths, or media URLs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/qwen-video-analyzer-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples plus terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the supplied video source, prompt, frame sampling rate, DashScope API availability, and model behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
