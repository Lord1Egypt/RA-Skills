## Description:

Downloads videos, extracts transcripts, and captures frames for analyzing YouTube, tutorial, podcast, due diligence, and meeting recordings with yt-dlp, Whisper, and ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zedit42](https://clawhub.ai/user/zedit42)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and other external users use this skill to turn remote video content into local transcripts, subtitle files, and frame captures for review, note-taking, summaries, and due diligence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads user-supplied remote videos and processes media locally, which can consume substantial disk, CPU, and model-download bandwidth.

Mitigation: Run it in an environment with adequate local resources, choose output directories deliberately, and monitor long videos or large Whisper models.

Risk: Generated transcripts may contain private recordings, credentials, meeting details, or confidential business content.

Mitigation: Review transcripts and extracted frames before sharing them or piping them to any AI service.

## Reference(s):

- [Video Analyzer on ClawHub](https://clawhub.ai/zedit42/skills/videoanalyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands plus generated transcript, subtitle, media, and image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes outputs under a configurable output directory; transcript summary prompts include up to the first 50000 characters.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
