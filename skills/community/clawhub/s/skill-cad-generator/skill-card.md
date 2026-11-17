## Description:

Skill Cad Generator helps agents turn CAD and 3D design requests into structured parameters, simple CAD project data, and exportable drawing files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimuge-doudou](https://clawhub.ai/user/zimuge-doudou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, design assistants, and event-production teams can use this skill to draft CAD parameters and generate simple venue, stage, meeting, exhibition, or parametric 3D design outputs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security evidence says the documentation, permissions, and code do not line up safely enough for automatic installation.

Mitigation: Review the skill before installing and use it only in a constrained workspace until the packaged behavior matches the advertised workflow.

Risk: The advertised remote CAD workflow uses an FRP-assisted localhost endpoint and the evidence notes that authentication and retention are not understood.

Mitigation: Avoid proprietary design prompts and require endpoint authentication, data-retention review, and network controls before enabling the remote workflow.

Risk: The artifact can write project and export files, and the security guidance calls out filename validation, overwrite protection, and SVG escaping.

Mitigation: Validate project names and output paths, prevent unintended overwrites, and escape generated SVG text before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zimuge-doudou/skills/skill-cad-generator)

## Skill Output:

**Output Type(s):** [text, json, code, shell commands, configuration, files]

**Output Format:** [JSON parameter objects, command-line text, and generated JSON, DXF, SVG, OBJ, or PNG artifacts depending on the available workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The release evidence describes an FRP-assisted localhost CAD rendering workflow, while the bundled artifact primarily provides stubs and a local DXF/SVG export script.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
