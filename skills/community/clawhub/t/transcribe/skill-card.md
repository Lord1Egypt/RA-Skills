## Description: <br>
Transcribe audio files to text using local Whisper (Docker). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javicasper](https://clawhub.ai/user/javicasper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to transcribe local audio files such as voice messages, meetings, and uploaded clips, then return the resulting text to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer is incomplete and attempts to install a missing transcribe wrapper into a system-wide path with sudo. <br>
Mitigation: Read the installer before running it, avoid system-wide installation until the missing wrapper is supplied and reviewed, or change installation to a user-local path. <br>
Risk: The Docker build fetches external Python and model dependencies during installation. <br>
Mitigation: Build in a controlled environment, review fetched dependencies, and verify the resulting Docker image before relying on transcripts. <br>
Risk: Transcription quality depends on the selected language and model settings. <br>
Mitigation: Verify the language argument and review transcripts, especially when using automatic language detection or accuracy-sensitive audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/javicasper/transcribe) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript with shell command usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Docker-based transcription and prints the transcript to stdout.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
