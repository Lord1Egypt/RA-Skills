## Description:

Qubitclient Scope documents QubitScopeClient APIs for numerical quantum-experiment curve fitting, parameter extraction, batch processing, and matplotlib/plotly visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaqiangsun](https://clawhub.ai/user/yaqiangsun)

### License/Terms of Use:

GPL-3.0

## Use Case:

Developers and quantum engineers use this skill to call QubitScopeClient for S21 peak detection, T1/T2 fitting, Rabi and Ramsey analysis, DRAG calibration, randomized benchmarking, and related numerical quantum-experiment analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents API calls but does not ship or review the underlying qubitclient implementation.

Mitigation: Review and scan the underlying qubitclient package before using it with sensitive experimental data.

Risk: Numerical curve fitting can produce misleading parameter estimates when input schemas, units, fit assumptions, or confidence thresholds are inappropriate for the experiment.

Mitigation: Validate input shapes and units, inspect status values, R2 or confidence outputs, and review generated plots before relying on extracted quantum parameters.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/yaqiangsun/QubitClient/tree/main/skills/qubitclient-scope)
- [ClawHub skill page](https://clawhub.ai/yaqiangsun/skills/qubitclient-scope)
- [Publisher profile](https://clawhub.ai/user/yaqiangsun)

## Skill Output:

**Output Type(s):** [guidance, code, API calls, configuration]

**Output Format:** [Markdown with Python and JSON code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents structured input dictionaries, task names, result schemas, confidence scores, fit parameters, status values, and visualization calls.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
