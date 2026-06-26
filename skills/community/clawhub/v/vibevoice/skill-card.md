## Description: <br>
Local Spanish TTS using Microsoft VibeVoice. Generate natural voice audio from text, optimized for WhatsApp voice messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javier887](https://clawhub.ai/user/javier887) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to generate local Spanish text-to-speech audio files, especially WhatsApp-compatible OGG voice messages, from inline text or text files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice selection and environment-derived values can lead to local code execution if supplied from untrusted input. <br>
Mitigation: Review and constrain the script before installation, keep voice names on a known allowlist, and do not pass untrusted voice names or environment values. <br>
Risk: Loading arbitrary .pt voice files can execute unsafe local model artifacts. <br>
Mitigation: Use a pinned, isolated VibeVoice environment and avoid loading arbitrary .pt voice files. <br>


## Reference(s): <br>
- [VibeVoice GitHub repository](https://github.com/microsoft/VibeVoice) <br>
- [ClawHub skill page](https://clawhub.ai/javier887/vibevoice) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text, guidance] <br>
**Output Format:** [Markdown with bash examples and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local .ogg, .mp3, or .wav audio files through the bundled shell script.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
