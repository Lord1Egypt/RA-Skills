## Description:

Runs a SYRI-based genome collinearity and structural variation workflow, including chromosome preparation, minimap2 alignment, SYRI analysis, and plotsr visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjw065](https://clawhub.ai/user/wangjw065)

### License/Terms of Use:

MIT-0

## Use Case:

Bioinformatics researchers and genome analysis engineers use this skill to prepare chromosome inputs, align genomes, detect structural variation with SYRI, and visualize collinearity with plotsr.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned bioinformatics software installation can change behavior across environments or introduce supply-chain exposure.

Mitigation: Install in a dedicated Conda or virtual environment and pin package versions or reviewed commits before operational use.

Risk: High-thread alignment jobs and large SAM outputs can exhaust shared CPU, memory, or disk resources.

Mitigation: Review thread counts, storage availability, and job scheduling limits before launching minimap2 or SYRI runs.

Risk: Running installation and analysis commands with elevated privileges can increase the impact of dependency or command mistakes.

Mitigation: Avoid running the workflow as root and use a least-privilege project environment.

## Reference(s):

- [SYRI 共线性分析 ClawHub release](https://clawhub.ai/wangjw065/skills/syri-analysis)
- [minimap2 source repository](https://github.com/lh3/minimap2.git)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides workflow steps, command examples, configuration notes, troubleshooting guidance, and expected SYRI output files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
