## Description:

Top-level orchestration skill for agentic SWMM modelling. Use when an agent needs one entrypoint that decides which module tools to run, in what order, and when to stop, for example to build, run, QA, and optionally calibrate a SWMM case from prepared or partially prepared inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate end-to-end SWMM modeling workflows, including input routing, model build, run, QA, optional plotting, calibration, uncertainty analysis, LID scenarios, and audit handoff. It is intended as the top-level orchestration entrypoint when a user has prepared or partially prepared SWMM inputs and needs the agent to choose the next module safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run external Agentic SWMM tooling and MCP server dependencies.

Mitigation: Install and run it only in a constrained project environment, preferably a container or unprivileged account, after reviewing the external repository, package manifests, lockfiles, and install script.

Risk: The workflow can persist audit notes outside the run directory through the default Obsidian export behavior.

Mitigation: Disable Obsidian export unless copying run evidence to the named local vault is explicitly intended.

## Reference(s):

- [Agentic SWMM project repository](https://github.com/Zhonghao1995/agentic-swmm-workflow)
- [ClawHub skill page](https://clawhub.ai/zhonghao1995/skills/swmm-end-to-end)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with shell commands, file paths, run manifests, QA summaries, and audit artifact descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates MCP tool calls and repository scripts; expected artifacts include SWMM input, report, output, QA JSON, manifests, plots when requested, calibration summaries when requested, and audit notes.]

## Skill Version(s):

0.7.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
