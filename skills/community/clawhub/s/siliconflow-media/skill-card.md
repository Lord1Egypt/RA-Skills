## Description: <br>
SiliconFlow media service skill for image generation with FLUX and Qwen models, video generation with Wan models, text-to-speech, and automatic speech recognition using voucher-backed SiliconFlow API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axdlee](https://clawhub.ai/user/axdlee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate images, videos, speech audio, and speech transcriptions through SiliconFlow from prompts or selected media files. It is intended for workflows where sending those prompts, text, images, or audio to SiliconFlow under the user's API key is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, text, images, and audio selected by the user are sent to SiliconFlow under the user's API key. <br>
Mitigation: Use only inputs that are acceptable for third-party processing and avoid confidential or regulated media unless SiliconFlow handling terms meet the user's requirements. <br>
Risk: Media generation and transcription consume the user's SiliconFlow account balance or vouchers. <br>
Mitigation: Confirm the intended API key, billing arrangement, and voucher balance before running high-volume or long video generation jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axdlee/siliconflow-media) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Text] <br>
**Output Format:** [Markdown guidance with command examples; generated media files and text transcription output from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SILICONFLOW_API_KEY and saves generated media locally when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
