## Description:

Zai Vision helps agents analyze images and short videos with Z.AI's GLM-4.6V model for OCR, UI analysis, diagram interpretation, chart reading, error diagnosis, and scene description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twolfe1991-cloud](https://clawhub.ai/user/twolfe1991-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Zai Vision to run image and video analysis workflows, including OCR, UI review, diagram and chart interpretation, screenshot-based error diagnosis, and short video scene description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images or videos may contain confidential, credential, regulated, or private content that is sent to Z.AI for processing.

Mitigation: Use the skill only with content your organization permits sending to Z.AI, and avoid confidential screenshots, secrets, regulated data, and private videos unless approved.

Risk: The zai-sdk dependency can change behavior or introduce dependency risk if installed without review.

Mitigation: Install the SDK in a virtual environment and pin a reviewed version before production use.

Risk: Large video files may have limited analysis quality.

Mitigation: Use short clips, compress large videos, or split them before analysis; the artifact recommends clips up to 8 MB.

Risk: OCR, UI analysis, chart interpretation, and error diagnosis outputs can be incomplete or incorrect.

Mitigation: Review model results before using them for decisions, code changes, or operational guidance.

## Reference(s):

- [Z.AI Vision API Reference](references/API.md)
- [ClawHub release page](https://clawhub.ai/twolfe1991-cloud/skills/zai-vision)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from Python scripts, with Markdown guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZAI_API_KEY; video analysis is recommended for clips up to 8 MB; default maximum response length is 2000 tokens.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
