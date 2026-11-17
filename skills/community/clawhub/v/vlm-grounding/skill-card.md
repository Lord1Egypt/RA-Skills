## Description:

Use GLM-4.7V multimodal grounding to detect and locate objects, text, UI elements, or regions in images and return bounding box results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qijimrc](https://clawhub.ai/user/qijimrc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route image-grounding requests to a GLM-4.7V model, parse normalized bounding boxes, and produce annotated image-location results for objects, text, UI elements, or regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package bundles a private OpenClaw session transcript.

Mitigation: Remove artifact/ssssss.json before release and audit whether it contains real user, prompt, image, or deployment data.

Risk: The skill instructs users to send images and prompts to a model endpoint over plain HTTP.

Mitigation: Use HTTPS with normal certificate validation and clearly disclose that images and prompts are sent to a model service.

Risk: The skill requires proxy bypass for internal model calls.

Mitigation: Avoid mandatory proxy bypass unless it is approved by the deployment administrator.

Risk: Bounding box coordinates are parsed from model text and may be approximate.

Mitigation: Treat coordinates as estimates unless the skill is updated to require structured grounding results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qijimrc/skills/vlm-grounding)
- [Publisher profile](https://clawhub.ai/user/qijimrc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets and bounding box coordinate examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce normalized bounding boxes and guidance for visualizing boxes on images.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
