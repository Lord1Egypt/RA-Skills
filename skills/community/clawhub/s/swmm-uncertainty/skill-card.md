## Description: <br>
Supports EPA SWMM uncertainty workflows for parameter and rainfall-forcing propagation, ensemble entropy, sensitivity screening, and source-decomposition reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run SWMM uncertainty studies, including fuzzy and Monte Carlo parameter propagation, rainfall ensembles, OAT/Morris/Sobol sensitivity screening, and reviewer-facing uncertainty source summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local analysis outputs and may read or write project run directories during SWMM uncertainty studies. <br>
Mitigation: Run it only against project and run directories you are comfortable letting the tool access, and review generated analysis artifacts before relying on them. <br>
Risk: SWMM execution and related Agentic SWMM dependencies are invoked only when the user chooses workflows that run simulations. <br>
Mitigation: Review the Agentic SWMM environment and dependencies before use, and use dry-run or sampling-only paths when simulation execution is not intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhonghao1995/swmm-uncertainty) <br>
- [Agentic SWMM Project](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown, text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/Markdown analysis artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local run directories containing resolved parameter spaces, sampled parameter sets, trial inputs, uncertainty summaries, entropy records, rainfall ensemble summaries, and source-decomposition reports.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
