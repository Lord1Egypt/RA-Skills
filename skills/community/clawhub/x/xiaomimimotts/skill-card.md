## Description: <br>
Generate speech audio (WAV) from text using Xiaomi MiMo TTS (mimo-v2-tts model). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heimaojingzhang888](https://clawhub.ai/user/heimaojingzhang888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert supplied text into spoken audio files with selectable Xiaomi MiMo voices, style tags, dialect or emotion controls, and optional user-role context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The text to synthesize and any optional --user-msg context are sent to Xiaomi MiMo. <br>
Mitigation: Avoid confidential, regulated, or private text unless Xiaomi's terms and the user's data-handling rules permit it. <br>
Risk: The skill requires a Xiaomi MiMo API key. <br>
Mitigation: Store MIMO_API_KEY with the same care as other API credentials and avoid exposing it in commands, logs, or shared files. <br>
Risk: Generated audio is saved locally. <br>
Mitigation: Choose output paths intentionally and apply local access controls appropriate for the synthesized content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heimaojingzhang888/xiaomimimotts) <br>
- [Xiaomi MiMo API](https://api.xiaomimimo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the script writes WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MIMO_API_KEY. Sends the text to synthesize and optional --user-msg context to Xiaomi MiMo, then saves the returned audio locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
