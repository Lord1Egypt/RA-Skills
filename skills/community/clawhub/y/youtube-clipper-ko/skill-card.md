## Description: <br>
Splits Korean YouTube videos or local video files into short-form clips by transcribing audio, selecting viral candidate segments, adding Korean subtitles, and writing clip metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thedalbee](https://clawhub.ai/user/thedalbee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and video workflow operators use this skill to turn Korean long-form videos into candidate Shorts, Reels, or TikTok clips with transcript-based segment analysis, subtitles, and reviewable metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal use sends extracted audio to OpenAI for transcription and transcript text to Anthropic for clip selection. <br>
Mitigation: Do not process private, confidential, unreleased, or restricted media unless that external processing is approved for the content. <br>
Risk: Generated media, transcripts, and metadata remain on disk after the run. <br>
Mitigation: Review output directories after use and delete source media, transcripts, clips, and metadata that should not be retained. <br>
Risk: The skill may be used on copyrighted or third-party media. <br>
Mitigation: Confirm rights, permissions, and platform rules before downloading, editing, or publishing clips. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thedalbee/youtube-clipper-ko) <br>
- [Clawitzer optional integration](https://github.com/thedalbee/clawitzer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands plus generated MP4 and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped output folders containing source media, transcript JSON, viral segment JSON, MP4 clips, and result metadata.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
