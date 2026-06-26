## Description: <br>
Local text-to-voice generation for OpenClaw workspaces using a canonical txt-to-mp3 pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[betonimig](https://clawhub.ai/user/betonimig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to convert prepared text files into MP3 voice output through a reusable local workspace workflow with stable input, output, and state paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents itself as local while its node-edge-tts backend may send text outside the local workspace. <br>
Mitigation: Use only with text that is acceptable to send to an external TTS provider, or replace the backend with a verifiably offline TTS engine. <br>
Risk: Secrets, private messages, customer data, or proprietary documents could be exposed during voice generation. <br>
Mitigation: Do not process sensitive or proprietary text unless the provider and data flow are clearly disclosed and approved for that data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/betonimig/text-to-voice-local) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated MP3 file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a canonical MP3 at tmp/voice-mode-latest.mp3 and updates skill state pointers.] <br>

## Skill Version(s): <br>
1.4.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
