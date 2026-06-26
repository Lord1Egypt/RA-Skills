## Description: <br>
Deterministic handbook-grounded retrieval and thermocouple computations for reflow profile compliance outputs such as ramp, TAL, peak, feasibility, and selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and process engineers use this skill to extract reflow-profile limits from handbook material and compute deterministic run-level compliance metrics from thermocouple, MES, or defect data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compliance conclusions may be misleading if handbook limits, liquidus thresholds, or thermocouple inputs are incomplete or stale. <br>
Mitigation: Verify the handbook-derived configuration and source data before using generated metrics for process decisions. <br>
Risk: Generated code or shell guidance may need local review before execution. <br>
Mitigation: Review proposed commands and code snippets in the target environment before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/reflow-profile-compliance-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/wu-uk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and structured configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sorts identifiers deterministically, rounds numeric values to two decimals, avoids NaN/Inf JSON values, and uses interpolation for threshold timing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
