## Description:

Publication-grade plotting for SWMM rainfall-runoff time-series figures, producing paired rainfall and node or link flow figures from SWMM .inp and .out files with strict SI-unit publication styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and stormwater engineers use this skill after a SWMM run has produced .inp and .out files to inspect rainfall-runoff behavior, compare rainfall with node or link flow, and generate publication-style PNG figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a separate Agentic SWMM toolchain and runtime that are not bundled or audited in this release evidence.

Mitigation: Review and install the external Agentic SWMM project and its dependencies before deploying this skill.

Risk: A wrong rainfall series, node, link, attribute, or time window can produce a misleading hydrology figure.

Mitigation: Inspect available plot options and ask the user to choose the entity, attribute, and window before plotting.

Risk: The skill reads local SWMM model and run files and writes PNG outputs.

Mitigation: Install it only where the agent should access the intended run directories, and review output paths before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhonghao1995/skills/swmm-plot)
- [Agentic SWMM project](https://github.com/Zhonghao1995/agentic-swmm-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Files]

**Output Format:** [Markdown guidance plus PNG plot or network-map files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads SWMM .inp and .out inputs, writes PNG figures, and supports optional focus-day or HH:MM window cropping.]

## Skill Version(s):

0.7.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
