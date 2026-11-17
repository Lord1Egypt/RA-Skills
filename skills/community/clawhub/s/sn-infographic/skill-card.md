## Description:

Generates professional infographics with various layout types and visual styles, analyzes content, recommends layout and style, and generates publication-ready infographics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to turn prompts, structured content, or source material into infographic images with selected layouts, styles, prompt expansion, and optional quality ranking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Infographic prompts and generated images may be sent through external SenseNova provider tools.

Mitigation: Avoid sensitive or confidential source material unless the provider dependency is acceptable in the deployment environment.

Risk: Intermediate prompts and generated images are written temporarily under /tmp.

Mitigation: Use environments where local temporary-file handling matches the user's data retention and access requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-infographic)
- [analysis-framework.md](references/analysis-framework.md)
- [evaluation-standard.md](references/evaluation-standard.md)
- [layout-style-selection.md](references/layout-style-selection.md)
- [runtime-parameters.md](references/runtime-parameters.md)
- [structured-content-template.md](references/structured-content-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [One-line text summary plus generated image output in friendly mode, or Markdown-style quality ranking with timing details and images in verbose mode; worker results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports friendly and verbose output modes, one to eight generation rounds, optional prompt expansion, inferred aspect ratio, and 2k or explicitly requested 4k image size when supported by the provider.]

## Skill Version(s):

2026.9.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
