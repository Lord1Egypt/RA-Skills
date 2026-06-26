## Description: <br>
Tts Voice Generator helps an agent browse voices, upload custom voice samples, generate speech from text, and check asynchronous task status through Datamass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanfeng1234](https://clawhub.ai/user/seanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to turn supplied text into speech, choose or upload a voice sample, and retrieve task results from the Datamass TTS service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text, transcripts, voice samples, and selected local audio files may be sent to Datamass. <br>
Mitigation: Use the skill only with content and voices you have permission to share, and avoid sensitive recordings or third-party voices without consent. <br>
Risk: The skill uses a stored Datamass API key. <br>
Mitigation: Use a dedicated scoped API key for this service, protect the local configuration file, and rotate or revoke the key if it may be exposed. <br>
Risk: Custom voices may persist without strong confirmation of deletion controls. <br>
Mitigation: Confirm retention and deletion options before uploading personal or third-party voice samples. <br>
Risk: Speech generation can consume paid Datamass credits. <br>
Mitigation: Confirm account balance and expected usage cost before submitting generation jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanfeng1234/tts-voice-generator) <br>
- [Datamass](https://www.datamass.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses and JSON-like result objects containing voice lists, task IDs, task status, or audio URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Datamass API key and may send text, transcripts, voice samples, and selected local audio files to Datamass.] <br>

## Skill Version(s): <br>
1.3.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
