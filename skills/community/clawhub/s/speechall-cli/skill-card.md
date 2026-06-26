## Description: <br>
Install and use the speechall CLI tool for speech-to-text transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atacan](https://clawhub.ai/user/atacan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and terminal users use this skill to install and operate the speechall CLI for transcribing audio or video files, listing speech-to-text models, and configuring transcription options such as diarization, subtitles, language, and model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio or video selected for transcription is sent to an external transcription service and may contain sensitive content. <br>
Mitigation: Only transcribe recordings the user is authorized and comfortable sending to the service. <br>
Risk: The Speechall API key can be exposed if placed directly in shell commands or logs. <br>
Mitigation: Prefer the SPEECHALL_API_KEY environment variable and keep the key private. <br>
Risk: Installing the CLI from an unexpected Homebrew tap or release source could install software the user did not intend to trust. <br>
Mitigation: Confirm the Homebrew tap or GitHub release is the intended Speechall source before installation. <br>


## Reference(s): <br>
- [Speechall CLI GitHub releases](https://github.com/Speechall/speechall-cli/releases) <br>
- [Speechall API keys](https://speechall.com/console/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI commands, option tables, JSON model-list output guidance, and redirection examples for transcript files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
