## Description:

Real-time quantum measurement control guidance for qubit spectroscopy, calibration, coherence measurement, readout optimization, and spectrum acquisition workflows using the QubitClient MCP control interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaqiangsun](https://clawhub.ai/user/yaqiangsun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantum-control engineers use this skill to guide an agent in generating Python and MCP control calls for qubit measurement, calibration, spectroscopy, and readout workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-generated measurement parameters can initiate calibration or acquisition tasks against real qubit-control hardware.

Mitigation: Review generated measurement parameters before running them against real hardware.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yaqiangsun/skills/qubitclient-control)
- [Server-resolved GitHub Source](https://github.com/yaqiangsun/QubitClient/tree/main/skills/qubitclient-control)
- [Publisher Profile](https://clawhub.ai/user/yaqiangsun)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, MCP API-call parameters, and result-shape examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers measurement task names, common parameters, task-specific examples, and review guidance before hardware execution.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
