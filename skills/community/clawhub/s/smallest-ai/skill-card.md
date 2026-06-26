## Description: <br>
Ultra-fast text-to-speech and speech-to-text through Smallest AI's Lightning v3.1 and Pulse models for generating speech, transcribing audio, and handling multilingual voice workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhishekmishragithub](https://clawhub.ai/user/abhishekmishragithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add Smallest AI voice workflows to an agent, including speech generation, audio transcription, voice notes, multilingual output, speaker diarization, timestamps, and emotion detection options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, audio recordings, transcripts, and related options are sent to Smallest AI for processing. <br>
Mitigation: Use the skill only for content that is appropriate to send to Smallest AI, and avoid confidential, regulated, or third-party recordings without consent. <br>
Risk: The SMALLEST_API_KEY credential is required for API calls. <br>
Mitigation: Keep the API key private, store it in the environment rather than in prompts or files, and rotate it if it may have been exposed. <br>
Risk: Generated audio can be saved to local files, and custom output paths may overwrite existing files. <br>
Mitigation: Review custom --out paths before running the TTS scripts and use dedicated output directories for generated media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhishekmishragithub/smallest-ai) <br>
- [Smallest AI API reference](references/api-reference.md) <br>
- [Supported languages](references/languages.md) <br>
- [Voice catalog](references/voices.md) <br>
- [Smallest AI Waves console](https://waves.smallest.ai) <br>
- [Smallest AI Waves documentation](https://waves-docs.smallest.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, audio files, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scripts return MEDIA file paths for generated audio or JSON/text transcripts for speech-to-text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and SMALLEST_API_KEY; Python scripts are optional for SDK or requests-based usage.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
