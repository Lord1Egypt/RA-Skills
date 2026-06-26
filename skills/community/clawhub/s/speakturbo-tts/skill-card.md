## Description: <br>
Speak Turbo lets an agent turn text into local speech output with fast built-in text-to-speech voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EmZod](https://clawhub.ai/user/EmZod) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to let an assistant speak responses aloud, play local audio by default, save WAV output when requested, and list or select the included voices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can play generated speech aloud by default, which may expose sensitive text in shared spaces. <br>
Mitigation: Avoid speaking highly sensitive text in shared environments; save to a file only when needed and review the text before playback. <br>
Risk: The skill can create local WAV files and supports a permanent output allowlist. <br>
Mitigation: Keep output directories narrow and avoid adding broad paths such as the whole home directory to the permanent allowlist. <br>
Risk: The skill runs a disclosed localhost text-to-speech daemon. <br>
Mitigation: Use it only on systems where a local TTS daemon and localhost service are acceptable, and stop the daemon when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EmZod/speakturbo-tts) <br>
- [Speak Turbo website](https://speakturbo-site.vercel.app) <br>
- [Pocket TTS](https://github.com/kyutai-labs/pocket-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and WAV audio file output when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May play audible speech locally by default and can save WAV files to allowed output directories.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
