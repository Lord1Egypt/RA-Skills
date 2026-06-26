## Description: <br>
Generate images via VAPI's OpenAI-compatible Images API with nano-banana and gpt-image model series. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[popdo](https://clawhub.ai/user/popdo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent generate or edit images through a configured VAPI endpoint, choose supported image models and aspect ratios, and optionally save generated images locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and any image passed with --input are sent to the configured VAPI endpoint under the user's VAPI key. <br>
Mitigation: Use only trusted VAPI endpoints and avoid sending prompts or source images that contain sensitive or restricted content. <br>
Risk: Generated images may be written to local media storage when --save or --oss is used, and gpt-image models always save image files. <br>
Mitigation: Review save options before use and manage files in ~/.openclaw/media/ or ~/.openclaw/oss/ according to local data handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/popdo/vapi-image-gen) <br>
- [Publisher profile](https://clawhub.ai/user/popdo) <br>
- [VAPI API](https://api.v3.cm) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text MEDIA lines, stderr status messages, and optional saved image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [URL output is the default for nano-banana models; saved files are produced when --save or --oss is used, and gpt-image models always save generated images because the API returns base64 data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
