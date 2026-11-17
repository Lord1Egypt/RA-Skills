## Description:

Use VLM Run (vlmrun) to generate transcriptions from YouTube videos. Download a video with yt-dlp, then run vlmrun to transcribe with optional timestamps. VLMRUN_API_KEY must be in .env; follow vlmrun-cli-skill for CLI setup and options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mehediahamed](https://clawhub.ai/user/mehediahamed)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to guide an agent through downloading a YouTube video, sending the media to VLM Run for transcription, and saving a transcript with optional timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow relies on unpinned external command-line tools.

Mitigation: Use a clean virtual environment, inspect dependencies before installation, and pin versions where repeatability is required.

Risk: Video content is processed by a third-party transcription service.

Mitigation: Only transcribe videos the user is allowed to download and is comfortable sending to VLM Run.

Risk: Credential exposure is possible if unrelated secrets are present in the shell or .env file.

Mitigation: Limit the environment used for transcription to the required VLMRUN_API_KEY and avoid exposing unrelated secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mehediahamed/skills/youtube-transcription-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and transcript file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for creating plain-text or timestamped transcript files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
