## Description: <br>
Converts de-identified nursing shift notes into a draft SBAR handoff packet for shift change, intra-facility transfer, provider escalation, or charge-nurse rounding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Nurses, charge nurses, and clinical educators use this skill to turn de-identified raw shift notes into a structured SBAR draft with priority concerns, read-back checklist, and unresolved items for licensed-nurse review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Protected health information or other patient identifiers could be pasted into the conversation. <br>
Mitigation: Use only de-identified notes and stop if identifiers appear; the skill prompts for de-identification before accepting clinical content. <br>
Risk: A draft handoff could contain omissions or transcription errors if used without review. <br>
Mitigation: Require a licensed nurse to verify every line against the chart and patient before verbal or written handoff. <br>
Risk: Users could mistake the draft for clinical advice or a clinical decision. <br>
Mitigation: Keep the output framed as a draft communication aid and avoid medication dosing, diagnoses, treatment recommendations, or lab interpretation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/sbar-handoff-drafter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown SBAR handoff packet with checklist and unresolved-information list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft output requires licensed-nurse review and should be based only on de-identified patient information.] <br>

## Skill Version(s): <br>
0.1.2 (source: changelog, released 2026-05-28; server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
