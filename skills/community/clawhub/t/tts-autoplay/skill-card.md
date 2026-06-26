## Description: <br>
Auto-play TTS voice files with wake word detection so audio plays only when user messages include configured wake words. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WangZjhz](https://clawhub.ai/user/WangZjhz) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
OpenClaw users on Windows use this skill to configure conditional text-to-speech playback for webchat responses. It is intended for users who want mostly text responses with on-demand voice output triggered by wake words or tagged TTS mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package references PowerShell scripts that were not present in the artifact, so install and start behavior cannot be verified from the package evidence. <br>
Mitigation: Do not run referenced scripts unless they are present, trusted, and inspected; avoid execution-policy bypass for unverified scripts. <br>
Risk: Voice playback can expose unintended content in shared or sensitive environments if TTS is always enabled or wake phrases are too broad. <br>
Mitigation: Prefer tagged TTS mode, configure explicit wake phrases, and test both text-only and wake-word messages before daily use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WangZjhz/tts-autoplay) <br>
- [README.md](README.md) <br>
- [WAKE-WORD-DESIGN.md](WAKE-WORD-DESIGN.md) <br>
- [WAKE-WORD-SUMMARY.md](WAKE-WORD-SUMMARY.md) <br>
- [examples/config-example.json](examples/config-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with PowerShell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Windows OpenClaw TTS setup; referenced executable scripts were not present in the package evidence.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
