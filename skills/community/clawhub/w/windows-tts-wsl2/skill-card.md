## Description: <br>
Enables agents running in WSL2 on Windows 11 to speak text through Windows built-in TTS using powershell.exe and System.Speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[547895019](https://clawhub.ai/user/547895019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users in WSL2 use this skill to play assistant output directly through Windows speakers, especially for Chinese speech or when generated TTS audio files are silent or unusable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted spoken text or options may be interpreted as Windows PowerShell commands. <br>
Mitigation: Install and use only with trusted text and options; avoid reading untrusted, quoted, copied, or code-like content until the speech script is hardened with typed PowerShell parameters or safe stdin handling plus rate and volume validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/547895019/windows-tts-wsl2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directly plays speech through the Windows default audio output and does not return an audio file path.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
