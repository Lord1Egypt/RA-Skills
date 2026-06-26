## Description: <br>
Text-to-Speech and Speech-to-Text integration using Resemble AI HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Adriano-VR](https://clawhub.ai/user/Adriano-VR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate MP3 speech from text and transcribe uploaded speech audio through Resemble AI's HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, uploaded audio, and the Resemble API key are sent to Resemble AI. <br>
Mitigation: Use only approved content, avoid sensitive or regulated data unless third-party processing is approved, and prefer a limited API key. <br>
Risk: Unusual quotes or special characters in TTS text can cause malformed requests. <br>
Mitigation: Review or escape text before synthesis, especially when it contains quotes or unusual characters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Adriano-VR/ressemble) <br>
- [Resemble AI Speech-to-Text API endpoint](https://app.resemble.ai/api/v2/speech-to-text) <br>
- [Resemble AI Synthesis API endpoint](https://f.cluster.resemble.ai/synthesize) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration] <br>
**Output Format:** [Plain text transcripts, MEDIA file paths for generated MP3 audio, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RESEMBLE_API_KEY and local curl, jq, and base64; selected text and audio are sent to Resemble AI.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
