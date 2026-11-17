## Description:

Intelligent model routing for OpenClaw. Automatically selects the best model from 8 available models based on task type, content length, and quality requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stpku](https://clawhub.ai/user/stpku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to choose a Bailian model for coding, writing, analysis, multimodal, or long-context tasks based on task type, content length, and quality requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Python helper reads /home/skyswind/.openclaw/openclaw.json when that file exists.

Mitigation: Back up the OpenClaw configuration and validate any JSON changes before following the configuration example.

Risk: The artifact is primarily a Chinese-language model routing helper, which may affect reviewability for teams that do not read Chinese.

Mitigation: Review the source and configuration examples with a qualified Chinese reader or translation workflow before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stpku/skills/stpku-model-router)
- [Publisher Profile](https://clawhub.ai/user/stpku)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text and Markdown with Python API examples, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces model IDs and short selection explanations; the Python helper can read an existing OpenClaw configuration file if present.]

## Skill Version(s):

1.0.1 (source: server release evidence, metadata.json, _meta.json, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
