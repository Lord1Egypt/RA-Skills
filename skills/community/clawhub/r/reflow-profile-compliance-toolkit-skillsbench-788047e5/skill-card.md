## Description:

Deterministic handbook-grounded retrieval and thermocouple computations for reflow profile compliance outputs such as ramp, TAL, peak, feasibility, and selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and manufacturing engineers use this skill to retrieve handbook limits and compute deterministic reflow profile compliance metrics from thermocouple, MES, or defect data. It supports ramp, time-above-liquidus, peak temperature, conveyor feasibility, and sensor-selection analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous handbook limits or multiple applicable constraints could lead to incorrect compliance conclusions.

Mitigation: Review outputs as engineering analysis and apply the stricter documented constraint when multiple limits apply.

Risk: Missing or non-monotonic thermocouple data can make computed metrics incomplete or misleading.

Mitigation: Sort samples deterministically, ignore non-positive time deltas, use null for unavailable metrics, and avoid claiming pass status without valid supporting data.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python code blocks and structured JSON guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sorts identifiers deterministically, rounds numeric outputs to 2 decimals, and uses null for missing or invalid numeric values.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
