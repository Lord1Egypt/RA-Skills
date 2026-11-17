## Description:

Analyzes images with SiliconFlow's Qwen2.5-VL model for image question answering, object recognition, scene description, and image-content understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomlee2013](https://clawhub.ai/user/tomlee2013)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send a local image and prompt to SiliconFlow's Qwen2.5-VL service for image description, object recognition, scene analysis, or image question answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images and prompt text are sent to SiliconFlow for processing.

Mitigation: Avoid sensitive, regulated, or confidential images and prompts unless the provider's data-handling terms have been reviewed and approved for the use case.

## Reference(s):

- [SiliconFlow chat completions API endpoint](https://api.siliconflow.cn/v1/chat/completions)
- [ClawHub skill page](https://clawhub.ai/tomlee2013/skills/siliconflow-qwen-vision)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text response or text file, with Markdown guidance and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls SiliconFlow with a user-supplied image and prompt; default max_tokens is 2048]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
