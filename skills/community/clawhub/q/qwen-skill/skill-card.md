## Description: <br>
Generate and edit images with Qwen Image via the DashScope API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huiya-code](https://clawhub.ai/user/huiya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate new images, edit a single image, or fuse up to three input images through DashScope-backed Qwen Image models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to DashScope using the configured API key. <br>
Mitigation: Use only with data approved for DashScope processing and protect the API key in the runtime environment. <br>
Risk: A configured media base URL can make generated outputs reachable outside the local machine. <br>
Mitigation: Keep OPENCLAW_MEDIA_BASE_URL empty unless public sharing is intended, and restrict access to any served media directory. <br>
Risk: Dependency ranges are not pinned to exact audited versions. <br>
Mitigation: Pin and audit dependency versions before production deployment. <br>


## Reference(s): <br>
- [Qwen Skill on ClawHub](https://clawhub.ai/huiya-code/qwen-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [One-line MEDIA reference with generated image files and optional preview HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; generated images are saved locally and may be copied to a configured media directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
