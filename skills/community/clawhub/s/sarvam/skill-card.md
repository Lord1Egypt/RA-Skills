## Description: <br>
Use Sarvam AI for Indian language Text-to-Speech (TTS), Speech-to-Text (STT), Translation, and Chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iammhk](https://clawhub.ai/user/iammhk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call Sarvam AI for Indian-language speech generation, transcription, translation, and chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, prompts, and audio files are sent to Sarvam AI for processing. <br>
Mitigation: Use the skill only with data that is allowed under Sarvam's terms and your organization's data-handling requirements. <br>
Risk: The skill requires a Sarvam API key. <br>
Mitigation: Provide SARVAM_API_KEY through a controlled environment variable and avoid committing or sharing the key. <br>
Risk: Dependency provenance may matter when using the bundled local Python environment. <br>
Mitigation: Recreate the local Python environment from trusted package sources before deployment when dependency provenance is required. <br>


## Reference(s): <br>
- [Sarvam AI API](https://api.sarvam.ai) <br>
- [ClawHub skill page](https://clawhub.ai/iammhk/sarvam) <br>
- [Publisher profile](https://clawhub.ai/user/iammhk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API responses, plain text chat responses, and generated audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SARVAM_API_KEY; text, prompts, and selected audio files are sent to Sarvam AI for processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
