## Description: <br>
Analyzes post-feeding aquarium or aquaculture videos to estimate fish gathering, feeding intensity, residual feed, and a 0-100 feeding activity score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aquarium owners, aquaculture operators, public aquarium staff, and developers use the skill to submit feeding-window videos or query historical reports so an agent can return structured feeding activity assessments and recommended observation or water-quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aquarium videos or video URLs and an open-id may be sent to the LifeEmergence/SMYX cloud service. <br>
Mitigation: Use only non-sensitive footage, avoid videos containing people or private spaces, and use a dedicated non-sensitive identifier where possible. <br>
Risk: The skill handles silent account login or registration, local token storage, and bundled API credentials. <br>
Mitigation: Review the workspace for stored tokens and bundled credentials before deployment, and install only when that account and credential behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-fish-feeding-activity-analysis) <br>
- [API interface documentation](artifact/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown or JSON reports with feeding activity scores, scene labels, alert levels, recommended actions, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an output file when the optional --output argument is used.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter states 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
