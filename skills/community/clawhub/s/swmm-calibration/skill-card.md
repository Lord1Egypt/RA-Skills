## Description:

Calibration and validation scaffold for EPA SWMM that helps agents compare simulated and observed hydrographs, evaluate candidate parameter sets, and run bounded search, SCE-UA, or DREAM-ZS calibration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and stormwater modelers use this skill to calibrate or validate EPA SWMM models against observed flow data, rank candidate parameters, and produce audit artifacts for review before model changes are accepted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calibration artifacts may be written outside the intended run directory when parameter-set JSON or validation trial names contain unsafe path components.

Mitigation: Run the skill with minimal filesystem privileges in a restricted workspace, trust or pre-validate calibration inputs, reject trial names containing path separators, absolute paths, '.', or '..', and review generated candidate artifacts before accepting INP changes.

Risk: Calibration results can be misleading when observed data, patch maps, objectives, or search bounds are inappropriate for the modeled event.

Mitigation: Use observed data as the calibration boundary, keep patch maps explicit, inspect KGE decomposition and secondary metrics, and require human review before promoting candidate INP patches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhonghao1995/skills/swmm-calibration)
- [Agentic SWMM project](https://github.com/Zhonghao1995/agentic-swmm-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, CSV, PNG, and INP patch artifacts produced by the calibration scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces rankings, best-parameter JSON, calibration summaries, candidate handoff artifacts, convergence traces, and optional posterior diagnostics.]

## Skill Version(s):

0.7.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
