## Description:

Guide for setting up a stable VMamba environment and resolving common CUDA, PyTorch, MMCV, and compilation errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangkaiqi2005](https://clawhub.ai/user/jiangkaiqi2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure a stable VMamba Python environment and troubleshoot CUDA, PyTorch, MMCV, selective_scan compilation, MKL, NumPy, and OpenCV setup failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation and build commands can alter the active Python environment or system state if run in the wrong context.

Mitigation: Install only in a fresh VMamba conda environment, confirm the environment is active, and avoid root or sudo for pip and build steps.

Risk: Compiling selective_scan runs native build steps from the local VMamba checkout.

Mitigation: Build selective_scan only from a trusted VMamba repository checkout.

## Reference(s):

- [VMamba repository](https://github.com/MzeroMiko/VMamba)
- [ClawHub skill page](https://clawhub.ai/jiangkaiqi2005/skills/vmamba-env-doctor)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides environment setup steps, version recommendations, and troubleshooting guidance for VMamba.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
