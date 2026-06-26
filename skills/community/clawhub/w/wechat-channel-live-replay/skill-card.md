## Description: <br>
Downloads WeChat Channels live replay videos for a selected channel and date, with optional Whisper transcription for downstream replay analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to retrieve WeChat Channels live replays, save video and transcript artifacts, and prepare inputs for live replay analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TikHub API token and calls external TikHub endpoints. <br>
Mitigation: Use a limited TikHub token, store it only in the expected config or environment location, and review network access before running the skill. <br>
Risk: User-provided channel names and dates are used in output paths. <br>
Mitigation: Avoid channel names or dates containing slashes, '..', or other path-like text, and run the skill in a constrained workspace until output path handling is fixed. <br>
Risk: The skill downloads media and depends on local ffmpeg and Python packages. <br>
Mitigation: Install ffmpeg and Python dependencies only from trusted sources, and review downloaded media handling before use in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ahsbnb/wechat-channel-live-replay) <br>
- [ffmpeg Download Documentation](https://ffmpeg.org/download.html) <br>
- [TikHub API Base](https://api.tikhub.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [Video file, plain text transcript, JSON report, and terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TikHub token, ffmpeg, requests, and openai-whisper; supports optional date selection, output directory selection, and download-only mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
