## Description: <br>
Windows SAPI5 text-to-speech with Neural voices for generating WAV files or playing speech on Windows 10/11 without GPU use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Korddie](https://clawhub.ai/user/Korddie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Windows users use this skill to create a PowerShell helper that converts text into local WAV files with installed SAPI5 voices and optionally plays the result immediately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated PowerShell helper writes WAV output to local paths. <br>
Mitigation: Review the script before saving it and choose output paths you trust. <br>
Risk: The optional -Play flag plays generated audio aloud immediately. <br>
Mitigation: Use -Play only in environments where immediate audible playback is intended. <br>
Risk: The helper depends on Windows SAPI voices and is not portable to non-Windows systems. <br>
Mitigation: Install and run it only on Windows systems where SAPI voices are intended to be used. <br>


## Reference(s): <br>
- [Sapi Tts on ClawHub](https://clawhub.ai/Korddie/sapi-tts) <br>
- [NaturalVoiceSAPIAdapter](https://github.com/gexgd0419/NaturalVoiceSAPIAdapter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local PowerShell TTS helper that can generate WAV files and optionally play audio immediately.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
