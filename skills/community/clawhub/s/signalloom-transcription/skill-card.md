## Description: <br>
Transcribe audio and video files using the Signal Loom AI API. Supports MP3, WAV, M4A, MP4, MOV, and more. Runs locally on Apple Silicon for speed and privacy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avale-slai](https://clawhub.ai/user/avale-slai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to transcribe meetings, podcasts, videos, and other media into searchable transcripts, subtitles, captions, or agent pipeline inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privacy behavior is unclear because the evidence flags unresolved claims about whether audio and video stay local or are uploaded to Signal Loom. <br>
Mitigation: Confirm data handling with the publisher before processing sensitive media. <br>
Risk: The runtime transcribe executable is missing from the reviewed artifact, leaving core behavior unavailable for review. <br>
Mitigation: Request the complete runtime binary or source for review before installation or deployment. <br>
Risk: The installer modifies .zshrc and sends install-time analytics. <br>
Mitigation: Review the installer before running it, and install only if PATH changes and analytics behavior are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/avale-slai/signalloom-transcription) <br>
- [Publisher profile](https://clawhub.ai/user/avale-slai) <br>
- [Signal Loom signup](https://signalloomai.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with transcription commands; generated transcripts may be JSON, SRT, VTT, or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a transcribe binary and a Signal Loom API key; supported media types include MP3, WAV, M4A, MP4, and MOV.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
