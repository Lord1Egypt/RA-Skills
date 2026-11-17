## Description:

Use GLM-4.7V's multimodal grounding capability to detect and locate objects, text, UI elements, or regions in images and return bounding-box coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qijimrc](https://clawhub.ai/user/qijimrc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask an agent to identify visual targets in images, parse bounding-box coordinates, and produce annotated outputs for image-grounding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a sensitive runtime trace that may contain captured headers, user content, or image-derived data.

Mitigation: Remove the raw trace file from the release and redact captured headers, user content, and image data before distribution.

Risk: The skill instructs users to submit images to a model API and includes plaintext internal HTTP endpoint examples.

Mitigation: Disclose that images are sent to a model service and prefer HTTPS endpoints with endpoint authentication.

Risk: The artifact instructs users to bypass proxies with NO_PROXY for model calls.

Mitigation: Avoid process-wide proxy bypasses; scope network exceptions narrowly and review them before installation.

Risk: Security evidence notes ambiguity between true model-grounded boxes and approximate visual estimates.

Mitigation: Clarify whether coordinates are model-grounded outputs or approximate estimates, and require user review before relying on localization results.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code examples and bounding-box coordinate output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounding boxes are described as 0-1000 normalized coordinates that can be converted to pixel coordinates for visualization.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
