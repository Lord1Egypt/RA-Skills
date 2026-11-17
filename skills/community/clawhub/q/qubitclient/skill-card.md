## Description:

Unified quantum calibration analysis package. Aggregates curve fitting and parameter extraction, neural network spectrum analysis, LLM-based calibration review, and MCP-based real-time measurement control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaqiangsun](https://clawhub.ai/user/yaqiangsun)

### License/Terms of Use:

GPL-3.0

## Use Case:

Developers and quantum calibration engineers use this skill to install and configure qubitclient, then work with numerical fitting, neural network spectrum analysis, LLM-based calibration review, and real-time measurement control workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides installation and configuration of software that can control live measurements and update parameters.

Mitigation: Require human approval and lab-specific safety limits before live measurement control or parameter updates.

Risk: The configuration file can contain API keys and license tokens.

Mitigation: Keep qubitclient.json out of source control, restrict file permissions, and prefer secret managers or environment variables.

Risk: Unverified packages or exposed endpoints could create security or operational risk.

Mitigation: Use an isolated virtual environment, pin and verify package versions, and prefer HTTPS or strictly local loopback endpoints.

## Reference(s):

- [Server-resolved source provenance](https://github.com/yaqiangsun/QubitClient/tree/main/skills/qubitclient)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with bash, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include configuration details for API keys, service endpoints, model names, and live measurement control clients.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
