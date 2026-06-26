## Description: <br>
Simulate standardized patient encounters for medical training, supporting OSCE-style history-taking practice, communication skills rehearsal, and educational debriefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Medical educators, learners, and training facilitators use this skill to rehearse standardized patient encounters, practice clinical interviewing, and prepare debriefing notes for OSCE-style education. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Simulated patient responses could be mistaken for real clinical advice. <br>
Mitigation: Use outputs only as training artifacts; keep the skill's education-only boundary, real-care exclusions, and faculty-supervision expectations visible in downstream use. <br>
Risk: Unsupported scenarios could create misleading certainty if treated as executed simulations. <br>
Mitigation: Use the packaged simulator only for supported scenarios and provide a manual teaching scaffold when a requested scenario is unsupported or execution fails. <br>
Risk: Unpinned requirements entries may create avoidable dependency ambiguity in stricter environments. <br>
Mitigation: Pin or remove the requirements entries before installation where dependency provenance and reproducibility controls are required. <br>


## Reference(s): <br>
- [Virtual Patient Roleplay References](references/references.md) <br>
- [Audit Reference](references/audit-reference.md) <br>
- [Guidelines](references/guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell commands for local simulator checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Educational simulation output; not clinical advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
