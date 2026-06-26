## Description: <br>
Extract audio from video URLs and transcribe using STT (Speech-to-Text). Supports local Whisper or cloud APIs. Use when: user provides a video URL and wants to know what is being said, transcribing YouTube videos, podcasts, or any video with audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[damienCronw](https://clawhub.ai/user/damienCronw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to extract audio from video URLs and generate speech-to-text transcripts for videos, podcasts, and other media with audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal use can download media, create transcript and audio files, create a Python virtual environment, and install Homebrew or Python packages. <br>
Mitigation: Review scripts before use, install dependencies from trusted sources, and run the skill in a controlled workspace. <br>
Risk: Crafted option values passed to the shell wrapper could run unintended local code. <br>
Mitigation: Avoid untrusted option values and prefer the Python entry point or reviewed command invocations for untrusted inputs. <br>
Risk: The artifact advertises cloud transcription, but server security guidance says cloud transcription is not actually implemented in this version. <br>
Mitigation: Use local Whisper mode for this release and do not provide cloud API keys for the unimplemented cloud path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/damienCronw/video-stt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated transcripts as TXT, SRT, VTT, or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local audio, transcript, and Python virtual environment files during execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
