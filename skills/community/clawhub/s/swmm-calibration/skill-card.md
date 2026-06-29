## Description: <br>
Calibration and validation scaffold for EPA SWMM that helps agents compare simulated and observed hydrographs, rank calibration candidates, run bounded searches, and produce SCE-UA or DREAM-ZS calibration outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to calibrate and validate EPA SWMM models against observed flow, depth, head, or volume data. It supports candidate scoring, bounded search, SCE-UA point-estimate calibration, DREAM-ZS posterior calibration, and human-reviewed candidate handoff before canonical INP changes are accepted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local calibration jobs can create many trial files and candidate patch artifacts. <br>
Mitigation: Review output directories and patch maps before running, and inspect generated candidate artifacts before relying on them. <br>
Risk: Calibration results can be misleading if observed data, calibration targets, or patch maps are incorrect. <br>
Mitigation: Use observed data for calibration and validation, confirm the target series and patch map, and review generated summaries before accepting any model change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhonghao1995/swmm-calibration) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files, Markdown reports] <br>
**Output Format:** [Markdown guidance with shell command examples and generated JSON, CSV, and Markdown calibration artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calibration outputs can include summaries, rankings, best-parameter files, convergence traces, candidate INP patches, and posterior artifacts depending on the selected strategy.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
