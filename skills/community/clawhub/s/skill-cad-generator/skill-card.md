## Description: <br>
Skill Cad Generator helps agents create CAD and 3D generation parameters, local project files, and rendering handoffs for M4 Pro and Three.js workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimuge-doudou](https://clawhub.ai/user/zimuge-doudou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers and developers use this skill to turn natural-language CAD requests into structured model parameters, project definitions, and exportable DXF/SVG or 3D-rendering handoff files for local design workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe file-writing behavior can overwrite or place project and output files unexpectedly. <br>
Mitigation: Use trusted project names only, run the skill in a sandbox or dedicated workspace, and require path containment, safe filename validation, and overwrite protection before deployment. <br>
Risk: The documentation does not fully match the included implementation and describes unauthenticated local or FRP rendering. <br>
Mitigation: Review the implementation against the documentation, keep any local or FRP renderer private, and add authentication or explicit confirmation before remote rendering. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/zimuge-doudou/skill-cad-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON parameter definitions, Python CAD project files, and DXF/SVG export instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local project JSON, DXF, and SVG files and hand off rendering requests to a configured local renderer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact metadata reports 1.0/1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
