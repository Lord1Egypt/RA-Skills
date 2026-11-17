## Description:

Use when a selective defect needs IS/IS-NOT difference analysis or a consequential option choice needs must/want weighting and adverse-consequence comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to structure defect diagnosis or consequential option selection with Kepner-Tregoe problem and decision analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The method may be over-applied to trivial choices, obvious causes, or tasks without a meaningful IS-NOT contrast.

Mitigation: Use the skill's When NOT to Use and over-application guard before building a full matrix.

Risk: A candidate cause or selected option may look stronger than it is if contradictory boundary evidence, failed MUST criteria, or adverse consequences are ignored.

Mitigation: Reject causes that do not explain both IS and IS-NOT; eliminate options that fail MUSTs; compare adverse consequences and sensitivity before selecting.

Risk: Unclear criteria or hidden scoring assumptions can make the resulting decision artifact misleading.

Mitigation: Make MUST criteria operational, assign WANT weights before scoring, and state assumptions or reversal conditions in the output.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown decision artifact with mode-specific matrices and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs either a Problem Analysis artifact or a Decision Analysis artifact, depending on the selected mode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
