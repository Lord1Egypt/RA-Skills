## Description:

Monitors YouTube channels, extracts audio URLs through YouTube innertube requests, submits audio to AssemblyAI for cloud transcription, and returns transcript text plus an AI summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azazlf09](https://clawhub.ai/user/azazlf09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content monitoring teams use this skill to monitor YouTube channels for new videos, transcribe video audio, and generate summaries through AssemblyAI cloud processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored channel URLs may cause the skill to contact non-YouTube or internal network addresses when checking channels.

Mitigation: Only add real HTTPS YouTube channel URLs and review data/channels.json before running check until the skill enforces channel destination validation.

Risk: AssemblyAI credentials can be placed in data/config.json.

Mitigation: Prefer the ASSEMBLYAI_API_KEY environment variable and keep any config file private and out of shared artifacts.

Risk: Video audio is processed by AssemblyAI cloud services.

Mitigation: Use the skill only for content that is acceptable to send to YouTube and AssemblyAI cloud processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/azazlf09/skills/yt-assemblyai-monitor)
- [AssemblyAI signup](https://www.assemblyai.com/app/signup)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Terminal text plus JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores transcripts and summaries under data/summaries/*.json; requires an AssemblyAI API key.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
