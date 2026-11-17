## Description:

Analyzes images with Alibaba Cloud DashScope Qwen Vision for visual understanding, OCR, chart analysis, and visual question answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perchouli](https://clawhub.ai/user/perchouli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send supported image files and prompts to DashScope Qwen Vision for image description, OCR, chart interpretation, and visual question answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DashScope API keys may be exposed when passed directly on the command line.

Mitigation: Prefer secure OpenClaw configuration or DASHSCOPE_API_KEY, and avoid placing real keys in shell history or shared logs.

Risk: Images and prompts are uploaded to Alibaba Cloud DashScope for analysis.

Mitigation: Do not submit confidential screenshots, identity documents, faces, source code, or business images unless organizational policy approves that cloud processing.

Risk: The release text describes video analysis, while the implementation analyzes images and can only support video through supplied frames.

Mitigation: Use the skill for image or extracted-frame workflows, and confirm any video workflow before relying on it.

## Reference(s):

- [Qwen Vision skill page](https://clawhub.ai/perchouli/skills/qwen-vision)
- [DashScope homepage](https://dashscope.aliyuncs.com/)
- [DashScope console](https://dashscope.console.aliyun.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text responses with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a DashScope API key; supported image formats include JPG, JPEG, PNG, GIF, WebP, and BMP.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
