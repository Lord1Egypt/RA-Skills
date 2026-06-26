## Description: <br>
Turns assistant reply text into generated speech using Noiz AI TTS and saves the audio locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardx0319](https://clawhub.ai/user/richardx0319) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert chat replies or supplied text into playable speech files, with optional Noiz voice selection, reference audio, and timeline rendering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assistant reply text, optional reference audio, and subtitle text can be sent to Noiz. <br>
Mitigation: Use the skill only with text and audio you are permitted to share with Noiz, or choose the local Kokoro backend where appropriate. <br>
Risk: The skill can store a Noiz API key in the user's home directory. <br>
Mitigation: Configure keys only on trusted machines, protect the key file, and rotate the key if the environment is shared or compromised. <br>
Risk: The skill may install the requests dependency at runtime. <br>
Mitigation: Install dependencies from trusted sources before use and review the environment before allowing runtime package installation. <br>
Risk: Generated audio can be saved and played locally, and previous generated audio may be deleted. <br>
Mitigation: Set explicit output paths for files that should be retained and review local playback and deletion behavior before enabling automatic voice replies. <br>
Risk: Reference-audio URLs and save_voice can enable remote voice-cloning behavior. <br>
Mitigation: Avoid remote reference-audio URLs and save_voice unless users have consent and intentionally want voice-cloning features. <br>


## Reference(s): <br>
- [Voice Reply on ClawHub](https://clawhub.ai/richardx0319/voice-reply-oc) <br>
- [Noiz AI](https://noiz.ai) <br>
- [Noiz API Keys](https://developers.noiz.ai/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, audio files, subtitle files, guidance] <br>
**Output Format:** [Command-line text plus generated audio files and optional SRT files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio may be saved locally and played through the host audio system.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
