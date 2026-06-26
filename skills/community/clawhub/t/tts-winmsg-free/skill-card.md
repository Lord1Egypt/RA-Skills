## Description: <br>
Windows local text-to-speech helper that sends visible assistant replies to a small Windows TTS window using WM_COPYDATA, with sentence splitting, queued playback, and speed and volume controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[512548510](https://clawhub.ai/user/512548510) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users on Windows use this skill to speak assistant replies aloud through a local TTS window while keeping the same reply visible in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Visible assistant replies sent to TTS may be audible to people nearby. <br>
Mitigation: Use the skill only in an environment where spoken replies are appropriate, and disable TTS mode when privacy is needed. <br>
Risk: Other local software could potentially send messages to the same Windows message target. <br>
Mitigation: Run the skill only on trusted Windows machines and close the TTS window with the documented quit command when finished. <br>
Risk: The skill invokes PowerShell and Windows speech components locally. <br>
Mitigation: Review and scan the skill before deployment, and prefer a tighter direct speech implementation when stronger local hardening is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/512548510/tts-winmsg-free) <br>
- [Project homepage](https://github.com/512548510/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and spoken text sent to a local Windows TTS process] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for Windows hosts with Python and pywin32; TTS playback uses the local Windows speech stack.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
