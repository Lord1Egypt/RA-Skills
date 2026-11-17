## Description: <br>
Helps creators write professional AI video prompts and optionally generate MP4 videos through the Seedance 2.0-backed RedFox API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, content operators, and creative teams use this skill to turn video ideas into structured cinematography prompts, diagnose common AI video issues, and optionally submit prompts for MP4 generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced media may be sent to the video provider and may consume API credits. <br>
Mitigation: Use the skill only when this data sharing and credit usage are acceptable, and avoid sensitive prompts or private media URLs. <br>
Risk: Generated shell commands can submit API jobs and download files. <br>
Mitigation: Review commands before execution and choose an explicit download location. <br>
Risk: API keys can be exposed if copied into prompts, logs, scripts, or output files. <br>
Mitigation: Prefer environment or local configuration storage for REDFOX_API_KEY and avoid hard-coding or sharing the key. <br>


## Reference(s): <br>
- [Core Workflow](references/core_workflow.md) <br>
- [ClawHub release page](https://clawhub.ai/redfox-data/skills/video-prompt-expert) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated videos are downloaded as MP4 files when the API flow is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports prompt writing, template guidance, issue diagnosis, and API-backed generation settings such as duration, aspect ratio, resolution, seed, audio, watermark, reference image, and output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
