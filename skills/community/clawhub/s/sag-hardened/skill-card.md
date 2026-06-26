## Description: <br>
ElevenLabs text-to-speech with mac-style say UX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate ElevenLabs speech audio through a mac-style command-line workflow, including voice selection, pronunciation guidance, and local playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive ElevenLabs API key. <br>
Mitigation: Keep the key in a secure environment variable and avoid pasting, logging, or passing the key as a command-line argument. <br>
Risk: Large or unbounded audio generation batches can incur API costs. <br>
Mitigation: Confirm before running broad voice or model iteration and keep batch scope explicit. <br>
Risk: Generated audio or credentials could be sent to external services unintentionally. <br>
Mitigation: Keep generated audio local unless the user intentionally chooses to share it through their own workflow. <br>
Risk: Installation uses a third-party Homebrew tap. <br>
Mitigation: Review the tap before installing and keep the sag binary updated through trusted package-management practices. <br>


## Reference(s): <br>
- [Sag Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/sag-hardened) <br>
- [Sag homepage](https://sag.sh) <br>
- [Faberlens safety evaluation for sag](https://faberlens.ai/explore/sag) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and local audio file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local MP3 files through the sag CLI when voice replies are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
