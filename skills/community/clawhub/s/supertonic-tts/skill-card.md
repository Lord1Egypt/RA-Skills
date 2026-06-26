## Description: <br>
On-device multilingual text-to-speech using Supertonic for local voice generation, speech synthesis, and text-to-audio workflows, with optional third-party voice cloning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratyushchauhan](https://clawhub.ai/user/pratyushchauhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate multilingual speech locally, select built-in Supertonic voices, create WAV audio, and prepare deployment guidance for Python or other ONNX runtimes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The first run downloads Supertonic model files, which may be unsuitable for locked-down or air-gapped environments. <br>
Mitigation: Preinstall and cache required model assets during deployment review, and confirm the environment permits the expected download path before use. <br>
Risk: Voice cloning requires uploading a reference voice clip to Supertone's online Voice Builder service. <br>
Mitigation: Use built-in offline voices for regulated, air-gapped, or highly private voice data, and only use cloning when the user has permission to upload the reference audio. <br>
Risk: Expression tags are only partially reliable, with only the laugh tag documented as user-verified in the artifact. <br>
Mitigation: Use expression tags conservatively and prefer wording, punctuation, speed settings, and manual review when emotional delivery matters. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/pratyushchauhan/supertonic-tts) <br>
- [Voice descriptions and cloning workflow](references/voices.md) <br>
- [Expression tag testing notes](references/expression-tags.md) <br>
- [Supported languages](references/languages.md) <br>
- [Deployment options](references/deployment.md) <br>
- [Supertonic repository](https://github.com/supertone-inc/supertonic) <br>
- [Supertonic Python SDK documentation](https://supertone-inc.github.io/supertonic-py/) <br>
- [Supertonic-3 model card](https://huggingface.co/Supertone/supertonic-3) <br>
- [Supertone Voice Builder](https://supertonic.supertone.ai/voice_builder) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python and shell examples; generated speech is saved as WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports 31 language codes, built-in voice IDs, optional custom voice style JSON files, speed controls, and quality step settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
