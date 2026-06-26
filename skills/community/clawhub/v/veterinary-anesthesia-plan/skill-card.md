## Description: <br>
Use this skill when a veterinarian, vet technician, or resident needs to build a patient-specific anesthesia plan for a scheduled procedure, producing a draft plan with weight-based dose ranges, monitoring and recovery protocols, an emergency-drug worksheet, and an equipment checklist for licensed-veterinarian review before any drug is drawn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Veterinary teams use this skill to draft patient-specific anesthesia plans, monitoring and recovery protocols, emergency-drug worksheets, and equipment checklists for clinician review. It is intended to support, not replace, licensed veterinarian judgment and sign-off. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft dose ranges or protocol suggestions could be incorrect, incomplete, or inconsistent with the clinic's current formulary. <br>
Mitigation: Verify all dose ranges against the current formulary and require attending veterinarian review and sign-off before any drug is drawn or administered. <br>
Risk: Dose calculations based on an estimated or outdated weight could misstate patient-specific totals and volumes. <br>
Mitigation: Use the current day-of measured weight and recalculate all dose totals before administration. <br>
Risk: Prompts may contain unnecessary owner personal information or sensitive clinical details. <br>
Mitigation: Keep owner personal information out of prompts and include only the clinical details needed for the anesthesia draft. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown draft plan with tables, worksheets, checklists, and sign-off items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only clinical support requiring licensed veterinarian review before use] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
