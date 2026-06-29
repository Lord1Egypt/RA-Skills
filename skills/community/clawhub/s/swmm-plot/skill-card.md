## Description: <br>
Publication-grade plotting for SWMM rainfall-runoff time-series figures from SWMM .inp and .out files, with paired inverted rainfall and node or link flow panels using SI units and publication styling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after a SWMM run to inspect rainfall versus flow behavior and generate publication-ready PNG figures for selected nodes, links, or network layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plotting scripts read local SWMM model and run files selected by the user. <br>
Mitigation: Point the skill only at intended run directories and model outputs from the Agentic SWMM/SWMM plotting toolchain. <br>
Risk: The scripts create parent directories and write PNG files at requested output paths. <br>
Mitigation: Review output paths before invocation to avoid overwriting or writing figures in unintended locations. <br>
Risk: Plot conclusions can be misleading if placeholder or incorrect rainfall series, node, link, or time-window inputs are used. <br>
Mitigation: Inspect available plot options first and select real rainfall series, entity identifiers, attributes, and time windows before rendering. <br>


## Reference(s): <br>
- [Agentic SWMM workflow](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>
- [Swmm Plot on ClawHub](https://clawhub.ai/zhonghao1995/swmm-plot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance and PNG figure files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces paired rainfall-flow plots and network layout PNGs from local SWMM model and run files.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
