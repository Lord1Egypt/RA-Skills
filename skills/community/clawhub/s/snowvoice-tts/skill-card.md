## Description: <br>
SnowVoice TTS helps agents use a local SnowVoice Studio and Qwen3-TTS setup to synthesize Chinese speech, clone authorized voices, design voices, and return generated audio paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webkubor](https://clawhub.ai/user/webkubor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to convert Chinese text into speech, list available voices, clone authorized voice personas, or design new voice styles through a local SnowVoice CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can run an installer from a mutable upstream GitHub repository. <br>
Mitigation: Install only after reviewing the upstream installer, confirming the install path, and trusting the SnowVoice Studio project. <br>
Risk: Voice cloning can be misused when the voice owner has not authorized use. <br>
Mitigation: Use cloning only with permission from the voice owner and review generated audio before distribution. <br>
Risk: The setup downloads large persistent model files locally. <br>
Mitigation: Confirm disk space and model storage location before setup, and run the status check before generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/webkubor/snowvoice-tts) <br>
- [SnowVoice Studio repository](https://github.com/webkubor/snowvoice-studio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [JSON status messages, shell commands, and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local SnowVoice Studio installation, large model downloads, and macOS Apple Silicon according to the artifact documentation.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
