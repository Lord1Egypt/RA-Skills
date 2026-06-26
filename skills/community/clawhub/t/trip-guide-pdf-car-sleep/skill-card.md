## Description: <br>
Research, plan, revise, and deliver car-sleep travel guides as HTML/PDF with verified overnight parking, charging, toilet access, next-morning route anchors, and formal copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allensu0314](https://clawhub.ai/user/allensu0314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and trip-planning agents use this skill to research car-sleep trips and create polished HTML/PDF guides. It focuses on verified overnight parking, charging, toilet access, route timing, screenshots, and fallback planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel, parking, charging, toilet, and overnight permission information can be stale or incomplete. <br>
Mitigation: Verify hard data against current map, official, or structured sources before presenting guide recommendations, and label unconfirmed overnight permission as a candidate rather than allowed. <br>
Risk: Guide revisions can overwrite earlier HTML/PDF outputs or make filenames ambiguous. <br>
Mitigation: Confirm desired filenames and output locations when revising guides, and use scenario-specific filenames for each variant. <br>


## Reference(s): <br>
- [Source Selection for Car-Sleep Guides](references/source-selection.md) <br>
- [QA Checklist for Car-Sleep Guides](references/qa-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/allensu0314/trip-guide-pdf-car-sleep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with HTML/PDF guide files and supporting screenshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local screenshots plus HTML/PDF guide files; confirm filenames and destinations when revising guides so prior versions are not accidentally replaced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
