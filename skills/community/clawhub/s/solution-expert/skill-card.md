## Description: <br>
Turns customer background, problems, and target requirements into consulting-grade solution narratives and PPT-ready JSON outlines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renqiukai](https://clawhub.ai/user/renqiukai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external consultants, and developers use this skill to convert customer context, current problems, target requirements, and constraints into structured solution narratives or PPT-ready JSON for proposals, pre-sales materials, and project reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PowerPoint export depends on local converter and template files that are referenced by the skill but not included in the package. <br>
Mitigation: Verify that the local Python generator and PowerPoint template are trusted before running PPT export. <br>
Risk: Generated proposal content can include inferred assumptions or business judgments that may be incomplete or misleading. <br>
Mitigation: Review the generated JSON, assumptions, and conclusions against source materials before sharing or converting to slides. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/renqiukai/solution-expert) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON object matching the skill's PPT outline schema; optional PPTX file generation through local workspace tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs JSON only for deck outlines; may write aligned .json and .pptx files when the user asks for PowerPoint generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
