## Description: <br>
Download and generate clean, readable transcripts from any YouTube video. Extracts subtitles (auto-generated or manual), removes timestamps and formatting, and outputs a clean paragraph-style transcript. Use when asked to transcribe, get transcript, or extract text from a YouTube video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[floriandarroman](https://clawhub.ai/user/floriandarroman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, content operators, and external users use this skill to retrieve subtitles from a YouTube URL and turn them into a readable transcript, optionally preserving timestamps or selecting a language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses yt-dlp to access YouTube and retrieve subtitle data. <br>
Mitigation: Install and run it only if you are comfortable using yt-dlp for the target video source. <br>
Risk: Transcript text is saved to disk and may include sensitive content from the source video. <br>
Mitigation: Avoid transcribing sensitive videos in synced or shared folders, and provide an explicit output path when you need control over where the transcript is stored. <br>


## Reference(s): <br>
- [YouTube Transcript Generator on ClawHub](https://clawhub.ai/floriandarroman/youtube-transcript-generator) <br>
- [OpenClaw Lab](https://openclawlab.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text transcript with optional timestamp markers; Markdown usage guidance with bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves a local transcript file and prints the transcript to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
