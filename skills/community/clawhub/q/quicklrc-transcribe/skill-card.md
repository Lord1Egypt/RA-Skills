## Description: <br>
Generate synced lyrics or subtitle files (LRC, SRT, WebVTT, ASS, TTML) from any audio/video URL or YouTube link using the QuickLRC AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiqingtangx](https://clawhub.ai/user/weiqingtangx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, media teams, and automation agents use this skill to generate time-synced lyrics or subtitle outputs from public audio, video, or YouTube URLs through the QuickLRC API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted media URLs and optional lyrics are sent to QuickLRC for processing. <br>
Mitigation: Avoid private, sensitive, regulated, or unauthorized copyrighted material unless use is permitted and QuickLRC terms have been reviewed. <br>
Risk: Successful transcription requests may spend QuickLRC credits. <br>
Mitigation: Confirm the target media and requested format before making API calls, and check remaining credits in the QuickLRC dashboard. <br>
Risk: The skill requires a QuickLRC API key. <br>
Mitigation: Provide the key through the QUICKLRC_API_KEY environment variable and avoid pasting credentials into shared logs, prompts, or generated files. <br>


## Reference(s): <br>
- [QuickLRC API Documentation](https://quicklrc.com/docs/api) <br>
- [QuickLRC Dashboard](https://quicklrc.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash curl examples; API responses are plain text lyric or subtitle content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports LRC, SRT, WebVTT, ASS, TTML, and TXT outputs when requested through the QuickLRC API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
