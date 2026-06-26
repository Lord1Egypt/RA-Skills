## Description: <br>
This skill helps agents configure and use local Qwen3-based text-to-speech and voice cloning workflows on Apple Silicon macOS systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsalfkjaklsdfjqw](https://clawhub.ai/user/dsalfkjaklsdfjqw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and accessibility teams use this skill to set up local speech synthesis, voice cloning, and batch audio generation for audiobooks, narration, character voices, and assistive applications. Voice cloning use requires consent for the source voice and appropriate disclosure of synthetic audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script may download Homebrew, Python packages, and a large model from external sources. <br>
Mitigation: Review the install script before execution, run it in an appropriate local environment, and confirm external downloads are acceptable for the deployment. <br>
Risk: Voice cloning can be misused to imitate people without consent or to create misleading audio. <br>
Mitigation: Clone only voices the user owns or has explicit permission to use, and disclose synthetic audio where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dsalfkjaklsdfjqw/qwen3-free-tts) <br>
- [OpenClaw voice cloning documentation](https://docs.openclaw.ai/skills/voice-cloning) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide generation of local WAV audio files when the user runs the provided demo or API examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, _meta.json, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
