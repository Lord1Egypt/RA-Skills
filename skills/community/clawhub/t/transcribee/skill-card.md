## Description:

Transcribe YouTube videos and local audio/video files with speaker diarization. Use when user asks to transcribe a YouTube URL, podcast, video, or audio file. Outputs clean speaker-labeled transcripts ready for LLM analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsfabioroma](https://clawhub.ai/user/itsfabioroma)

### License/Terms of Use:

ISC

## Use Case:

Developers and external users can use this skill to transcribe online or local audio/video media into speaker-labeled transcripts and metadata for later LLM analysis or personal knowledge organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private, regulated, copyrighted, or sensitive media may be uploaded to external AI services for transcription and categorization.

Mitigation: Review data handling obligations before use and only process media that is authorized for ElevenLabs and Anthropic processing.

Risk: Transcripts and metadata are stored persistently under the user's Documents directory.

Mitigation: Confirm local storage permissions and retention expectations, then delete or protect transcript folders that contain sensitive content.

Risk: The output category path is selected by a model and is reported by the security scan as unsafe.

Mitigation: Validate and restrict generated category paths before routine use so writes remain inside the intended transcript directory.

Risk: URL input handling depends on downloader behavior and the security guidance calls for restricting supported URLs.

Mitigation: Limit URL inputs to documented supported services and add explicit URL allowlisting before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itsfabioroma/skills/transcribee)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
- [ElevenLabs](https://elevenlabs.io/)
- [Anthropic](https://anthropic.com/)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, configuration]

**Output Format:** [Speaker-labeled plain text transcript, metadata JSON, optional raw transcription JSON, and terminal progress output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcript artifacts under ~/Documents/transcripts/{category}/{title-date}/ and requires ElevenLabs and Anthropic API keys.]

## Skill Version(s):

1.2.1 (source: server release metadata; package.json declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
