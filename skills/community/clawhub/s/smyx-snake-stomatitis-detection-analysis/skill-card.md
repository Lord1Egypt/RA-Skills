## Description: <br>
Analyzes snake mouth images or videos for visual signs associated with stomatitis risk and returns structured oral-health observations, risk levels, suggested next steps, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Snake keepers, reptile clinics, breeding facilities, and agent operators use this skill to submit mouth images or videos of snakes and receive a visual stomatitis-risk assessment with non-treatment handling guidance, report output, and history lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files or provided URLs are sent to a vendor cloud service for analysis and history lookup. <br>
Mitigation: Install and use the skill only when external processing is acceptable, avoid submitting sensitive media, and review service data-handling expectations before use. <br>
Risk: The skill silently creates or reuses local identity state and stores service tokens. <br>
Mitigation: Review local state and token storage policies before installation, isolate the workspace when needed, and remove stored credentials if persistent identity state is not acceptable. <br>
Risk: Visual stomatitis-risk output is not a veterinary diagnosis and can be unreliable when image quality is poor or context such as shedding, feeding, species, temperature, or humidity is missing. <br>
Mitigation: Use the output as triage guidance only, require clear mouth images and relevant context, and consult a reptile veterinarian for suspected infection or treatment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-snake-stomatitis-detection-analysis) <br>
- [Skill API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON analysis output and Markdown summaries or history tables produced through the bundled Python command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include visual observation fields, risk levels, recommended non-treatment actions, disclaimers, report links, and historical report tables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
