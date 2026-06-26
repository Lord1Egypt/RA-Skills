## Description: <br>
Use Chanjing TTS API to synthesize speech from text, using user-provided voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyuting214](https://clawhub.ai/user/zuoyuting214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to create a cloned voice from a publicly accessible reference audio URL, submit text for Chanjing text-to-speech synthesis, and retrieve the generated audio URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the reference voice URL and synthesis text to the Chanjing API. <br>
Mitigation: Use only voice samples the user has permission to clone and avoid confidential or sensitive synthesis text. <br>
Risk: The skill depends on local Chanjing credentials stored in a credentials file. <br>
Mitigation: Store credentials with restrictive permissions and rotate the key when the skill is no longer used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zuoyuting214/zyt-tts-voice-clone) <br>
- [Chanjing Open API](https://open-api.chanjing.cc) <br>
- [Chanjing OpenAPI login](https://www.chanjing.cc/openapi/login) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with API request examples, shell commands, and generated audio URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Chanjing voice IDs, task IDs, task status, subtitles, and generated audio download URLs.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
