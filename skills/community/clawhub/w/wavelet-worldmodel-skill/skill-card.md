## Description:

Generates a world model representation from state inputs using discrete wavelet transforms (DWT) to capture multi-resolution temporal and spatial features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aadipapp](https://clawhub.ai/user/aadipapp)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill with OpenClaw agents to generate compact multi-resolution representations of high-dimensional sequential state data for robotic control, continuous state tracking, or downstream predictive models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned NumPy and PyWavelets dependencies can create supply-chain or reproducibility risk when running the helper script.

Mitigation: Run the helper in a virtual environment and pin trusted NumPy and PyWavelets versions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aadipapp/skills/wavelet-worldmodel-skill)
- [Publisher profile](https://clawhub.ai/user/aadipapp)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with command names and Python script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a compressed temporal state representation; helper execution depends on local NumPy and PyWavelets installation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
