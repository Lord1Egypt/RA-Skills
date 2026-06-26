## Description: <br>
Fast on-device speech-to-text using Apple Speech.framework (macOS 26+). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobihagemann](https://clawhub.ai/user/tobihagemann) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and macOS users use this skill to transcribe audio or video files with the yap CLI, including locale selection and TXT or SRT output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on a third-party Homebrew CLI. <br>
Mitigation: Install only when the publisher and Homebrew formula are acceptable for the environment. <br>
Risk: Transcription may process private audio or video content and newer live-audio features may trigger macOS privacy prompts. <br>
Mitigation: Use the CLI only with files intended for transcription and review macOS microphone or system-audio prompts before granting access. <br>
Risk: Transcript output paths can save text or captions to disk. <br>
Mitigation: Review output locations before using the output-file option. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobihagemann/yap) <br>
- [yap project homepage](https://github.com/finnvoor/yap) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is specific to macOS and the yap CLI; transcript files may be written as TXT or SRT when the user requests an output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
