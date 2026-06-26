## Description: <br>
Converts user-provided text into spoken MP3 audio through a hosted text-to-speech API with provider, voice, emotion, rate, and pitch options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengwm64](https://clawhub.ai/user/fengwm64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate narration, voiceovers, read-aloud audio, or browser-playable TTS links from supplied text while selecting providers, voices, and speech tuning parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text supplied for speech synthesis is sent to an external TTS service. <br>
Mitigation: Do not submit secrets, private documents, regulated data, or sensitive personal content unless the external service is trusted for that data. <br>
Risk: Generated MP3 files may remain on disk after use. <br>
Mitigation: Store generated audio only in intended output locations and delete files that should not persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengwm64/tts-api) <br>
- [Publisher profile](https://clawhub.ai/user/fengwm64) <br>
- [TTS API base URL](https://tts.102465.xyz) <br>
- [TTS endpoint](https://tts.102465.xyz/api/tts) <br>
- [Azure voices endpoint](https://tts.102465.xyz/api/voices?provider=azure) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Files] <br>
**Output Format:** [Markdown guidance with curl examples, generated MP3 files, and optional browser-playable URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is MP3; GET requests require URL-encoded text and parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
