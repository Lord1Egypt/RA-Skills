## Description: <br>
Quantifies plant wilting from full-plant images or videos and returns severity, likely underwatering or overwatering cause, guidance, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze plant images, videos, or URLs for wilting severity, possible water-stress cause, intervention direction, and historical report access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant photos, videos, or supplied URLs may be processed by the publisher's cloud service. <br>
Mitigation: Avoid sending sensitive indoor footage or private/internal URLs unless that processing is acceptable. <br>
Risk: The skill can silently create or reuse an identity and link reports to that identity. <br>
Mitigation: Review identity handling before installation and use a controlled workspace or account boundary for testing. <br>
Risk: The skill may persist user records and authentication tokens locally for report history access. <br>
Mitigation: Review local workspace data files and token storage before deployment and clean them according to the environment's retention policy. <br>


## Reference(s): <br>
- [Plant Wilting Quantification API Documentation](references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-plant-wilting-quantification-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON text with report links and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call publisher cloud APIs for analysis and historical report retrieval.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
