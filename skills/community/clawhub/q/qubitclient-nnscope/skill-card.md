## Description:

NNScope helps agents document and use QubitClient APIs for neural-network based quantum spectrum peak detection, curve segmentation, parameter extraction, batch processing, and visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaqiangsun](https://clawhub.ai/user/yaqiangsun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantum computing engineers use this skill to call QubitClient NNScope workflows for S21 peak detection, spectrum region analysis, 2D curve segmentation, S21-vs-flux fitting, power-shift segmentation, and result visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples load local spectrum data and save generated visualization files, so an unintended path could read or write the wrong data.

Mitigation: Confirm input data directories and output paths before running examples.

Risk: The client.request workflow may process provided spectrum data through the qubitclient backend.

Mitigation: Review data sensitivity and backend handling expectations before sending spectrum data.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/yaqiangsun/QubitClient/tree/main/skills/qubitclient-nnscope)
- [ClawHub skill page](https://clawhub.ai/yaqiangsun/skills/qubitclient-nnscope)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with Python code examples and JSON-shaped result schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API task names, input data shapes, output schemas, confidence filtering guidance, and visualization examples.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
