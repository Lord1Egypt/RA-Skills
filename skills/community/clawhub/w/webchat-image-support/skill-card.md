## Description:

Enables agents to detect and analyze images sent via WebChat or other channels using vision-capable models or fallback media processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[styoha](https://clawhub.ai/user/styoha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let OpenClaw agents understand images sent through WebChat and other supported chat channels, including screenshots, photos, and multiple images in one message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images sent to agents may be analyzed by the configured vision model provider or OpenClaw media pipeline.

Mitigation: Use only with providers and retention settings acceptable for the image content, and avoid sensitive screenshots, documents, or photos unless approved.

## Reference(s):

- [OpenClaw docs](https://openclaw.dev)
- [Gateway fix: GitHub #57064](https://github.com/openclaw/openclaw/issues/57064)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance and natural-language image analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image descriptions, configuration examples, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
