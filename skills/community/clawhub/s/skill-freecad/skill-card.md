## Description: <br>
Create or modify 3D CAD models in FreeCAD using parametric JSON operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninja7v](https://clawhub.ai/user/ninja7v) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and CAD users use this skill to convert natural-language CAD requests into structured FreeCAD operations for creating primitives, transforms, booleans, arrays, modifiers, profile operations, exports, and document inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or updates model.FCStd, model.step, and requested export files in the active workspace. <br>
Mitigation: Install and run it in a dedicated project folder and keep backups when same-named CAD files matter. <br>
Risk: A custom FREECAD_PATH can direct the engine to a local FreeCAD installation or directory. <br>
Mitigation: Set FREECAD_PATH only to a trusted FreeCAD installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ninja7v/skill-freecad) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files] <br>
**Output Format:** [Structured JSON commands passed to a Python engine, JSON status output, and CAD files such as FCStd, STEP, STL, or BREP] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local CAD files in the active workspace, including model.FCStd and model.step by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact/skill.json says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
