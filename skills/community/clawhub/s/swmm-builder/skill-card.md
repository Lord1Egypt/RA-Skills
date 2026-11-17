## Description:

Assemble runnable SWMM INP and manifest artifacts from subcatchment geometry/attributes, merged parameter JSON, network JSON, and climate references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assemble auditable SWMM model input files and source manifests from upstream hydrology, network, parameter, and climate artifacts for downstream simulation or calibration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SWMM INP files can be altered by crafted input strings because some emitted text fields are not safely constrained for the target format.

Mitigation: Use the skill in a constrained workspace, choose output paths deliberately, and treat generated INP files from third-party inputs as untrusted until target-format string validation is added.

Risk: The release security verdict is suspicious for workflows that may process untrusted model inputs.

Mitigation: Review the skill before installation or deployment and scan generated artifacts before using them in downstream SWMM workflows.

## Reference(s):

- [Swmm Builder ClawHub Skill Page](https://clawhub.ai/zhonghao1995/skills/swmm-builder)
- [Agentic SWMM Project](https://github.com/Zhonghao1995/agentic-swmm-workflow)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [SWMM INP text, JSON manifests, and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic file artifacts from explicit local input paths and reports validation diagnostics for critical SWMM sections.]

## Skill Version(s):

0.7.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
