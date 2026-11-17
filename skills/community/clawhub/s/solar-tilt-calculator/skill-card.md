## Description:

Calculate solar radiation on tilted surfaces based on NASA POWER data, user-provided tilt and azimuth angles, and structured Excel inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuepeng1985-web](https://clawhub.ai/user/yuepeng1985-web)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and energy analysts use this skill to calculate monthly mean daily solar radiation on tilted surfaces from NASA POWER-style Excel workbooks and compare tilted-surface results with horizontal-surface radiation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script against user-provided Excel files and writes an Excel report.

Mitigation: Use trusted input workbooks and review the generated output path before execution, especially when no explicit --output value is supplied.

Risk: Solar-radiation results depend on the workbook structure, latitude field, and model assumptions documented by the artifact.

Mitigation: Confirm the input workbook uses the expected NASA POWER-style sheets and columns, then review the generated workbook before relying on results.

## Reference(s):

- [NASA POWER](https://power.larc.nasa.gov)
- [ClawHub skill page](https://clawhub.ai/yuepeng1985-web/skills/solar-tilt-calculator)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated Excel workbook output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese-labeled Excel sheets for basic information, tilted-surface radiation data, and parameter notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
