## Description:

Deterministic handbook-grounded retrieval and thermocouple computations for reflow profile compliance outputs such as ramp, TAL, peak, feasibility, and selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing engineers and developers use this skill to answer reflow-profile compliance questions from thermocouple, MES, or defect data against handbook-defined regions, windows, and limits. It supports deterministic calculations for ramp rate, time above liquidus, peak temperature, conveyor feasibility, and sensor selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides computation recipes and a scaffold rather than the actual handbook or a complete validated implementation.

Mitigation: Review generated outputs against the current handbook before using them for compliance decisions.

Risk: Incorrect or incomplete handbook limits, thermocouple traces, or MES inputs can produce misleading compliance results.

Mitigation: Confirm extracted limits and input data quality, and avoid claiming pass results when required thermocouple records or valid metric segments are missing.

## Reference(s):

- [Source skill definition](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/reflow-profile-compliance-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code snippets and JSON-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be deterministic, sorted by stable identifiers, rounded to 2 decimal places for floats, and free of NaN or Inf values.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
