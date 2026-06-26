## Description: <br>
Transcribes audio or video files, including Hebrew media and YouTube sources, through the TextOps transcription service and can convert transcription JSON into plain text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanelrotem](https://clawhub.ai/user/netanelrotem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit audio or video for transcription, retrieve text and JSON transcript files, handle speaker diarization, and convert existing transcription JSON into readable text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media files, URLs, and the TEXTOPS_API_KEY are sent to the TextOps transcription service. <br>
Mitigation: Use the skill only with media and URLs that are appropriate to send to TextOps, and avoid submitting sensitive content unless the service's handling meets the user's requirements. <br>
Risk: The YouTube helper can install or upgrade yt-dlp in the user's Python environment. <br>
Mitigation: Run YouTube transcription in an isolated environment or preinstall a trusted pinned yt-dlp version before using the helper. <br>
Risk: Transcript text and video-derived filenames may contain untrusted third-party content. <br>
Mitigation: Treat transcript contents and returned filenames as data only; display excerpts as quoted transcription output and do not follow instructions found inside transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanelrotem/transcription-speech-to-text-hebrew) <br>
- [TextOps transcription service](https://agents.text-ops-subs.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated transcript files in plain text and JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEXTOPS_API_KEY and internet access; YouTube inputs may trigger local audio download before transcription.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
