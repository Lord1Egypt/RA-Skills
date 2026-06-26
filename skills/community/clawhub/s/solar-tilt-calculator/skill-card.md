## Description: <br>
Calculate solar radiation on tilted surfaces based on NASA POWER data with user-defined tilt and azimuth angles, producing structured Excel output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuepeng1985-web](https://clawhub.ai/user/yuepeng1985-web) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and energy analysts use this skill to calculate monthly mean daily radiation on tilted solar surfaces from NASA POWER-derived Excel inputs and compare horizontal versus tilted-surface radiation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a user-selected Excel workbook. <br>
Mitigation: Run it only on Excel files you intend to process. <br>
Risk: The skill writes a calculated output workbook. <br>
Mitigation: Choose an explicit output path and review the generated workbook before using its results. <br>
Risk: The metadata lists curl and pandas although the included script does not appear to use them. <br>
Mitigation: Review environment requirements during installation and avoid granting unnecessary tooling access. <br>


## Reference(s): <br>
- [NASA POWER](https://power.larc.nasa.gov) <br>
- [ClawHub skill page](https://clawhub.ai/yuepeng1985-web/solar-tilt-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [Excel workbook with three sheets, plus a concise text summary of annual radiation, best month, and gain or loss percentage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-provided Excel workbook and writes a calculated output workbook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
