## Description: <br>
Smart TTS synthesizes speech by trying configured DashScope CosyVoice model and voice combinations until one succeeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppop0uuiu](https://clawhub.ai/user/ppop0uuiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate single or batch WAV speech files from provided text with an Aliyun DashScope API key. It is useful when a preferred model or voice may be unavailable and fallback synthesis options are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to DashScope. <br>
Mitigation: Only synthesize text that is appropriate to send to DashScope under the user's data-handling requirements. <br>
Risk: A DashScope API key is required to run the scripts. <br>
Mitigation: Use a limited-purpose API key and provide it through the DASHSCOPE_API_KEY environment variable or an approved runtime configuration. <br>
Risk: Default WAV output paths can overwrite earlier generated audio files. <br>
Mitigation: Move or rename generated WAV files when older outputs need to be retained. <br>
Risk: The skill depends on the dashscope Python SDK at runtime. <br>
Mitigation: Install the SDK from a trusted package source before running the scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppop0uuiu/smart-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and generated WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; default outputs are written under ~/.openclaw/workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
