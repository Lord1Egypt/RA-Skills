## Description:

Turn customer background, current problems, and target requirements into a consulting-grade solution narrative and PPT-ready JSON outline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renqiukai](https://clawhub.ai/user/renqiukai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, consultants, and pre-sales teams use this skill to turn customer background, current problems, target requirements, and constraints into a structured solution narrative and PPT-ready JSON outline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks may carry an inaccurate hardcoded author value.

Mitigation: Replace or confirm the cover author before using the JSON or generated PPTX.

Risk: The skill processes local business files and can trigger PPT conversion commands that write local outputs.

Mitigation: Use explicit input files, avoid sensitive documents unless intended, and approve the conversion command and output path before execution.

Risk: Incomplete customer inputs can lead to assumptions or misleading consulting guidance.

Mitigation: Review the generated assumptions, facts, and recommendations before sharing with stakeholders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renqiukai/skills/solution-expert)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON for a consulting-style presentation outline; optional PPTX file generation when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs must use the skill's fixed JSON schema and may include local file names for generated JSON and PPTX artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
