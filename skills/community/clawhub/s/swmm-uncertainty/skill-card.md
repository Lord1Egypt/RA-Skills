## Description:

Parameter and forcing uncertainty propagation and sensitivity analysis for EPA SWMM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and stormwater engineers use this skill to guide agents through EPA SWMM uncertainty workflows, including fuzzy alpha-cut propagation, Monte Carlo sampling, rainfall forcing ensembles, entropy summaries, and OAT, Morris, or Sobol sensitivity analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An output-writing path may escape its intended directory.

Mitigation: Use fresh, controlled run and output directories, and do not pass untrusted node names or paths until the node-name output-path issue is fixed.

Risk: The skill can run batch local SWMM simulations.

Mitigation: Install and execute it only in trusted Agentic SWMM workspaces, keep sample counts modest, and run with --dry-run first where supported.

## Reference(s):

- [Agentic SWMM repository](https://github.com/Zhonghao1995/agentic-swmm-workflow)
- [ClawHub skill page](https://clawhub.ai/zhonghao1995/skills/swmm-uncertainty)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and output file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or describe SWMM run directories, JSON summaries, CSV rainfall realisations, plots, and uncertainty source reports when the referenced local scripts are executed.]

## Skill Version(s):

0.7.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
